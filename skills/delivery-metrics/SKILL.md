---
name: delivery-metrics
description: Measures the four DORA delivery keys from existing git history, deploy logs and incident notes, plus eval pass rate, cost per accepted task and edit rate for AI features. Use when asking how delivery is going. Not for ranking people.
---

# Measure delivery without gaming it

Get honest numbers for how work reaches users and how well AI features behave, using records that already exist. Report trends and context, never league tables or targets for individuals.

Step: Check. Rules: 3 Read back the real result, 4 Claim only what you can show. The four keys come from the DORA research programme; credit it.

## When not to use this

Skip it for a team with no deploys and no repository history yet; say there is nothing to measure and name what to start recording. Do not use it to rank people or to set bonuses.

## Steps

1. **Pick the unit and window.** Choose one service or product, and a window of at least eight weeks. Write both down. Say what counts as a deploy to production for this team.
2. **Find the sources.** Usually: git tags or merge history, the deploy or release log, the incident or issue tracker, the on-call notes. For AI features also: the eval run results, the provider usage export, and the review log of edits. Note any source you cannot open.
3. **Compute the four keys.**
   - Deployment frequency: count production deploys in the window, report per week.
   - Lead time for changes: for a sample of changes, time from first commit (or merge request opened) to running in production. Report the median and the slowest quartile.
   - Change failure rate: deploys that needed a fix, rollback or hotfix, divided by all deploys. Say how you decided a deploy failed.
   - Time to restore: for each incident caused by a change, time from detection to service restored. Report the median and list each one.
4. **For AI features, add four more.**
   - Eval pass rate: cases passed over cases run, on the current eval set, with the date of the run.
   - Cost per accepted task: total model and tooling cost divided by tasks a person accepted, including the cost of tasks that were rejected or redone.
   - Latency: median and 95th percentile, from the logs.
   - Human edit rate: share of outputs edited before acceptance, from review records. Split unedited, lightly edited and rejected.
5. **Show denominators and gaps.** Every number carries its count (for example 3 failures in 41 deploys). If a number rests on fewer than ten events, say it is too few to read a trend. Mark any figure derived from partial data.
6. **Read them together.** Speed and stability move together in healthy teams. Flag a rise in frequency with a rise in failure rate, long lead time with low frequency, or a rising edit rate with a flat pass rate. Offer questions to ask the team, not conclusions.
7. **Add the guard against gaming.** State in the report: these describe the system, not people; do not set a target on any single key; if a number becomes a target, change how it is gathered or stop using it. Prefer a trend over eight or more weeks to a single week.
8. **Name the next measure to start recording** if a key could not be computed.

## Output

Use [template.md](template.md). Save as `.work/<task>/delivery-metrics.md`. Keep it to one page and a table of sources.

## Checks

- Each figure has a window, a source and a count.
- Definitions of "deploy" and "failed deploy" are written down.
- No figure is described as a target, a score for a person or a pass or fail on its own.
- Gaps and thin samples are marked.
- AI-feature figures include rework in the cost per accepted task.
