# Control 7: Independent review

**The rule:** Size review to the risk, give the reviewer the acceptance and the evidence but not the author's conclusion, and treat agreement as information, not authority.

Serves rule 3, [Read back the real result](../docs/controls.md). Matters most in **Operate** and **Track** for work that matters.

## Why it exists

An analyst at Millbrook Rovers asks an agent to work out how many members renewed. The agent writes the query, runs it, and then, in the same session, reviews its own work and finds it correct. The query counted anyone with a payment in the period, including people who had paid for a guest pass. The review in the same session repeated the same assumption, because it had the same context and the same blind spot.

Checking your own work is discipline, not review. A second pass catches errors only when it differs from the first in some way: another agent, another model, another person, or a fresh session that was given the acceptance and the evidence but not the author's story.

## What the agent does

As **lead** (author):
1. States the review level from the route line in [control 1](01-route-the-work.md).
2. Prepares a review packet: the acceptance card, the exact output revision, the approved evidence and what was not checked. Share only the inputs the reviewer needs and is allowed to access. Route any remaining check to an authorised reviewer. It leaves out its own reasoning and its verdict.
3. Hands the packet over and does not argue the reviewer into agreement.
4. Fixes the findings it accepts and answers, with evidence, the ones it disputes.

As **reviewer**:
1. Reads the acceptance card first, then the output, then the evidence.
2. Tries to break the work: runs the failure case, checks the edge, looks for what is missing.
3. Reports findings by severity: blocks acceptance, should change, note.
4. States what it could not check.
5. Does not accept the work. Acceptance belongs to the owner.

## What a person does

- Chooses the level of review when the route is set.
- Reads disagreements between lead and reviewer. A disagreement is the most useful output of the whole exercise.
- Resists counting agreement as proof. Two agents trained on similar data can be wrong in the same way.
- Accepts or rejects. The owner may overrule a reviewer, and records why.

## The format

The review packet and result:

```
review level: independent (different session, same acceptance)
packet: acceptance.md, output/renewals.xlsx, evidence/query.sql, not checked: guest-pass handling
result: blocks acceptance (1), should change (2), notes (1)
  1. Count includes guest passes (rows 41 to 58). Failure case 3 on the card not met.
decision: owner
```

## Sizing by risk

| Work | Review |
|---|---|
| **Small** (reversible, internal, easy to see) | Self-check against the card. A person glances at the result. |
| **Normal** (someone relies on it) | One independent pass: a fresh session or another model with the packet, plus the owner's review. |
| **High-risk** (money, personal data, external, irreversible, consequential) | Independent review by a different model or person, a human reviewer who has read the packet, and the split in [control 8](08-two-session-execution.md). Add a specialist only for a distinct risk the pair cannot test, such as security or legal. |

## Common mistakes

- Giving the reviewer the author's summary of the work. They will agree with it.
- Asking "is this good?" instead of "does this meet these checks, and what would break it?".
- Stacking many reviewers on low-risk work. Review has a cost in time and attention; spend it where risk is.
- Treating two agents agreeing as a reason to skip the human.
- Letting the reviewer fix the work silently. Findings go back to the author and are recorded.
- Ignoring the "could not check" list.

## How to check it is working

- Look at the last ten reviews. In how many did the reviewer find something? Never finding anything means the reviews are too gentle or the packets leak the conclusion.
- Seed a known flaw, such as the guest-pass rows, and see whether the reviewer finds it.
- High-risk work in the last month all has a named human reviewer.
- Findings and the decisions made on them are in the task record.

## Related

[Control 5: acceptance first](05-acceptance-first.md) · [Control 8: two-session execution](08-two-session-execution.md) · [quality guardrail](guardrails/quality.md) · [rules index](README.md)
