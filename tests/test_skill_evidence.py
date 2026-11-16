import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# docs/skill-format.md: every README has an Evidence line in one of three states. These READMEs are held to
# it now; the older READMEs are still to be brought in line.
CHECKED = ("skills/show-me/README.md", "skills/pilot-before-scale/README.md", "skills/cross-agent-review/README.md",
           "packs/setup/skills/config-as-code/README.md")
STATE = re.compile(r"\*\*Evidence:\*\* (Tested in paired evals, \[[^\]]+\]\([^)]+\)|Cases written, not yet run\."
                   r"|Example only\.)")


class SkillEvidence(unittest.TestCase):
    def test_each_checked_readme_has_one_evidence_line_in_a_known_state(self):
        for path in CHECKED:
            with self.subTest(path=path):
                lines = [line for line in (ROOT / path).read_text(encoding="utf-8").splitlines()
                         if line.startswith("**Evidence:**")]
                self.assertEqual(len(lines), 1, path)
                self.assertRegex(lines[0], STATE)


if __name__ == "__main__":
    unittest.main()
