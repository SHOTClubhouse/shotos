---
name: inbox-triage
description: Triages one named mail account by action state and drafts replies from real threads. Use when asked to clear, sort or get on top of an inbox. Asks which account, lists its existing labels and uses only those; never sends.
---

# Inbox triage

Sort mail by what it needs from the owner, draft the replies, and surface what has gone quiet. The output is a short list the owner can act on, not a cleaned inbox for its own sake.

Stage: Operate. Rules: 1 Stop at the boundaries, 3 Read back the real result.

## Context and handoff

Confirm mailbox, time window, existing folders and what the user considers urgent. Use whole threads when the latest message lacks context.

Use `email-reply` for a draft if installed. Link to the original thread and record any still-unassigned action.

## Start here

**Minimum to start:** the named account, time window and what counts as urgent. **First output:** counts by state and the needs-reply list with draft status, ahead of detail. **Uncertain:** truncated or partial thread history is flagged beside the counts, and affected threads are not marked resolved. **Handoff:** surface only the threads that need the owner's decision or reply, each with the question being asked and the date it is waiting from.

## When not to use this

Skip it for a single known thread (just draft the reply), for a request to send mail, or for an account the owner has not named. Never triage someone else's mailbox on a guess.

## Steps

1. **Confirm the account.** Name the mail account and the time window in scope (for example, the last 7 days, or unread). If there are several accounts, ask which. Do not read an account that was not named.
2. **Read the existing filing scheme.** List the account's current folders or labels before any filing and treat that scheme as the owner's. A label mentioned in a note or earlier request may not exist; check, and do not assume. Never restructure the mailbox (rename, merge, delete or move folders) without asking.
3. **Read the threads.** Read each thread in full. Identify the latest substantive human message, promised dates and any later evidence that resolves or changes the request. Mark partial or unavailable thread history as incomplete.
4. **Classify each thread** into exactly one action state:
   - **Needs reply:** a person is waiting on the owner.
   - **To read:** worth the owner's time, no reply needed.
   - **Waiting on others:** the owner has acted and is waiting.
   - **For information:** keep, no action.
   - **Notification:** automated and expected.
   - **Noise:** can be ignored.
5. **Draft replies.** Use the current question, recipients and approved commitments. Keep private notes and missing attachments out of the draft. If asked to save to the mailbox, first look for an existing draft against the same thread and source message. Reuse a current draft, flag a stale one for review and keep new text in the summary if draft access or thread history is incomplete. Never send.
6. **Check for slipped threads.** Find outstanding requests where the owner sent the last substantive human message and an agreed due date or chase period has passed. Use the owner's working calendar and timezone if given, with a default of five working days for the chase period. Automated acknowledgements do not resolve a request. Respect an explicit return date, agreed follow-up date or a later human reply. Record the last substantive date and why a chase is due.
7. **File within the existing scheme.** Apply the closest suitable existing label if the owner has agreed to filing. If none fits, leave the thread unlabelled and add a proposal to the report: the label name you suggest and the threads it would cover. The owner decides whether it is created. Do not apply a misleading label as a stand-in.
8. **Read back.** Re-list the labels or folders and the drafts to confirm what changed. Report anything that failed.

## Output

Use [template.md](template.md): counts by state, the needs-reply list with draft status, slipped threads, label gaps and what was changed.

## Checks

- The account and window were confirmed before reading.
- The existing scheme was read first, nothing was created or restructured, and any new label was proposed rather than made.
- Each reviewed thread has one action state. Report any incomplete coverage beside the counts.
- Drafts use current facts and recipients. A rerun does not create duplicate mailbox drafts.
- Slipped threads show the substantive message and the date or chase threshold used. Nothing was sent.
