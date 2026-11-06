import tempfile
import unittest
from pathlib import Path

from evals.run_outcomes import grade_proposal


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


if __name__ == "__main__":
    unittest.main()
