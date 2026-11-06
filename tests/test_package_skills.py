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
            result = subprocess.run([sys.executable, str(TOOL), "--pack", "media", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            zips = sorted(Path(tmp).glob("*.zip"))
            self.assertIn("voiceover.zip", [z.name for z in zips])
            self.assertIn("agree-acceptance.zip", [z.name for z in zips])
            for z in zips:
                with zipfile.ZipFile(z) as archive:
                    names = archive.namelist()
                    top = {n.split("/")[0] for n in names}
                    self.assertEqual(top, {z.stem})
                    self.assertIn(f"{z.stem}/SKILL.md", names)
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

    def test_unknown_pack_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(TOOL), "--pack", "no-such-pack", "--out", tmp],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
