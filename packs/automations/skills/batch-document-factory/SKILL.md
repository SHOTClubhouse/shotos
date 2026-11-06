---
name: batch-document-factory
description: Makes one Google Doc or Slides file per sheet row from a master template using Apps Script, with dry run and sample first. Use when the same letters, quotes or certificates are needed for many people. Never sends or shares.
---

# Set up and run the batch document factory

Stage: Operate. Rules served: 1 Stop at the boundaries, 3 Read back the real result, and control 9 (pilot before scale). The script is `Code.gs` in the SHOTos repository at `packs/automations/scripts/batch-document-factory/`, or in `.shotos/packs/automations/scripts/batch-document-factory/` in a project where SHOTos is installed; read the README beside it first.

## When not to use this

- The documents must be emailed or shared as they are made. The script does neither; sending is a separate step for a person.
- The content is legal, medical or financial text that has not been approved as a template. Get the template approved first.
- It is a handful of documents. Make them by hand.
- The rows contain data about children or other sensitive people and nobody has said who may see the output folder. Settle access first.

## Steps

1. **Agree acceptance.** Name the owner, how many documents, what a correct document contains, and what must not happen (no sending, no sharing, no deleting). Use [template.md](template.md).
2. **Check the template.** Read it with the person. Every `{{placeholder}}` must match a sheet column. Tokens should be typed in one go. Look for text that varies per recipient but is not yet a placeholder. Ask who approved the wording.
3. **Check the data.** Look at the rows with the person: empty cells, duplicates, odd characters, anything that must not appear. Agree the banned terms and add them to the BannedTerms tab. A free-text column (notes, remarks, comments) is never merged into a letter on the strength of one request: say that it can carry private or sensitive remarks, have the owner read the non-empty rows, hold back or ban the risky ones, and run the sample of three first for the owner to confirm before any full run.
4. **Choose the output folder.** A copy inherits the folder's sharing. Recommend a private folder, and say so. `OUTPUT_FOLDER_ID` is required: a live run will not start without it.
5. **Person installs.** The agent cannot paste the script or approve permissions. Give the steps from the script README. Confirm `setupFactory` ran and the tabs exist.
6. **Dry run.** Run `dryRun`. Read the Report tab: template placeholders found, columns matched, rows blocked and why. Fix blocked rows and mismatches. Nothing is created.
7. **Sample of three.** Run `runSample`. Open each of the three documents in Drive.
8. **Read back the real result.** Check: every placeholder replaced with the right value for that row; layout and formatting intact; the name is right; no leftover braces; the row shows DONE with a link; the Report has one line per document. Compare against the source data, not just against the script's own check.
9. **Owner accepts the sample.** Show the three documents. If any is wrong, fix the template or data, clear `done` on those rows, and repeat the sample. Do not go on.
10. **Full batch.** Run `runBatch`. Expect it to stop and schedule a continuation if the batch is large. Check afterwards that the continuation trigger is gone (`removeContinuation` if not).
11. **Reconcile.** Count: rows, DONE, blocked, error. Run `auditDocuments`. Use `retryFailed` for errors, after reading why.
12. **Record and hand over.** Fill the template with counts and links. Tell the owner the documents exist and nothing has been sent; sending is theirs.

## Output

A filled [template.md](template.md): acceptance, template and data checks, dry-run result, sample evidence and final counts.

## Checks

- The dry run and the sample come before the full batch, always.
- Blocked rows are reported with their reason, not worked around.
- The agent never sends, shares, moves to the bin or deletes a generated document.
- Final counts add up: rows = done + blocked + error + not yet processed.
- The report says what was checked in the real documents and what was not.
