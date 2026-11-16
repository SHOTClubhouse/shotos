#!/usr/bin/env python3
"""Check that no private term from a denylist appears in the repository.

The denylist is kept outside the repository. Its path comes from --denylist or
the SHOTOS_DENYLIST environment variable. Each line is one entry:

    # a comment
    Term            a case-sensitive whole word or phrase
    i:term          a case-insensitive whole word or phrase
    path:text       text that must never appear anywhere, such as a folder path

The scan reads every tracked text file, every tracked file name and, with
--history, every file version and commit message in a range of commits.
Reports name the file, the line and the denylist line number. They never
print the term or the matching text.

A deliberate public use can be listed in tools/leak-allowlist.txt as a file
path and a denylist line number, for example `MAINTAINERS.md 12`. The
allowlist never names a term.

Exit codes: 0 no hits, 1 hits found, 2 the scan could not run.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ALLOWLIST = "tools/leak-allowlist.txt"


@dataclass(frozen=True)
class Entry:
    line: int
    kind: str  # "word", "iword" or "path"
    text: str

    def found(self, text: str, slashed: str = None, lowered: str = None) -> bool:
        if self.kind == "path":
            return self.text in text or _slashes(self.text) in (slashed or _slashes(text))
        # A plain substring test first: much faster than the regex on text that cannot match.
        if self.kind == "word" and self.text not in text:
            return False
        if self.kind == "iword" and self.text.lower() not in (lowered or text.lower()):
            return False
        return bool(self.pattern.search(text))

    @cached_property
    def pattern(self):
        flags = re.IGNORECASE if self.kind == "iword" else 0
        return re.compile(rf"(?<!\w){re.escape(self.text)}(?!\w)", flags)


@dataclass(frozen=True)
class Hit:
    path: str
    line: int
    entry: int
    commit: str = ""
    where: str = "file"  # "file", "name" or "message"

    def describe(self) -> str:
        prefix = f"commit {self.commit[:12]} " if self.commit else ""
        if self.where == "name":
            return f"{prefix}{self.path} (file name): denylist line {self.entry}"
        if self.where == "message":
            return f"{prefix}message line {self.line}: denylist line {self.entry}"
        return f"{prefix}{self.path}:{self.line}: denylist line {self.entry}"


def _slashes(text: str) -> str:
    # Match a path however it is written: C:\x, C:/x or the JSON-escaped C:\\x.
    return text.replace("\\\\", "/").replace("\\", "/")


def denylist_path(explicit=None):
    """The denylist to use, or None when none is configured or the file is missing."""
    value = explicit or os.environ.get("SHOTOS_DENYLIST", "")
    path = Path(value) if value else None
    return path if path and path.is_file() else None


def load_denylist(path: Path) -> list:
    entries = []
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        if text.startswith("i:"):
            kind, text = "iword", text[2:].strip()
        elif text.startswith("path:"):
            kind, text = "path", text[5:].strip()
        else:
            kind = "word"
        if text:
            entries.append(Entry(number, kind, text))
    if not entries:
        raise ValueError("the denylist has no entries")
    return entries


def load_allowlist(path: Path) -> set:
    """Read `path denylist-line` pairs. Anything else is an error, so a term cannot hide here."""
    allowed = set()
    if not path.is_file():
        return allowed
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        match = re.fullmatch(r"(\S+)\s+([1-9][0-9]*)", text)
        if not match:
            raise ValueError(f"{path.name} line {number} must be a file path and a denylist line number")
        allowed.add((match[1], int(match[2])))
    return allowed


def text_hits(text: str, entries) -> list:
    """(line number, denylist line) for each match, reading only lines that can match."""
    hits = []
    slashed, lowered = _slashes(text), text.lower()
    candidates = [entry for entry in entries if entry.found(text, slashed, lowered)]
    if not candidates:
        return hits
    for number, line in enumerate(text.splitlines(), 1):
        hits += [(number, entry.line) for entry in candidates if entry.found(line)]
    return hits


def redact(text: str, entries) -> str:
    """Replace any line that matches the denylist, for text that will be shown or saved."""
    lines = []
    for line in text.splitlines():
        matched = [entry.line for entry in entries if entry.found(line)]
        lines.append(f"[withheld: matches denylist line {matched[0]}]" if matched else line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def decode(content: bytes):
    if b"\0" in content[:8192]:
        return None
    return content.decode("utf-8", errors="replace")


def git(repo: Path, *args, input=None) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], input=input, capture_output=True,
                          check=True, timeout=120).stdout


def scan_tree(repo: Path, entries) -> tuple:
    """Scan the checked-out copy of every tracked file. Returns hits and the binary file count."""
    hits, binary = [], 0
    for path in git(repo, "ls-files", "-z").decode("utf-8").split("\0"):
        if not path:
            continue
        hits += [Hit(path, 0, entry.line, where="name") for entry in entries if entry.found(path)]
        file = repo / path
        if not file.is_file():
            continue
        text = decode(file.read_bytes())
        if text is None:
            binary += 1
            continue
        hits += [Hit(path, line, entry) for line, entry in text_hits(text, entries)]
    return hits, binary


def scan_history(repo: Path, revisions, entries) -> list:
    """Scan every file version and commit message added by the commits in `revisions`."""
    commits = git(repo, "rev-list", *revisions).decode().split()
    hits, blobs = [], {}
    for commit in commits:
        changes = git(repo, "diff-tree", "-r", "-z", "-m", "--root", "--no-commit-id", "--no-renames",
                      "--diff-filter=AM", commit).decode("utf-8").split("\0")
        for meta, path in zip(changes[0::2], changes[1::2]):
            _, mode, _, blob, _ = meta.split()
            if mode != "160000":  # a submodule commit is not a file version
                blobs.setdefault(blob, (commit, path))
        message = git(repo, "log", "-1", "--format=%B", commit).decode("utf-8", errors="replace")
        hits += [Hit("", line, entry, commit, "message") for line, entry in text_hits(message, entries)]
    names = {}
    for commit, path in blobs.values():
        names.setdefault(path, commit)
    for path, commit in names.items():
        hits += [Hit(path, 0, entry.line, commit, "name") for entry in entries if entry.found(path)]
    if blobs:
        batch = git(repo, "cat-file", "--batch", input="".join(f"{blob}\n" for blob in blobs).encode())
        offset = 0
        for blob, (commit, path) in blobs.items():
            header_end = batch.index(b"\n", offset)
            size = int(batch[offset:header_end].split()[2])
            content = batch[header_end + 1:header_end + 1 + size]
            offset = header_end + 1 + size + 1
            text = decode(content)
            if text is not None:
                hits += [Hit(path, line, entry, commit) for line, entry in text_hits(text, entries)]
    return hits


def scan(repo: Path, entries, allowed=frozenset(), history=()) -> dict:
    hits, binary = scan_tree(repo, entries)
    for revisions in history:
        hits += scan_history(repo, revisions, entries)
    kept = [hit for hit in hits if hit.where == "message" or (hit.path, hit.entry) not in allowed]
    seen, unique = set(), []
    for hit in kept:
        key = hit.describe()
        if key not in seen:
            seen.add(key)
            unique.append(hit)
    used = {(hit.path, hit.entry) for hit in hits}
    return {"hits": unique, "binary": binary, "allowed": len(hits) - len(kept),
            "stale": sorted(allowed - used)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--denylist", help="denylist file (default: the SHOTOS_DENYLIST environment variable)")
    parser.add_argument("--allowlist", help=f"allowlist file (default: {ALLOWLIST})")
    parser.add_argument("--repo", type=Path, default=REPO, help="repository to scan")
    parser.add_argument("--history", action="append", default=[], metavar="RANGE",
                        help="also scan the commits in this range, for example origin/main..HEAD")
    args = parser.parse_args(argv)
    denylist = denylist_path(args.denylist)
    if denylist is None:
        print("Leak scan could not run: no denylist. Set SHOTOS_DENYLIST to the private denylist file.",
              file=sys.stderr)
        return 2
    try:
        entries = load_denylist(denylist)
        allowed = load_allowlist(Path(args.allowlist) if args.allowlist else args.repo / ALLOWLIST)
        result = scan(args.repo, entries, allowed, [r.split() for r in args.history])
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Leak scan could not run: {error}", file=sys.stderr)
        return 2
    for hit in result["hits"]:
        print(hit.describe())
    for path, entry in result["stale"]:
        print(f"note: allowlist entry {path} {entry} no longer matches anything")
    print(f"{len(result['hits'])} hit(s). {result['allowed']} allowed by the allowlist. "
          f"{result['binary']} binary file(s) not read.")
    return 1 if result["hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
