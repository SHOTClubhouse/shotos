# proposal-factory

**Produce many tailored proposals from one master, pilot three first, check every item, and send none.**

The agent builds a master proposal with reader variables, fills a reader sheet with sources, pilots three proposals for the owner to accept, runs the rest in groups, checks claims, names and rendering per item, and ends with a batch report.

It belongs to **Operate**. It serves rule 3, Read back the real result, rule 4, Claim only what you can show, and rule 1, Stop at the boundaries, and applies [control 9, pilot before scale](../../../../rules/09-pilot-before-scale.md).

## The problem it solves

Millbrook Rovers youth club wants to ask 18 local businesses for sponsorship. A volunteer copies the first proposal 18 times and changes the company name. Three proposals still name the garage the master was written for, one uses the wrong price, and a sponsorship ask to a bakery talks about "your fleet of vehicles". The volunteer sent the first ten before anyone noticed.

## When to use it, and when not to

Use it when [one-off-or-factory](../one-off-or-factory/README.md) has recommended a factory and you need five or more proposals that differ by reader detail.

Do not use it for fewer than five, for proposals that differ in substance, or without a decision record.

## Who it is for

- Fundraisers and club committees approaching many local businesses.
- Sales teams with a repeated offer for different readers.
- Founders who need volume without losing the feeling of being written to.

## How to use it

> The decision record says factory. Here is our accepted master and the list of 18 businesses. Build the variable list, pilot three, and give me the batch report. Send nothing.

The decision record already holds a pilot of three that you accepted, with the master revision each was made from. The agent reuses those three accepted proposals if the master revision, the reader data and your acceptance still match, and redoes only an item that changed or has no accepted output. It stops if your signoff is missing or the record says author directly. Read the pilot items, correct the master if needed, and tell the agent to continue. The batch report uses [template.md](template.md).

For a restart, or to reuse the accepted pilot, use the [worked revision check](restart-example.md). It shows which pilot items and drafts can be reused, which buyer changes need a new review and how to preserve an owner's edits.

## How it connects

- **Before:** [one-off-or-factory](../one-off-or-factory/README.md) decides; [contextual-proposal](../contextual-proposal/README.md) produces the master.
- **Alongside:** [relationship-map](../relationship-map/README.md) for warm routes; [outbound-prospecting](../outbound-prospecting/README.md) for the messages that carry the proposals.
- **Rule:** [rules/09-pilot-before-scale.md](../../../../rules/09-pilot-before-scale.md).

## Needs

Nothing beyond the agent. A spreadsheet or CSV of readers helps. Rendering needs a way to produce and view the file.

## Tips

- Leave a value blank rather than inventing it. A blank gets fixed; an invention gets sent.
- Search every file for the master reader's name before accepting the batch.
- Ask for the least typical reader in the pilot.
- Do not rerun a pilot that the owner accepted. Check each item against its master revision and recheck only what changed.

## Limits

- The batch is only as personal as the reader sheet. Thin research makes thin proposals.
- Rendered checks by the writing agent are not independent. Ask a person to read a sample.
- It never sends, schedules or uploads.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/proposal-factory/input.md) and [output](../../examples/proposal-factory/output.md).
