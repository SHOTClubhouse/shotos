#!/usr/bin/env python3
"""Sixty-second demo: an agent's confident report, checked against the evidence.

Creates a throwaway git repository, makes it look like an agent half-finished a
task, then runs claim-check on the report the agent wrote. Nothing outside the
temporary folder is touched.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OVERCLAIM = """All done. I've written the pricing summary, the tests pass, it's committed,
and I've emailed it to the finance team.

## Claims
- [file] created: pricing-summary.md
- [command] passes: python -m unittest
- [git] committed: HEAD
- [external] sent: pricing summary to finance
- [unverified] I did not check how the summary renders in the finance team's email client
"""

READBACK = """The pricing summary exists. The test failed, and the draft has not
been committed or sent.

## Claims
- [file] created: pricing-summary.md
- [unverified] The summary still needs a review for accuracy.
"""


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def check_report(repo, label, report, expected_exit, expected_states):
    print(label)
    print(report)
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "claim_check.py"), "-", "--cwd", str(repo),
         "--allow-command", "python -m unittest", "--json"],
        input=report, capture_output=True, text=True,
    )
    if run.returncode != expected_exit:
        raise RuntimeError(f"Unexpected claim-check exit: {run.returncode}\n{run.stderr}\n{run.stdout}")
    result = json.loads(run.stdout)
    states = [claim["state"] for claim in result["claims"]]
    if states != expected_states or result["ok"] != (expected_exit == 0):
        raise RuntimeError(f"Unexpected claim-check result: {result}")
    for claim in result["claims"]:
        print(f"{claim['state']:<12} {claim['claim']} ({claim['evidence']})")
    print()


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        sh(repo, "git", "init", "-q", "-b", "main")
        sh(repo, "git", "config", "user.email", "demo@example.com")
        sh(repo, "git", "config", "user.name", "Demo")
        (repo / "test_prices.py").write_text(
            "import unittest\n\nclass T(unittest.TestCase):\n"
            "    def test_total(self):\n        self.assertEqual(2 + 2, 5)\n", encoding="utf-8")
        sh(repo, "git", "add", ".")
        sh(repo, "git", "commit", "-q", "-m", "start")
        (repo / "pricing-summary.md").write_text("# Pricing summary\n", encoding="utf-8")
        (repo / "test_prices.py").write_text(
            (repo / "test_prices.py").read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")

        check_report(repo, "1. The overclaim", OVERCLAIM, 1,
                     ["SUPPORTED", "UNSUPPORTED", "UNSUPPORTED", "NO EVIDENCE", "DECLARED"])
        check_report(repo, "2. The same work, reported accurately", READBACK, 0,
                     ["SUPPORTED", "DECLARED"])
        print("Demo passed. The file exists and its quality still needs review.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
