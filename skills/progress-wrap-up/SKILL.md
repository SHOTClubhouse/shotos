---
name: progress-wrap-up
description: Writes the weekly progress wrap-up on an evidence ledger, classing each claimed win as live, gated, merged only or unverified, and ending with asks. Use when reporting weekly progress to a sponsor or team. Final results go to evidence-pack.
---

# Write the weekly progress wrap-up

Report the week by what can be shown, not by what was said. Every claimed win goes into a ledger with a status, so a reader can tell what users can use today from what is only built.

Step: Build and Check. Rules: 3 Read back the real result, 4 Claim only what you can show.

## When not to use this

Skip it for a one-off incident report or a final evidence pack ([evidence-pack](../evidence-pack/README.md)). Do not use it to make the week sound better than it was.

## Steps

1. **Define the window.** Write the dates (for example Monday 00:00 to Sunday 23:59) and the time zone. Use the same window every week with no gaps or overlaps. Find last week's wrap-up and carry its open items forward.
2. **Collect from the sources.** Read meeting notes, documents, the code history (merges, tags), the release log and the tracker for that window. Note every source you could not open. Collect claims as the sources state them, including "it's done" statements from people.
3. **Turn each claim into a ledger row.** One row per win: the claim, its date, the source, the status, why it matters to the reader and the ask. Merge duplicates reported in several places.
4. **Classify the status by looking, not by the label.**
   - Live: users or the intended audience can use it now, and you saw it in its real home (the live site, the production release, the sent message) or have a receipt.
   - Gated: built and working, but behind a flag, a staged rollout or an approval that has not been given. Name the gate and who opens it.
   - Merged only: the change is in the main branch or the document is final, but it has not been released or shown in use.
   - Unverified: it is claimed, but you cannot see evidence. Say what evidence would settle it.
5. **Never upgrade a status on someone's word.** A person saying "it's live" gives you a claim; the evidence gives you a status. If a release was planned for the window and has no log entry, it is merged only or unverified.
6. **Add what slipped and what changed.** List planned items not done, with a reason if known, and risks that appeared. Compare with last week's asks: which were answered?
7. **End with specific asks.** Each ask names a person, a decision or action, and a date: "Priya to approve the pricing page flag by Thursday", not "needs review". Cap the list at five. If an ask needs spending, sending or publishing, say so; the agent does not do it.
8. **Publish in one place, one issue per week.** Use a single dated issue or page per week, for example titled with the week-ending date. Edit it in place when corrections come in and add a short "changed since first posted" line. Do not post a new issue for a correction. Drafting only: a person posts or sends it.

## Output

Use [template.md](template.md). Open with a three-line summary: how many wins are live, gated, merged only and unverified, and the asks. Keep the ledger table the main body.

## Checks

- The window is stated and matches last week's end date.
- Every ledger row has a source and a status from the four allowed.
- No row is marked live without evidence seen in its real home or a receipt.
- Asks name a person and a date and are five or fewer.
- A correction edits the existing issue instead of creating another.
