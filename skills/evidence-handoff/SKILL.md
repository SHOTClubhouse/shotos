---
name: evidence-handoff
description: Hands work to a person, team, agent or later session with state, evidence, open decisions and next step intact. Use when pausing work, ending a session or passing work on. Final task claims use report-with-evidence; Track results use evidence-pack.
---

# Evidence handoff

A good handoff lets the next person continue in minutes without asking you anything.

## Context and handoff

Read the task record, original acceptance, actual output and receipts. Verify the current state independently of the previous status report.

Use `resume-pack` for a new session. Keep one handoff linked to the artefact, open checks and named next action.

## Steps

1. **State where the work is.** Pick one: *prepared* (drafted, not run or checked), *executed* (done and checked against the acceptance checks) or *accepted* (the owner said yes, with the record). Say which checks passed and which did not.
2. **Point to the evidence.** List where the work and its proof live: files, commits, documents, receipts. Use paths or links, not descriptions.
3. **List open decisions.** Say what needs a person's decision, who that person is and by when, if a date exists.
4. **List what is not done or not checked.** Include known risks and anything you assumed.
5. **Give the next step.** Write one concrete action the next person can take straight away, and how they will know it worked.
6. **Write a resume prompt.** Add two or three sentences the next person or agent can paste to pick up the work.
7. **Keep it short.** One page. Link to detail rather than copying it.

## Output

Use [template.md](template.md) in this skill's folder. Save it beside the work, for example `.work/<task>/HANDOFF.md`, and end with a Claims block (see the report-with-evidence skill).

## Checks

- Someone new could take the next step without asking a question.
- The state is one of prepared, executed or accepted, and "accepted" has a record.
- Every claim of progress points to evidence.
