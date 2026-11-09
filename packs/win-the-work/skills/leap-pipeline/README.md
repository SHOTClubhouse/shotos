# leap-pipeline

**Run a pipeline through Lead, Explore, Agree and Plan, flag stalled deals with evidence, and hand won work over to Scope.**

The agent reads your pipeline, keeps the recorded stage and evidence assessment visible together, produces a pipeline table, runs a weekly review that names stalled deals with dates and counts, and prepares a handover packet once the agreement is verified.

It can be used at any SHOTos stage and hands over into **Scope**. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

The owner of Harbourside Lettings, a small property agency, sells a managed-services contract to landlord groups. Her spreadsheet says nine deals are "hot". Three of them have not had a reply in three weeks, and one has a proposal that nobody has confirmed was read. When one deal is won, the person who will deliver it learns the terms from a forwarded email chain and misses a promise made in the second meeting.

## When to use it, and when not to

Use it to set up a pipeline, to review deals weekly, to decide whether a deal can move stage, or to hand over a won deal.

Do not use it for a one-day enquiry, or to forecast revenue. A pipeline table shows evidence; it does not predict.

## Who it is for

- Founders and sales leads who run a pipeline by hand.
- Account managers who inherit deals and need the history.
- Delivery leads who receive the handover.

## How to use it

> Here is our pipeline export. Place each deal in the LEAP stages, flag anything stalled with the evidence, and tell me which deal I can honestly move to Agree this week.

You get a table, a short review and, for any verified agreement, a handover packet using [template.md](template.md). Use the [stage review example](stage-review.md) to check how a stage label and a signed agreement are handled. The pipeline owner reviews any proposed changes.

## How it connects

- **Alongside:** [nudge-qualify](../nudge-qualify/README.md) scores a deal during Explore and Agree; [relationship-map](../relationship-map/README.md) shows who is connected to whom.
- **Drafting:** [contextual-proposal](../contextual-proposal/README.md) and [email-reply](../email-reply/README.md) write the proposal and the replies.
- **After:** the handover packet starts SHOTos Scope; see [capture-the-problem](../../../../skills/capture-the-problem/README.md) and [agree-acceptance](../../../../skills/agree-acceptance/README.md).
- **Rules:** [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent. Read access to a CRM export or spreadsheet helps. The skill does not write to it.

## Tips

- Set the stalled threshold yourself; 14 days suits some sales cycles and not others.
- Ask for the criteria check on any deal before you tell your team it has moved.
- Put the handover packet in front of the delivery owner and let them mark it accepted.

## Limits

- The agent can only see what is in the pipeline source. A conversation that was never written down does not count as evidence.
- Values are as reliable as the person who entered them.
- The skill proposes stage changes. It does not make them.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/leap-pipeline/input.md) and [output](../../examples/leap-pipeline/output.md).
