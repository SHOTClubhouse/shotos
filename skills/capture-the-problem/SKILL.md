---
name: capture-the-problem
description: "Turns rough notes, a complaint, an idea or a request into a problem statement: who is affected, the cost, what is unknown and the cheapest first test. Use when a request describes a solution rather than a problem."
---

# Capture the problem

Before building anything, write down what is actually wrong. Most wasted work starts with a solution nobody checked against a problem.

## Context and handoff

Read the requester’s description and a concrete occurrence. Separate who experiences it, its effect and the solution they initially asked for.

Use `stakeholder-map` if ownership is unclear. Keep the brief and baseline question with the task.

## When not to use this

Skip it for a small, clear change where the problem is obvious and the fix is cheap to undo, such as a typo, a broken link or a one-line config change.

## Steps

1. **Start with the request and one concrete occurrence.** If the task includes a large set of files, start with the owning record and the most relevant example. Open another source only to resolve a gap that could change the problem, owner or first test. Separate what the person reported from what the sources directly show, and separate both from their proposed solution.
2. **Name who is affected.** List the people or teams who feel the problem, and who decides whether it is fixed.
3. **Describe today.** Describe the known steps and mark anything that is inferred or missing. Say what it costs: time, money, errors, missed chances or frustration. Use a number when the source gives one. Write "not measured" when it does not. Never invent a figure.
4. **State the problem in one or two sentences.** Name who has it and what it causes. Do not mention the solution.
5. **List the unknowns.** Say what would change the answer if it turned out differently.
6. **Propose the cheapest first test.** Name the smallest thing that would show whether the problem is real and worth solving. It could be a conversation, a count or a quick prototype.
7. **Stop.** Do not start building. Hand the statement back for the owner to confirm.

## Output

Use [template.md](template.md) in this skill's folder. Keep it under one page.

## Checks before handing back

- The problem statement contains no solution.
- Every number has a source or is marked "not measured". A reported symptom stays attributed until verified.
- There is at least one unknown, and one test that could prove the problem is not worth solving.
- A named person owns it. For anything large, risky or unclear, they confirm it before work starts; otherwise it is shared with them as the work begins.
