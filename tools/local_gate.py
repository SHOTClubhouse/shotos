#!/usr/bin/env python3
"""Run every SHOTos check locally and write a plain-English go/no-go card.

Examples:
  python tools/local_gate.py                 full gate, compared with origin/main
  python tools/local_gate.py --fast          quick gate, as the pre-push hook runs it
  python tools/local_gate.py --release       full gate that must be fit for a release
  python tools/local_gate.py --base v1.15.0  compare with a tag or other ref

The card is saved as .work/gate/<short-sha>.md (fast runs add -fast). The exit
code is 0 only when the verdict is GO.

The full gate runs the unit tests, the demo, the JavaScript tests when Node.js
is installed, the leak scan, the skill ZIP link check and the skill structure
checks for every skill changed since the base. The fast gate leaves out the
unit tests and checks ZIP links only for changed skills.

The leak scan needs the private denylist named by SHOTOS_DENYLIST. Without it
the gate warns, and the card cannot be used for a release.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import leak_scan  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CARDS = REPO / ".work" / "gate"
ZERO = "0" * 40
CONTROL_FILES = ("docs/controls.md", "docs/claims.md", "rules/", "hooks/", "tools/claim_check.py",
                 "templates/AGENTS.md", "install.py")


@dataclass
class Check:
    name: str
    status: str  # "pass", "fail" or "skip"
    line: str
    details: list = field(default_factory=list)


@dataclass
class Context:
    head: str
    branch: str
    base: str
    base_label: str
    fast: bool
    release: bool
    denylist: Path = None
    dirty: list = field(default_factory=list)
    untracked: int = 0
    commits: list = field(default_factory=list)
    changes: list = field(default_factory=list)  # (status, path)
    history: list = field(default_factory=list)  # revision ranges for the leak scan
    notes: list = field(default_factory=list)


def git(*args, repo: Path = REPO, check=True) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=check, timeout=60).stdout.rstrip()


def short(sha: str) -> str:
    return sha[:12]


def card_path(head: str, fast: bool = False, cards: Path = CARDS) -> Path:
    return cards / f"{short(head)}{'-fast' if fast else ''}.md"


def resolve(ref: str, repo: Path = REPO):
    found = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", "--end-of-options",
                            f"{ref}^{{commit}}"], capture_output=True, text=True, timeout=30)
    return found.stdout.strip() if found.returncode == 0 else None


def choose_base(explicit=None, repo: Path = REPO) -> tuple:
    """(commit, label) to compare with: the named ref, the fork point from origin/main, or the last tag."""
    head = git("rev-parse", "HEAD", repo=repo)
    if explicit:
        commit = resolve(explicit, repo)
        if not commit:
            raise ValueError(f"base {explicit} is not a commit")
        return commit, explicit
    main = resolve("origin/main", repo)
    if main:
        fork = git("merge-base", "HEAD", main, repo=repo)
        if fork != head:
            return fork, "origin/main"
    tag = git("describe", "--tags", "--abbrev=0", "--match", "v*", repo=repo, check=False)
    if tag and resolve(tag, repo) != head:
        return resolve(tag, repo), tag
    parent = resolve("HEAD^", repo)
    return (parent, "the previous commit") if parent else (head, "HEAD")


def push_ranges(lines) -> tuple:
    """Revision ranges for the commits a pre-push hook is about to send, and the commits pushed."""
    ranges, pushed = [], []
    for line in lines:
        parts = line.split()
        if len(parts) != 4 or parts[1] == ZERO:
            continue
        local, remote = parts[1], parts[3]
        pushed.append(local)
        if remote != ZERO and resolve(remote):
            ranges.append([f"{remote}..{local}"])
        else:
            ranges.append([local, "--not", "--remotes"])
    return ranges, pushed


def worktree_state(repo: Path = REPO) -> tuple:
    """(tracked paths with uncommitted changes, number of untracked files)."""
    status = git("status", "--porcelain", "--untracked-files=all", "--no-renames", repo=repo).splitlines()
    return [line[3:] for line in status if line and not line.startswith("??")], \
        sum(line.startswith("??") for line in status)


def read_context(base=None, fast=False, release=False, denylist=None, push_lines=None) -> Context:
    head = git("rev-parse", "HEAD")
    commit, label = choose_base(base)
    dirty, untracked = worktree_state()
    context = Context(
        head=head, branch=git("rev-parse", "--abbrev-ref", "HEAD"), base=commit, base_label=label,
        fast=fast, release=release, denylist=leak_scan.denylist_path(denylist), dirty=dirty, untracked=untracked,
    )
    if commit != head:
        log = git("log", "--format=%h %s", "--no-merges", f"{commit}..{head}")
        context.commits = log.splitlines()
        diff = git("diff", "--name-status", "--no-renames", commit, head)
        context.changes = [tuple(row.split("\t", 1)) for row in diff.splitlines() if "\t" in row]
    known = {path for _, path in context.changes}
    context.changes += [("U", path) for path in context.dirty if path not in known]
    context.history = [[f"{commit}..{head}"]] if commit != head else []
    if push_lines is not None:
        ranges, pushed = push_ranges(push_lines)
        context.history = ranges
        if any(sha != head for sha in pushed):
            context.notes.append("You are pushing a commit that is not your current checkout. "
                                 "The leak scan read the pushed commits; the other checks ran on the checkout.")
    return context


# Checks. Each returns a Check and never raises.

def run_command(name, command, ok_line, timeout=1800) -> Check:
    started = time.monotonic()
    try:
        done = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as error:
        return Check(name, "fail", f"Could not run: {error}.")
    output = (done.stdout + "\n" + done.stderr).strip().splitlines()
    seconds = round(time.monotonic() - started)
    if done.returncode == 0:
        return Check(name, "pass", ok_line(output, seconds))
    tail = [line for line in output if line.strip()][-8:]
    return Check(name, "fail", f"Failed with exit code {done.returncode}. See the lines below.", tail)


def unit_tests() -> Check:
    def summary(output, seconds):
        ran = next((line for line in reversed(output) if line.startswith("Ran ")), "Ran the tests")
        skipped = re.search(r"skipped=(\d+)", output[-1] if output else "")
        extra = f", {skipped[1]} skipped" if skipped else ""
        return f"{ran.split(' in ')[0].replace('Ran', 'All')} passed{extra} in {seconds} seconds."
    return run_command("Unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"], summary)


def demo() -> Check:
    return run_command("Demo", [sys.executable, "examples/demo/run_demo.py"],
                       lambda output, seconds: "The claim-check demo ran to the end.")


def node_tests() -> Check:
    node = shutil.which("node")
    if not node:
        return Check("JavaScript tests", "skip", "Node.js is not installed, so the JavaScript tests did not run.")
    files = sorted(str(path.relative_to(REPO)) for path in (REPO / "tests").glob("*.test.js"))

    def summary(output, seconds):
        count = next((line.split()[-1] for line in output if line.startswith("# pass")), "all")
        return f"{count} JavaScript tests passed."
    return run_command("JavaScript tests", [node, "--test", *files], summary)


def leak_check(context: Context) -> Check:
    if context.denylist is None:
        return Check("Leak scan", "skip", "No private denylist (SHOTOS_DENYLIST), so nothing was checked for "
                                          "private terms.")
    try:
        entries = leak_scan.load_denylist(context.denylist)
        allowed = leak_scan.load_allowlist(REPO / leak_scan.ALLOWLIST)
        result = leak_scan.scan(REPO, entries, allowed, context.history)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return Check("Leak scan", "fail", f"Could not run: {error}.")
    scope = "tracked files" + (" and the commits being checked" if context.history else "")
    if result["hits"]:
        return Check("Leak scan", "fail", f"{len(result['hits'])} private term(s) found in {scope}. Remove them "
                                          "before pushing.", [hit.describe() for hit in result["hits"][:20]])
    allowed_note = f" {result['allowed']} deliberate use(s) are on the allowlist." if result["allowed"] else ""
    return Check("Leak scan", "pass", f"No private terms in {scope}.{allowed_note}",
                 [f"Allowlist entry {leak_scan.redact_path(path, entries)} {entry} no longer matches anything."
                  for path, entry in result["stale"]])


def skill_folders() -> list:
    """(skill folder, examples folder) for every skill, as the packaging tool finds them."""
    found = [(path, REPO / "examples" / path.name) for path in sorted((REPO / "skills").iterdir())
             if (path / "SKILL.md").is_file()]
    for pack in sorted((REPO / "packs").iterdir()):
        if (pack / "skills").is_dir():
            found += [(path, pack / "examples" / path.name) for path in sorted((pack / "skills").iterdir())
                      if (path / "SKILL.md").is_file()]
    return found


def changed_skills(changes, skills=None) -> list:
    """Skills whose folder or worked example changed."""
    skills = skill_folders() if skills is None else skills
    paths = [path for _, path in changes]
    changed = []
    for skill, examples in skills:
        prefixes = [f"{folder.relative_to(REPO).as_posix()}/" for folder in (skill, examples)]
        if any(path.startswith(prefix) for path in paths for prefix in prefixes):
            changed.append((skill, examples))
    return changed


def guides_changed(changes) -> bool:
    return any(path.startswith(("docs/guides/", "LICENSE")) for _, path in changes)


def zip_links(context: Context) -> Check:
    import package_skills
    skills = skill_folders()
    if context.fast:
        targets = changed_skills(context.changes, skills)
        if guides_changed(context.changes):
            targets += [s for s in skills if s[0].name == "decision-brief" and s not in targets]
        scope = f"{len(targets)} changed skill(s)"
    else:
        targets, scope = skills, f"all {len(skills)} skills"
    if not targets:
        return Check("Skill ZIP links", "skip", "No skill changed, so no ZIP was built.")
    problems = []
    with tempfile.TemporaryDirectory() as out:
        for skill, _ in targets:
            try:
                package_skills.package(skill, Path(out))
            except SystemExit as error:
                problems.append(str(error))
            except (OSError, ValueError) as error:
                problems.append(f"{skill.name}.zip could not be built: {error}")
    if problems:
        return Check("Skill ZIP links", "fail", f"{len(problems)} skill ZIP(s) have links a reader could not "
                                                "follow.", problems[:10])
    return Check("Skill ZIP links", "pass", f"Built ZIPs for {scope}; every link opens.")


def eval_cases() -> list:
    files = [REPO / "evals/cases.json", *sorted((REPO / "evals/core").glob("*.json")),
             *sorted((REPO / "evals/packs").glob("*.json"))]
    cases = []
    for path in files:
        cases += json.loads(path.read_text(encoding="utf-8"))["cases"]
    return cases


def shown(path: Path) -> str:
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def structure_problems(skill: Path, examples: Path, cases) -> list:
    """The mechanical checks from the skill quality gate and CONTRIBUTING.md."""
    name, problems = skill.name, []
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    front = text.split("---", 2)[1] if text.startswith("---\n") else ""
    found = re.search(r"^name:\s*(.+)$", front, re.M)
    if not front:
        problems.append(f"{name}: SKILL.md does not start with front matter.")
    elif not found or found[1].strip().strip("\"'") != name:
        problems.append(f"{name}: the front matter name does not match the folder name.")
    description = re.search(r"^description:\s*(.+)$", front, re.M)
    if front and not description:
        problems.append(f"{name}: the front matter has no description.")
    elif description:
        words = description[1].strip().strip("\"'")
        if len(words) > 1024 or len(words.split()) > 45:
            problems.append(f"{name}: the description is longer than 45 words or 1,024 characters.")
    if not re.search(r"(?im)^##\s+(?:.*\b)?checks\b", text):
        problems.append(f"{name}: SKILL.md has no Checks section saying how to check the result.")
    readme = skill / "README.md"
    if not readme.is_file():
        problems.append(f"{name}: there is no README.md.")
    elif not re.search(r"(?im)^\s*(?:#+\s+|\*\*)Needs\b", readme.read_text(encoding="utf-8")):
        problems.append(f"{name}: README.md does not say what the skill needs.")
    for kind in ("input", "output"):
        if not (examples / f"{kind}.md").is_file():
            problems.append(f"{name}: there is no worked {kind} at {shown(examples / f'{kind}.md')}.")
    kinds = {case.get("type") for case in cases if case.get("skill") == name}
    for kind in ("normal", "contrary"):
        if kind not in kinds:
            problems.append(f"{name}: there is no {kind} eval case.")
    return problems


def skill_structure(context: Context) -> Check:
    targets = changed_skills(context.changes)
    if not targets:
        return Check("Skill structure", "skip", "No skill changed since the base.")
    try:
        cases = eval_cases()
        problems = [problem for skill, examples in targets for problem in structure_problems(skill, examples, cases)]
    except (OSError, ValueError, KeyError, IndexError) as error:
        return Check("Skill structure", "fail", f"Could not run: {error}.")
    if problems:
        return Check("Skill structure", "fail", f"{len(problems)} problem(s) in changed skills.", problems[:20])
    names = ", ".join(skill.name for skill, _ in targets[:6]) + (" and others" if len(targets) > 6 else "")
    return Check("Skill structure", "pass", f"{len(targets)} changed skill(s) have front matter, a Checks section, "
                                            f"a README, worked examples and eval cases: {names}.")


def claim_check() -> Check:
    return Check("Claim check", "skip", "claim_check.py checks an agent's report with a Claims block. It does not "
                                        "check docs, so there is nothing for it to read here.")


def run_checks(context: Context) -> list:
    jobs = [demo, node_tests, lambda: leak_check(context), lambda: zip_links(context),
            lambda: skill_structure(context)]
    if not context.fast:
        jobs.insert(0, unit_tests)
    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        futures = [pool.submit(job) for job in jobs]
        checks = []
        for future in futures:
            try:
                checks.append(future.result())
            except Exception as error:  # a broken check must show on the card, not crash the gate
                checks.append(Check("Gate", "fail", f"A check crashed: {error!r}."))
    if context.fast:
        checks.insert(0, Check("Unit tests", "skip", "Fast mode leaves out the unit tests. Run the full gate "
                                                     "before a release."))
    checks.append(claim_check())
    return checks


# The card.

def release_blockers(context: Context) -> list:
    blockers = []
    if context.fast:
        blockers.append("this was a fast run")
    if context.denylist is None:
        blockers.append("the private denylist was missing")
    if context.dirty:
        blockers.append("there were uncommitted changes")
    return blockers


def decide(context: Context, checks) -> str:
    if any(check.status == "fail" for check in checks):
        return "NO-GO"
    if context.release and release_blockers(context):
        return "NO-GO"
    return "GO"


def areas(changes) -> list:
    labels = [("skills/", "core skills"), ("packs/", "optional packs"), ("rules/", "rules"),
              ("docs/", "docs"), ("tools/", "tools"), ("tests/", "tests"), ("examples/", "examples"),
              ("evals/", "evals"), ("hooks/", "the Stop hook"), ("templates/", "templates"),
              (".github/", "GitHub files"), ("install.py", "the installer")]
    found = []
    for prefix, label in labels:
        if any(path.startswith(prefix) for _, path in changes) and label not in found:
            found.append(label)
    if any("/" not in path and not path.startswith("install.py") for _, path in changes):
        found.append("top-level files")
    return found


def look_at(context: Context, checks) -> list:
    items = []
    for check in checks:
        if check.status == "fail":
            items.append(f"{check.name} failed. Fix it and run the gate again.")
    if context.denylist is None:
        items.append("The private denylist was not found. Set SHOTOS_DENYLIST before a release; until then "
                     "nobody has checked this change for private terms.")
    if context.dirty:
        items.append(f"{len(context.dirty)} file(s) have uncommitted changes. The checks ran on them, but the "
                     "commit itself is what gets pushed.")
    if context.untracked:
        items.append(f"{context.untracked} untracked file(s) were not checked. Add them to Git or remove them.")
    for skill, _ in changed_skills(context.changes):
        items.append(f"{skill.name} changed. A person runs the skill quality gate scenarios on it (normal, "
                     "conflicting source, authority boundary) and records who decided.")
    if any(path.startswith(CONTROL_FILES) for _, path in context.changes):
        items.append("A file that defines or enforces the four controls, the Claims block or the Stop hook "
                     "changed. The release script will stop until the owner approves it, as a major release if "
                     "it breaks them.")
    if not context.fast:
        try:
            import yaml  # noqa: F401
        except ImportError:
            items.append("PyYAML is not installed, so the skill front matter test was skipped. Install it with "
                         "`python -m pip install PyYAML==6.0.3`.")
    items.append(f"The checks ran on one machine: Python {platform.python_version()} on {platform.system()}. "
                 "Other Python versions and systems were not run.")
    return items + context.notes


def render(context: Context, checks, verdict: str, stamp=None) -> str:
    stamp = stamp or datetime.now(timezone.utc)
    blockers = release_blockers(context) + (["the verdict is NO-GO"] if verdict != "GO" else [])
    added = sum(status.startswith("A") for status, _ in context.changes)
    removed = sum(status.startswith("D") for status, _ in context.changes)
    changed = len(context.changes) - added - removed
    lines = [
        f"# SHOTos gate card: {verdict}",
        "",
        f"**Verdict:** {verdict}",
        f"**Commit:** {context.head} on {context.branch}",
        f"**Compared with:** {context.base_label} ({short(context.base)})",
        f"**Mode:** {'fast' if context.fast else 'full'}{', release' if context.release else ''}",
        f"**For release:** {'no, because ' + ' and '.join(blockers) if blockers else 'yes'}",
        f"**Checked:** {stamp:%d %B %Y %H:%M} UTC",
        "",
        "## What changed",
        "",
        f"- {len(context.commits)} commit(s) since {context.base_label}: {added} file(s) added, {changed} changed, "
        f"{removed} removed.",
    ]
    if areas(context.changes):
        lines.append(f"- Areas: {', '.join(areas(context.changes))}.")
    lines += [f"- {commit}" for commit in context.commits[:15]]
    if len(context.commits) > 15:
        lines.append(f"- and {len(context.commits) - 15} more commit(s).")
    lines += ["", "## Checks", ""]
    for check in checks:
        lines.append(f"- {check.status.upper():<4} {check.name}: {check.line}")
        lines += [f"  - {detail}" for detail in check.details]
    lines += ["", "## What a person should look at", ""]
    lines += [f"- {item}" for item in look_at(context, checks)]
    return "\n".join(lines) + "\n"


def safe(text: str, context: Context) -> str:
    """Withhold any line that matches the denylist, so the card cannot carry a private term."""
    if context.denylist is None:
        return text
    try:
        return leak_scan.redact(text, leak_scan.load_denylist(context.denylist))
    except (OSError, ValueError):
        return text


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="ref to compare with (default: where this branch left origin/main)")
    parser.add_argument("--fast", action="store_true", help="leave out the slow checks")
    parser.add_argument("--release", action="store_true",
                        help="NO-GO unless the card can be used for a release (full run, denylist, clean tree)")
    parser.add_argument("--denylist", help="denylist file (default: SHOTOS_DENYLIST)")
    parser.add_argument("--pre-push", action="store_true",
                        help="read the refs being pushed from standard input, as Git gives them to a hook")
    parser.add_argument("--out", type=Path, default=CARDS, help="folder for the card (default: .work/gate)")
    args = parser.parse_args(argv)
    if args.release and (args.fast or args.pre_push):
        parser.error("--release needs the full gate")
    fast = args.fast or args.pre_push
    try:
        context = read_context(args.base, fast, args.release, args.denylist,
                               sys.stdin.read().splitlines() if args.pre_push else None)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"The gate could not start: {error}", file=sys.stderr)
        return 2
    if context.denylist is None:
        print("Warning: SHOTOS_DENYLIST is not set or the file is missing. The leak scan is skipped and this "
              "card cannot be used for a release.", file=sys.stderr)
    print(f"Running the {'fast' if fast else 'full'} gate on {short(context.head)}...", flush=True)
    checks = run_checks(context)
    verdict = decide(context, checks)
    card = safe(render(context, checks, verdict), context)
    path = card_path(context.head, fast, args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(card, encoding="utf-8")
    print(card)
    print(f"Card saved to {path}")
    return 0 if verdict == "GO" else 1


if __name__ == "__main__":
    sys.exit(main())
