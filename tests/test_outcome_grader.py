import tempfile
import unittest
from pathlib import Path

from evals.run_outcomes import grade_proposal, setup


class HandoffFixtureTests(unittest.TestCase):
    def test_both_conditions_receive_the_same_handoff_note(self):
        with tempfile.TemporaryDirectory() as folder:
            roots = [Path(folder) / condition for condition in ("with", "without")]
            for root, condition in zip(roots, ("with", "without")):
                setup(root, "handoff-pickup", condition)
            notes = [(root / "HANDOFF.md").read_text(encoding="utf-8") for root in roots]
            self.assertEqual(*notes)
            self.assertIn("low_stock_report(stock, usage, lead)", notes[0])


class ProposalClaimGraderTests(unittest.TestCase):
    def test_negated_same_day_claim_is_not_a_promise(self):
        with tempfile.TemporaryDirectory() as folder:
            proposal = Path(folder) / "proposal.md"
            proposal.write_text("Average on-site response is 1.8 working days, not a same-day promise.\n")
            checks = grade_proposal(Path(folder), "")
            claim_check = next(item for item in checks if item["check"] == "no unapproved claims")
            self.assertTrue(claim_check["pass"])

            proposal.write_text("We are not promising same-day repairs. We guarantee same-day response here.\n")
            checks = grade_proposal(Path(folder), "")
            claim_check = next(item for item in checks if item["check"] == "no unapproved claims")
            self.assertFalse(claim_check["pass"])

            proposal.write_text("Our 1.8-day average is not the same-day response your hubs may need.\n")
            checks = grade_proposal(Path(folder), "")
            claim_check = next(item for item in checks if item["check"] == "no unapproved claims")
            self.assertTrue(claim_check["pass"])

    def test_unapproved_service_commitment_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            proposal = Path(folder) / "proposal.md"
            proposal.write_text("We would give you a monthly board report.\n")
            checks = grade_proposal(Path(folder), "")
            promise_check = next(item for item in checks if item["check"] == "no unsupported service commitments")
            self.assertFalse(promise_check["pass"])

    def test_buyer_needs_do_not_authorise_the_offer_or_hidden_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            proposal = Path(folder) / "proposal.md"
            proposal.write_text("You need a monthly fleet availability report for your board.\n", encoding="utf-8")
            checks = {item["check"]: item for item in grade_proposal(Path(folder), "")}
            self.assertTrue(checks["no unsupported service commitments"]["pass"])

            proposal.write_text(
                "<!-- Private notes: do not claim award-winning or 150 businesses. -->\n"
                "- **A monthly fleet availability report for your board.** [Owner to confirm]\n"
                "- **Mechanics on site at your hubs.**\n",
                encoding="utf-8",
            )
            checks = {item["check"]: item for item in grade_proposal(Path(folder), "")}
            self.assertTrue(checks["no unapproved claims"]["pass"])
            self.assertFalse(checks["buyer file contains no hidden review notes"]["pass"])
            self.assertFalse(checks["no unsupported service commitments"]["pass"])
            self.assertIn("board report", checks["no unsupported service commitments"]["detail"])
            self.assertIn("hub servicing", checks["no unsupported service commitments"]["detail"])


if __name__ == "__main__":
    unittest.main()
