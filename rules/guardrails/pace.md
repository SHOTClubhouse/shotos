# Guardrail: Pace

## What it protects

Honest delivery against what was agreed. Pace is about whether work is on schedule and at the quality promised, and whether the person who needs to know is told while there is still time to act. Speed that quietly lowers quality, and quality that quietly misses the date, both fail the same guardrail.

## Minimum practice

### 1. One status line per task, on schedule and on quality

Every task in progress carries a status line in its owning record ([control 11](../11-context-control.md)). It has seven fields. Schedule and quality are reported separately, because a task can be on time and wrong, or right and late.

| Field | What goes in it |
|---|---|
| **Task** | What the work is, in a few words |
| **Owner** | The person who accepts it |
| **Agreed time** | The date or time the owner expects it, and who agreed it |
| **Schedule status** | `on track`, `at risk` or `late`, with the reason in a clause |
| **Quality status** | `meets acceptance`, `partly meets` or `not yet checked`, against the acceptance card |
| **Evidence** | Where the proof is: a file, a command result, a receipt |
| **Next action** | The next step, who takes it, by when |

Example (invented):

```
task: tenancy renewal letters | owner: Maya | agreed time: Fri 14:00 (agreed by Maya, Mon)
schedule: at risk (two cases awaiting a landlord answer) | quality: partly meets (31 of 40 checked)
evidence: .work/renewals/checks.log | next: ask landlord about cases 12 and 27, Priya, Wed
```

An unknown stays written as `unknown`. Do not fill a field with a guess.

### 2. Update at meaningful checkpoints

Update the line when acceptance is agreed, at the end of each substantial step, when anything changes in either status, and at handover. A status line that is a week old is not a status line.

### 3. Raise problems early

- Tell the owner when schedule moves to `at risk`, not when it reaches `late`.
- Offer options: reduce scope, move the date, or add help. Let the owner choose.
- Never lower quality silently to hold a date. If acceptance cannot be met by the agreed time, say so.

### 4. Pace by evidence, not by feeling

- Estimates are labelled inferred. Actuals are labelled literal, with the source ([control 10](../10-claim-discipline.md)).
- Use pilot results ([control 9](../09-pilot-before-scale.md)) to set the schedule for the batch.
- When the time is unknown, write it as unknown and say what would make it known.

### 5. Autonomy follows the record

- Use the graduation ladder ([control 12](../12-graduation.md)) to decide how much of a repeated task runs without a person. Pace of work can rise only as acceptance holds.

## Checks

- Every active task has a status line with all seven fields, updated within the last few working days.
- Pick a task that finished late. When did the status first say `at risk`? If it never did, the guardrail was not working.
- Pick a task that was on time. Does its quality status match what the owner thought on acceptance?
- Check that each `quality: meets acceptance` points to evidence a stranger could open.
- Review the weekly count of tasks by status. Many tasks stuck at `not yet checked` suggest review is the bottleneck.

## Controls and skills

| Control | How it applies |
|---|---|
| [1: route the work](../01-route-the-work.md) | The route and proof fields set the expectation |
| [5: acceptance first](../05-acceptance-first.md) | Quality status is measured against the card |
| [9: pilot before scale](../09-pilot-before-scale.md) | Evidence for the schedule |
| [12: graduation](../12-graduation.md) | Pace of autonomy follows the log |

Skills: `agree-acceptance` supplies the quality baseline; `report-with-evidence` supplies the evidence field; `evidence-handoff` carries the status line into the next session.

## Common failure

A project at Northgate Cycles reports "green" every week because the schedule is green. Quality is unchecked, and nobody notices until the launch, when half the product descriptions are missing. Two separate fields would have shown a green schedule beside a "not yet checked" quality from week one.
