"""Find an external program before launching it, so a release runs the same on Windows as elsewhere.

Python cannot start a program by bare name when Windows knows it only as a `.cmd` or `.bat` shim, which is how
many command-line tools (npm packages, `claude`, sometimes `gh`) are installed there. `launchable` looks the
program up with `shutil.which`, names it plainly when it is missing, and turns a `.cmd` or `.bat` shim into a
command line that `cmd.exe` can run. It never uses `shell=True`: a shim is run only when no argument carries
a character that `cmd.exe` would read as syntax.
"""

from __future__ import annotations

import os
import shutil
import subprocess

WINDOWS = os.name == "nt"
SHIMS = (".cmd", ".bat")
# cmd.exe reads these inside a quoted argument as well: expansion, escapes, redirection, pipes, quotes, line ends.
UNSAFE = set('"%^&|<>!\r\n\0')


class LaunchError(OSError):
    """A program could not be started, with a message fit to show the person running the release."""


class MissingTool(LaunchError):
    pass


class UnsafeArgument(LaunchError):
    pass


def launchable(command):
    """Return what to hand to subprocess for `command`: a list, or one command line for a Windows shim."""
    name, *args = command
    found = shutil.which(str(name))
    if not found:
        raise MissingTool(f"`{name}` is not installed or is not on PATH, so it could not be run.")
    if WINDOWS and found.lower().endswith(SHIMS):
        args = [str(arg) for arg in args]
        bad = [arg for arg in args if UNSAFE & set(arg)]
        if bad:
            raise UnsafeArgument(f"`{name}` is a Windows .cmd shim, which cannot be given an argument containing "
                                 f"any of  \" % ^ & | < > !  or a line break: {bad[0][:60]!r}.")
        return f'cmd.exe /d /s /c "{subprocess.list2cmdline([found, *args])}"'
    return [found, *args]
