---
name: outbound-prospecting
description: "Plans outbound as a test on one segment: five contacts, research each, one drafted message each for a person to send. Success means qualified conversations, never volume sent. Use for outreach to strangers. Never sends; known contacts use email-reply."
---

# Outbound prospecting

Test whether one kind of buyer responds, using five carefully written messages, before writing five hundred.

Stage: Operate. Rules served: 1 (stop at the boundaries), 4 (claim only what you can show) and 3 (read back the real result). Applies control 9, pilot before scale (`rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed)).

## When not to use this

Skip it for people who already know you (use `email-reply`), for bulk mailings or newsletters, and for anything that would be sent automatically. Do not use it where the rules of the country or the platform for unsolicited contact have not been checked by the sender.

## Steps

1. **Define one testable segment.** One kind of organisation or role, one problem, one offer, one place. Write the hypothesis: "People in segment S with problem P will take a conversation about offer O." Write what counts as success before starting: for example, two qualified conversations from five messages in three weeks. A qualified conversation means the person described the problem, agreed it matters, and agreed to a next step.
2. **Choose a batch of five.** Five named contacts from the sources the person provides, each with the reason they fit the segment. Do not scrape, buy lists or add contacts that the person has not approved.
3. **Check suppression and sender identity first.** Ask for the suppression list (people who asked not to be contacted, clients, current conversations, competitors, anyone already being approached by a colleague). Check each of the five against it. Confirm who the sender is, that the real name, role and organisation will be shown, and that there is a way to say no. Record both checks per contact. If either list is missing, the contact is not ready.
4. **Research each contact.** Five to eight lines per person from approved sources: role, what the organisation does, one recent specific fact tied to the problem, and the source. Mark anything unverified. Skip anything personal that is not professional and public.
5. **Draft one message per contact** for a person to send. Under 120 words; opens with the specific fact; names the problem in the contact's likely words; one clear small ask (a 15-minute conversation, not a purchase); no invented claims, no false familiarity, no fake "re:" subject; the sender's real identity and a simple opt-out line. Never claim to have met or spoken with someone.
6. **Mark readiness.** For each draft: ready for the sender's review only if suppression and identity are checked, facts are sourced, and the ask is clear. Otherwise "not ready" with the reason.
7. **Define the measure and the review.** Count qualified conversations, replies of any kind, opt-outs and bounces. After three weeks the owner reviews against the success line written in step 1. Do not extend the batch until then.
8. **Stop.** The agent does not send, schedule, enrol in a sequence or follow up.

## Output

Use [template.md](template.md): the hypothesis, success line, five contact rows with checks, five drafts and the review date. Save with the project, for example `.work/outbound/<segment>.md`.

## Checks

- One segment, one hypothesis, success defined as qualified conversations.
- Exactly five contacts, each with sourced research.
- Suppression and sender identity recorded as checked for every contact before "ready".
- Every draft is for a named sender to send; none claims a past meeting or an unverified fact.
- No sending, scheduling or follow-up.
