# Drift check (Python)

**Lists every file that differs between a shared repository folder and an installed copy, and changes neither.**

It is the read-only part of the [config-as-code](../../skills/config-as-code/README.md) skill: step 2 (check for drift first) and step 7 (read back). Deciding what to do with each difference stays with a person.

## Files

- `drift_check.py`: the script. Standard library only, Python 3.9 or later.

## Run it

From the folder that holds both sides, or with full paths:

```
python drift_check.py --repo team-config --installed installed-config
```

Map each folder the setup manages, so the check covers that list and nothing else:

```
python drift_check.py --repo team-config --installed installed-config --map rules=rules --map skills=agent-skills
```

Add `--ignore "*.local.json"` (repeatable) or `--ignore-file` for secrets and machine-only files. Add `--json` for a machine-readable report.

Example report (fictional):

```
DIFFERS:            rules/review.md (installed newer)
ONLY IN REPO:       skills/intake/SKILL.md
2 difference(s). Nothing was changed.
```

## What the result means

| Exit code | Meaning |
|---|---|
| 0 | No drift in the files compared. |
| 1 | Drift found. Each difference is listed. |
| 2 | A folder is missing or a file could not be read. This is never a clean result. |

- Contents are compared by SHA-256. A file that was touched but not changed is not drift.
- "repo newer" or "installed newer" comes from file times. It is a hint, not a verdict on which side is right.
- Logs, caches and byte-code (`.git`, `__pycache__`, `*.pyc`, `node_modules`, `logs`, `*.log`, `.DS_Store`) are ignored at any depth, because they change on every run and bury real drift.
- Links and junctions are not followed.

## Limits

- Anything not under `--repo` and `--installed`, or not mapped, is invisible to the check.
- An ignored file is not checked at all. A clean result says nothing about whether a machine-only file is correct.
- A clean result shows the files match. It does not show the skills work.
