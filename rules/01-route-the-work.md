# Control 1: Route the work

**The rule:** Before starting, write one line that names the asset, the job, the risk, the reader, the route and the proof.

Serves rule 2, [Agree acceptance first](../docs/controls.md). Matters most in **Brief**, where a wrong route wastes the most effort.

## Why it exists

Priya at Harbourside Lettings asks an agent to "sort out the tenancy renewal letters". The agent starts drafting forty letters. Halfway through, Priya mentions that three tenants are in dispute and that the letters go out under the landlord's name. Nobody had said who the reader was, what the risk was, or who needed to approve. The agent had picked a route (bulk draft) that suited a routine job, and the job was not routine.

A route line takes ten seconds to write and makes that mismatch visible before any work is done.

## What the agent does

1. Reads the request and finds the **asset**: the thing that will exist or change afterwards (a letter, a spreadsheet, a pull request, a decision note).
2. Names the **job** in a few words: draft, summarise, check, change, decide, report.
3. Names the **risk**, using [control 2](02-evidence-based-risk.md): `low` unless evidence says otherwise, and says which evidence.
4. Names the **reader**: the person or system that will act on the result, and whether they are inside or outside the team.
5. Picks the **route**: do it directly, do it with a reviewer, split into review and execution sessions, or hand it to a person.
6. Names the **proof**: the observable thing that will show the work is right, as agreed under [control 5](05-acceptance-first.md).
7. Writes the line in the task record and shows it to the owner. For small work it goes in one chat message. The agent starts when the owner has not objected, unless the route includes an external action, in which case it waits for a yes.

## What a person does

- Reads the line and corrects it. The most common correction is the reader or the risk.
- Decides if the route is proportionate. A person who sees "reviewer" on a one-line fix can say "direct".
- Answers questions the agent could not answer from context, such as who approves.

## The format

One line, fields in this order:

```
asset: renewal letters (40) | job: draft | risk: elevated (3 tenants in dispute) | reader: tenants, external | route: draft then owner review | proof: owner reads 5 sampled letters and the dispute list is excluded
```

Missing fields are written as `unknown`, not left out. An `unknown` in reader or risk means the agent asks before going further.

## Sizing by risk

- **Small work** (a rewrite, a lookup, a note for yourself): the route line can be one clause in the reply. Skip the task record.
- **Normal work** (a document or change someone else will rely on): write the full line in the task record, and keep it current if the route changes.
- **High-risk work** (money, personal data, anything external, anything hard to undo): the route line is mandatory, names the approving person, and the route must include review under [control 7](07-independent-review.md) or the split in [control 8](08-two-session-execution.md).

## Common mistakes

- Writing the line after the work, as a description. It must come first, or it routes nothing.
- Choosing the route by habit. If every task is "direct", the line is decoration.
- Leaving the reader as "the team" when a named external person will receive the result.
- Treating the proof field as "tests pass". Proof is what the owner would accept, not what the agent finds convenient.
- Never revisiting it. If the agent finds a dispute, a personal-data field or an external recipient mid-task, it stops and rewrites the line.

## How to check it is working

- Open the last five task records. Each has a route line written before the first output.
- At least one line in the last five has an `unknown` that led to a question.
- No task with an external reader has a route of `direct` without a named approver.
- When work comes back rejected, ask which field of the route line was wrong. If it is always the same field, the agent needs a better prompt for that field.

## Related

[Control 2: evidence-based risk](02-evidence-based-risk.md) · [Control 5: acceptance first](05-acceptance-first.md) · the `capture-the-problem` and `agree-acceptance` skills · [rules index](README.md)
