# Output

Collection: `northgate-skills/`, three skills. No file has been changed.

| Skill | Frontmatter | README | Example | Eval normal | Eval contrary | Links | Evidence status |
|---|---|---|---|---|---|---|---|
| `repair-quote` | pass | pass | pass | pass | **missing** | pass | not stated in this input |
| `repair-estimate` | **fail**: name `repair-estimates` does not match the folder | **missing** | **missing** | **missing** | **missing** | not checked | not stated |
| `stock-check` | pass | pass | pass | pass | pass | **fail** | **flag** |

**Collisions**

| Skill A | Skill B | Sample request both match | Suggestion |
|---|---|---|---|
| `repair-quote` | `repair-estimate` | "Write a price for repairing Mrs Okafor's bike from the job sheet" | Merge them, or add a "when not to use this" line to each: quotes are a fixed price offered to the customer, estimates are internal guides. |

**Broken links:** `stock-check/README.md` links to `../templates/stock-sheet.md`, which does not exist.

**Evidence-status flags:** `stock-check` says "Tested in paired evals" but links no result. Until a result is linked, the honest state is "Cases written, not yet run".

This audit checks wiring only. It does not show that any skill is correct, useful or good practice. Tell me which findings to fix, and I will make the changes in a separate step.
