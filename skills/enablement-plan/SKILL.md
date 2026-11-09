---
name: enablement-plan
description: "Plans how a team becomes self-sufficient with a new process or agent-assisted way of working: capability matrix, pairing, train-the-trainer, and an exit test of one cycle without the builders. Use when results still depend on the people who built them."
---

# Plan enablement to self-sufficiency

Make the team able to run, fix and improve the result without the people who built it. Success is a full cycle run by the team with the builders watching only.

Stage: Own. Rules: 3 Read back the real result, 4 Claim only what you can show, 2 Agree acceptance first (the exit criterion).

## Context and handoff

Read the receiving team’s real permissions, capacity and current runbook. Agree an independent cycle that includes an exception.

Use `runbook` for gaps and `rollout-plan` after the lead accepts the cycle. Record observed intervention and sign-off.

## When not to use this

Skip it when the result is a one-off with no repeat, or when one person will run it and the runbook alone is enough (a founder's weekly report, say), or when a vendor will run it permanently by contract (then plan the handover of requirements instead). Do not use training attendance as proof of ability.

## Steps

1. **Name the receiving team and the sponsor.** List the people who will own the result, their roles and the share of time they can give. Name who accepts that the plan is met. If the team has not been asked, ask before drafting.
2. **List the capabilities the result needs.** Separate: running it (routine operation), checking it (reading results, spotting a bad one), fixing it (common faults), changing it (small changes) and deciding about it (when to stop or escalate). Keep to the dozen that matter.
3. **Build the capability matrix.** Rows are people, columns are capabilities. Use four levels: 0 not yet, 1 can do with help, 2 can do alone, 3 can teach others. Score from observation of someone doing the task, not from self-rating alone. Show both the current level and the target level, and mark cells nobody can reach target in the window.
4. **Check the single points of failure.** For every capability, count people at level 2 or above. Flag any with fewer than two.
5. **Set the pairing schedule.** Use a progression: builder does and the learner watches, learner does and the builder watches, learner does alone and the builder reviews afterwards. Give dates, pairs, the task and the time box. Keep sessions short and tied to real work.
6. **Plan train-the-trainer.** Choose one or two people per capability who will teach others, give them the teaching material (the `runbook` and worked examples), and have them teach once while the builder watches. Leave a written guide so new joiners do not depend on a person.
7. **Write the exit criterion first.** Agree it before training starts: the team runs one full cycle of the process end to end, including a check and a handled fault, with the builders observing silently and stepping in only to stop an unsafe action, which fails the cycle. Name the cycle, the date window, and what counts as a pass.
8. **Plan the fault drill.** Introduce one safe, known fault (a bad input in a test copy, a missing value) and see whether the team finds and handles it using the runbook.
9. **Set an early stop.** Name what pauses training before the window ends: a pairing round where the learner still needs the builder at every step, a person who leaves, or no time given for two weeks running. On a stop, keep the builder as the named operator, record who runs it meanwhile, and re-plan with the sponsor instead of extending silently.
10. **Set support after exit.** The builders' reduced role: a named contact for a set period, and the date it ends. Decide what is escalated to whom afterwards.
11. **Record the result.** After the exit run, update the matrix with observed levels, list what was needed from the builders, and mark the exit as passed, passed with conditions or not yet. A named person accepts it. Only a passed exit, or a pass with conditions the sponsor accepts, lets `rollout-plan` start; "not yet" schedules a second independent cycle with a fresh fault.

## Output

Use [template.md](template.md). Save as `.work/<task>/enablement-plan.md` and update the matrix after each pairing round.

## Checks

- Each capability has at least two people planned to reach level 2.
- Levels come from observation.
- The exit criterion is written before training starts and requires builders to observe only.
- A fault drill, an early-stop trigger and a post-exit support end date are in the plan.
- The result states whether the next cycle was run without the builders, or that it is still to do.
- A named person accepts the exit result.
