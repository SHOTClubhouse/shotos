import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "stop_claim_check.py"
LAUNCHER = HOOK.parent / "run_hook.sh"


def transcript(tmp: Path, text: str, tools=("Write",), earlier=(), history=()) -> Path:
    path = tmp / "t.jsonl"
    lines = [*history, {"type": "user", "message": {"role": "user", "content": "Write the plan."}}]
    for name in tools:
        lines.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": {}}]}})
        lines.append({"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}})
    for part in earlier:
        lines.append({"type": "assistant", "message": {"content": [{"type": "text", "text": part}]}})
    lines.append({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})
    path.write_text("\n".join(json.dumps(line, ensure_ascii=False) for line in lines), encoding="utf-8")
    return path


class StopHookTests(unittest.TestCase):
    def run_hook(self, text, active=False, command=None, tools=("Write",), opted_in=True, earlier=(), history=()):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as home:
            tmp = Path(tmp)
            if opted_in:
                (tmp / ".shotos").mkdir()
            event = {"transcript_path": str(transcript(tmp, text, tools, earlier, history)), "cwd": str(tmp), "stop_hook_active": active}
            env = {**os.environ, "HOME": home, "USERPROFILE": home}  # no user config on the machine running the test
            return subprocess.run(command or [sys.executable, str(HOOK)], input=json.dumps(event),
                                  capture_output=True, text=True, env=env)

    def test_never_blocks_a_project_that_has_not_set_up_claim_check(self):
        run = self.run_hook("Done.\n\n## Claims\n- [file] created: plan.md\n", opted_in=False)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_fenced_example_does_not_satisfy_the_stop_hook(self):
        run = self.run_hook("Done.\n\n~~~markdown\n## Claims\n- [unverified] example\n~~~")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("no Claims block", run.stderr)

    def test_hook_leaves_no_bytecode_behind(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as home:
            hooks = Path(tmp) / ".shotos" / "hooks"
            tools = Path(tmp) / ".shotos" / "tools"
            hooks.mkdir(parents=True)
            tools.mkdir(parents=True)
            shutil.copy(HOOK, hooks / "stop_claim_check.py")
            shutil.copy(HOOK.parents[1] / "tools" / "claim_check.py", tools / "claim_check.py")
            event = {"transcript_path": str(transcript(Path(tmp), "Done, written.")), "cwd": tmp, "stop_hook_active": False}
            env = {**os.environ, "HOME": home, "USERPROFILE": home}
            subprocess.run([sys.executable, str(hooks / "stop_claim_check.py")], input=json.dumps(event),
                           capture_output=True, text=True, env=env)
            self.assertEqual(list(Path(tmp).rglob("__pycache__")), [])

    @unittest.skipUnless(shutil.which("sh"), "needs a POSIX shell")
    def test_launcher_finds_python_and_blocks_a_false_claim(self):
        run = self.run_hook("Done.\n\n## Claims\n- [file] created: plan.md\n",
                            command=[shutil.which("sh"), LAUNCHER.as_posix()])
        self.assertEqual(run.returncode, 2, run.stderr)

    def test_conversation_without_changes_is_never_blocked(self):
        run = self.run_hook("Done. That is my answer to your question.", tools=())
        self.assertEqual(run.returncode, 0)

    def test_changes_reported_as_done_without_claims_are_blocked(self):
        run = self.run_hook("Done, the plan is written.", tools=("Write",))
        self.assertEqual(run.returncode, 2)

    def test_earlier_completion_claim_is_checked(self):
        run = self.run_hook("Let me know if you need anything.", earlier=("Done, I emailed the client.",))
        self.assertEqual(run.returncode, 2)

    def test_old_turns_do_not_supply_current_claims(self):
        old = {"type": "assistant", "message": {"content": [{"type": "text", "text": "Done, I sent it."}]}}
        run = self.run_hook("Nothing was sent.", history=(old,))
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_long_record_keeps_current_claim_lines_in_order(self):
        body = "é" * 70000 + "\n\n## Claims"
        run = self.run_hook("- [file] created: absent.md", earlier=(body,))
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("UNSUPPORTED", run.stderr)

    def test_unverified_only_cannot_back_a_done_claim(self):
        run = self.run_hook("Done.\n\n## Claims\n- [unverified] everything\n")
        self.assertEqual(run.returncode, 2)

    def test_bad_input_never_blocks(self):
        run = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
        self.assertEqual(run.returncode, 0)

    def test_false_claim_blocks_the_stop(self):
        run = self.run_hook("Done.\n\n## Claims\n- [file] created: plan.md\n")
        self.assertEqual(run.returncode, 2)
        self.assertIn("UNSUPPORTED", run.stderr)

    def test_honest_report_lets_the_agent_stop(self):
        run = self.run_hook("I drafted nothing yet.\n\n## Claims\n- [unverified] no file written\n")
        self.assertEqual(run.returncode, 0)

    def test_an_unsent_status_does_not_trigger_a_retry(self):
        run = self.run_hook("Nothing was sent or published.\n\n## Claims\n- [unverified] external delivery\n")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_never_blocks_twice_in_one_turn(self):
        run = self.run_hook("Done.\n\n## Claims\n- [file] created: plan.md\n", active=True)
        self.assertEqual(run.returncode, 0)


if __name__ == "__main__":
    unittest.main()
