import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import production_preflight  # noqa: E402

GUIDE = ROOT / "skills/pilot-before-scale/delegated-run.md"


def example_manifest() -> dict:
    """The fictional manifest shown in the delegated-run guide, so the guide and the tool cannot drift apart."""
    block = re.search(r"```json\n(.*?)```", GUIDE.read_text(encoding="utf-8"), re.S)
    return json.loads(block[1])


class PreflightCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest = Path(self.tmp.name) / "manifest.json"

    def run_cli(self, plan, action="check", *extra):
        self.manifest.write_text(json.dumps(plan), encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = production_preflight.main([action, str(self.manifest), *extra])
        return code, json.loads(out.getvalue())

    def small_run(self, launches=1):
        plan = dict(example_manifest(), units=["club-a", "club-b"],
                    budget={"max_launches": launches, "max_calls": 5, "max_minutes": 10})
        plan.pop("scale_reason")
        return plan


class TestCheck(PreflightCase):
    def test_the_guide_example_passes(self):
        self.assertEqual(self.run_cli(example_manifest()), (0, {"status": "pass", "action": "check",
                                                                "task": "spring-newsletter-batch"}))

    def test_production_without_a_pilot_is_refused_and_names_the_route(self):
        code, out = self.run_cli(dict(example_manifest(), pilots=[]))
        self.assertEqual(code, 2)
        self.assertIn("standard-club", out["reason"])
        self.assertIn("club-with-sponsor", out["reason"])

    def test_a_pilot_at_an_older_acceptance_revision_is_refused(self):
        code, out = self.run_cli(dict(example_manifest(), acceptance_revision="acceptance-2026-03-09"))
        self.assertEqual(code, 2)
        self.assertIn("acceptance revision", out["reason"])

    def test_a_large_launch_budget_needs_a_reason(self):
        plan = example_manifest()
        plan.pop("scale_reason")
        code, out = self.run_cli(plan)
        self.assertEqual(code, 2)
        self.assertIn("scale_reason", out["reason"])

    def test_missing_budget_and_owner_are_both_reported(self):
        plan = example_manifest()
        plan.pop("owner")
        plan["budget"] = {"max_launches": 6}
        code, out = self.run_cli(plan)
        self.assertEqual(code, 2)
        self.assertIn("owner is required", out["reason"])
        self.assertIn("budget.max_calls", out["reason"])

    def test_judgement_work_needs_a_reason(self):
        plan = dict(example_manifest(), mechanical=False)
        self.assertEqual(self.run_cli(plan)[0], 2)
        plan["judgement_reason"] = "Each newsletter argues a different case to its own club."
        self.assertEqual(self.run_cli(plan)[0], 0)

    def test_contrary_a_pilot_of_three_passes_without_a_scale_reason(self):
        plan = dict(example_manifest(), phase="pilot", units=["club-a", "club-b", "club-c"],
                    budget={"max_launches": 3, "max_calls": 10, "max_minutes": 30})
        plan.pop("scale_reason")
        self.assertEqual(self.run_cli(plan)[0], 0)

    def test_a_pilot_of_four_is_refused(self):
        plan = dict(example_manifest(), phase="pilot", units=["club-a", "club-b", "club-c", "club-d"])
        code, out = self.run_cli(plan)
        self.assertEqual(code, 2)
        self.assertIn("three units", out["reason"])

    def test_a_missing_manifest_is_refused(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = production_preflight.main(["check", str(Path(self.tmp.name) / "none.json")])
        self.assertEqual(code, 2)


class TestAdmit(PreflightCase):
    def test_a_repeated_unit_and_an_exhausted_budget_are_refused(self):
        plan = self.small_run(launches=1)
        self.assertEqual(self.run_cli(plan, "admit", "--unit", "club-a")[0], 0)
        code, out = self.run_cli(plan, "admit", "--unit", "club-a")
        self.assertEqual(code, 2)
        self.assertIn("already admitted", out["reason"])
        code, out = self.run_cli(plan, "admit", "--unit", "club-b")
        self.assertEqual(code, 2)
        self.assertIn("budget exhausted", out["reason"])
        ledger = json.loads(production_preflight.ledger_path(self.manifest).read_text(encoding="utf-8"))
        self.assertEqual(ledger["units"], ["club-a"])

    def test_a_unit_outside_the_manifest_is_refused(self):
        code, out = self.run_cli(self.small_run(), "admit", "--unit", "club-z")
        self.assertEqual(code, 2)
        self.assertIn("not in this manifest", out["reason"])

    def test_a_changed_acceptance_revision_stops_further_admissions(self):
        plan = self.small_run(launches=2)
        self.assertEqual(self.run_cli(plan, "admit", "--unit", "club-a")[0], 0)
        changed = dict(plan, acceptance_revision="acceptance-2026-03-09")
        changed["pilots"] = [dict(p, acceptance_revision="acceptance-2026-03-09") for p in plan["pilots"]]
        code, out = self.run_cli(changed, "admit", "--unit", "club-b")
        self.assertEqual(code, 2)
        self.assertIn("rerun the pilot", out["reason"])

    def test_a_held_lock_refuses_admission_and_leaves_the_lock(self):
        plan = self.small_run()
        lock = self.manifest.with_name(self.manifest.name + ".lock")
        lock.write_text("", encoding="utf-8")
        code, out = self.run_cli(plan, "admit", "--unit", "club-a")
        self.assertEqual(code, 2)
        self.assertIn("lock", out["reason"])
        self.assertTrue(lock.exists())
        self.assertFalse(production_preflight.ledger_path(self.manifest).exists())


if __name__ == "__main__":
    unittest.main()
