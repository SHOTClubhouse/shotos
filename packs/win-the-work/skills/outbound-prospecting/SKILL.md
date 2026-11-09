---
name: outbound-prospecting
description: "Plans outbound as a test on one segment: up to five eligible contacts, research and one drafted message each for a person to send. Success means qualified conversations, never volume sent. Use for outreach to strangers. Never sends; known contacts use email-reply."
---

# Outbound prospecting

Test whether one kind of buyer responds, using five carefully written messages, before writing five hundred.

Stage: Operate. Rules served: 1 (stop at the boundaries), 4 (claim only what you can show) and 3 (read back the real result). Applies control 9, pilot before scale (`rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed)).

## Context and handoff

Read the audience hypothesis, approved contact source, relationship history and actual offer. Exclude duplicates and anyone already in a live conversation.

Route replies through `email-reply` and qualification through `nudge-qualify`. Use `contextual-proposal` only when a reply or qualified conversation shows a priced proposal is warranted, after `nudge-qualify` clears the pricing gate. A sent or drafted message, an opened email or interest alone is not that evidence. Record inclusion, exclusions and drafts in the campaign record.

## When not to use this

Skip it for people who already know you (use `email-reply`), for bulk mailings or newsletters, and for anything that would be sent automatically. Do not use it where the rules of the country or the platform for unsolicited contact have not been checked by the sender.

## Steps

1. **Define one testable segment.** One kind of organisation or role, one problem, one offer, one place. Write the hypothesis: "People in segment S with problem P will take a conversation about offer O." Write what counts as success before starting: for example, two qualified conversations from five messages in three weeks. A qualified conversation means the person described the problem, agreed it matters, and agreed to a next step.
2. **Review up to five approved candidates.** Keep one row per candidate with the reason they fit. Match duplicates across email aliases and CRM records before drafting. Do not scrape, buy lists or substitute unapproved contacts.
3. **Check suppression and sender identity first.** Open the current approved suppression list (people who asked not to be contacted, clients, current conversations, competitors, anyone already being approached by a colleague). Check each of the five against it. Confirm who the sender is, that the real name, role and organisation will be shown, and that there is a way to say no. Record the suppression source, identity check and any live account overlap per candidate. Hold an unclear match for the relationship owner. Missing suppression or sender confirmation keeps the candidate out of the draft batch.
4. **Research each contact.** For each eligible contact, verify their current professional role and one recent fact that explains the fit. Record the source and date. Add detail only when it changes the decision or the draft. Mark anything unverified. Skip anything personal that is not professional and public.
5. **Draft one message per contact** for a person to send. Under 120 words; opens with the specific fact; names the problem in the contact's likely words; one clear small ask (a 15-minute conversation, not a purchase); no invented claims, no false familiarity, no fake "re:" subject; the sender's real identity and a simple opt-out line. Never claim to have met or spoken with someone. Check that any hook is relevant to the offer and would still make sense if the recipient forwarded the email. If no specific sourced reason remains, hold that draft instead of using generic praise.
6. **Mark readiness.** For each draft: ready for the sender's review only if suppression and identity are checked, facts are sourced, and the ask is clear. Otherwise record held or excluded with the reason. If fewer than five are ready, report the gap. Ask the campaign owner to confirm a smaller test and its success measure or supply more approved candidates before launch. See the [eligibility exercise](eligibility-exercise.md).
7. **Define the measure and the review.** Count qualified conversations, replies, opt-outs and bounces against the number actually sent by the sender. A ready draft is not a send or a response. After three weeks the owner reviews against the success line written in step 1. Do not extend the batch until then.
8. **Stop.** The agent does not send, schedule, enrol in a sequence or follow up.

## Output

Use [template.md](template.md): the hypothesis, success line, candidate rows with checks, drafts for eligible contacts and the review date. Save with the project, for example `.work/outbound/<segment>.md`.

## Checks

- One segment, one hypothesis, success defined as qualified conversations.
- The batch contains at most five distinct approved contacts. Every held or excluded candidate has a reason. Drafts cite the relevant source.
- Suppression and sender identity recorded as checked for every contact before "ready".
- Every draft is for a named sender to send; none claims a past meeting or an unverified fact.
- No sending, scheduling or follow-up.
