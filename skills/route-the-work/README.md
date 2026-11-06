# route-the-work

**One line before any task: what is being made, why, how risky, for whom, who does it and how it will be checked.**

The agent writes a route line with six parts: asset, job, risk, reader, route and proof. It picks direct work, a skill, a role agent or an independent reviewer to match the risk, and adds a risk tag only when it can point to evidence.

It belongs to the Operate stage but is useful at any point. It serves rule 1, Stop at the boundaries, and rule 4, Claim only what you can show. The detail is in [rules/01-route-the-work.md](../../rules/01-route-the-work.md) and [rules/02-evidence-based-risk.md](../../rules/02-evidence-based-risk.md).

## The problem it solves

Northgate Cycles asks its agent for two things in one morning: fix a typo on the delivery page, and send a "we got your order wrong, here is a refund" message to 38 customers. Without a route, the agent treats both the same way. It either asks five questions about the typo or sends the refund messages after a quick glance.

## What the agent does differently

For the typo it writes a direct, low-risk line and does it. For the refund message it writes `money` and `external` tags, each with its evidence (a refund amount in the file, 38 customer email addresses), picks an independent reviewer, and names the first yes it needs: the owner's, before anything is sent. See [examples/route-the-work/output.md](../../examples/route-the-work/output.md).

## When to use it, and when not to

Use it at the start of any task that produces something other people will rely on. Skip it for a quick factual answer or an edit the person sees at once.

## Who it is for

- **Anyone briefing an agent:** gets the right amount of care without asking for it each time.
- **Team lead:** can see at a glance why work was routed as it was.
- **Reviewer:** knows what they are checking and why.

## How to use it

> Route this before you start: tidy the delivery page typo, and draft the refund note for the 38 customers in `data/wrong-orders.csv`.

Read the lines. Change a route if you disagree, and give the yes where one is asked for.

## How it connects

- **Next:** [agree-acceptance](../agree-acceptance/README.md) for the checks, [cross-agent-review](../cross-agent-review/README.md) for medium and high risk, [pilot-before-scale](../pilot-before-scale/README.md) for work on many items.
- **Rules:** [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 1 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 2 of 2, Opus 1 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Keep the line short enough to read in ten seconds.
- A risk tag with no evidence beside it is a guess. Delete it or find the evidence.
- Writing "Reader" forces the question of who will act on the result.

## Limits

- The route is advice from the agent. It does not enforce itself; the stop boundaries need the owner and, where installed, a hook.
- A risk the agent cannot see, such as a contract term in a document it was not given, will not be tagged.
- Sizing the route is a judgement; the owner can always raise it.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/route-the-work/input.md) and [output](../../examples/route-the-work/output.md).
