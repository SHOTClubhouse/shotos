# written-content

**Write a piece for a named reader on a six-part arc, with every fact sourced, a fixed QA gate, and publishing kept as a separate step that needs a yes.**

The agent agrees the brief, picks the type, gathers sources before writing, builds the draft on situation, problem, evidence, idea, how it works and what to do next, and runs a fixed QA gate. Publishing is a separate step that waits for the owner.

It supports the Operate stage. It serves rule 2 (agree acceptance first), rule 4 (claim only what you can show) and rule 1 (stop at the boundaries).

## The problem it solves

A property management firm wants a one-page paper for landlords on rising void periods. The first draft has a confident statistic with no source, names a landlord who spoke to the firm and ends on a vague call to "get in touch". Each of those is a small fix before publishing and a bad day after.

## What the agent does differently

Without the skill, an agent writes a fluent piece and says it is ready. With the skill, it builds a source table, marks the unsourced figure "owner to confirm", replaces the named landlord with an anonymous example and ends on one specific action. See [the worked example](../../examples/written-content/output.md).

## When to use it, and when not to

Use it for white papers, reports, one-pagers and blog posts where facts, names and claims matter.

Do not use it for emails, replies or short messages, for legal or regulated text, or for a piece whose argument the owner has not decided. Use [explainer](../explainer/README.md) when the task is to explain how something works to a named audience.

## Who it is for

- **Founders and managers:** thought-leadership that holds up when read closely.
- **Marketing leads:** a gate that catches unsourced claims.
- **Analysts:** a clear route from findings to a readable piece.

## How to use it

Install the content pack as described in the [pack README](../../README.md). Then ask:

> Write a one-page paper for landlords on how long properties sit empty between tenants. Reader: small landlords with 1 to 5 properties. Use only the figures in the attached survey. Run the QA gate and do not publish.

## How it connects

- **Before:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) sets the checks for the piece.
- **After:** [plain-english-check](../../../writing/skills/plain-english-check/README.md) and [ai-tell-check](../../../writing/skills/ai-tell-check/README.md) polish the draft.
- **Alongside:** [explainer](../explainer/README.md) for how-it-works pieces, and [press-release](../press-release/README.md) for announcements.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent for drafting. Optional: a document or file connector to read sources and to save the draft, and the publishing tool of your choice, used only after the owner's yes.

## Tips and common mistakes

- Name the reader in one line before the first draft.
- If you cannot source a figure, cut it. A paper with fewer numbers that are all true reads better.
- Keep publishing as its own step with its own yes.

## Limits

- The gate checks that sources are listed. It cannot tell whether a source is correct.
- Consent has to come from the person. The agent can only record it.
- The six-part arc suits argued pieces; a pure data report may reorder parts but should keep them.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/written-content/input.md) and [output](../../examples/written-content/output.md).
