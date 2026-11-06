# progress-wrap-up

**Report each week by what can be shown: an evidence ledger that says whether every win is live, gated, merged only or unverified.**

The agent defines the week, reads meetings, documents, code history and releases, and writes one ledger row per claimed win with its date, source, status, why it matters and the ask. It ends with specific asks that name a person and a date. There is one dated issue per week, edited in place.

It supports Operate and Track. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

At a fictional firm, Northgate Cycles, the Monday update said "online booking is done". On Tuesday a customer could not find it. It was merged, but behind a switch the owner had not turned on. The update had not lied, but it had let the owner believe customers had it.

With a ledger, that row reads "Online booking, merged and gated behind the booking flag; Dev to ask the owner to switch on by Thursday". The owner sees the real state and the ask.

## When to use it, and when not to

Use it every week of a project and before any update that claims progress. Skip it for a single incident or a final report; use [evidence-pack](../evidence-pack/README.md) for the latter.

## Who it is for

- **Sponsor or business unit leader:** a status you can trust without asking again.
- **Small team lead:** one routine for the Monday update.
- **Engineering or practice lead:** separates merged from released from used.
- **Product owner:** a clear list of what is waiting on a decision.

## How to use it

Ask:

> Write this week's progress wrap-up for the booking project: Monday 20 to Sunday 26 October. Use the meeting notes folder, the repository and the release log. Draft only.

Check each status against what you know, then post it yourself.

## How it connects

- **Before:** [report-with-evidence](../report-with-evidence/README.md) covers a single piece of work. [evidence-handoff](../evidence-handoff/README.md) records what passed.
- **After:** [evidence-pack](../evidence-pack/README.md) rolls the weeks into a decision. [retrospective](../retrospective/README.md) looks back across them.
- **Related:** [delivery-metrics](../delivery-metrics/README.md) supplies trends. Claims follow [docs/claims.md](../../docs/claims.md).

## Needs

Read access to meeting notes, documents, the repository and the release log. The skill drafts; a person posts.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Look at the real home before calling something live.
- Keep gated visible. It is progress, and it is also a decision waiting for someone.
- Five asks at most, each with a name and a date.
- Edit the week's issue in place; do not start a second one.

## Limits

- The agent cannot see systems it has no access to; those rows stay unverified.
- A clean ledger can hide the wrong work. It shows state, not value.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/progress-wrap-up/input.md) and [output](../../examples/progress-wrap-up/output.md).
