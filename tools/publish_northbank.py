#!/usr/bin/env python3
"""Publish the fictional Northbank demo site to the gh-pages branch.

Examples:
  python tools/publish_northbank.py            build the site and say what would be pushed
  python tools/publish_northbank.py --publish  push it to gh-pages on origin

The site is built the way the old Pages workflow built it: the files in
examples/northbank-club/site at the current commit, plus release.json naming
that commit, so anyone can compare the live marker with the source. An empty
.nojekyll file tells GitHub Pages to serve the files as they are.

The build is saved in .work/northbank/site so you can open it first. Publishing
needs HEAD to be the same commit as origin/main. GitHub Pages must be set to
deploy from the gh-pages branch: see MAINTAINERS.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from launch import launchable  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SITE = "examples/northbank-club/site"
BRANCH = "gh-pages"
BUILD = REPO / ".work" / "northbank" / "site"


class Stopped(Exception):
    pass


def git(*args, repo: Path = REPO, input=None, env=None, check=True) -> str:
    # Bytes in and out, so Windows cannot turn the newlines Git reads into CRLF.
    done = subprocess.run(launchable(["git", "-C", str(repo), *args]), capture_output=True,
                          input=None if input is None else input.encode("utf-8"), env=env, timeout=120)
    if check and done.returncode != 0:
        raise Stopped(f"git {args[0]} failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout.decode("utf-8").strip()


def site_files(commit: str, repo: Path = REPO) -> list:
    """(mode, blob, path inside the site) for each file in the site folder at this commit."""
    listing = git("ls-tree", "-r", "-z", "--full-tree", commit, "--", SITE, repo=repo)
    files = []
    for row in filter(None, listing.split("\0")):
        meta, path = row.split("\t", 1)
        mode, kind, blob = meta.split()
        if kind == "blob":
            files.append((mode, blob, path[len(SITE) + 1:]))
    if not any(path == "index.html" for _, _, path in files):
        raise Stopped(f"{SITE} has no index.html at {commit[:12]}")
    return files


def marker(commit: str) -> str:
    # The same marker the Pages workflow wrote, so earlier read-backs still compare.
    return json.dumps({"commit": commit}, separators=(",", ":")) + "\n"


def build(commit: str, out: Path = BUILD, repo: Path = REPO) -> list:
    """Write the site to a folder to look at. Returns the published paths."""
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    paths = []
    for _, blob, path in site_files(commit, repo):
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.run(launchable(["git", "-C", str(repo), "cat-file", "blob", blob]),
                                          capture_output=True, check=True, timeout=60).stdout)
        paths.append(path)
    (out / "release.json").write_text(marker(commit), encoding="utf-8", newline="\n")
    (out / ".nojekyll").write_bytes(b"")
    return sorted(paths + ["release.json", ".nojekyll"])


def site_commit(commit: str, parent, repo: Path = REPO) -> tuple:
    """Make the gh-pages commit with Git plumbing, without touching the checkout. Returns (commit, tree)."""
    index = Path(git("rev-parse", "--git-path", "northbank-index", repo=repo))
    if not index.is_absolute():
        index = repo / index
    env = {**os.environ, "GIT_INDEX_FILE": str(index)}
    try:
        git("read-tree", "--empty", repo=repo, env=env)
        entries = [(mode, blob, path) for mode, blob, path in site_files(commit, repo)]
        entries.append(("100644", git("hash-object", "-w", "--stdin", repo=repo, input=marker(commit)),
                        "release.json"))
        entries.append(("100644", git("hash-object", "-w", "--stdin", repo=repo, input=""), ".nojekyll"))
        info = "".join(f"{mode} {blob}\t{path}\n" for mode, blob, path in entries)
        git("update-index", "--index-info", repo=repo, env=env, input=info)
        tree = git("write-tree", repo=repo, env=env)
    finally:
        if index.exists():
            index.unlink()
    if parent and git("rev-parse", f"{parent}^{{tree}}", repo=repo) == tree:
        return parent, tree
    args = ["commit-tree", tree, "-m", f"Publish the Northbank demo from {commit}"]
    if parent:
        args[2:2] = ["-p", parent]
    return git(*args, repo=repo), tree


def main(argv=None, repo: Path = REPO) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--publish", action="store_true", help=f"push to {BRANCH} on origin (default: dry run)")
    args = parser.parse_args(argv)
    try:
        head = git("rev-parse", "HEAD", repo=repo)
        paths = build(head, repo / ".work" / "northbank" / "site", repo)
        print(f"Built {len(paths)} files from {SITE} at {head[:12]} in .work/northbank/site:")
        for path in paths:
            print(f"  {path}")
        if not args.publish:
            main_commit = git("rev-parse", "--verify", "--quiet", "origin/main", repo=repo, check=False)
            if main_commit != head:
                print("Note: HEAD is not origin/main. Publishing will refuse until it is.")
            print(f"\nDry run: nothing was pushed. Run again with --publish to update {BRANCH}.")
            return 0
        git("fetch", "-q", "origin", repo=repo)
        if git("rev-parse", "origin/main", repo=repo, check=False) != head:
            raise Stopped("publish from main as it is on GitHub: HEAD is not the same commit as origin/main")
        remote = git("ls-remote", "origin", f"refs/heads/{BRANCH}", repo=repo).split()
        parent = remote[0] if remote else None
        if parent:
            git("fetch", "-q", "origin", f"refs/heads/{BRANCH}", repo=repo)
        commit, _ = site_commit(head, parent, repo)
        if commit == parent:
            print(f"\n{BRANCH} already holds this site. Nothing was pushed.")
            return 0
        git("push", "origin", f"{commit}:refs/heads/{BRANCH}", repo=repo)
        print(f"\nPushed {commit[:12]} to {BRANCH}. GitHub Pages serves it once its source is the {BRANCH} branch.")
        print("Check the public release.json names "
              f"{head} before you record the read-back.")
    except (Stopped, OSError, subprocess.SubprocessError) as error:
        print(f"Publishing stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
