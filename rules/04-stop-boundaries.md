# Control 4: Stop at the boundaries

**The rule:** No external send, spend, delete, overwrite, deploy or publish happens without the owner's yes, and the agent drafts everything up to that point. When the owner's request names an action inside the project, that request is the yes for it.

Serves rule 1, [Stop at the boundaries](../docs/controls.md). Matters in every stage and most in **Operate** and **Own**.

## Why it exists

A small business owner, Dev at Northgate Cycles, asks an agent to "chase the three overdue invoices". The agent finds the invoices, finds the customers' emails and sends polite reminders. One customer had already paid by bank transfer that morning; another had been promised an extension by phone. Three emails went out under Dev's name, and the agent could not take them back.

The agent did a reasonable thing in an unreasonable way. Nothing in the task said "send". The failure was treating the end of the task as the send.

## What the agent does

1. Treats these as boundary actions, needing a yes unless the owner's request already names them: **send** (email, message, post, comment, invite), **spend** (any payment or paid service), **delete** (files, records, messages, branches), **overwrite** (replace existing content that cannot be recovered), **deploy** (anything that changes a live system), **publish** (anything visible outside the team), and **change someone else's work**. Pushing to a shared remote counts as acting outside the project: other people can see it, even though it can usually be reversed. Do it when the request names it ("commit and push") and otherwise ask first.
2. **Treats an explicit request as the yes for what it names.** If the owner asked for an action inside the project ("commit the fix", "finish the colleague's change", "delete these duplicates"), the request is the approval for that action. Do it, and ask only about things the request did not cover or that cannot be undone. Asking again for what was already asked for wastes the owner's time and teaches them to ignore the questions that matter. Actions that leave the project (send, post, publish, deploy, spend) still need a yes on the exact content and recipients, because a request like "send them out" approves the intent, not the wording.
3. Does everything short of the boundary: finds the data, writes the draft, prepares the diff, builds the list of recipients and shows it.
4. Stops and shows the owner exactly what would happen: the full text, the exact recipients, the amounts, the targets.
5. Waits for a yes that names the action. "Looks fine" about a draft is not a yes to send it.
6. Performs only what was approved. If anything differs from what was shown, it stops and asks again.
7. Keeps a receipt for the action: what was done, when, to what, and the id the other system returned. The receipt is what [control 10](10-claim-discipline.md) accepts as proof that something happened.
8. Never widens an approval. A yes to send one email is not a yes to send a second.

## What a person does

- Names who may approve each boundary. By default it is the task owner; for spend or deletion it may be someone else.
- Reads the exact thing to be sent, not a summary of it.
- Says yes in words that name the action, for example "yes, send these three reminders", and no in words as well.
- Revokes approval by saying so; the agent stops and records it.

## The format

An approval request is short and complete:

```
Ready to send. 3 emails from the invoices mailbox.
To: customer A, B, C (addresses listed below)
Text: attached, identical apart from name and amount
Not sent: customer D (payment received today)
Reply "yes, send" to proceed, or tell me what to change.
```

After the action, the receipt line: `sent 3 emails 10:42, message ids in .work/receipts/send.json`.

## Sizing by risk

- **Small work:** the boundary still applies. A yes can be a single word to a clearly described single action.
- **Normal work:** the approval request lists exact items and targets. The receipt goes in the task record.
- **High-risk work:** use [control 8](08-two-session-execution.md): the approval is a frozen manifest and the action runs in a fresh session. Include a pilot under [control 9](09-pilot-before-scale.md) when more than three items are affected.

## Common mistakes

- Reading an earlier approval ("go ahead and finish this") as covering an action nobody described.
- Treating a draft saved in a mailbox as safe. Drafts in shared mailboxes or auto-send tools can still go out; check the tool.
- Sending a test message to a real person "just to check".
- Deleting a duplicate "because it was obviously a copy". Move it aside and ask.
- Approving for the person who is not the owner. A colleague's yes is only valid if the owner named them.

## How to check it is working

- Search the last month's records for any external action. Each has a named yes and a receipt.
- Run a rehearsal: ask the agent to "close out the open invoices". It should produce drafts and a list, and stop.
- Check connector permissions in the [security guardrail](guardrails/security.md): the boundary should also be enforced where the tool allows it, because instructions alone do not block a command.
- The Stop hook and claim-check flag a report that says "sent" without a receipt.

## Related

[Control 3: mode contract](03-mode-contract.md) · [Control 8: two-session execution](08-two-session-execution.md) · [Control 10: claim discipline](10-claim-discipline.md) · [rules index](README.md)
