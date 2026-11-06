---
name: one-off-or-factory
description: Decides whether to write items directly or build a factory, weighing build cost and rework against direct authoring; a factory needs a three-item pilot showing better accepted quality or lower total cost. Use when someone says "let's automate this".
---

# One-off or factory

Avoid building machinery that costs more than writing the items by hand. Test the factory on three real items first, then decide with numbers.

Stage: Hypothesise. Rules served: 2 (agree acceptance first) and 4 (claim only what you can show). Applies control 9, pilot-before-scale (`rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed)).

## Context and handoff

Read representative requests, expected volume, source variation and error cost. Compare a direct draft with the work of maintaining a master.

Use `proposal-factory` or `batch-document-factory` when the shape repeats. Record the routing decision with the brief.

## When not to use this

Skip it when only one item is needed, or when the process already exists and has been accepted (then use it). Do not use it to justify a tool someone already wants to build; use it to test the want.

## Steps

1. **Count and name the work.** How many items, how alike, by when, who accepts them, how much each differs by reader. If fewer than five, or if they differ in substance, author directly and record why.
2. **Define accepted.** Write the acceptance for one item (see `agree-acceptance`): what a person would accept without editing. This is the yardstick for both routes.
3. **Estimate both routes in the same units.** Direct: minutes per item to author and check, times the count. Factory: time to build, time per item to run and check, expected rework rate. Mark every figure as measured, estimated or guessed.
4. **Run a pilot of three.** Produce three items by direct authoring and three by the factory (or use the same three readers in both). Use three real, varied items, including the hardest. Time each, record what was edited before acceptance, and have the owner accept or reject each.
5. **Compare.** Per route: items accepted unedited, items accepted after edits (with the edits), items rejected, total time including building and rework. Quality counts first; cost second.
6. **Decide by the rule.** Build the factory only if it gives better accepted quality, or lower total cost including rework and build time, across the whole planned count. If the pilot is a draw or the sample is too small to tell, author directly and say so.
7. **Write the decision record** using [template.md](template.md). If the decision is factory, the next step is `proposal-factory` or the relevant production method, which must start with the same pilot items.

## Output

A one-page decision record: the work, acceptance, both routes with figures and their status, pilot results, the decision and the reason, and what would change the decision. Save with the project, for example `.work/decisions/<topic>.md`.

## Checks

- The count and the differences between items are stated.
- Every figure is labelled measured, estimated or guessed.
- The pilot used three real items and the owner accepted or rejected each.
- The decision follows the rule and names the figures it rests on.
- Authoring directly is the default when the evidence is thin.
