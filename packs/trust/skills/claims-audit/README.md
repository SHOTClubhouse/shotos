# claims-audit

**List every factual claim in a public or customer-facing document, check its source and status, and propose fixes without changing anything.**

This skill reads a document meant for customers, investors or the public and lists every factual claim in it. For each claim it records the source, a status (supported, outdated, unsupported or illustrative) and a proposed fix. Numbers such as users, customers or revenue need a dated source. Nothing in the document changes until its owner says yes.

It supports the Track stage. It serves rule 4, Claim only what you can show, and control [10, claim-discipline](../../../../rules/10-claim-discipline.md).

## The problem it solves

Northgate Cycles is about to send a brochure to a council buyer. It says "trusted by over 5,000 riders" and "the UK's fastest repairs". The first figure came from a spreadsheet two years ago. The second has no source at all. A buyer who checks either can end the conversation. An audit finds both before the brochure leaves, and puts the decision with the owner.

## When to use it, and when not to

Use it before any public or customer-facing document goes out: a brochure, web page, proposal, press release, deck or grant bid. Reopen affected checks if material wording, audience or destination changes. Try the [release review example](release-review-example.md) to see how facts and permission are checked separately.

Skip it for internal notes, private drafts and personal messages. It does not judge the quality of the writing and it is not a legal review.

## Who it is for

- Founders and sales leads sending proposals or decks.
- Marketing teams approving web copy.
- Anyone who inherited a document and wants to know what it promises.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Audit this brochure for claims before it goes to the council. List each claim, its source, its status and the fix. Do not edit the brochure.

You get a table of claims with source, status and proposed fix, a short list of the claims that block sending, and a question for each claim you must decide. The brochure is untouched.

## How it connects

- **Rules:** [10, claim-discipline](../../../../rules/10-claim-discipline.md) and [docs/claims.md](../../../../docs/claims.md) explain the separate states of installed, executed and accepted.
- **Related:** [public-exposure-check](../public-exposure-check/README.md) checks the same document for secrets and personal data.
- **After:** [report-with-evidence](../../../../skills/report-with-evidence/README.md) can summarise the audit for the owner.

## Needs

Nothing beyond the agent. It reads the document and any evidence you provide. If a claim needs a live figure, such as a user count, the owner or a connector must supply it with a date.

## Tips and common mistakes

- Give the agent the sources you already have; it should not guess where a figure came from.
- Treat a number without a date as outdated until proven otherwise.
- Mark marketing examples as illustrative where they are, and say so in the document.
- Ask the owner to rule on each fix; the agent proposes wording but does not apply it.

## Limits

- It checks claims against evidence you give it. It cannot know a figure is true from the document alone.
- It does not give legal advice on advertising rules.
- Superlatives and comparisons need a named, dated comparison to count as supported.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/claims-audit/input.md) and [output](../../examples/claims-audit/output.md).
