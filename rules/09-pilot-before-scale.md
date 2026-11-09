# Control 9: Pilot before scale

**The rule:** Run three units or fewer first, read them back, then run the preflight before the rest.

Serves rule 2, [Agree acceptance first](../docs/controls.md). Matters most in **Operate**, and again in **Sustain and Scale**.

## Why it exists

A volunteer coordinator at Millbrook Rovers asks an agent to generate and email personalised training schedules to 140 families. The agent builds the template, merges the data and sends all 140. The merge field for the child's name pulled the parent's surname instead. One hundred and forty families received "Hi Patel, here is Patel's schedule". A single message, sent first and looked at, would have caught it.

Errors that repeat cost the same each time. Volume turns a small mistake into a large one. A pilot is cheap insurance: do a few, look hard, then continue.

## What the agent does

1. Counts the units: items, records, messages, files, pages, changes.
2. If there are more than three, picks a **pilot of three or fewer**. The pilot includes the most typical item and the item most likely to fail, such as the longest name, the empty field or the one with special characters.
3. Runs only the pilot. For external actions, the pilot needs the same approval as the whole batch (see [control 4](04-stop-boundaries.md)), and the owner may prefer to receive the pilot items themselves.
4. Reads the pilot back in the real home under [control 6](06-read-back.md), and compares with the acceptance card.
5. Fixes what the pilot reveals and reruns the pilot items the fix touched (all three only if it touched all of them).
6. Runs the **preflight checklist** below.
7. Asks for a go for the rest. The go names the count and what was learned.
8. Runs the remainder, reports progress at sensible intervals, and stops on the first unexpected result.

### Preflight checklist

- [ ] The pilot was read back in the real home, not just in the agent's log.
- [ ] Every item in the remainder has the fields the pilot needed, with no blanks or oddities.
- [ ] The count and the list are the ones the owner approved, with exclusions applied.
- [ ] Rate limits, quotas and cost are known and within what was agreed.
- [ ] A stop point exists: the agent can halt after any item.
- [ ] A way to undo or contain exists, or the owner has accepted that none does.
- [ ] Receipts will be kept per item.
- [ ] Nothing changed between the pilot and now (inputs, template, target). If it did, recheck only the pilot items the change touches (see below).

### Reusing an accepted pilot

A pilot the owner has already accepted, for example from `one-off-or-factory`, is not run again.

- Carry forward each item whose output, source and acceptance still match the accepted revision, with its review status.
- Recheck only the items whose template, relevant data, target or acceptance changed, and any item with no accepted output.
- Repeat the whole pilot only if the change touches every pilot item or invalidates the owner's acceptance.
- Stop if acceptance or evidence for a pilot item is missing; do not rerun to fill the gap.
- Reuse never waives the checks that apply today. Gates for pricing, suppression, approval and access are checked again on each reused item.

## What a person does

- Looks at the pilot results with their own eyes, preferably as the recipient would see them.
- Names the pilot items if they know where it tends to go wrong.
- Gives the go, with the number, or says stop.
- Decides what amount of failure is acceptable. For personal data or money, the answer is usually none.

## The format

A pilot line in the task record:

```
pilot: 3 of 140 (typical: family 012; long surname: family 087; no second guardian: family 131)
result: 2 correct, 1 wrong (family 087 surname truncated)
fix: template widened | rerun pilot: 3 of 3 correct
preflight: all 8 items ticked
go: "run remaining 137" by Maya, 14:20
```

## Sizing by risk

- **Small work:** fewer than three units needs no pilot; do them and look at each.
- **Normal work** (a batch of documents, a repeated edit): pilot of one to three, read back, then the rest.
- **High-risk work** (external, personal data, spend, irreversible): pilot of one first, then up to three, with the owner viewing results before any larger run. Combine with [control 8](08-two-session-execution.md). Large runs go in stages with a check between each.

## Common mistakes

- Choosing the three easiest items.
- Calling the first success the pilot and skipping the read-back.
- Piloting on test data while the real data has different shapes.
- Fixing a fault and not rechecking the pilot items it touched.
- Rerunning an accepted pilot, or reusing one whose revision no longer matches.
- Setting off the remainder in a way that cannot be stopped.
- Treating the pilot as approval for the batch without a separate go.

## How to check it is working

- Look at the last three batch jobs. Each has a pilot line, a read-back and a go with a number.
- The pilot found at least one issue in a meaningful share of jobs. If it never finds anything, the pilot items are too easy.
- No batch above ten items started without a named go.
- Errors found after the batch are rare and traceable to something no pilot could have shown.

## Related

[Control 6: read-back](06-read-back.md) · [Control 8: two-session execution](08-two-session-execution.md) · [scale guardrail](guardrails/scale.md) · [rules index](README.md)
