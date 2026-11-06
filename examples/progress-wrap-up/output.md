# Progress wrap-up: week ending 26 October

**Window:** Monday 20 October 00:00 to Sunday 26 October 23:59, UK time. Carries on from the 19 October wrap-up.
**Prepared by:** the agent (draft for Ines Calder to post)
**Sources read:** meeting notes of 21 October, repository history, release log, shared drive, tracker
**Sources not opened:** the live website was checked only for the price page; the booking page behind the flag was not tested in production.

## Summary
Live: 0 | Gated: 1 | Merged only: 1 | Unverified: 2. Biggest ask: Ines to decide when to switch on the `online_booking` flag.

## Evidence ledger
| # | Claim | Date | Source | Status | Why it matters | Ask |
|---|---|---|---|---|---|---|
| 1 | "Online booking is done" | 21 Oct | Meeting notes; repository merge 21 Oct; release 1.8.0 on 23 Oct | Gated | Customers cannot book until the flag is on, so no benefit yet | Ines to say when to switch on the `online_booking` flag |
| 2 | Confirmation email "should be working" | 21 Oct | Meeting notes; template merged 22 Oct | Merged only | Not in release 1.8.0, so booking confirmations cannot go out | Tomasz Wrona to include it in the next release |
| 3 | Workshop price list final | 24 Oct | Shared drive v4, Ines's approval comment | Merged only (final document, not published) | The public price page still shows version 3, so customers see old prices | Ines to say who updates the website page, and by when |
| 4 | Opening hours fixed on contact page | 22 Oct | Tracker card moved to Done | Unverified | Wrong hours cost customers a wasted trip | Tomasz to link the change or show the live page |
| 5 | Reminder text message change | 24 Oct | Draft change in the repository, not merged | Unverified (draft only) | No customer impact yet | None this week |

## Slipped or changed
| Planned | What happened | Reason (if known) |
|---|---|---|
| Cancellation-policy wording for the booking page | Not reported and no change found | Unknown |
| Confirmation email in the release | Left out of 1.8.0 | Unknown |

## Last week's asks
| Ask | Answered? | Outcome |
|---|---|---|
| Ines to choose workshop slot lengths | Yes | 30 and 60 minutes, agreed on 21 October |
| Ines to switch on the booking flag when ready | No | Carried forward as ask 1 |

## Risks that appeared
- If the flag is switched on before the confirmation email ships, customers will book and receive nothing. Do these two together.

## Asks for this week
1. Ines Calder to decide a date for switching on `online_booking`, by Wednesday 29 October.
2. Tomasz Wrona to put the confirmation email in the next release, by Thursday 30 October.
3. Ines Calder to name who publishes the version 4 price list to the website, by Wednesday 29 October.
4. Tomasz Wrona to link the opening-hours fix to a live page or reopen the card, by Wednesday 29 October.
5. Ines Calder to confirm the cancellation-policy wording, by Friday 31 October.

## Changed since first posted
(None yet. Edit this issue in place if anything changes; do not start a second one.)
