---
name: runbook
description: "Writes a runbook from what was actually done: owner, steps, checks, failure handling and rollback, so a team that did not build it can run it. Use when a process becomes someone else's job or depends on one person's memory."
---

# Write the runbook from what happened

Turn a process that works into instructions a different person can follow without the builder in the room. Base it on what was done and observed, not on what the design said should happen.

Step: Hand over. Rules: 3 Read back the real result, 4 Claim only what you can show, 1 Stop at the boundaries.

## When not to use this

Skip it for a one-off task that will never repeat. Do not write a runbook for a process nobody has run successfully; run it first, or say the runbook is a draft from the design and mark every step "not yet run".

## Steps

1. **Name the owner and the purpose.** Who runs it now, who is the backup, and what the process is for in one sentence. Name the person who accepts the runbook as usable.
2. **Gather what really happened.** Use the logs, shell history, commit history, meeting notes, tickets and the builder's own account. If possible, watch or have the builder run it once while you record each step. Mark each step "seen", "told" or "from design".
3. **State the schedule and triggers.** When it runs (time, frequency, event), how long it takes, what must be true before it starts and what it depends on.
4. **Write the steps.** Numbered, one action each, in the order done. Give the exact command, button or page, the account or role needed (never the secret itself), and the expected result after each step. Replace "check it looks right" with what right looks like.
5. **Write the checks.** After the run: what to look at, where, and what a good result and a bad result look like. Include a way to confirm that the effect reached the real place (the live page, the sent file, the database count).
6. **Write the failure section.** For each failure seen or foreseeable: symptom, likely cause, what to try first, when to stop and escalate. Use failures from the incident notes before inventing any.
7. **Write the rollback.** How to undo or stop safely, what cannot be undone, and who must say yes before an irreversible step (sending, spending, deleting, deploying, publishing).
8. **Say who to call.** Names or roles, how to reach them, and when. Escalation order. No personal contact details in a public repository; point to the team contact sheet.
9. **Test it with someone new.** Ask a person who did not build it to follow the runbook, with the builder only observing. Record where they stopped or guessed and fix those lines. Mark the runbook "tested by (name) on (date)".
10. **Set a review date** and say what changes trigger an update.

## Output

Use [template.md](template.md). Save with the process, for example `runbooks/weekly-invoice-run.md`. Never include passwords, tokens or keys; say where they are held and who can grant access. Do not repeat a secret's value in your reply either: say plainly that you will not include it, name it only by what it is ("the bank password"), and advise rotating it because it was pasted into a chat.

## Checks

- Every step is marked seen, told or from design.
- Steps give the expected result, not just the action.
- Failures, rollback and an escalation list are present.
- No secrets appear in the text, and none is repeated in the reply.
- A person who did not build the process has followed it, or the runbook says "untested".
