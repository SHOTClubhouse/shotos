"""The walkthrough's reference numbers must match its data."""

import csv
import re
import unittest
from collections import Counter
from pathlib import Path

WALK = Path(__file__).resolve().parents[1] / "examples" / "walkthrough"


class WalkthroughTests(unittest.TestCase):
    def setUp(self):
        with open(WALK / "data" / "enquiries.csv", encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f))
        with open(WALK / "data" / "open-repairs.csv", encoding="utf-8") as f:
            self.repairs = list(csv.DictReader(f))
        self.findings = (WALK / "reference" / "2-findings.md").read_text(encoding="utf-8")

    def repeats(self):
        seen, counts = set(), Counter()
        for row in self.rows:
            key = (row["tenant"], row["category"])
            if key in seen:
                counts[row["category"]] += 1
            seen.add(key)
        return counts

    def test_category_and_repeat_counts_match_the_table(self):
        totals, repeats = Counter(r["category"] for r in self.rows), self.repeats()
        for category, emails in totals.items():
            with self.subTest(category=category):
                pattern = rf"\| {category.capitalize()} \| {emails} \| {repeats[category]} \|"
                self.assertRegex(self.findings, pattern)
        self.assertIn(f"**{len(self.rows)}** | **{sum(repeats.values())}**", self.findings)

    def test_repair_issues_match_open_repairs(self):
        repair_tenants = {r["tenant"] for r in self.rows if r["category"] == "repair"}
        self.assertEqual(repair_tenants, {r["tenant"] for r in self.repairs})
        self.assertIn(f"only {len(repair_tenants)} separate repair issues", self.findings)

    def test_exactly_one_repair_needs_a_person(self):
        self.assertEqual([r["tenant"] for r in self.repairs if not r["next_date"]], ["T-618"])
        report = (WALK / "reference" / "4-report.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"T-\d+\.md", report)), len(self.repairs))


if __name__ == "__main__":
    unittest.main()
