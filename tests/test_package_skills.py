import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "package_skills.py"


class PackageSkillsTests(unittest.TestCase):
    def test_each_zip_holds_one_skill_folder_with_skill_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(TOOL), "--all-packs", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            zips = sorted(Path(tmp).glob("*.zip"))
            repo = TOOL.parents[1]
            sources = [*repo.glob("skills/*/SKILL.md"), *repo.glob("packs/*/skills/*/SKILL.md")]
            self.assertCountEqual((z.stem for z in zips), (source.parent.name for source in sources))
            by_name = {source.parent.name: source for source in sources}
            for z in zips:
                with zipfile.ZipFile(z) as archive:
                    names = archive.namelist()
                    self.assertIsNone(archive.testzip())
                    self.assertEqual(len(names), len(set(names)), z.name)
                    top = {n.split("/")[0] for n in names}
                    self.assertEqual(top, {z.stem})
                    self.assertEqual(archive.read(f"{z.stem}/SKILL.md"), by_name[z.stem].read_bytes())
                    self.assertTrue(all(entry.date_time == (1980, 1, 1, 0, 0, 0) for entry in archive.infolist()))
                    self.assertIn(f"{z.stem}/example-input.md", names)
                    self.assertIn(f"{z.stem}/example-output.md", names)
                    self.assertIn(f"{z.stem}/LICENSE-docs.md", names)
                    self.assertIn(f"{z.stem}/LICENSE", names)

    def test_executive_review_travels_with_decision_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            repo = TOOL.parents[1]
            subprocess.run([sys.executable, str(repo / "install.py"), "--runtime", "claude",
                            "--scope", "project", "--target", tmp, "--pack", "exec-ops"],
                           check=True, capture_output=True)
            subprocess.run([sys.executable, str(TOOL), "--pack", "exec-ops", "--out", tmp],
                           check=True, capture_output=True)
            installed = target / ".claude" / "skills" / "decision-brief"
            workflow = (installed / "review-cycle.md").read_bytes()
            self.assertIn("(review-cycle.md)", (installed / "SKILL.md").read_text(encoding="utf-8"))
            with zipfile.ZipFile(target / "decision-brief.zip") as archive:
                self.assertEqual(archive.read("decision-brief/review-cycle.md"), workflow)
                desktop_guide = archive.read("decision-brief/guides/codex-claude-code.md")
                self.assertIn(b"(chat-assistants.md#run-the-retail-scenario)", desktop_guide)
                chat_guide = archive.read("decision-brief/guides/chat-assistants.md")
                for name in ("retail-trial", "bank-remediation", "startup-proposal"):
                    with self.subTest(scenario=name):
                        relative = f"scenarios/{name}.md"
                        self.assertIn(f"({relative})", workflow.decode("utf-8"))
                        content = (installed / relative).read_bytes()
                        self.assertIn(b"Fictional scenario", content)
                        self.assertEqual(archive.read(f"decision-brief/{relative}"), content)
                        if name != "retail-trial":
                            for phase in ("initial", "follow-up"):
                                filename = f"{name}-{phase}.md"
                                input_path = f"scenarios/{filename}"
                                self.assertIn(f"({filename})".encode("ascii"), content)
                                self.assertIn(f"(../{input_path})".encode("ascii"), chat_guide)
                                self.assertEqual(archive.read(f"decision-brief/{input_path}"),
                                                 (installed / input_path).read_bytes())
                retail_example = (installed / "scenarios/retail-trial.md").read_text(encoding="utf-8")
                for phase, record_ids in (("initial", [b"1", b"2", b"3"]),
                                          ("follow-up", [b"4", b"5", b"6"])):
                    with self.subTest(phase=phase):
                        name = f"retail-trial-{phase}.md"
                        self.assertIn(f"({name})", retail_example)
                        relative = f"scenarios/{name}"
                        content = (installed / relative).read_bytes()
                        self.assertEqual(archive.read(f"decision-brief/{relative}"), content)
                        self.assertIn(f"(../{relative})".encode("ascii"), chat_guide)
                        self.assertEqual(re.findall(rb"(?m)^- \*\*R([1-6]),", content), record_ids)

    def test_proposal_resources_travel_in_both_skill_zips(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, str(TOOL), "--pack", "win-the-work",
                            "--pack", "customer-success", "--out", tmp],
                           check=True, capture_output=True)
            target = Path(tmp)
            with zipfile.ZipFile(target / "contextual-proposal.zip") as proposal, \
                    zipfile.ZipFile(target / "success-handoff.zip") as handoff:
                for name in ("worked-deal.md", "organisation-templates.md", "template.md"):
                    with self.subTest(resource=name):
                        self.assertEqual(proposal.read(f"contextual-proposal/{name}"),
                                         handoff.read(f"success-handoff/proposal/{name}"))
                self.assertIn(b"(proposal/worked-deal.md)", handoff.read("success-handoff/README.md"))

    def test_release_zip_pins_repository_links_and_keeps_bundled_links_local(self):
        source_commit = "b" * 40
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, str(TOOL), "--pack", "exec-ops",
                            "--source-commit", source_commit, "--out", tmp],
                           check=True, capture_output=True)
            with zipfile.ZipFile(Path(tmp) / "decision-brief.zip") as archive:
                guide = archive.read("decision-brief/guides/chat-assistants.md")
                self.assertIn(f"/blob/{source_commit}/templates/AGENTS.md".encode("ascii"), guide)
                self.assertIn(b"(../scenarios/retail-trial-initial.md)", guide)
                self.assertIn("decision-brief/scenarios/retail-trial-initial.md", archive.namelist())

    def test_unknown_pack_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(TOOL), "--pack", "no-such-pack", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
