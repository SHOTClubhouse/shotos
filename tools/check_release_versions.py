#!/usr/bin/env python3
"""Check version changes for a committed SHOTos release candidate."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORE = ".claude-plugin/plugin.json"
VERSION = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          encoding="utf-8", check=True, timeout=30).stdout


def read(ref, path):
    return git("show", f"{ref}:{path}")


def version(value):
    if not isinstance(value, str) or not re.fullmatch(VERSION, value):
        raise ValueError(f"expected a stable release version, got {value!r}")
    return tuple(map(int, value.split(".")))


def metadata_version(text, pattern):
    match = re.search(pattern, text, re.MULTILINE)
    return match[1] if match else None


def pack_manifests(ref):
    paths = git("ls-tree", "-r", "-z", "--name-only", ref, "--", "packs").split("\0")
    return {path: json.loads(read(ref, path)) for path in paths
            if re.fullmatch(r"packs/[^/]+/\.claude-plugin/plugin\.json", path)}


def check(previous, candidate):
    old = json.loads(read(previous, CORE))["version"]
    current = json.loads(read(candidate, CORE))["version"]
    errors = []
    if version(current) <= version(old):
        errors.append(f"Core version {current} must advance from {old}.")
    citation = metadata_version(read(candidate, "CITATION.cff"), rf'^version:\s*["\']?({VERSION})["\']?\s*$')
    changelog = metadata_version(read(candidate, "CHANGELOG.md"), rf"^## ({VERSION})(?:\s|$)")
    for label, value in (("CITATION.cff", citation), ("CHANGELOG.md", changelog)):
        if value != current:
            errors.append(f"{label} names {value or 'no version'} but Core names {current}.")

    earlier = pack_manifests(previous)
    later = pack_manifests(candidate)
    changed = set(git("diff", "--name-only", "--no-ext-diff", "--no-renames", "-z",
                      previous, candidate, "--", "packs").split("\0"))
    for path, manifest in sorted(later.items()):
        name = manifest["name"]
        new = version(manifest["version"])
        if path not in earlier:
            continue
        prior = earlier[path]
        old = version(prior["version"])
        prefix = "/".join(path.split("/")[:2]) + "/"
        content_changed = any(item.startswith(prefix) and item != path for item in changed)
        metadata_changed = {k: v for k, v in prior.items() if k != "version"} != {
            k: v for k, v in manifest.items() if k != "version"
        }
        if new < old or ((content_changed or metadata_changed) and new == old):
            errors.append(f"{name} needs a version newer than {prior['version']} for its shipped changes.")
    return errors, len(later)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("previous_tag", help="last stable release, for example v1.7.0")
    parser.add_argument("--candidate", default="HEAD", help="committed release candidate, default HEAD")
    args = parser.parse_args()
    if not re.fullmatch(f"v{VERSION}", args.previous_tag):
        parser.error("previous_tag must be a stable release tag")
    try:
        previous = git("rev-parse", "--verify", "--end-of-options", f"refs/tags/{args.previous_tag}^{{commit}}").strip()
        candidate = git("rev-parse", "--verify", "--end-of-options", f"{args.candidate}^{{commit}}").strip()
        errors, packs = check(previous, candidate)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"Version check could not run: {error}", file=sys.stderr)
        return 2
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Release version and {packs} optional pack versions checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
