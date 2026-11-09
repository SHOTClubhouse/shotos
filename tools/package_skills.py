#!/usr/bin/env python3
"""Package SHOTos skills as zip files for upload to the Claude app or claude.ai.

The Claude apps take a custom skill as a zip holding the skill folder, with
SKILL.md inside it. See docs/guides/chat-assistants.md for upload and file setup.
Each zip made here is one skill. Upload the ones you want, one at a time.

Examples:
  python tools/package_skills.py                     core skills only
  python tools/package_skills.py --pack exec-ops     core plus one pack
  python tools/package_skills.py --all-packs --out dist/skills
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from skill_resources import PUBLIC_REPO, example_files, portable_markdown, portable_readme

REPO = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
LINKS = re.compile(r"\]\(\s*<?([^\s)>]+)|^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)")
SOURCE_LINK = re.compile(re.escape(PUBLIC_REPO) + r"/(?:blob|tree)/([^/]+)/([^?#]+)")


def require_source(path: Path) -> None:
    if not path.is_relative_to(REPO) or path.resolve() != path:
        raise SystemExit(f"refusing linked package source: {path.name}")


def skill_folders(packs) -> list:
    sources = [REPO / "skills"] + [REPO / "packs" / name / "skills" for name in packs]
    found = []
    for source in sources:
        require_source(source)
        if not source.is_dir():
            raise SystemExit(f"No such pack: {source.parent.name}")
        found += [p for p in sorted(source.iterdir()) if (p / "SKILL.md").is_file()]
    return found


def link_problems(members, source_ref: str) -> list:
    """List Markdown links in a ZIP that a reader could not follow."""
    names = {name for name, _ in members}
    problems = []
    for name, content in members:
        if not name.endswith(".md"):
            continue
        fence = None
        for line in content.decode("utf-8").splitlines():
            marker = FENCE.match(line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                    fence = None
                continue
            if fence:
                continue
            for found in LINKS.findall(re.sub(r"`[^`]*`", "", line)):
                link = found[0] or found[1]
                parts = urlsplit(link)
                source = SOURCE_LINK.match(link)
                if source:
                    if source[1] != source_ref:
                        problems.append(f"{name} links to {source[1]} instead of {source_ref}: {link}")
                    elif not (REPO / unquote(source[2])).exists():
                        problems.append(f"{name} links to a missing repository file: {link}")
                elif not (parts.scheme or parts.netloc) and parts.path:
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parts.path)))
                    if target not in names and not any(member.startswith(target + "/") for member in names):
                        problems.append(f"{name} links to a file missing from the ZIP: {link}")
    return problems


def bundled_markdown(source: Path, name: str, bundled: dict, source_ref: str) -> bytes:
    """Keep links to bundled files local and point other parent links at the public source."""
    folder = "/" + posixpath.dirname(name)
    links = {path: posixpath.relpath("/" + installed, folder) for path, installed in bundled.items()}
    markdown = portable_markdown(source, REPO, links, source_ref=source_ref)
    # Leave the bytes alone when no link had to move.
    return source.read_bytes() if markdown == source.read_text(encoding="utf-8") else markdown.encode("utf-8")


def write_member(archive: zipfile.ZipFile, name: str, content: bytes) -> None:
    # Avoid embedding the build time, checkout timestamps or the host filesystem's mode.
    entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    entry.create_system = 3
    entry.external_attr = 0o100644 << 16
    archive.writestr(entry, content, compress_type=zipfile.ZIP_DEFLATED)


def package(skill: Path, out: Path, *, source_ref: str = "main") -> Path:
    require_source(skill)
    paths = sorted(skill.rglob("*"))
    examples = list(example_files(skill))
    guides = []
    if skill == REPO / "packs" / "exec-ops" / "skills" / "decision-brief":
        guides = [REPO / "docs" / "guides" / name for name in ("codex-claude-code.md", "chat-assistants.md")]
    notices = [REPO / name for name in ("LICENSE-docs.md", "LICENSE")]
    for path in [*paths, *(source for source, _ in examples), *guides, *notices]:
        require_source(path)

    bundled = {path.resolve(): path.relative_to(skill).as_posix() for path in paths}
    bundled.update((path.resolve(), name) for path, name in examples)
    bundled.update((guide.resolve(), f"guides/{guide.name}") for guide in guides)
    members = []
    for path in paths:
        name = path.relative_to(skill).as_posix()
        if path == skill / "README.md":
            content = portable_readme(skill, REPO, source_ref=source_ref).encode("utf-8")
        elif path.suffix == ".md" and path.is_file():
            content = bundled_markdown(path, name, bundled, source_ref)
        elif path.is_file():
            content = path.read_bytes()
        else:
            continue
        members.append((f"{skill.name}/{name}", content))
    for path, name in examples:
        if name in {"example-input.md", "example-output.md"}:
            content = portable_markdown(path, REPO, {}, source_ref=source_ref).encode("utf-8")
        elif path.suffix == ".md":
            content = bundled_markdown(path, name, bundled, source_ref)
        else:
            content = path.read_bytes()
        members.append((f"{skill.name}/{name}", content))
    if guides:
        scenarios = {path.resolve(): f"../scenarios/{path.name}"
                     for path in (skill / "scenarios").glob("*.md")}
        for guide in guides:
            markdown = portable_markdown(guide, REPO, scenarios, source_ref=source_ref)
            members.append((f"{skill.name}/guides/{guide.name}", markdown.encode("utf-8")))
    for notice in notices:
        members.append((f"{skill.name}/{notice.name}", notice.read_bytes()))

    problems = link_problems(members, source_ref)
    if problems:
        raise SystemExit(f"{skill.name}.zip has broken links:\n  " + "\n  ".join(problems))
    target = out / f"{skill.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in members:
            write_member(archive, name, content)
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pack", action="append", default=[], help="also package this pack's skills (repeatable)")
    parser.add_argument("--all-packs", action="store_true")
    parser.add_argument("--out", default="dist/skills", help="folder for the zip files (default: dist/skills)")
    parser.add_argument("--source-commit", help="full Git commit to use for links back to repository files")
    args = parser.parse_args(argv)
    if args.source_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.source_commit):
        parser.error("--source-commit must be a full 40-character Git commit")
    source_ref = args.source_commit.lower() if args.source_commit else "main"
    if args.all_packs:
        require_source(REPO / "packs")
    packs = sorted(p.name for p in (REPO / "packs").iterdir() if (p / "skills").is_dir()) if args.all_packs else args.pack
    skills = skill_folders(dict.fromkeys(packs))
    seen = set()
    for skill in skills:
        if skill.name.casefold() in seen:
            parser.error(f"duplicate skill ZIP name: {skill.name}.zip")
        seen.add(skill.name.casefold())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [package(skill, out, source_ref=source_ref) for skill in skills]
    for path in made:
        print(path)
    print(f"\n{len(made)} skill zip(s) in {out}. See docs/guides/chat-assistants.md for setup.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
