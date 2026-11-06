---
name: contextual-proposal
description: Researches a named organisation, then writes a proposal argued for that reader, with a claim ledger, asset register and every page rendered and checked. Use when writing one proposal, bid or pitch. Never sends; many similar ones use proposal-factory.
---

# Contextual proposal

Write the proposal that this reader needs, in their terms, with every claim traceable and every page looked at before anyone is told it is ready.

Stage: Operate. Rules served: 3 (read back the real result) and 4 (claim only what you can show), and rule 1 (nothing is sent).

## Context and handoff

Read the buyer’s own words, organisation type, current constraints, approved offer and relevant prior proposal. Verify buyer-specific claims against current sources.

Use `nudge-qualify` for a weak buying signal. Keep approved claims and commitments in the deal working sheet.

## When not to use this

Skip it when the reader is unknown and a generic one-pager will do, or when many near-identical proposals are needed (use `one-off-or-factory` first, then `proposal-factory`). If the person only wants a reply to a message, use `email-reply`.

## Steps

1. **Name the reader, decision and proposal owner.** Use the request or the deal record for assignments and contact details. If the source gives only a role, use that role internally and leave the contact line out of the customer copy. The signed-in account, repository author and personal profile do not supply a sender. Ask about missing ownership only if it blocks the requested work.
2. **Research the reader.** From the sources provided and any public pages the person approves: what the organisation does, its stated priorities, its language, recent news, constraints and how it buys. Write ten lines at most. Label each fact with its source and date. Mark gaps as unknown.
3. **Find the argument.** One sentence: because the reader cares about X (evidence), the approved offer does Y, and the reader can assess Z. Do not turn a buyer's need into a seller capability or promise. If no approved offer answers the need, record a decision for the proposal owner before writing that section.
4. **Draft the structure for this reader.** Lead with their problem in their words, then the approved offer, the evidence, what each side would agree next, the money and the next step. Cut anything the reader has no use for. Keep any unapproved service level, staffing, reporting, delivery location, timeline, scope or date in the private working sheet. A `[TO CONFIRM]` beside a promise does not make the promise safe in the customer copy.
5. **Build the claim and commitment ledger.** List each factual claim and commitment with source, approval and status. Keep unsupported claims and proposed, unapproved commitments in the working sheet. Read the customer copy on its own and remove any sentence a buyer could reasonably treat as an unapproved commitment, including offers, guarantees and conditional promises. If pricing, free access or entitlements are proposed and approval is missing, put the terms only in the private sheet. In the proposal, ask the buyer to review the pilot and agree terms before a start. Do this even if the brief asks to discuss those terms. Label illustrative comparisons and keep their limits with them.
6. **Build the asset register.** List every image, chart, logo, quote and figure with its origin, owner, rights (owned, licensed, permission pending, unknown), and who is shown. Nothing with unknown rights or a person who has not agreed goes in; use a placeholder and flag it.
7. **Explain the money in the reader's terms.** Show what they pay, what they get for it and what it replaces or saves, using their budget lines and units where known. State assumptions. Show what they do not pay for.
8. **Read back the requested format.** For plain-text copy, reopen the saved draft and check it against the brief, claim and commitment ledger, and any length limit. Record the text check. For a formatted document or deck, render and inspect each page or slide for overflow, cut-off text, broken images, wrong names, inconsistent numbers and placeholders. Record the check per page.
9. **Report the separate decisions.** Record draft review or acceptance, authorisation for the exact revision, and dispatch evidence in separate fields. The owner or their authorised sender handles dispatch.

## Output

A proposal file, plus [template.md](template.md): reader note, argument sentence, claim ledger, asset register, money note, page check and status. Save with the deal, for example `.work/proposals/<reader>/`. Keep the ledger, the register and all working notes in that separate file: the proposal the reader sees contains none of them, and a rejected claim never appears in it, not even as something left out. When writing files, save the proposal and the private working sheet as separate files so the proposal can be reviewed on its own.

## Checks

- Reader and decision are named; research facts have sources and dates.
- Every factual claim and proposed commitment is in the ledger with a status; none unsupported remains in customer copy, even beside a placeholder.
- Every asset has rights recorded; none unknown in the file.
- The money section uses the reader's terms and states assumptions.
- The saved copy was reopened. A formatted document or deck has a recorded visual check for every page or slide.
- The status says "ready for review" at most, and nothing was sent.
