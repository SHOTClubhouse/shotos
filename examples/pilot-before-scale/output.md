# Pilot and preflight

**Task:** recalculate the age-group code (column H) for every player in `registrations.xlsx` from date of birth (column F), using age on 1 September
**Owner (gives the yes for the full run):** the administrator
**Items in the full run:** 212 rows
**Action on each item, and can it be undone:** overwrites column H. The sheet feeds the fees page, so a wrong code changes what a parent sees. Reversible only if a copy is taken first

I will not edit the shared sheet until a copy exists and you have said yes to the pilot. The pilot below runs on the copy.

## Pilot (three items or fewer)
| Item | Why chosen | Result, read in its real home | Problems found |
|---|---|---|---|
| Row 14, date of birth 03/04/2016 typed as a real date | Typical case | Code recalculated and agrees with a hand calculation | None |
| Row 87, date of birth typed as text "5 Nov 2014" | Awkward: text, not a date | First attempt left the old code unchanged without warning because the cell was not read as a date | Silent skip. A rule that ignores text dates would leave 31 rows (my count of text cells in column F) on last year's code with no error |
| Row 140, date of birth blank | Should be skipped | First attempt wrote "U8", treating a blank as a very young child | Wrong: blank was handled as zero |

## Fixes made, and re-run result
- Text dates are now converted before the calculation. Any text I cannot read as a date is flagged, not guessed.
- A blank date of birth leaves the code unchanged and adds the row to a "needs review" list.
- Re-ran the same three rows: row 14 correct, row 87 now correct, row 140 untouched and listed. I looked at the three cells in the copy of the sheet, not only in my log.

## Preflight checklist
- [x] Inputs: 212 rows counted in the Players sheet; no duplicate player numbers found; dates are in column F. 31 text dates and an unknown number of blanks to be reported in the run
- [x] Targets: column H on a copy first, then column H of the live sheet only after your yes. The fees page reads the live sheet
- [x] Rollback: copy of the whole workbook saved as `registrations-before-age-bands.xlsx` before the pilot. Restore tested by opening the copy and checking row 14's old code. Restoring the live sheet means pasting column H back from the copy
- [x] Budget: about 10 minutes of agent time and no money. Pause if it takes longer than 20 minutes
- [x] Stop condition: halt after two rows that cannot be classified in a row, or after 15 flagged rows in total, and tell you
- [ ] External actions: none. No email is sent. The fees page updates by itself; I cannot see it, so please look at it afterwards

## One-off or repeatable?
Chosen: one-off. The age bands change at most once a year, and the sheet layout may change before then. Keep a short note of the rule instead of building a tool. If the club's rule changes mid-season too, revisit.

## Run log
| Batch | Items | Done | Skipped | Failed | Sample checked |
|---|---|---|---|---|---|
| Not run yet. Waiting for your yes to run the first batch of 50 on the live sheet | | | | | |

## Owner's yes for the full run
Waiting. After the first batch of 50, I will report the counts and show you a sample of ten rows before the remaining 162.
