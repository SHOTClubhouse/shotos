# Pilot and preflight

**Draft for the administrator.** The three invented rows were checked on paper. Workbook pilot, rollback and live run are pending.

**Scope.** Update only column H in the Players sheet from the dates in column F and the age on 1 September 2026. The administrator reports 212 rows and says the fees page uses this sheet. Both facts still need read-back from the actual systems.

## Desk check

| Sample | Why chosen | Expected result in H | What to verify on the copy |
| --- | --- | --- | --- |
| A | Date stored as a date | U11. Age is 10 on 1 September. | The workbook reads the date and changes U10 to U11. |
| B | Date stored as text | U12. Age is 11 on 1 September. | The workbook parses the supplied format and changes U11 to U12. Flag other formats that cannot be interpreted confidently. |
| C | Blank date | Keep U10 and list the row for review. | H remains unchanged. The exception appears in the review list. |

## Preflight before the full run

- **Inputs.** Confirm the cut-off and bands with the administrator. Count and deduplicate the actual rows. Record how blanks and invalid dates are handled.
- **Target.** Ask the administrator for a copy that the fees page cannot read. Use three representative rows in that copy and inspect their values in the sheet.
- **Rollback.** Preserve the original workbook and rehearse restoring the original column H values on the copy before asking to write live.
- **Budget.** Ask the administrator for a run limit once the workbook and pilot timing are known.
- **Stop condition.** Stop on any mismatch with the expected outcomes or any change outside column H. An expected blank remains a review item.
- **Approval.** Present the inspected pilot and recovery proof to the administrator. Record approval for the exact target and first batch before any live write. The fees page needs its own read-back.

Keep this as a one-off unless the administrator confirms the change repeats and names an owner. No workbook rows were attempted, so there are no observed write, skip or failure counts.
