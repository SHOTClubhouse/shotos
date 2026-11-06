# label-the-proof

**Mark every figure, quote and example as literal, inferred or illustrative, and edit the one real file instead of making copies.**

The agent labels each claim-bearing part of an artefact by how it is known. Literal means taken directly from a source or the real system. Inferred means reasoned from evidence. Illustrative means made up to show the idea. It then edits the canonical file in place so the labels stay true.

It belongs to the Build step but applies anywhere. It serves rule 4, Claim only what you can show, and rule 3, Read back the real result. The detail is in [rules/10-claim-discipline.md](../../rules/10-claim-discipline.md).

## The problem it solves

Millbrook Rovers youth club sends its committee a draft dashboard with a table of attendance by age group, a chart and a "projected membership" line. Half the numbers are real, one is a guess and the chart uses sample values that were never replaced. A committee member quotes the projection at the league meeting as if the club had counted it. There are also three files, `dashboard.xlsx`, `dashboard-v2.xlsx` and `dashboard-final.xlsx`, and no one knows which is current.

## What the agent does differently

It labels the attendance table literal, with the sheet and date range as the pointer. It labels the projection inferred, with the three data points and the method. It labels the chart illustrative and says it must be replaced before use. It edits `dashboard.xlsx` in place and deletes nothing, noting where the old versions are kept. See [examples/label-the-proof/output.md](../../examples/label-the-proof/output.md).

## When to use it, and when not to

Use it for reports, proposals, dashboards, demos and examples where a reader could mistake an example for a result. Skip it for short chat answers with no factual claims.

## Who it is for

- **Anyone who sends a report upward:** it protects you when a number is quoted.
- **Reviewer:** can see in a minute which parts to check first.
- **Teams with many near-copies of files:** one file, with history kept by the tool.

## How to use it

> Label the proof in `dashboard.xlsx` as literal, inferred or illustrative. Edit the file in place. Do not make a new version.

Read the label table, and check a literal item against its source.

## How it connects

- **Before:** [research-and-assemble](../research-and-assemble/README.md) produces the source log that supplies the pointers.
- **After:** [report-with-evidence](../report-with-evidence/README.md) turns the labelled artefact into a report, and [evidence-handoff](../evidence-handoff/README.md) records what was accepted.
- **Reference:** [docs/claims.md](../../docs/claims.md) and [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent. Editing a file in place needs write access to that file.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 1 of 2, Opus 1 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Mark illustrative material where the reader will see it, not in a footnote.
- If you cannot find the source for a number, it is not literal.
- Say whether a thing is installed, run and accepted. They are three claims.

## Limits

- A literal label is only as good as the source behind it.
- The skill relies on the agent to label honestly; a reviewer should check a sample.
- Some tools keep poor version history. Where that is so, the skill asks for a dated archive, not a copy beside the original.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/label-the-proof/input.md) and [output](../../examples/label-the-proof/output.md).
