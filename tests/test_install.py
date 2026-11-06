import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

INSTALL = Path(__file__).resolve().parents[1] / "install.py"


def run(*args):
    return subprocess.run([sys.executable, str(INSTALL), *args], capture_output=True, text=True)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def install(self, *extra):
        result = run("--runtime", "claude", "--scope", "project", "--target", str(self.root), *extra)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def uninstall(self):
        return run("--uninstall", "--scope", "project", "--target", str(self.root))

    def test_dry_run_changes_nothing(self):
        self.install("--with-hook", "--dry-run")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_install_then_uninstall_restores_the_project(self):
        settings = self.root / ".claude" / "settings.json"
        settings.parent.mkdir()
        settings.write_text(json.dumps({"permissions": {"allow": ["Read"]}}), encoding="utf-8")
        self.install("--with-hook")
        self.assertTrue((self.root / ".claude/skills/report-with-evidence/SKILL.md").is_file())
        self.assertTrue((self.root / ".shotos/tools/claim_check.py").is_file())
        self.assertIn("run_hook.sh", settings.read_text(encoding="utf-8"))
        self.assertEqual((self.root / "CLAUDE.md").read_text(encoding="utf-8"), "@AGENTS.md\n")
        self.assertEqual(self.uninstall().returncode, 0)
        self.assertEqual(json.loads(settings.read_text(encoding="utf-8")), {"permissions": {"allow": ["Read"]}})
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), [".claude"])
        self.assertEqual([p.name for p in (self.root / ".claude").iterdir()], ["settings.json"])

    def test_gemini_and_antigravity_share_the_same_canon_file(self):
        for runtime, skills in (("gemini", ".gemini/skills"), ("antigravity", ".agents/skills")):
            with self.subTest(runtime=runtime):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "GEMINI.md").write_text("# House rules\n", encoding="utf-8")
                    result = run("--runtime", runtime, "--scope", "project", "--target", str(root))
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue((root / skills / "report-with-evidence" / "SKILL.md").is_file())
                    self.assertTrue((root / "AGENTS.md").is_file())
                    self.assertEqual((root / "GEMINI.md").read_text(encoding="utf-8"), "# House rules\n@AGENTS.md\n")
                    self.assertFalse((root / "CLAUDE.md").exists())
                    out = run("--uninstall", "--scope", "project", "--target", str(root))
                    self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
                    self.assertEqual((root / "GEMINI.md").read_text(encoding="utf-8"), "# House rules\n")
                    self.assertFalse((root / skills / "report-with-evidence").exists())

    def test_all_runtimes_in_one_install_share_one_canon_and_uninstall_cleanly(self):
        (self.root / "CLAUDE.md").write_text("# Mine\n", encoding="utf-8")
        result = run("--runtime", "all", "--scope", "project", "--target", str(self.root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in (".claude/skills", ".agents/skills"):
            self.assertTrue((self.root / folder / "report-with-evidence" / "SKILL.md").is_file(), folder)
        self.assertEqual((self.root / "CLAUDE.md").read_text(encoding="utf-8"), "# Mine\n@AGENTS.md\n")
        self.assertEqual((self.root / "GEMINI.md").read_text(encoding="utf-8"), "@AGENTS.md\n")
        self.assertEqual(sum(1 for _ in self.root.glob("AGENTS.md")), 1)
        out = run("--uninstall", "--scope", "project", "--target", str(self.root))
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual((self.root / "CLAUDE.md").read_text(encoding="utf-8"), "# Mine\n")
        self.assertFalse((self.root / "GEMINI.md").exists())
        self.assertFalse((self.root / ".agents").exists())

    def test_codex_reads_agents_md_itself_so_no_import_file_is_made(self):
        result = run("--runtime", "codex", "--scope", "project", "--target", str(self.root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "AGENTS.md").is_file())
        self.assertFalse((self.root / "CLAUDE.md").exists())
        self.assertFalse((self.root / "GEMINI.md").exists())

    def test_user_scope_paths_for_gemini_and_antigravity(self):
        for runtime, skills in (("gemini", ".gemini/skills"), ("antigravity", ".gemini/config/skills")):
            with self.subTest(runtime=runtime):
                with tempfile.TemporaryDirectory() as tmp:
                    result = run("--runtime", runtime, "--scope", "user", "--target", tmp)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue((Path(tmp) / skills / "report-with-evidence" / "SKILL.md").is_file())

    def test_uninstall_restores_existing_files_byte_for_byte(self):
        gitignore = self.root / ".gitignore"
        claude = self.root / "CLAUDE.md"
        gitignore.write_bytes(b"node_modules/\n*.log")
        claude.write_bytes(b"# Mine\r\nline two\r\n")
        settings = self.root / ".claude" / "settings.json"
        settings.parent.mkdir()
        original = b'{"permissions":{"allow":["Read"]}}'
        settings.write_bytes(original)
        self.install("--with-hook")
        self.assertEqual(self.uninstall().returncode, 0)
        self.assertEqual(gitignore.read_bytes(), b"node_modules/\n*.log")
        self.assertEqual(claude.read_bytes(), b"# Mine\r\nline two\r\n")
        self.assertEqual(settings.read_bytes(), original)

    def test_uninstall_removes_a_settings_file_it_created_and_hook_bytecode(self):
        self.install("--with-hook")
        cache = self.root / ".shotos" / "tools" / "__pycache__"
        cache.mkdir()
        (cache / "claim_check.cpython-313.pyc").write_bytes(b"x")
        self.assertEqual(self.uninstall().returncode, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_install_refuses_to_write_through_a_symlink_that_leaves_the_folder(self):
        outside = tempfile.TemporaryDirectory()
        try:
            try:
                (self.root / ".claude").symlink_to(outside.name, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are not available here")
            result = run("--runtime", "claude", "--scope", "project", "--target", str(self.root))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("outside the target folder", result.stdout)
            self.assertEqual(list(Path(outside.name).iterdir()), [])
            self.assertFalse((self.root / ".shotos-install.json").exists())
        finally:
            outside.cleanup()

    def test_all_runtimes_work_in_user_scope_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run("--runtime", "all", "--scope", "user", "--target", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for folder in (".claude/skills", ".agents/skills"):
                self.assertTrue((Path(tmp) / folder / "report-with-evidence" / "SKILL.md").is_file(), folder)

    def test_manifest_uses_relative_paths_only(self):
        self.install()
        manifest = (self.root / ".shotos-install.json").read_text(encoding="utf-8")
        self.assertNotIn(str(self.root), manifest)
        self.assertNotIn(self.root.as_posix(), manifest)

    def test_uninstall_never_touches_paths_outside_the_target(self):
        outside = tempfile.TemporaryDirectory()
        victim = Path(outside.name) / "precious.txt"
        victim.write_text("keep me", encoding="utf-8")
        manifest = {"version": 2, "files": {f"../{Path(outside.name).name}/precious.txt": "x"},
                    "dirs": [f"../{Path(outside.name).name}"]}
        (self.root / ".shotos-install.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.uninstall()
        self.assertTrue(victim.is_file())
        outside.cleanup()

    def test_files_changed_after_install_are_kept(self):
        self.install()
        (self.root / "AGENTS.md").write_text("my own rules\n", encoding="utf-8")
        result = self.uninstall()
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "my own rules\n")
        self.assertIn("changed since install", result.stdout)

    def test_existing_claude_md_gets_one_import_line_removed_on_uninstall(self):
        (self.root / "CLAUDE.md").write_text("# House rules\n", encoding="utf-8")
        self.install()
        self.assertEqual((self.root / "CLAUDE.md").read_text(encoding="utf-8"), "# House rules\n@AGENTS.md\n")
        self.uninstall()
        self.assertEqual((self.root / "CLAUDE.md").read_text(encoding="utf-8"), "# House rules\n")

    def test_work_folder_is_ignored_and_the_line_removed_on_uninstall(self):
        (self.root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        self.install()
        self.assertIn(".work/", (self.root / ".gitignore").read_text(encoding="utf-8").splitlines())
        self.uninstall()
        self.assertEqual((self.root / ".gitignore").read_text(encoding="utf-8"), "node_modules/\n")

    def test_settings_that_are_not_plain_json_stop_the_install_before_any_change(self):
        settings = self.root / ".claude" / "settings.json"
        settings.parent.mkdir()
        settings.write_text('{ // a comment\n "a": 1 }', encoding="utf-8")
        result = run("--runtime", "claude", "--scope", "project", "--target", str(self.root), "--with-hook")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), [".claude"])
        self.assertFalse((self.root / ".shotos-install.json").exists())

    def test_existing_agents_file_is_never_overwritten(self):
        (self.root / "AGENTS.md").write_text("mine", encoding="utf-8")
        self.install()
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "mine")


    def test_packs_and_agents_install_and_uninstall_cleanly(self):
        packs = sorted(p.name for p in (INSTALL.parent / "packs").iterdir() if (p / "skills").is_dir())
        if not packs:
            self.skipTest("no packs yet")
        self.install("--all-packs", "--with-agents")
        for pack in packs:
            for skill in (INSTALL.parent / "packs" / pack / "skills").iterdir():
                self.assertTrue((self.root / ".claude/skills" / skill.name / "SKILL.md").is_file(), skill.name)
        self.assertTrue((self.root / ".claude/agents/qa-lead.md").is_file())
        self.assertFalse((self.root / ".claude/agents/README.md").exists())
        self.assertTrue((self.root / ".shotos/docs/connect-your-tools.md").is_file())
        for pack in packs:
            if (INSTALL.parent / "packs" / pack / "scripts").is_dir():
                self.assertTrue((self.root / ".shotos/packs" / pack / "scripts").is_dir(), pack)
        self.assertEqual(self.uninstall().returncode, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unknown_pack_is_refused_before_any_change(self):
        result = run("--runtime", "claude", "--scope", "project", "--target", str(self.root), "--pack", "no-such-pack")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown pack", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_list_packs_runs(self):
        result = run("--list-packs")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
