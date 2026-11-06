---
name: resume-pack
description: "Writes a resume pack when a session ends or context fills: handoff note, exact next prompt, pending manual steps and learnings, with no secrets or raw conversation. Use when stopping mid-task or passing work on. Finished work uses evidence-handoff."
---

# Write a resume pack

Leave enough for a fresh session to carry on correctly, and nothing that should not be stored. The pack points to files; it does not copy conversations.

Step: any. Rules: 4 Claim only what you can show, 1 Stop at the boundaries. Supports control 11, context-control.

## When not to use this

Skip it when the work is finished and handed over with an [evidence-handoff](../evidence-handoff/README.md). Skip it for a short chat with nothing to continue. Do not use it to store a conversation.

## Steps

1. **Find the owning record.** Work has one place where its state lives (a task file, an issue, a folder). Update that record first. The pack summarises and points to it; it does not replace it.
2. **Write the state in a few lines.** What the task is, the step, what is done and checked, what is in progress, what is blocked and by whom. Label each item done and checked, done but unchecked, or planned.
3. **List files and where they are.** Give relative paths, branch names and commit identifiers for the work touched. Say which are uncommitted. Do not paste the contents of files.
4. **List decisions made and open questions.** One line each with the date and who decided. Mark anything the agent assumed.
5. **List pending manual steps.** Things that have not been done and need a person: database changes still to apply, environment settings to change, approvals to obtain, messages to send, releases to trigger. For each one: what, where, who can do it, the order, and what proves it was done. Mark any irreversible step.
6. **Write the exact next prompt.** A paragraph the next session can paste: the goal, the first file to read, the first command or check to run, the acceptance in one line, and the boundary. It should work with no memory of this session.
7. **Record learnings.** What worked, what failed and why, and any suggested rule or skill change, labelled as a suggestion for the [learning-loop](../learning-loop/README.md). Keep these as short, factual sentences.
8. **Strip it.** Remove anything that looks like a secret (keys, tokens, passwords, connection strings), personal data about private individuals, private message text and raw conversation. Replace with where the item is held and who can grant access.
9. **Say what you have not verified.** List claims in the pack that rest on memory of the session instead of a file you read back.
10. **Save it where the next session will look,** for example `.work/<task>/resume.md`, overwriting the previous pack for this task so only the latest remains. Keep it under one page where possible.

## Output

Use [template.md](template.md).

## Checks

- The next prompt could start a session with no other context.
- Pending manual steps name who does them and how to confirm.
- No secrets, personal data or raw conversation text appear.
- Items are labelled done and checked, done but unchecked, or planned.
- The pack points to the owning record and does not duplicate it.
