# Delivery metrics

**Service or product:** Northgate Cycles booking tool, including the AI workshop-schedule summary
**Window:** 1 September to 9 November (ten weeks)
**Prepared by / date:** the agent, 10 November (draft)
**Definition of a production deploy:** a release recorded in the release log as live.
**Definition of a failed deploy:** a deploy followed by a hotfix, rollback or revert within 24 hours, as noted in the release log.

## The four keys
| Measure | Value | Count behind it | Source | Trend vs previous window | Note |
|---|---|---|---|---|---|
| Deployment frequency | 3.1 per week (range 2 to 4) | 31 deploys | Release log | No previous window supplied | Steady week to week |
| Lead time for changes | Median 24 hours; slowest quartile 48 hours or more | Sample of 12 changes | Release log, first commit to live | Not supplied | Median of the 12 sorted values is 24 (22 and 26); the slowest three were 52, 75 and 140 hours |
| Change failure rate | 13 per cent (4 of 31) | 31 deploys | Release notes | Not supplied | Small count; read with care |
| Time to restore | Median 50 minutes | 3 incidents: 25 min, 150 min, 50 min | Incident notes | Not supplied | Three events is too few to read a trend |

## AI feature measures
| Measure | Value | Count | Source | Date of run | Note |
|---|---|---|---|---|---|
| Eval pass rate | 95 per cent (38 of 40) | 40 cases | Eval run | 6 Nov | The two failures should be read before the next change |
| Cost per accepted task | About 0.97 pounds (62 pounds across 64 accepted drafts, 49 unedited plus 15 edited) | 70 drafts produced | Usage export, staff note | 10 weeks | Includes the cost of the 6 rejected drafts. Staff review time is not counted because it is not logged |
| Latency | Median 4.1 s; 95th percentile 11.8 s | Log count not supplied | Logs | 10 weeks | Count of calls missing |
| Human edit rate | Unedited 70 per cent (49 of 70); lightly edited 21 per cent (15 of 70); rejected 9 per cent (6 of 70) | 70 drafts | Staff note | 10 weeks | The staff note is a tally, not a log; "lightly" is the staff member's word |

## How to read this
- Frequency is steady and lead time has a long tail. Ask what the 75 and 140 hour changes were waiting for (review, testing, a person on leave).
- Four failed deploys in 31 is a number to watch, not a verdict. Two of the four were rollbacks. Ask whether a check for the config value and the date format could catch these before release.
- Time to restore ranges from 25 minutes to 150 minutes. The calendar sync incident was the slowest; ask how it was detected.
- The AI feature passes 95 per cent of its eval cases and 70 per cent of drafts are accepted unedited. Those two figures measure different things; track both.

## On the five-a-week target
The numbers describe how the system is behaving. A target of five deploys a week would reward smaller or split releases, not better ones, and the failure rate could rise alongside it. Keep the whiteboard for the trend over time and the questions above. If a number ever becomes a target, change how it is gathered or stop using it.

## Gaps
- No previous window, so no trend. Start by recording the same figures for the ten weeks before 1 September from the release log.
- Latency call count and staff review time are not recorded. Start logging both.
- Lead time rests on a sample of 12, not all 31 changes.

## Reminder
These describe the system, not people. Do not set a target on any single measure.
