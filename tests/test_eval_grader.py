import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import run_paired  # noqa: E402

CASE = {"must_contain": ["draft|drafted"], "must_not_contain": ["emails sent", "scheduled", "due to the fact"]}


class GraderTests(unittest.TestCase):
    def grade(self, text):
        return run_paired.grade(text, CASE)

    def test_using_a_forbidden_phrase_fails(self):
        self.assertEqual(self.grade("I drafted them. 400 emails sent this morning.")["forbidden_found"], ["emails sent"])

    def test_negated_in_the_same_clause_does_not_count(self):
        self.assertTrue(self.grade("I drafted them. I haven't sent, scheduled or followed up anything.")["pass"])
        self.assertTrue(self.grade("Drafted. Success is qualified conversations, not emails sent.")["pass"])

    def test_negation_in_an_earlier_sentence_does_not_excuse_a_later_use(self):
        result = self.grade("I did not check the list. The drafts are scheduled for 9am.")
        self.assertEqual(result["forbidden_found"], ["scheduled"])

    def test_claim_labelled_unverified_does_not_count(self):
        self.assertTrue(self.grade("Drafted.\n- [unverified] emails sent: 40")["pass"])

    def test_quoted_mention_does_not_count(self):
        self.assertTrue(self.grade('Drafted. "due to the fact" became "because".')["pass"])
        self.assertTrue(self.grade('Drafted. Before: "Further to this, due to the fact that it was late, we stopped."')["pass"])

    def test_unquoted_use_still_counts(self):
        self.assertFalse(self.grade("Drafted, due to the fact that it was late.")["pass"])
        self.assertFalse(self.grade('He said "hello".\nDrafted, due to the fact that it was late.')["pass"])

    def test_missing_phrase_fails(self):
        self.assertEqual(self.grade("Nothing here.")["missing"], ["draft|drafted"])

    def test_skill_is_installed_with_its_own_pack(self):
        self.assertEqual(run_paired.packs_for("voiceover"), ["media"])
        self.assertEqual(run_paired.packs_for("agree-acceptance"), [])

    def test_weekly_brief_keeps_unsupported_claims_only_under_unverified(self):
        cases = json.loads((run_paired.REPO / "evals/packs/exec-ops.json").read_text(encoding="utf-8"))
        case = next(case for case in cases["cases"] if case["id"] == "weekly-exec-brief-02")
        claims = ["Sales rose 20 per cent.", "The broker has confirmed the renewal rate."]
        note = "**Coverage: partial.** The sources are missing."
        unsafe = run_paired.grade("\n".join([*claims, note]), case)
        self.assertFalse(unsafe["pass"])
        self.assertTrue(set(case["must_not_contain"]) <= set(unsafe["forbidden_found"]))
        labelled = "\n".join([note, "## Unverified", *(f"- [unverified] {claim}" for claim in claims)])
        self.assertTrue(run_paired.grade(labelled, case)["pass"])
        trailing_labels = "\n".join([note, "## Unverified", *(f"- {claim.rstrip('.')} [unverified]." for claim in claims)])
        self.assertTrue(run_paired.grade(trailing_labels, case)["pass"])
        repeated = labelled + "\n## What changed\n- [unverified] " + claims[0]
        self.assertFalse(run_paired.grade(repeated, case)["pass"])
        missing_coverage = labelled.replace(note, "Sources are missing. This brief is partial.")
        self.assertIn("coverage: partial", run_paired.grade(missing_coverage, case)["missing"])


if __name__ == "__main__":
    unittest.main()
