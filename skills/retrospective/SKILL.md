---
name: retrospective
description: "Runs a short blameless retrospective: what we expected, what happened, why, and what we change, with an owner and date each. Use when a pilot, release, incident or project phase ends, or after a surprise. Not for appraising people."
---

# Run a blameless retrospective

Look at the work honestly, find causes in the system and not in people, and leave with a few changes that have an owner and a date. Keep it short.

Stage: Track and Sustain. Rules: 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Read the agreed goal, actual outcome and observed friction. Separate anecdotes from repeated signals and agree one change to try.

Use `learning-loop` to track the change. Record owner and next review with the retrospective.

## When not to use this

Skip it for tiny tasks with nothing to learn. Do not use it to assign fault, to appraise a person, or to settle a dispute. If a person's conduct is the question, that is a different process with different people.

## Steps

1. **Set the scope and the people.** Name the piece of work, the period and who took part (the people who did the work, plus the person who accepted it). Keep to eight people or fewer. The agent prepares and writes up; people supply what happened.
2. **Collect what was expected.** Pull it from the problem statement, acceptance card, plan and evidence pack, with dates. Do not reconstruct expectations from memory if a record exists; if none exists, say that expectations were not written down.
3. **Collect what happened.** Build a short timeline from the records (decisions, releases, incidents, changes of plan, measures). Add people's own accounts as accounts, labelled by role, not by name where blame could follow. Include what went well and what was luck.
4. **Compare.** List the gaps between expected and actual in both directions: worse than expected and better than expected. For each, say how big, with a figure from the evidence where there is one.
5. **Ask why, in the system.** For the three to five biggest gaps ask "what in our setup made this likely?" at least three times. Look at information, tools, timing, handoffs, unclear acceptance, missing review, pressure and unclear owners. Rule out "someone should have been more careful": it is not a cause. If a cause is a guess, mark it.
6. **Choose a few changes.** Pick at most five. For each: the change, which cause it answers, how we will know it worked, one named owner and a date. Do not add changes without an owner. Some gaps get "accept and watch" instead of a change, and that is recorded.
7. **Check authority.** If a change touches a boundary, a shared standard or budget, name who must approve it. The agent does not make those changes.
8. **Feed the other loops.** Pass any candidate rule to the `learning-loop`, any evidence to the next `evidence-pack` and any shared decision to a `decision-record`.
9. **Share it in the right circle.** The write-up goes to the people involved and the sponsor. Anything about named individuals' performance stays out. Drafting only; a person circulates it.
10. **Follow up.** On each date, check whether the change was made and whether it did what was expected. Record the answer on the same page.

## Output

Use [template.md](template.md). One page, maximum two. Save as `.work/<task>/retrospective.md`.

## Checks

- Expectations come from records, or the page says none were written.
- Every gap has a cause in the system, and guesses are marked.
- No sentence blames a named person for an outcome.
- At most five changes, each with one owner, a date and a measure of success.
- Better-than-expected results are included.
