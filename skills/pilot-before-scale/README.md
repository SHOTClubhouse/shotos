# pilot-before-scale

**Run it on three items or fewer, look at what happened, fix it, check the list, and only then run the rest.**

The agent pilots any bulk job on up to three varied items, inspects each result in its real home, fixes the problems, and completes a preflight checklist covering inputs, targets, rollback, budget and stop condition before the full run. It also says whether the job should stay a one-off or become a repeatable process.

It belongs to the Operate stage. It serves rule 1, Stop at the boundaries, and rule 3, Read back the real result. The detail is in [rules/09-pilot-before-scale.md](../../rules/09-pilot-before-scale.md).

## The problem it solves

Millbrook Rovers youth club has 212 player records to update with a new age-group code before the season. An agent can edit them all in one pass. In a run on all records, a date in an unexpected format turns 31 children into the wrong age group, and the same pass has already changed the sheet that the fees page reads from. Someone finds out when parents ring.

## What the agent does differently

It picks three records that exercise different behaviour. The [worked example](../../examples/pilot-before-scale/output.md) checks the expected codes for an ordinary date, a date stored as text and a blank. The workbook is absent in the exercise, so the result is a proposed pilot. On real work, use an authorised copy, inspect the written values and test restoration before requesting approval for the live batch.

## When to use it, and when not to

Use it for bulk edits, mass emails or drafts, data clean-ups, migrations and batch AI generation. Skip it for three items or fewer, or read-only runs you can repeat at no cost.

## Who it is for

- **Anyone letting an agent loose on a list:** a cheap way to find the mistake before it is multiplied.
- **Team lead:** a preflight checklist that can be reviewed in a minute.
- **Operations owner:** a clear count of what was done, skipped and failed.

## How to use it

> Update the age-group code on the 212 rows in `registrations.xlsx` using the new bands. Pilot it first, show me the pilot and the preflight, and wait for my yes before the full run.

Read the pilot results yourself in the sheet. Give the yes for the full run only when the checklist is complete.

## How it connects

- **Before:** [route-the-work](../route-the-work/README.md) sets the risk, and [agree-acceptance](../agree-acceptance/README.md) sets the checks the pilot is held to.
- **After:** [report-with-evidence](../report-with-evidence/README.md) reports the run, and [cross-agent-review](../cross-agent-review/README.md) reviews it when the risk calls for it.
- **Rules:** [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent. The agent needs write access to a copy of the data for a pilot.

## Tips

- Pick the awkward items on purpose. Three easy ones prove nothing.
- Take the backup before the pilot, not after.
- A stop condition that is only in your head will not stop a run; write it in the checklist.

## Limits

- A pilot of three cannot find every problem. It finds the common ones early.
- The rollback is only as good as its test. "We can restore from backup" is not a rollback until someone has restored.
- The skill asks the agent to stop. It does not stop a tool that is already running.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/pilot-before-scale/input.md) and [output](../../examples/pilot-before-scale/output.md).
