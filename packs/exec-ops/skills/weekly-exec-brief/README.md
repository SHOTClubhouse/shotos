# weekly-exec-brief

**A one-page weekly briefing built from evidence: what changed, what needs deciding, and how much of it is proven.**

The agent reads the week's ledger, notes and signals, lists changes with sources, puts decisions in front with a decision maker and date, and keeps recommendations apart from commitments. It lists what is unverified and which sources it could not read. A line repeated from the daily notes is not counted as a new commitment.

It serves the Check step. Rules: 3 Read back the real result, 4 Claim only what you can show.

## The problem it solves

The managing director of Harbourside Lettings gets a Monday summary that says "agreed to renew the insurance and to review the contractor". The first phrase came from a daily note that was only a reminder, and the second was the assistant's own suggestion. Both read as commitments, and one person is chased for something they never agreed.

With the skill, the renewal appears as a decision with a date, the contractor review appears under recommendations, and a note says the broker's portal could not be read.

## When to use it, and when not to

Use it for a regular leadership update. Skip it when nothing changed, or when the reader needs options and a recommendation on a single question (use [decision-brief](../decision-brief/README.md)).

## Who it is for

Executives, chiefs of staff, team leads and founders who report upward or to a team each week.

## How to use it

> Write this week's brief for me. Use the daily ledger, the meeting notes folder and the task board. Tell me what you could not read.

Output uses [template.md](template.md). Worked example: [input](../../examples/weekly-exec-brief/input.md) and [output](../../examples/weekly-exec-brief/output.md).

## How it connects

- **Reads:** the [daily-brief](../daily-brief/README.md) ledger and [meeting-notes](../meeting-notes/README.md) files.
- **Hands on:** open decisions go to [decision-brief](../decision-brief/README.md).
- **Evidence habits:** [report-with-evidence](../../../../skills/report-with-evidence/README.md).

## Needs

Document connector to read the ledger, notes and board. Calendar and mail connectors read-only, optional. If a source is not connected, the brief says so.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 1 of 2, Opus 1 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Make "unverified" a standing section, even when empty.
- Write commitments with a name and a date or leave them out.
- Keep it to one page; link to detail.

## Limits

- It cannot report what was never written down.
- External signals depend on the sources you give it; it does not search the whole web unless you ask.
- Judging importance is yours; the agent proposes, you edit.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/weekly-exec-brief/input.md), [example output](../../examples/weekly-exec-brief/output.md).
