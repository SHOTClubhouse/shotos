# Control 6: Read back the real result

**The rule:** Before reporting, look at the actual result in the place where it lives, not at the agent's memory of making it.

Serves rule 3, [Read back the real result](../docs/controls.md). Matters most in **Track**, and at the end of every **Operate** step.

## Why it exists

An agent at Northgate Cycles updates the opening hours on the shop's booking page. It edits the configuration file, sees no error and reports "opening hours updated". The live page still shows the old hours: the file it edited is a template that the site only reads on the next deployment. The agent verified that its edit was saved. It never looked at the page a customer sees.

Reports built from intent ("I changed the file") are wrong often enough that they cannot be trusted. Reports built from observation ("I loaded the page and it shows 9 to 5 on Saturdays") can be.

## What the agent does

1. Looks up the **real home** of the result: where the person or system that depends on it will meet it. A page in a browser, a sent folder, a spreadsheet's calculated cells, the merged branch, the record in the other system.
2. Reads it from there, using a different path from the one used to make it where possible: open the page rather than the file, query the system rather than the log of the call.
3. Compares what it sees with each check on the acceptance card from [control 5](05-acceptance-first.md), one by one.
4. Records what it saw: the page address, the cell values, the command and its output, the id the other system returned.
5. Notes any difference between the real result and the expected one, even if small, and fixes it or reports it.
6. Marks any check it could not perform as unchecked, and says why. It does not infer a pass.
7. Reports in the Claims format from [the claims guide](../docs/claims.md), so each statement can be tested.

## What a person does

- Spot-checks one item in the real home before accepting. Pick the item the agent is least likely to have tested, such as the last row, the mobile view or a record with odd characters.
- Asks "where did you look?" when a report only says "done".
- Accepts or rejects based on what was observed, not on how confident the report sounds.

## The format

A read-back line is a claim plus where it was observed:

```
- [file] changed: config/hours.yaml
- [observed] live booking page shows Saturday 9:00 to 17:00 | where: public page, loaded 14:07 | not checked: mobile layout
```

The Stop hook and claim-check test the file and command claims automatically. Observed claims about places a tool cannot reach, such as a customer's inbox, stay with the person.

## Sizing by risk

- **Small work:** one look in the real home. A document summary is read as the recipient will see it; a one-line fix is run once.
- **Normal work:** every check on the card is observed, with the evidence kept in the task record. Edge cases get a deliberate look.
- **High-risk work:** an observer other than the author performs the read-back, per [control 7](07-independent-review.md). For external actions, the read-back uses the receipt from the other system, not the agent's own log.

## Common mistakes

- Reading back the file that was written when the thing that matters is the deployed or sent version.
- Reading the agent's own summary of the result.
- Checking the happy path only. Pair each check with the failure case from the acceptance card.
- Treating "no error" as success. Silence is not evidence.
- Looking once, then making a further change and not looking again.
- Reporting the check as passed when the tool for checking was unavailable.

## How to check it is working

- Take three recent "done" reports. Each names where the result was observed and when.
- Plant a deliberate fault, such as a wrong figure in a cell the agent edited. The agent's read-back finds it.
- For claims about change, `claim_check.py` returns SUPPORTED for each file and command claim.
- The proportion of reports later found to be wrong falls over time. Track it under [control 12](12-graduation.md).

## Related

[Control 5: acceptance first](05-acceptance-first.md) · [Control 10: claim discipline](10-claim-discipline.md) · `report-with-evidence` skill and its [README](../skills/report-with-evidence/README.md) · [the claims guide](../docs/claims.md) · [rules index](README.md)
