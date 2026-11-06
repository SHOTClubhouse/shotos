---
name: pilot-before-scale
description: Runs a varied pilot of three items or fewer, then requires a preflight with tested rollback, stop condition and owner authority before a full run. Use for bulk edits, mass drafts, clean-ups, migrations or any run touching many records.
---

# Pilot before scale

Mistakes multiply with the size of the run. A pilot of three items finds most of them for the price of three.

For a live or bulk change, answer with the pilot, backup or rollback, stop condition and owner approval before discussing the full run. If asked *how* to do a job without the source file, give this concrete plan first and mark execution pending. Do not search outside the stated project to compensate for a missing input. If any safety item is missing, the full run is not ready.

**Planning answer, even when the source is missing:** (1) pilot three varied items; (2) save a backup and test restoring one pilot item; (3) list the preflight checks for input, target, cost and live dependencies; (4) state the condition that stops the full run; (5) identify who must approve the live run. Then name missing facts. A dry run without those five items is not the plan.

**Step:** Build. **Rules:** 1 Stop at the boundaries; 3 Read back the real result. Detail: `rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed).

## When not to use this

Skip it when there are three items or fewer, or the run is read-only and can be repeated at no cost. Do not pilot a task you would do by hand in a minute.

## Steps

1. **Count the items and state the action.** If asked how you will do the job, lead with the pilot of three varied items and the preflight checklist, including backup, tested rollback, a stop condition and owner sign-off before live scale. Say how many items, what will happen to each and whether it can be undone. A missing source blocks execution, not the plan. If the count is three or fewer, run it and inspect each one.
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
