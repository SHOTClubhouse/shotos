# inbox-triage

**Sort a mail account by what each thread needs, draft the replies, and find the threads that went quiet.**

The agent confirms the account, lists the existing labels, reads each thread and gives it one action state: needs reply, to read, waiting on others, for information, notification or noise. It drafts replies from the real thread, flags threads where you sent last and nobody answered, and files only within the label or folder scheme you already use. It never sends, and it proposes a new label rather than creating one.

It serves the Operate stage. Rules: 1 Stop at the boundaries, 3 Read back the real result.

## The problem it solves

The operations director at Harbourside Lettings has 140 unread threads after a week away. She asked a roofing contractor for a quote nine days ago; nothing since. A landlord asked about an inspection date. A tool that sorts by keywords files the contractor thread under "done" because she was the last to write.

With the skill, the contractor thread is listed as slipped, the landlord's thread gets a draft that quotes the inspection date from the company's own notice, and a suggested "Inspections" label is proposed to her instead of being created.

## When to use it, and when not to

Use it for a backlog, a regular sweep, or a check for threads gone quiet. Skip it for one thread, for sending anything, or for an account that has not been named.

## Who it is for

Anyone with a busy inbox: operations directors, head teachers, shop owners and the assistants who support them.

## How to use it

> Triage my work inbox for the last two weeks. Draft replies where I owe one, list anything I sent that nobody answered, and file only within the labels I already have and suggest any new ones.

Output uses [template.md](template.md). Worked example: [input](../../examples/inbox-triage/input.md) and [output](../../examples/inbox-triage/output.md).

## How it connects

- **Daily:** [daily-brief](../daily-brief/README.md) uses the same signal for obligations.
- **Voice and tone:** if you keep a style guide, give it to the agent so drafts sound like you.
- **Boundaries:** [docs/controls.md](../../../../docs/controls.md).

## Needs

Mail connector: read threads, list labels, create drafts, and (only if you agree) apply existing labels. Creating labels is not needed. Sending is not needed and should stay off.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 1 of 2, Opus 2 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Name the account every time if you have more than one.
- Tell the agent the chase period for your work; five working days is only a default.
- Accept an unlabelled thread over a wrong label, and decide the agent's label proposals yourself.

## Limits

- It judges urgency from the thread, not from your private priorities.
- A draft is a starting point; it may miss context that lives outside the thread.
- Label choice is a judgement; review the first batch.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/inbox-triage/input.md), [example output](../../examples/inbox-triage/output.md).
