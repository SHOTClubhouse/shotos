#!/usr/bin/env python3
"""drift-check: a read-only report of how an installed copy differs from the shared repository.

Steps 2 and 7 of the config-as-code skill, the two comparisons that change nothing:

    python drift_check.py --repo <shared folder> --installed <installed folder>
    python drift_check.py --repo team-config --installed ~/.claude --map rules=rules --map skills=skills
    python drift_check.py --repo team-config --installed ~/.claude --ignore "*.local.json" --json

Each file is reported as one of three kinds:

    ONLY IN REPO       the repository has it, the installed copy does not
    ONLY IN INSTALLED  the installed copy has it, the repository does not
    DIFFERS            both have it and the contents differ

Contents are compared by SHA-256, so a file that was touched but not changed is
not drift. "repo newer" or "installed newer" beside a difference is a hint from
file times. It does not say which side is right.

Use --map REPO_SUB=INSTALLED_SUB for each folder the setup manages, so the check
covers that list and not a whole home folder. Anything not mapped is not checked.
Without --map, the whole of --repo is compared with the whole of --installed.

Logs, caches and byte-code are ignored by default, at any depth. Add --ignore
(shell-style, on the forward-slash path) for secrets and machine-only files.
Links and junctions are not followed. Nothing is written, copied or deleted.
Standard library only, Python 3.9 or later.

Exit codes: 0 no drift, 1 drift found, 2 a folder is missing or a file could not be read.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import sys
from pathlib import Path

DEFAULT_IGNORE = (".git/*", "__pycache__/*", "*.pyc", "node_modules/*", "logs/*", "*.log", ".DS_Store")
LABELS = {"only-in-repo": "ONLY IN REPO", "only-in-installed": "ONLY IN INSTALLED", "differs": "DIFFERS"}
REPARSE_POINT = 0x400  # a Windows junction or symbolic link


def is_link(path: str) -> bool:
    stat = os.lstat(path)
    return os.path.islink(path) or bool(getattr(stat, "st_file_attributes", 0) & REPARSE_POINT)


def ignored(rel: str, patterns) -> bool:
    return any(fnmatch.fnmatchcase(rel, p) or fnmatch.fnmatchcase(rel, "*/" + p) for p in patterns)


def collect(root: Path, patterns) -> dict:
    """Forward-slash relative path to full path, leaving out ignored files and links."""
    files = {}
    for folder, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not is_link(os.path.join(folder, d)))
        for name in names:
            full = os.path.join(folder, name)
            rel = Path(full).relative_to(root).as_posix()
            if not is_link(full) and not ignored(rel, patterns):
                files[rel] = full
    return files


def digest(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            sha.update(block)
    return sha.hexdigest()


def newer(repo_file: str, installed_file: str) -> str:
    left, right = os.path.getmtime(repo_file), os.path.getmtime(installed_file)
    return "repo newer" if left > right else "installed newer" if right > left else "same time"


def compare(repo: Path, installed: Path, patterns, prefix: str = "") -> list:
    left, right = collect(repo, patterns), collect(installed, patterns)
    findings = []
    for rel in sorted(left.keys() | right.keys()):
        shown = prefix + rel
        if rel not in right:
            findings.append({"kind": "only-in-repo", "path": shown})
        elif rel not in left:
            findings.append({"kind": "only-in-installed", "path": shown})
        elif digest(left[rel]) != digest(right[rel]):
            findings.append({"kind": "differs", "path": shown, "hint": newer(left[rel], right[rel])})
    return findings


def pairs(repo: Path, installed: Path, maps) -> list:
    """(repository folder, installed folder, path prefix) for each comparison."""
    if not maps:
        return [(repo, installed, "")]
    found = []
    for item in maps:
        if "=" not in item:
            raise OSError(f"--map needs REPO_SUB=INSTALLED_SUB, got {item!r}")
        left, right = (part.strip().strip("/\\") for part in item.split("=", 1))
        if not left or not right:
            raise OSError(f"--map needs a folder on both sides, got {item!r}")
        found.append((repo / left, installed / right, left + "/"))
    return found


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, required=True, help="the shared repository folder")
    parser.add_argument("--installed", type=Path, required=True, help="the folder the tool actually reads")
    parser.add_argument("--map", action="append", default=[], metavar="REPO_SUB=INSTALLED_SUB",
                        help="compare one named folder on each side (repeatable)")
    parser.add_argument("--ignore", action="append", default=[], metavar="PATTERN",
                        help="also ignore paths matching this pattern (repeatable)")
    parser.add_argument("--ignore-file", type=Path, help="a file of patterns, one per line, # for comments")
    parser.add_argument("--json", action="store_true", help="print the findings as JSON")
    args = parser.parse_args(argv)

    patterns = [*DEFAULT_IGNORE, *args.ignore]
    findings = []
    try:
        if args.ignore_file:
            lines = args.ignore_file.read_text(encoding="utf-8").splitlines()
            patterns += [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]
        if not args.repo.is_dir() or not args.installed.is_dir():
            raise OSError("--repo and --installed must both be existing folders")
        for left, right, prefix in pairs(args.repo, args.installed, args.map):
            if not left.is_dir() and not right.is_dir():
                raise OSError(f"mapped folder {prefix.rstrip('/')} is missing on both sides")
            if not right.is_dir():
                findings.append({"kind": "only-in-repo", "path": prefix})
            elif not left.is_dir():
                findings.append({"kind": "only-in-installed", "path": prefix})
            else:
                findings += compare(left, right, patterns, prefix)
    except OSError as error:
        print(f"drift_check: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"drift": len(findings), "findings": findings}, indent=2))
    else:
        for finding in findings:
            hint = f" ({finding['hint']})" if "hint" in finding else ""
            print(f"{LABELS[finding['kind']] + ':':<19} {finding['path']}{hint}")
        print(f"{len(findings)} difference(s). Nothing was changed." if findings else "No drift. Nothing was changed.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
