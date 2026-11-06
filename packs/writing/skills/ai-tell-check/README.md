# ai-tell-check

**Find the patterns that make text read as machine-written, fix them line by line, and never change a fact.**

The agent reads a numbered copy of the draft and checks seven known patterns. It reports each finding with the line and a proposed fix, applies the fixes to a separate copy and verifies that every fact is unchanged.

It supports the Check step. It serves rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A bicycle shop owner uses an agent to draft a launch email. It reads smoothly but it is full of em dashes, opens with "In today's fast-moving world", lists three adjectives for every product and ends with a paragraph restating the offer. Regular customers say it does not sound like her. The patterns are findable and fixable, but only if the price, dates and product names survive the edit.

## What the agent does differently

Without the skill, an agent asked to "make it sound human" tends to rewrite freely and may change the offer. With the skill, it works line by line and reports each change. See [the worked example](../../examples/ai-tell-check/output.md).

## When to use it, and when not to

Use it on any draft before it goes to a reader: emails, posts, articles, reports and web copy.

Do not use it to disguise authorship or to get past a rule that requires disclosure of AI use. Do not use it on quotations, legal text or text the owner has said must stay as written. Do not run it as the only check: a text can be free of these patterns and still be wrong.

## Who it is for

- **Small business owners:** emails and posts that sound like the owner.
- **Writers and editors:** a repeatable pass before sign-off.
- **Teams using agents for drafting:** a shared checklist for the patterns readers notice.

## How to use it

Install the writing pack as described in the [pack README](../../README.md). Then ask:

> Run the AI-tell check on this email and show me each finding with its line and the fix. Do not change the price or the dates.

## How it connects

- **Before:** [written-content](../../../content/skills/written-content/README.md), [explainer](../../../content/skills/explainer/README.md) and [creator-edit](../../../content/skills/creator-edit/README.md) produce drafts this skill can check.
- **Alongside:** [plain-english-check](../plain-english-check/README.md) covers length, jargon and answer-first order.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Keep your own voice sample to hand. The best fix is the way you would say it.
- A pattern once is style; the same pattern five times is a tell.
- Read the fixed version aloud before you send it.

## Limits

- It finds patterns, not authorship, and it is not a detector.
- Some readers use these patterns in their own writing; the owner decides.
- The word list dates quickly. Keep your own list in the project.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/ai-tell-check/input.md) and [output](../../examples/ai-tell-check/output.md).
