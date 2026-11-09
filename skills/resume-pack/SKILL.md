---
name: resume-pack
description: "Writes a resume pack when a session ends or context fills: handoff note, exact next prompt, pending manual steps and learnings, with no secrets or raw conversation. Use when pausing unfinished work for another session. Use evidence-handoff when a new owner needs to take over."
---

# Write a resume pack

Leave enough for a fresh session to carry on correctly, and nothing that should not be stored. The pack points to files; it does not copy conversations.

Stage: any. Rules: 4 Claim only what you can show, 1 Stop at the boundaries. Supports control 11, context-control.

## Context and handoff

Read the previous decision, existing files, actual open tasks and unresolved checks. Verify state before picking up the next action.

Use `evidence-handoff` if responsibility changes. Link this pack from that handoff if unfinished work needs detailed restart instructions. Update the existing task record with recovery instructions.

## When not to use this

Skip it when the work is finished and handed over with an `evidence-handoff`. Skip it for a short chat with nothing to continue. Do not use it to store a conversation.

## Steps

1. **Find the owning record.** Work has one place where its state lives (a task file, an issue, a folder). Update that record first. The pack summarises and points to it; it does not replace it.
2. **Write the state in a few lines.** What the task is, the stage, what is done and checked, what is in progress, what is blocked and by whom. Label each item done and checked, done but unchecked, or planned.
3. **List files and where they are.** Give relative paths, branch names and commit identifiers for the work touched. Say which are uncommitted. Do not paste the contents of files.
4. **List decisions made and open questions.** One line each with the date and who decided. Mark anything the agent assumed.
5. **List pending manual steps.** Things that have not been done and need a person: database changes still to apply, environment settings to change, approvals to obtain, messages to send, releases to trigger. For each one: what, where, who can do it, the order, and what proves it was done. Mark any irreversible step.
6. **Write the exact next prompt.** A paragraph the next session can paste: the goal, the first file to read, a read-only first check, the acceptance in one line, and the boundary. Ask the next session to compare the current task status and artefact revision with the checkpoint. Reopen the checks or approvals affected by any difference before acting. Confirm evidence for a pending action before attempting it, so it is not done twice. If access is missing, name who can provide the evidence. The prompt should work with no memory of this session.
7. **Record learnings.** What worked, what failed and why, and any suggested rule or skill change, labelled as a suggestion for the `learning-loop`. Keep these as short, factual sentences.
8. **Record the way back.** For uncommitted or half-applied work, give the last known good point (commit, copy, backup) and how to return to it. Say what to stop and ask about if the checks in the next prompt do not match.
9. **Strip it.** Remove anything that looks like a secret (keys, tokens, passwords, connection strings), personal data about private individuals, private message text and raw conversation. Replace with where the item is held and who can grant access.
10. **Say what you have not verified.** List claims in the pack that rest on memory of the session instead of a file you read back.
11. **Save it where the next session will look,** for example `.work/<task>/resume.md`, updating the existing pack when it belongs to this task and you are authorised to edit it. Keep it under one page where possible. Add the date, and treat a pack older than the owning record's last change as stale until checked.

## Output

Use [template.md](template.md).

## Checks

- The next prompt starts from current evidence with no other session context, and says how to handle a changed revision, status or authority.
- Pending manual steps name who does them and how to confirm.
- A last known good point and a stop condition are given for unfinished changes.
- No secrets, personal data or raw conversation text appear.
- Items are labelled done and checked, done but unchecked, or planned.
- The pack points to the owning record and does not duplicate it.
