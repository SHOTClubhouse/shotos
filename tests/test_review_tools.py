import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import review_packet  # noqa: E402
import run_contained  # noqa: E402

RUNNER = ROOT / "tools" / "run_contained.py"


class ReviewCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.scope = self.base / "spring-fair"
        self.scope.mkdir()
        (self.scope / "rota.md").write_text("Sam: 4 shifts\nPriya: 2 shifts\n", encoding="utf-8")
        self.spec = {"request": "Check the volunteer rota against the rule card.",
                     "acceptance": ["No one has more than 3 shifts."], "sources": ["rota.md"],
                     "evidence": [{"source": "rule card", "text": "Maximum 3 shifts each."}],
                     "limitations": ["The availability list was not supplied."]}

    def packet_cli(self, *args):
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
            code = review_packet.main([str(a) for a in args])
        return code, out.getvalue(), err.getvalue()

    def build(self, spec=None, *extra):
        path = self.base / "spec.json"
        path.write_text(json.dumps(self.spec if spec is None else spec), encoding="utf-8")
        return self.packet_cli("build", path, "--scope", self.scope, *extra)

    def packet(self) -> Path:
        out = self.base / "work" / "packet.json"
        code, _, err = self.build(None, "--revision", "r1", "--out", out)
        self.assertEqual(code, 0, err)
        return out


class TestPacket(ReviewCase):
    def test_build_then_validate_gives_the_same_hash(self):
        out = self.packet()
        built = json.loads(self.packet_cli("validate", out, "--scope", self.scope)[1])
        self.assertEqual(built["status"], "valid")
        self.assertEqual(built["sha256"], json.loads(self.build(None, "--revision", "r1", "--out", out)[2])["sha256"])
        packet = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(packet["sources"], [{"path": "rota.md", "revision": "r1",
                                              "text": "Sam: 4 shifts\nPriya: 2 shifts\n"}])

    def test_a_packet_used_with_a_different_folder_is_refused(self):
        out = self.packet()
        other = self.base / "another-project"
        other.mkdir()
        code, _, err = self.packet_cli("validate", out, "--scope", other)
        self.assertEqual(code, 2)
        self.assertIn("built for spring-fair", err)

    def test_a_tampered_source_revision_is_refused(self):
        out = self.packet()
        packet = json.loads(out.read_text(encoding="utf-8"))
        packet["sources"][0]["revision"] = "r0"
        out.write_text(json.dumps(packet), encoding="utf-8")
        self.assertEqual(self.packet_cli("validate", out, "--scope", self.scope)[0], 2)

    def test_an_incomplete_packet_is_refused(self):
        out = self.packet()
        good = json.loads(out.read_text(encoding="utf-8"))
        broken = {
            "no request or acceptance": dict(good, request=None, acceptance=None,
                                             sources=[{"revision": "r1"}]),
            "no request": dict(good, request=None),
            "empty acceptance": dict(good, acceptance=[]),
            "a source with only its revision": dict(good, sources=[{"revision": "r1"}]),
            "a source with no text": dict(good, sources=[{"path": "rota.md", "revision": "r1"}]),
            "a source outside the scope": dict(good, sources=[dict(good["sources"][0], path="../rota.md")]),
            "a malformed evidence item": dict(good, evidence=[{"source": "rule card"}]),
            "a malformed limitation": dict(good, limitations=[None]),
        }
        for name, packet in broken.items():
            with self.subTest(name):
                out.write_text(json.dumps(packet), encoding="utf-8")
                code, _, err = self.packet_cli("validate", out, "--scope", self.scope)
                self.assertEqual(code, 2, name)
                self.assertEqual(json.loads(err)["status"], "refused")

    def test_a_packet_from_another_project_with_the_same_folder_name_is_refused(self):
        out = self.packet()
        other = self.base / "elsewhere" / "spring-fair"
        other.mkdir(parents=True)
        (other / "rota.md").write_text("Sam: 1 shift\n", encoding="utf-8")
        code, _, err = self.packet_cli("validate", out, "--scope", other)
        self.assertEqual(code, 2)
        self.assertIn("built for spring-fair at", err)

    def test_a_source_that_has_changed_since_the_packet_was_built_is_refused(self):
        out = self.packet()
        (self.scope / "rota.md").write_text("Sam: 3 shifts\n", encoding="utf-8")
        code, _, err = self.packet_cli("validate", out, "--scope", self.scope)
        self.assertEqual(code, 2)
        self.assertIn("does not match", err)

    def test_a_packet_from_another_project_with_the_same_name_and_identical_text_is_refused(self):
        out = self.packet()
        other = self.base / "elsewhere" / "spring-fair"
        other.mkdir(parents=True)
        (other / "rota.md").write_bytes((self.scope / "rota.md").read_bytes())
        code, _, err = self.packet_cli("validate", out, "--scope", other)
        self.assertEqual(code, 2)
        self.assertIn(str(self.scope.resolve()), json.loads(err)["reason"])
        scope = json.loads(out.read_text(encoding="utf-8"))["scope"]
        self.assertEqual(scope, {"name": "spring-fair", "path": str(self.scope.resolve()), "root_commit": None})

    def test_a_packet_records_the_root_commit_and_refuses_another_repository_at_the_same_path(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.scope), "-c", "user.name=Test", "-c", "user.email=t@example.org",
                                   "-c", "commit.gpgsign=false", *args], capture_output=True, text=True,
                                  check=True).stdout.strip()

        def new_repository(message):
            git("init", "-q")
            git("add", "rota.md")
            git("commit", "-q", "-m", message)
            return git("rev-parse", "HEAD")

        try:
            first = new_repository("first")
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git is not available")
        out = self.packet()
        self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["scope"]["root_commit"], first)
        self.assertEqual(self.packet_cli("validate", out, "--scope", self.scope)[0], 0)
        for path in (self.scope / ".git").rglob("*"):
            os.chmod(path, 0o700)
        shutil.rmtree(self.scope / ".git")
        self.assertNotEqual(new_repository("second"), first)
        code, _, err = self.packet_cli("validate", out, "--scope", self.scope)
        self.assertEqual(code, 2)
        self.assertIn("root commit", err)

    def test_contrary_secrets_and_paths_outside_the_scope_are_refused(self):
        (self.scope / ".env").write_text("X=1", encoding="utf-8")
        (self.scope / "notes.md").write_text("api_key = abcdefgh12345678", encoding="utf-8")
        (self.base / "outside.md").write_text("outside", encoding="utf-8")
        for bad in (".env", "notes.md", "../outside.md", str(self.base / "outside.md"), "missing.md"):
            with self.subTest(source=bad):
                code, _, err = self.build(dict(self.spec, sources=[bad]), "--revision", "r1")
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(err)["status"], "refused")

    def test_a_source_through_a_link_is_refused(self):
        target = self.base / "elsewhere"
        target.mkdir()
        (target / "plan.md").write_text("plan", encoding="utf-8")
        try:
            (self.scope / "linked").symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("this system does not allow symbolic links here")
        code, _, err = self.build(dict(self.spec, sources=["linked/plan.md"]), "--revision", "r1")
        self.assertEqual(code, 2)
        self.assertIn("link", err)

    def test_the_revision_is_required(self):
        code, _, err = self.build()
        self.assertEqual(code, 2)
        self.assertIn("--revision", err)

    def test_an_oversized_packet_is_refused(self):
        spec = dict(self.spec, evidence=[{"source": f"note {i}", "text": "x" * 15000} for i in range(10)])
        code, _, err = self.build(spec, "--revision", "r1")
        self.assertEqual(code, 2)
        self.assertIn("limit", err)


class TestRunner(ReviewCase):
    def run_tool(self, *args, env=None, launch=True):
        flag = ["--allow-network"] if launch else []
        return subprocess.run([sys.executable, str(RUNNER), *flag, *map(str, args)], capture_output=True, text=True,
                              env=env, timeout=120)

    def test_without_the_network_flag_nothing_is_launched(self):
        receipt = self.base / "work" / "receipt.json"
        marker = self.base / "launched.txt"
        script = f"open({str(marker)!r}, 'w').write('launched')"
        result = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c", script,
                               launch=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run", result.stdout)
        self.assertIn("--allow-network", result.stdout)
        self.assertIn(Path(sys.executable).name, result.stdout)
        self.assertFalse(marker.exists())
        self.assertFalse(receipt.exists())
        launched = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c", script)
        self.assertEqual(launched.returncode, 0, launched.stderr)
        self.assertTrue(marker.exists())
        self.assertTrue(json.loads(receipt.read_text(encoding="utf-8"))["network_allowed"])

    def test_the_packet_reaches_the_command_and_the_receipt_holds_no_content(self):
        receipt = self.base / "work" / "receipt.json"
        result = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c",
                               "import sys, json; print(json.load(sys.stdin)['revision'])")
        self.assertEqual((result.returncode, result.stdout.strip()), (0, "r1"))
        data = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertFalse(data["sandboxed"])
        self.assertEqual(data["argument_count"], 2)
        self.assertNotIn("Sam", receipt.read_text(encoding="utf-8"))
        self.assertNotIn("revision", json.dumps(data["command"]))

    def test_the_command_runs_outside_the_project_folder(self):
        receipt = self.base / "receipt.json"
        result = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c",
                               "import os; print(sorted(os.listdir('.')))")
        self.assertEqual(result.stdout.strip(), "[]")

    def test_an_environment_variable_that_was_not_allowed_is_absent(self):
        receipt = self.base / "receipt.json"
        script = "import os; print(os.environ.get('REVIEW_TOKEN', 'absent'))"
        env = dict(os.environ, REVIEW_TOKEN="leak")
        result = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c", script,
                               env=env)
        self.assertEqual(result.stdout.strip(), "absent")
        allowed = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--allow-env", "REVIEW_TOKEN", "--",
                                sys.executable, "-c", script, env=env)
        self.assertEqual(allowed.stdout.strip(), "leak")

    def test_the_time_limit_stops_the_command_and_its_children(self):
        receipt = self.base / "receipt.json"
        child = "import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); time.sleep(60)"
        started = time.monotonic()
        result = self.run_tool("--packet", self.packet(), "--timeout", "2", "--receipt", receipt, "--",
                               sys.executable, "-c", child)
        self.assertEqual(result.returncode, 124)
        self.assertLess(time.monotonic() - started, 40)
        self.assertTrue(json.loads(receipt.read_text(encoding="utf-8"))["timed_out"])

    def test_output_is_capped_while_it_is_read_and_the_cut_is_recorded(self):
        noisy = [sys.executable, "-c", "import sys\nfor _ in range(200): sys.stdout.write('x' * 10000)"]
        with patch.object(run_contained, "MAX_OUTPUT", 1000):
            code, timed_out, output, truncated = run_contained.run(noisy, b"{}", dict(os.environ), 60)
        self.assertEqual((code, timed_out, len(output), truncated), (0, False, 1000, True))
        receipt = self.base / "receipt.json"
        result = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", *noisy[:2],
                               "import sys\nfor _ in range(150): sys.stdout.write('x' * 10000)")
        self.assertEqual(len(result.stdout), run_contained.MAX_OUTPUT)
        data = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual((data["output_bytes"], data["output_truncated"]), (run_contained.MAX_OUTPUT, True))
        quiet = self.run_tool("--packet", self.packet(), "--receipt", receipt, "--", sys.executable, "-c", "pass")
        self.assertEqual(quiet.returncode, 0)
        self.assertFalse(json.loads(receipt.read_text(encoding="utf-8"))["output_truncated"])

    def test_a_missing_packet_or_command_is_refused(self):
        receipt = self.base / "receipt.json"
        self.assertEqual(self.run_tool("--packet", self.base / "none.json", "--receipt", receipt, "--",
                                       sys.executable, "-c", "pass").returncode, 125)
        self.assertEqual(self.run_tool("--packet", self.packet(), "--receipt", receipt).returncode, 125)
        self.assertEqual(self.run_tool("--packet", self.base / "none.json", "--receipt", receipt, "--",
                                       sys.executable, "-c", "pass", launch=False).returncode, 125)
        self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()
