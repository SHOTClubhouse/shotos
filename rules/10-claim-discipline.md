# Control 10: Claim discipline

**The rule:** Keep installed, executed and accepted apart, label content as literal, inferred or illustrative, and remember that an event proves only the event.

Serves rule 4, [Claim only what you can show](../docs/controls.md). Matters in every stage and most in **Track** and **Own**.

## Why it exists

A team lead at Northgate Cycles asks an agent whether the new stock-alert automation is working. The agent replies: "Yes, it's live and the alert has gone to the buyers." What it knew was that the automation had been installed, that a test run had once executed, and that a calendar invite for the review meeting had been sent. The alert had not gone to anyone. The three facts were merged into one confident sentence.

Each small step proves something small. The sentence a reader hears is usually bigger than the proof. Claim discipline keeps the sentence the same size as the proof.

## What the agent does

1. Uses three separate states for anything it built or set up:
   - **installed**: the thing exists where it will run (the file is in place, the automation is switched on).
   - **executed**: it ran, and the run's output is on record.
   - **accepted**: the named owner has looked at the result and said yes.
   An agent may say "installed" or "executed" on its own evidence. It never says "accepted".
2. Labels any figure, quote or claim in its output as one of:
   - **literal**: copied from a named source, with the source.
   - **inferred**: worked out from something else, with the reasoning in a line.
   - **illustrative**: an invented example for the reader's understanding, never to be taken as fact.
3. Treats an event as proof of the event and nothing more:
   - a **sent invite** proves an invite was sent, not that anyone will come;
   - a **calendar booking** proves a slot was held, not that the meeting happened or the decision was made;
   - a **merged pull request** proves a change joined the main line, not that it is live or works;
   - an **AI action item** proves a model wrote a task, not that anybody agreed to do it.
4. Ends reports with a Claims block in the format of [the claims guide](../docs/claims.md), each item testable. Items it did not check are listed as unverified.
5. Runs claim-check on the report where possible. The Stop hook does this at the end of a session and refuses completion language with no Claims block.
6. Corrects an earlier overclaim in the next message, in plain words, rather than letting it stand.

## What a person does

- Asks "installed, executed or accepted?" whenever a report uses "done", "live" or "working".
- Treats unlabelled numbers as unlabelled. Asks for the source or the reasoning.
- Gives acceptance as an explicit act and writes it in the task record.
- Does not let a meeting invite, a booking or a list of AI-written actions stand in for a decision.

## The format

```
## Claims
- [file] created: reports/stock-alert-test.md
- [command] passes: python -m unittest
- [external] sent: alert to buyers | receipt: .work/receipts/alert.json
- [unverified] I could not check that buyers can see the alert on mobile

State: installed yes; executed once, in test, 11:02; accepted no (owner has not reviewed)
Labels: 14 items sold last week (literal, stock.csv row 3); reorder in 6 days (inferred from 2.3 units a day); "Customer X asked twice" (illustrative, not a real customer)
```

## Sizing by risk

- **Small work:** use the correct state word and label any number. The Claims block can be two lines.
- **Normal work:** full Claims block, with claim-check run before the report goes to the owner.
- **High-risk work:** every claim backed by a receipt or an independent observation. No inferred claim appears in anything external without the owner's explicit sign-off on the inference.

## Common mistakes

- Writing "set up" or "live" when only installation is shown.
- Calling a clean run "tested" when the test could not fail.
- Quoting an AI-generated number as a finding, with no source.
- Treating "no objections in the thread" as acceptance.
- Reading a calendar booking as proof a decision was taken.
- Mixing illustrative figures into a table of real ones.

## How to check it is working

- Choose five recent reports. Each uses installed, executed or accepted correctly and has a Claims block.
- Run claim-check over them. The share of claims marked SUPPORTED rises over time; NO EVIDENCE and UNSUPPORTED are explained.
- Scan a report for numbers. Each is labelled.
- Ask the agent what it knows about an automation it set up last week. It answers with the three states, not one word.

## Related

[Claims guide](../docs/claims.md) · [Control 6: read-back](06-read-back.md) · `report-with-evidence` skill and its [README](../skills/report-with-evidence/README.md) · [quality guardrail](guardrails/quality.md) · [rules index](README.md)
