---
name: graduation-ladder
description: "Decides how much autonomy a repeated task class has earned from logged acceptance outcomes: draft only, automatic with notice, or silent. Use when reviewing a task class or considering less supervision. Never loosens send, spend, delete or publish limits."
---

# Climb the graduation ladder

Autonomy is earned by a record, class by class. The agent logs outcomes, reads the status, and recommends a rung. A person grants it.

Step: Improve. Rules: 1 Stop at the boundaries, 4 Claim only what you can show. This is control 12, graduation.

## When not to use this

Skip it for one-off tasks with no repeat. Do not use it to loosen a boundary: sending, spending, deleting or publishing outside the project keeps its owner's yes unless a named person explicitly grants a standing permission for that class and scope.

## The ladder

| Rung | What the agent may do | Needs |
|---|---|---|
| 1 | Draft only. A person reviews and accepts every output. | Where every class starts |
| 2 | Run automatically and notify the owner. The owner can still look. | At least 95 per cent accepted unedited over at least 50 samples |
| 3 | Run silently and report exceptions only. | At least 200 samples in total, and at least 98 per cent accepted unedited over the most recent window (default 50) |

A class drops one rung when its rate over the most recent window falls below the bar for its current rung. High-risk classes stay at rung 1 unless a named person explicitly promotes them, with the reason recorded.

## Steps

1. **Define the task class.** One narrow, repeated kind of task, with a name in lowercase words joined by hyphens, such as `weekly-invoice-summary`. A class that is too broad hides failures. Write what counts as the same kind of task.
2. **Mark the risk.** A class is high-risk if a wrong output could cause harm, expose private data, send something outside, spend money, or change records others rely on. Record that decision and who made it. When unsure, treat it as high-risk.
3. **Log each outcome as it happens.** After the owner reviews an output, run `python .shotos/tools/graduation_log.py record --class <class> --outcome accepted-unedited|accepted-edited|rejected --by <name>`, adding `--high-risk` for a high-risk class. Log what the person did, not what the agent thinks. Do not log an outcome the owner has not reviewed.
4. **Check the standing.** Run `python .shotos/tools/graduation_log.py status --class <class>` (or `status` for all). Read the counts, the unedited rate, the sample size and the current rung it reports. If the tool is not available, say so; do not compute a rung by memory.
5. **Compare with the bar.** Unedited rate means accepted-unedited divided by all logged outcomes. Both rate and sample size must pass. Look at the distribution of the edits, not just the rate: a class that is "unedited" except for one serious error a month is not ready.
6. **Recommend, do not promote.** Write a recommendation: stay, promote to the next rung, or drop one. A named person decides and the decision is recorded with the date, class, rung, evidence counts and what would drop it. For a high-risk class, say plainly that only a named person can promote it and the reason must be written down.
7. **State the exceptions policy for rung 2 and 3.** What counts as an exception (a failed check, a rejected output, a detected boundary case), who gets notified and how fast, and how to switch the class back to rung 1 at once.
8. **Review on a schedule.** After a change to the skill, the model, the data source or the people, restart the sample count for the class, or at least mark the date and review the rate. Review every class quarterly.

## Output

A short standing note per class: class, risk, current rung, counts, rate, recommendation, decision and decider, date and next review. Use [template.md](template.md).

## Checks

- Every logged outcome came from a person reviewing it.
- The rung is read from the tool's status output, with counts shown.
- Promotion shows both the rate and the sample size over the bar.
- A high-risk class is at rung 1 unless a named person's promotion is recorded.
- A recommendation to drop is made when the rate falls below the bar.
