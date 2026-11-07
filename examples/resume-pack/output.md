# Resume pack: deposit reminders to a database table

**Written (date, time):** end of session (add the date when saved)
**Owning record:** `.work/deposit-reminders/task.md` (updated first; this pack points to it)
**Stage:** Operate
**Branch / commit / version:** `feature/reminders-table`; last commit does not include the two files marked uncommitted below

## State
- Done and checked: table definition `migrations/0004_reminders.sql` passes a dry run on the test database. The import script loads 212 rows into the test database and skips duplicates; its test passes.
- Done, not checked: `draft_emails.py` is written and has never been run against real rows.
- In progress: tests for the draft emails.
- Blocked, and by whom: the live migration waits for a person to apply it (below). The date column type waits for Dominic Hale to confirm.
- Planned: run `draft_emails.py` on a sample, show ten drafts to Dominic, then a full batch only after his yes.

## Files and where they are
| Path (relative) | What it is | Committed? |
|---|---|---|
| `migrations/0004_reminders.sql` | Creates the reminders table | Yes |
| `import_reminders.py` | Loads the spreadsheet rows, skips duplicates | Yes |
| `draft_emails.py` | Creates draft emails in a folder | No |
| `tests/test_drafts.py` | Empty placeholder for draft tests | No |
| `.work/deposit-reminders/task.md` | Owning record with acceptance | Yes |

## Decisions and open questions
| Date | Decision or question | Decided by / who can answer | Assumed by the agent? |
|---|---|---|---|
| (call) | No email sends until Dominic has seen ten drafts | Dominic Hale | No |
| Open | Should the reminder date be a date type or text? | Dominic Hale | Yes: the agent assumed a date type |
| Open | One tenant row is noted as disputed with "call first". How should such rows be excluded from batches? | Dominic Hale | Not decided |

## Pending manual steps
| Order | Step | Where | Who can do it | How to confirm it was done | Irreversible? |
|---|---|---|---|---|---|
| 1 | Confirm the date column type and the treatment of disputed rows | Task record and migration file | Dominic Hale | Written decisions in the task record | No |
| 2 | Check the final revision on the test database and approve the live plan | Test database and task record | Operator runs the test, Dominic Hale approves | Test result and approval name the same revision | No |
| 3 | Apply the approved migration and import after checking current live state | Live database | Named live operator, once Dominic Hale confirms authority | Schema matches the approved revision and the eligible unique rows reconcile | Requires a rollback or recovery plan |
| 4 | Review ten drafts and approve the first batch | Draft folder | Dominic Hale | His written yes in the task file | Sending is irreversible; the agent does not send |

## Next prompt (paste into the next session)
> Goal: finish the deposit reminders task in `.work/deposit-reminders/task.md`. The last checkpoint had no live migration receipt.
> Read first: `.work/deposit-reminders/task.md` and this pack.
> Read-only state and version check: open the task record, current branch status and migration revision. Check for a newer migration receipt in the task record.
> If the record or revision changed: rerun the affected test checks and confirm the scope of any approval. Keep live work with the named operator, who checks the current schema before any application.
> Done means: each eligible reminder appears once in the table, with disputed rows handled under the agreed rule, drafts are created but never sent, and Dominic Hale has approved the first batch after seeing ten drafts.
> Do not do without the owner's yes: touching the live database, sending any email, changing the date column type.

## Learnings
- What worked: a dry run of the migration on the test database before any live step.
- What failed and why: the first import created duplicate rows because the spreadsheet had trailing spaces in the tenant reference. Trimming the spaces fixed it.
- Suggested rule or skill change (not yet a rule): add a trim-and-compare check to any import from a spreadsheet. Pass to the learning loop with the duplicate case as evidence.

## Not verified in this pack
- The 212-row count and passing import test describe the earlier test revision. Re-run the checks if the input or migration revision changed.
- That `draft_emails.py` has no obvious fault: it has not been run.

## Kept out on purpose
The live connection string and password, tenant names, phone numbers and the call notes about the disputed tenant are not included. Credentials are held in the team password manager; Dominic Hale can grant access. The spreadsheet row with the "call first" note is in the source spreadsheet.
