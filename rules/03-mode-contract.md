# Control 3: Mode contract

**The rule:** What an agent can do is separate from what it may do. Agree an access level for each task, start read-only, and widen only when the owner says so.

Serves rule 1, [Stop at the boundaries](../docs/controls.md). Matters in every step, and most in **Build**.

## Why it exists

An agent connected to a shared drive and a mailbox can do almost anything. Capability says nothing about permission. Imagine a manager at a small lettings firm asking an agent, "what's the situation with the roof repair quote?" The agent can read the contractor's thread, so it reads it. It can also reply, so it replies, confirming a date it guessed. The question was read-only. The tools were not.

An access level states, in words, what this task allows. The tools stay the same; the permission changes with the level.

## The four access levels

Agree one of these per task. They describe how far the agent may reach, from least to most.

| Access level | The agent may | The agent may not |
|---|---|---|
| Read-only | Read the named sources, summarise, classify, ask questions and say what it would do | Change anything outside its own notes; contact anyone |
| Propose | Everything above, plus write plans, drafts, acceptance examples and recommended changes into the task record | Apply a change to the thing being worked on; run anything with side effects |
| Change inside the project | Everything above, plus edit files or records inside the named project to the agreed acceptance, and run local checks | Touch anything outside the project; send, spend, delete, publish or deploy |
| Act outside the project | Take one named external action, for one named step, after a named person's yes | Anything beyond the named action; repeat it later without a new yes |

The last level is deliberately narrow. External actions are covered by [control 4](04-stop-boundaries.md) and, for high-risk work, by the split in [control 8](08-two-session-execution.md). A coordinating agent that supervises several workers holds no extra authority: it reports, it does not approve, and it cannot widen a worker's level.

## What the agent does

1. Starts every task read-only unless the owner names a higher level in the request.
2. States the access level in the first line of the task record.
3. Stays inside the level. If the work needs more, it stops and asks, naming the step that needs it and why.
4. Treats the level as a ceiling, not a target. Permission to change files does not oblige it to change them.
5. Records when the level changed, who changed it and for which step.
6. Drops back to the narrowest level once the widened step is finished.

## What a person does

- Sets the level when assigning the work, in plain words: "just tell me what you find" is read-only; "draft the plan" is propose; "make the change in the repo" is change inside the project.
- Widens the level deliberately, one step at a time, and says what the widening covers.
- Reads the level line in the record before reading the output. If the output did more than the level allowed, that is a defect to report, not a favour.

## Examples

**A business task.** An operations director asks for a summary of unanswered supplier emails.
- Read-only is enough: the agent reads the mailbox and lists the threads.
- She then says "draft chasers". The level moves to propose: drafts go into the record, nothing is sent.
- Sending a chaser is an external action. She approves each one by name, and the agent returns to read-only afterwards.

**A technical task.** A developer asks why a nightly import fails.
- Read-only: the agent reads logs and code and explains the cause.
- The developer says "fix it in the importer". The level moves to change inside the project: the agent edits the importer and runs local tests.
- Deploying the fix is outside the project. It needs the owner's yes, and the agent does not deploy on its own.

## The format

First line of the task record:

```
access: propose | widened: none | owner: Priya | project: supplier-chasers
```

## Sizing by risk

- **Small work:** read-only or propose is nearly always enough. Say so in a clause.
- **Normal work:** propose first, then change inside the project for the build step.
- **High-risk work:** change inside the project for building the draft only. The action itself needs [control 4](04-stop-boundaries.md) and [control 8](08-two-session-execution.md).

## Common mistakes

- Starting with wide access "because the tools are there".
- Treating a connector permission as the task's permission. Connector permissions are set in the [security guardrail](guardrails/security.md); the access level sets what a task uses of them.
- Letting a coordinating agent slide into authority over its workers' output.
- Widening for one step and never narrowing again.
- Writing the level in the prompt but not the record, so the next session starts without it.

## How to check it is working

- Every task record starts with an access line.
- Compare the record's level to the tools actually called in the session log. No call should exceed the level.
- Ask the agent, mid-task, "what access do you have and what would you need to go wider?" It answers without hesitation.
- A test task phrased as a question ("what is the status of X?") ends with an answer and no side effects.

## Related

[Control 4: stop boundaries](04-stop-boundaries.md) · [Control 8: two-session execution](08-two-session-execution.md) · [security guardrail](guardrails/security.md) · [rules index](README.md)
