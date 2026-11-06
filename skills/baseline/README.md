# baseline

**Write down how things are today, with the source of each number, before you change anything.**

This skill makes the agent record the current value of each measure that matters, where the value came from and what period it covers. Where there is no data, it writes "not measured" and says how to find out. It never fills a gap with a quiet guess.

It belongs to the Brief step. It serves rule 4, Claim only what you can show, and rule 3, Read back the real result, because a later result can only be read against a real before.

## The problem it solves

Northgate Cycles, a small online bike shop, wants to cut the time it takes to answer customer emails. The owner says replies "take about a day". Nobody has checked. After a month of using an AI drafting tool, the owner says replies are now "much quicker" and wants to roll it out to the returns inbox. There is no before figure, so there is no way to know whether anything changed.

## What the agent does differently

It finds what exists (the helpdesk export has first-reply times for the last 60 days), records that, and writes "not measured" for the returns inbox, which has no timestamps. It offers the cheapest way to fill that gap and leaves the decision to the owner. See [examples/baseline/output.md](../../examples/baseline/output.md).

## When to use it, and when not to

Use it before any change you will later call better or worse. Skip it for a single task with no comparison afterwards.

## Who it is for

- **Business owner:** gets a before figure to hold the result against.
- **Operations or product lead:** avoids debating whose memory is right.
- **Anyone approving spend:** sees which claims rest on data.

## How to use it

> We are about to start using AI drafts for customer emails. Record the baseline first. Use the helpdesk export in `data/helpdesk-export.csv` and say what we do not have.

Read the table, decide what to do about each gap, and confirm it.

## How it connects

- **Before:** [stakeholder-map](../stakeholder-map/README.md) shows who decides what counts as better.
- **After:** [hypothesis-card](../hypothesis-card/README.md) sets a target against this baseline, and [report-with-evidence](../report-with-evidence/README.md) reports against it.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent. If a data export is used, the agent needs read access to that file.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Two or three honest measures beat ten doubtful ones.
- Keep the definition with the number ("calendar hours from first customer message to first human reply").
- A guard measure protects against winning on speed by losing on quality.

## Limits

- The agent can only read what you give it. It cannot verify that a source is itself correct.
- A short baseline window can mislead if the period was unusual.
- The skill does not collect new data on its own.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/baseline/input.md) and [output](../../examples/baseline/output.md).
