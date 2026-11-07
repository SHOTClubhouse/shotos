# Batch document factory (Apps Script)

**Makes one Google Doc or Slides file per row of a sheet, filled from a master template, and records every decision.**

It creates copies of your template and fills them. It does not send, share or delete anything. A copy that fails is renamed with a `FAILED - ` prefix and kept.

## What it does

1. Reads the **Rows** tab: one row per document you want.
2. Finds the `{{placeholders}}` in your template. Each placeholder needs a column with the same name in Rows.
3. For each pending row it checks for empty values, banned terms and values containing placeholder text such as `{{client}}`. A failing row is blocked before any document is made. The report lists the affected columns. Replace placeholder-shaped values with plain text before retrying.
4. Copies the template into your output folder, replaces every placeholder in **one atomic update** (every tab of a Doc, every slide of a deck), then reads the document back and confirms no placeholder is left.
5. Writes the result into the row (done marker, document link, attempt count) and a line in the **Report** tab.

## Files

- `Code.gs`: the script. Configuration is at the top.
- `appsscript.json`: the manifest, which enables the Docs and Slides services.

## Setup

Time: about 15 minutes.

1. Make the master template as a Google Doc or Slides file. Write placeholders such as `{{client}}` and `{{start_date}}`. Type each one in a single go, without changing the formatting in the middle of it.
2. Create a Google Sheet. Open **Extensions > Apps Script**. Paste `Code.gs`. In **Project Settings**, show the manifest file and paste `appsscript.json`.
3. In **Project Settings > Script Properties**, add `TEMPLATE_ID` (the long ID in the template's URL) and `OUTPUT_FOLDER_ID` (the ID of a private Drive folder for the copies). `OUTPUT_FOLDER_ID` is required: a live run refuses to start without it, and a dry run warns that copies inherit the folder's sharing.
4. Run `setupFactory`. Approve permissions. It creates the Rows, BannedTerms and Report tabs and adds the control columns.
5. In **Rows**, add one column per placeholder (header `client` fills `{{client}}`), then one row per document.
6. Optional: set `NAME_PATTERN` in `CONFIG` (for example `Welcome pack {{client}}`), or fill the `doc_name` column.
7. Add any terms that must never appear to the **BannedTerms** tab.

## Columns the script manages

| Column | Meaning |
|---|---|
| `doc_name` | Optional name for the document. |
| `done` | `DONE` once a document is made. DONE rows are never touched on a rerun. |
| `status` | `ok`, `blocked` or `error`. |
| `doc_id`, `doc_url` | The generated document. |
| `attempts` | Failed or completed attempts. A row stops at `MAX_ATTEMPTS` (3) until you run `retryFailed`. |
| `copy_state` | `retry` while the row's `doc_id` is a copy that is not yet filled and checked; `complete` once it is. This is how a retry is told apart from a redo. |
| `previous_doc_ids` | Earlier documents for this row, kept, never deleted. |
| `last_message`, `done_at` | Last result and time. |

## Run order

| Function | Effect |
|---|---|
| `dryRun` | Checks the template, columns, empty values and banned terms. Creates nothing. |
| `runSample` | Makes documents for the first three pending rows. Read them before going on. |
| `runBatch` | Processes all pending rows in time-boxed batches. |
| `retryFailed` | Resets and retries only unfinished rows in error. If the time limit is reached, run it again for the remaining errors. |
| `auditDocuments` | Checks every DONE row still has a document that is not in the bin. |
| `removeContinuation` | Removes a waiting continuation trigger. |

When a batch runs out of time (4.5 minutes) it creates a one-off trigger to continue in about a minute. Each run deletes any old continuation trigger first, and when no rows are left no new one is made.

## Redoing a row

To make a row's document again, clear its `done` cell. Because `copy_state` is `complete`, the script makes a new copy and records the old document in `previous_doc_ids`. It does not alter or delete the old one, and it never refills a finished document.

When an attempt fails after the copy was made, the copy's id is saved on the row (`status` `error`, `copy_state` `retry`) and the copy is renamed `FAILED - <name>`. The next attempt (after `retryFailed`, or once the cause is fixed) fills that same copy and removes the prefix on success. If that copy has been binned, a fresh one is made and the old id goes to `previous_doc_ids`.

If a verified document exists but the row update fails, the run stops with `receipt-error`. Open the logged document and check the row before rerunning. If its values and link match the verified copy, reconcile the row's receipt and mark it DONE. If they differ, leave the old copy intact and resolve which input revision should be used before regenerating.

If you upgrade from an earlier version, run `setupFactory` once to add the `copy_state` column.

## Safety notes

- **Sharing is inherited.** A copy made inside a shared folder is visible to everyone who can see that folder. Use a private output folder until you have checked the documents.
- **Literal report text.** A document name or diagnostic message beginning with an equals sign stays text in the sheet.
- **Blocked is not failed.** A blocked row waits for you to fix the sheet. Fix the value and run again.
- **Sample documents are real.** Rows made by `runSample` are marked DONE. If they are wrong, clear `done` on those rows after fixing the template or data.
- **Banned-term check** matches whole words, ignoring case, in the document name and every placeholder value. It checks your data, not the template wording.
- **Read-back** checks every tab of a Doc (body, headers, footers, footnotes), or the slides of a deck, for leftover placeholders. For slides it ignores layouts, masters and speaker notes, and the replacement skips them too, so a placeholder there is neither filled nor flagged. Put placeholders on the slides themselves. It cannot judge whether the content is right; a person reads the sample.

## Limits and honest caveats

- Apps Script has quotas for running time (six minutes per run), Drive copies and API calls. Large batches rely on the continuation trigger.
- Placeholders split by formatting in the template are found, but a placeholder containing double braces inside another is not supported.
- The script has been syntax-checked and its text functions tested outside Google. It has not been run in a live account by the author, so the dry run and sample are your real test.
