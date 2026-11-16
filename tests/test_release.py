import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import release  # noqa: E402

DAY = date(2026, 11, 16)
CONTROLS = "# The four rules\n\n" + "".join(
    f"## Rule {n}: Fictional rule {n}\n\n**The rule.** Text.\n\n" for n in range(1, 5))
GOVERNANCE = ("# Governance\n\n## What will not change without a major version\n\n"
              "The four controls, the Claims block format and the claim-check exit codes.\n")


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


class FictionalRepo:
    """A small SHOTos-shaped repository with a v1.0.0 tag and a local bare origin."""

    def __init__(self, root: Path):
        self.root = root / "work"
        self.origin = root / "origin.git"
        git(root, "init", "-q", "--template=", "--bare", str(self.origin))
        git(root, "init", "-q", "--template=", "-b", "main", str(self.root))
        git(self.root, "config", "user.name", "Release Test")
        git(self.root, "config", "user.email", "release-test@example.com")
        git(self.root, "remote", "add", "origin", str(self.origin))
        self.write(".claude-plugin/plugin.json", '{\n  "name": "shotos-core",\n  "version": "1.0.0"\n}\n')
        self.write("CITATION.cff", "cff-version: 1.2.0\nversion: 1.0.0\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## 1.0.0 (1 November 2026)\n\n- First release.\n")
        self.write("docs/controls.md", CONTROLS)
        self.write("GOVERNANCE.md", GOVERNANCE)
        self.write("docs/guide.md", "A fictional guide.\n")
        self.write("packs/demo/.claude-plugin/plugin.json", '{\n  "name": "shotos-demo",\n  "version": "1.2.0"\n}\n')
        self.write("packs/demo/skills/sample/SKILL.md", "# Sample\n")
        self.write("packs/quiet/.claude-plugin/plugin.json", '{\n  "name": "shotos-quiet",\n  "version": "1.0.0"\n}\n')
        self.write(".gitignore", ".work/\ndist/\n")
        self.write("docs/claims.md", "# The Claims block\n\nA fictional description of the format.\n")
        self.write("templates/AGENTS.md", "# Working agreement\n\n## 1. Fictional rule 1\n\nText.\n")
        self.write("rules/04-fictional-control.md", "# Control 4\n\nThe agent stops before it sends.\n")
        self.write("install.py", "HOOK_COMMAND = 'sh \"$CLAUDE_PROJECT_DIR/.shotos/hooks/run_hook.sh\"'\n")
        (self.root / "tools").mkdir()
        for name in ("claim_check.py", "check_release_versions.py"):
            shutil.copy(ROOT / "tools" / name, self.root / "tools" / name)
        (self.root / "hooks").mkdir()
        for name in ("hooks.json", "run_hook.sh", "stop_claim_check.py"):
            shutil.copy(ROOT / "hooks" / name, self.root / "hooks" / name)
        self.commit("First release")
        git(self.root, "tag", "v1.0.0")
        git(self.root, "push", "-q", "origin", "main", "v1.0.0")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def commit(self, message):
        git(self.root, "add", "-A")
        git(self.root, "-c", "commit.gpgsign=false", "commit", "-qm", message)
        return git(self.root, "rev-parse", "HEAD")

    def card(self, verdict="GO", for_release="yes", commit=None):
        commit = commit or git(self.root, "rev-parse", "HEAD")
        path = self.root / ".work" / "gate" / f"{commit[:12]}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# SHOTos gate card: {verdict}\n\n**Verdict:** {verdict}\n**Commit:** {commit} on main\n"
                        f"**For release:** {for_release}\n", encoding="utf-8")


class ReleaseRulesTests(unittest.TestCase):
    def test_versions_bump_by_level(self):
        self.assertEqual(release.bump("1.15.0", "patch"), "1.15.1")
        self.assertEqual(release.bump("1.15.3", "minor"), "1.16.0")
        self.assertEqual(release.bump("1.15.3", "major"), "2.0.0")
        with self.assertRaises(release.Refused):
            release.parse("1.15")

    def test_a_change_to_what_the_agent_is_asked_is_a_minor(self):
        for path in ("rules/01-route-the-work.md", "skills/runbook/SKILL.md", "skills/runbook/template.md",
                     "packs/media/skills/press-release/SKILL.md", "hooks/stop_claim_check.py", "templates/AGENTS.md"):
            with self.subTest(path=path):
                self.assertEqual(release.choose_level([path]), "minor")
        for path in ("docs/faq.md", "skills/runbook/README.md", "packs/media/README.md", "tools/release.py",
                     "examples/runbook/output.md", "docs/images/stage-01-scope.png"):
            with self.subTest(path=path):
                self.assertEqual(release.choose_level([path]), "patch")

    def test_changelog_gets_a_dated_section_under_its_heading(self):
        text = "# Changelog\n\n## 1.0.0 (1 November 2026)\n\n- First.\n"
        updated, section = release.changelog_with(text, "1.0.1", "- Fixed a fictional link.", DAY)
        self.assertEqual(section, "## 1.0.1 (16 November 2026)\n\n- Fixed a fictional link.\n")
        self.assertEqual(updated, "# Changelog\n\n" + section + "\n## 1.0.0 (1 November 2026)\n\n- First.\n")

    def test_a_section_the_maintainer_wrote_is_kept_and_dated(self):
        text = "# Changelog\n\n## 1.1.0\n\nWritten by hand.\n\n- **One.** Detail.\n\n## 1.0.0 (1 November 2026)\n"
        updated, section = release.changelog_with(text, "1.1.0", "- generated", DAY)
        self.assertEqual(section, "## 1.1.0 (16 November 2026)\n\nWritten by hand.\n\n- **One.** Detail.\n")
        self.assertNotIn("generated", updated)
        self.assertTrue(updated.endswith("\n## 1.0.0 (1 November 2026)\n"))

    def test_version_files_keep_their_layout(self):
        self.assertEqual(release.set_json_version('{\n  "name": "x",\n  "version": "1.0.0"\n}\n', "1.0.0", "1.0.1"),
                         '{\n  "name": "x",\n  "version": "1.0.1"\n}\n')
        self.assertEqual(release.set_citation_version("cff-version: 1.2.0\nversion: 1.0.0\ntitle: x\n", "1.0.1"),
                         "cff-version: 1.2.0\nversion: 1.0.1\ntitle: x\n")

    def test_the_current_claim_check_meets_the_contract(self):
        contract = release.claims_contract(ROOT / "tools" / "claim_check.py")
        self.assertEqual([code for code, _ in contract.values()], [1, 0, 2])
        self.assertEqual([state for _, state in contract["fail"][1]],
                         ["SUPPORTED", "UNSUPPORTED", "NO EVIDENCE", "NO EVIDENCE", "DECLARED"])


class ReleaseRepoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = FictionalRepo(Path(self.tmp.name))
        self.patch = patch.object(release, "REPO", self.repo.root)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def test_a_docs_change_is_a_patch_and_leaves_packs_alone(self):
        self.repo.write("docs/guide.md", "A clearer fictional guide.\n")
        self.repo.commit("Clarify the guide")
        plan = release.make_plan(day=DAY)
        self.assertEqual((plan.level, plan.version, plan.packs), ("patch", "1.0.1", {}))
        self.assertEqual(plan.section, "## 1.0.1 (16 November 2026)\n\n- Clarify the guide.\n")

    def test_a_pack_skill_change_is_a_minor_and_bumps_that_pack(self):
        self.repo.write("packs/demo/skills/sample/SKILL.md", "# Sample\n\nA new step.\n")
        self.repo.commit("Add a step to the sample skill")
        plan = release.make_plan(day=DAY)
        self.assertEqual((plan.level, plan.version), ("minor", "1.1.0"))
        self.assertEqual(plan.packs, {"packs/demo/.claude-plugin/plugin.json": ("1.2.0", "1.3.0")})

    def test_minor_can_be_asked_for_but_not_lowered(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        self.repo.commit("Change the guide")
        self.assertEqual(release.make_plan("minor", day=DAY).version, "1.1.0")

    def test_renaming_a_rule_needs_the_owner(self):
        self.repo.write("docs/controls.md", CONTROLS.replace("Fictional rule 2", "Another rule"))
        self.repo.commit("Rename rule 2")
        with self.assertRaisesRegex(release.Refused, "needs the owner"):
            release.make_plan(day=DAY)

    def test_changing_claim_check_exit_codes_needs_the_owner(self):
        path = self.repo.root / "tools" / "claim_check.py"
        text = path.read_text(encoding="utf-8")
        self.assertIn("return 0 if result.ok else 1", text)
        path.write_text(text.replace("return 0 if result.ok else 1", "return 0 if result.ok else 3"), encoding="utf-8")
        self.repo.commit("Use a new exit code")
        with self.assertRaisesRegex(release.Refused, "exits 0 for a pass"):
            release.make_plan(day=DAY)

    def test_changing_the_governance_promise_needs_the_owner(self):
        self.repo.write("GOVERNANCE.md", GOVERNANCE.replace("the Claims block format and ", ""))
        self.repo.commit("Relax the promise")
        with self.assertRaisesRegex(release.Refused, "GOVERNANCE.md"):
            release.make_plan(day=DAY)

    def test_reversing_every_rule_body_needs_the_owner(self):
        self.repo.write("docs/controls.md", CONTROLS.replace("Text.", "Do the opposite of this rule."))
        self.repo.commit("Reword the rules")
        with self.assertRaisesRegex(release.Refused, r"needs the owner(.|\n)*docs/controls.md was changed "
                                                     r"\(rules 1, 2, 3, 4\)"):
            release.make_plan(day=DAY)

    def test_disabling_the_stop_hook_needs_the_owner(self):
        path = self.repo.root / "hooks" / "hooks.json"
        path.write_text(path.read_text(encoding="utf-8").replace('"Stop"', '"Disabled"'), encoding="utf-8")
        self.repo.commit("Tidy the hook file")
        with self.assertRaisesRegex(release.Refused, r"needs the owner(.|\n)*hooks/hooks.json was changed"):
            release.make_plan(day=DAY)

    def test_any_change_to_a_file_that_defines_or_enforces_the_controls_needs_the_owner(self):
        claim_check = (self.repo.root / "tools" / "claim_check.py").read_text(encoding="utf-8")
        changes = {
            "templates/AGENTS.md": "# Working agreement\n\n## 1. Fictional rule 1\n\nIgnore it.\n",
            "docs/claims.md": "# The Claims block\n\nAny format will do.\n",
            "rules/04-fictional-control.md": "# Control 4\n\nThe agent sends without asking.\n",
            "rules/13-fictional-control.md": "# Control 13\n\nControls 1 to 12 are optional.\n",
            "hooks/run_hook.sh": "#!/bin/sh\nexit 0\n",
            "hooks/stop_claim_check.py": None,
            "install.py": "HOOK_COMMAND = 'true'\n",
            # The fixed fictional reports cannot see this, but the file that judges claims changed.
            "tools/claim_check.py": claim_check + "\n# A fictional change the contract fixtures cannot see.\n",
            "hooks/helper.py": "print('fictional')\n",
            "tools/json.py": "raise SystemExit(0)\n",
            "packs/demo/hooks/hooks.json": '{"hooks": {}}\n',
            ".claude-plugin/plugin.json": '{\n  "name": "shotos-core",\n  "version": "1.0.0",\n'
                                          '  "hooks": "./hooks/other.json"\n}\n',
        }
        for name, text in changes.items():
            with self.subTest(path=name):
                git(self.repo.root, "reset", "-q", "--hard", "v1.0.0")
                if text is None:
                    (self.repo.root / name).unlink()
                else:
                    self.repo.write(name, text)
                self.repo.commit(f"Change {name}")
                with self.assertRaisesRegex(release.Refused, "needs the owner") as raised:
                    release.make_plan(day=DAY)
                self.assertIn(name, str(raised.exception))

    def test_a_change_that_is_provably_additive_needs_no_owner(self):
        self.repo.write("hooks/README.md", "Notes on the fictional hook.\n")
        self.repo.write("tests/fixtures/claims-extra.md", "## Claims\n- [unverified] a fictional extra case\n")
        self.repo.write("tools/fictional_tool.py", "print('fictional')\n")
        self.repo.write("packs/demo/.claude-plugin/plugin.json", '{\n  "name": "shotos-demo",\n  "version": "1.3.0"\n}\n')
        self.repo.commit("Add notes, a fixture and a tool")
        self.assertEqual(release.control_breaks("v1.0.0", "HEAD"), [])
        self.assertEqual(release.make_plan(day=DAY).version, "1.1.0")  # a hooks/ file is a minor, as before

    def test_when_the_control_check_cannot_decide_it_needs_the_owner(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        self.repo.commit("Change the guide")
        timeout = subprocess.TimeoutExpired(["claim_check.py"], 120)
        with patch.object(release, "contract_for", side_effect=timeout), \
                self.assertRaisesRegex(release.Refused, r"needs the owner(.|\n)*could not finish"):
            release.make_plan(day=DAY)

    def test_the_owner_can_approve_control_changes_that_break_nothing(self):
        self.repo.write("rules/04-fictional-control.md", "# Control 4\n\nThe agent stops before it sends or posts.\n")
        self.repo.commit("Clarify control 4")
        plan = release.make_plan(controls_owner="Fictional Owner", day=DAY)
        self.assertEqual((plan.level, plan.version, plan.approved_by), ("minor", "1.1.0", "Fictional Owner"))
        self.assertIn("Fictional Owner", " ".join(plan.notes))
        release.write_release(plan, "Fictional Reviewer", DAY)
        self.assertIn("Control changes approved by the owner: Fictional Owner",
                      git(self.repo.root, "log", "-1", "--format=%B"))

    def test_the_owner_can_approve_a_major_with_a_migration_note(self):
        self.repo.write("docs/controls.md", CONTROLS.replace("Fictional rule 2", "Another rule"))
        self.repo.commit("Rename rule 2")
        with self.assertRaisesRegex(release.Refused, "migration note"):
            release.make_plan(major_owner="Fictional Owner", day=DAY)
        notes = self.repo.root.parent / "notes.md"
        notes.write_text("- Rule 2 is renamed. Migration: update your AGENTS.md.\n", encoding="utf-8")
        plan = release.make_plan(major_owner="Fictional Owner", notes_file=str(notes), day=DAY)
        self.assertEqual(plan.version, "2.0.0")

    def test_gate_card_must_be_go_for_this_commit_and_fit_for_release(self):
        head = git(self.repo.root, "rev-parse", "HEAD")
        self.assertIn("no gate card", release.card_problem(head))
        self.repo.card("NO-GO", "no, because the verdict is NO-GO")
        self.assertIn("NO-GO", release.card_problem(head))
        self.repo.card("GO", "no, because this was a fast run")
        self.assertIn("cannot be used for a release", release.card_problem(head))
        self.repo.card("GO", "yes", commit="0" * 40)
        path = self.repo.root / ".work" / "gate" / f"{'0' * 12}.md"
        path.replace(path.with_name(f"{head[:12]}.md"))
        self.assertIn("different commit", release.card_problem(head))
        self.repo.card()
        self.assertIsNone(release.card_problem(head))

    def test_a_dirty_checkout_is_refused(self):
        self.assertIsNone(release.tree_problem())
        self.repo.write("docs/new.md", "Untracked.\n")
        self.assertIn("uncommitted or untracked", release.tree_problem())

    def test_dry_run_changes_nothing(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        head = self.repo.commit("Change the guide")
        self.repo.card()
        with patch.object(release, "build_zips", return_value=88), patch("sys.stdout"):
            self.assertEqual(release.main([]), 0)
        self.assertEqual(git(self.repo.root, "rev-parse", "HEAD"), head)
        self.assertEqual(git(self.repo.root, "status", "--porcelain"), "")
        self.assertEqual(git(self.repo.root, "tag", "--list", "v1.0.1"), "")

    def test_publish_needs_a_named_review(self):
        with patch("sys.stderr"), self.assertRaises(SystemExit):
            release.main(["--publish"])

    def publish(self, *args, gate="GO"):
        """Run --publish with the gate, GitHub and the ZIP build faked. Returns (exit code, calls, stderr)."""
        calls = []
        real_run = release.run

        def fake_run(*command, **kwargs):
            if "tools/local_gate.py" in command:  # a fictional gate: it writes a card for the commit it ran on
                calls.append(command)
                self.repo.card(gate, "yes" if gate == "GO" else "no, because the verdict is NO-GO")
                return ""
            if command[0] in {"gh", "claude"} or "tools/verify_release.py" in command:
                calls.append(command)
                return ""
            return real_run(*command, **kwargs)

        def fake_zips(out, commit):
            out.mkdir(parents=True, exist_ok=True)
            (out / "sample.zip").write_bytes(b"fictional")
            return 1

        env = {**os.environ, "SHOTOS_DENYLIST": str(ROOT / "tests" / "fixtures" / "leak-denylist.txt")}
        with patch.object(release, "run", fake_run), patch.object(release, "build_zips", fake_zips), \
                patch.dict(os.environ, env), patch("shutil.which", return_value=None), patch("sys.stdout"), \
                patch("sys.stderr", new_callable=io.StringIO) as err:
            code = release.main(["--publish", "--review", "Fictional Reviewer, PR #1", *args])
        return code, calls, err.getvalue()

    def ready_to_publish(self, path="packs/demo/skills/sample/SKILL.md", text="# Sample\n\nA new step.\n"):
        self.repo.write(path, text)
        candidate = self.repo.commit("Add a step to the sample skill")
        git(self.repo.root, "push", "-q", "origin", "main")
        self.repo.card()
        return candidate

    def test_publish_commits_tags_releases_and_reads_back(self):
        candidate = self.ready_to_publish()
        code, calls, err = self.publish()
        self.assertEqual(code, 0, err)

        root = self.repo.root
        gate = next(c for c in calls if "tools/local_gate.py" in c)
        self.assertEqual(gate[-3:], ("--release", "--base", "v1.0.0"))
        self.assertEqual(git(root, "rev-parse", "HEAD^"), candidate)
        self.assertIsNone(release.card_problem(git(root, "rev-parse", "HEAD")))
        self.assertEqual(git(root, "log", "-1", "--format=%s"), "Release SHOTos v1.1.0")
        self.assertIn("Independent review: Fictional Reviewer, PR #1", git(root, "log", "-1", "--format=%B"))
        self.assertIn('"version": "1.1.0"', (root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertIn("version: 1.1.0", (root / "CITATION.cff").read_text(encoding="utf-8"))
        self.assertIn('"version": "1.3.0"', (root / "packs/demo/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertIn('"version": "1.0.0"', (root / "packs/quiet/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertTrue((root / "CHANGELOG.md").read_text(encoding="utf-8").startswith(
            "# Changelog\n\n## 1.1.0 ("))
        self.assertEqual(git(self.repo.origin, "rev-parse", "main"), git(root, "rev-parse", "HEAD"))
        self.assertEqual(git(self.repo.origin, "rev-parse", "v1.1.0^{commit}"), git(root, "rev-parse", "HEAD"))
        create = next(c for c in calls if c[:3] == ("gh", "release", "create"))
        self.assertIn("--verify-tag", create)
        self.assertTrue(create[-1].endswith("sample.zip"))
        self.assertTrue(any("tools/verify_release.py" in c for c in calls))

    def test_the_release_commit_itself_must_pass_the_gate(self):
        candidate = self.ready_to_publish()
        code, calls, err = self.publish(gate="NO-GO")
        self.assertEqual(code, 1)
        self.assertIn("did not pass the gate", err)
        self.assertEqual(git(self.repo.origin, "rev-parse", "main"), candidate)
        self.assertEqual(git(self.repo.origin, "tag", "--list"), "v1.0.0")
        self.assertFalse(any(c[0] == "gh" for c in calls))

    def assert_nothing_published(self, candidate, calls):
        self.assertEqual(git(self.repo.origin, "rev-parse", "main"), candidate)
        self.assertFalse(any(c[0] == "gh" for c in calls))

    def side_commit(self):
        """A fictional commit outside main's history, for a tag that points somewhere else."""
        return git(self.repo.root, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "Fictional side commit")

    def test_a_tag_that_points_elsewhere_stops_the_publish(self):
        candidate = self.ready_to_publish()
        git(self.repo.root, "tag", "v1.1.0", self.side_commit())
        code, calls, err = self.publish()
        self.assertEqual(code, 1)
        self.assertIn("v1.1.0 already exists here", err)
        self.assert_nothing_published(candidate, calls)
        self.assertEqual(git(self.repo.origin, "tag", "--list"), "v1.0.0")

    def test_a_tag_on_github_that_points_elsewhere_stops_the_publish(self):
        candidate = self.ready_to_publish()
        side = self.side_commit()
        git(self.repo.root, "tag", "-a", "-m", "Fictional tag", "v1.1.0", side)
        git(self.repo.root, "push", "-q", "origin", "v1.1.0")
        git(self.repo.root, "tag", "-d", "v1.1.0")
        code, calls, err = self.publish()
        self.assertEqual(code, 1)
        self.assertIn("v1.1.0 already exists on origin", err)
        self.assert_nothing_published(candidate, calls)
        self.assertEqual(git(self.repo.origin, "rev-parse", "v1.1.0^{commit}"), side)

    def test_a_tag_already_on_the_release_commit_is_used(self):
        self.ready_to_publish()
        release.write_release(release.make_plan(day=DAY), "Fictional Reviewer", DAY)
        git(self.repo.root, "tag", "v1.1.0")
        code, calls, err = self.publish()
        self.assertEqual(code, 0, err)
        self.assertEqual(git(self.repo.origin, "rev-parse", "v1.1.0^{commit}"), git(self.repo.root, "rev-parse", "HEAD"))

    def test_publish_checks_the_controls_on_the_release_commit(self):
        self.ready_to_publish("rules/04-fictional-control.md", "# Control 4\n\nThe agent may send without asking.\n")
        plan = release.make_plan(controls_owner="Fictional Owner", day=DAY)
        plan.breaks, plan.approved_by = [], ""  # as if the plan had been made without the control check
        with patch.object(release, "make_plan", return_value=plan):
            code, calls, err = self.publish()
        self.assertEqual(code, 1)
        self.assertIn("needs the owner", err)
        self.assertEqual(git(self.repo.origin, "tag", "--list"), "v1.0.0")
        self.assertFalse(any(c[0] == "gh" for c in calls))

    def test_a_resumed_release_still_needs_the_owner_for_control_changes(self):
        self.ready_to_publish("rules/04-fictional-control.md", "# Control 4\n\nThe agent may send without asking.\n")
        release.write_release(release.make_plan(controls_owner="Fictional Owner", day=DAY), "Fictional Reviewer", DAY)
        with self.assertRaisesRegex(release.Refused, "needs the owner"):
            release.make_plan(day=DAY)
        resumed = release.make_plan(controls_owner="Fictional Owner", day=DAY)
        self.assertEqual((resumed.resumed, resumed.version, resumed.approved_by), (True, "1.1.0", "Fictional Owner"))
        with self.assertRaisesRegex(release.Refused, "makes a minor release"):
            release.make_plan(major_owner="Fictional Owner", day=DAY)

    def test_a_resumed_release_must_carry_the_approval_given_again(self):
        self.ready_to_publish("rules/04-fictional-control.md", "# Control 4\n\nThe agent may send without asking.\n")
        release.write_release(release.make_plan(controls_owner="Fictional Owner", day=DAY), "Fictional Reviewer", DAY)
        with self.assertRaisesRegex(release.Refused, "records approval by Fictional Owner, but this run was approved by "
                                                     "Another Fictional Owner"):
            release.make_plan(controls_owner="Another Fictional Owner", day=DAY)
        # The release commit keeps its subject but has lost the approval message.
        git(self.repo.root, "-c", "commit.gpgsign=false", "commit", "-q", "--amend", "-m", "Release SHOTos v1.1.0")
        with self.assertRaisesRegex(release.Refused, "does not record the owner's approval"):
            release.make_plan(controls_owner="Fictional Owner", day=DAY)
        # Even a plan that skipped that check cannot publish the commit.
        stale =release.Plan("v1.0.0", git(self.repo.root, "rev-parse", "HEAD^"), "resume", "1.1.0", resumed=True,
                             breaks=release.control_breaks("v1.0.0", "HEAD"), approved_by="Fictional Owner")
        with patch.object(release, "make_plan", return_value=stale):
            code, calls, err = self.publish("--controls-approved-by", "Fictional Owner")
        self.assertEqual(code, 1)
        self.assertIn("does not record the owner's approval", err)
        self.assertEqual(git(self.repo.origin, "tag", "--list"), "v1.0.0")
        self.assertFalse(any(c[0] == "gh" for c in calls))

    def test_a_release_commit_may_change_only_version_numbers_in_its_manifests(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        self.repo.commit("Change the guide")
        release.write_release(release.make_plan(day=DAY), "Fictional Reviewer", DAY)
        self.repo.write(".claude-plugin/plugin.json", '{\n  "name": "shotos-core",\n  "version": "1.0.1",\n'
                                                      '  "description": "Changed in the release commit."\n}\n')
        git(self.repo.root, "add", "-A")
        git(self.repo.root, "-c", "commit.gpgsign=false", "commit", "-q", "--amend", "--no-edit")
        with self.assertRaisesRegex(release.Refused, r"more than the version files(.|\n)*\.claude-plugin/plugin.json"):
            release.make_plan(day=DAY)

    def test_an_interrupted_publish_carries_on_from_the_release_commit(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        candidate = self.repo.commit("Change the guide")
        self.repo.card()
        plan = release.make_plan(day=DAY)
        release.write_release(plan, "Fictional Reviewer", DAY)
        resumed = release.make_plan(day=DAY)
        self.assertTrue(resumed.resumed)
        self.assertEqual((resumed.version, resumed.candidate), ("1.0.1", candidate))
        self.assertTrue(resumed.section.startswith("## 1.0.1 (16 November 2026)"))
        self.assertIsNone(release.card_problem(resumed.candidate))
        git(self.repo.root, "tag", "v1.0.1")  # tagged locally, then the push failed
        self.assertEqual(release.make_plan(day=DAY).previous, "v1.0.0")

    def test_a_private_term_in_a_file_name_is_withheld_from_the_release_error(self):
        self.repo.write("docs/Zentrix Ltd.md", "Fictional.\n")
        self.repo.commit("Add a fictional note")
        plan = release.Plan("v1.0.0", git(self.repo.root, "rev-parse", "HEAD^"), "patch", "1.0.1")
        env = {**os.environ, "SHOTOS_DENYLIST": str(ROOT / "tests" / "fixtures" / "leak-denylist.txt")}
        with patch.object(release, "run", return_value=""), patch.dict(os.environ, env), \
                self.assertRaises(release.Refused) as raised:
            release.check_release_commit(plan)
        self.assertIn("docs/[withheld: denylist line 6] (file name)", str(raised.exception))
        self.assertNotIn("Zentrix", str(raised.exception))

    def test_a_private_term_in_a_path_is_withheld_from_what_the_script_prints(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        self.repo.commit("Change the guide")
        release.write_release(release.make_plan(day=DAY), "Fictional Reviewer", DAY)
        self.repo.write("docs/Zentrix Ltd.md", "Fictional.\n")
        git(self.repo.root, "add", "-A")
        git(self.repo.root, "-c", "commit.gpgsign=false", "commit", "-q", "--amend", "--no-edit")
        env = {**os.environ, "SHOTOS_DENYLIST": str(ROOT / "tests" / "fixtures" / "leak-denylist.txt")}
        with patch.dict(os.environ, env), patch("sys.stderr", new_callable=io.StringIO) as err, \
                patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(release.main([]), 1)
        self.assertIn("[withheld: matches denylist line 6]", err.getvalue())
        self.assertNotIn("Zentrix", err.getvalue())

    def test_a_release_commit_holding_other_changes_is_refused(self):
        self.repo.write("docs/guide.md", "Changed.\n")
        self.repo.commit("Change the guide")
        release.write_release(release.make_plan(day=DAY), "Fictional Reviewer", DAY)
        self.repo.write("docs/guide.md", "Changed again.\n")
        git(self.repo.root, "add", "-A")
        git(self.repo.root, "-c", "commit.gpgsign=false", "commit", "-q", "--amend", "--no-edit")
        with self.assertRaisesRegex(release.Refused, "more than the version files"):
            release.make_plan(day=DAY)


if __name__ == "__main__":
    unittest.main()
