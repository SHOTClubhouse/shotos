# explainer

**Turn a topic into a document a named reader understands, with checked examples, and file it before anyone is told.**

The agent classifies the explainer, agrees the brief, sources the facts and drafts the mechanism with worked examples. It adds a picture only where it shows how the thing works, runs a five-part QA gate, files the result and waits for a yes before sharing.

It supports the Operate stage. It serves rule 2 (agree acceptance first), rule 3 (read back the real result) and rule 1 (stop at the boundaries).

## The problem it solves

A letting agency needs a page explaining how a tenancy deposit is protected for new tenants. The first draft is accurate but uses scheme jargon, has no example of how a deduction is calculated and includes a decorative stock-style picture. A tenant cannot tell what happens to their money on day 31.

## What the agent does differently

Without the skill, an agent writes a tidy summary and shares it. With the skill, it classifies the page as external, adds a worked example with invented figures, drops the decoration, checks links and alt text and files it for the owner. See [the worked example](../../examples/explainer/output.md).

## When to use it, and when not to

Use it when someone needs to understand how something works: a process, a product, a policy or a technical design.

Do not use it for an argued opinion piece (use written-content), a press announcement (use press-release), or a quick chat answer. Do not use it when the subject is not understood yet; learn the facts first.

## Who it is for

- **Operations and customer teams:** pages that cut repeat questions.
- **Engineers:** design notes a new colleague can follow.
- **Managers:** briefings that explain before they ask for a decision.

## How to use it

Install the content pack as described in the [pack README](../../README.md). Then ask:

> Write an external explainer for new tenants on how their deposit is protected. Include one worked example with invented figures. Run the QA gate, file it in the drafts folder and do not publish.

## How it connects

- **Before:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) sets the checks.
- **After:** [plain-english-check](../../../writing/skills/plain-english-check/README.md) and [ai-tell-check](../../../writing/skills/ai-tell-check/README.md) polish the text.
- **Alongside:** [image-create](../../../media/skills/image-create/README.md) for illustrations, and [written-content](../written-content/README.md) for argued pieces.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent. Optional: a folder or repository for filing explainers, an image model for illustrations, and a diagram tool.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Pick the class first. It decides what you can include.
- Run every worked example. An example that fails is worse than none.
- Keep a one-line index entry for each filed explainer so people can find it later.

## Limits

- The agent can check links and structure, not whether a source is right.
- Accessibility checks cover the basics; a person should test important pages with a screen reader.
- A picture can mislead. Check it shows what the text says.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/explainer/input.md) and [output](../../examples/explainer/output.md).
