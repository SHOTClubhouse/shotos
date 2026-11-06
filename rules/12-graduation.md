# Control 12: Graduation

**The rule:** A class of task earns more autonomy only through logged acceptance, drops a rung when the record slips, and stays at rung 1 if high-risk unless a named person promotes it.

Serves rule 4, [Claim only what you can show](../docs/controls.md): trust is a claim, and the log is its evidence. Matters most in **Sustain and Scale**.

## Why it exists

A bookkeeper at Northgate Cycles lets an agent send weekly stock summaries without checking them, because the first few were fine. Six weeks later a supplier changes its file format. The agent keeps producing confident summaries with half the lines missing, and nobody has looked in a month. Trust was granted on a feeling and never revisited.

Autonomy should be earned the way a new colleague earns it: by a record of work accepted without changes, in a class of task, and withdrawn quickly when the record changes.

## What the agent does

1. Names the **task class**: a type of repeated task with a stable shape, for example `weekly-stock-summary` or `enquiry-reply-draft`. The class is not "everything".
2. Starts every class at **rung 1**.
3. After the owner reviews each output, records the outcome with the graduation log tool: `accepted-unedited`, `accepted-edited` or `rejected`. It never records its own work as accepted.
4. Reads the status regularly and acts on the rung:
   - **Rung 1, draft only.** The agent drafts; a person reviews every output before it is used.
   - **Rung 2, auto-run and notify.** The agent runs the task on its own and tells the owner what it did; the owner can still check any output. Needs at least 95% accepted unedited over at least 50 samples.
   - **Rung 3, silent, exceptions only.** The agent runs the task and speaks only when something is out of range. Needs at least 200 samples in total and at least 98% accepted unedited over the most recent window (default 50).
5. Computes the rate over the **most recent window** (50 by default), so a class that falls below the bar **drops a rung** automatically on the next status check.
6. Keeps **high-risk classes** at rung 1 unless a named person records a promotion. A promotion is a ceiling, not a guarantee; the class still has to hold the rate.
7. Never lets a rung override [control 4](04-stop-boundaries.md). External sends, spend and deletion still need the owner's yes at any rung unless the owner has explicitly delegated that exact action for that class in writing.

## What a person does

- Records the outcome honestly, including `accepted-edited` when they changed anything at all.
- Adjusts the thresholds for their own situation. The defaults are a starting point.
- Decides whether a class is high-risk, and records a promotion with their name when they choose to raise one.
- Reviews exceptions at rung 3 promptly, and drops the rung by hand if something feels wrong.

## The format and the tool

The tool is `.shotos/tools/graduation_log.py`. The log is append-only JSONL at `.work/graduation-log.jsonl`.

```
python .shotos/tools/graduation_log.py record --class weekly-stock-summary --outcome accepted-unedited --by "Priya Nair"
python .shotos/tools/graduation_log.py record --class supplier-email --outcome rejected --by <name> --note "wrong tone" --high-risk
python .shotos/tools/graduation_log.py status
python .shotos/tools/graduation_log.py promote --class supplier-email --to 2 --by "Sam Rivers"
```

### The graduation ladder (defaults)

| Rung | Behaviour | Needs |
|---|---|---|
| 1 | Draft only; person reviews every output | Starting point for every class; always the ceiling for high-risk until promoted |
| 2 | Auto-run and notify | At least 95% accepted unedited over the recent window, at least 50 samples in total |
| 3 | Silent, exceptions only | At least 98% accepted unedited over the recent window, at least 200 samples in total |

Change the thresholds with `--rung2-rate`, `--rung2-samples`, `--rung3-rate`, `--rung3-samples` and `--window` on `status`. Record the values you chose and why in the project, so a later reader knows the bar.

## Sizing by risk

- **Small, low-risk classes** (internal summaries, formatting): graduate normally. A rung 2 notification is fine.
- **Normal classes** (anything someone relies on): graduate, but sample outputs even at rung 2, on a schedule the owner sets.
- **High-risk classes** (money, personal data, children's data, external, irreversible): rung 1 until a named promotion. Even when promoted to 2, keep the stops under [control 4](04-stop-boundaries.md). Rung 3 is rarely appropriate.

## Common mistakes

- Recording `accepted-unedited` after only glancing at the output.
- Treating a rung as a permanent grant. It is a current reading.
- Defining the class too broadly so that easy and hard cases mix and hide failures.
- Promoting a high-risk class because the numbers look good, without a named person deciding.
- Forgetting to record. A gap in the log is a gap in the evidence.
- Counting `accepted-edited` as success. Edited means the agent was not right first time.

## How to check it is working

- Run `status` for each class. Samples, rate and rung are shown with a reason.
- Deliberately record five rejections in a test class and run `status` again. The rung drops.
- Every promotion in the log has a name.
- Rung 2 and 3 classes have a sampled-check habit with dates.
- Look at a rung 3 class once a quarter, by hand. Does the owner still agree it should be silent?

## Related

[Control 5: acceptance first](05-acceptance-first.md) · [Control 7: independent review](07-independent-review.md) · [Control 10: claim discipline](10-claim-discipline.md) · [pace guardrail](guardrails/pace.md) · [rules index](README.md)
