# Runbook: monthly landlord statements

**Purpose (one sentence):** Produce a statement for each landlord from the month's rent export and publish it to the landlord portal.
**Owner / backup:** Mei Tan / Jaswinder Gill (backup while Mei is on leave from the 14th)
**Accepted as usable by (name, date):** Dominic Hale, finance lead, not yet accepted
**Status:** Run once, observed (4 November, Jaswinder watched Mei). Not yet run by Jaswinder.
**Review date:** after the December run, then every six months

## Schedule and triggers
Runs once a month. Export on the 2nd working day, publish on the 5th working day. The export plus script takes about 5 minutes; checking takes longer. Needs: the month's rent export in the accounts system, the fees sheet with a management fee rate for every property, and the ledger report for the month.

## Access needed
Read access to the accounts system rent export; write access to the statements folder; the statement script on the team machine; a landlord portal login with the "publish" role. Ask Dominic Hale for access. Do not store the portal password in this document.

## Steps
| # | Action | Expected result | Basis |
|---|---|---|---|
| 1 | On the 2nd working day, export the month's rents from the accounts system. | A CSV file. | Seen (3 minutes) |
| 2 | Save it in the statements folder as rent-YYYY-MM.csv, for example rent-2025-10.csv. | File present with that exact name. | Told, consistent with the command history |
| 3 | Run `python statements.py --month 2025-10 --input rent-2025-10.csv --out output/2025-10` with the month changed. | About 2 minutes; the script ends with no error; 74 PDFs for October. Count may differ by month. | Seen |
| 4 | Open the ledger report for the month and compare its total with the sum of the statements. | They match to the penny (October: 38,412.60 pounds). | Seen |
| 5 | If they match, upload the PDFs from the output folder to the landlord portal as unpublished. | PDFs listed in the portal, not yet emailed. | Told |
| 6 | Ask Dominic Hale to confirm the statements may be published. Wait for his yes. | A written yes. | From design: not yet seen |
| 7 | On the 5th working day, press publish in the portal. | The portal emails landlords. This cannot be undone. | Told |

## Checks after the run
| Check | Where to look | Good looks like | Bad looks like |
|---|---|---|---|
| Totals | Ledger report against the statements | Equal to the penny | Any difference at all |
| Count | Output folder | One PDF per landlord with rent due, 74 in October | Fewer than the previous month without a known reason |
| Published | Portal status page | All statements show "published" | Some "draft" |

## When it fails
| Symptom | Likely cause | Try first | Escalate when |
|---|---|---|---|
| Script stops with "missing management fee rate for property N" | The fees sheet has no rate for that property (happened last month at landlord 61 of 74, property 118) | Add the rate to the fees sheet, after asking the finance lead which rate applies, and re-run | The rate is unknown, or the error repeats |
| Totals do not match the ledger | Late payment entered after the export, or a wrong rate | Re-take the export and re-run | Still different: stop, tell Dominic Hale, do not publish |
| Script fails on a month with no export file | Not seen. Probably a missing file | Check the file name and folder | Cannot find an export in the accounts system |
| Portal rejects the upload or login | Not seen | Not known | Ask Mei Tan or the portal supplier through the contacts sheet |

The location of the fees sheet ("the finance folder") and the portal login steps were not seen. Mei to add them before leave.

## Rollback
Before publish: delete the draft PDFs in the portal and the output folder, then re-run from step 3. After publish: the emails cannot be recalled. Tell Dominic Hale at once; he decides whether to send a correction to landlords. Nobody else sends one.

## Who to call
| Order | Role or name | When | How |
|---|---|---|---|
| 1 | Mei Tan (until the 13th), then Jaswinder Gill | Any step is unclear | See "Finance contacts" in the team handbook |
| 2 | Dominic Hale, finance lead | Totals do not match, a rate is unknown, or publish is needed | Same sheet |
| 3 | Portal supplier support | Portal outage or login failure | Same sheet |

## Changes made to this runbook
| Date | Change | By |
|---|---|---|
| (draft) | First version from Mei's account, shell history and the 4 November observation | the agent |
