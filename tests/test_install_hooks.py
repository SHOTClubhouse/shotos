import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import install_hooks  # noqa: E402


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


class InstallHooksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "work"
        git(Path(self.tmp.name), "init", "-q", "--template=", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.name", "Hook Test")
        git(self.repo, "config", "user.email", "hook-test@example.com")
        git(self.repo, "config", "core.hooksPath", ".git/hooks")
        self.hook = self.repo / ".git" / "hooks" / "pre-push"

    def tearDown(self):
        self.tmp.cleanup()

    def test_installs_a_hook_that_runs_the_fast_gate(self):
        install_hooks.install(self.repo)
        text = self.hook.read_bytes().decode("utf-8")
        self.assertNotIn("\r\n", text)
        self.assertIn(install_hooks.MARKER, text)
        self.assertIn("tools/local_gate.py --pre-push", text)
        install_hooks.install(self.repo)  # running it again is fine

    def test_keeps_a_hook_it_did_not_write_unless_forced(self):
        self.hook.parent.mkdir(parents=True, exist_ok=True)
        self.hook.write_text("#!/bin/sh\necho earlier hook\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            install_hooks.install(self.repo)
        install_hooks.install(self.repo, force=True)
        self.assertIn("earlier hook", self.hook.with_name("pre-push.before-shotos").read_text(encoding="utf-8"))
        self.assertIn("put the earlier hook back", install_hooks.uninstall(self.repo))
        self.assertIn("earlier hook", self.hook.read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):
            install_hooks.uninstall(self.repo)

    @unittest.skipUnless(shutil.which("sh") or sys.platform == "win32", "needs a shell for Git hooks")
    def test_a_no_go_from_the_gate_stops_the_push(self):
        origin = Path(self.tmp.name) / "origin.git"
        git(Path(self.tmp.name), "init", "-q", "--template=", "--bare", str(origin))
        git(self.repo, "remote", "add", "origin", str(origin))
        stub = self.repo / "tools" / "local_gate.py"
        stub.parent.mkdir()
        # A fictional gate that records what Git passed it, then says NO-GO.
        stub.write_text("import sys\nopen('pushed.txt', 'w').write(sys.stdin.read() + ' '.join(sys.argv[1:]))\n"
                        "sys.exit(1)\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "Fictional commit")
        install_hooks.install(self.repo)
        pushed = git(self.repo, "push", "origin", "main", check=False)
        self.assertNotEqual(pushed.returncode, 0)
        self.assertEqual(git(origin, "branch", "--list", "main").stdout, "")
        record = (self.repo / "pushed.txt").read_text(encoding="utf-8")
        self.assertIn("refs/heads/main", record)
        self.assertTrue(record.endswith("--pre-push"))


if __name__ == "__main__":
    unittest.main()
