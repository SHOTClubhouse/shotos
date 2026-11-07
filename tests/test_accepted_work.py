import contextlib
import io
import unittest
from pathlib import Path

from tools.summarise_accepted_work import read_ledger, summarise

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "accepted-work-ledger.csv"


class AcceptedWorkTests(unittest.TestCase):
    def report(self, groups):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            summarise(groups)
        return output.getvalue()

    def test_abandoned_and_reworked_attempts_count_towards_cost(self):
        report = self.report(read_ledger(EXAMPLE))
        self.assertIn("| proposal | with | 3 | 3 | 2 | 2/3 | 0.0900 |", report)
        self.assertIn("| proposal | without | 3 | 4 | 2 | 1/3 | 0.0800 |", report)
        self.assertIn("3 task ID(s) appear in every condition", report)

    def test_missing_cost_is_unmeasured(self):
        groups = read_ledger(EXAMPLE)
        groups["proposal", "with"]["F-03"][0].measures["model_cost_usd"] = None
        self.assertIn("| proposal | with | 3 | 3 | 2 | 2/3 | unmeasured |", self.report(groups))

    def test_duplicate_attempt_cannot_be_counted(self):
        groups = read_ledger(EXAMPLE)
        history = groups["proposal", "without"]["F-01"]
        history[1].number = history[0].number
        with self.assertRaisesRegex(ValueError, "unique, consecutive attempts"):
            self.report(groups)


if __name__ == "__main__":
    unittest.main()
