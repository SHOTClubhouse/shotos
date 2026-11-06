# evidence-pack

**Compare the result with the baseline, show where every figure came from, say what you could not measure, and record the decision.**

This skill produces a two-page pack for the Check step. It copies the baseline from the brief, collects the after figures from the source systems, compares them with the threshold agreed in the brief, lists other explanations and gaps, and drafts a recommendation. The decision itself is recorded by a named person.

It supports the Check step. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

A property manager at a fictional firm, Harbourside Lettings, ran a three-month pilot of an agent that drafts repair-request replies. The sponsor asks for a verdict. The team says "replies are much faster". Nobody can say how fast they were before, whether the quieter autumn helped, or how many drafts staff rewrote.

The pack answers each of those. It shows first-reply time before and after from the helpdesk export, flags that October volume dropped when a block of flats changed agent, lists the three measures nobody tracked, and leaves a blank line for the sponsor's decision.

## When to use it, and when not to

Use it when a pilot or release has run long enough to judge, before more money or a wider rollout is requested, and whenever someone says "it worked" without numbers.

Do not use it for work still being built or for a weekly note. Use [report-with-evidence](../report-with-evidence/README.md) or [progress-wrap-up](../progress-wrap-up/README.md) there.

## Who it is for

- **Sponsor or business unit leader:** a decision page you can trust and challenge.
- **Product owner or analyst:** a fixed structure so figures and sources never separate.
- **Engineering or practice lead:** links delivery numbers to the original hypothesis.
- **Solo founder:** an honest answer to "is this working?" before spending more.

## How to use it

Ask:

> The repair-reply pilot at Harbourside Lettings ran 1 August to 31 October. Build the evidence pack against the baseline in the problem statement, and draft a recommendation for the managing director.

Read the pack, check the could-not-measure list, and give the decision yourself on the last section.

## How it connects

- **Before:** [agree-acceptance](../agree-acceptance/README.md) set the threshold. [capture-the-problem](../capture-the-problem/README.md) set the baseline.
- **Alongside:** [delivery-metrics](../delivery-metrics/README.md) supplies engineering figures. [decision-record](../decision-record/README.md) keeps the decision.
- **After:** [retrospective](../retrospective/README.md) looks at how the work went. [rollout-plan](../rollout-plan/README.md) follows a scale decision.

## Needs

Read access to the systems that hold the figures (exports, logs, repository). Nothing is sent or published by the skill.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Copy the baseline word for word. Do not restate it from memory.
- Use equal-length windows.
- Keep the could-not-measure list even when it is uncomfortable.
- Write "no baseline" instead of guessing one.
- The agent drafts the recommendation. The named person decides.

## Limits

- A pack is only as good as the baseline. A weak brief gives a weak pack.
- It cannot prove cause. It lists other explanations; a controlled comparison is stronger.
- Sources the agent cannot open stay on the gap list.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/evidence-pack/input.md) and [output](../../examples/evidence-pack/output.md).
