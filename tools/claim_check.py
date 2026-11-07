#!/usr/bin/env python3
"""claim-check: test an agent's "done" claims against the evidence.

An agent ends its report with a Claims block:

    ## Claims
    - [file] created: docs/plan.md
    - [file] changed: src/app.py
    - [command] passes: python -m unittest
    - [git] committed: HEAD
    - [git] pushed: main
    - [external] sent: weekly update to finance | receipt: .work/receipts/send.json
    - [unverified] I could not check the live site

Each claim is checked against files, git, an allowed command or a receipt, and
gets one state:

    SUPPORTED    the evidence backs the claim
    UNSUPPORTED  the evidence contradicts the claim
    NO EVIDENCE  the claim cannot be checked here (no receipt, command not allowed)
    DECLARED     the agent said itself that it did not check this

The report passes only when every claim is SUPPORTED or DECLARED. A report that
uses completion language ("done", "sent", "tests pass") without a Claims block
fails. claim-check never marks work as accepted: acceptance is a person's decision.

Standard library only. Commands are run only when listed in --allow-command or
in .shotos/claim-check.json, never because a report asks for them.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

PASS_STATES = {"SUPPORTED", "DECLARED"}
EXTERNAL_KINDS = {"external"}
STATUS_RECEIPTS = {
    "authorised": "attach the named owner's approval for the exact action",
    "offered": "attach the dispatch receipt for the authorised offer",
    "accepted": "attach the named receiver's acceptance record",
    "completed": "attach the completion record and its evidence",
    "independent": "attach the cycle evidence and receiving lead's sign-off",
}
COMPLETION = re.compile(
    r"\b(done|completed?|finished|fixed|sent|emailed|deployed|published|pushed|merged|"
    r"tests? pass(?:es|ed)?|all green|works now)\b",
    re.IGNORECASE,
)
HEADING = re.compile(r"^\s*(#{1,6}\s*claims\b|\*\*claims\*\*|claims:)\s*$", re.IGNORECASE)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s*\[(\w+)\]\s*(.*)$")
COMMENT = re.compile(r"\s+\([^()]*\)\s*$")


@dataclass
class Claim:
    kind: str
    verb: str
    target: str
    receipt: str = ""
    line: str = ""


@dataclass
class ClaimResult:
    claim: Claim
    state: str
    evidence: str


@dataclass
class Result:
    claims: list = field(default_factory=list)
    problems: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems and all(r.state in PASS_STATES for r in self.claims)


def report_lines(report: str):
    fence = ""
    for line in report.splitlines():
        match = FENCE.match(line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = ""
        elif match:
            fence = match[1]
        else:
            yield line


def has_completion_language(report: str) -> bool:
    return any(COMPLETION.search(line) for line in report_lines(report))


def parse_claims(report: str) -> list:
    claims, inside = [], False
    for line in report_lines(report):
        if HEADING.match(line):
            inside = True
            continue
        if inside and line.lstrip().startswith("#"):
            inside = False
            continue
        if not inside:
            continue
        match = ITEM.match(line)
        if not match:
            continue
        kind, rest = match.group(1).lower(), match.group(2).strip()
        receipt = ""
        if "| receipt:" in rest:
            rest, receipt = (part.strip() for part in rest.split("| receipt:", 1))
        verb, target = "", rest
        if kind not in STATUS_RECEIPTS and kind != "unverified" and ":" in rest:
            verb, target = (part.strip() for part in rest.split(":", 1))
        claims.append(Claim(kind, verb.lower(), target, receipt, line.strip()))
    return claims


def has_claims_block(report: str) -> bool:
    return any(HEADING.match(line) for line in report_lines(report))


def _unquote(text: str) -> str:
    return text.strip().strip("`'\"").strip()


def _paths(target: str) -> list:
    """Split a file target into paths, dropping backticks and a trailing (comment)."""
    target = COMMENT.sub("", target.strip())
    return [p for p in (_unquote(COMMENT.sub("", part)) for part in target.split(",")) if p]


SAFE_REF = re.compile(r"[\w./~^@{}+-]+")
FILE_CHANGE_VERBS = {"created", "written", "saved", "added", "changed", "updated", "edited", "modified"}


def valid_ref(cwd: Path, ref: str) -> bool:
    """A git ref that cannot be read as an option and names a real commit."""
    if not ref or ref.startswith("-") or not SAFE_REF.fullmatch(ref):
        return False
    return _git(cwd, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}")[0] == 0


def _git(cwd: Path, *args: str):
    run = subprocess.run(["git", "--literal-pathspecs", *args], cwd=cwd, capture_output=True, text=True)
    return run.returncode, run.stdout.strip(), run.stderr.strip()


def _inside(cwd: Path, target: str):
    path = (cwd / target).resolve()
    try:
        path.relative_to(cwd.resolve())
    except ValueError:
        return None
    return path


def _is_git(cwd: Path) -> bool:
    return _git(cwd, "rev-parse", "--is-inside-work-tree")[0] == 0


def check_file(claim: Claim, cwd: Path, base: str | None) -> ClaimResult:
    paths = _paths(claim.target)
    if not paths:
        return ClaimResult(claim, "NO EVIDENCE", "no path given")
    results = [_check_one_file(claim, p, cwd, base) for p in paths]
    for state in ("UNSUPPORTED", "NO EVIDENCE"):
        bad = [r for r, p in zip(results, paths) if r.state == state]
        if bad:
            detail = "; ".join(f"{p}: {r.evidence}" for r, p in zip(results, paths) if r.state == state)
            return ClaimResult(claim, state, detail if len(paths) > 1 else bad[0].evidence)
    return ClaimResult(claim, "SUPPORTED", results[0].evidence if len(paths) == 1 else f"all {len(paths)} files: {results[0].evidence}")


def _check_one_file(claim: Claim, target: str, cwd: Path, base: str | None) -> ClaimResult:
    path = _inside(cwd, target)
    if path is None:
        return ClaimResult(claim, "UNSUPPORTED", "path is outside the workspace")
    verb = claim.verb
    if verb in {"created", "exists", "written", "saved", "added"}:
        if not path.exists():
            return ClaimResult(claim, "UNSUPPORTED", "file not found")
        if base and verb in {"created", "added"}:
            rel = path.relative_to(cwd.resolve()).as_posix()
            if _git(cwd, "cat-file", "-e", f"{base}:./{rel}")[0] == 0:
                return ClaimResult(claim, "UNSUPPORTED", f"file already existed at {base}")
            return ClaimResult(claim, "SUPPORTED", f"file exists and was absent at {base}")
        return ClaimResult(claim, "SUPPORTED", "file exists")
    if verb in {"deleted", "removed"}:
        if path.exists():
            return ClaimResult(claim, "UNSUPPORTED", "file still exists")
        if base:
            rel = path.relative_to(cwd.resolve()).as_posix()
            if _git(cwd, "cat-file", "-e", f"{base}:./{rel}")[0] != 0:
                return ClaimResult(claim, "NO EVIDENCE", f"file was not recorded at {base}")
            return ClaimResult(claim, "SUPPORTED", f"file was present at {base} and is now gone")
        return ClaimResult(claim, "SUPPORTED", "file is gone")
    if verb in {"changed", "updated", "edited", "modified"}:
        if not path.exists():
            return ClaimResult(claim, "UNSUPPORTED", "file not found")
        if not _is_git(cwd):
            return ClaimResult(claim, "NO EVIDENCE", "not a git repository, so a change cannot be shown")
        rel = str(path.relative_to(cwd.resolve())).replace("\\", "/")
        code, status, _ = _git(cwd, "status", "--porcelain", "--", rel)
        if code:
            return ClaimResult(claim, "NO EVIDENCE", "git status failed")
        if status:
            return ClaimResult(claim, "SUPPORTED", "uncommitted change in the working tree")
        if base:
            code, diff, _ = _git(cwd, "diff", "--name-only", base, "--", rel)
            if code:
                return ClaimResult(claim, "NO EVIDENCE", f"git diff against {base} failed")
            if diff:
                return ClaimResult(claim, "SUPPORTED", f"changed since {base}")
            return ClaimResult(claim, "UNSUPPORTED", f"no change since {base}")
        return ClaimResult(claim, "NO EVIDENCE",
                           "no uncommitted change; if it was committed, rerun with --base <ref>")
    return ClaimResult(claim, "NO EVIDENCE", f"unknown file claim '{verb}'")


def check_git(claim: Claim, cwd: Path, base: str | None, claimed_files=()) -> ClaimResult:
    if not _is_git(cwd):
        return ClaimResult(claim, "UNSUPPORTED", "not a git repository")
    verb = claim.verb
    target = (_unquote(COMMENT.sub("", claim.target)).split() or ["HEAD"])[0].strip("`")
    if verb == "committed":
        code, sha, _ = _git(cwd, "rev-parse", "--verify", "--end-of-options", f"{target}^{{commit}}")
        if code:
            return ClaimResult(claim, "UNSUPPORTED", f"no commit '{target}'")
        code, dirty, _ = _git(cwd, "status", "--porcelain", "--untracked-files=no")
        if code:
            return ClaimResult(claim, "NO EVIDENCE", "git status failed")
        if dirty:
            return ClaimResult(claim, "UNSUPPORTED", "tracked files still have uncommitted changes")
        uncommitted = [f for f in claimed_files if _git(cwd, "status", "--porcelain", "--", f)[1]]
        if uncommitted:
            return ClaimResult(claim, "UNSUPPORTED", "claimed files not committed: " + ", ".join(uncommitted))
        if not base:
            return ClaimResult(claim, "NO EVIDENCE", "no starting commit; rerun with --base <ref>")
        if _git(cwd, "rev-parse", base)[1] == sha:
            return ClaimResult(claim, "UNSUPPORTED", f"no new commit since {base}")
        if _git(cwd, "merge-base", "--is-ancestor", base, sha)[0]:
            return ClaimResult(claim, "UNSUPPORTED", f"{target} is not a descendant of {base}")
        return ClaimResult(claim, "SUPPORTED", f"commit {sha[:10]}, working tree clean")
    if verb == "pushed":
        if target == "HEAD":
            target = _git(cwd, "rev-parse", "--abbrev-ref", "HEAD")[1]
        code, upstream, _ = _git(cwd, "rev-parse", "--abbrev-ref", f"{target}@{{upstream}}")
        if code:
            return ClaimResult(claim, "UNSUPPORTED", f"'{target}' has no upstream branch")
        local, remote = _git(cwd, "rev-parse", target)[1], _git(cwd, "rev-parse", upstream)[1]
        if local == remote:
            return ClaimResult(claim, "SUPPORTED", f"{target} matches {upstream} (as of the last fetch)")
        return ClaimResult(claim, "UNSUPPORTED", f"{target} differs from {upstream}")
    if verb == "clean":
        code, dirty, _ = _git(cwd, "status", "--porcelain")
        if code:
            return ClaimResult(claim, "NO EVIDENCE", "git status failed")
        return ClaimResult(claim, "UNSUPPORTED" if dirty else "SUPPORTED",
                           "working tree has changes" if dirty else "working tree clean")
    return ClaimResult(claim, "NO EVIDENCE", f"unknown git claim '{verb}'")


def check_command(claim: Claim, cwd: Path, allow_commands) -> ClaimResult:
    command = claim.target.strip().strip("`").strip()
    if command not in {c.strip().strip("`").strip() for c in allow_commands}:
        return ClaimResult(claim, "NO EVIDENCE", "command is not on the allow list, so it was not run")
    try:
        run = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True, timeout=COMMAND_TIMEOUT)
    except subprocess.TimeoutExpired:
        return ClaimResult(claim, "UNSUPPORTED", f"command timed out after {COMMAND_TIMEOUT} seconds")
    want_pass = claim.verb in {"passes", "passed", "succeeds", "runs"}
    passed = run.returncode == 0
    if passed == want_pass:
        return ClaimResult(claim, "SUPPORTED", f"exit code {run.returncode}")
    return ClaimResult(claim, "UNSUPPORTED", f"exit code {run.returncode}")


def check_receipt(claim: Claim, cwd: Path, missing: str) -> ClaimResult:
    if not claim.receipt:
        return ClaimResult(claim, "NO EVIDENCE", missing)
    path = _inside(cwd, claim.receipt)
    if path is None or not path.is_file() or path.stat().st_size == 0:
        return ClaimResult(claim, "NO EVIDENCE", f"receipt '{claim.receipt}' not found or empty")
    return ClaimResult(claim, "SUPPORTED", f"receipt {claim.receipt}")


def check_claim(claim: Claim, cwd: Path, allow_commands, base, claimed_files=()) -> ClaimResult:
    if claim.kind == "file":
        return check_file(claim, cwd, base)
    if claim.kind == "git":
        return check_git(claim, cwd, base, claimed_files)
    if claim.kind == "command":
        return check_command(claim, cwd, allow_commands)
    if claim.kind in EXTERNAL_KINDS:
        return check_receipt(claim, cwd, "external action with no receipt")
    if claim.kind in STATUS_RECEIPTS:
        return check_receipt(claim, cwd, STATUS_RECEIPTS[claim.kind])
    if claim.kind == "unverified":
        return ClaimResult(claim, "DECLARED", "the agent said this was not checked")
    return ClaimResult(claim, "NO EVIDENCE", f"unknown claim kind '{claim.kind}'")


def check_report(report: str, cwd=".", allow_commands=None, base=None) -> Result:
    cwd = Path(cwd)
    result = Result()
    claims = parse_claims(report)
    if not claims:
        if has_claims_block(report):
            result.problems.append("Claims block is empty")
        elif has_completion_language(report):
            result.problems.append("completion language used but no Claims block: say what was done and how to check it")
        return result
    if base and not valid_ref(cwd, base):
        result.problems.append(f"--base '{base}' is not a commit in this repository, so it was ignored")
        base = None
    claimed_files = []
    for c in claims:
        if c.kind == "file" and c.verb in FILE_CHANGE_VERBS:
            for rel in _paths(c.target):
                path = _inside(cwd, rel)
                if path is not None and path.exists():
                    claimed_files.append(str(path.relative_to(cwd.resolve())).replace("\\", "/"))
    result.claims = [check_claim(c, cwd, allow_commands or [], base, claimed_files) for c in claims]
    return result


USER_CONFIG = Path.home() / ".shotos" / "claim-check.json"
COMMAND_TIMEOUT = 100  # seconds; below the 120 second Stop hook limit so a slow command reports instead of being killed


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def load_config(cwd: Path, path: str | None, trust_project: bool = False) -> dict:
    """Merge the user's own config with the project's.

    Commands are a trust decision. They come from the user's config
    (~/.shotos/claim-check.json), from a config file named on the command line,
    or from the project's .shotos/claim-check.json only when trust_project is
    set. A repository you cloned cannot make claim-check run its commands.
    """
    user = _read(USER_CONFIG)
    project = _read(Path(path)) if path else _read(Path(cwd) / ".shotos" / "claim-check.json")
    trusted = bool(path) or trust_project
    return {
        "allow_commands": list(user.get("allow_commands", [])) + (project.get("allow_commands", []) if trusted else []),
        "base": project.get("base") or user.get("base"),
    }


def render(result: Result) -> str:
    lines = [f"{r.state:<12} {r.claim.line[2:] if r.claim.line.startswith('- ') else r.claim.line}  ({r.evidence})"
             for r in result.claims]
    lines += [f"PROBLEM      {p}" for p in result.problems]
    lines.append("")
    lines.append("PASS" if result.ok else "FAIL")
    lines.append("claim-check checks that work was executed. Acceptance is a person's decision.")
    return "\n".join(lines)


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Check an agent's claims against the evidence.")
    parser.add_argument("report", nargs="?", default="-", help="report file, or - for stdin")
    parser.add_argument("--cwd", default=".", help="workspace the claims refer to")
    parser.add_argument("--base", help="git ref the work started from, to check committed changes")
    parser.add_argument("--allow-command", action="append", default=[], help="command that may be run to check a claim")
    parser.add_argument("--config", help="config file you trust, including its commands")
    parser.add_argument("--trust-project-config", action="store_true",
                        help="also run commands listed in this project's .shotos/claim-check.json")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args(argv)
    cwd = Path(args.cwd)
    try:
        config = load_config(cwd, args.config, args.trust_project_config)
        report = sys.stdin.read() if args.report == "-" else Path(args.report).read_text(encoding="utf-8")
        result = check_report(report, cwd, args.allow_command + config.get("allow_commands", []),
                              args.base or config.get("base"))
    except (OSError, ValueError) as error:  # unreadable report or config: say so, and do not look like a FAIL
        print(f"claim-check could not run: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"ok": result.ok, "problems": result.problems, "claims": [
            {"claim": r.claim.line, "state": r.state, "evidence": r.evidence} for r in result.claims]}, indent=2))
    else:
        print(render(result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
