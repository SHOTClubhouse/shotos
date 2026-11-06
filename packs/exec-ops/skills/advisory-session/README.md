# advisory-session

**Prepare and run an advisory session so the group's time goes to one question and every action has one owner.**

The agent writes the group's mandate, maps what each member can contribute, plans the session around progress, one main question and actions, and captures what was actually said apart from any AI view. It produces one action record with one owner per action, and a handoff for the next session. It drafts everything and sends nothing.

It serves the Own stage. Rules: 1 Stop at the boundaries, 4 Claim only what you can show.

## The problem it solves

The chair of the Millbrook Rovers volunteer advisory group runs a two-hour session on seven topics. Afterwards, three people think they own the fundraising action and nobody owns the pitch-hire contract. The minutes include a recommendation from the assistant that members remember as the group's view.

With the skill, there is one main question, the minutes say what members said, the assistant's suggestion sits under "AI view, not the group's", and each action has a single named owner or says "owner needed".

## When to use it, and when not to

Use it for advisory groups, working groups and board committees where members advise and a leader decides. Skip it for one-to-one meetings or groups whose members have not agreed to take part.

## Who it is for

Chairs, chiefs of staff, secretaries and the leaders who consult a group.

## How to use it

> Prepare next Tuesday's advisory session for the youth club group. Main question: should we add a Saturday junior session. Last session's actions are in the notes folder. Draft the plan and pre-read; I will send them.

Output uses [template.md](template.md). Worked example: [input](../../examples/advisory-session/input.md) and [output](../../examples/advisory-session/output.md).

## How it connects

- **Before:** [decision-brief](../decision-brief/README.md) supplies the main question and paper.
- **Capture:** [meeting-notes](../meeting-notes/README.md) for recordings and transcripts.
- **After:** actions go into the [daily-brief](../daily-brief/README.md) ledger once the chair confirms them.

## Needs

Document connector to read terms of reference and previous notes, read-only. A transcript connector or the chair's notes for capture. Mail and calendar only to read availability; invitations are drafted for the chair.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 0 of 2, Sonnet 1 of 2, Opus 1 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- One main question per session. Park the rest in a list.
- Show the AI view in its own box so nobody mistakes it for the group.
- An action without an owner is a finding, not a task.
- Ask members before sharing what they said outside the group.

## Limits

- The map only holds what members have said or published; private views are not inferred.
- Attribution depends on knowing who spoke; unknown speakers stay unnamed.
- It cannot make members attend or act.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/advisory-session/input.md), [example output](../../examples/advisory-session/output.md).
