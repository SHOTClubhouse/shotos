#!/usr/bin/env python3
"""Read back a published SHOTos release against a checkout and the built skill ZIPs."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from skill_resources import PUBLIC_REPO

REPO = Path(__file__).resolve().parents[1]
SLUG = PUBLIC_REPO.removeprefix("https://github.com/")


def fetch(url, expected_size=None):
    request = Request(url, headers={"User-Agent": "SHOTos-release-readback"})
    with urlopen(request, timeout=30) as response:
        if expected_size is None:
            return response.read()
        content = response.read(expected_size + 1)
    if len(content) != expected_size:
        raise ValueError(f"download size differs: {url}")
    return content


def tag_commit(tag):
    ref = f"refs/tags/{tag}"
    run = subprocess.run(["git", "ls-remote", PUBLIC_REPO, ref, ref + "^{}"],
                         capture_output=True, text=True, check=True, timeout=30)
    refs = {name: commit for commit, name in (line.split() for line in run.stdout.splitlines())}
    return refs.get(ref + "^{}", refs.get(ref))


def check_inventory(label, actual, expected):
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError(f"{label} inventory differs. Missing: {', '.join(missing) or 'none'}. "
                         f"Extra: {', '.join(extra) or 'none'}.")


def verify(tag, source, assets):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=source, capture_output=True,
                          text=True, check=True, timeout=10).stdout.strip()
    if tag_commit(tag) != head:
        raise ValueError(f"public tag {tag} does not match checkout {head}")

    folders = [*source.glob("skills/*/SKILL.md"), *source.glob("packs/*/skills/*/SKILL.md")]
    expected = {f"{path.parent.name}.zip" for path in folders}
    if not expected or len(expected) != len(folders):
        raise ValueError("checkout has no skill inventory or has duplicate skill names")
    local = {path.name for path in assets.glob("*.zip") if path.is_file()}
    check_inventory("local ZIP", local, expected)

    data = json.loads(fetch(f"https://api.github.com/repos/{SLUG}/releases/tags/{quote(tag)}"))
    if data.get("draft") or data.get("tag_name") != tag:
        raise ValueError(f"GitHub did not return a published release for {tag}")
    published = {asset["name"]: asset for asset in data["assets"] if asset["name"].endswith(".zip")}
    check_inventory("published ZIP", published.keys(), expected)
    base = f"{PUBLIC_REPO}/releases/download/{quote(tag)}/"

    def verify_zip(name):
        content = (assets / name).read_bytes()
        asset = published[name]
        if asset.get("state") != "uploaded" or asset["size"] != len(content):
            raise ValueError(f"GitHub metadata differs: {name}")
        checksum = hashlib.sha256(content).hexdigest()
        if asset.get("digest") and asset["digest"] != f"sha256:{checksum}":
            raise ValueError(f"GitHub SHA-256 differs: {name}")
        if hashlib.sha256(fetch(base + quote(name), len(content))).hexdigest() != checksum:
            raise ValueError(f"public download SHA-256 differs: {name}")

    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(verify_zip, sorted(expected)))

    guides = sorted((source / "docs/guides").glob("*.md"))
    required = {"codex-claude-code.md", "chat-assistants.md"}
    if not required <= {path.name for path in guides}:
        raise ValueError("checkout is missing one or both setup guides")
    raw = f"https://raw.githubusercontent.com/{SLUG}/{quote(tag)}/"
    for path in guides:
        relative = path.relative_to(source).as_posix()
        content = path.read_bytes()
        if fetch(raw + quote(relative), len(content)) != content:
            raise ValueError(f"tagged guide differs: {relative}")
    return head, len(expected), len(guides)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="the published tag, for example v1.7.0")
    parser.add_argument("--assets", type=Path, required=True, help="directory of the ZIPs built for this release")
    parser.add_argument("--source", type=Path, default=REPO, help="clean source checkout at the release tag")
    args = parser.parse_args()
    if not re.fullmatch(r"v\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.+-]+)?", args.tag):
        parser.error("expected a release tag such as v1.7.0")
    try:
        head, assets, guides = verify(args.tag, args.source.resolve(), args.assets.resolve())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"Release verification failed: {error}", file=sys.stderr)
        return 1
    print(f"Verified {args.tag} at {head}: {assets} public ZIPs match by SHA-256 and {guides} guides match the checkout.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
