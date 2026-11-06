# resume-pack

**Before a session ends or context fills, leave a short, clean pack that lets the next session carry on without the conversation.**

The agent updates the owning record, then writes a one-page pack: the state, the files, decisions, pending manual steps, the exact next prompt and the learnings. It holds metadata only. It strips secrets, personal data and raw conversation.

It works at any stage. It serves rule 4, Claim only what you can show, and rule 1, Stop at the boundaries. It is the practical form of control 11, context-control.

## The problem it solves

At a fictional firm, Harbourside Lettings, an agent is half way through moving the tenant-deposit reminders to a new table. The session fills. The next session starts from a vague summary, assumes the database change was already applied, and writes code against a column that does not exist yet. A run then fails on a Friday.

The pack lists the migration as pending, names who can apply it, says how to confirm (the column exists), and gives a next prompt that starts with that check.

## When to use it, and when not to

Use it when stopping mid-task, when the context window is nearly full, and when work passes to someone else. Skip it when the work is finished (use [evidence-handoff](../evidence-handoff/README.md)) or the chat has nothing to continue.

## Who it is for

- **Engineering or practice lead:** reliable pause and resume across sessions.
- **Small team lead:** a way to hand a task to a colleague or another agent.
- **Solo founder:** pick up tomorrow exactly where you stopped.
- **Product owner:** a visible list of manual steps that are waiting.

## How to use it

Ask:

> The context is nearly full. Write a resume pack for the deposit reminders task. List any database changes still to apply. Leave out anything secret.

Read the pending steps and the next prompt, then start a fresh session with the prompt.

## How it connects

- **Related:** [evidence-handoff](../evidence-handoff/README.md) closes finished work. [runbook](../runbook/README.md) holds steady-state process. [learning-loop](../learning-loop/README.md) takes the learnings on.
- **Control:** control 11, [context control](../../rules/11-context-control.md), one of the [twelve controls](../../rules/README.md) behind the four rules.

## Needs

Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 1 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Update the owning record first. The pack is a pointer to it.
- Mark pending steps as pending, never as done.
- Paste no secrets. Say where they live.
- Overwrite the old pack so there is one latest.

## Limits

- It records what the agent knows. If something was not read back, it goes in "not verified".
- It does not stop a person from approving the wrong thing in the next session.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/resume-pack/input.md) and [output](../../examples/resume-pack/output.md).
