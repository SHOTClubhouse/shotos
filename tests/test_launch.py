import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import launch  # noqa: E402
import release  # noqa: E402

SHIM = r"D:\tools\npm\claude.cmd"


class LaunchableTests(unittest.TestCase):
    def test_a_cmd_shim_is_launched_through_cmd_exe_with_the_arguments_quoted(self):
        with patch("shutil.which", return_value=SHIM) as which, patch.object(launch, "WINDOWS", True):
            line = launch.launchable(["claude", "plugin", "validate", "."])
        which.assert_called_once_with("claude")
        self.assertEqual(line, f'cmd.exe /d /s /c "{SHIM} plugin validate ."')

    def test_a_bat_shim_with_spaces_in_its_path_and_arguments_is_quoted(self):
        shim = r"C:\Program Files\gh\gh.BAT"
        with patch("shutil.which", return_value=shim), patch.object(launch, "WINDOWS", True):
            line = launch.launchable(["gh", "release", "create", "--title", "SHOTos v1.0"])
        self.assertEqual(line, 'cmd.exe /d /s /c ""C:\Program Files\gh\gh.BAT" release create --title "SHOTos v1.0""')

    def test_an_argument_cmd_would_read_as_syntax_is_refused_for_a_shim(self):
        with patch("shutil.which", return_value=SHIM), patch.object(launch, "WINDOWS", True):
            for bad in ("a&calc", "%PATH%", "x|y", 'say "hi"', "a\nb", "^x", "a>b", "f(x)", "(", ")"):
                with self.subTest(bad=bad), self.assertRaises(launch.UnsafeArgument):
                    launch.launchable(["claude", bad])

    def test_a_real_executable_is_passed_as_a_list_with_its_resolved_path(self):
        with patch("shutil.which", return_value=r"C:\Git\cmd\git.exe"), patch.object(launch, "WINDOWS", True):
            self.assertEqual(launch.launchable(["git", "-C", "x", "status"]), [r"C:\Git\cmd\git.exe", "-C", "x", "status"])

    def test_a_cmd_file_is_an_ordinary_program_off_windows(self):
        with patch("shutil.which", return_value="/opt/tool.cmd"), patch.object(launch, "WINDOWS", False):
            self.assertEqual(launch.launchable(["tool", "a&b"]), ["/opt/tool.cmd", "a&b"])

    def test_a_missing_tool_is_named_plainly(self):
        with patch("shutil.which", return_value=None):
            with self.assertRaises(launch.MissingTool) as caught:
                launch.launchable(["gh", "release", "view"])
        self.assertIn("`gh` is not installed or is not on PATH", str(caught.exception))
        self.assertIsInstance(caught.exception, OSError)


class ReleaseRunTests(unittest.TestCase):
    def test_release_run_launches_a_cmd_shim_through_cmd_exe(self):
        done = subprocess.CompletedProcess([], 0, stdout="ok\n", stderr="")
        with patch("shutil.which", return_value=SHIM), patch.object(launch, "WINDOWS", True), \
                patch("subprocess.run", return_value=done) as run:
            self.assertEqual(release.run("claude", "plugin", "validate", "."), "ok")
        self.assertEqual(run.call_args.args[0], f'cmd.exe /d /s /c "{SHIM} plugin validate ."')
        self.assertNotIn("shell", run.call_args.kwargs)

    def test_a_resolved_shim_path_cmd_would_read_as_syntax_is_refused_and_never_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "ran.txt"
            paths = (r"C:\missing&ver&rem\gh.cmd", r"C:\%TEMP%\gh.cmd",
                     r"C:\x&echo.>" + str(marker) + r"&rem\gh.cmd")
            for path in paths:
                with self.subTest(path=path), patch("shutil.which", return_value=path), \
                        patch.object(launch, "WINDOWS", True), self.assertRaises(launch.UnsafeArgument) as caught:
                    release.run("gh", "release", "view")
                self.assertIn("so it was not run", str(caught.exception))
            self.assertFalse(marker.exists())

    def test_an_argument_with_parentheses_is_refused_and_never_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "ran.txt"
            shim = Path(tmp) / "tool.cmd"
            shim.write_text(f'@echo ran> "{marker}"\r\n', encoding="utf-8")
            with patch("shutil.which", return_value=str(shim)), patch.object(launch, "WINDOWS", True):
                for bad in ("(echo hi)", "a)b", "(x"):
                    with self.subTest(bad=bad), self.assertRaises(launch.UnsafeArgument):
                        release.run("tool", bad)
            self.assertFalse(marker.exists())

    def test_release_run_names_a_missing_tool_instead_of_winerror_2(self):
        with patch("shutil.which", return_value=None), patch("subprocess.run") as run:
            with self.assertRaises(launch.MissingTool) as caught:
                release.run("gh", "release", "view", "v1.0.0", check=False)
        run.assert_not_called()
        self.assertIn("`gh` is not installed", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
