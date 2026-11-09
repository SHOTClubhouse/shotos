---
name: learning-loop
description: "Turns mistakes and wins into improvements: observe, diagnose, propose, test, promote, check. A rule needs evidence, a test, a contrary case and authority; one case is weak evidence, so name where the rule would be wrong. Use before adding any rule."
---

# Run the learning loop

Improve the method from real events without piling up rules nobody can justify. A lesson is a suggestion until it has passed every test below.

Stage: Sustain and Scale. Rules: 2 Agree acceptance first, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Read the accepted outcome and recurring exceptions. Prefer a change tied to observed behaviour with a clear owner and review date.

Use `skill-quality-gate` when changing a skill. Link the learning entry to the affected work.

## When not to use this

For a small team, a lesson record can be six lines: event, cause, one change, contrary case, owner, review date. Skip it for a one-off mistake with a clear local fix and no sign of repeating. Do not use it to change a rule that someone else owns without their yes, or to write a rule because one case felt bad.

## Steps

1. **Observe.** Record the event in plain facts: what happened, when, in what task class, with a link to the output, log or review note. Add how often it has happened, from the records, and count similar events that went well. Do not diagnose yet.
2. **Diagnose.** Say why it happened. Check the likely causes in order: the input was wrong or missing, the instruction was unclear or conflicting, the skill lacked a step, the model made a slip, the reviewer's standard changed, the world changed. Mark each cause as shown, suspected or ruled out, and what showed it. If you cannot tell, say so and plan the cheapest way to find out.
3. **Propose.** Write one candidate change in plain words, as small as possible: a new check, a reworded step, an added example, a changed boundary. Say what it replaces, what it adds and what it could make worse. One change per proposal.
4. **Test.** Before promoting, show evidence and run a test.
   - Evidence: the events that support it, with sources and counts, and how strong they are.
   - A test that would have caught the original event: an eval case with an input, must-contain and must-not-contain.
   - A contrary case: a situation where the new rule would be wrong or unhelpful, and what the agent should do there. If you cannot find one, look harder; a rule with no contrary case is probably too broad.
   - Run the old and new version on the cases and read the results. Use `skill-quality-gate` for skills.
5. **Check authority.** Name the person who owns the instruction and can change it. If the change touches a boundary, a privacy rule or a shared standard, that owner must say yes. The agent proposes; the owner promotes. If the owner insists on adding a rule from one case with no testing, their request is the yes. Add exactly what they asked for, in the one place, labelled "untested, from one case". In the same message say that one case is thin evidence, name the contrary case where the rule would be wrong (for example, a real mistake that deserves an apology), set a review date, and say in the report that no test was run. Never call it tested.
6. **Promote.** Record how to withdraw it: the signal that it is hurting (for example, the contrary case appearing twice, or more rework) and who can remove it before the review date. Record the rule with all six parts: evidence, test, contrary case, the authority (who approved and when), a review date and what it supersedes (the older rule or text it replaces, with a pointer). Add the eval cases to the project. Change the instruction in one place only.
7. **Check later.** Put the review date on the owner's calendar or task list, not only in the record. On the review date, look at the events since: did the problem fall, did the contrary case appear, did anything get worse. Keep, change or remove the rule, and record that decision. A rule nobody has reviewed is a candidate for removal.

## Output

Use [template.md](template.md): one lesson record per proposal. Keep the records together in the project, for example `.work/lessons/`.

## Checks

- The lesson record has evidence with counts, a test, a contrary case, an approving person, a review date and a supersedes line.
- Diagnosis lists causes ruled out as well as likely ones.
- The change is one change and the smallest that would do.
- The agent did not promote its own proposal.
- A rule added at the owner's insistence is labelled untested and from one case, names its contrary case, has a review date, and the report says so.
- A promoted rule says what would make it be withdrawn early and who can do that.
- A promoted rule has a review date that has been put in a place someone will see.
