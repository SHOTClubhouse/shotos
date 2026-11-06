# quarantine

**Put doubtful files in a quarantine folder with a register, rather than deleting them, and review on a date.**

This skill moves files with an unknown owner, possible personal data, possible duplicates or unclear rights into a `_quarantine` folder and records each in a register: file, why, found by, date, decision needed and owner. It sets a review date. Nothing is deleted.

It supports the Operate stage. It serves rule 1, Stop at the boundaries, and rule 4, Claim only what you can show.

## The problem it solves

A tidy-up at Northgate Cycles turns up a spreadsheet of customer names and phone numbers in a shared folder, and a folder of product photos with no sign of who took them. Deleting them risks losing something the business needs. Leaving them risks exposing personal data. A quarantine folder with a register makes someone decide by a date.

## When to use it, and when not to

Use it when you meet a file you cannot classify: unknown owner, possible personal data, possible duplicate, unclear licence or origin.

Skip it for files that are clearly owned, wanted and safe. Do not quarantine files you were not asked to touch, and never use it to hide a file from its owner.

## Who it is for

- Anyone tidying a shared folder.
- Data protection leads and office managers.
- Agents that find doubtful files while doing other work.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> While tidying the marketing folder you found three files you are unsure about. Quarantine them, write the register and set a review date.

You get a quarantine folder with the files moved into it, a register entry for each, and a review date. At the review, the owner records a decision for each entry.

## How it connects

- **Related:** [filing-and-dedupe](../filing-and-dedupe/README.md) sends doubtful files here.
- **Next:** [sensitive-data-check](../../../trust/skills/sensitive-data-check/README.md) applies if a file holds special-category or children's data.
- **Rules:** [04, stop-boundaries](../../../../rules/04-stop-boundaries.md): deletion is the owner's decision.

## Needs

Nothing beyond the agent, plus read and write access to the folder. No connectors.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 3 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Write why in one plain sentence a stranger could check.
- Leave the quarantine folder out of any sync or share while it holds possible personal data.
- Name an owner for every entry, even if the owner is the person who found it.
- Set a real date for review and put it on a calendar yourself.

## Limits

- The skill cannot tell whether a file is lawful to hold; it can only flag and move.
- A quarantine folder is still storage. Personal data in it needs the same protection as anywhere else.
- If nobody reviews it on the date, the folder becomes the next mess.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/quarantine/input.md) and [output](../../examples/quarantine/output.md).
