# evidence-handoff

**Pass work on so the next person can continue in minutes without asking you anything.**

This skill writes a one-page handoff. It states whether the work is prepared, executed or accepted, points to the evidence, lists open decisions and what was not checked, gives one concrete next step and adds a resume prompt to paste into the next session.

It supports the Hand over step, where a team becomes able to carry the work on. It serves rule 4, Claim only what you can show, and rule 2, Agree acceptance first, because the handoff says which acceptance checks passed.

## The problem it solves

A consultant is pausing a supplier comparison for a client. A colleague will pick it up next week. Without a handoff, the colleague spends the first morning reading folders, working out which scores are sourced, guessing what the client still has to decide and asking the first consultant, who is now on another project.

The same happens when an agent session ends and another begins, or when a team passes work to a customer.

## What the agent does differently

Without the skill, an agent can write a sensible summary and still skip the structure: no state, no resume prompt, no named decision. With the skill, the output looks like [examples/evidence-handoff/output.md](../../examples/evidence-handoff/output.md).

The state is exact and does not oversell:

> **Executed.** Checks 1 to 3 of the acceptance card pass (all three suppliers scored on the agreed six criteria, each score sourced). Check 4, a reference call with one current customer per supplier, is not done.

The open decision has an owner:

> Whether supplier B's missing pension feature rules it out | Client finance director | Before the reference calls

The next person can start at once:

> "Continue the payroll supplier comparison. Read work/payroll/HANDOFF.md and acceptance.md. Scoring is complete; reference calls and the supplier B decision are outstanding."

It ends with a Claims block, including `[unverified] supplier C pricing for the client's size`.

## When to use it, and when not to

Use it when pausing, ending a session, passing work to a colleague or customer, or whenever a task will continue later.

Skip it for work that is finished and accepted, with nothing left to pick up. A short report is enough.

## Who it is for

- **Small team lead:** work moves between people without a meeting.
- **Engineering or practice lead:** consistent handoffs between shifts, sessions and agents.
- **Business unit leader:** you can see what is accepted and what is only drafted.
- **Product owner or analyst:** open decisions are named, with who decides and by when.
- **Solo founder:** a note to your future self, or to the agent you start tomorrow.
- **Enablement coach:** a good model for client handover, where the aim is to leave a team more capable.

## How to use it

Install SHOTos as described in the [main README](../../README.md#install). Then ask:

> End of day handoff: website copy rewrite. Pages done: home, pricing, about. Not done: FAQ, contact. Drafts are in copy/drafts/. Nobody has reviewed anything yet. Write the handoff for tomorrow's session.

You get a page on [template.md](template.md), saved beside the work, for example `.work/<task>/HANDOFF.md`.

On paper: print the template and fill in the state first. Choose one of prepared, executed or accepted and delete the other two. If you pick accepted, write down where the record is.

## How it connects

- **Before:** [capture-the-problem](../capture-the-problem/README.md) gives the unknowns that often become open decisions.
- **Before:** [agree-acceptance](../agree-acceptance/README.md) provides the checks the state refers to.
- **With:** [report-with-evidence](../report-with-evidence/README.md) supplies the Claims block at the end of the handoff.

## How it is tested

The skill has five cases in [evals/cases.json](../../evals/cases.json). Three are normal: a payroll comparison, a website copy rewrite and an onboarding checklist. Two are contrary: the agent should not mark everything accepted because a client nodded, and should not invent a migration status it cannot see.

From the paired run in [docs/evidence.md](../../docs/evidence.md): evidence-handoff passed 5 of 5 cases with SHOTos and 3 without, at $0.58 against $0.33. That is the largest cost gap of the four skills.

The caveat: "One run per case per condition, on one model. Agent output varies between runs." The grader checks for key words, some of which match the skills' own wording.

## Tips and common mistakes

- Never write accepted without a record. A nod in a meeting is not one.
- Use paths and links in the evidence list, not descriptions.
- Give one next step, not five, and say how the reader will know it worked.
- Keep it to one page and link to detail.
- Test the resume prompt by pasting it into a fresh session.

## Limits

- A handoff is only as good as the state it records. If the agent cannot see the files, it must say so and mark what it cannot confirm.
- It does not make a person read it.
- It cost more than a loose summary in the paired run.
- One model, one run per case. Codex has not been tested.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/evidence-handoff/input.md) and [output](../../examples/evidence-handoff/output.md).

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 5 of 5, Sonnet 5 of 5, Opus 5 of 5. Without: Haiku 5 of 5, Sonnet 5 of 5, Opus 5 of 5. See [evidence](../../docs/evidence.md) for how to read this.
