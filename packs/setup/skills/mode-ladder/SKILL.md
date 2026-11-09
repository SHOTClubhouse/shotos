---
name: mode-ladder
description: Chooses Quick, Standard, Thorough or Team of agents based on size, risk and uncertainty. Use to route a task, respond to a change in risk, or set a team policy. Effort leaves authority with the owner.
---

# Right-size the effort

Stage: Scope. Rule 1 (stop at the boundaries). Controls 3 (mode contract) and 11 (context control).

## Context and handoff

Start with the output, its reader, the acceptance check and the authority already given. Look for a recorded route that worked on comparable tasks. Use `graduation-ladder` for a change in autonomy, and `connect-tools` when a required capability is unproven. Keep the route and any change in the task record.

## Trigger and minimum inputs

Run it at the start of a task, when a check fails, or when risk or scope changes. It needs a one-line task, the reader or user, the cost of an error and the acceptance check. If the acceptance check is missing, say the level is provisional and ask the owner for it. Without model or tool inventory, name the level and leave the model choice to the owner.

## When not to use this

Skip the routing ceremony for a simple question. Resolve permission from the owner's scope and project rules.

## Choose the route

Size the work by how many things it touches, the cost and reversibility of an error, and how much of the method is unknown.

| Level | Use when | Context and check |
| --- | --- | --- |
| Quick | The task is understood, low risk and reversible. Use a small model or deterministic tool. | Give it the exact input and expected result. Run one observable check. |
| Standard | Several steps or shared artefacts, with a clear acceptance decision. Use a model capable of the work. | Read the acceptance and current project sources. Open the saved result and check it against the examples. |
| Thorough | Unfamiliar judgement, sensitive material or a costly reversal. Use the smallest route that can pass the required checks. | Add sources for the decision at risk. Give a bounded independent reviewer the result, acceptance and relevant evidence. |
| Team of agents | Independent pieces benefit from parallel workers after a small pilot. Use a fixed procedure or script as supervisor. | Set worker count, time, cost, supervisor and stop condition. Pilot three units or fewer, then compare outputs and read back a sample. |

Use a deterministic script for repeated exact work when it can meet the checks. Load the current brief and primary sources first. Open more context for an identified gap, contradictory evidence or a material decision.

## Change one thing at a time

1. If a check fails, name the cause. Missing evidence calls for retrieval or a held decision. Unavailable access calls for another authorised route or the owner. Weak reasoning can justify a stronger model or independent review.
2. Carry the saved result, exact revision and failed check into a retry or handoff. If the result already meets acceptance, resolve the access or delivery check first. Rebuild only when the approved result is missing, wrong or superseded.
3. Continue inside existing authority. Ask for a decision if the new route increases spend beyond the approved limit, needs new access or expands the work. Sending, spending, deleting, deploying and publishing follow the same approval boundaries at every level.

For a recurring workflow, record the default, who can change it and the evidence required to step down. Compare equivalent accepted work before changing the default.

## Blockers and handoff

Stop and ask the owner when the route needs more spend, new access or wider scope than approved. Hand a Team of agents route to the owner with the pilot plan. Hand a failed check back to the skill that owns the work, with the new level and reason.

## Output and checks

Record the level, reason, model or tool, minimum sources and review in one line. Use [template.md](template.md) when the choice needs to be shared. Check that the route can perform the task, the review matches the risk and any parallel work has limits and a pilot.
