---
name: meeting-notes
description: Turns new meeting recordings or transcripts into structured notes, tracked in a ledger, with a rolling file per person or organisation. Use when catching up on meetings or processing recordings. Drafts only; never sent to attendees.
---

# Meeting notes

Convert new recordings into notes that stay useful, and never process the same recording twice or lose one silently.

Stage: Track. Rules: 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Read the agenda and source transcript or notes. Verify names, commitments and dates against the source, and mark disputed or missing details.

Use `decision-record` for a material decision and link to the original meeting record.

## When not to use this

Skip it for a live meeting that has no recording yet, for a request to publish or send notes to attendees (draft only; the owner sends), and for recordings the owner has marked private.

## Steps

1. **Open the ledger.** Read the processed-recordings ledger in place ([ledger-template.md](ledger-template.md)). Read the last completed coverage checkpoint. If the legacy watermark is the latest processed recording, recheck that boundary and any recorded gaps before treating coverage as complete. On the first run, record the agreed source and start.
2. **List recordings in scope.** Set a cutoff with its timezone and list the approved source from the checkpoint through the cutoff, including the boundary timestamp and earlier known gaps. Match by stable recording ID, not title or time. A partial page or a pasted transcript with no inventory can support a note, but cannot establish complete coverage. Leave private recordings outside the processing scope.
3. **Skip short recordings.** Recordings under the agreed length (default 3 minutes) are logged as "skipped, too short" with their length. They are not processed and not deleted.
4. **Read the transcript first.** Use the full transcript as the record of what was said. Use the calendar entry only for context: title, attendees, organisation. Do not fill gaps in the transcript from the calendar.
5. **Confirm identity.** Before naming anyone, check who spoke: use self-identification, a verified speaker map or the owner's confirmation. A calendar attendee list can suggest a match but does not identify a speaker. If a speaker is unclear, write "unidentified speaker" and ask. Never guess a name or an organisation.
6. **Write the notes** using [template.md](template.md): purpose, decisions, actions with owner and date where stated, open questions, and anything said that conflicts with earlier notes.
7. **Update the rolling file.** One file per person or organisation: a short **standing position** at the top (what they want, what is agreed, what is open), then one dated entry per recording ID, newest first. Before retrying, find any output already written for that ID. Reuse or reconcile the same entry and avoid appending a duplicate. Update the standing position only from verified notes.
8. **Verify, then record coverage.** Read back the per-meeting note and rolling entry, and check names, numbers, dates and actions against the transcript. Mark that ID processed only after verification. Keep inaccessible transcripts, material identity questions and failed writes as pending with their reasons. Read back the ledger. Advance the checkpoint only after the source listing is complete and every in-scope ID is verified or explicitly skipped under the agreed rule. Otherwise retain the checkpoint and report where to retry. See the [retry example](retry-example.md).
9. **Stop at the boundary.** Sending notes to attendees or creating tasks elsewhere needs the owner's yes.

## Output

Per-meeting notes, the updated rolling file and the updated ledger.

## Checks

- The retry matches stable IDs. An incomplete listing or pending recording keeps the last completed coverage in place.
- Short recordings were logged as skipped.
- No person or organisation was named without confirmation.
- Notes match the transcript; calendar data is labelled as context.
- A processed row has a checked note and rolling entry. Ledger edits were read back.
