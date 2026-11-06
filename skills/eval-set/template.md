# Eval set

**Task (what the AI produces):**
**Owner (decides what good looks like):**
**Where the real examples came from:**
**Date created:**

## Cases
| ID | Input (private details removed) | Must contain | Must not contain | Why this case | Expected to fail? |
|---|---|---|---|---|---|
| 01 | | | | | no |
| 02 | | | | | no |
| 03 | | | | | yes |

For a JSON file, use one object per case:

```json
{"cases": [
  {"id": "01", "input": "", "must_contain": ["a|b"], "must_not_contain": [""], "note": ""}
]}
```

## How to grade
- Automatic check: case-insensitive text match on must contain (`|` means any of) and must not contain.
- A person reads: all failures, and a sample of passes.
- Pass bar, set before the first run:

## Run log
| Date | Model and prompt version | Passed | Failed | Read by |
|---|---|---|---|---|
| | | | | |
