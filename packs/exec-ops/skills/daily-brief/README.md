# daily-brief

**A pull-based daily loop that keeps a ledger of dated obligations current and tells you only what needs you.**

The agent loads your ledger, reads fresh mail and calendar (ignoring your own automated mail), updates the ledger in place, drafts what needs drafting and writes one digest. It lists decisions, slipping items, today's fixed points and drafts to review. It sends nothing.

It serves the Build step. Rules: 1 Stop at the boundaries, 3 Read back the real result, 4 Claim only what you can show.

## The problem it solves

The founder of Harbourside Lettings has a landlord insurance renewal on the 14th, a promise to send a tenant survey result by Thursday and a board call the same day. Each lives in a different inbox thread. Last month the renewal date slipped because a reminder was buried under 40 automated rent-collection notices that her own system sends her.

With the skill, the agent filters those notices out, sees the broker thread, marks the row as slipping and puts a drafted reply to the broker at the top of a short digest.

## When to use it, and when not to

Use it once or twice a day, or whenever dated obligations are at risk of slipping. Skip it for a single question about one thread, or if you do not want a ledger.

## Who it is for

Founders, executives, chiefs of staff and anyone with more commitments than a calendar shows.

## How to use it

> Run my morning brief. Ledger is in the Operations folder, mail account is my work one, calendar is the main one.

You get an updated ledger and a digest on [digest-template.md](digest-template.md). Start a ledger from [ledger-template.md](ledger-template.md). Worked example: [input](../../examples/daily-brief/input.md) and [output](../../examples/daily-brief/output.md).

## How it connects

- **Feeds:** [weekly-exec-brief](../weekly-exec-brief/README.md) reads the ledger, and [inbox-triage](../inbox-triage/README.md) handles mail in depth.
- **Autonomy:** any task class that should run without review earns it through [rules/12-graduation.md](../../../../rules/12-graduation.md).
- **Boundaries:** [docs/controls.md](../../../../docs/controls.md).

## Needs

Mail connector (read, create drafts), calendar connector (read), document connector (read and write the ledger). Read-only first. Without connectors, paste the signal in and the agent says what it could not read.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 1 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 0 of 2, Sonnet 1 of 2, Opus 0 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Keep one ledger, edited in place.
- Run it at set times. Pulling on demand beats a feed that interrupts you.
- A quiet digest is a good digest.
- Do not let the loop read mail that your own scripts generate; it will log its own output as new work.

## Limits

- It only knows what mail and calendar show. A promise made in a corridor is not in the ledger until you add it.
- Date extraction from free text can be wrong; the digest cites the source so you can check.
- It does not enforce the no-send rule in a tool; keep send permission off.

Files: [SKILL.md](SKILL.md), [ledger-template.md](ledger-template.md), [digest-template.md](digest-template.md), [example input](../../examples/daily-brief/input.md), [example output](../../examples/daily-brief/output.md).
