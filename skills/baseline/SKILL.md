---
name: baseline
description: "Records how things are today before a change: the measures that matter, each value's source and date, and \"not measured\" where no data exists. Use when starting a change later judged better or worse, or before setting a target."
---

# Record the baseline

You cannot show an improvement without a "before". Write the before down first, with its source, so the result can be compared with something real.

**Stage:** Scope. **Rules:** 4 Claim only what you can show; 3 Read back the real result.

## Context and handoff

Read the current source, measurement window and denominator. Check exclusions and mark measures that were never observed.

Use `evidence-pack` for the later comparison. Save definitions and source dates beside the programme record.

## When not to use this

Skip it for a one-off task with no later comparison, such as drafting a single letter. Do not build a measurement project when the change is small; two or three measures are enough.

## Steps

1. **State the change in one sentence** and who will judge whether it worked.
2. **Choose two to five measures.** Pick numbers that the change should move, plus one that it must not make worse (a guard measure). Prefer measures the team already collects.
3. **For each measure, find the current value in a real source.** A report, a log, a system export, a count someone made. Record: the value, the unit, the source (where a person can look), the date or period it covers, and who collected it.
4. **Write "not measured" where there is no data.** Do not fill the gap with a guess, an average from elsewhere or a number that "feels right". State what it would take to measure it: the cheapest honest way, who would do it and how long. If a rough figure is useful, record it separately as `estimate`, name who made it and how, and keep it out of the baseline column.
5. **Check the data is comparable.** Note the period, the definition (for example "business days" or "calendar days") and anything that makes this window unusual, such as a holiday or an outage. The later measurement must use the same definition.
6. **Decide what to do about the gaps.** For each "not measured", choose one: measure it before starting (and how long that delays the work), start without it and drop the claim that depends on it, or accept an estimate and label every later use of it.
7. **Get the owner to confirm** the table before any target is set.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/baseline.md`.

## Checks

- Every measure has a value with a source and date, or the words "not measured".
- No value is an unlabelled guess.
- Definitions and periods are stated so the same measure can be repeated later.
- At least one guard measure is included.
- The owner has seen the gaps.
