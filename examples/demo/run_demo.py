#!/usr/bin/env python3
"""Sixty-second demo: an agent's confident report, checked against the evidence.

Creates a throwaway git repository, makes it look like an agent half-finished a
task, then runs claim-check on the report the agent wrote. Nothing outside the
temporary folder is touched.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT = """All done. I've written the pricing summary, the tests pass, it's committed,
and I've emailed it to the finance team.

## Claims
- [file] created: pricing-summary.md
- [command] passes: python -m unittest
- [git] committed: HEAD
- [external] sent: pricing summary to finance
- [unverified] I did not check how the summary renders in the finance team's email client
"""


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


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

        print("The agent says:\n")
        print("    " + REPORT.replace("\n", "\n    "))
        print("claim-check says:\n")
        run = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "claim_check.py"), "-", "--cwd", str(repo),
             "--allow-command", "python -m unittest"],
            input=REPORT, capture_output=True, text=True)
        print(run.stdout)
        return 0


if __name__ == "__main__":
    sys.exit(main())
