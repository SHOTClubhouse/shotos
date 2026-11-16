#!/usr/bin/env python3
"""Install a Git pre-push hook that runs the SHOTos gate in fast mode.

Examples:
  python tools/install_hooks.py              install the hook
  python tools/install_hooks.py --uninstall  remove it

Before each push the hook runs `tools/local_gate.py --pre-push`. It scans the
commits being pushed for private terms and runs the quick checks. A NO-GO
stops the push and the card says why.

The SHOTos lines sit in a marked block. Installing again replaces only that
block, and uninstalling removes only that block, so checks you add before or
after it are kept. Checks after the block can still read the pushed refs.

An existing pre-push hook that this script did not write, a SHOTos block with
lines added or changed inside it, or a hook from an earlier version of this
script that was changed by hand, is left alone unless you pass --force, which
keeps a copy as pre-push.before-shotos. Uninstalling leaves all of these alone.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from launch import launchable  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
MARKER = "# Installed by SHOTos tools/install_hooks.py"
BEGIN = f"{MARKER}: start of the SHOTos block. Add your own checks outside it."
END = "# End of the SHOTos block."
BACKUP = "pre-push.before-shotos"
SHEBANG = "#!/bin/sh\n"


def hooks_dir(repo: Path = REPO) -> Path:
    found = subprocess.run(launchable(["git", "-C", str(repo), "rev-parse", "--git-path", "hooks"]), capture_output=True,
                           text=True, check=True, timeout=30).stdout.strip()
    path = Path(found)
    return path if path.is_absolute() else repo / path


def block(python: str = sys.executable) -> str:
    return _block(Path(python).as_posix())


def _block(python: str) -> str:
    return f"""{BEGIN}
# Runs the SHOTos gate in fast mode before each push. Git passes the refs being pushed on standard input;
# they are kept so that checks after this block can read them too.
shotos_refs="$(mktemp)" || exit 1
cat > "$shotos_refs"
(
  cd "$(git rev-parse --show-toplevel)" || exit 1
  PYTHON="{python}"
  [ -x "$PYTHON" ] || PYTHON="$(command -v python3 || command -v python)"
  "$PYTHON" tools/local_gate.py --pre-push
) < "$shotos_refs"
shotos_status=$?
exec < "$shotos_refs"
rm -f "$shotos_refs"
[ "$shotos_status" -eq 0 ] || exit "$shotos_status"
{END}
"""


def hook_text(python: str = sys.executable) -> str:
    return SHEBANG + block(python)


def _legacy(python: str) -> str:
    return f"""#!/bin/sh
{MARKER}
# Runs the SHOTos gate in fast mode before each push. Git passes the refs being pushed on standard input.
cd "$(git rev-parse --show-toplevel)" || exit 1
PYTHON="{python}"
[ -x "$PYTHON" ] || PYTHON="$(command -v python3 || command -v python)"
exec "$PYTHON" tools/local_gate.py --pre-push
"""


# The whole-file hook an earlier version of this script wrote, with whichever Python it named.
LEGACY = re.compile(r'[^"\n]*'.join(re.escape(part) for part in _legacy("\0").split("\0")))


def is_legacy(text: str) -> bool:
    """True when the text is exactly the hook an earlier version wrote, so nothing in it is anyone else's."""
    return bool(LEGACY.fullmatch(text))


# The SHOTos block this script writes, with whichever Python it named.
BLOCK = re.compile(r'[^"\n]*'.join(re.escape(part) for part in _block("\0").split("\0")))


def is_ours(middle: str) -> bool:
    """True when the block is exactly as this script wrote it, so replacing it removes nobody's check."""
    return bool(BLOCK.fullmatch(middle.replace("\r\n", "\n")))


def split_block(text: str):
    """(before, block, after) for the one SHOTos block, or None when there is not exactly one whole block."""
    lines = text.splitlines(keepends=True)
    starts = [n for n, line in enumerate(lines) if line.rstrip("\r\n") == BEGIN]
    ends = [n for n, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        return None
    before = "".join(lines[:starts[0]])
    middle = "".join(lines[starts[0]:ends[0] + 1])
    middle += "" if middle.endswith("\n") else "\n"
    return (before + ("" if not before or before.endswith("\n") else "\n"), middle,
            "".join(lines[ends[0] + 1:]))


def refuse(hook: Path, text: str, action: str):
    if MARKER in text:
        return f"{hook} has SHOTos lines that were changed by hand, so {action}. Move your own checks " \
               "outside the SHOTos lines, or remove them by hand."
    return f"{hook} already exists and was not written by SHOTos, so {action}."


def install(repo: Path = REPO, force: bool = False, python: str = sys.executable) -> str:
    hook = hooks_dir(repo) / "pre-push"
    hook.parent.mkdir(parents=True, exist_ok=True)
    text = hook.read_text(encoding="utf-8", errors="replace") if hook.exists() else None
    parts = split_block(text) if text is not None else None
    if text is None or is_legacy(text):
        new, done = hook_text(python), f"Installed the pre-push hook at {hook}."
    elif parts is not None and is_ours(parts[1]):
        new, done = parts[0] + block(python) + parts[2], f"Updated the SHOTos block in {hook}; the rest was kept."
    else:
        if not force:
            raise SystemExit(refuse(hook, text, "it was left alone") + " Run again with --force to replace it; "
                             f"a copy is kept as {BACKUP}.")
        backup = hook.with_name(BACKUP)
        if backup.exists():
            raise SystemExit(f"{backup} already exists. Move it somewhere safe first, so it is not overwritten.")
        if parts is not None:
            # Only the block was changed by hand: keep a copy of the whole hook, then replace just the block.
            backup.write_bytes(hook.read_bytes())
            new, done = parts[0] + block(python) + parts[2], \
                f"Replaced the SHOTos block in {hook}, which was changed by hand; the rest was kept. " \
                f"The earlier hook is in {backup}."
        else:
            hook.replace(backup)
            new, done = hook_text(python), f"Installed the pre-push hook at {hook}. The earlier hook is in {backup}."
    hook.write_text(new, encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    return done


def uninstall(repo: Path = REPO) -> str:
    hook = hooks_dir(repo) / "pre-push"
    if not hook.exists():
        return "There is no pre-push hook to remove."
    text = hook.read_text(encoding="utf-8", errors="replace")
    parts = split_block(text)
    if parts is not None and not is_ours(parts[1]):
        raise SystemExit(refuse(hook, text, "it was left alone"))
    if parts is not None and (parts[0] + parts[2]).strip() not in ("", SHEBANG.strip()):
        hook.write_text(parts[0] + parts[2], encoding="utf-8", newline="\n")
        return "Removed the SHOTos block from the pre-push hook and kept the rest."
    if parts is None and not is_legacy(text):
        raise SystemExit(refuse(hook, text, "it was left alone"))
    hook.unlink()
    backup = hook.with_name(BACKUP)
    if backup.exists():
        backup.replace(hook)
        return "Removed the SHOTos pre-push hook and put the earlier hook back."
    return "Removed the SHOTos pre-push hook."


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--uninstall", action="store_true", help="remove the SHOTos pre-push hook")
    parser.add_argument("--force", action="store_true",
                        help="replace a pre-push hook SHOTos cannot update in place; a copy is kept")
    args = parser.parse_args(argv)
    print(uninstall() if args.uninstall else install(force=args.force))
    return 0


if __name__ == "__main__":
    sys.exit(main())
