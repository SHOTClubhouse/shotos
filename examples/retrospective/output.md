# Retrospective: Quayside repair-reply pilot

**Period:** 14 April to 30 June
**Took part (roles):** pilot owner, branch lead, developer, reviewer, operations head (Priya Nair)
**Prepared by / date:** the agent, for the meeting on 8 July (draft)
**Accepted the work (name):** Priya Nair

## What we expected
From the plan of 28 March: pilot from 14 April to 16 June. Success: median first reply under 8 hours and 60 per cent answered within 4 hours, against a March baseline of 31 hours and 15 per cent. From the acceptance card of 4 April: any wrong contractor, date or cost in a reply counts as a failure. The plan did not say who owned the contractor list or what "ready to finish" meant.

## What happened
| Date | Event | Source |
|---|---|---|
| 14 Apr | Pilot starts | Tracker |
| 9 May | Out-of-hours emergencies found to be missing from the baseline | Chat export |
| 23 May | Two plumbers added to the contractor list on a Friday evening, live without review | Release log |
| 27 May | A draft named a retired plumber; caught by the reviewer before sending | Tracker |
| 2 Jun | "Are we ready to finish?" produced three meanings of ready | Chat export |
| 16 Jun | Planned end; extended two weeks to collect more data | Tracker |
| 30 Jun | Pilot ends | Tracker |

What went well: no wrong reply was sent. Reviewer time per draft fell from about 6 minutes to 2 after week two (the reviewer's own notes; not logged).
What was luck: the reviewer caught the retired plumber. There was no check that would have caught it otherwise.

## The gaps
| Gap (better or worse than expected) | How big (figure and source) |
|---|---|
| Finished late | 14 days past 16 June (tracker) |
| Within 4 hours target missed | 52 per cent against 60 per cent target (helpdesk export) |
| Median target met | 6.9 hours against under 8 (helpdesk export) |
| One failure caught | 1 draft with a wrong contractor, caught before sending (tracker) |
| Reviewer time lower than expected | 6 minutes down to 2 (reviewer's notes, unlogged) |

## Why (causes in the system)
| Gap | Cause | Shown or guessed |
|---|---|---|
| Late finish | Emergencies handled by phone were missing from the baseline, so more data was needed; no one had asked how emergencies were handled in March | Shown (chat of 9 May, extension on 16 June) |
| Wrong contractor in a draft | The contractor list had no named owner, and a change could go live without a review | Shown (release log; two accounts of who owned it) |
| Disagreement on finishing | "Ready" was not defined in the plan | Shown (chat of 2 June) |
| Missed 4-hour target | Not diagnosed. Out-of-hours emergencies and the busy start may play a part | Guessed |
| Reviewer time fell | Reviewers learned the typical errors; no checklist existed | Guessed |

The Friday edit is a symptom. The developer was not told the list was live and there was no review step; the causes lie in the setup.

## What we change
| Change | Answers which cause | How we will know it worked | Owner (one name) | Date |
|---|---|---|---|---|
| Name an owner for the contractor list and require a second pair of eyes before any change goes live | No owner, no review | Every list change in the release log has a reviewer | Fatima Rahman | 18 July |
| Write a short checklist for reviewers (contractor, date, cost) from the failures so far | No list of what to check | Checklist exists; reviewers use it for two weeks | The reviewer | 15 July |
| Add "ready to finish" to the plan template: measures and the date they are read | Undefined ready | Next plan has it before start | Priya Nair | 25 July |
| Ask how phone and out-of-hours work is logged before any baseline | Missing emergencies in baseline | The Millfield problem statement lists every channel | Priya Nair | Before the Millfield baseline |

Accept and watch: the missed 4-hour target. Re-read it after the emergency data are added; no change until its cause is known.

## Needs someone else's approval
None of these changes touches a boundary or budget. The contractor-list review step changes who may publish a shared list; Priya Nair approves it.

## Passed on
To the learning loop: the candidate rule "Any change to a list the agent quotes from needs a named owner and a reviewer before it goes live", with the 23 May to 27 May sequence as evidence and a contrary case still to find. To the evidence pack: the 52 per cent figure and the unmeasured emergencies. To a decision record: none.

## Follow-up (filled in on each date)
| Change | Done? | Did it work? | Note |
|---|---|---|---|
