---
name: daily-brief
description: "Runs the pull-based daily loop: reconciles a ledger with fresh mail and calendar and writes one digest. Use for a morning brief or evening close. Sends nothing; repeated accepted drafts may earn a higher automation rung only with the owner's approval."
---

# Daily brief

Pull the signal when the owner asks or on a set schedule, update one ledger, and report only what needs a person. Silence beats noise: a day with nothing to decide gets a short digest, not a long one.

Step: Build. Rules: 1 Stop at the boundaries, 3 Read back the real result, 4 Claim only what you can show.

## When not to use this

Skip it for a one-off question about a single thread or date, or when there is no ledger and the owner does not want one. In that case offer to start the ledger from [ledger-template.md](ledger-template.md) and stop.

## Steps

1. **Confirm scope.** Name the owner, the mail account and the calendar in scope, and the run (morning or evening). If any is unclear, ask once.
2. **Load the ledger.** Read the existing ledger in place. Never create a second copy. If none exists, create it from the template and say so.
3. **Gather fresh signal.** Read mail and calendar since the ledger's "last run" time. Filter out the owner's own automated mail (their scripts, digests, receipts they generate and notifications from their own systems), so the loop does not feed on itself. Note any source that was unavailable.
4. **Reconcile in place.** For each ledger row, mark it done, moved (new date), slipping, or unchanged, citing the message or event that shows it. Add new obligations the signal creates, each with a source. A date mentioned only in passing is a candidate, not a row, until the owner confirms.
5. **Draft what needs drafting.** Write replies or reminders as drafts in the mail account or the digest. Never send. Use the real thread, not a guess at it.
6. **Build the digest.** Use [digest-template.md](digest-template.md). Include only four things: decisions needed, things slipping, today's fixed points, drafts ready to review. Leave a section out when it is empty. If all four are empty, say "Nothing needs you today" and list the sources read.
7. **Read back.** Re-open the ledger and confirm the changes landed and the "last run" time moved. Report any source that failed.
8. **Offer graduation, never assume it.** If a task class inside the loop (for example "draft routine meeting confirmations") has been accepted unedited many times, suggest a rung change under `rules/12-graduation.md` (in the SHOTos repository, or `.shotos/rules/12-graduation.md` where SHOTos is installed). Until the owner agrees, every class stays at rung 1: draft only.
   A request to make the daily brief automatic or to send replies without review is a graduation question, not a shortcut. State the current rung, the acceptance evidence needed to earn the next rung and the owner's approval point.

## Output

The reconciled ledger (updated in place) and one digest, both using the templates in this folder.

## Checks

- The digest lists only items that need a person, each with the evidence that raised it.
- Every ledger change cites a message, event or the owner's word.
- The owner's own automated mail did not create or close any row.
- No message was sent, no event created or changed, nothing deleted.
- Unavailable sources are named, not skipped silently.
