# hypothesis-card

**Turn "this will help" into a bet you can lose: a change, an expected result, a number that moves, a deadline and a stop line.**

The agent writes one card in the form "We believe that X will result in Y, and we will know because Z changes". It adds the measure, the baseline, the target, the time box and the result that would make you stop.

It belongs to the Hypothesise stage. It serves rule 2, Agree acceptance first, and rule 4, Claim only what you can show.

## The problem it solves

Harbourside Lettings wants a chatbot on its website to "reduce calls". The owner is sure it will help and asks for a quote. Nobody has written down which calls, how many there are, how many would go, or when to give up. Three months later there is a chatbot, a bill and an argument about whether it worked.

## What the agent does differently

It writes the belief for one named group (tenants reporting repairs), picks one measure (repair-status calls per week), records the baseline as "not measured" because no one counts them, and sets a stop line. It lists the assumption that tenants would use a chatbot at all as the cheapest thing to test first. See [examples/hypothesis-card/output.md](../../examples/hypothesis-card/output.md).

## When to use it, and when not to

Use it before building or buying anything whose benefit is assumed. Skip it for required work, such as a legal change, or for tasks smaller than the card.

## Who it is for

- **Founder or owner:** a short way to say what "worth it" means.
- **Product or operations lead:** a card to attach to a budget request.
- **Anyone asked to build something nobody has measured:** a reason to ask for the baseline first.

## How to use it

> Write a hypothesis card for adding a repair-status chatbot to our website. Use the baseline notes in `.work/chatbot/baseline.md`.

Read the card, change the target or the stop line, and confirm it.

## How it connects

- **Before:** [capture-the-problem](../capture-the-problem/README.md) and [baseline](../baseline/README.md).
- **After:** [experiment-plan](../experiment-plan/README.md) designs the smallest test, and [agree-acceptance](../agree-acceptance/README.md) fixes what done looks like for the build.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- One change, one group, one main measure. If you need three, write three cards.
- Set the target at the smallest result that would justify continuing.
- If nobody will say what would make them stop, the idea is not ready to test.

## Limits

- A card does not make the bet a good one; it makes it checkable.
- Targets are judgements. The agent proposes, the owner sets.
- The time box can be too short for slow effects. Say so on the card.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/hypothesis-card/input.md) and [output](../../examples/hypothesis-card/output.md).
