# Control 11: Context control

**The rule:** Keep one owning record per task, pass on metadata and decisions rather than raw conversation, and work within a stated context and token budget.

Serves rule 3, [Read back the real result](../docs/controls.md), because a result built on a lost or inflated context cannot be read back reliably. Matters in every step and most in **Build** and **Improve**.

## Why it exists

Three agents and two people at Harbourside Lettings work on one tenancy review across a fortnight. Each session starts by pasting in the earlier chat. By the fourth session the paste is forty pages, half of it superseded. The agent follows an instruction from day two that the owner withdrew on day five, and a private note about a tenant's family circumstances travels into a report for the landlord. Nobody meant any of that. The context simply grew without an owner.

Long context costs money, hides the instruction that matters, and carries private detail into places it should not go. A short, owned record does the same job better.

## What the agent does

1. Finds or creates the **one owning record** for the task before starting: a file in the project, such as `.work/<task>/record.md`. If one exists, it works from it and does not start another.
2. Keeps in the record, and only in the record: the route line, the mode, the acceptance card, decisions with who made them and when, the current state, the next action, evidence references, and open questions.
3. Writes **metadata-only continuity**: when handing on, it passes the record and links to evidence, not the transcript. It does not copy raw chat, personal messages or sensitive source text into the record. It names the file and the line instead.
4. Works to a stated **context budget**, for example: read at most these files, summarise rather than paste, and clear any source not needed for the next step. If the work needs more, it says so and asks.
5. Updates the record at each checkpoint: after acceptance is agreed, after each substantial step, before a session ends and before handing over.
6. Marks superseded decisions as superseded. It does not delete them.
7. Starts a fresh session for a distinct task, or when the current one has grown noisy, and reloads only the record.

## What a person does

- Names where the record lives, once, for the project.
- Reads the record rather than the chat to see where things stand.
- Corrects the record directly when something is wrong, and says so in the next message.
- Sets the budget when cost or speed matters, for example "no more than ten files, no external lookups".
- Keeps private material out of the record and out of prompts.

## The format

A task record is short, with these headings:

```
task: tenancy review, Harbourside Lettings | owner: Maya | mode: 1 | updated: 2026-03-04 16:10
route: asset: review note | job: summarise | risk: personal-data | reader: Maya | route: owner review | proof: Maya checks 5 cases
acceptance: acceptance.md (agreed 2026-03-02)
decisions: (1) use 2025 cases only, Maya, 03-02. (2) [superseded] include arrears, withdrawn 03-04.
state: 31 of 40 cases summarised | next: finish remaining 9, then read back
evidence: .work/tenancy/cases-summary.md, .work/tenancy/checks.log
open: ask Maya whether disputed cases are in scope
budget: read cases folder only; no external sources; summaries not full text
```

A **context budget** has three numbers where practical: files or sources read, size of anything pasted, and the number of sessions before the record is rewritten.

## Sizing by risk

- **Small work:** no record; the chat is the record. If it takes more than one session, make one.
- **Normal work:** one record, updated at the checkpoints above.
- **High-risk work:** the record also lists who has seen what, which data classes are involved under the [data governance guardrail](guardrails/data-governance.md), and the approvals. The handoff is reviewed before another session or person picks it up (the `evidence-handoff` skill produces one).

## Common mistakes

- Starting a second record for the same task "to keep it clean".
- Treating the transcript as the record.
- Copying sensitive text into notes for convenience.
- Never pruning, so the record becomes the forty pages it replaced.
- Writing decisions without a name or date.
- Letting the budget slip silently. Say when it is exceeded and why.

## How to check it is working

- One record per active task, in the agreed place. A new session can pick up in minutes from the record alone.
- Grep the records for personal data classes that should not be there. None appear unless the task needs them.
- Open the record and ask: can I tell the current decision, the next action and who decided? If not, repair the record.
- Session start-up size trends down or stays level.

## Related

[Control 1: route the work](01-route-the-work.md) · `evidence-handoff` skill and its [README](../skills/evidence-handoff/README.md) · [handoff template](../templates/handoff.md) · [productivity guardrail](guardrails/productivity.md) · [rules index](README.md)
