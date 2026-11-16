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

    def test_reinstalling_keeps_a_check_someone_added(self):
        install_hooks.install(self.repo, python="/fictional/old/python")
        with self.hook.open("a", encoding="utf-8", newline="\n") as hook:
            hook.write("echo fictional extra check\n")
        install_hooks.install(self.repo, python="/fictional/new/python")
        text = self.hook.read_text(encoding="utf-8")
        self.assertIn("echo fictional extra check", text)
        self.assertIn("/fictional/new/python", text)
        self.assertNotIn("/fictional/old/python", text)
        self.assertEqual(text.count(install_hooks.BEGIN), 1)
        self.assertIn("Removed the SHOTos block", install_hooks.uninstall(self.repo))
        text = self.hook.read_text(encoding="utf-8")
        self.assertEqual(text, "#!/bin/sh\necho fictional extra check\n")

    def test_a_check_added_inside_the_block_is_never_removed_silently(self):
        install_hooks.install(self.repo, python="/fictional/old/python")
        text = self.hook.read_text(encoding="utf-8")
        changed = text.replace(install_hooks.END, "mandatory_extra_check || exit 1\n" + install_hooks.END)
        self.hook.write_text(changed, encoding="utf-8", newline="\n")
        with self.assertRaises(SystemExit) as refused:
            install_hooks.install(self.repo, python="/fictional/new/python")
        self.assertIn("changed by hand", str(refused.exception))
        with self.assertRaises(SystemExit):
            install_hooks.uninstall(self.repo)
        self.assertEqual(self.hook.read_text(encoding="utf-8"), changed)
        install_hooks.install(self.repo, force=True, python="/fictional/new/python")
        self.assertEqual(self.hook.with_name("pre-push.before-shotos").read_text(encoding="utf-8"), changed)
        self.assertNotIn("mandatory_extra_check", self.hook.read_text(encoding="utf-8"))
        self.assertIn("/fictional/new/python", self.hook.read_text(encoding="utf-8"))
        # A block saved with Windows line endings is still recognised as unchanged.
        crlf = self.hook.read_text(encoding="utf-8").replace("\n", "\r\n")
        self.hook.write_bytes(crlf.encode("utf-8"))
        self.assertIn("Updated the SHOTos block", install_hooks.install(self.repo))

    def test_a_hook_from_the_earlier_installer_is_updated_only_when_unchanged(self):
        self.hook.parent.mkdir(parents=True, exist_ok=True)
        legacy = ("#!/bin/sh\n" + install_hooks.MARKER + "\n# Runs the SHOTos gate in fast mode before each push. "
                  "Git passes the refs being pushed on standard input.\ncd \"$(git rev-parse --show-toplevel)\" || "
                  "exit 1\nPYTHON=\"/fictional/python\"\n[ -x \"$PYTHON\" ] || PYTHON=\"$(command -v python3 || "
                  "command -v python)\"\nexec \"$PYTHON\" tools/local_gate.py --pre-push\n")
        self.hook.write_text(legacy, encoding="utf-8", newline="\n")
        install_hooks.install(self.repo)
        self.assertIn(install_hooks.BEGIN, self.hook.read_text(encoding="utf-8"))
        self.hook.write_text(legacy + "echo fictional extra check\n", encoding="utf-8", newline="\n")
        with self.assertRaises(SystemExit):
            install_hooks.install(self.repo)
        with self.assertRaises(SystemExit):
            install_hooks.uninstall(self.repo)
        self.assertIn("fictional extra check", self.hook.read_text(encoding="utf-8"))
        install_hooks.install(self.repo, force=True)
        self.assertIn("fictional extra check",
                      self.hook.with_name("pre-push.before-shotos").read_text(encoding="utf-8"))

    @unittest.skipUnless(shutil.which("sh") or sys.platform == "win32", "needs a shell for Git hooks")
    def test_a_check_after_the_block_runs_and_reads_the_pushed_refs(self):
        origin = Path(self.tmp.name) / "origin.git"
        git(Path(self.tmp.name), "init", "-q", "--template=", "--bare", str(origin))
        git(self.repo, "remote", "add", "origin", str(origin))
        stub = self.repo / "tools" / "local_gate.py"
        stub.parent.mkdir()
        stub.write_text("import sys\nsys.stdin.read()\nsys.exit(0)\n", encoding="utf-8")  # a fictional GO
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-qm", "Fictional commit")
        install_hooks.install(self.repo)
        self.assertEqual(git(self.repo, "push", "-q", "origin", "main", check=False).returncode, 0)
        with self.hook.open("a", encoding="utf-8", newline="\n") as hook:
            hook.write("cat > extra.txt\nexit 1\n")
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "Another fictional commit")
        pushed = git(self.repo, "push", "origin", "main", check=False)
        self.assertNotEqual(pushed.returncode, 0)
        self.assertIn("refs/heads/main", (self.repo / "extra.txt").read_text(encoding="utf-8"))

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
