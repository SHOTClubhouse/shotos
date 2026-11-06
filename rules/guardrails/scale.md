# Guardrail: Scale

## What it protects

The organisation's ability to do more of something without doing more harm. A task that is fine once can fail badly a hundred times: costs climb, a small error repeats, the one person who understood it is unavailable and nobody can tell what is running.

## Minimum practice

### 1. Pilot, then scale

- Run three units or fewer first, read them back, and run the preflight before the rest ([control 9](../09-pilot-before-scale.md)).
- Scale in stages: pilot, then ten times the pilot, then the batch, with a check between each step.
- Record the pilot, the preflight and the go in the task record.

### 2. Be able to stop

- Any run can be halted after any item, by the owner or by the agent on an unexpected result.
- Large runs report progress at intervals and stop on the first error that is not understood.
- A pause is a normal result, not a failure.

### 3. Know the cost per unit

- Before volume, work out the time, money and attention one unit takes, using the pilot. Multiply, and compare with what was agreed.
- Label estimates as inferred and actual figures as literal ([control 10](../10-claim-discipline.md)).
- Set a ceiling on spend and on number of external actions per run.

### 4. Check the receiving team can run it before copying it

- A result that only works while its builders are present is not ready to copy. The team that will run it must be able to run it, with a guide, a record and a person who has done it once without help.
- Hand over using the `evidence-handoff` skill, and keep the record under [control 11](../11-context-control.md).

### 5. Earn autonomy, do not assume it

- Use the graduation ladder for repeated task classes ([control 12](../12-graduation.md)). A class moves to auto-run only through logged unedited acceptance, and drops back if the rate slips.
- High-risk classes stay at draft-only unless a named person promotes them.

### 6. Keep an inventory

- List what runs on its own: automations, scheduled tasks, agents with standing permission. For each: owner, purpose, connectors used, rung on the ladder, date last reviewed.
- Retire what nobody owns.

## Checks

- Every batch above ten items has a pilot line and a go with a number.
- Pick an automation at random. The inventory names its owner and the last review date, and the owner can say what it does.
- Stop a run mid-batch. It stops cleanly and the receipts show exactly what was done.
- Compare actual cost per unit with the pilot's estimate. A large gap is explained.
- A second person can run the process from the record without asking the builder.
- `python .shotos/tools/graduation_log.py status` shows each automated class with its rung and reason.

## Controls and skills

| Control | How it applies |
|---|---|
| [8: two-session execution](../08-two-session-execution.md) | Large or irreversible runs go from a frozen manifest |
| [9: pilot before scale](../09-pilot-before-scale.md) | Small first, preflight, then go |
| [12: graduation](../12-graduation.md) | Autonomy earned by logged acceptance |
| [11: context control](../11-context-control.md) | The record that lets others pick it up |

Skills: `evidence-handoff` for ownership transfer; `report-with-evidence` for per-stage reports.

## Common failure

A volunteer coordinator at a youth club sets an agent to send weekly reminders to every family. It works for six weeks. A family moves away and asks to be removed; the request is made in an email nobody connects to the automation, and reminders continue. The inventory and the withdrawal check in the [data governance guardrail](data-governance.md) would have caught it.
