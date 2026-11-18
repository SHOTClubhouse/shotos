#!/usr/bin/env python3
"""Publish the built SHOTos website to the gh-pages branch for GitHub Pages.

Examples:
  python tools/publish_site.py            build and check the site, then say what would be pushed
  python tools/publish_site.py --publish  push it to gh-pages on origin

The site is built and checked by tools/build_site.py: links, uncommitted sources
and the private denylist named by SHOTOS_DENYLIST. Only a build that passes all
three can be published. The gh-pages branch holds the built files and nothing
else, so GitHub Pages never serves a source file. An empty .nojekyll file tells
Pages to serve the files as they are.

The gh-pages commit is made with Git plumbing, so the checkout and its branch are
never touched. Publishing needs HEAD to be the same commit as origin/main.

GitHub Pages runs its own managed pages-build-deployment job for each push to a
Pages branch. GitHub Pages must be set to deploy from the gh-pages branch: see
MAINTAINERS.md.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site  # noqa: E402
import leak_scan  # noqa: E402
from launch import launchable  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
BRANCH = "gh-pages"
PAGES_FILES = {".nojekyll": b""}


class Stopped(Exception):
    pass


def git(*args, repo: Path = REPO, input=None, env=None, check=True) -> str:
    # Bytes in and out, so Windows cannot turn the newlines Git reads into CRLF.
    data = input.encode("utf-8") if isinstance(input, str) else input
    done = subprocess.run(launchable(["git", "-C", str(repo), *args]), capture_output=True, input=data,
                          env=env, timeout=120)
    if check and done.returncode != 0:
        raise Stopped(f"git {args[0]} failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout.decode("utf-8").strip()


def site_commit(files: dict, source: str, parent, repo: Path = REPO) -> tuple:
    """The gh-pages commit holding exactly `files` (site path -> bytes). Returns (commit, tree)."""
    index = Path(git("rev-parse", "--git-path", "site-index", repo=repo))
    if not index.is_absolute():
        index = repo / index
    env = {**os.environ, "GIT_INDEX_FILE": str(index)}
    try:
        git("read-tree", "--empty", repo=repo, env=env)
        rows = []
        for path, data in sorted({**files, **PAGES_FILES}.items()):
            rows.append(f"100644 {git('hash-object', '-w', '--stdin', repo=repo, input=data)}\t{path}\n")
        git("update-index", "--index-info", repo=repo, env=env, input="".join(rows))
        tree = git("write-tree", repo=repo, env=env)
    finally:
        if index.exists():
            index.unlink()
    if parent and git("rev-parse", f"{parent}^{{tree}}", repo=repo) == tree:
        return parent, tree
    args = ["commit-tree", tree, "-m", f"Publish the SHOTos site from {source}"]
    if parent:
        args[2:2] = ["-p", parent]
    return git(*args, repo=repo), tree


def checked_build(repo: Path, denylist) -> build_site.Site:
    """Build the site and refuse anything build_site.py would not call fit to publish."""
    try:
        site = build_site.build(repo, repo / ".work" / "site")
    except build_site.BuildError as error:
        raise Stopped(f"the site did not build: {error}")
    if not site.clean:
        raise Stopped("the site sources have uncommitted changes")
    path = leak_scan.denylist_path(denylist)
    if path is None:
        raise Stopped("no denylist, so the output cannot be scanned. Set SHOTOS_DENYLIST")
    hits = build_site.scan(site, path)
    if hits:
        raise Stopped("private terms in the output:\n  " + "\n  ".join(hits))
    return site


def main(argv=None, repo: Path = REPO) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--publish", action="store_true", help=f"push to {BRANCH} on origin (default: dry run)")
    parser.add_argument("--denylist", help="denylist file (default: the SHOTOS_DENYLIST environment variable)")
    args = parser.parse_args(argv)
    try:
        site = checked_build(repo, args.denylist)
        head = site.commit
        print(f"Built and checked {len(site.files)} files from {head[:12]} in .work/site.")
        if not args.publish:
            if git("rev-parse", "--verify", "--quiet", "origin/main", repo=repo, check=False) != head:
                print("Note: HEAD is not origin/main. Publishing will refuse until it is.")
            print(f"Dry run: nothing was pushed. Run again with --publish to update {BRANCH}.")
            return 0
        git("fetch", "-q", "origin", repo=repo)
        if git("rev-parse", "origin/main", repo=repo, check=False) != head:
            raise Stopped("publish from main as it is on GitHub: HEAD is not the same commit as origin/main")
        remote = git("ls-remote", "origin", f"refs/heads/{BRANCH}", repo=repo).split()
        parent = remote[0] if remote else None
        if parent:
            git("fetch", "-q", "origin", f"refs/heads/{BRANCH}", repo=repo)
        commit, _ = site_commit(site.files, head, parent, repo)
        if commit == parent:
            print(f"{BRANCH} already holds this site. Nothing was pushed.")
            return 0
        git("push", "origin", f"{commit}:refs/heads/{BRANCH}", repo=repo)
        print(f"Pushed {commit[:12]} to {BRANCH}. GitHub Pages serves it once its source is the {BRANCH} branch.")
        print(f"Check the public release.json names {head} before you record the read-back.")
    except (Stopped, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Publishing stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
