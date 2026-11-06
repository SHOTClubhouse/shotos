---
name: agree-acceptance
description: "Agrees what done looks like before work starts: concrete checks, who accepts, what the agent must not do, plus examples (one failing) for variable output. Use when starting any task whose result someone else will rely on."
---

# Agree acceptance before work

Write down how everyone will know the work is finished before starting it. It takes five minutes and saves the rework that comes from building the wrong thing well.

## Context and handoff

Read the actual request and last accepted comparable result. Identify the named person who can accept and what evidence would make them reject it.

Use `example-mapping` when rules are ambiguous. Save the card with the task and link it from the handoff.

## When not to use this

Skip it for a quick answer to a question, or a trivial change the person can check at a glance. One sentence of expected result is enough there.

## Steps

1. **Name the owner.** One person accepts the work. If nobody will accept it, ask who should before starting.
2. **Write the outcome in one sentence.** Say what will be true afterwards that is not true now.
3. **Write the checks.** List three to seven observable checks that a person or a command can verify. Use this form where it helps:
   - Given a starting situation, when something happens, then this observable result.
4. **Add a failure example.** Describe at least one input or situation where the work should refuse, warn or stop. A set of checks that cannot fail is not checking anything.
5. **For variable output, write a small example set.** When the work is AI-written text, a summary, a classification or anything that varies between runs, list three to ten example inputs with what a good answer must contain and must not contain. This is the eval set. Keep it in the project, not in the chat.
6. **Set the boundaries.** List what the agent must not do without the owner's yes. Always include sending or posting anything external, spending money, deleting, deploying, publishing, and changing someone else's work.
7. **Get confirmation when it matters.** For large, risky or unclear work, show the card to the owner and wait for a yes or for changes before doing the work. When the request already states what done looks like and nothing on the card crosses a boundary, write the card from the request, name your assumptions on it, and start; the owner can correct the card while you work. If one part is unclear or contradictory, do the rest and park that part with a question.

## Output

Use [template.md](template.md) in this skill's folder. Save it with the work, for example `.work/<task>/acceptance.md`.

## Checks before starting the work

- Each check could be verified by someone who was not in the conversation.
- At least one example should fail.
- Boundaries are listed. For large, risky or unclear work the owner has confirmed; otherwise the card is written from the request with its assumptions named.
