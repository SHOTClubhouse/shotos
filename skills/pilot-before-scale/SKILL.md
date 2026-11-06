---
name: pilot-before-scale
description: Runs a task on three items or fewer first, inspects and fixes, then completes a preflight checklist before the full run. Use for bulk edits, mass drafts, clean-ups, migrations or any run touching many records.
---

# Pilot before scale

Mistakes multiply with the size of the run. A pilot of three items finds most of them for the price of three.

**Stage:** Operate. **Rules:** 1 Stop at the boundaries; 3 Read back the real result. Detail: `rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed).

## Context and handoff

Read the exact target list, authority, recovery route and change limits. Select varied items that include a failure or edge case.

Use `evidence-pack` to decide from the pilot results. Keep batch receipts and rollback proof together.

## When not to use this

Skip it when there are three items or fewer, or the run is read-only and can be repeated at no cost. Do not pilot a task you would do by hand in a minute.

## Steps

1. **Count the items and state the action.** If you are asked how you will do the job, answer with the pilot of three and the preflight checklist by name, and say what each will hold for this job. Say how many items, what will happen to each, and whether it can be undone. If the count is three or fewer, run it and inspect each one.
2. **Pick the pilot items.** Choose up to three that differ from each other: a typical one, an awkward one (missing data, odd format) and, if you can find it, one that should be skipped. Say why each was chosen. Do not pick the three easiest.
3. **Run the pilot in the real home, within the boundaries.** If the action goes outside the team (a send, a post, a purchase, a delete), the pilot goes to the owner or to a test address first and needs the owner's yes. A pilot is not a licence to send three.
4. **Inspect the results.** Open each result where it actually lives, not just the agent's log. Compare with the input and the acceptance checks. Write down what is wrong, what is surprising and what took longer or cost more than expected.
5. **Fix and re-run.** Change the instructions, template or script, and run the three again. If a fix changes the nature of the task, pick three fresh items. Repeat until all three pass, or stop and report that it does not work.
6. **Complete the preflight checklist** (see [template.md](template.md)) before the full run:
   - **Inputs:** the list of items is final, counted, deduplicated and read from the right source.
   - **Targets:** where each result will go, and that the target is the right place (the live site or the copy).
   - **Rollback:** how to undo it, tested on a pilot item, or "cannot be undone" with the owner's explicit yes.
   - **Budget:** time and money for the run, including AI usage, and the limit at which it pauses.
   - **Stop condition:** what makes the run halt itself (for example, two failures in a row, or a percentage of rejections), and who is told.
7. **Run in stages.** Run a small batch, inspect again, then the rest. Log what each item received so the run can be audited and picked up after a stop.
8. **Decide one-off or repeatable.** If this will run once, keep it simple: a script or a careful session, and delete the scaffolding. Build something repeatable only when the task will recur at least a few times, the format is stable and someone will own it. Say which you chose and why.
9. **Read back the whole run.** Check a sample from the full run in its real home and report counts: attempted, done, skipped, failed.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/pilot.md`.

## Checks

- Three or fewer pilot items, chosen to differ, with reasons.
- Each pilot result was inspected in its real home.
- The preflight lists inputs, targets, rollback, budget and stop condition.
- Anything that goes outside the team waited for the owner's yes.
- The final report gives counts and a sample check.
