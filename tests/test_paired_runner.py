import json
import unittest
from unittest.mock import patch

from evals import run_paired


class PairedRunnerTests(unittest.TestCase):
    def test_runtime_only_receives_fixture_tools_and_errors_stay_unscored(self):
        case = {"id": "fictional", "skill": "baseline", "type": "normal", "prompt": "Read the fixture.",
                "must_contain": ["done"], "must_not_contain": []}
        with patch.object(run_paired.subprocess, "run"), patch.object(run_paired.subprocess, "Popen") as popen:
            popen.return_value.returncode = 1
            popen.return_value.communicate.return_value = (json.dumps({"is_error": True, "result": "Offline"}), "")
            result = run_paired.run_one(case, "without", "haiku", 5, None)
        args = popen.call_args.args[0]
        self.assertEqual(args[args.index("--tools") + 1], "Read,Write,Edit,Glob,Grep")
        self.assertEqual(result["error"], "runtime failed: Offline")
        self.assertEqual(result["missing"], [])
        scored = {**result, "condition": "with", "error": None, "pass": False}
        self.assertIn("| baseline | 1 | 0/1 | 0/0 | 0 / 1 |", run_paired.summarise([result, scored]))


if __name__ == "__main__":
    unittest.main()
