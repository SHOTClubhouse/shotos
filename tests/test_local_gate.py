import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import local_gate as gate  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "leak-denylist.txt"
STAMP = datetime(2026, 11, 16, 9, 30, tzinfo=timezone.utc)


def context(**changes):
    values = dict(head="a" * 40, branch="fictional", base="b" * 40, base_label="origin/main", fast=False,
                  release=False, denylist=FIXTURE)
    values.update(changes)
    return gate.Context(**values)


def passing():
    return [gate.Check("Unit tests", "pass", "All 3 tests passed."), gate.Check("Demo", "pass", "Ran.")]


class GateDecisionTests(unittest.TestCase):
    def test_any_failed_check_is_no_go(self):
        checks = passing() + [gate.Check("Leak scan", "fail", "1 private term(s) found.")]
        self.assertEqual(gate.decide(context(), checks), "NO-GO")
        self.assertEqual(gate.decide(context(), passing()), "GO")

    def test_a_missing_denylist_warns_locally_and_is_no_go_for_a_release(self):
        local = context(denylist=None)
        self.assertEqual(gate.decide(local, passing()), "GO")
        card = gate.render(local, passing(), "GO", STAMP)
        self.assertIn("**For release:** no, because the private denylist was missing", card)
        self.assertIn("The private denylist was not found.", card)
        self.assertEqual(gate.decide(context(denylist=None, release=True), passing()), "NO-GO")

    def test_fast_and_dirty_runs_cannot_be_used_for_a_release(self):
        self.assertEqual(gate.release_blockers(context(fast=True)), ["this was a fast run"])
        self.assertEqual(gate.release_blockers(context(dirty=["docs/faq.md"])), ["there were uncommitted changes"])
        self.assertEqual(gate.decide(context(fast=True, release=True), passing()), "NO-GO")

    def test_card_states_the_verdict_changes_checks_and_what_to_look_at(self):
        ctx = context(commits=["abc1234 Clarify the fictional guide"], changes=[("M", "docs/faq.md"),
                                                                                  ("A", "tools/new.py")])
        card = gate.render(ctx, passing() + [gate.Check("Claim check", "skip", "Not for docs.")], "GO", STAMP)
        self.assertTrue(card.startswith("# SHOTos gate card: GO\n"))
        for line in ("**Verdict:** GO", f"**Commit:** {'a' * 40} on fictional", "**For release:** yes",
                     "**Compared with:** origin/main (bbbbbbbbbbbb)", "1 file(s) added, 1 changed, 0 removed",
                     "- Areas: docs, tools.", "- abc1234 Clarify the fictional guide",
                     "- PASS Unit tests: All 3 tests passed.", "- SKIP Claim check: Not for docs.",
                     "## What a person should look at"):
            self.assertIn(line, card)

    def test_a_changed_control_file_is_flagged_for_a_person(self):
        items = gate.look_at(context(changes=[("M", "tools/claim_check.py")]), passing())
        self.assertTrue(any("stop until the owner approves it" in item for item in items))

    def test_the_card_never_carries_a_denylist_term(self):
        ctx = context(commits=["abc1234 Move the Quillbury notes"])
        card = gate.safe(gate.render(ctx, passing(), "GO", STAMP), ctx)
        self.assertNotIn("Quillbury", card)
        self.assertIn("[withheld: matches denylist line 2]", card)

    def test_fast_cards_do_not_replace_the_full_card(self):
        self.assertEqual(gate.card_path("c" * 40, cards=Path("cards")), Path("cards") / f"{'c' * 12}.md")
        self.assertEqual(gate.card_path("c" * 40, True, Path("cards")), Path("cards") / f"{'c' * 12}-fast.md")


class GateRepositoryTests(unittest.TestCase):
    def test_changed_skills_include_a_changed_worked_example(self):
        skills = gate.skill_folders()
        skill, examples = skills[0]
        folder = skill.relative_to(ROOT).as_posix()
        example = examples.relative_to(ROOT).as_posix()
        self.assertEqual(gate.changed_skills([("M", f"{folder}/SKILL.md")], skills), [(skill, examples)])
        self.assertEqual(gate.changed_skills([("M", f"{example}/output.md")], skills), [(skill, examples)])
        self.assertEqual(gate.changed_skills([("M", "docs/faq.md")], skills), [])

    def test_every_current_skill_meets_the_structure_checks(self):
        cases = gate.eval_cases()
        problems = [p for skill, examples in gate.skill_folders() for p in gate.structure_problems(skill, examples, cases)]
        self.assertEqual(problems, [])

    def test_structure_checks_name_each_missing_part(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "fictional-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: other-name\n---\n# Fictional\n", encoding="utf-8")
            problems = gate.structure_problems(skill, Path(directory) / "examples", [
                {"skill": "fictional-skill", "type": "normal"}])
        joined = "\n".join(problems)
        for expected in ("name does not match", "no description", "no Checks section", "no README.md",
                         "no worked input", "no worked output", "no contrary eval case"):
            self.assertIn(expected, joined)
        self.assertNotIn("no normal eval case", joined)

    def test_pre_push_scans_only_the_commits_being_sent(self):
        head = gate.git("rev-parse", "HEAD")
        parent = gate.git("rev-parse", "HEAD^")
        zero = "0" * 40
        ranges, pushed = gate.push_ranges([
            f"refs/heads/fictional {head} refs/heads/fictional {zero}",
            f"refs/heads/main {head} refs/heads/main {parent}",
            f"(delete) {zero} refs/heads/old {parent}",
        ])
        self.assertEqual(ranges, [[head, "--not", "--remotes"], [f"{parent}..{head}"]])
        self.assertEqual(pushed, [head, head])

    def test_base_falls_back_to_the_last_tag(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, check=True)
            run("init", "-q", "--template=")
            run("config", "user.name", "Gate Test")
            run("config", "user.email", "gate-test@example.com")
            for name in ("one", "two"):
                (repo / f"{name}.md").write_text(name, encoding="utf-8")
                run("add", "-A")
                run("-c", "commit.gpgsign=false", "commit", "-qm", name)
                if name == "one":
                    run("tag", "v1.0.0")
            commit, label = gate.choose_base(repo=repo)
            self.assertEqual(label, "v1.0.0")
            self.assertEqual(commit, gate.resolve("v1.0.0", repo))
            (repo / "one.md").write_text("changed", encoding="utf-8")
            (repo / "three.md").write_text("new", encoding="utf-8")
            self.assertEqual(gate.worktree_state(repo), (["one.md"], 1))

    def test_fast_gate_writes_a_card_and_its_exit_code_matches_the_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            env = {**os.environ, "SHOTOS_DENYLIST": ""}
            run = subprocess.run([sys.executable, str(ROOT / "tools" / "local_gate.py"), "--fast", "--out", directory],
                                 capture_output=True, text=True, encoding="utf-8", env=env, timeout=600)
            self.assertIn("SHOTOS_DENYLIST is not set", run.stderr)
            cards = list(Path(directory).glob("*-fast.md"))
            self.assertEqual(len(cards), 1, run.stdout + run.stderr)
            card = cards[0].read_text(encoding="utf-8")
            self.assertIn("**Mode:** fast", card)
            self.assertIn("- SKIP Leak scan:", card)
            self.assertIn("**For release:** no, because this was a fast run", card)
            self.assertEqual(run.returncode == 0, "**Verdict:** GO" in card)

    def test_release_mode_needs_the_full_gate(self):
        run = subprocess.run([sys.executable, str(ROOT / "tools" / "local_gate.py"), "--release", "--fast"],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
