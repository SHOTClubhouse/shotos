import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import check_release_versions as versions


class ReleaseVersionTests(unittest.TestCase):
    def test_changed_pack_needs_new_version_and_unchanged_pack_can_stay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                                      text=True, check=True).stdout.strip()

            def write(name, value):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding="utf-8")

            def commit():
                git("add", ".")
                git("-c", "commit.gpgsign=false", "commit", "-qm", "fictional release")
                return git("rev-parse", "HEAD")

            git("init", "-q")
            git("config", "user.name", "Release Test")
            git("config", "user.email", "release-test@example.com")
            changed = "packs/changed/.claude-plugin/plugin.json"
            stable = "packs/stable/.claude-plugin/plugin.json"
            write(versions.CORE, json.dumps({"version": "1.0.0"}))
            write(changed, json.dumps({"name": "changed", "version": "1.0.0"}))
            write(stable, json.dumps({"name": "stable", "version": "1.0.0"}))
            previous = commit()
            write(versions.CORE, json.dumps({"version": "1.1.0"}))
            write("CITATION.cff", "version: 1.1.0\n")
            write("CHANGELOG.md", "# Changelog\n\n## 1.1.0 (fictional)\n")
            write("packs/changed/skills/sample/SKILL.md", "# Updated instructions\n")
            candidate = commit()

            with patch.object(versions, "REPO", root):
                self.assertEqual(versions.check(previous, candidate), (
                    ["changed needs a version newer than 1.0.0 for its shipped changes."], 2,
                ))
                write(changed, json.dumps({"name": "changed", "version": "1.1.0"}))
                self.assertEqual(versions.check(previous, commit()), ([], 2))
