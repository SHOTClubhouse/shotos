import re
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[1] / "packs" / "exec-ops"


def read(*parts):
    return PACK.joinpath(*parts).read_text(encoding="utf-8")


def headings(text):
    return [line for line in text.splitlines() if line.startswith("## ")]


class DecisionBriefShape(unittest.TestCase):
    def test_recommendation_precedes_facts_and_decision_is_requested(self):
        for text in (read("skills", "decision-brief", "template.md"), read("examples", "decision-brief", "output.md")):
            found = headings(text)
            rec = next(i for i, h in enumerate(found) if h.startswith("## Recommendation"))
            self.assertLess(rec, next(i for i, h in enumerate(found) if h.startswith("## Facts")))
            self.assertTrue(found[-1].startswith("## Decision requested") or found[-1].startswith("## Questions for"))
            self.assertIn("## Decision requested", found)
            self.assertIn("What would change this", text)


class WeeklyBriefShape(unittest.TestCase):
    def test_coverage_line_precedes_decisions_and_unverified_is_labelled(self):
        for text in (read("skills", "weekly-exec-brief", "template.md"), read("examples", "weekly-exec-brief", "output.md")):
            self.assertLess(text.index("**Coverage:"), text.index("## Decisions needed"))
            self.assertLess(text.index("## Decisions needed"), text.index("## What changed"))
        example = read("examples", "weekly-exec-brief", "output.md")
        self.assertIn("**Coverage: partial.**", example)
        self.assertIn("**Comparison point:**", example)
        unverified = example.split("## Unverified", 1)[1]
        bullets = [l for l in unverified.splitlines() if l.startswith("- ")]
        self.assertTrue(bullets and all("[unverified]" in b for b in bullets))
        self.assertNotIn("[unverified]", example.split("## Unverified", 1)[0])


if __name__ == "__main__":
    unittest.main()
