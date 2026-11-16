#!/usr/bin/env python3
"""run-contained: run a reviewer command on a review packet, with a time limit, a clean environment and a receipt.

Control 7 (independent review) and the cross-agent-review skill:

    python tools/run_contained.py --packet .work/<task>/packet.json --timeout 300 --receipt .work/<task>/receipt.json -- <reviewer command> [args...]

The packet is piped to the command's standard input. The command runs in a new,
empty temporary folder, with only these environment variables: PATH, HOME,
USERPROFILE, SYSTEMROOT, TEMP, TMP and LANG, plus any name given with
--allow-env NAME (repeatable). It cannot inherit a token from your shell by
accident, and it does not start inside your project folder. Output is capped at
1 MB. At the time limit the command and anything it started are stopped.

This is process hygiene, not a sandbox. It does not block network access, and
it does not stop a command that reads files by absolute path or from the home
folder. If the reviewer must be unable to read or write anything, use the
reviewer tool's own read-only or no-tools mode as well, and say in the review
record which controls were actually applied.

The receipt records the command name (not its path or arguments), the number of
arguments, the packet's SHA-256, the exit code, whether it timed out, the time
taken, the output size, the environment names passed and "sandboxed": false. It
never stores the packet or the output text. Standard library only, Python 3.9
or later.

Exit codes: the command's own code; 124 when the time limit stopped it; 125 when
it could not be started.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE_ENV = ("PATH", "HOME", "USERPROFILE", "SYSTEMROOT", "TEMP", "TMP", "LANG")
MAX_OUTPUT = 1_000_000
WINDOWS = os.name == "nt"
NEW_PROCESS_GROUP = 0x200  # subprocess.CREATE_NEW_PROCESS_GROUP on Windows


def stop(process: subprocess.Popen) -> None:
    """Stop the command and anything it started."""
    try:
        if WINDOWS:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True, timeout=30)
        else:
            os.killpg(process.pid, signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        pass
    if process.poll() is None:
        process.kill()


def run(command: list, packet: bytes, env: dict, timeout: int) -> tuple:
    """(exit code, timed out, output) for the command run in an empty temporary folder."""
    with tempfile.TemporaryDirectory(prefix="review-") as work:
        options = {"creationflags": NEW_PROCESS_GROUP} if WINDOWS else {"start_new_session": True}
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   cwd=work, env=env, **options)
        try:
            output, _ = process.communicate(packet, timeout=timeout)
            return process.returncode, False, output
        except subprocess.TimeoutExpired:
            stop(process)
            try:
                output, _ = process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                output = b""
            return 124, True, output


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--packet", type=Path, required=True, help="the review packet (JSON)")
    parser.add_argument("--timeout", type=int, default=300, help="seconds before the command is stopped (default 300)")
    parser.add_argument("--receipt", type=Path, required=True, help="where to write the receipt (JSON)")
    parser.add_argument("--allow-env", action="append", default=[], metavar="NAME",
                        help="also pass this environment variable (repeatable)")
    parser.add_argument("--output", type=Path, help="write the reviewer's output here (default: standard output)")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- then the reviewer command")
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        print("refused: give the reviewer command after --", file=sys.stderr)
        return 125
    if args.timeout < 1:
        print("refused: --timeout must be at least 1 second", file=sys.stderr)
        return 125
    try:
        packet = args.packet.read_bytes()
        json.loads(packet)
    except (OSError, ValueError):
        print("refused: the packet is missing or is not valid JSON", file=sys.stderr)
        return 125
    env = {name: os.environ[name] for name in dict.fromkeys([*BASE_ENV, *args.allow_env]) if name in os.environ}
    started = time.monotonic()
    try:
        code, timed_out, output = run(command, packet, env, args.timeout)
    except OSError as error:
        print(f"refused: could not start the command ({type(error).__name__})", file=sys.stderr)
        return 125
    output = output[:MAX_OUTPUT]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output)
    else:
        sys.stdout.buffer.write(output)
        sys.stdout.flush()
    receipt = {"command": Path(command[0]).name, "argument_count": len(command) - 1,
               "packet_sha256": hashlib.sha256(packet).hexdigest(), "exit_code": code, "timed_out": timed_out,
               "seconds": round(time.monotonic() - started, 2), "output_bytes": len(output),
               "environment_names": sorted(env), "sandboxed": False}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=1), encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
