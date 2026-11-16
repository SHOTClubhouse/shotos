#!/usr/bin/env python3
"""Install a Git pre-push hook that runs the SHOTos gate in fast mode.

Examples:
  python tools/install_hooks.py              install the hook
  python tools/install_hooks.py --uninstall  remove it

Before each push the hook runs `tools/local_gate.py --pre-push`. It scans the
commits being pushed for private terms and runs the quick checks. A NO-GO
stops the push and the card says why.

An existing pre-push hook that this script did not write is left alone unless
you pass --force, which keeps a copy as pre-push.before-shotos.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MARKER = "# Installed by SHOTos tools/install_hooks.py"


def hooks_dir(repo: Path = REPO) -> Path:
    found = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-path", "hooks"], capture_output=True,
                           text=True, check=True, timeout=30).stdout.strip()
    path = Path(found)
    return path if path.is_absolute() else repo / path


def hook_text(python: str = sys.executable) -> str:
    python = Path(python).as_posix()
    return f"""#!/bin/sh
{MARKER}
# Runs the SHOTos gate in fast mode before each push. Git passes the refs being pushed on standard input.
cd "$(git rev-parse --show-toplevel)" || exit 1
PYTHON="{python}"
[ -x "$PYTHON" ] || PYTHON="$(command -v python3 || command -v python)"
exec "$PYTHON" tools/local_gate.py --pre-push
"""


def install(repo: Path = REPO, force: bool = False, python: str = sys.executable) -> str:
    hook = hooks_dir(repo) / "pre-push"
    hook.parent.mkdir(parents=True, exist_ok=True)
    if hook.exists() and MARKER not in hook.read_text(encoding="utf-8", errors="replace"):
        if not force:
            raise SystemExit(f"{hook} already exists and was not written by SHOTos. "
                             "Run again with --force to replace it; a copy is kept.")
        hook.replace(hook.with_name("pre-push.before-shotos"))
    hook.write_text(hook_text(python), encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    return f"Installed the pre-push hook at {hook}."


def uninstall(repo: Path = REPO) -> str:
    hook = hooks_dir(repo) / "pre-push"
    if not hook.exists():
        return "There is no pre-push hook to remove."
    if MARKER not in hook.read_text(encoding="utf-8", errors="replace"):
        raise SystemExit(f"{hook} was not written by SHOTos, so it was left alone.")
    hook.unlink()
    backup = hook.with_name("pre-push.before-shotos")
    if backup.exists():
        backup.replace(hook)
        return "Removed the SHOTos pre-push hook and put the earlier hook back."
    return "Removed the SHOTos pre-push hook."


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--uninstall", action="store_true", help="remove the SHOTos pre-push hook")
    parser.add_argument("--force", action="store_true", help="replace a pre-push hook SHOTos did not write")
    args = parser.parse_args(argv)
    print(uninstall() if args.uninstall else install(force=args.force))
    return 0


if __name__ == "__main__":
    sys.exit(main())
