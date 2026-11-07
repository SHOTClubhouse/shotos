#!/usr/bin/env python3
"""Install or uninstall SHOTos skills, tools and the optional claim-check hook.

Deterministic: it copies files from this repository and records, relative to the
target folder, every file it created (with a checksum), every folder it created
and every line it added. --uninstall reverses exactly that. It never touches a
path outside the target, never removes a file you have changed since install,
and never downloads anything. Use --dry-run to see the plan first.

Examples:
  python install.py --runtime claude --scope project --dry-run
  python install.py --runtime claude --scope project --with-hook
  python install.py --runtime codex --scope user
  python install.py --runtime all --scope project
  python install.py --runtime gemini --scope project
  python install.py --runtime antigravity --scope project
  python install.py --pack exec-ops --pack win-the-work
  python install.py --all-packs --with-agents
  python install.py --list-packs
  python install.py --status --scope project
  python install.py --uninstall --scope project
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from tools.skill_resources import example_files, portable_markdown, portable_readme

REPO = Path(__file__).resolve().parent
MANIFEST = ".shotos-install.json"
SKILL_DIRS = {
    ("claude", "project"): ".claude/skills",
    ("claude", "user"): ".claude/skills",
    ("codex", "project"): ".codex/skills",
    ("codex", "user"): ".codex/skills",
    ("agents", "project"): ".agents/skills",
    ("agents", "user"): ".agents/skills",
    ("gemini", "project"): ".gemini/skills",
    ("gemini", "user"): ".gemini/skills",
    ("antigravity", "project"): ".agents/skills",
    ("antigravity", "user"): ".gemini/config/skills",
}
# "all" installs for every runtime at once: Claude Code reads .claude/skills; Codex, Gemini CLI and Antigravity
# all read the shared .agents/skills folder. One command, one AGENTS.md, no drift between copies.
ALL = ("claude", "agents")
# Runtimes that need one line in their own instruction file to load AGENTS.md, the shared canon.
# Codex reads AGENTS.md itself. Claude Code reads CLAUDE.md. Gemini CLI and Antigravity read GEMINI.md.
IMPORT_FILES = {"claude": "CLAUDE.md", "gemini": "GEMINI.md", "antigravity": "GEMINI.md", "agents": "GEMINI.md"}
HOOK_COMMAND = 'sh "$CLAUDE_PROJECT_DIR/.shotos/hooks/run_hook.sh"'
WORK_LINE = ".work/"
IMPORT_LINE = "@AGENTS.md"
CANON_LINE = "For SHOTos work, read and apply the installed working agreement at .shotos/templates/AGENTS.md."


class InstallError(Exception):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, rel: str):
    path = (root / rel).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def contained(root: Path, path: Path) -> bool:
    """True if path, after following every symlink on the way, stays inside root."""
    probe = path
    while not probe.exists() and not probe.is_symlink():
        if probe.parent == probe:
            return False
        probe = probe.parent
    try:
        probe.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def b64(data):
    return None if data is None else base64.b64encode(data).decode("ascii")


def available_packs() -> list:
    return sorted(p.name for p in (REPO / "packs").iterdir() if (p / "skills").is_dir()) if (REPO / "packs").is_dir() else []


def plan(runtime: str, scope: str, root: Path, with_hook: bool, packs=(), with_agents=False, packs_only=False):
    runtimes = ALL if runtime == "all" else (runtime,)
    for r in runtimes:
        if (r, scope) not in SKILL_DIRS:
            raise InstallError(f"{r} does not support {scope} scope")
    unknown = sorted(set(packs) - set(available_packs()))
    if unknown:
        raise InstallError(f"unknown pack(s): {', '.join(unknown)}. Run --list-packs to see them.")
    copies = []
    sources = [] if packs_only else [REPO / "skills"]
    sources += [REPO / "packs" / name / "skills" for name in packs]
    for r in runtimes:
        skills_dir = root / SKILL_DIRS[(r, scope)]
        for source in sources:
            for skill in sorted(source.iterdir()):
                if (skill / "SKILL.md").is_file():
                    destination = skills_dir / skill.name
                    copies.append((skill, destination))
                    copies.extend((source, destination / name) for source, name in example_files(skill))
    if with_agents:
        if "claude" not in runtimes:
            raise InstallError("--with-agents installs Claude Code subagents; for other runtimes paste agents/*.md as instructions")
        for agent in sorted((REPO / "agents").glob("*.md")):
            if agent.name != "README.md":
                copies.append((agent, root / ".claude" / "agents" / agent.name))
    project = scope == "project"
    if project and not packs_only:
        copies += [
            (REPO / "tools" / "claim_check.py", root / ".shotos" / "tools" / "claim_check.py"),
            (REPO / "tools" / "graduation_log.py", root / ".shotos" / "tools" / "graduation_log.py"),
            (REPO / "rules", root / ".shotos" / "rules"),
            (REPO / "agents", root / ".shotos" / "agents"),
            (REPO / "lenses", root / ".shotos" / "lenses"),
            (REPO / "hooks" / "stop_claim_check.py", root / ".shotos" / "hooks" / "stop_claim_check.py"),
            (REPO / "hooks" / "run_hook.sh", root / ".shotos" / "hooks" / "run_hook.sh"),
            (REPO / "templates", root / ".shotos" / "templates"),
            (REPO / "docs" / "claims.md", root / ".shotos" / "claims.md"),
            (REPO / "docs" / "connect-your-tools.md", root / ".shotos" / "docs" / "connect-your-tools.md"),
            (REPO / "docs" / "full-pack.md", root / ".shotos" / "docs" / "full-pack.md"),
            (REPO / "LICENSE", root / ".shotos" / "LICENSE"),
            (REPO / "LICENSE-docs.md", root / ".shotos" / "LICENSE-docs.md"),  # the credit line the CC BY files need travels with them
        ]
        if not (root / "AGENTS.md").exists():
            copies.append((REPO / "templates" / "AGENTS.md", root / "AGENTS.md"))
    if project:
        for name in packs:
            scripts = REPO / "packs" / name / "scripts"
            if scripts.is_dir():
                copies.append((scripts, root / ".shotos" / "packs" / name / "scripts"))
    hook = with_hook and "claude" in runtimes and project
    import_files = list(dict.fromkeys(IMPORT_FILES[r] for r in runtimes if r in IMPORT_FILES)) if project else []
    if runtime == "agents" or packs_only:
        import_files = []  # plain .agents/skills install: the user chose no runtime-specific file
    return copies, hook, import_files


def read_settings(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise InstallError(f"{path} is not plain JSON ({error}). Nothing was changed. Add the hook by hand: "
                           f'Stop -> command: {HOOK_COMMAND}')


def write_settings(path: Path, settings: dict) -> None:
    path.write_bytes((json.dumps(settings, indent=2) + "\n").encode("utf-8"))


def add_hook(settings_path: Path) -> None:
    settings = read_settings(settings_path)
    stops = settings.setdefault("hooks", {}).setdefault("Stop", [])
    if not any(h.get("command") == HOOK_COMMAND for group in stops for h in group.get("hooks", [])):
        stops.append({"hooks": [{"type": "command", "command": HOOK_COMMAND, "timeout": 120}]})
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    write_settings(settings_path, settings)


def remove_hook(settings_path: Path) -> None:
    try:
        settings = read_settings(settings_path)
    except InstallError as error:
        print(f"skip  {error}")
        return
    if not settings:
        return
    stops = settings.get("hooks", {}).get("Stop", [])
    kept = [g for g in stops if not any(h.get("command") == HOOK_COMMAND for h in g.get("hooks", []))]
    if kept:
        settings["hooks"]["Stop"] = kept
    else:
        settings.get("hooks", {}).pop("Stop", None)
        if not settings.get("hooks"):
            settings.pop("hooks", None)
    write_settings(settings_path, settings)


def add_line(path: Path, line: str):
    """Add a line to a text file if missing, byte for byte. Returns 'created', 'appended' or False."""
    newline = b"\n"
    wanted = line.encode("utf-8")
    if path.is_file():
        data = path.read_bytes()
        if wanted in [part.rstrip(b"\r\n") for part in data.splitlines()]:
            return False
        if b"\r\n" in data:
            newline = b"\r\n"
        path.write_bytes(data + (b"" if data.endswith(b"\n") or not data else newline) + wanted + newline)
        return "appended"
    path.write_bytes(wanted + newline)
    return "created"


def remove_line(path: Path, line: str, created: bool) -> None:
    """Remove the last copy of a line, leaving every other byte as it was."""
    if not path.is_file():
        return
    wanted = line.encode("utf-8")
    parts = path.read_bytes().splitlines(keepends=True)
    for index in range(len(parts) - 1, -1, -1):
        if parts[index].rstrip(b"\r\n") == wanted:
            del parts[index]
            break
    if created and not parts:
        path.unlink()
        return
    path.write_bytes(b"".join(parts))


def restore_or_trim(root: Path, rel: str, edit: dict, line, dry_run: bool, created_state) -> None:
    """Undo one edit to an existing text file: exact original bytes if untouched since, else remove our line only."""
    path = root / rel
    if not path.is_file():
        return
    label = "settings.json hook" if line is None else f"{line} from {rel}"
    print(f"{'would remove' if dry_run else 'remove'}  {label}")
    if dry_run:
        return
    if edit and sha(path) == edit.get("after"):
        original = edit.get("original")
        if original is None:
            path.unlink()
        else:
            path.write_bytes(base64.b64decode(original))
    elif line is None:
        remove_hook(path)
    else:
        remove_line(path, line, created_state == "created")


def write_manifest(path: Path, manifest: dict) -> None:
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temp = Path(stream.name)
            json.dump(manifest, stream, indent=2)
            stream.write("\n")
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


@contextmanager
def install_lock(root: Path):
    path = root / ".shotos-install.lock"
    try:
        handle = path.open("x", encoding="utf-8")
    except FileExistsError as error:
        raise InstallError("Another install or uninstall is active for this target. If it was interrupted, check the target before removing its lock.") from error
    try:
        with handle:
            handle.write(f"{os.getpid()}\n")
        yield
    finally:
        path.unlink(missing_ok=True)


def installed_markdown_locations(copies):
    locations = {}
    for original, installed in copies:
        locations.setdefault(original.resolve(), installed)
        if original.is_dir():
            for resource in original.rglob("*.md"):
                locations.setdefault(resource.resolve(), installed / resource.relative_to(original))
    return locations


def install(runtime: str, scope: str, root: Path, with_hook: bool, dry_run: bool, packs=(), with_agents=False) -> int:
    root = root.resolve()
    manifest_path = root / MANIFEST
    previous = None
    packs = sorted(set(packs))
    if manifest_path.exists():
        if manifest_path.is_symlink() or not contained(root, manifest_path):
            raise InstallError("The existing manifest is a link. Nothing was changed.")
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (previous.get("version") != 2 or (previous.get("runtime"), previous.get("scope")) != (runtime, scope)
                or (with_hook and not previous.get("hook")) or (with_agents and not previous.get("agents"))):
            raise InstallError("Use the existing runtime and scope when adding packs. Reinstall to change setup options.")
        packs = [name for name in packs if name not in previous.get("packs", [])]
        if not packs:
            print("The requested packs are already installed. Nothing was changed.")
            return 0
    copies, hook, import_files = plan(runtime, scope, root, with_hook and previous is None, packs,
                                     with_agents and previous is None, packs_only=previous is not None)
    existing_agreement = previous is None and scope == "project" and (root / "AGENTS.md").is_file()
    settings_path = root / ".claude" / "settings.json"
    if hook:
        read_settings(settings_path)
    outside = [dst for dst in [d for _, d in copies] + [root / ".gitignore"] + [root / n for n in import_files]
               + ([root / "AGENTS.md"] if existing_agreement else [])
               + ([settings_path] if hook else []) if not contained(root, dst)]
    if outside:
        raise InstallError("these paths lead outside the target folder (through a symlink), so nothing was changed:\n  "
                           + "\n  ".join(str(d) for d in outside))
    clashes = [dst for _, dst in copies if dst.exists()]
    verb = "would" if dry_run else "will"
    for src, dst in copies:
        print(f"{verb} copy  {src.relative_to(REPO)}  ->  {dst.relative_to(root)}")
    if hook:
        print(f"{verb} add   the claim-check Stop hook to .claude/settings.json")
    elif with_hook and previous is None:
        print("note  --with-hook only applies to Claude Code in project scope, so no hook was added")
    if scope == "project" and previous is None:
        print(f"{verb} add   {WORK_LINE} to .gitignore (if missing)")
    if existing_agreement:
        print(f"{verb} link  the installed SHOTos agreement from the existing AGENTS.md")
    for name in import_files:
        print(f"{verb} add   {IMPORT_LINE} to {name} (if missing), so the four rules load")
    if clashes:
        print("\nThese already exist, so nothing was changed:\n  " + "\n  ".join(str(c.relative_to(root)) for c in clashes))
        return 1
    if dry_run:
        print("\nDry run: nothing was changed.")
        return 0

    manifest = {"version": 2, "runtime": runtime, "scope": scope, "packs": list(packs), "agents": with_agents,
                "files": {}, "dirs": [],
                "hook": False, "gitignore": False, "import_files": {}, "edits": {}}

    def record(rel: str, before) -> None:
        manifest["edits"][rel] = {"original": b64(before), "after": sha(root / rel)}

    shared_guides = tuple(root / ".shotos" / name for name in ("docs", "rules", "agents", "lenses", "templates"))
    locations = installed_markdown_locations(copies) if scope == "project" and previous is None else {}
    try:
        for src, dst in copies:
            missing = []
            parent = dst.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for folder in reversed(missing):
                folder.mkdir()
                manifest["dirs"].append(folder.relative_to(root).as_posix())
            if src.is_dir():
                readme = portable_readme(src, REPO) if (src / "SKILL.md").is_file() else None
                shutil.copytree(src, dst)
                manifest["dirs"].append(dst.relative_to(root).as_posix())
                files = [p for p in dst.rglob("*") if p.is_file()]
                manifest["dirs"] += [p.relative_to(root).as_posix() for p in dst.rglob("*") if p.is_dir()]
            else:
                shutil.copy2(src, dst)
                files = [dst]
            for f in files:
                relative_path = f.relative_to(root).as_posix()
                manifest["files"][relative_path] = sha(f)
                if locations and f.suffix == ".md" and any(f.is_relative_to(folder) for folder in shared_guides):
                    original = src / f.relative_to(dst) if src.is_dir() else src
                    guide = portable_markdown(original, REPO, locations, installed_dir=f.parent)
                    f.write_bytes(guide.encode("utf-8"))
                    manifest["files"][relative_path] = sha(f)
            if src.is_dir() and readme is not None:
                installed_readme = dst / "README.md"
                installed_readme.write_bytes(readme.encode("utf-8"))
                manifest["files"][installed_readme.relative_to(root).as_posix()] = sha(installed_readme)
        if hook:
            before = settings_path.read_bytes() if settings_path.is_file() else None
            if not settings_path.parent.exists():
                manifest["dirs"].append(settings_path.parent.relative_to(root).as_posix())
            add_hook(settings_path)
            manifest["hook"] = True
            record(".claude/settings.json", before)
        if scope == "project" and previous is None:
            before = (root / ".gitignore").read_bytes() if (root / ".gitignore").is_file() else None
            manifest["gitignore"] = add_line(root / ".gitignore", WORK_LINE)
            if manifest["gitignore"]:
                record(".gitignore", before)
        if existing_agreement:
            before = (root / "AGENTS.md").read_bytes()
            manifest["agreement_link"] = add_line(root / "AGENTS.md", CANON_LINE)
            if manifest["agreement_link"]:
                record("AGENTS.md", before)
        for name in import_files:
            before = (root / name).read_bytes() if (root / name).is_file() else None
            state = add_line(root / name, IMPORT_LINE)
            if state:
                manifest["import_files"][name] = state
                record(name, before)
        if previous is None:
            write_manifest(manifest_path, manifest)
        else:
            combined = {
                **previous,
                "packs": sorted(set(previous.get("packs", [])) | set(packs)),
                "files": {**previous["files"], **manifest["files"]},
                "dirs": list(dict.fromkeys(previous["dirs"] + manifest["dirs"])),
            }
            write_manifest(manifest_path, combined)
    except Exception:
        print("\nInstall failed part-way; rolling back.")
        _reverse(root, manifest)
        raise
    print(f"\nInstalled. Manifest: {manifest_path.name}")
    return 0


def _reverse(root: Path, manifest: dict, dry_run=False) -> list:
    kept = []
    edits = manifest.get("edits", {})
    for rel, digest in manifest.get("files", {}).items():
        path = inside(root, rel)
        if path is None:
            print(f"skip  {rel} (outside the target folder)")
            continue
        if not path.is_file():
            continue
        if sha(path) != digest:
            kept.append(rel)
            print(f"keep  {rel} (changed since install)")
            continue
        print(f"{'would remove' if dry_run else 'remove'}  {rel}")
        if not dry_run:
            path.unlink()
    if manifest.get("hook"):
        restore_or_trim(root, ".claude/settings.json", edits.get(".claude/settings.json"), None, dry_run, None)
    if manifest.get("gitignore"):
        restore_or_trim(root, ".gitignore", edits.get(".gitignore"), WORK_LINE, dry_run, manifest["gitignore"])
    if manifest.get("agreement_link"):
        restore_or_trim(root, "AGENTS.md", edits.get("AGENTS.md"), CANON_LINE, dry_run, manifest["agreement_link"])
    imports = dict(manifest.get("import_files", {}))
    if manifest.get("claude_md"):  # manifests written before Gemini and Antigravity were added
        imports["CLAUDE.md"] = manifest["claude_md"]
    for name, state in imports.items():
        restore_or_trim(root, name, edits.get(name), IMPORT_LINE, dry_run, state)
    if not dry_run:
        shotos = root / ".shotos"
        if shotos.is_dir():
            for cache in [c for c in shotos.rglob("__pycache__") if c.is_dir()]:
                shutil.rmtree(cache, ignore_errors=True)  # bytecode written when the tools ran, never installed by us
        for rel in sorted(manifest.get("dirs", []), key=lambda d: d.count("/"), reverse=True):
            path = inside(root, rel)
            if path is not None and path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    return kept


def uninstall(root: Path, dry_run: bool) -> int:
    root = root.resolve()
    manifest_path = root / MANIFEST
    if not manifest_path.is_file():
        print(f"No manifest at {manifest_path}; nothing to remove.")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != 2:
        print("This manifest is from an older installer. Remove the files it lists by hand.")
        return 1
    kept = _reverse(root, manifest, dry_run=dry_run)
    if not dry_run:
        manifest_path.unlink()
    if kept:
        print(f"\nKept {len(kept)} file(s) you changed after install. Remove them yourself if you want them gone.")
    print("\nDry run: nothing was changed." if dry_run else "\nUninstalled.")
    return 0


def status(root: Path) -> int:
    root = root.resolve()
    manifest_path = root / MANIFEST
    if manifest_path.is_symlink():
        raise InstallError("The existing manifest is a link.")
    if not manifest_path.is_file():
        print("No installer-managed SHOTos setup was found here. Manually copied skills are outside this check.")
        return 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), dict):
        raise InstallError("The install manifest does not contain a managed file list.")
    packs = manifest.get("packs", [])
    if not isinstance(packs, list) or not all(isinstance(name, str) for name in packs):
        raise InstallError("The install manifest has an invalid pack list.")
    print(f"Runtime: {manifest.get('runtime', 'unknown')}. Scope: {manifest.get('scope', 'unknown')}.")
    print(f"Optional packs: {', '.join(packs) if packs else 'none'}.")
    files = manifest["files"]
    differences = []
    for name, digest in sorted(files.items()):
        relative = Path(name)
        path = root / relative
        if relative.is_absolute() or relative.anchor or ".." in relative.parts or not contained(root, path):
            differences.append(("Skipped outside target", name))
        elif path.is_symlink() or (path.exists() and not path.is_file()):
            differences.append(("Replaced", name))
        elif not path.exists():
            differences.append(("Missing", name))
        elif sha(path) != digest:
            differences.append(("Changed", name))
    print(f"Managed files: {len(files)} recorded, {len(files) - len(differences)} unchanged.")
    for description, name in differences:
        print(f"  {description}: {name}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runtime", choices=["all", "claude", "codex", "gemini", "antigravity", "agents"], default="claude")
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--target", help="project folder (default: current folder) or home folder for user scope")
    parser.add_argument("--with-hook", action="store_true", help="add the claim-check Stop hook (Claude Code, project scope)")
    parser.add_argument("--pack", action="append", default=[], help="also install this pack's skills (repeatable)")
    parser.add_argument("--all-packs", action="store_true", help="install every pack")
    parser.add_argument("--with-agents", action="store_true", help="install the role agents into .claude/agents (Claude Code)")
    parser.add_argument("--dry-run", action="store_true")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--list-packs", action="store_true", help="list the packs and exit")
    action.add_argument("--status", action="store_true", help="check the recorded setup without changing the target")
    action.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    if args.list_packs:
        for name in available_packs():
            skills = sorted(p.name for p in (REPO / "packs" / name / "skills").iterdir() if (p / "SKILL.md").is_file())
            print(f"{name:20} {', '.join(skills)}")
        return 0
    packs = available_packs() if args.all_packs else list(dict.fromkeys(args.pack))
    default = Path.home() if args.scope == "user" else Path.cwd()
    root = Path(args.target) if args.target else default
    try:
        if args.status:
            return status(root)
        if args.dry_run or (args.uninstall and not root.exists()):
            return uninstall(root, True) if args.uninstall else install(
                args.runtime, args.scope, root, args.with_hook, True, packs, args.with_agents)
        root.mkdir(parents=True, exist_ok=True)
        with install_lock(root.resolve()):
            return uninstall(root, False) if args.uninstall else install(
                args.runtime, args.scope, root, args.with_hook, False, packs, args.with_agents)
    except (InstallError, OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
