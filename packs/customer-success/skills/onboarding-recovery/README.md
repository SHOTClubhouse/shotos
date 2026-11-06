# onboarding-recovery

**Find where a stalled onboarding stopped, pick the smallest next step to first value, and draft the message for a person to send.**

The agent builds a dated timeline from mail, calendar, notes and usage, finds the last confirmed step and the first missed one, and labels the likely cause as a hypothesis. It proposes one next step with an owner and date on each side, says what the customer must do and drafts the message. It never sends.

It serves the Build step. Rules: 1 Stop at the boundaries, 3 Read back the real result, 4 Claim only what you can show.

## The problem it solves

Northgate Cycles sells a booking system to a bike hire firm. The owner signed five weeks ago, the setup call went well, and then nothing. Everyone assumes the customer is busy. A closer look shows the customer sent their price list on day 3 and nobody replied, so the next step was ours all along.

With the skill, the timeline shows the unanswered message, the diagnosis says "waiting on us" with the evidence, the next step is for Northgate to load the price list this week, and the draft message begins by owning the delay.

## When to use it, and when not to

Use it when a customer has gone quiet after signing, a setup step is overdue or a launch date has passed without first value. Skip it for cancellations and complaints, which go to the owner first, and for accounts that never started.

## Who it is for

Customer success managers, account managers, delivery leads and founders who onboard their own customers.

## How to use it

> The Larkfield onboarding stalled. Work out where it stopped from the mail thread and the calendar, tell me the smallest step to first value, and draft the message for me to review.

Output uses [template.md](template.md). Worked example: [input](../../examples/onboarding-recovery/input.md) and [output](../../examples/onboarding-recovery/output.md).

## How it connects

- **Before:** [success-handoff](../success-handoff/README.md) when the account needs a new owner.
- **Method:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) for defining first value up front.
- **Boundaries:** [docs/controls.md](../../../../docs/controls.md).

## Needs

Mail and calendar connectors, read-only, with permission to create drafts. A document connector to read the onboarding plan and notes. Usage data is optional; without it the diagnosis says so. Sending is not needed and should stay off.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 1 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Check whether the stall is yours before writing to the customer.
- Ask for one thing, not five.
- Define recovery as the first value event, not a reply.
- Do not suggest the customer is in breach of anything the evidence does not show.

## Limits

- The cause is a hypothesis unless the customer has said so.
- It sees mail and meetings, not what the customer is doing day to day.
- It cannot judge a relationship; use the draft as a starting point.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/onboarding-recovery/input.md), [example output](../../examples/onboarding-recovery/output.md).
