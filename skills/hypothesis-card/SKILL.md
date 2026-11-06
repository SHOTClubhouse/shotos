---
name: hypothesis-card
description: "Turns an idea into a testable bet: \"We believe X will result in Y, and we will know because Z changes\", with measure, baseline, target and stop result. Use when a benefit is assumed, or someone says \"this will help\"."
---

# Write the hypothesis card

An idea says what to do. A hypothesis says what you expect to happen and how you would find out you were wrong. Write the second one before spending anything on the first.

**Step:** Brief. **Rules:** 2 Agree acceptance first; 4 Claim only what you can show.

## When not to use this

Skip it for work that is required regardless of benefit, such as a legal change, or for a task so small that being wrong costs less than writing the card.

## Steps

1. **Start from the problem and the baseline.** Name the confirmed problem (see [capture-the-problem](../capture-the-problem/README.md)) and the current value of the measure (see [baseline](../baseline/README.md)). If either is missing, say so and write "not measured" instead of continuing on a guess.
2. **Write the belief in one sentence** (the hypothesis form from Lean UX by Jeff Gothelf and Josh Seiden, and from hypothesis-driven development by Barry O'Reilly): "We believe that [change] will result in [outcome for a named group], and we will know because [measure] changes from [baseline] to [target] within [time box]." Use one change, one group and one main measure.
3. **Name the measure exactly.** State the definition, the unit and where the number will be read. It must be a measure that can move within the time box.
4. **Set the target and the time box.** The target is the smallest change that would justify going on, not the best case. The time box is a date or a number of weeks, agreed with the owner.
5. **Write the stop result.** State the result that makes you stop, change course or drop the idea. Include a guard measure that must not get worse. If you cannot state what would make you stop, the card is not ready.
6. **List the assumptions.** Write the two or three things that must be true for the belief to hold, and mark each as checked, unchecked or unknown. Mark any that could be tested more cheaply than the whole idea (see [experiment-plan](../experiment-plan/README.md)).
7. **Name the decider.** One person decides, after the time box, whether to continue, change or stop. Write their name or role.
8. **Stop at the boundaries.** Writing the card does not authorise the test. Any spend, external contact or change to live systems needs the owner's yes.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/hypothesis.md`.

## Checks

- The belief names a change, a group, an outcome and a measure.
- The baseline has a source, or says "not measured".
- The target is a number or a clear yes/no, and the time box has an end.
- A stop result and a guard measure are written down.
- A named person decides.
