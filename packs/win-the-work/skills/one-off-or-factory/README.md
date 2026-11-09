# one-off-or-factory

**Decide whether to write each item yourself or build a factory, using a pilot of three and the rule that quality and total cost decide.**

The agent counts the work, defines what an accepted item looks like, estimates both routes in the same units, runs or plans a pilot of three, compares accepted quality and total cost including rework, and writes a decision record. When the evidence is thin it authors directly.

It belongs to **Hypothesise**. It serves rule 2, Agree acceptance first, and rule 4, Claim only what you can show, and applies [control 9, pilot before scale](../../../../rules/09-pilot-before-scale.md).

## The problem it solves

Harbourside Lettings wants 40 tailored landlord letters. An enthusiastic colleague spends three days building a template system with merge fields. The first six letters come out with the wrong tone for older landlords and every one needs editing. Writing the 40 by hand would have taken about four days of focused work, and each letter would have been right the first time.

## When to use it, and when not to

Use it before building a template, generator or batch process for repeated output.

Do not use it for a single item, or to justify a tool someone already wants. Run it to test the want.

## Who it is for

- Founders and managers deciding whether to automate.
- Anyone about to build a template for fewer than a few dozen items.
- Teams whose last automation cost more than it saved.

## How to use it

> I need 25 tailored welcome letters to new landlords. Should I write them directly or build a factory? Plan the pilot and give me the decision record.

You get the record from [template.md](template.md) with the pilot plan. After the pilot, bring the results and the agent completes the comparison. For each pilot item the record notes the output and revision you accepted. A factory decision hands those three accepted items to the next skill, which reuses them instead of running a second pilot. A direct decision is a stop: nothing reruns until you reopen it with new evidence.

## How it connects

- **Next:** [proposal-factory](../proposal-factory/README.md) if the answer is factory; [contextual-proposal](../contextual-proposal/README.md) if it is direct.
- **Needs first:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) defines the yardstick.
- **Rule:** [rules/09-pilot-before-scale.md](../../../../rules/09-pilot-before-scale.md).

## Needs

Nothing beyond the agent.

## Tips

- Pick the hardest item for the pilot, not the easiest.
- Count your own checking time. It is the cost that hides.
- Record edits, not just a yes or no.
- Write down which revision of each item you accepted, so the next step can tell what has changed.

## Limits

- Three items is a small sample. It is enough to catch a bad factory, not to prove a good one.
- Time figures are only as good as the stopwatch. The record marks them measured, estimated or guessed.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/one-off-or-factory/input.md) and [output](../../examples/one-off-or-factory/output.md).
