#!/usr/bin/env python3
"""Claude Code Stop hook: run claim-check on the agent's text in this turn.

A Claims block outside a code fence in the assistant's turn is checked. Completion language
("done", "sent", "tests pass") without a Claims block is only challenged when
the agent used a tool that changes things in this turn, so ordinary
conversation is never blocked. If the check fails, the hook blocks the stop and
tells the agent why (exit code 2). A second stop in the same turn is never
blocked, so the hook cannot loop.

Commands are run only if the user's own config (~/.shotos/claim-check.json)
allows them. A repository's own config cannot make this hook run commands.

The hook only acts where claim-check is set up: a project with a .shotos folder, or a user who has
~/.shotos/claim-check.json. Installing the plugin alone never blocks anyone.
"""

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # never leave bytecode behind in a project the installer must restore exactly

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import claim_check  # noqa: E402

CHANGING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Bash", "PowerShell"}


def _is_human_turn(entry: dict) -> bool:
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "text" for c in content)


def last_turn(transcript: Path):
    """Return assistant text and tools used since the last human message."""
    texts, tools = [], set()
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") == "user" and _is_human_turn(entry):
            texts, tools = [], set()
            continue
        if entry.get("type") != "assistant":
            continue
        content = (entry.get("message") or {}).get("content") or []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "tool_use":
                tools.add(item.get("name", ""))
        parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
        texts.extend(p for p in parts if p.strip())
    return "\n\n".join(texts), tools


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if event.get("stop_hook_active"):
        return 0
    cwd = Path(event.get("cwd") or ".")
    if not (cwd / ".shotos").is_dir() and not claim_check.USER_CONFIG.is_file():
        return 0  # not opted in: neither this project nor the user has set up claim-check
    transcript = Path(event.get("transcript_path", ""))
    if not transcript.is_file():
        return 0
    report, tools = last_turn(transcript)
    if not claim_check.has_claims_block(report) and not (tools & CHANGING_TOOLS):
        return 0
    if tools & CHANGING_TOOLS and claim_check.has_completion_language(report):
        claims = claim_check.parse_claims(report)
        if claims and all(c.kind == "unverified" for c in claims):
            print("claim-check needs a checkable claim for reported completed work, not only [unverified].", file=sys.stderr)
            return 2
    config = claim_check.load_config(cwd, None)
    result = claim_check.check_report(report, cwd, config.get("allow_commands", []), config.get("base"))
    if result.ok:
        return 0
    print("claim-check found claims the evidence does not support:\n", file=sys.stderr)
    print(claim_check.render(result), file=sys.stderr)
    print("\nFix the work, or correct the Claims block. Mark anything you could not check as [unverified].",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
