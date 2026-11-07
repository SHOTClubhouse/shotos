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


def _is_human_turn(content) -> bool:
    if isinstance(content, str):
        return True
    return isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "text" for c in content)


def _reverse_lines(transcript: Path, block_size: int = 65536):
    """Read JSONL from the end, joining a record that spans multiple blocks."""
    with transcript.open("rb") as stream:
        offset = stream.seek(0, 2)
        suffix = []
        while offset:
            size = min(offset, block_size)
            offset -= size
            stream.seek(offset)
            lines = stream.read(size).split(b"\n")
            if len(lines) > 1:
                yield b"".join([lines[-1], *reversed(suffix)])
                yield from reversed(lines[1:-1])
                suffix.clear()
            suffix.append(lines[0])
        if suffix:
            yield b"".join(reversed(suffix))


def last_turn(transcript: Path):
    """Return assistant text and tools used since the last human message."""
    texts, tools = [], set()
    for line in _reverse_lines(transcript):
        try:
            entry = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(entry, dict) or not isinstance(entry.get("message"), dict):
            continue
        content = entry["message"].get("content")
        if entry.get("type") == "user" and _is_human_turn(content):
            break
        if entry.get("type") != "assistant" or not isinstance(content, list):
            continue
        for item in reversed(content):
            if not isinstance(item, dict):
                continue
            if item.get("type") == "tool_use" and isinstance(item.get("name"), str):
                tools.add(item["name"])
            if item.get("type") == "text" and isinstance(item.get("text"), str) and item["text"].strip():
                texts.append(item["text"])
    return "\n\n".join(reversed(texts)), tools


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
