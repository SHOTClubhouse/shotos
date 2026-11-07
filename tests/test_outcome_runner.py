import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from evals import run_outcomes


class OutcomeRunnerTests(unittest.TestCase):
    def test_authentication_failure_does_not_grade_the_fixture(self):
        payload = {"is_error": True, "result": "Failed to authenticate"}
        with patch.object(run_outcomes.subprocess, "Popen") as popen:
            popen.return_value.communicate.return_value = (json.dumps(payload), "")
            popen.return_value.returncode = 1
            response = run_outcomes.claude_json("Prompt", "haiku", Path.cwd(), 10)
        self.assertIn("Failed to authenticate", response["error"])
        grader = Mock()
        with patch.object(run_outcomes, "setup"), patch.object(run_outcomes, "claude_json", return_value=response):
            with patch.dict(run_outcomes.GRADERS, {"proposal": grader}):
                result = run_outcomes.run_one("proposal", "with", "haiku", 1, 10, None)
        grader.assert_not_called()
        self.assertIsNone(result["outcome_pass"])
        self.assertEqual(result["checks"], [])
        summary = run_outcomes.summarise([result])
        self.assertIn("1 run(s) unavailable for scoring", summary)
        self.assertIn("No complete with/without pairs", summary)

    def test_unavailable_fact_extraction_is_not_a_failed_outcome(self):
        def grader(root, reply):
            return run_outcomes.extract("Find the fact.", reply)

        responses = [{"result": "A draft was saved."}, {"result": "I did not return JSON."}]
        with patch.object(run_outcomes, "setup"), patch.object(run_outcomes, "claude_json", side_effect=responses):
            with patch.dict(run_outcomes.GRADERS, {"proposal": grader}):
                result = run_outcomes.run_one("proposal", "with", "haiku", 1, 10, None)
        self.assertIsNone(result["outcome_pass"])
        self.assertEqual(result["error"], "fact extraction returned no JSON object")


if __name__ == "__main__":
    unittest.main()
