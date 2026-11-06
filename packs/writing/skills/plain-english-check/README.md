# plain-english-check

**Make a draft readable on the first pass by the person it is for, without changing a fact.**

The agent asks who the reader is, finds the answer and puts it first, shortens sentences, turns passive phrasing into active verbs and explains or replaces jargon. It sets a length for that reader and reports every change so the owner can reverse any of them.

It supports the Track stage. It serves rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A letting agency sends tenants a four-paragraph email about a change to the repairs process. The action, which is to report faults through the new form, sits in the third paragraph behind two paragraphs of background and a sentence of 54 words. Tenants keep phoning the office. The fix is a rewrite that puts the action first, which is cheap, but only if the facts survive it.

## What the agent does differently

Without the skill, an agent tends to rewrite the whole text in its own voice, which can drop a date or soften a commitment. With the skill, it keeps a before and after, checks every figure and name, and lists what it left alone. See [the worked example](../../examples/plain-english-check/output.md).

## When to use it, and when not to

Use it on any text where the reader has to act or understand quickly: emails, notices, guides, web pages, policies and handover notes.

Do not use it on legal wording, quoted text, regulated notices or anything that must stay word for word. Flag the problems and leave the text alone there. Do not use it to shorten a draft whose length the owner has fixed.

## Who it is for

- **Operations and customer teams:** notices and replies people can act on.
- **Managers:** briefings that lead with the decision.
- **Small business owners:** web copy and emails that read as written by a person.
- **Anyone writing for the public:** a check that does not need a style guide to hand.

## How to use it

Install the writing pack as described in the [pack README](../../README.md). Then ask:

> Check this notice for plain English. The readers are tenants who read it on their phones. Use British English. Do not change dates or amounts.

## How it connects

- **Before:** [written-content](../../../content/skills/written-content/README.md) and [explainer](../../../content/skills/explainer/README.md) produce drafts this skill can check.
- **Alongside:** [ai-tell-check](../ai-tell-check/README.md) catches machine-written patterns that plain English alone does not.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Name the reader. Plain for a solicitor is not plain for a tenant.
- Check the numbers yourself on anything that carries a legal or money consequence.
- Keep the original beside the fixed version.

## Limits

- Sentence length is a guide, not a measure of clarity.
- It cannot know which terms a particular reader already uses unless you say.
- It does not check that the content is true. Use the fact checks in the writing skills for that.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/plain-english-check/input.md) and [output](../../examples/plain-english-check/output.md).
