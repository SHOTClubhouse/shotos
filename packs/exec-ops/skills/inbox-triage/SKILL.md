---
name: inbox-triage
description: Triages one named mail account by action state and drafts replies from real threads. Use when asked to clear, sort or get on top of an inbox. Asks which account, lists its existing labels and uses only those; never sends.
---

# Inbox triage

Sort mail by what it needs from the owner, draft the replies, and surface what has gone quiet. The output is a short list the owner can act on, not a cleaned inbox for its own sake.

Stage: Operate. Rules: 1 Stop at the boundaries, 3 Read back the real result.

## When not to use this

Skip it for a single known thread (just draft the reply), for a request to send mail, or for an account the owner has not named. Never triage someone else's mailbox on a guess.

## Steps

1. **Confirm the account.** Name the mail account and the time window in scope (for example, the last 7 days, or unread). If there are several accounts, ask which. Do not read an account that was not named.
2. **Read the existing filing scheme.** List the account's current folders or labels before any filing and treat that scheme as the owner's. A label mentioned in a note or earlier request may not exist; check, and do not assume. Never restructure the mailbox (rename, merge, delete or move folders) without asking.
3. **Read the threads.** Read each thread in full, not just the subject or the latest message.
4. **Classify each thread** into exactly one action state:
   - **Needs reply:** a person is waiting on the owner.
   - **To read:** worth the owner's time, no reply needed.
   - **Waiting on others:** the owner has acted and is waiting.
   - **For information:** keep, no action.
   - **Notification:** automated and expected.
   - **Noise:** can be ignored.
5. **Draft replies.** For needs-reply threads, write the draft from the real thread: its dates, names, questions and commitments. Save it as a draft in the account or show it in the output. Never send. If the thread lacks something needed to answer, say what is missing instead of inventing it.
6. **Check for slipped threads.** Find threads where the owner sent the last message and nobody has replied beyond a stated period (default 5 working days). List them with the date of the owner's last message and a one-line chase draft.
7. **File within the existing scheme.** Apply the closest suitable existing label if the owner has agreed to filing. If none fits, leave the thread unlabelled and add a proposal to the report: the label name you suggest and the threads it would cover. The owner decides whether it is created. Do not apply a misleading label as a stand-in.
8. **Read back.** Re-list the labels or folders and the drafts to confirm what changed. Report anything that failed.

## Output

Use [template.md](template.md): counts by state, the needs-reply list with draft status, slipped threads, label gaps and what was changed.

## Checks

- The account and window were confirmed before reading.
- The existing scheme was read first, nothing was created or restructured, and any new label was proposed rather than made.
- Each thread has one action state.
- Drafts quote facts from the thread, and nothing was sent.
- Slipped threads show who sent last and when.
