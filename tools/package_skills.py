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
import re
import sys
import zipfile
from pathlib import Path

from skill_resources import example_files, portable_markdown, portable_readme

REPO = Path(__file__).resolve().parents[1]


def skill_folders(packs) -> list:
    sources = [REPO / "skills"] + [REPO / "packs" / name / "skills" for name in packs]
    found = []
    for source in sources:
        if not source.is_dir():
            raise SystemExit(f"No such pack: {source.parent.name}")
        found += [p for p in sorted(source.iterdir()) if (p / "SKILL.md").is_file()]
    return found


def package(skill: Path, out: Path, *, source_ref: str = "main") -> Path:
    target = out / f"{skill.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill.rglob("*")):
            if path == skill / "README.md":
                archive.writestr(f"{skill.name}/README.md", portable_readme(skill, REPO, source_ref=source_ref))
            elif path.is_file():
                archive.write(path, Path(skill.name) / path.relative_to(skill))
        for path, name in example_files(skill):
            archive.write(path, Path(skill.name) / name)
        if skill == REPO / "packs" / "exec-ops" / "skills" / "decision-brief":
            scenarios = {path.resolve(): f"../scenarios/{path.name}"
                         for path in (skill / "scenarios").glob("retail-trial-*.md")}
            for name in ("codex-claude-code.md", "chat-assistants.md"):
                guide = REPO / "docs" / "guides" / name
                archive.writestr(f"{skill.name}/guides/{name}", portable_markdown(guide, REPO, scenarios, source_ref=source_ref))
        for notice in ("LICENSE-docs.md", "LICENSE"):
            archive.write(REPO / notice, Path(skill.name) / notice)
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
    packs = sorted(p.name for p in (REPO / "packs").iterdir() if (p / "skills").is_dir()) if args.all_packs else args.pack
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [package(skill, out, source_ref=source_ref) for skill in skill_folders(packs)]
    for path in made:
        print(path)
    print(f"\n{len(made)} skill zip(s) in {out}. See docs/guides/chat-assistants.md for setup.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
