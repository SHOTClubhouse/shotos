# Does SHOTos help your team finish work?

The comparison that matters is the time, cost and quality of getting work your team can use. A fast draft still needs checking. A slower draft can be worth it if it needs fewer corrections or someone else can take it over without starting again.

## Aim

Compare the same job in the same AI assistant, using an ordinary prompt on its own and using the relevant SHOTos skill. Start the clock with the first request. Stop when a named reviewer accepts the work against the same agreed checks in both cases. If the job includes a handover, check that the next person can pick it up.

| What matters | What to record |
| --- | --- |
| Pace | Time to the first draft, then total time to sign-off, including waiting. |
| Quality | Whether the first draft was usable, which errors mattered and what the reviewer had to fix. |
| Repeated work | Extra prompts, revised drafts and minutes people spent checking or correcting them. |
| Cost | AI usage in tokens if available, the AI bill, and staff time at the same agreed rates. Count unsuccessful attempts too. |
| Scale | Whether another person can do the next round from the saved instructions and records, without the original person stepping in. |
| Value | The result the business wanted, such as fewer repeat enquiries or a proposal the sales lead can approve. Record it separately from the AI bill. |

## Experiment

### What we measured

In October 2026, we ran ten fictional jobs with and without an earlier SHOTos build. We used the same prompts and starting files in both versions, on Claude Haiku, Sonnet and Opus. Each model attempted each job twice. The table compares the 59 pairs where both sides returned a result. In the proposal exercise, the checks included covering the buyer's needs and using the right price.

| October exercise | Ordinary prompt | Same prompt with SHOTos |
| --- | ---: | ---: |
| All jobs passing the agreed checks | 58 of 59 | 58 of 59 |
| Average AI time per attempt | 39 seconds | 56 seconds |
| Average AI spend per attempt | US$0.137 | US$0.195 |
| Proposal attempts passing the agreed checks | 6 of 6 | 6 of 6 |
| Average AI time per proposal attempt | 31 seconds | 54 seconds |
| Average AI spend per proposal attempt | US$0.109 | US$0.164 |

These are first attempts. The checks assessed the work produced. The runs did not record comparable token totals, reviewer time, revision rounds or time to human sign-off. The comparison changes the instructions available to the assistant. Windows is where the software runs, so keep it the same in both versions if your team works on Windows. [October run results](../evals/results/2026-10-31-outcomes-run3.json)

A later ten-job check on fictional work shows why individual errors matter. Nine jobs tied. One proposal from the ordinary prompt included an unsupported commitment. The SHOTos version passed that check. The October proposal attempts passed both ways, so the later result is an example of a difference a reviewer would care about. [November task results](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#separate-release-regression-check)

### What a finished-job comparison looks like

This fictional proposal example shows how to record the whole job. The sales lead signs off on the same buyer requirements, price and terms in both versions. These figures are invented for the example.

| One proposal | Ordinary prompt | With the SHOTos proposal skill |
| --- | ---: | ---: |
| AI time across all drafts | 7 minutes | 4 minutes |
| Reviewer time | 8 minutes | 3 minutes |
| Time spent correcting the work | 8 minutes | 0 minutes |
| Drafts before sign-off | 2 | 1 |
| Total elapsed time to sign-off | 27 minutes | 12 minutes |
| AI spend through sign-off | US$0.07 | US$0.06 |
| Total AI and staff cost at US$60 an hour for active review and corrections | US$16.07 | US$3.06 |
| Issues found in the first review | 2 | 0 |
| Time for the next owner to pick up the signed-off work | 6 minutes | 5 minutes |

The 27 and 12 minutes include waiting. The cost row charges for active staff time and the AI bill. The pickup happens after sign-off and is shown separately. In your own comparison, use the same start and finish points, and include pickup in the total if the handover is part of the job. [Fictional worksheet](../examples/accepted-work-ledger.csv)

## Conclusion

In the October comparison, both approaches passed the same number of checks at job level. SHOTos took longer and cost more per AI attempt. We have no measured comparison yet of the full cost and time to get real work accepted. The proposal example shows how fewer corrections could change the business case. Whether that happens on your work is the thing to measure.

### Try it on your work

1. Choose a recurring job, such as writing a proposal, briefing the leadership team or handing a customer over to onboarding. Agree what the reviewer needs before they can use the result.
2. Give the same starting material and request to the same AI model in two fresh chats. Add the relevant SHOTos skill to one. Use the same access, deadlines and rules in both.
3. Ask the reviewer to check both drafts without telling them which used the skill. Continue each version until the reviewer accepts it or you reach the same agreed limit. Keep a record of unfinished jobs and the time and cost already spent.
4. Repeat with several jobs of the same kind. Compare total time and cost per accepted job, first-draft quality and any handover work. If you want to expand to another team, have them run a full round on their own before deciding.

Start with the [measurement guide](prerequisites.md#measuring-your-own-cost-per-accepted-task) and [worksheet](../templates/accepted-work-ledger.csv).

## Six-stage runtime check

The [Harbourside walkthrough](walkthrough.md) follows a team trying to reduce repeat repairs emails. The supplied data and drafts let you practise the first three stages. The later decisions are fictional examples. Codex and Claude Code also rehearsed a [proposal and handover](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#six-stage-runtime-check). Both held the transfer when a sales-system label was the only evidence. The [invoice-query exercise](guides/invoice-query-exercise.md#replay-check) shows what changes once the receiving team completes a full round and the sponsor sets conditions for the next site.

The [v1.11.0 test record](https://github.com/SHOTClubhouse/shotos/blob/v1.11.0/docs/evidence.md) contains the detailed skill checks, weekly-brief results and links to earlier runs.

### Weekly brief routing after v1.9.0

The [weekly brief test record](https://github.com/SHOTClubhouse/shotos/blob/v1.11.0/docs/evidence.md#weekly-brief-coverage-and-placement) shows how the assistant handled missing information and kept unverified claims out of the confirmed brief.
