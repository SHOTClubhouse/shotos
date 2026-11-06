---
name: evidence-pack
description: "Builds the Track evidence pack with sourced results, the Scope baseline and measurement gaps. Use after a pilot or when someone claims an improvement without numbers. A named owner decides whether to proceed to Own, pivot or stop."
---

# Build the evidence pack

Put the before and after side by side, show where each number came from, say what you could not measure, and record the decision. The pack is what lets a sponsor decide on facts and lets the next person trust the decision.

Stage: Track. Rules: 3 Read back the real result, 4 Claim only what you can show.

## When not to use this

Skip it for a result that is still being built (use [report-with-evidence](../report-with-evidence/README.md)) or a weekly status note (use [progress-wrap-up](../progress-wrap-up/README.md)). If no baseline was written in Scope, still build the pack, but say so on the first page and treat every "before" figure as reconstructed.

## Steps

1. **Find the baseline.** Open the problem statement and acceptance card from Scope and Hypothesise. Copy each baseline measure and the success threshold exactly as written, with its date and source. If a measure has no baseline, mark it "no baseline" rather than inventing one.
2. **Fix the window.** State the before period and the after period with dates. Use periods of the same length and, where the work is seasonal, the same time of year. Note anything else that changed in the window, such as staffing, pricing or a holiday.
3. **Collect the after figures from the source.** Read from the system of record (logs, exports, the ledger, the repository), not from a message that quotes it. For each figure write the value, the unit, the date range, the source and how it was calculated. Do not round in a favourable direction.
4. **Compare like with like.** For each measure give before, after, change and whether the Hypothesise threshold was met. Show the change as an absolute and a percentage only where the base is large enough to make a percentage mean something. Label small samples as small.
5. **State what could not be measured.** List every measure that has no baseline, no after figure, a thin sample or a source you could not open. Say what it would take to measure it. Never fill a gap with an estimate unless it is labelled as one.
6. **List other explanations.** Write at least two reasons the change might not be due to the work (seasonality, a pricing change, a one-off event, selection of who was included). Say what you checked and what you could not.
7. **Add cost and side effects.** Include time and money spent, rework, complaints, defects after release and anything that got worse. A pack with only good news is not finished.
8. **Draft the decision.** Propose proceeding to Own, pivoting to Hypothesise or stopping, with reasons tied to the figures. Hold if outcome evidence is missing. Name the decision owner and leave the decision line open for their decision, role and date. Wider rollout requires an accepted independent cycle and its own approval.
9. **Check every claim.** Each sentence with a number must trace to a row in the evidence table. Run claim-check or read each row back against its source.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/evidence-pack.md`. Keep it to two pages plus the evidence table. Lead with the decision needed and the one-line finding.

## Checks

- Every figure has a value, unit, date range, source and calculation.
- The before figures match the Scope baseline, or the difference is explained.
- A "could not measure" section exists and is not empty unless you can say why.
- At least two alternative explanations are listed.
- The decision field names a person and stays blank until they give it.
- Nothing is called a success that missed its Hypothesise threshold.
