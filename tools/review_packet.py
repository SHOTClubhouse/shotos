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
packet over 128 KiB. `validate` checks a packet again before use and prints its
SHA-256 for the review record. It refuses a packet with a missing or malformed
request, acceptance list, source, evidence item or limitation, a packet whose
scope or any source revision does not match, and a packet whose source text
differs from the file in the scope folder.

The packet identifies its scope by the folder's name and an identity: the
SHA-256 of the compact JSON array ["shotos-review-scope/1", <path>, <root>],
where <path> is the resolved absolute path, case-normalised on Windows, and
<root> is the root commit of the git repository holding the folder, or null
outside one. A packet built from another project, even one with the same
folder name and identical source text, is refused, and so is one built from
a file that has changed since. The scope metadata carries no readable path,
but the hash is not anonymous: someone who guesses the path and root commit
can confirm the guess. Evidence and source text are carried exactly as given,
so authors must not paste private paths into them. Error and refusal messages
show a path under the home folder as ~ and any other absolute path as <path>. The revision itself is a label the builder was given;
validate cannot check it against version control.

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
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 128 * 1024
SECRET_NAME = re.compile(r"(^|[\\/])(\.env.*|.*\.(pem|key|pfx|p12)|id_rsa.*|.*credential.*|.*secret.*)$", re.I)
SECRET_TEXT = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|secret|token|password)\s*[:=]\s*\S{8,}",
                         re.I)
FIELDS = ("schema", "scope", "revision", "request", "acceptance", "sources", "evidence", "limitations")
REPARSE_POINT = 0x400  # a Windows junction or symbolic link
SCHEMA = 3
IDENTITY_FORMAT = "shotos-review-scope/1"


class Refused(Exception):
    pass


ABSOLUTE = r"(?:[A-Za-z]:[\\/]|\\\\|/)"
QUOTED_PATH = re.compile(r"(['\"])(" + ABSOLUTE + r".*?)\1")
BARE_PATH = re.compile(r"(?<![\w.~])" + ABSOLUTE + r"[^\s'\"]*")
WHOLE_PATH = re.compile(ABSOLUTE + r"[^\r\n]*")


def redact(message: str) -> str:
    """The message with a path under the home folder shown as ~ and any other absolute path as <path>.

    A value that is itself one absolute path, spaces and all, is redacted whole, so callers redact each path
    value before putting it into a message; the patterns below are the second safety net for the finished message."""
    message = _home_as_tilde(message)
    if WHOLE_PATH.fullmatch(message):
        return message if message.startswith("~") else "<path>"
    message = QUOTED_PATH.sub(lambda m: m.group(1) + "<path>" + m.group(1), message)
    return BARE_PATH.sub("<path>", message)


def _home_as_tilde(message: str) -> str:
    homes = set()
    for home in {str(Path.home()), str(Path.home().resolve())}:
        homes.update((home, home.replace("\\", "\\\\"), home.replace("\\", "/")))
    for home in sorted(homes, key=len, reverse=True):
        message = re.sub(re.escape(home) + r"(?=[\\/'\"\s]|$)", "~", message, flags=re.I if os.name == "nt" else 0)
    return message


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


def root_commit(scope: Path):
    """The root commit of the git repository holding the scope, or None when it is not in one.

    With more than one root, the lowest hash is used, so the answer does not depend on history order."""
    env = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    try:
        result = subprocess.run(["git", "-C", str(scope), "-c", "core.fsmonitor=false", "rev-list", "--max-parents=0",
                                 "HEAD"], capture_output=True, text=True, env=env, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    roots = sorted(result.stdout.split()) if result.returncode == 0 else []
    return roots[0] if roots else None


def identity(scope: Path) -> dict:
    """What the packet records to tell this scope from any other: its name and a SHA-256 of where it is.

    The hash covers a compact JSON array of a format label, the normalised resolved path and the root commit
    (null outside git), so no two different paths and commits hash the same text. The path itself is not kept."""
    key = [IDENTITY_FORMAT, os.path.normcase(str(scope.resolve())), root_commit(scope)]
    data = json.dumps(key, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return {"name": scope.name, "identity": hashlib.sha256(data).hexdigest()}


def read_source(scope: Path, rel: str) -> str:
    if not isinstance(rel, str) or not rel.strip():
        raise Refused("each source must be a relative path")
    parts = Path(rel).parts
    if Path(rel).is_absolute() or Path(rel).drive or ".." in parts:
        raise Refused(f"source must be a relative path inside the scope: {redact(rel)}")
    current = scope
    for part in parts:
        current = current / part
        if os.path.lexists(current) and is_link(current):
            raise Refused(f"source passes through a link: {redact(rel)}")
    if not current.is_file():
        raise Refused(f"source not found: {redact(rel)}")
    if SECRET_NAME.search(rel):
        raise Refused(f"source name looks like a secret: {redact(rel)}")
    try:
        body = current.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Refused(f"source is not UTF-8 text: {redact(rel)}") from None
    if SECRET_TEXT.search(body):
        raise Refused(f"source looks like it contains a secret: {redact(rel)}")
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
        "schema": SCHEMA,
        "scope": identity(scope),
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
    """The packet's SHA-256, or Refused with the reason it cannot be used with this scope.

    The scope must have the packet's name and identity, the hash of its resolved path and root commit, so a
    packet cannot pass with a folder it was not built from, even one with the same name and identical text.
    Every source is read again and must match the packet's text. The rest must be what build writes."""
    if not isinstance(packet, dict) or set(packet) != set(FIELDS):
        raise Refused("packet has missing or unexpected fields")
    if packet["schema"] != SCHEMA:
        raise Refused("unsupported packet schema: build the packet again")
    recorded, actual = packet["scope"], identity(scope)
    if not isinstance(recorded, dict) or set(recorded) != set(actual):
        raise Refused("the packet's scope needs exactly a name and an identity")
    if recorded["name"] != actual["name"]:
        raise Refused(f"packet was built for {recorded['name']}, not {actual['name']}")
    if recorded["identity"] != actual["identity"]:
        raise Refused(f"packet was built for another {actual['name']}: the folder's path or its repository's "
                      "root commit is not the same")
    sources = items(packet["sources"], "sources", True)
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"path", "revision", "text"}:
            raise Refused("each source needs exactly a path, a revision and a text")
        if source["revision"] != packet["revision"]:
            raise Refused(f"source {redact(str(source['path']))} was read at a different revision")
    spec = {name: packet[name] for name in ("request", "acceptance", "evidence", "limitations")}
    rebuilt = build(dict(spec, sources=[source["path"] for source in sources]), scope, packet["revision"])
    rebuilt["scope"] = recorded
    for source, fresh in zip(sources, rebuilt["sources"]):
        if source["text"] != fresh["text"]:
            raise Refused(f"source {redact(str(source['path']))} does not match the file in {scope.name}: the packet was built "
                          "from another folder, or the file has changed since")
    if rebuilt != packet:
        raise Refused("packet fields are not as build writes them")
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
        print(json.dumps({"status": "refused", "reason": redact(str(error))}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
