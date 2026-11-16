# show-me

**Show the point with the smallest thing that proves it, and say which parts are real.**

The agent names the reader, the one question and the claim to prove, then picks the lowest form of demonstration that answers it: the real thing, a compact example, a static visual, an interactive page or a working prototype, in that order. It labels each part literal, inferred or illustrative and edits the existing file instead of making a copy.

It belongs to the Operate stage but applies anywhere. It serves rule 2, Agree acceptance first, rule 3, Read back the real result, and rule 4, Claim only what you can show. The detail is in [rules/10-claim-discipline.md](../../rules/10-claim-discipline.md).

## The problem it solves

The treasurer of Ashby Lane Youth Club explains in four paragraphs why a new set of age-band fees will not cost families more. The committee still disagrees after two meetings. Meanwhile a volunteer offers to build an interactive fee calculator for a decision that a small table would settle.

## What the agent does differently

It writes down the reader (the committee), the question (do the new bands cost families more?) and the source (the fee list and the membership register in `fees.xlsx`). It stops at level 2: a short before-and-after table. The band counts and totals are labelled literal, the four sample families illustrative. The table goes on a new sheet in the existing `fees.xlsx`, not in a copy. The table also shows something the paragraphs hid: the club would collect less in total. See [examples/show-me/output.md](../../examples/show-me/output.md).

## When to use it, and when not to

Use it when someone says "show me", asks for a mock-up, a worked example or a before-and-after, or when an explanation has not landed. Skip it for a plain factual answer or a finished document in a set format.

## Who it is for

- **Anyone explaining a change to a committee, a manager or a customer:** one table instead of four paragraphs.
- **Designers and product people:** a rule for when a prototype is worth building and when it is not.
- **Reviewers:** every figure on the page traces to a source or an illustrative label.

## How to use it

> Show me what the new fee bands mean for families. Use the smallest form that proves it and label what is real. Edit `fees.xlsx`, do not make a copy.

Read the table, then trace one figure back to the register.

## How it connects

- **Before:** [capture-the-problem](../capture-the-problem/README.md) names the question, and [research-and-assemble](../research-and-assemble/README.md) gathers the source.
- **After:** [report-with-evidence](../report-with-evidence/README.md) when the reader needs a finished report, or [build-small-website](../../packs/content/skills/build-small-website/README.md) when they need a finished site.
- **Related:** [label-the-proof](../label-the-proof/README.md) supplies the three labels.

**Needs:** Nothing beyond the agent for levels 1 and 2. A browser or renderer for levels 3 to 5. Editing in place needs write access to the file.

## Tips

- Start from the question, not from the form you would enjoy building.
- A table that a reader can check beats a page they can only click.
- Put the illustrative label beside the made-up figure, not in a footnote.

## Limits

- Labels are only as honest as the sourcing behind them.
- A polished mock-up can still persuade more than it should. Keep it at the level the question needs.
- The skill cannot check a visual it cannot open. It says so and stays at level 1 or 2.

**Evidence:** Cases written, not yet run.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/show-me/input.md) and [output](../../examples/show-me/output.md).
