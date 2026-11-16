import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packs/setup/scripts/config-as-code"))

import drift_check  # noqa: E402


def put(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def snapshot(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


class DriftCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "repo"
        self.installed = Path(tmp.name) / "installed"
        self.repo.mkdir()
        self.installed.mkdir()

    def run_cli(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = drift_check.main(["--repo", str(self.repo), "--installed", str(self.installed), *extra])
        return code, out.getvalue()


class TestDrift(DriftCase):
    def test_identical_folders_have_no_drift(self):
        put(self.repo, "rules/a.md", "one")
        put(self.installed, "rules/a.md", "one")
        code, out = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("No drift.", out)

    def test_three_kinds_are_reported_and_nothing_is_changed(self):
        for root in (self.repo, self.installed):
            put(root, "same.md", "x")
        put(self.repo, "only-repo.md", "r")
        put(self.installed, "only-installed.md", "i")
        put(self.repo, "diff.md", "new")
        put(self.installed, "diff.md", "old")
        before = (snapshot(self.repo), snapshot(self.installed))
        code, out = self.run_cli("--json")
        self.assertEqual(code, 1)
        kinds = {(f["kind"], f["path"]) for f in json.loads(out)["findings"]}
        self.assertEqual(kinds, {("only-in-repo", "only-repo.md"), ("only-in-installed", "only-installed.md"),
                                 ("differs", "diff.md")})
        self.assertEqual((snapshot(self.repo), snapshot(self.installed)), before)

    def test_a_touched_but_unchanged_file_is_not_drift(self):
        put(self.repo, "a.md", "same")
        put(self.installed, "a.md", "same")
        os.utime(self.installed / "a.md", (1_000_000_000, 1_000_000_000))
        self.assertEqual(self.run_cli()[0], 0)

    def test_the_time_hint_names_the_newer_side(self):
        put(self.repo, "a.md", "new")
        put(self.installed, "a.md", "old")
        os.utime(self.repo / "a.md", (1_000_000_000, 1_000_000_000))
        code, out = self.run_cli()
        self.assertEqual(code, 1)
        self.assertIn("DIFFERS:            a.md (installed newer)", out)

    def test_contrary_caches_logs_and_machine_only_files_are_ignored(self):
        put(self.installed, "logs/run.log", "noise")
        put(self.installed, "skills/intake/__pycache__/x.cpython-313.pyc", "noise")
        put(self.installed, "skills/intake/logs/today.txt", "noise")
        put(self.installed, "settings.local.json", "machine only")
        self.assertEqual(self.run_cli()[0], 1)
        self.assertEqual(self.run_cli("--ignore", "*.local.json")[0], 0)

    def test_an_ignore_file_is_read(self):
        put(self.installed, "secrets.env", "TOKEN=x")
        ignore = self.repo.parent / "ignore.txt"
        ignore.write_text("# machine only\n*.env\n", encoding="utf-8")
        self.assertEqual(self.run_cli("--ignore-file", str(ignore))[0], 0)

    def test_map_compares_differently_named_folders_and_skips_the_rest(self):
        put(self.repo, "rules/a.md", "x")
        put(self.installed, "installed-rules/a.md", "y")
        put(self.installed, "unmanaged/notes.md", "not part of the setup")
        code, out = self.run_cli("--map", "rules=installed-rules", "--json")
        self.assertEqual(code, 1)
        self.assertEqual([(f["kind"], f["path"]) for f in json.loads(out)["findings"]], [("differs", "rules/a.md")])

    def test_a_mapped_folder_missing_on_one_side_is_drift(self):
        put(self.repo, "rules/a.md", "x")
        code, out = self.run_cli("--map", "rules=rules", "--json")
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["findings"], [{"kind": "only-in-repo", "path": "rules/"}])

    def test_missing_folders_are_an_error_not_a_clean_result(self):
        self.installed.rmdir()
        self.assertEqual(self.run_cli()[0], 2)
        self.installed.mkdir()
        self.assertEqual(self.run_cli("--map", "nothing=nothing")[0], 2)
        self.assertEqual(self.run_cli("--map", "no-equals-sign")[0], 2)


if __name__ == "__main__":
    unittest.main()
