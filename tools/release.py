#!/usr/bin/env python3
"""Cut a SHOTos patch or minor release from a GO gate card.

Examples:
  python tools/release.py                                   say what a release would do
  python tools/release.py --publish --review "Sam, PR #140"  cut and publish it

Without --publish nothing in the repository changes: the script checks the
gate card, works out the version, shows the changelog section and rehearses
the ZIP build in a temporary folder.

With --publish it updates the version files and changelog, commits the release,
checks the release commit as fully as the candidate (versions, private terms,
the control check and the full gate), builds the ZIPs, pushes main and the
tag, creates the GitHub release with the ZIPs through the gh CLI and reads the
release back with tools/verify_release.py.

A change that breaks the four controls, the Claims block format or the
claim-check exit codes is a major release. The script cannot tell a harmless
change to those from a breaking one, so it refuses any change to a file that
defines or enforces them (the rule text, the Claims block, the Stop hook and
where it is registered, the installer and claim-check) unless the change is
provably additive, such as a new note or fixture beside the hook. It says the
release needs the owner, as GOVERNANCE.md requires. If the check itself cannot
finish, it says the same. The owner then approves a major release with
--major-approved-by, or a change that breaks nothing with
--controls-approved-by.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import leak_scan  # noqa: E402
from local_gate import card_path  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CORE = ".claude-plugin/plugin.json"
CITATION = "CITATION.cff"
CHANGELOG = "CHANGELOG.md"
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
SUBJECT = "Release SHOTos v{}"
# Folders the ZIPs are built from. Stray files here would end up in a ZIP.
PACKAGED = ["skills", "packs", "examples", "docs/guides", "LICENSE", "LICENSE-docs.md"]
CONTRACT_FAIL = """The fictional task is finished.

## Claims
- [file] created: present.txt
- [file] created: absent.txt
- [command] passes: python -c "print(1)"
- [external] sent: fictional update to the fictional team | receipt: receipts/none.json
- [unverified] I could not check the fictional live site
"""
CONTRACT_PASS = """## Claims
- [file] created: present.txt
- [unverified] nothing else was checked
"""


class Refused(Exception):
    """The release cannot go ahead. The message says why in plain words."""


@dataclass
class Plan:
    previous: str
    candidate: str
    level: str
    version: str
    packs: dict = field(default_factory=dict)  # manifest path -> (old, new)
    section: str = ""
    resumed: bool = False
    notes: list = field(default_factory=list)
    breaks: list = field(default_factory=list)  # what control_breaks found, which the owner approved
    approved_by: str = ""


def run(*command, cwd=None, check=True, input=None, env=None) -> str:
    done = subprocess.run(command, cwd=cwd or REPO, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", input=input, env=env, timeout=1800)
    if check and done.returncode != 0:
        raise Refused(f"`{' '.join(command[:3])}` failed: {(done.stderr or done.stdout).strip()[-600:]}")
    return done.stdout.rstrip()


def git(*args, check=True) -> str:
    return run("git", *args, check=check)


def show(ref: str, path: str) -> str:
    return git("show", f"{ref}:{path}", check=False)


def parse(version: str) -> tuple:
    match = VERSION.fullmatch(version or "")
    if not match:
        raise Refused(f"{version!r} is not a release version")
    return tuple(int(part) for part in match.groups())


def bump(version: str, level: str) -> str:
    major, minor, patch = parse(version)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def core_version(ref: str) -> str:
    return json.loads(show(ref, CORE))["version"]


def previous_tag(ref: str = "HEAD") -> str:
    tag = git("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", ref, check=False)
    if not tag:
        raise Refused("there is no earlier release tag to compare with")
    return tag


def changed_paths(previous: str, candidate: str) -> list:
    return [line for line in git("diff", "--name-only", "--no-renames", previous, candidate).splitlines() if line]


def asks_more_of_the_agent(path: str) -> bool:
    """True when a change alters what a rule or skill asks of the agent, which RELEASING.md makes a minor."""
    if path.startswith(("rules/", "agents/", "hooks/", "templates/")):
        return True
    parts = path.split("/")
    in_skill = (parts[0] == "skills" and len(parts) > 2) or (
        parts[0] == "packs" and len(parts) > 4 and parts[2] == "skills")
    return in_skill and parts[-1] != "README.md"


def choose_level(paths) -> str:
    return "minor" if any(asks_more_of_the_agent(path) for path in paths) else "patch"


def pack_bumps(previous: str, candidate: str, paths) -> dict:
    """New versions for each optional pack with shipped changes, as check_release_versions.py expects."""
    bumps = {}
    for manifest in sorted(set(re.findall(r"^packs/[^/]+/\.claude-plugin/plugin\.json$",
                                          git("ls-tree", "-r", "--name-only", candidate, "--", "packs"),
                                          re.M))):
        before, after = show(previous, manifest), show(candidate, manifest)
        if not before:
            continue  # a new pack ships with the version it was given
        old, new = json.loads(before), json.loads(after)
        prefix = "/".join(manifest.split("/")[:2]) + "/"
        mine = [path for path in paths if path.startswith(prefix) and path != manifest]
        metadata = {k: v for k, v in old.items() if k != "version"} != {k: v for k, v in new.items() if k != "version"}
        if (mine or metadata) and parse(new["version"]) <= parse(old["version"]):
            bumps[manifest] = (new["version"], bump(old["version"], choose_level(mine)))
    return bumps


# The four controls, the Claims block and the exit codes.

# Files that define or enforce them: the rule text, the Claims block format, the Stop hook, the code that
# registers it and claim-check itself. Any change to one needs the owner unless it is provably additive.
CONTROL_FILES = ("docs/controls.md", "docs/claims.md", "templates/AGENTS.md", "tools/claim_check.py", "install.py")
CONTROL_TREES = re.compile(r"(?:rules|hooks|packs/[^/]+/hooks)/")
MANIFEST = re.compile(r"(?:packs/[^/]+/)?\.claude-plugin/(?:plugin|marketplace)\.json")
# Fields in a plugin manifest or marketplace entry that say where hooks come from or whether they load.
HOOK_FIELDS = ("hooks", "strict")


def is_control_file(path: str) -> bool:
    return path in CONTROL_FILES or bool(CONTROL_TREES.match(path))


def is_inert(path: str) -> bool:
    """True for a new file beside the hooks that nothing loads: a note, or a fixture that is not code.

    Claude Code reads only hooks/hooks.json there, and Python only imports code, so these cannot change
    what the hook does. Every new rule card or template is read by agents, so none of those is inert."""
    if not re.match(r"(?:packs/[^/]+/)?hooks/", path) or path.endswith(".py"):
        return False
    return path.endswith((".md", ".txt")) or "/fixtures/" in path


def imported_names(candidate: str) -> set:
    """Top-level modules claim-check and the Stop hook import, which a new file in tools/ could replace."""
    names = {"claim_check", "stop_claim_check"} | set(getattr(sys, "stdlib_module_names", ()))
    for path in ("tools/claim_check.py", "hooks/stop_claim_check.py"):
        text = show(candidate, path)
        if not text:
            continue
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Import):
                names |= {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
                names.add(node.module.split(".")[0])
    return names


def shadows(path: str, names: set) -> bool:
    """True when a new file in tools/ could be imported by claim-check in place of a module it uses."""
    match = re.match(r"tools/([^/]+)", path)
    if not match:
        return False
    if not hasattr(sys, "stdlib_module_names"):
        return True  # this Python cannot list its own modules, so the file may hide one of them
    return match[1].split(".")[0] in names


def hook_registration(text: str, core: str) -> dict:
    """The parts of a plugin manifest or marketplace file that register hooks or locate the core plugin."""
    data = json.loads(text) if text else {}
    found = {field: data.get(field) for field in HOOK_FIELDS if field in data}
    for entry in data.get("plugins", []):
        keep = HOOK_FIELDS + (("source",) if entry["name"] == core else ())
        found[f"plugin {entry['name']}"] = {field: entry[field] for field in keep if field in entry}
    return found


def rule_sections(ref: str) -> dict:
    text = show(ref, "docs/controls.md")
    return {match[1]: match[0].strip() for match in
            re.finditer(r"^## Rule (\d+):.*?(?=^## |\Z)", text, re.M | re.S)}


def control_file_changes(previous: str, candidate: str) -> list:
    """A reason for every change to a file that defines or enforces the controls that is not provably additive."""
    reasons = []
    fields = git("diff", "--name-status", "--no-renames", "-z", previous, candidate).split("\0")
    rows = [(status, path) for status, path in zip(fields[0::2], fields[1::2]) if path]
    core = json.loads(show(candidate, CORE) or show(previous, CORE))["name"]
    names = None
    for status, path in rows:
        verb = {"A": "added", "D": "removed"}.get(status[:1], "changed")
        if is_control_file(path):
            if status == "A" and is_inert(path):
                continue
            detail = ""
            if path == "docs/controls.md":
                before, after = rule_sections(previous), rule_sections(candidate)
                changed = [n for n in sorted(set(before) | set(after), key=int) if before.get(n) != after.get(n)]
                detail = (f" (rule{'s' if len(changed) > 1 else ''} {', '.join(changed)})" if changed
                          else " (outside the rule sections)")
            reasons.append(f"{path} was {verb}{detail}. It defines or enforces the controls, so only the owner "
                           "can say it breaks nothing.")
        elif MANIFEST.fullmatch(path):
            if hook_registration(show(previous, path), core) != hook_registration(show(candidate, path), core):
                reasons.append(f"{path} changed how hooks are registered or where the core plugin loads from.")
        elif status == "A":
            names = imported_names(candidate) if names is None else names
            if shadows(path, names):
                reasons.append(f"{path} was added where claim-check could import it in place of a module it uses.")
    return reasons


def rule_headings(ref: str) -> list:
    return re.findall(r"^## Rule (\d+): (.+?)\s*$", show(ref, "docs/controls.md"), re.M)


def governance_promise(ref: str) -> str:
    text = show(ref, "GOVERNANCE.md")
    match = re.search(r"^## What will not change without a major version\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match[1].strip() if match else ""


def claims_contract(script: Path) -> dict:
    """How a claim-check script treats a fixed fictional report, a passing one and a missing one."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        work = root / "work"
        work.mkdir()
        (work / "present.txt").write_text("fictional\n", encoding="utf-8", newline="\n")
        # Keep the person's own claim-check config, and any commands it allows, out of the check.
        env = {**os.environ, "HOME": str(root), "USERPROFILE": str(root)}
        result = {}
        for name, report in (("fail", CONTRACT_FAIL), ("pass", CONTRACT_PASS), ("missing", None)):
            path = root / f"{name}.md"
            if report is not None:
                path.write_text(report, encoding="utf-8", newline="\n")
            done = subprocess.run([sys.executable, "-I", str(script), str(path), "--cwd", str(work), "--json"],
                                  capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
            try:
                data = json.loads(done.stdout)
                claims = [(item["claim"], item["state"]) for item in data["claims"]]
            except (ValueError, KeyError, TypeError):
                claims = None
            result[name] = (done.returncode, claims)
        return result


@lru_cache(maxsize=8)
def contract_for(text: str) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        script = Path(directory) / "claim_check.py"
        script.write_text(text, encoding="utf-8", newline="\n")
        return claims_contract(script)


def control_breaks(previous: str, candidate: str) -> list:
    """Reasons this change may break a promise GOVERNANCE.md says needs a major release, for the owner to judge.

    Anything this check cannot finish is a reason too: it never passes a change it could not read."""
    try:
        return _control_breaks(previous, candidate)
    except Exception as error:  # noqa: BLE001 - whatever went wrong, the answer is "ask the owner"
        return [f"The control check could not finish ({type(error).__name__}: {error}), so it cannot show "
                "that nothing broke."]


def _control_breaks(previous: str, candidate: str) -> list:
    reasons = []
    before, after = rule_headings(previous), rule_headings(candidate)
    if len(after) != 4:
        reasons.append(f"docs/controls.md now has {len(after)} rules instead of four.")
    elif before != after:
        reasons.append("A rule in docs/controls.md was renamed, removed or reordered.")
    reasons += control_file_changes(previous, candidate)
    if not governance_promise(candidate):
        reasons.append("GOVERNANCE.md no longer says what may not change without a major version.")
    elif governance_promise(previous) != governance_promise(candidate):
        reasons.append("GOVERNANCE.md changed what may not change without a major version.")
    texts = {label: show(ref, "tools/claim_check.py") for label, ref in (("previous", previous),
                                                                         ("candidate", candidate))}
    if not texts["candidate"]:
        reasons.append("tools/claim_check.py was removed.")
    else:
        now = contract_for(texts["candidate"])
        if now["pass"][0] != 0 or now["fail"][0] != 1 or now["missing"][0] != 2:
            reasons.append("claim-check no longer exits 0 for a pass, 1 for a fail and 2 when it cannot run.")
        if texts["previous"] and contract_for(texts["previous"]) != now:
            reasons.append("claim-check reads or judges the standard Claims block differently from "
                           f"{previous}.")
    log = git("log", "--format=%B", f"{previous}..{candidate}")
    if re.search(r"^BREAKING(?: CHANGE)?:", log, re.M):
        reasons.append("A commit message since the last release says it is a breaking change.")
    return reasons


# The gate card and the working tree.

def card_problem(candidate: str):
    """Why the gate card cannot be used for this release, or None when it can."""
    path = card_path(candidate, cards=REPO / ".work" / "gate")
    if not path.is_file():
        return f"there is no gate card for {candidate[:12]}. Run `python tools/local_gate.py --release` first."
    text = path.read_text(encoding="utf-8")
    fields = dict(re.findall(r"^\*\*(.+?):\*\* (.*)$", text, re.M))
    if fields.get("Commit", "").split(" ")[0] != candidate:
        return f"the gate card at {path.name} is for a different commit."
    if fields.get("Verdict") != "GO":
        return "the gate card says NO-GO. Fix what it lists and run the gate again."
    if fields.get("For release") != "yes":
        return f"the gate card cannot be used for a release: {fields.get('For release', 'it does not say')}."
    return None


def tree_problem():
    if git("status", "--porcelain", "--untracked-files=all"):
        return "the checkout has uncommitted or untracked files. Commit or remove them first."
    stray = git("status", "--porcelain", "--ignored", "--untracked-files=all", "--", *PACKAGED)
    if stray:
        return "ignored files sit inside folders the ZIPs are built from: " + \
               ", ".join(line[3:] for line in stray.splitlines()[:5])
    return None


def release_commit():
    """The version HEAD releases, when HEAD is a release commit this script made, published or not."""
    version = core_version("HEAD")
    return version if git("log", "-1", "--format=%s") == SUBJECT.format(version) else None


PACK_MANIFEST = r"packs/[^/]+/\.claude-plugin/plugin\.json"
LEVELS = ("patch", "minor", "major")


def release_extras(candidate: str, release: str) -> list:
    """Paths the release commit changes beyond the version numbers and the changelog."""
    def without_version(path, ref):
        text = show(ref, path)
        if path == CITATION:
            return re.sub(r"^version:.*$", "", text, flags=re.M) if text else None
        try:
            return {k: v for k, v in json.loads(text).items() if k != "version"}
        except (ValueError, AttributeError):
            return None  # unreadable, so it cannot be shown to differ only in its version
    extra = []
    for path in changed_paths(candidate, release):
        if path == CHANGELOG:
            continue
        if path in (CORE, CITATION) or re.fullmatch(PACK_MANIFEST, path):
            before = without_version(path, candidate)
            if before is not None and before == without_version(path, release):
                continue
        extra.append(path)
    return extra


def level_between(previous: str, version: str) -> str:
    old, new = parse(previous), parse(version)
    return "major" if new[0] != old[0] else "minor" if new[1] != old[1] else "patch"


# Changelog.

def generated_section(previous: str, candidate: str) -> str:
    subjects = git("log", "--no-merges", "--reverse", "--format=%s", f"{previous}..{candidate}").splitlines()
    lines = []
    for subject in subjects:
        subject = re.sub(r"\s*\[skip ci\]$", "", subject).strip()
        if subject and not subject.startswith("Release SHOTos"):
            lines.append(f"- {subject}{'' if subject.endswith('.') else '.'}")
    return "\n".join(lines) or "- Maintenance release."


def heading(version: str, day: date) -> str:
    return f"## {version} ({day.day} {day:%B %Y})"


def changelog_with(text: str, version: str, body: str, day: date) -> tuple:
    """(new changelog, section). Keeps a section a maintainer already wrote for this version."""
    top = re.search(r"^## (\S+)[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if top and top[1] == version:
        section = f"{heading(version, day)}\n{top[2].rstrip()}\n"
        return text[:top.start()] + section + "\n" + text[top.end():].lstrip("\n"), section
    if not text.startswith("# Changelog"):
        raise Refused("CHANGELOG.md does not start with its # Changelog heading")
    section = f"{heading(version, day)}\n\n{body.strip()}\n"
    rest = text[len("# Changelog"):].lstrip("\n")
    return f"# Changelog\n\n{section}\n{rest}", section


def set_json_version(text: str, old: str, new: str) -> str:
    updated, count = re.subn(rf'("version"\s*:\s*"){re.escape(old)}(")', rf"\g<1>{new}\g<2>", text, count=1)
    if not count:
        raise Refused(f"could not find version {old} to update")
    return updated


def set_citation_version(text: str, new: str) -> str:
    updated, count = re.subn(rf"^(version:[ \t]*[\"']?){VERSION.pattern}([\"']?[ \t]*)$", rf"\g<1>{new}\g<5>",
                             text, count=1, flags=re.M)
    if not count:
        raise Refused("CITATION.cff has no version line")
    return updated


# Planning and doing.

def needs_owner(breaks) -> Refused:
    return Refused("this needs the owner. It changes what defines or enforces the controls:\n  - "
                   + "\n  - ".join(breaks)
                   + "\nIf it breaks a control, that is a major release: the owner approves it with "
                     "--major-approved-by and a migration note in the changelog. If the owner checked that it "
                     "breaks nothing, they approve it with --controls-approved-by.")


def approve(plan: Plan, breaks, major_owner=None, controls_owner=None) -> None:
    """Record the owner's approval of the control changes, or refuse when there is none."""
    if not breaks:
        return
    if not (major_owner or controls_owner):
        raise needs_owner(breaks)
    plan.breaks, plan.approved_by = list(breaks), major_owner or controls_owner
    if major_owner:
        plan.notes.append(f"Major release approved by {major_owner}: " + " ".join(breaks))
    else:
        plan.notes.append(f"The owner, {controls_owner}, checked these control changes and approved them as "
                          "breaking nothing: " + " ".join(breaks))


def make_plan(level=None, major_owner=None, notes_file=None, day=None, controls_owner=None) -> Plan:
    version = release_commit()
    if version:
        # Carry on after a failed step. Each publishing step can safely run again.
        previous = previous_tag("HEAD^")
        candidate = git("rev-parse", "HEAD^")
        extra = release_extras(candidate, "HEAD")
        if extra:
            raise Refused("the release commit changes more than the version files and changelog: "
                          + ", ".join(extra[:5]))
        section = re.search(r"^## " + re.escape(version) + r".*?(?=^## |\Z)", show("HEAD", CHANGELOG), re.M | re.S)
        plan = Plan(previous, candidate, "resume", version, section=section[0].strip() + "\n" if section else "",
                    resumed=True)
        # Carrying on never skips the control check: the commit about to be published is checked again.
        breaks = control_breaks(previous, "HEAD")
        approve(plan, breaks, major_owner, controls_owner)
        made, needed = level_between(core_version(previous), version), "major" if major_owner else "minor"
        if breaks and LEVELS.index(made) < LEVELS.index(needed):
            raise Refused(f"the release commit makes a {made} release, v{version}, but the approval given needs a "
                          f"{needed}. Remove the release commit with `git reset --hard HEAD^` and run again.")
        plan.notes.append(f"HEAD already prepares v{version}; carrying on from there.")
        return plan
    previous = previous_tag()
    candidate = git("rev-parse", "HEAD")
    if candidate == git("rev-parse", f"{previous}^{{commit}}"):
        raise Refused(f"nothing has changed since {previous}")
    paths = changed_paths(previous, candidate)
    chosen = choose_level(paths)
    if level == "minor" and chosen == "patch":
        chosen = "minor"
    breaks = control_breaks(previous, candidate)
    if breaks and not (major_owner or controls_owner):
        raise needs_owner(breaks)
    if major_owner:
        chosen = "major"
    elif breaks:
        chosen = "minor"  # the owner approved a change to what a rule asks of the agent: a minor at least
    version = bump(core_version(previous), chosen)
    if parse(core_version(candidate)) > parse(version):
        raise Refused(f"{CORE} already names {core_version(candidate)}, ahead of the planned {version}")
    body = Path(notes_file).read_text(encoding="utf-8") if notes_file else generated_section(previous, candidate)
    changelog = show(candidate, CHANGELOG)
    top = re.search(rf"^## ({VERSION.pattern})", changelog, re.M)
    if top and top[1] != version and parse(top[1]) > parse(core_version(previous)):
        raise Refused(f"CHANGELOG.md starts with a section for {top[1]}, but this release is {version}")
    _, section = changelog_with(changelog, version, body, day or date.today())
    if chosen == "major" and "migration" not in section.lower():
        raise Refused("a major release needs a migration note in its changelog section")
    plan = Plan(previous, candidate, chosen, version, pack_bumps(previous, candidate, paths), section)
    approve(plan, breaks, major_owner, controls_owner)
    if any(path.startswith(("rules/", "install.py", "skills/")) for path in paths):
        plan.notes.append("Rules, a core skill or the installer changed. RELEASING.md asks for an outcome eval "
                          "run on at least one model; keep the result with the review.")
    return plan


def write_release(plan: Plan, review: str, day: date) -> None:
    """Update the version files and changelog, then commit the release."""
    core = REPO / CORE
    core.write_text(set_json_version(core.read_text(encoding="utf-8"), core_version("HEAD"), plan.version),
                    encoding="utf-8", newline="\n")
    citation = REPO / CITATION
    citation.write_text(set_citation_version(citation.read_text(encoding="utf-8"), plan.version),
                        encoding="utf-8", newline="\n")
    changelog = REPO / CHANGELOG
    body = plan.section.split("\n", 1)[1]
    text, _ = changelog_with(changelog.read_text(encoding="utf-8"), plan.version, body, day)
    changelog.write_text(text, encoding="utf-8", newline="\n")
    for manifest, (old, new) in plan.packs.items():
        path = REPO / manifest
        path.write_text(set_json_version(path.read_text(encoding="utf-8"), old, new), encoding="utf-8",
                        newline="\n")
    git("add", "--", CORE, CITATION, CHANGELOG, *plan.packs)
    approval = f"\nControl changes approved by the owner: {plan.approved_by}" if plan.approved_by else ""
    git("commit", "-q", "-s", "-m", SUBJECT.format(plan.version), "-m",
        f"Independent review: {review}\nGate card: {plan.candidate[:12]} GO{approval}")


def build_zips(out: Path, commit: str) -> int:
    if out.exists():
        shutil.rmtree(out)
    run(sys.executable, "tools/package_skills.py", "--all-packs", "--out", str(out), "--source-commit", commit)
    return len(list(out.glob("*.zip")))


def check_release_commit(plan: Plan, release: str = "HEAD") -> None:
    """The checks the release commit itself must pass, besides the gate: versions, private terms, that it
    changes only the version files and changelog, and the control check, which is never skipped."""
    run(sys.executable, "tools/check_release_versions.py", plan.previous)
    denylist = leak_scan.denylist_path()
    if denylist is None:
        raise Refused("the private denylist (SHOTOS_DENYLIST) is missing, so the release commit cannot be checked")
    result = leak_scan.scan(REPO, leak_scan.load_denylist(denylist),
                            leak_scan.load_allowlist(REPO / leak_scan.ALLOWLIST), [[f"{release}^..{release}"]])
    if result["hits"]:
        raise Refused("the release commit has private terms: " + "; ".join(h.describe() for h in result["hits"]))
    extra = release_extras(plan.candidate, release)
    if extra:
        raise Refused("the release commit changes more than the version files and changelog: " + ", ".join(extra[:5]))
    breaks = control_breaks(plan.previous, release)
    if breaks and (not plan.approved_by or breaks != plan.breaks):
        raise needs_owner(breaks)


def gate_release_commit(plan: Plan, release: str) -> None:
    """Run the full gate on the commit that will be published, unless it already has a GO release card."""
    if card_problem(release):
        run(sys.executable, "tools/local_gate.py", "--release", "--base", plan.previous, check=False)
    problem = card_problem(release)
    if problem:
        raise Refused(f"the release commit {release[:12]} did not pass the gate: {problem} It has not been pushed.")


def publish(plan: Plan, review: str, day: date) -> list:
    done = []
    git("fetch", "-q", "origin")
    if not plan.resumed and plan.candidate != git("rev-parse", "origin/main", check=False):
        raise Refused("release from main as it is on GitHub: HEAD is not the same commit as origin/main")
    if not plan.resumed:
        write_release(plan, review, day)
        done.append(f"Committed {SUBJECT.format(plan.version)}.")
    release = git("rev-parse", "HEAD")
    check_release_commit(plan, release)
    done.append("Checked the release versions, scanned the release commit for private terms, checked it changes "
                "only the version files and changelog, and checked the controls again.")
    gate_release_commit(plan, release)
    done.append(f"The full gate card for the release commit {release[:12]} is GO.")
    assets = REPO / "dist" / f"v{plan.version}"
    count = build_zips(assets, release)
    done.append(f"Built {count} skill ZIPs in dist/v{plan.version}.")
    if shutil.which("claude"):
        run("claude", "plugin", "validate", ".")
        done.append("`claude plugin validate .` passed.")
    else:
        done.append("Skipped `claude plugin validate .`: the claude CLI is not installed.")
    tag = f"v{plan.version}"
    git("push", "origin", "HEAD:refs/heads/main")
    if not git("tag", "--list", tag):
        git("tag", tag)
    git("push", "origin", f"refs/tags/{tag}")
    done.append(f"Pushed main and the tag {tag}.")
    notes = REPO / ".work" / "release" / f"notes-{tag}.md"
    notes.parent.mkdir(parents=True, exist_ok=True)
    notes.write_text(plan.section.split("\n", 1)[1].strip() + "\n", encoding="utf-8", newline="\n")
    if run("gh", "release", "view", tag, check=False):
        done.append(f"The GitHub release {tag} already exists; it was left as it is.")
    else:
        run("gh", "release", "create", tag, "--verify-tag", "--title", f"SHOTos {tag}", "--notes-file", str(notes),
            *sorted(str(path) for path in assets.glob("*.zip")))
        done.append(f"Created the GitHub release {tag} with {count} ZIPs.")
    print(withheld(run(sys.executable, "tools/verify_release.py", tag, "--assets", str(assets))))
    done.append("Read the release back with tools/verify_release.py.")
    return done


def rehearse(plan: Plan) -> str:
    with tempfile.TemporaryDirectory() as directory:
        count = build_zips(Path(directory) / "skills", plan.candidate)
    return f"Rehearsed the ZIP build: {count} skill ZIPs built and every link opens."


def summary(plan: Plan) -> list:
    lines = [f"Release v{plan.version} ({plan.level}) after {plan.previous}, from {plan.candidate[:12]}."]
    if plan.packs:
        lines.append("Optional packs: " + ", ".join(f"{path.split('/')[1]} {old} -> {new}"
                                                    for path, (old, new) in plan.packs.items()) + ".")
    lines += plan.notes
    return lines


def withheld(text: str) -> str:
    """The text with each line that holds a private term withheld, when the denylist is set.

    Errors can quote git output, such as the paths in a refused release commit."""
    denylist = leak_scan.denylist_path()
    if denylist is None:
        return text
    try:
        return leak_scan.redact(text, leak_scan.load_denylist(denylist))
    except (OSError, ValueError):
        return text


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    say = lambda text, **kwargs: print(withheld(str(text)), **kwargs)  # noqa: E731
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--publish", action="store_true", help="cut and publish the release (default: dry run)")
    parser.add_argument("--review", help="who did the independent review, or a link to it (needed to publish)")
    parser.add_argument("--minor", action="store_true", help="make it a minor release even if a patch would do")
    parser.add_argument("--notes", help="file with the changelog text (default: one line per commit)")
    parser.add_argument("--major-approved-by", metavar="OWNER",
                        help="for the owner only: allow a major release that breaks the controls")
    parser.add_argument("--controls-approved-by", metavar="OWNER",
                        help="for the owner only: the control changes were checked and break nothing, so "
                             "release them as a minor")
    args = parser.parse_args(argv)
    if args.publish and not (args.review or "").strip():
        parser.error("--publish needs --review: name who did the independent review, or link to it")
    if args.major_approved_by and args.controls_approved_by:
        parser.error("pass --major-approved-by or --controls-approved-by, not both")
    day = date.today()
    try:
        plan = make_plan("minor" if args.minor else None, args.major_approved_by, args.notes, day,
                         args.controls_approved_by)
        problem = card_problem(plan.candidate) or tree_problem()
        if problem:
            raise Refused(problem)
        for line in summary(plan):
            say(line)
        say("\n" + plan.section)
        if not args.publish:
            say(rehearse(plan))
            say("\nDry run: nothing was changed. Run again with --publish --review \"...\" to release.")
            return 0
        for line in publish(plan, args.review.strip(), day):
            say(line)
    except Refused as error:
        say(f"Release stopped: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        say(f"Release stopped: {error}", file=sys.stderr)
        return 2
    print(f"\nReleased v{plan.version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
