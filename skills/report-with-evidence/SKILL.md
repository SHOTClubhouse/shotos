---
name: report-with-evidence
description: "Ends a task that changed something with a short report and Claims block: what was done, how to check it, what was only planned or unchecked. Use when saying something is done, fixed, sent, deployed or passing."
---

# Report with evidence

An agent's report is evidence, not narration. Say what you checked, what you could not check and what you are assuming.

## Context and handoff

Read the saved output and run results before drafting a completion claim. Check receipts for external actions and mark unchecked claims.

Use `evidence-handoff` if work passes to another owner. Keep the Claims block with the task outcome.

## Steps

1. **Check the work in its real home before reporting.** Open the file you wrote. Run the tests you say pass. Look at the commit you say you made. Do not report from memory of what you intended.
2. **Write a short summary for the reader.** Put the result first, in plain words, then anything they must decide or do.
3. **End with a Claims block.** One line per claim, in this form:

   ```
   ## Claims
   - [file] created: path/to/file
   - [file] changed: path/to/file
   - [file] deleted: path/to/file
   - [command] passes: the exact command
   - [git] committed: HEAD
   - [git] pushed: branch-name
   - [external] sent: what and to whom | receipt: path/to/receipt
   - [unverified] anything you did not or could not check
   ```

4. **Use the right state.** Work can be *installed* (present), *executed* (run and checked) or *accepted* (a person said yes). Only a person can accept. Never write that work is accepted, approved or signed off unless you hold the record, and attach it as a receipt.
5. **Be honest about gaps.** Anything you could not verify goes on an `[unverified]` line. An honest gap passes. A confident claim with no evidence fails.
6. **Run claim-check if it is installed.** `python .shotos/tools/claim_check.py report.md` (or `tools/claim_check.py` in the SHOTos repository), or let the Stop hook run it. Fix the work or the report until it passes.

## What not to do

- Do not say "done", "all tests pass" or "sent" in the summary without a matching claim.
- Do not claim an external action (email, post, deploy, share) without a receipt such as a message ID, a URL or a log saved in the project.
- Do not mark work accepted for someone.
