#!/usr/bin/env python3
"""review-packet: build or validate a self-contained packet for an independent reviewer.

Control 7 (independent review) and the cross-agent-review skill. The packet
carries the exact text the reviewer may use, so the reviewer needs no access to
the project folder:

    python tools/review_packet.py build spec.json --scope <project folder> --revision <commit or version> --out .work/<task>/packet.json
    python tools/review_packet.py validate .work/<task>/packet.json --scope <project folder>

A spec is a JSON object:

    {"request": "what to review and what to decide",
     "acceptance": ["the agreed check", ...],
     "sources": ["relative/path/inside/the/scope.md", ...],
     "evidence": [{"source": "where it came from", "text": "what it shows"}],
     "limitations": ["what the reviewer cannot see", ...]}

`build` refuses a source outside the scope folder, a source reached through a
link, a source whose name or text looks like a secret, a missing revision and a
packet over 128 KiB. `validate` checks a packet again before use, refuses it if
the scope folder name or any source revision does not match, and prints its
SHA-256 for the review record.

The secret check is a safety net based on file names and a simple text
pattern. It is not proof that nothing sensitive remains: the owner still
decides what the reviewer may see. Nothing is sent anywhere. Standard library
only, Python 3.9 or later.

Exit codes: 0 built or valid, 2 refused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

MAX_BYTES = 128 * 1024
SECRET_NAME = re.compile(r"(^|[\\/])(\.env.*|.*\.(pem|key|pfx|p12)|id_rsa.*|.*credential.*|.*secret.*)$", re.I)
SECRET_TEXT = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|secret|token|password)\s*[:=]\s*\S{8,}",
                         re.I)
FIELDS = ("schema", "scope", "revision", "request", "acceptance", "sources", "evidence", "limitations")
REPARSE_POINT = 0x400  # a Windows junction or symbolic link


class Refused(Exception):
    pass


def is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(os.lstat(path), "st_file_attributes", 0) & REPARSE_POINT)


def text(value, limit: int, what: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Refused(f"{what} must be text of 1 to {limit} characters")
    return value


def items(value, what: str, required: bool) -> list:
    if value is None and not required:
        return []
    if not isinstance(value, list) or (required and not value):
        raise Refused(f"{what} must be a{' non-empty' if required else ''} list")
    return value


def read_source(scope: Path, rel: str) -> str:
    if not isinstance(rel, str) or not rel.strip():
        raise Refused("each source must be a relative path")
    parts = Path(rel).parts
    if Path(rel).is_absolute() or Path(rel).drive or ".." in parts:
        raise Refused(f"source must be a relative path inside the scope: {rel}")
    current = scope
    for part in parts:
        current = current / part
        if os.path.lexists(current) and is_link(current):
            raise Refused(f"source passes through a link: {rel}")
    if not current.is_file():
        raise Refused(f"source not found: {rel}")
    if SECRET_NAME.search(rel):
        raise Refused(f"source name looks like a secret: {rel}")
    try:
        body = current.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Refused(f"source is not UTF-8 text: {rel}") from None
    if SECRET_TEXT.search(body):
        raise Refused(f"source looks like it contains a secret: {rel}")
    return body


def build(spec: dict, scope: Path, revision: str) -> dict:
    if not isinstance(spec, dict):
        raise Refused("the spec must be a JSON object")
    revision = text(revision, 128, "revision")
    evidence = []
    for item in items(spec.get("evidence"), "evidence", False):
        if not isinstance(item, dict):
            raise Refused("each evidence item needs a source and a text")
        evidence.append({"source": text(item.get("source"), 4096, "evidence source"),
                         "text": text(item.get("text"), 16000, "evidence text")})
    return {
        "schema": 1,
        "scope": scope.name,
        "revision": revision,
        "request": text(spec.get("request"), 8192, "request"),
        "acceptance": [text(a, 8192, "acceptance item") for a in items(spec.get("acceptance"), "acceptance", True)],
        "sources": [{"path": rel, "revision": revision, "text": text(read_source(scope, rel), 60000, str(rel))}
                    for rel in items(spec.get("sources"), "sources", True)],
        "evidence": evidence,
        "limitations": [text(x, 8192, "limitation") for x in items(spec.get("limitations"), "limitations", False)],
    }


def encode(packet: dict) -> bytes:
    data = json.dumps(packet, indent=1, ensure_ascii=False).encode("utf-8")
    if len(data) > MAX_BYTES:
        raise Refused(f"packet is {len(data)} bytes; the limit is {MAX_BYTES}")
    return data


def validate(packet, scope: Path) -> str:
    """The packet's SHA-256, or Refused with the reason it cannot be used with this scope."""
    if not isinstance(packet, dict) or set(packet) != set(FIELDS):
        raise Refused("packet has missing or unexpected fields")
    if packet["schema"] != 1:
        raise Refused("unsupported packet schema")
    if packet["scope"] != scope.name:
        raise Refused(f"packet was built for {packet['scope']}, not {scope.name}")
    text(packet["revision"], 128, "revision")
    for source in items(packet["sources"], "sources", True):
        if not isinstance(source, dict) or source.get("revision") != packet["revision"]:
            raise Refused(f"source {source.get('path') if isinstance(source, dict) else source} was read at a "
                          "different revision")
        if SECRET_TEXT.search(str(source.get("text", ""))):
            raise Refused(f"source {source.get('path')} looks like it contains a secret")
    return hashlib.sha256(encode(packet)).hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("build", "validate"))
    parser.add_argument("file", type=Path, help="the spec (build) or the packet (validate)")
    parser.add_argument("--scope", type=Path, required=True, help="the project folder the sources come from")
    parser.add_argument("--revision", help="the exact commit or version being reviewed (build)")
    parser.add_argument("--out", type=Path, help="write the packet here (default: standard output)")
    args = parser.parse_args(argv)
    try:
        scope = args.scope.resolve(strict=True)
        if not scope.is_dir():
            raise Refused("--scope must be a folder")
        raw = json.loads(args.file.read_text(encoding="utf-8"))
        if args.action == "validate":
            print(json.dumps({"status": "valid", "sha256": validate(raw, scope)}))
            return 0
        if not args.revision:
            raise Refused("--revision is required: name the exact commit or version reviewed")
        data = encode(build(raw, scope, args.revision))
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_bytes(data)
        else:
            sys.stdout.write(data.decode("utf-8") + "\n")
        print(json.dumps({"status": "built", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}),
              file=sys.stderr)
        return 0
    except (Refused, OSError, ValueError) as error:
        print(json.dumps({"status": "refused", "reason": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
