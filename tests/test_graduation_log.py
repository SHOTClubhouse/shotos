import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import graduation_log  # noqa: E402


class LogCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.log = Path(self.tmp.name) / "nested" / "log.jsonl"

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = graduation_log.main(["--log", str(self.log), *args])
        return code, out.getvalue()

    def record(self, task_class, outcome, count=1, *extra):
        for _ in range(count):
            self.run_cli("record", "--class", task_class, "--outcome", outcome, "--by", "Sam Rivers", *extra)

    def status(self, *args):
        _, out = self.run_cli("status", "--json", *args)
        return {c["class"]: c for c in json.loads(out)["classes"]}


class TestRecord(LogCase):
    def test_record_appends_jsonl_and_creates_folder(self):
        self.record("summary", "accepted-unedited")
        self.record("summary", "rejected", 1, "--note", "wrong client")
        lines = self.log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        second = json.loads(lines[1])
        self.assertEqual(second["outcome"], "rejected")
        self.assertEqual(second["note"], "wrong client")
        self.assertEqual(second["by"], "Sam Rivers")

    def test_record_requires_by(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.run_cli("record", "--class", "x", "--outcome", "rejected")
        with self.assertRaises(SystemExit):
            self.run_cli("record", "--class", "x", "--outcome", "rejected", "--by", " ")

    def test_records_without_by_are_not_counted(self):
        self.record("summary", "accepted-unedited", 3)
        self.log.write_text(self.log.read_text(encoding="utf-8") + json.dumps(
            {"type": "record", "ts": "t", "class": "summary", "outcome": "accepted-unedited"}) + "\n",
            encoding="utf-8")
        self.assertEqual(self.status()["summary"]["samples"], 3)

    def test_rejects_unknown_outcome(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.run_cli("record", "--class", "x", "--outcome", "great", "--by", "Sam")

    def test_empty_status(self):
        _, out = self.run_cli("status")
        self.assertIn("no samples", out)


class TestStatus(LogCase):
    def test_new_class_is_rung_one(self):
        self.record("summary", "accepted-unedited", 10)
        info = self.status()["summary"]
        self.assertEqual(info["rung"], 1)
        self.assertEqual(info["samples"], 10)
        self.assertEqual(info["unedited_rate"], 1.0)

    def test_threshold_for_rung_two(self):
        self.record("summary", "accepted-unedited", 48)
        self.record("summary", "accepted-edited", 2)  # 96%
        self.assertEqual(self.status()["summary"]["rung"], 2)

    def test_just_below_threshold_stays_rung_one(self):
        self.record("summary", "accepted-unedited", 47)
        self.record("summary", "rejected", 3)  # 94%
        self.assertEqual(self.status()["summary"]["rung"], 1)

    def test_not_enough_samples_for_rung_two(self):
        self.record("summary", "accepted-unedited", 49)
        self.assertEqual(self.status()["summary"]["rung"], 1)

    def test_rung_three_needs_two_hundred_samples(self):
        self.record("summary", "accepted-unedited", 199)
        self.assertEqual(self.status()["summary"]["rung"], 2)
        self.record("summary", "accepted-unedited")
        self.assertEqual(self.status()["summary"]["rung"], 3)

    def test_drop_when_recent_window_falls_below_bar(self):
        self.record("summary", "accepted-unedited", 60)
        self.assertEqual(self.status()["summary"]["rung"], 2)
        self.record("summary", "accepted-edited", 5)
        info = self.status()["summary"]
        self.assertEqual(info["rung"], 1)
        self.assertEqual(info["samples"], 65)

    def test_configurable_thresholds_and_window(self):
        self.record("summary", "accepted-unedited", 10)
        info = self.status("--rung2-samples", "10", "--rung2-rate", "0.9", "--window", "10")["summary"]
        self.assertEqual(info["rung"], 2)

    def test_window_must_be_positive(self):
        for bad in ("0", "-5", "abc"):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.run_cli("status", "--window", bad)

    def test_rung_three_needs_rate_over_recent_window(self):
        self.record("summary", "accepted-edited", 150)
        self.record("summary", "accepted-unedited", 50)  # 200 total, recent window all clean
        self.assertEqual(self.status()["summary"]["rung"], 3)

    def test_class_filter(self):
        self.record("a", "accepted-unedited")
        self.record("b", "accepted-unedited")
        self.assertEqual(list(self.status("--class", "a")), ["a"])


class TestHighRisk(LogCase):
    def test_high_risk_capped_at_rung_one(self):
        self.record("payment-email", "accepted-unedited", 60, "--high-risk")
        info = self.status()["payment-email"]
        self.assertEqual(info["earned_rung"], 2)
        self.assertEqual(info["rung"], 1)
        self.assertIn("promotion", info["why"])

    def test_explicit_promotion_lifts_the_cap(self):
        self.record("payment-email", "accepted-unedited", 60, "--high-risk")
        code, _ = self.run_cli("promote", "--class", "payment-email", "--to", "2", "--by", "Sam Rivers")
        self.assertEqual(code, 0)
        self.assertEqual(self.status()["payment-email"]["rung"], 2)

    def test_promotion_does_not_exceed_ceiling(self):
        self.record("payment-email", "accepted-unedited", 250, "--high-risk")
        self.run_cli("promote", "--class", "payment-email", "--to", "2", "--by", "Sam Rivers")
        self.assertEqual(self.status()["payment-email"]["rung"], 2)

    def test_promoted_class_still_drops_when_rate_falls(self):
        self.record("payment-email", "accepted-unedited", 60, "--high-risk")
        self.run_cli("promote", "--class", "payment-email", "--to", "2", "--by", "Sam Rivers")
        self.record("payment-email", "rejected", 5)
        self.assertEqual(self.status()["payment-email"]["rung"], 1)

    def test_promote_needs_valid_rung_and_name(self):
        self.record("x", "accepted-unedited", 1, "--high-risk")
        with self.assertRaises(SystemExit):
            self.run_cli("promote", "--class", "x", "--to", "4", "--by", "Sam")
        with self.assertRaises(SystemExit):
            self.run_cli("promote", "--class", "x", "--to", "2", "--by", " ")

    def test_promote_on_non_high_risk_class_fails_and_records_nothing(self):
        self.record("summary", "accepted-unedited", 60)
        before = self.log.read_text(encoding="utf-8")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code, _ = self.run_cli("promote", "--class", "summary", "--to", "2", "--by", "Sam Rivers")
        self.assertNotEqual(code, 0)
        self.assertIn("no effect", err.getvalue())
        self.assertEqual(self.log.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
