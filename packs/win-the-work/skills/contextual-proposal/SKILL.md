---
name: contextual-proposal
description: Turns an organisation name, short request or existing brief into a researched proposal for a specific buyer. Use to find the buyer and approved offer, draft the proposal and prepare the deal record for handoff. Routes tenders, buyer RFPs and repeat batches to dedicated skills.
---

# Contextual proposal

Write a buyer draft and a separate private working sheet. The buyer draft carries approved claims and terms. The working sheet holds sources, unapproved terms, reviewer notes and asset rights.

Stage: Operate. Rules served: 3 (read back the real result) and 4 (claim only what you can show), and rule 1 (nothing is sent).

## Context and handoff

An organisation name and an offer description are enough to start. Search the permitted account or deal record, meeting notes and project files for the buyer's priorities. Find the current approved offer, closest proposal template and reusable assets in the supplier's own files. Follow attachments or links only when they answer a missing point. Use the buyer's official sources to verify identity and public facts. If two organisations plausibly match, ask which one before writing buyer-specific copy.

Reuse the closest proposal's structure and approved assets. Verify the new buyer's needs, terms, rights and decision process independently. If a source is inaccessible, record which one. Ask one focused question if the answer would change the scope, terms or buyer decision. Otherwise draft the supported parts and keep the open items in the working sheet.

Use `nudge-qualify` for a weak buying signal. Keep approved claims and commitments in the deal working sheet. If leadership needs to decide whether to proceed, link the exact draft and the private working sheet from the decision brief. Distinguish proposal readiness, authority to send, buyer response and delivery handoff.

## Choose the proposal route

| Request | Skill to use |
| --- | --- |
| One tailored offer or pitch for a named buyer | `contextual-proposal`. Choose the [organisation template](organisation-templates.md) that fits the buying route. |
| Supplier response to an issued tender or RFP | `bid-response`. The buyer's instructions govern the format and submission requirements. |
| Buyer preparing an invitation for suppliers | `rfp-authoring`. Set requirements, scoring and approval gates. |
| Repeated proposals for similar buyers | `one-off-or-factory`, then `proposal-factory` if the work qualifies. |

## When not to use this

Skip it when the reader is unknown and a generic one-pager will do, or when many near-identical proposals are needed (use `one-off-or-factory` first, then `proposal-factory`). If the person only wants a reply to a message, use `email-reply`.

## Steps

1. **Name the reader, decision and proposal owner.** Use the request or the deal record for assignments and contact details. If the source gives only a role, use that role internally and leave the contact line out of the customer copy. The signed-in account, repository author and personal profile do not supply a sender. Ask about missing ownership only if it blocks the requested work.
2. **Research the reader.** From the sources provided and any public pages the person approves: what the organisation does, its stated priorities, its language, recent news, constraints and how it buys. Write ten lines at most. Label each fact with its source and date. Mark gaps as unknown.
3. **Split the inputs before drafting.** In the private ledger, give each claim or term a source and status: buyer need, verified fact, approved offer or decision needed. Approval to describe a past result, a capability or an average does not authorise a future commitment. For example, a buyer's monthly reporting need can appear as a need. An offer to supply the report, even conditionally, needs its own approval.
4. **Draft from the approved rows.** Lead with the buyer's problem, then the approved offer, supporting evidence, price and next decision. Where a service level, staffing plan, reporting, delivery location, timeline, scope, fee, access or entitlement needs approval, ask the buyer to agree the relevant requirement before a start. Put the proposed term and its owner in the working sheet. Label illustrative comparisons and keep their limits with them.
5. **Check the buyer copy as a standalone file.** Read each offer sentence as the buyer. Check the scope, price, timing, location and obligations against their approved ledger rows. Move unsupported sentences and internal notes to the private sheet, including notes hidden in comments. A placeholder or conditional verb beside a term does not make the term approved.
6. **Build the asset register.** List every image, chart, logo, quote and figure with its origin, owner, rights (owned, licensed, permission pending, unknown), and who is shown. Nothing with unknown rights or a person who has not agreed goes in; use a placeholder and flag it.
7. **Explain the money in the reader's terms.** Show what they pay, what they get for it and what it replaces or saves, using their budget lines and units where known. State assumptions. Show what they do not pay for.
8. **Read back the requested format.** For plain-text copy, reopen the saved draft and check it against the brief, claim and commitment ledger, and any length limit. Record the text check. For a formatted document or deck, render and inspect each page or slide for overflow, cut-off text, broken images, wrong names, inconsistent numbers and placeholders. Record the check per page.
9. **Report the separate decisions.** Record draft review or acceptance, authorisation for the exact revision, and dispatch evidence in separate fields. The owner or their authorised sender handles dispatch.

## Output

A proposal file and a private [working sheet](template.md). Save both with the deal. Keep the ledger, asset register and draft terms in the working sheet so the buyer-facing proposal can be reviewed on its own.

Keep **Delivery handoff** in the existing deal record, or in the working sheet until a deal record exists. Give `success-handoff` that one reference with permitted access. Carry the exact proposal revision, source-backed commitments, open decisions, current owner, proposed receiver and first-action date if agreed. If the proposal has yet to be accepted, label the revision as a draft and the commitments as proposed. Buyer acceptance and receiver acceptance require their own evidence. See the [worked fictional deal](worked-deal.md).

## Checks

- Reader and decision are named; research facts have sources and dates.
- Every factual claim and proposed commitment is in the ledger with a status; none unsupported remains in customer copy, even beside a placeholder.
- Every asset has rights recorded; none unknown in the file.
- The money section uses the reader's terms and states assumptions.
- The saved copy was reopened. A formatted document or deck has a recorded visual check for every page or slide.
- The status says "ready for review" at most, and nothing was sent.
