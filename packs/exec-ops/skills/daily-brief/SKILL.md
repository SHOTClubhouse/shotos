---
name: daily-brief
description: "Runs the pull-based daily loop: reconciles a ledger of dated obligations with fresh mail and calendar and writes one digest of what needs a person. Use for a morning brief, evening close or \"what needs me today\". Sends nothing."
---

# Daily brief

Pull the signal when the owner asks or on a set schedule, update one ledger, and report only what needs a person. Silence beats noise: a day with nothing to decide gets a short digest, not a long one.

Stage: Operate. Rules: 1 Stop at the boundaries, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Start with today’s calendar, actual deadlines, inbox changes and yesterday’s unresolved priorities. Mark gaps in source access.

Use `leaders-inbox` for decisions that need routing. Keep one dated brief with links to owning tasks.

## Start here

**Minimum to start:** owner, mail account, calendar and run type. **First output:** the digest with a Coverage line (complete or partial) and what was actually read, even if a source failed. **Uncertain:** a date mention or unread source stays a candidate or gap, never a closed row. **Handoff:** lead with the decisions needed, each with who decides, the evidence and what slips if it waits; route routing questions to `leaders-inbox`.

## When not to use this

Skip it for a one-off question about a single thread or date, or when there is no ledger and the owner does not want one. In that case offer to start the ledger from [ledger-template.md](ledger-template.md) and stop.

## Steps

1. **Confirm scope.** Name the owner, the mail account and the calendar in scope, and the run (morning or evening). If any is unclear, ask once.
2. **Load the ledger.** Read the existing ledger in place. Treat its last completed coverage as the start of this run. Older ledgers may call it “Last run”. For a first run, record the agreed starting point and create the ledger from the template.
3. **Read one bounded window.** Record a cutoff with its timezone before reading. Read mail and calendar changes since the saved start through the cutoff. Read today's current appointments for the digest. Filter the owner's automated mail out of the obligations. Treat an unavailable source, truncated results, or a pasted sample with unknown coverage as incomplete. Report what was actually read.
4. **Reconcile in place.** Match by the obligation and source thread or event before adding a row. Apply only changes supported by a source you read. Reopening the same window must update the same row. Missing source access cannot close, move or confirm a row. A passing date mention stays a candidate until the owner confirms.
5. **Draft what needs drafting.** Use the real thread. If coverage is incomplete, leave the drafts in the digest. On a complete run, reuse an existing matching mail draft where available, or leave the draft in the digest when you cannot check for a duplicate. Never send.
6. **Build the digest.** Use [digest-template.md](digest-template.md). List decisions needed, things slipping, today's fixed points and drafts to review. Omit empty sections. If coverage is incomplete, label the brief partial even when the available sources show no items.
7. **Read back and save coverage.** Reopen the ledger and verify the changes. Advance the coverage to the cutoff only when both sources covered the window and the ledger reconciliation is verified. Read back the saved timestamp. On a partial run keep the previous completed coverage, name the missing source and retry from that same point.
8. **Offer graduation, never assume it.** If a task class inside the loop (for example "draft routine meeting confirmations") has been accepted unedited many times, suggest a rung change under `rules/12-graduation.md` (in the SHOTos repository, or `.shotos/rules/12-graduation.md` where SHOTos is installed). Until the owner agrees, every class stays at rung 1: draft only.

## Output

The reconciled ledger (updated in place) and one digest, both using the templates in this folder.

## Checks

- The digest lists only items that need a person, each with the evidence that raised it.
- Every ledger change cites a message, event or the owner's word.
- The owner's own automated mail did not create or close any row.
- No message was sent, no event created or changed, nothing deleted.
- A partial or unverified run leaves the previous completed coverage in place. Retrying matches existing rows and drafts. See [the recovery example](recovery-example.md).
