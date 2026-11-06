#!/usr/bin/env python3
"""Package SHOTos skills as zip files for upload to the Claude app or claude.ai.

The Claude apps take a custom skill as a zip holding the skill folder, with
SKILL.md inside it (Settings, then Capabilities, then Skills, then Upload skill).
Each zip made here is one skill. Upload the ones you want, one at a time.

Examples:
  python tools/package_skills.py                     core skills only
  python tools/package_skills.py --pack exec-ops     core plus one pack
  python tools/package_skills.py --all-packs --out dist/skills
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from skill_resources import example_files

REPO = Path(__file__).resolve().parents[1]


def skill_folders(packs) -> list:
    sources = [REPO / "skills"] + [REPO / "packs" / name / "skills" for name in packs]
    found = []
    for source in sources:
        if not source.is_dir():
            raise SystemExit(f"No such pack: {source.parent.name}")
        found += [p for p in sorted(source.iterdir()) if (p / "SKILL.md").is_file()]
    return found


def package(skill: Path, out: Path) -> Path:
    target = out / f"{skill.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill.rglob("*")):
            if path.is_file():
                archive.write(path, Path(skill.name) / path.relative_to(skill))
        for path, name in example_files(skill):
            archive.write(path, Path(skill.name) / name)
        for notice in ("LICENSE-docs.md", "LICENSE"):
            archive.write(REPO / notice, Path(skill.name) / notice)
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pack", action="append", default=[], help="also package this pack's skills (repeatable)")
    parser.add_argument("--all-packs", action="store_true")
    parser.add_argument("--out", default="dist/skills", help="folder for the zip files (default: dist/skills)")
    args = parser.parse_args(argv)
    packs = sorted(p.name for p in (REPO / "packs").iterdir() if (p / "skills").is_dir()) if args.all_packs else args.pack
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [package(skill, out) for skill in skill_folders(packs)]
    for path in made:
        print(path)
    print(f"\n{len(made)} skill zip(s) in {out}. Upload each in the Claude app under Settings, Capabilities, Skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
