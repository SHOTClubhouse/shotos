---
name: experiment-plan
description: "Plans the smallest test of a hypothesis: method, sample, duration, cost, success and stop criteria, and who decides. Use when a hypothesis card exists and before building, buying or rolling out the full solution to find out whether it works."
---

# Plan the smallest test

The question is not "how do we build this" but "what is the cheapest thing we can do to find out whether it is worth building". Plan that test, and agree how it will be judged before it runs.

**Stage:** Hypothesise. **Rules:** 2 Agree acceptance first; 1 Stop at the boundaries.

## When not to use this

Skip it when the hypothesis can be answered by a lookup or a conversation that costs minutes, or when the decision is already made and the work is required. Do not turn a plan into a research project.

## Steps

1. **Start from the hypothesis card.** Copy the belief, measure, baseline and stop result. If there is no card, write one first with [hypothesis-card](../hypothesis-card/README.md).
2. **Find the riskiest assumption.** Pick the one assumption that, if false, makes the whole idea fail. The test is aimed at that one.
3. **Choose the smallest method that tests it.** Options, from cheapest: ask five people directly; look at existing data; a mock-up or manual version run by a person (the "concierge" test); a link or button that counts clicks before anything is built; a limited pilot with real users; a split between two groups. Choose the cheapest one that could actually show the belief is wrong.
4. **Set the sample.** Say who is included, how many and how they are chosen. For small numbers, say what the number can and cannot show, and do not claim a statistical result from it.
5. **Set the duration and cost.** Give a start and end date, staff hours and money. Money, outside contact or live systems need the owner's yes before the plan starts.
6. **Write success and stop criteria before the test.**
   - Success: the result that would justify the next step, as a number or a plain yes/no.
   - Stop: the result that ends the test early, including any harm to the guard measure.
   - In between: say what you will do if the result is unclear (usually: run once more with a changed design, or stop).
7. **Name who decides** and when they will look at the result. Agree that the criteria will not change after the test starts.
8. **Plan the read-back.** Say where each number will be read from and who records it. Plan to report failures as plainly as successes.
9. **Check the harm.** List anyone who could be affected by the test, and what they will be told. Anything that touches customers, children's data or money has to be shown to the owner first.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/experiment-plan.md`.

## Checks

- The test targets the riskiest assumption, not the whole idea.
- Success and stop criteria were written before the test.
- Duration, cost and sample are stated, with the limits of the sample.
- One person decides, and the owner has said yes to any spend or outside contact.
