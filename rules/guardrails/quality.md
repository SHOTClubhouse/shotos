# Guardrail: Quality

## What it protects

The standard of finished work, and the reader's ability to rely on it. Quality here is not polish. It is that the work does what it was agreed to do, can be checked by someone else, and says only what it can support.

## Minimum practice

### 1. Definition of Done

A piece of work is done only when every line below is true. Adopters can add lines for their domain; they should not drop these.

- [ ] The owner and the outcome were agreed before the work started, with an acceptance card ([control 5](../05-acceptance-first.md)).
- [ ] Every check on the card has been run, including at least one failure case, and the results are recorded.
- [ ] The result was read back in its real home, not from the agent's memory ([control 6](../06-read-back.md)).
- [ ] The review level in the route line was met ([control 7](../07-independent-review.md)).
- [ ] The report ends with a Claims block, with installed, executed and accepted kept apart and figures labelled ([control 10](../10-claim-discipline.md)).
- [ ] Things not checked are listed as such.
- [ ] No boundary action happened without a named yes and a receipt ([control 4](../04-stop-boundaries.md)).
- [ ] The task record is current and holds no data it should not ([control 11](../11-context-control.md)).
- [ ] The named owner has accepted the work. Not the agent, not the reviewer, not claim-check.

For work an external reader will meet, add: the reader's needs were considered, the wording is plain, no figure is unsourced, and a second person has read it as the recipient would.

### 2. The skill quality gate

A skill (a reusable instruction an agent follows) must pass this gate before it is added to a shared library. It applies to your own skills as well as those you adopt.

1. **Format.** One folder, a `SKILL.md` with a name matching the folder and a one-line description that says what and when. Steps are numbered; there is an Output section and a Checks section. See [the skill format](../../docs/skill-format.md).
2. **Boundary.** If the skill can act outside the project, it drafts by default and stops for a named person's yes. No automated likes, follows, comments, sends, posts, purchases or deletes.
3. **Examples.** At least one realistic invented input with an output that passes the skill's own checks. No real people, customers or data.
4. **Cases.** At least one normal case and one contrary case: the agent refuses, asks first, drafts instead of sending, or stays honest about a gap.
5. **Secrets.** None in the skill, its examples or its history.
6. **Evidence.** The README states whether it has been run. "Cases written, not yet run" is honest; "tested" is not, unless it has been run against the cases and the results kept.
7. **Language.** Plain, British English, sentences with verbs, no filler.
8. **Review.** Someone other than the author has read it and tried it on an example.

## Checks

- Pick any "done" item. Walk the Definition of Done list against its record. Every line has an answer and a pointer.
- Look at the last month's rejected work. Which line of the list would have caught it? If none, add a line.
- Run claim-check on the last five reports. Unsupported claims are explained.
- Pick a skill at random. Run its contrary case. The agent refuses or drafts.
- Compare first-pass acceptance across task classes with `python .shotos/tools/graduation_log.py status`. A class whose rate is falling has a quality problem to find.
- Ask a reviewer who has not seen the work to find one fault in ten minutes. If they find none on several occasions, change what you give them.

## Controls and skills

| Control | How it applies |
|---|---|
| [5: acceptance first](../05-acceptance-first.md) | The standard is set before the work |
| [6: read-back](../06-read-back.md) | The standard is tested where the work lives |
| [7: independent review](../07-independent-review.md) | A second view sized to the risk |
| [10: claim discipline](../10-claim-discipline.md) | The report says no more than the proof shows |

Skills: `agree-acceptance`, `report-with-evidence`. claim-check and the Stop hook test the Claims block.

## Common failure

A reviewer at Millbrook Rovers is shown a summary and the author's explanation of why it is right. Both seem sound. The reviewer approves it. The summary leaves out the guest-pass rows. The review packet in [control 7](../07-independent-review.md) would have given the reviewer the acceptance card and the data, not the author's conclusion.
