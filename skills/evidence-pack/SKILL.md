---
name: evidence-pack
description: "Builds the Check-step pack comparing results with the baseline in the brief: sourced figures, unmeasured gaps, and a scale, pivot or stop decision by a named person. Use when a pilot has run, or someone says \"it worked\" without numbers."
---

# Build the evidence pack

Put the before and after side by side, show where each number came from, say what you could not measure, and record the decision. The pack is what lets a sponsor decide on facts and lets the next person trust the decision.

Step: Check. Rules: 3 Read back the real result, 4 Claim only what you can show.

## When not to use this

Skip it for a result that is still being built (use [report-with-evidence](../report-with-evidence/README.md)) or a weekly status note (use [progress-wrap-up](../progress-wrap-up/README.md)). If no baseline was written in the brief, still build the pack, but say so on the first page and treat every "before" figure as reconstructed.

## Steps

1. **Find the baseline.** Open the problem statement and acceptance card from the brief. Copy each baseline measure and the success threshold exactly as written, with its date and source. If a measure has no baseline, mark it "no baseline" rather than inventing one.
2. **Fix the window.** State the before period and the after period with dates. Use periods of the same length and, where the work is seasonal, the same time of year. Note anything else that changed in the window, such as staffing, pricing or a holiday.
3. **Collect the after figures from the source.** Read from the system of record (logs, exports, the ledger, the repository), not from a message that quotes it. For each figure write the value, the unit, the date range, the source and how it was calculated. Do not round in a favourable direction.
4. **Compare like with like.** For each measure give before, after, change and whether the agreed threshold was met. Show the change as an absolute and a percentage only where the base is large enough to make a percentage mean something. Label small samples as small.
5. **State what could not be measured.** List every measure that has no baseline, no after figure, a thin sample or a source you could not open. Say what it would take to measure it. Never fill a gap with an estimate unless it is labelled as one.
6. **List other explanations.** Write at least two reasons the change might not be due to the work (seasonality, a pricing change, a one-off event, selection of who was included). Say what you checked and what you could not.
7. **Add cost and side effects.** Include time and money spent, rework, complaints, defects after release and anything that got worse. A pack with only good news is not finished.
8. **Draft the decision, do not make it.** Propose scale, pivot or stop, with the reasons tied to the figures. Name the person who decides. Leave the decision line empty until that person gives it, with their name, role and date. An agent never records the decision for them.
9. **Check every claim.** Each sentence with a number must trace to a row in the evidence table. Run claim-check or read each row back against its source.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/evidence-pack.md`. Keep it to two pages plus the evidence table. Lead with the decision needed and the one-line finding.

## Checks

- Every figure has a value, unit, date range, source and calculation.
- The before figures match the baseline in the brief, or the difference is explained.
- A "could not measure" section exists and is not empty unless you can say why.
- At least two alternative explanations are listed.
- The decision field names a person and stays blank until they give it.
- Nothing is called a success that missed its agreed threshold.
