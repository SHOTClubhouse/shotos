#!/usr/bin/env python3
"""run-contained: run a reviewer command on a review packet, with a time limit, a clean environment and a receipt.

Control 7 (independent review) and the cross-agent-review skill:

    python tools/run_contained.py --packet .work/<task>/packet.json --timeout 300 --receipt .work/<task>/receipt.json -- <reviewer command> [args...]
    python tools/run_contained.py --allow-network --packet ... --receipt ... -- <reviewer command> [args...]

By default this is a dry run: it checks the packet, prints what it would launch
and launches nothing. Nothing is written, not even the receipt. The runner
cannot block the network, so any reviewer it launches can send the packet
somewhere, using credentials it finds under the home folder. It therefore
launches a reviewer only with --allow-network, which the owner passes once
they have agreed that the packet may leave this machine. The receipt records
"network_allowed": true.

The packet is piped to the command's standard input. The command runs in a new,
empty temporary folder, with only these environment variables: PATH, HOME,
USERPROFILE, SYSTEMROOT, TEMP, TMP and LANG, plus any name given with
--allow-env NAME (repeatable). It cannot inherit a token from your shell by
accident, and it does not start inside your project folder. Output is capped at
1 MB while it is read: the first 1 MB is kept and the rest is read and dropped,
so a noisy command cannot fill memory. The time limit covers the output as
well as the command: if the command exits while something it started still
holds its output open, the run is not over until that output ends. At the
time limit the command and anything it started are stopped, through a job
object on Windows and a process group elsewhere, even if the command itself
has already exited. On Windows the command starts suspended and runs only
once it is inside its job object: if the job cannot be made or the command
cannot join it, the command is stopped before it runs and the run is refused.

This is process hygiene, not a sandbox. It does not block network access, and
it does not stop a command that reads files by absolute path or from the home
folder. If the reviewer must be unable to read or write anything, use the
reviewer tool's own read-only or no-tools mode as well, and say in the review
record which controls were actually applied.

The receipt records the command name (not its path or arguments), the number of
arguments, the packet's SHA-256, the exit code, whether it timed out, the time
taken, the output size kept, whether output was cut, at the cap or by the
time limit ("output_truncated"), the environment names passed, "network_allowed": true
and "sandboxed": false. It never stores the packet or the output text. Standard
library only, Python 3.9 or later.

Exit codes: 0 for a dry run; the command's own code; 124 when the time limit
stopped it; 125 when it was refused or could not be started.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from launch import launchable  # noqa: E402

BASE_ENV = ("PATH", "HOME", "USERPROFILE", "SYSTEMROOT", "TEMP", "TMP", "LANG")
MAX_OUTPUT = 1_000_000
WINDOWS = os.name == "nt"
NEW_PROCESS_GROUP = 0x200  # subprocess.CREATE_NEW_PROCESS_GROUP on Windows
SUSPENDED = 0x4  # CREATE_SUSPENDED on Windows
GRACE = 10  # seconds to wait for the output to end once everything has been stopped

if WINDOWS:
    from ctypes import wintypes
    KERNEL32, NTDLL = ctypes.WinDLL("kernel32", use_last_error=True), ctypes.WinDLL("ntdll")
    KERNEL32.CreateJobObjectW.restype = wintypes.HANDLE
    KERNEL32.CreateJobObjectW.argtypes = (wintypes.LPVOID, wintypes.LPCWSTR)
    KERNEL32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    KERNEL32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    KERNEL32.CloseHandle.argtypes = (wintypes.HANDLE,)
    NTDLL.NtResumeProcess.argtypes = (wintypes.HANDLE,)


class Uncontained(Exception):
    """The command could not be put in a job object, so it was stopped before it ran."""


def contain(process: subprocess.Popen):
    """Put the command, started suspended, in a new Windows job object, then let it run.

    Everything it starts joins the job, so the whole tree can be stopped even after the command itself has
    exited. Returns the job handle. If no job can be made, the command cannot join it or it cannot be resumed,
    the command is stopped while still suspended and Uncontained is raised: it never runs outside a job."""
    job, failure = None, None
    try:
        job = KERNEL32.CreateJobObjectW(None, None)
        if not job:
            failure = f"could not create a job object (Windows error {ctypes.get_last_error()})"
        elif not KERNEL32.AssignProcessToJobObject(job, int(process._handle)):
            failure = f"could not put the command in a job object (Windows error {ctypes.get_last_error()})"
        elif NTDLL.NtResumeProcess(int(process._handle)) != 0:
            failure = "could not resume the command inside its job object"
    except BaseException:
        discard(process, job)
        raise
    if failure:
        discard(process, job)
        raise Uncontained(failure)
    return job


def discard(process: subprocess.Popen, job=None) -> None:
    """Stop a command that was never let run, close its pipes and release its job object, if it has one."""
    try:
        if job:
            KERNEL32.TerminateJobObject(job, 125)
        if process.poll() is None:
            process.kill()
        process.wait()
    finally:
        process.stdin.close()
        process.stdout.close()
        if job:
            KERNEL32.CloseHandle(job)


def stop(process: subprocess.Popen, job=None) -> None:
    """Stop the command and anything it started, even if the command itself has already exited."""
    try:
        if job and KERNEL32.TerminateJobObject(job, 124):
            pass
        elif WINDOWS:
            subprocess.run(launchable(["taskkill", "/F", "/T", "/PID", str(process.pid)]),
                           capture_output=True, timeout=30)
        else:
            os.killpg(process.pid, signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        pass
    if process.poll() is None:
        process.kill()


def run(command: list, packet: bytes, env: dict, timeout: int) -> tuple:
    """(exit code, timed out, output, truncated) for the command run in an empty temporary folder.

    Output is read in chunks and only the first MAX_OUTPUT bytes are kept, so a noisy command cannot fill
    memory. The rest is read and dropped, so the command is never blocked on a full pipe. The run lasts until
    the command has exited and its output has ended, whichever is later, and the time limit applies to both:
    a child that keeps the output open after the command exits is stopped with it. Output is truncated when
    it passed the cap or the time limit cut it short."""
    cap, kept, seen = MAX_OUTPUT, bytearray(), [0]
    deadline = time.monotonic() + timeout
    with tempfile.TemporaryDirectory(prefix="review-") as work:
        options = {"creationflags": NEW_PROCESS_GROUP | SUSPENDED} if WINDOWS else {"start_new_session": True}
        process = subprocess.Popen(launchable(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=work, env=env, **options)
        job = contain(process) if WINDOWS else None

        def read():
            try:
                for chunk in iter(lambda: os.read(process.stdout.fileno(), 65536), b""):
                    seen[0] += len(chunk)
                    kept.extend(chunk[:max(0, cap - len(kept))])
            except OSError:
                pass

        def write():
            try:
                process.stdin.write(packet)
                process.stdin.close()
            except OSError:
                pass

        reader, writer = threading.Thread(target=read, daemon=True), threading.Thread(target=write, daemon=True)
        reader.start()
        writer.start()
        try:
            try:
                process.wait(timeout=max(0.0, deadline - time.monotonic()))
                reader.join(max(0.0, deadline - time.monotonic()))
                timed_out = reader.is_alive()
            except subprocess.TimeoutExpired:
                timed_out = True
            if timed_out:
                stop(process, job)
                reader.join(GRACE)
            if not reader.is_alive():
                process.stdout.close()
            code = 124 if timed_out else process.returncode
            return code, timed_out, bytes(kept), timed_out or seen[0] > cap
        finally:
            if job:
                KERNEL32.CloseHandle(job)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--packet", type=Path, required=True, help="the review packet (JSON)")
    parser.add_argument("--timeout", type=int, default=300, help="seconds before the command is stopped (default 300)")
    parser.add_argument("--receipt", type=Path, required=True, help="where to write the receipt (JSON)")
    parser.add_argument("--allow-env", action="append", default=[], metavar="NAME",
                        help="also pass this environment variable (repeatable)")
    parser.add_argument("--output", type=Path, help="write the reviewer's output here (default: standard output)")
    parser.add_argument("--allow-network", action="store_true",
                        help="launch the reviewer, which can reach the network and send the packet anywhere "
                             "(default: a dry run that launches nothing)")
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
    if not args.allow_network:
        print(f"Dry run: nothing was launched.\n"
              f"Would run: {subprocess.list2cmdline(command) if WINDOWS else shlex.join(command)}\n"
              f"In: a new, empty temporary folder\n"
              f"Packet: {len(packet)} bytes, SHA-256 {hashlib.sha256(packet).hexdigest()}, on standard input\n"
              f"Environment names: {', '.join(sorted(env)) or 'none'}\n"
              f"Time limit: {args.timeout} seconds\n"
              "The reviewer could reach the network and send the packet anywhere, using any credentials it can "
              "read under the home folder. Run again with --allow-network to launch it.")
        return 0
    started = time.monotonic()
    try:
        code, timed_out, output, truncated = run(command, packet, env, args.timeout)
    except Uncontained as error:
        print(f"refused: {error}. The command was stopped before it ran, because its time limit could not be "
              "enforced on anything it started", file=sys.stderr)
        return 125
    except OSError as error:
        print(f"refused: could not start the command ({type(error).__name__})", file=sys.stderr)
        return 125
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output)
    else:
        sys.stdout.buffer.write(output)
        sys.stdout.flush()
    receipt = {"command": Path(command[0]).name, "argument_count": len(command) - 1,
               "packet_sha256": hashlib.sha256(packet).hexdigest(), "exit_code": code, "timed_out": timed_out,
               "seconds": round(time.monotonic() - started, 2), "output_bytes": len(output),
               "output_truncated": truncated,
               "environment_names": sorted(env), "network_allowed": True, "sandboxed": False}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=1), encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
