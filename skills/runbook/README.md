# runbook

**Write down how a process really runs, so someone who did not build it can run it, fix it and roll it back.**

The agent builds the runbook from logs, history and the builder's account, marks each step as seen, told or from design, and adds checks, failure handling, rollback and who to call. A person who did not build the process then follows it, and the gaps they hit get fixed.

It supports the Own stage. It serves rule 3, Read back the real result, rule 4, Claim only what you can show, and rule 1, Stop at the boundaries, for irreversible steps.

## The problem it solves

At a fictional firm, Harbourside Lettings, one analyst runs the monthly landlord statements by a mix of a script, a spreadsheet and a few clicks in the accounts system. She goes on leave and the run is two days late, because the script needs an export that only she knows to take first.

The runbook captures the export step, the check that totals match the ledger, what to do when the script stops half way, and the rule that nothing is emailed to landlords until the finance lead says yes.

## When to use it, and when not to

Use it when a process or automation becomes someone else's job, or depends on one person's memory. Skip it for a one-off task. Do not write one for a process nobody has run; mark it a draft from design.

## Who it is for

- **Operations or business unit leader:** continuity when someone is away.
- **Small team lead:** a shared way to hand over.
- **Engineering or practice lead:** a runbook for an automation or release.
- **Enablement coach:** the main written asset for the exit test in [enablement-plan](../enablement-plan/README.md).

## How to use it

Ask:

> Write a runbook for the monthly landlord statement run, from the script, the shell history and my notes. Mark which steps you have seen. Then give me a checklist for a colleague to test it.

You get a runbook on [template.md](template.md). Ask a colleague to follow it while you watch, and record any help they needed. Use the [handover exercise](handover-exercise.md) to check how evidence carries between revisions.

## How it connects

- **Before:** [report-with-evidence](../report-with-evidence/README.md) shows the process works.
- **After:** [enablement-plan](../enablement-plan/README.md) trains the team, and [resume-pack](../resume-pack/README.md) carries context between sessions. [rollout-plan](../rollout-plan/README.md) reuses the runbook for the next team.
- **Boundaries:** see rule 1 in [docs/controls.md](../../docs/controls.md).

## Needs

Read access to logs, history and scripts. Nothing beyond the agent otherwise.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Test with someone new. The builder will skip steps without noticing.
- Write the expected result after each step.
- Keep secrets out; say where they live.
- Put the irreversible step behind a named yes.

## Limits

- A runbook goes out of date as the process changes. Set a review date.
- Steps marked "told" or "from design" may be wrong until tested.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/runbook/input.md) and [output](../../examples/runbook/output.md).
