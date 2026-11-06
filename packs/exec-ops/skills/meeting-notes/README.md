# meeting-notes

**Turn new recordings into verified notes, with a watermark ledger and one rolling file per person or organisation.**

The agent reads only recordings newer than the ledger's watermark, skips very short ones, reads the transcript before the calendar, confirms who is who before naming anyone, and updates a rolling file with a standing position and a dated entry per meeting. It marks a recording processed only after checking the output and reading the ledger back. It works with any transcript source, including pasted text.

It serves the Track stage. Rules: 3 Read back the real result, 4 Claim only what you can show.

## The problem it solves

A consultant at Northgate Cycles records supplier calls. A catch-up run last month processed the same call twice, named the wrong supplier because the calendar title said so, and overwrote the ledger, so nobody knew which calls were done.

With the skill, the watermark prevents reprocessing, the speaker is checked against what was said aloud, and the ledger is edited in place and read back before anything is marked done.

## When to use it, and when not to

Use it to catch up on recordings or process a transcript. Skip it for a meeting with no recording, and do not use it to send notes to attendees; it drafts and you send.

## Who it is for

Executives, account leads, consultants and anyone who talks to people for a living.

## How to use it

> Process my new meeting recordings since the last run. Use the ledger in the Meetings folder, and tell me who you could not identify.

Output uses [template.md](template.md); the ledger starts from [ledger-template.md](ledger-template.md). Worked example: [input](../../examples/meeting-notes/input.md) and [output](../../examples/meeting-notes/output.md).

## How it connects

- **Feeds:** [weekly-exec-brief](../weekly-exec-brief/README.md) and [advisory-session](../advisory-session/README.md) read the rolling files.
- **Actions:** move agreed actions to the [daily-brief](../daily-brief/README.md) ledger once the owner confirms them.

## Needs

A transcript connector (list recordings with start times and lengths, return transcripts) or pasted transcripts. A calendar connector for context, read-only. A document connector to keep the ledger and rolling files.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 1 of 2, Opus 2 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Keep the minimum length setting visible in the ledger.
- Never fix a bad ledger by deleting it; correct the rows.
- Treat the calendar title as a hint, not a fact.

## Limits

- Transcript quality limits note quality. Names and numbers can be misheard; the agent flags doubt rather than correcting from memory.
- It cannot judge tone or what was meant, only what was said.
- Verification is by the agent against the transcript; an independent check is yours to request for sensitive meetings.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [ledger-template.md](ledger-template.md), [example input](../../examples/meeting-notes/input.md), [example output](../../examples/meeting-notes/output.md).
