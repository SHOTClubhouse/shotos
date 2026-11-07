import json
import unittest

from evals.judge_paired import paired, parse_verdict


def row(model, condition, passed, batch=1):
    return {"id": "one", "model": model, "condition": condition, "pass": passed, "source_batch": batch}


class PairedJudgeTests(unittest.TestCase):
    def test_cases_are_paired_within_each_model_and_batch(self):
        rows = [row("haiku", "with", True), row("haiku", "without", False),
                row("sonnet", "with", False), row("sonnet", "without", True),
                row("haiku", "with", False, batch=2), row("haiku", "without", True, batch=2),
                row("haiku", "with", True, batch=3), row("sonnet", "without", True, batch=3)]
        self.assertEqual(paired(rows, "pass"), (3, 1, 2))

    def test_duplicate_side_in_one_batch_is_refused(self):
        rows = [row("haiku", "with", True), row("haiku", "with", False)]
        with self.assertRaisesRegex(ValueError, "duplicate run"):
            paired(rows, "pass")

    def test_only_json_booleans_count_as_verdicts(self):
        case = {"must_contain": ["one"], "must_not_contain": []}
        invalid = json.dumps({"result": json.dumps({"requirements": ["false"], "prohibitions": []})})
        valid = json.dumps({"result": json.dumps({"requirements": [False], "prohibitions": []})})
        self.assertIn("error", parse_verdict(case, invalid))
        self.assertIs(parse_verdict(case, valid)["pass"], False)


if __name__ == "__main__":
    unittest.main()
