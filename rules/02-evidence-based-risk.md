# Control 2: Evidence-based risk

**The rule:** Add a risk tag to a task only when evidence in the task triggers it, and name the evidence.

Serves rule 2, [Agree acceptance first](../docs/controls.md). Matters most in **Scope**, when the route is chosen, and again in **Operate**, when new facts appear.

## Why it exists

Two failures sit at opposite ends. In the first, every task is tagged "high risk" out of caution. Reviewers see the tag on a request to fix a typo and learn to ignore it, so the tag is useless on the day it matters. In the second, nothing is tagged, because nobody looked.

Take Northgate Cycles. An agent summarises a folder of customer emails into a themes list. The task looks routine and gets no tag. One email contains a customer's medical condition, quoted to explain why they could not collect a bike. The summary repeats it in a list that is later pasted into a staff newsletter. Evidence of special-category data was in the input, and nobody was required to look for it. If the rule had been "tag only when evidence triggers it, and look for the evidence", the agent would have scanned for the triggers, found the email and held the output back.

## What the agent does

1. Starts every task at **baseline**: no extra tag.
2. Before choosing the route, scans the inputs and the planned action for triggers. Use the list below as a starting point and let the adopter extend it.
3. For each trigger found, adds a tag and writes the evidence next to it: the file, the field, the sentence or the target.
4. Lets the tag change the route (see [control 1](01-route-the-work.md)): a tag means more review, a narrower mode under [control 3](03-mode-contract.md), or a person's approval.
5. Rechecks when something new arrives mid-task, such as a new input file, a new recipient or a changed target.
6. Removes a tag only when the evidence is gone, and says so.

### Starter triggers

| Evidence | Tag |
|---|---|
| Names, emails, phone numbers or addresses of individuals | `personal-data` |
| Health, religion, ethnicity, union membership, sexual orientation, biometrics | `special-category` |
| Anyone under 18 appears in the data or is the audience | `children` |
| Prices, payments, contracts, invoices, spend | `money` |
| Recipient is outside the organisation, or output will be public | `external` |
| Action cannot be undone (delete, send, publish, deploy) | `irreversible` |
| Credentials, keys or tokens appear anywhere | `secret` |
| Output informs a legal, safety or employment decision | `consequential` |

Each tag is defined further in the [data governance guardrail](guardrails/data-governance.md) and [security guardrail](guardrails/security.md).

## What a person does

- Reviews the tags and the evidence, not just the tag names. A tag with no evidence is a guess and should be questioned.
- Adds a trigger the agent could not know about, such as "this client is in a dispute".
- Removes a tag when the agent is wrong, and says why, so the next run improves.

## The format

Tags travel on the route line from control 1, each followed by its evidence:

```
risk: personal-data (customer names in emails.csv), special-category (row 214 mentions a medical condition), external (summary goes in staff newsletter)
```

## Sizing by risk

- **Small work:** scan the input quickly. If nothing triggers, say "baseline" and continue.
- **Normal work:** scan, tag with evidence, and let the tags set the review level.
- **High-risk work:** two or more tags, or any of `children`, `special-category`, `money` with `external`, `irreversible`, means a named approver, independent review and a pilot before volume.

## Common mistakes

- Tagging from the topic ("this is about HR, so high risk") instead of from the content.
- Tagging without evidence, which turns the tag into noise.
- Stopping the scan once the first trigger is found. Several tags can apply and the combination is what raises the level.
- Forgetting that the output can create a trigger the input did not have, for example by combining two lists so individuals can be identified.
- Keeping a tag after the sensitive input has been removed.

## How to check it is working

- Pick a recent task at random. Every tag has evidence beside it.
- Seed a test file with one obvious trigger (a made-up health note) and run a routine task. The agent finds it and changes the route.
- Fewer than half of recent tasks carry a tag. If nearly all do, the triggers are too broad; if none do, the scan is not happening.

## Related

[Control 1: route the work](01-route-the-work.md) · [Control 3: mode contract](03-mode-contract.md) · [guardrails](guardrails/README.md) · [rules index](README.md)
