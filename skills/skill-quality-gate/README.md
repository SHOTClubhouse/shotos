# skill-quality-gate

**Test one change to a skill on three kinds of situation, block it on any material failure, and judge cost per accepted outcome.**

The agent states a single change, compares it with the current version on a normal case, a conflicting-source case and an authority-boundary case, classes every failure as material or minor, and refuses to recommend promotion if a material factual, privacy or authority failure appears, however good the average. It also computes cost per accepted outcome including rework, assigns a maturity label and runs a disclosure checklist before anything is published.

It supports Sustain and Scale. It serves rule 2, Agree acceptance first, rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

A team at a fictional firm, Northgate Cycles, improves a customer-reply skill so it is friendlier and cheaper to run. Average scores go up. Nobody notices that, in one test, the new version invented a delivery date when the order record and the email thread disagreed. It goes live, and a customer is promised a date nobody set.

The gate runs the conflicting-source scenario, finds the invented date, labels it a material factual failure and blocks promotion, even though the average improved.

## When to use it, and when not to

Use it before changing, promoting or publishing a skill, prompt, template or agent instruction. Skip it for typo and link fixes. Do not let the author be the only grader.

## Who it is for

- **Engineering or practice lead:** a release check for skills as for code.
- **Product owner:** a clear reason a change was held back.
- **Enablement coach:** shows what "tested" means for an instruction.
- **Anyone publishing a skill:** the disclosure checklist.

## How to use it

Ask:

> Gate this change to the customer-reply skill: it adds a step that suggests a delivery date. Compare with the current version on the three scenarios, count rework, and tell me whether it can be promoted. I decide.

Read the result first, then the failures, then the cost table.

## How it connects

- **Before:** [agree-acceptance](../agree-acceptance/README.md) supplies the eval set shape.
- **After:** [graduation-ladder](../graduation-ladder/README.md) governs autonomy once a skill is Used. [learning-loop](../learning-loop/README.md) proposes the changes this gate tests.
- **Related:** [delivery-metrics](../delivery-metrics/README.md) for cost per accepted task on a feature; [docs/claims.md](../../docs/claims.md) for how results are claimed.

## Needs

The ability to run the skill on test inputs. Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 1 of 2, Opus 1 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- One change at a time. A bundle hides which part caused a failure.
- Keep the conflicting-source and boundary scenarios in every gate; they catch what averages hide.
- Count the time spent fixing outputs in the cost.
- Do not give a maturity label the evidence does not earn.

## Limits

- Three scenarios are a floor. They will not find every fault.
- Model output varies; a pass on one run is not a guarantee.
- The gate does not replace a person's judgement about whether a skill is worth having.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/skill-quality-gate/input.md) and [output](../../examples/skill-quality-gate/output.md).
