# cross-agent-review

**A lead agent does the work and an independent reviewer from a different model or runtime checks it against the same card. Then a person decides.**

Both agents get the same acceptance card and evidence. The reviewer reports findings with evidence, the lead responds to each, and the owner decides. When the two agents agree, that is not permission.

It belongs to the Build step. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show. The detail is in [rules/07-independent-review.md](../../rules/07-independent-review.md).

## The problem it solves

Harbourside Lettings has an agent draft a rent-increase letter and a spreadsheet of new rents for 64 tenancies. The same agent then checks its own work and reports "all correct". Two tenants are given an increase above the cap in their agreements. The agent could not see the error because it made the error with the same assumptions it used to check.

## What the agent does differently

The lead's work goes with the acceptance card and the source data to a reviewer on a different runtime. The reviewer recomputes the rents from the agreements and reports two rows over the cap, with the clause quoted. The lead fixes them and the reviewer rechecks. The reviewer also says it could not check the legal wording of the letter. The owner reads both reports and decides. See [examples/cross-agent-review/output.md](../../examples/cross-agent-review/output.md).

## When to use it, and when not to

Use it for medium and high risk work and for anything that goes outside the team. Skip it for low-risk, easily reversed work.

## Who it is for

- **Owner or manager:** a second opinion that is not an echo.
- **Team using more than one AI tool:** a defined way to use them together.
- **Anyone approving agent work:** a record of what was checked and what was not.

## How to use it

> Have the rent-letter work reviewed by a different agent. Give it the acceptance card and the tenancy data. Read-only. I will decide after I see both reports.

## How it connects

- **Before:** [route-the-work](../route-the-work/README.md) decides when a review is needed, and [agree-acceptance](../agree-acceptance/README.md) supplies the card.
- **After:** [report-with-evidence](../report-with-evidence/README.md) and [evidence-handoff](../evidence-handoff/README.md).
- **Rules:** [docs/controls.md](../../docs/controls.md).

**Needs:** A second agent on a different model or runtime, for example a second tool installed beside the first. If only one is available, the skill says so and uses a fresh session with a weaker-check note.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 1 of 2, Opus 1 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Do not tell the reviewer what you think the answer is.
- Ask for what the reviewer could not check. That list is as useful as the findings.
- Give a finding without evidence back to the reviewer.

## Limits

- Two models can be wrong in the same way. Review reduces risk; it does not remove it.
- It costs a second run. Use it where the risk repays that.
- The reviewer has read-only access by default. The skill relies on that being set; it does not enforce it.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/cross-agent-review/input.md) and [output](../../examples/cross-agent-review/output.md).
