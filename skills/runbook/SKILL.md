---
name: runbook
description: "Writes a runbook from what was actually done: owner, steps, checks, failure handling and rollback, so a team that did not build it can run it. Use when a process becomes someone else's job or depends on one person's memory."
---

# Write the runbook from what happened

Turn a process that works into instructions a different person can follow without the builder in the room. Base it on what was done and observed, not on what the design said should happen.

Stage: Own. Rules: 3 Read back the real result, 4 Claim only what you can show, 1 Stop at the boundaries.

## Context and handoff

Observe the existing process and read current access and exception records. Have the intended operator attempt it using the instructions. Record the runbook revision, environment and allowed actions before that attempt.

Use `enablement-plan` if they need training or a supervised exit. Save the runbook in the team’s maintained location.

## When not to use this

Skip it for a one-off task that will never repeat. For a small, low-risk process, write the short version: purpose, owner, steps with expected results, one rollback line and a review date. Do not write a runbook for a process nobody has run successfully; run it first, or say the runbook is a draft from the design and mark every step "not yet run".

## Steps

1. **Name the owner and the purpose.** Who runs it now, who is the backup, and what the process is for in one sentence. Name the person who accepts the runbook as usable.
2. **Gather what really happened.** Use the logs, shell history, commit history, meeting notes, tickets and the builder's own account. If possible, watch or have the builder run it once while you record each step. Mark each step "seen", "told" or "from design".
3. **State the schedule and triggers.** When it runs (time, frequency, event), how long it takes, what must be true before it starts and what it depends on.
4. **Write the steps.** Numbered, one action each, in the order done. Give the exact command, button or page, the account or role needed (never the secret itself), and the expected result after each step. Replace "check it looks right" with what right looks like.
5. **Write the checks.** After the run: what to look at, where, and what a good result and a bad result look like. Include a way to confirm that the effect reached the real place (the live page, the sent file, the database count).
6. **Write the failure section.** For each failure seen or foreseeable: symptom, likely cause, what to try first, when to stop and escalate. Use failures from the incident notes before inventing any.
7. **Write the rollback and the stop point.** Say when to stop mid-run (for example, a check fails twice or a total is off by more than the agreed tolerance) and leave things in a known state. Give how to undo or stop safely, what cannot be undone, and who must say yes before an irreversible step (sending, spending, deleting, deploying, publishing).
8. **Say who to call.** Names or roles, how to reach them, and when. Escalation order. No personal contact details in a public repository; point to the team contact sheet.
9. **Test it with someone new.** Ask a person who did not build it to follow the runbook, with the builder only observing. Record where they stopped or guessed and fix those lines. Record which steps were tried, what the operator needed from the builder and what remains untested. Mark independent operation verified only for a complete, checked cycle with no help. An assisted run can improve the runbook. Test the affected steps again after a change to the runbook, tools, access or process. See the [handover exercise](handover-exercise.md).
10. **Plan the next cycle without the builder.** Name who runs the next real cycle, with the builder reachable only to stop it. Record the result on the same page; a second clean cycle on a changed runbook is the evidence that it has stuck.
11. **Set a review date** and say what changes trigger an update.

## Output

Use [template.md](template.md). Save with the process, for example `runbooks/weekly-invoice-run.md`. Never include passwords, tokens or keys; say where they are held and who can grant access. Do not repeat a secret's value in your reply either: say plainly that you will not include it, name it only by what it is ("the bank password"), and advise rotating it because it was pasted into a chat.

## Checks

- Every step is marked seen, told or from design.
- Steps give the expected result, not just the action.
- Failures, rollback, a stop point and an escalation list are present.
- No secrets appear in the text, and none is repeated in the reply.
- The run record names the operator, revision, environment, assistance and observed outcome. The status matches those facts.
