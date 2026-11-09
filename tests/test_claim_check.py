import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import claim_check  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


class RepoCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        (self.repo / "plan.md").write_text("first\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "start")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, report, **kwargs):
        return claim_check.check_report(report, cwd=self.repo, **kwargs)

    def states(self, results):
        return [r.state for r in results.claims]


class ParsingTests(unittest.TestCase):
    def test_an_unreadable_report_exits_2_not_1(self):
        # 0 pass, 1 fail, 2 could not run: a crash must never look like a failed claim.
        run = subprocess.run([sys.executable, str(ROOT / "tools" / "claim_check.py"), "no-such-report.md"],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("could not run", run.stderr)

    def test_parses_claims_block(self):
        report = "Done.\n\n## Claims\n- [file] created: docs/a.md\n- [command] passes: python -m unittest\n- [unverified] staging deploy not checked\n"
        claims = claim_check.parse_claims(report)
        self.assertEqual([(c.kind, c.verb, c.target) for c in claims], [
            ("file", "created", "docs/a.md"),
            ("command", "passes", "python -m unittest"),
            ("unverified", "", "staging deploy not checked"),
        ])

    def test_parses_each_claims_block_in_a_turn(self):
        report = "## Claims\n- [file] created: first.md\n\n## Update\nLater.\n\n## Claims\n- [file] created: second.md\n"
        self.assertEqual([c.target for c in claim_check.parse_claims(report)], ["first.md", "second.md"])

    def test_a_fenced_example_cannot_support_a_completion_claim(self):
        report = "Done.\n\n~~~markdown\n## Claims\n- [unverified] example\n~~~"
        result = claim_check.check_report(report)
        self.assertFalse(result.ok)
        self.assertIn("no Claims block", result.problems[0])

    def test_a_code_sample_alone_does_not_claim_completion(self):
        fence = chr(96) * 3
        report = f"{fence}markdown\nDone.\n## Claims\n- [file] created: example.md\n{fence}"
        self.assertTrue(claim_check.check_report(report).ok)
        self.assertFalse(claim_check.has_claims_block(report))

    def test_unexecuted_status_does_not_imply_completion(self):
        for report in ("Nothing was sent or published.", "No messages were sent.", "I haven’t sent it.",
                       "The draft is not yet finished.", "The release was never deployed."):
            with self.subTest(report=report):
                self.assertTrue(claim_check.check_report(report).ok)
                self.assertFalse(claim_check.check_report(report + " I published the preview.").ok)

    def test_not_been_sent_is_negated_completion(self):
        for report in ("The email has not been sent yet.", "The email has not yet been sent.",
                       "The email has never been sent."):
            with self.subTest(report=report):
                self.assertTrue(claim_check.check_report(report).ok)
        self.assertFalse(claim_check.check_report("The email has been sent.").ok)

    def test_parse_real_claims_after_a_fenced_example(self):
        report = "~~~~\n~~~\n## Claims\n- [file] created: example.md\n~~~~\n## Claims\n- [file] created: real.md"
        self.assertEqual([c.target for c in claim_check.parse_claims(report)], ["real.md"])

    def test_receipt_is_split_from_target(self):
        claims = claim_check.parse_claims("## Claims\n- [external] sent: update to finance | receipt: out/send.json\n")
        self.assertEqual(claims[0].target, "update to finance")
        self.assertEqual(claims[0].receipt, "out/send.json")


class FileClaimTests(RepoCase):
    def test_created_file_that_exists_is_supported(self):
        (self.repo / "new.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: new.md\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])
        self.assertTrue(result.ok)

    def test_existing_baseline_file_cannot_be_claimed_as_created(self):
        result = self.check("## Claims\n- [file] created: plan.md\n", base="HEAD")
        self.assertEqual(result.claims[0].state, "UNSUPPORTED")
        self.assertIn("already existed", result.claims[0].evidence)

    def test_tracked_baseline_file_can_be_verified_as_deleted(self):
        (self.repo / "plan.md").unlink()
        result = self.check("## Claims\n- [file] deleted: plan.md\n", base="HEAD")
        self.assertEqual(result.claims[0].state, "SUPPORTED")

    def test_absence_from_both_trees_does_not_verify_deletion(self):
        result = self.check("## Claims\n- [file] deleted: missing.md\n", base="HEAD")
        self.assertEqual(result.claims[0].state, "NO EVIDENCE")

    def test_created_file_that_is_missing_is_unsupported(self):
        result = self.check("## Claims\n- [file] created: missing.md\n")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])
        self.assertFalse(result.ok)

    def test_changed_file_with_no_change_since_base_is_unsupported(self):
        result = self.check("## Claims\n- [file] changed: plan.md\n", base="HEAD")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])

    def test_changed_file_with_no_base_and_no_change_has_no_evidence(self):
        result = self.check("## Claims\n- [file] changed: plan.md\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])

    def test_committed_change_since_base_is_supported(self):
        (self.repo / "plan.md").write_text("second\n", encoding="utf-8")
        git(self.repo, "commit", "-qam", "edit")
        result = self.check("## Claims\n- [file] changed: plan.md\n", base="HEAD~1")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_changed_file_with_a_change_is_supported(self):
        (self.repo / "plan.md").write_text("second\n", encoding="utf-8")
        result = self.check("## Claims\n- [file] changed: plan.md\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_literal_brackets_do_not_match_a_different_changed_file(self):
        literal = self.repo / "plan[1].md"
        neighbour = self.repo / "plan1.md"
        literal.write_text("first\n", encoding="utf-8")
        neighbour.write_text("first\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "add notes")
        neighbour.write_text("second\n", encoding="utf-8")
        result = self.check("## Claims\n- [file] changed: plan[1].md\n", base="HEAD")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])

    def test_path_outside_the_workspace_is_refused(self):
        result = self.check("## Claims\n- [file] exists: ../../etc/passwd\n")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])


class GitClaimTests(RepoCase):
    def test_failed_git_status_does_not_verify_a_clean_tree(self):
        with patch.object(claim_check, "_git", side_effect=[(0, "true", ""), (128, "", "status unavailable")]):
            result = self.check("## Claims\n- [git] clean: working tree\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])

    def test_committed_with_uncommitted_changes_is_unsupported(self):
        (self.repo / "plan.md").write_text("dirty\n", encoding="utf-8")
        result = self.check("## Claims\n- [git] committed: HEAD\n")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])

    def test_committed_and_clean_without_base_has_no_evidence(self):
        result = self.check("## Claims\n- [git] committed: HEAD\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])

    def test_committed_change_since_base_is_supported(self):
        (self.repo / "plan.md").write_text("second\n", encoding="utf-8")
        git(self.repo, "commit", "-qam", "edit")
        result = self.check("## Claims\n- [git] committed: HEAD\n", base="HEAD~1")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_named_commit_must_contain_the_current_file_version(self):
        plan = self.repo / "plan.md"
        plan.write_text("intermediate\n", encoding="utf-8")
        git(self.repo, "commit", "-qam", "intermediate")
        plan.write_text("final\n", encoding="utf-8")
        git(self.repo, "commit", "-qam", "final")
        result = self.check("## Claims\n- [file] changed: plan.md\n- [git] committed: HEAD~1\n", base="HEAD~2")
        self.assertEqual(self.states(result), ["SUPPORTED", "UNSUPPORTED"])

    def test_ignored_draft_is_not_part_of_a_commit(self):
        (self.repo / ".gitignore").write_text(".work/\n", encoding="utf-8")
        git(self.repo, "add", ".gitignore")
        git(self.repo, "commit", "-qm", "ignore work")
        (self.repo / ".work").mkdir()
        (self.repo / ".work/draft.md").write_text("draft\n", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: .work/draft.md\n- [git] committed: HEAD\n", base="HEAD~1")
        self.assertEqual(self.states(result), ["SUPPORTED", "UNSUPPORTED"])

    def test_named_commit_must_contain_the_reported_deletion(self):
        git(self.repo, "commit", "--allow-empty", "-qm", "checkpoint")
        (self.repo / "plan.md").unlink()
        git(self.repo, "commit", "-qam", "remove")
        result = self.check("## Claims\n- [file] deleted: plan.md\n- [git] committed: HEAD~1\n", base="HEAD~2")
        self.assertEqual(self.states(result), ["SUPPORTED", "UNSUPPORTED"])
        result = self.check("## Claims\n- [file] deleted: plan.md\n- [git] committed: HEAD\n", base="HEAD~2")
        self.assertEqual(self.states(result), ["SUPPORTED", "SUPPORTED"])

    def test_pushed_without_upstream_is_unsupported(self):
        result = self.check("## Claims\n- [git] pushed: main\n")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])

    def test_pushed_uses_the_real_upstream_ref_when_a_local_branch_shadows_it(self):
        git(self.repo, "remote", "add", "origin", ".")
        git(self.repo, "update-ref", "refs/remotes/origin/main", "HEAD")
        git(self.repo, "branch", "--set-upstream-to=origin/main", "main")
        git(self.repo, "commit", "--allow-empty", "-q", "-m", "update")
        git(self.repo, "branch", "origin/main", "HEAD")
        claim = "## Claims\n- [git] pushed: main\n"
        self.assertEqual(self.states(self.check(claim)), ["UNSUPPORTED"])
        git(self.repo, "update-ref", "refs/remotes/origin/main", "HEAD")
        self.assertEqual(self.states(self.check(claim)), ["SUPPORTED"])

    def test_check_never_launches_the_repository_filesystem_monitor(self):
        monitor = self.repo / "monitor.sh"
        monitor.write_bytes(b"#!/bin/sh\nprintf invoked > monitor-marker\n")
        monitor.chmod(0o755)
        git(self.repo, "config", "core.fsmonitor", "./monitor.sh")
        git(self.repo, "status", "--porcelain")
        marker = self.repo / "monitor-marker"
        self.assertTrue(marker.is_file(), "test fixture did not run")
        marker.unlink()
        self.check("## Claims\n- [git] clean: working tree\n")
        self.assertFalse(marker.exists())

    def test_worktree_claims_never_launch_a_configured_git_clean_filter(self):
        (self.repo / ".gitattributes").write_bytes(b"plan.md filter=probe\n")
        git(self.repo, "add", ".gitattributes")
        git(self.repo, "commit", "-q", "-m", "attributes")
        git(self.repo, "config", "filter.probe.clean", "printf invoked > filter-marker; cat")
        plan = self.repo / "plan.md"
        original = plan.stat()
        os.utime(plan, (original.st_atime, original.st_mtime + 5))
        git(self.repo, "--no-optional-locks", "status", "--porcelain")
        marker = self.repo / "filter-marker"
        self.assertTrue(marker.is_file(), "test fixture did not run")
        marker.unlink()
        self.assertEqual(self.states(self.check("## Claims\n- [git] clean: working tree\n")), ["SUPPORTED"])
        self.assertFalse(marker.exists())


class CommandClaimTests(RepoCase):
    def test_command_is_not_run_unless_allowed(self):
        result = self.check("## Claims\n- [command] passes: python -c \"print(1)\"\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])
        self.assertFalse(result.ok)

    def test_allowed_passing_command_is_supported(self):
        cmd = f'"{sys.executable}" -c "print(1)"'
        result = self.check(f"## Claims\n- [command] passes: {cmd}\n", allow_commands=[cmd])
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_allowed_failing_command_is_unsupported(self):
        cmd = f'"{sys.executable}" -c "import sys; sys.exit(3)"'
        result = self.check(f"## Claims\n- [command] passes: {cmd}\n", allow_commands=[cmd])
        self.assertEqual(self.states(result), ["UNSUPPORTED"])


class ExternalAndHonestyTests(RepoCase):
    def test_external_claim_without_receipt_has_no_evidence(self):
        result = self.check("## Claims\n- [external] sent: weekly update to the board\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])

    def test_external_claim_with_receipt_is_supported(self):
        (self.repo / "receipt.json").write_text(json.dumps({"id": "abc"}), encoding="utf-8")
        result = self.check("## Claims\n- [external] sent: weekly update | receipt: receipt.json\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_declared_unverified_is_honest_and_passes(self):
        result = self.check("## Claims\n- [unverified] I could not check the live site\n")
        self.assertEqual(self.states(result), ["DECLARED"])
        self.assertTrue(result.ok)

    def test_completion_language_without_claims_block_fails(self):
        result = self.check("All done. Tests pass and the email has been sent.")
        self.assertFalse(result.ok)
        self.assertIn("no Claims block", result.problems[0])

    def test_plain_question_without_claims_passes(self):
        result = self.check("Which folder should the report go in?")
        self.assertTrue(result.ok)

    def test_accepted_is_never_claimed_by_the_tool(self):
        result = self.check("## Claims\n- [accepted] client signed it off\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])


    def test_handoff_claims_require_a_receipt(self):
        (self.repo / "receipt.json").write_text('{"id": "abc"}', encoding="utf-8")
        for kind in ("authorised", "offered", "accepted", "completed", "independent"):
            with self.subTest(kind=kind):
                claim = f"## Claims\n- [{kind}] transfer: case 42"
                self.assertEqual(self.states(self.check(claim + "\n")), ["NO EVIDENCE"])
                result = self.check(claim + " | receipt: receipt.json\n")
                self.assertEqual(self.states(result), ["SUPPORTED"])


class RealWorldFormattingTests(RepoCase):
    """Agents decorate their claims. Decoration must not turn a true claim false."""

    def test_backticked_path_is_understood(self):
        (self.repo / "notes.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: `notes.md`\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_trailing_comment_in_brackets_is_ignored(self):
        (self.repo / "notes.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: notes.md (three-line summary)\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_several_files_on_one_line_must_all_hold(self):
        (self.repo / "a.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: a.md, b.md\n")
        self.assertEqual(self.states(result), ["UNSUPPORTED"])
        (self.repo / "b.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: `a.md`, `b.md`\n")
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_git_ref_with_commentary_uses_the_ref(self):
        result = self.check("## Claims\n- [git] committed: HEAD (`abc123` on main)\n")
        self.assertEqual(self.states(result), ["NO EVIDENCE"])

    def test_backticked_command_is_matched_against_the_allow_list(self):
        cmd = f'"{sys.executable}" -c "print(1)"'
        result = self.check(f"## Claims\n- [command] passes: `{cmd}`\n", allow_commands=[cmd])
        self.assertEqual(self.states(result), ["SUPPORTED"])

    def test_bold_kind_and_numbered_list_are_understood(self):
        (self.repo / "n.md").write_text("x", encoding="utf-8")
        result = self.check("### Claims\n1. [file] created: n.md\n* [unverified] layout not checked\n")
        self.assertEqual(self.states(result), ["SUPPORTED", "DECLARED"])

    def test_render_survives_non_ascii(self):
        result = self.check("## Claims\n- [unverified] café menu not checked ✓\n")
        self.assertIn("caf", claim_check.render(result))


class ReviewFindingTests(RepoCase):
    """Holes found in the first release review."""

    def test_committed_fails_when_a_claimed_file_was_never_committed(self):
        (self.repo / "summary.md").write_text("x", encoding="utf-8")
        result = self.check("## Claims\n- [file] created: summary.md\n- [git] committed: HEAD\n", base="HEAD")
        self.assertEqual(self.states(result), ["SUPPORTED", "UNSUPPORTED"])

    def test_committed_passes_when_the_claimed_file_is_committed(self):
        (self.repo / "summary.md").write_text("x", encoding="utf-8")
        git(self.repo, "add", "summary.md")
        git(self.repo, "commit", "-q", "-m", "add")
        result = self.check("## Claims\n- [file] created: summary.md\n- [git] committed: HEAD\n", base="HEAD~1")
        self.assertEqual(self.states(result), ["SUPPORTED", "SUPPORTED"])

    def test_option_shaped_base_is_refused(self):
        outside = Path(self.tmp.name).parent / "claim-check-should-not-exist.txt"
        result = self.check("## Claims\n- [file] changed: plan.md\n", base=f"--output={outside}")
        self.assertFalse(outside.exists())
        self.assertFalse(result.ok)

    def test_project_config_cannot_allow_commands_unless_trusted(self):
        shotos = self.repo / ".shotos"
        shotos.mkdir()
        (shotos / "claim-check.json").write_text(json.dumps({"allow_commands": ["echo pwned"]}), encoding="utf-8")
        config = claim_check.load_config(self.repo, None)
        self.assertEqual(config.get("allow_commands", []), [])
        trusted = claim_check.load_config(self.repo, None, trust_project=True)
        self.assertEqual(trusted["allow_commands"], ["echo pwned"])

    def test_malformed_project_config_cannot_disable_checks_unless_trusted(self):
        shotos = self.repo / ".shotos"
        shotos.mkdir()
        settings = shotos / "claim-check.json"
        for broken in ("{", "[]", '{"base": 42}'):
            with self.subTest(config=broken):
                settings.write_text(broken, encoding="utf-8")
                with patch.object(claim_check, "USER_CONFIG", self.repo / "absent-user-config"):
                    self.assertEqual(claim_check.load_config(self.repo, None), {"base": None, "allow_commands": []})
                    with self.assertRaises(ValueError):
                        claim_check.load_config(self.repo, None, trust_project=True)

    def test_everyday_words_without_claims_do_not_fail(self):
        result = self.check("I shared my thinking above and posted the options for you to pick from.")
        self.assertTrue(result.ok)


class CliTests(RepoCase):
    def test_exit_code_reflects_result(self):
        report = self.repo / "report.md"
        report.write_text("## Claims\n- [file] created: nope.md\n", encoding="utf-8")
        run = subprocess.run([sys.executable, str(ROOT / "tools" / "claim_check.py"), str(report)],
                             cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertIn("UNSUPPORTED", run.stdout)


if __name__ == "__main__":
    unittest.main()
