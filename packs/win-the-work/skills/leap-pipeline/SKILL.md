---
name: leap-pipeline
description: Runs a sales or partnership pipeline through four LEAP stages with exit criteria and a weekly stalled-deal review. Use when setting up a pipeline, reviewing deals or handing over a won deal. Contacts no one.
---

# LEAP pipeline

Keep every deal in one of four stages, move it only when the exit criteria are met with evidence, and review the whole pipeline weekly so stalled deals are named rather than hoped about.

Step: any. It hands over into SHOTos Brief. Rules served: 3 (read back the real result) and 4 (claim only what you can show).

## When not to use this

Skip it for a single one-off enquiry that will close in a day, or when the person only wants a message drafted (use `email-reply` or `outbound-prospecting`). Do not use it to forecast revenue; a pipeline table shows evidence, not probability.

## The stages

| Stage | Sub-steps | Exit criteria (all must be true, each with evidence) |
|---|---|---|
| Lead | warm (known contact or referral), cold (no prior contact), target (a chosen account you are pursuing) | A named person at a named organisation; the route in is recorded (warm, cold or target); the person has agreed to a first conversation, with a date. |
| Explore | meeting, discovery, define | Meeting held; the problem and the cost of leaving it are written in their words; a one-paragraph definition of the work exists and the buyer has seen it; NUDGE has been scored (see `nudge-qualify`). |
| Agree | proposal, statement of work, gatekeepers | A proposal has been sent by its owner and read; scope, price and terms are written as a statement of work; every gatekeeper is named with their position; the person who can sign has accepted in writing. |
| Plan | start date, handover, delivery | A start date is agreed; a delivery owner is named; the handover packet is complete and accepted; delivery is registered as a SHOTos Brief task. |

A deal is "closed lost" or "parked" only with a reason written down.

## Steps

1. **Collect the deals.** Ask for the pipeline source (spreadsheet, CRM export, notes). Read it; do not edit it. If there is none, start the table from the template.
2. **Place each deal.** For each, set the step and sub-step from the criteria above, not from the owner's feeling. If the evidence for the claimed stage is missing, place the deal one step back and say so.
3. **Fill the pipeline table.** One row per deal using [template.md](template.md): organisation, contact, stage and sub-step, owner, value (label as estimate if it is), last contact date, evidence link, next action and its date.
4. **Run the weekly review.** Flag a deal as stalled when any of these is true: no recorded contact for 14 days (or the cadence the owner sets); next action is overdue; the same stage for longer than the owner's expected time; the main contact has not replied to the last two messages. For each flag, give the evidence: the last dated touch, the overdue action, the number of days. Do not guess why; propose one question the owner could ask.
5. **Check stage moves.** For any deal the owner wants to advance, list each exit criterion and the evidence. Mark each met, not met or unknown. Advance only when all are met.
6. **Write the handover packet** for any deal at the end of Plan: who the customer is, what was agreed (link to the statement of work), the price and payment terms, the gatekeepers and what each cares about, promises made in meetings, risks and unknowns, the delivery owner, the start date and the first three actions. Mark every item confirmed or unconfirmed. The packet is the input to SHOTos Brief.
7. **Stop at the boundaries.** Do not contact anyone, change a CRM record or move a deal's recorded stage. Propose the changes; the pipeline owner makes them.

## Output

A pipeline table, a short weekly review (stalled deals with evidence, proposed stage moves with criteria, the three actions that matter this week) and, where a deal has reached Plan, a handover packet. Use [template.md](template.md). Save with the pipeline, for example `.work/pipeline/2026-w44.md`.

## Checks

- Every stage claim has evidence or is marked unknown.
- Every stalled flag cites a date or a count, not an impression.
- No deal moved forward with a criterion unmet or unknown.
- Estimated values are labelled estimates.
- The handover packet separates confirmed from unconfirmed and names an owner and a start date.
- Nothing was sent or changed outside the project.
