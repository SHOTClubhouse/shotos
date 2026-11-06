#!/bin/sh
# Run the claim-check Stop hook with whichever Python 3.9+ works on this machine.
dir=$(dirname "$0")
for py in python3 python py; do
  if "$py" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1; then
    exec "$py" "$dir/stop_claim_check.py"
  fi
done
echo "claim-check: no Python 3.9 or later found, so the check was skipped." >&2
exit 0
