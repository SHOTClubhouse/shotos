---
name: plain-english-check
description: "Fixes a draft for plain English without changing its meaning: amounts, dates and obligations stay; requested term changes are a separate marked edit for the owner to confirm. Use for emails, notices, policies and guides. Style tics belong to ai-tell-check."
---

# Check a draft for plain English

Make a draft readable on the first pass by the person it is for, without changing what it says.

**Stage:** Track. **Rules served:** rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the reader’s task, decision and terms they already use. Preserve legally or technically meaningful language when simplifying.

Use `claims-audit` if a proposed edit changes meaning. Record the edited text in the original document.

Cite the approved source brief or draft revision so fixes can be compared with it. If `.work/capabilities.md` exists, read the section for this runtime. If a file or diff tool is missing, say so first, report the edit in chat beside the original text and mark the check pending.

## When not to use this

Do not use it on legal wording, quoted text, regulated notices or anything that must stay word for word. Flag the problems and leave the text alone there. Do not use it to shorten a draft whose length the owner has fixed.

## Steps

1. **Confirm the reader and the spelling.** Ask who reads it, what they already know and what they must do afterwards. Ask whether the owner wants British or American English. If unanswered, use the spelling the draft already uses and say so.
2. **Find the answer.** State the main point or the action the reader must take in one sentence. If the draft opens with background, move the answer to the first sentence and keep the background below it.
3. **Set the length.** Choose a length for this reader: a notice for the public can be two short paragraphs, a briefing for a specialist can run longer. Say the target before editing.
4. **Shorten sentences.** Aim for an average under 20 words and split anything over 30. One idea per sentence. Two facts become two sentences.
5. **Use active verbs.** Change "the form must be completed by the tenant" to "the tenant completes the form". Turn noun phrases back into verbs: "make a decision" becomes "decide".
6. **Handle jargon.** For each specialist term, either replace it with a plain word or explain it once the first time it appears. Leave a term alone if the reader uses it every day, and say that you did.
7. **Replace weak words.** Swap long words for short ones where the meaning stays the same, remove hedges that add nothing, and cut phrases like "in order to" and "due to the fact that".
8. **Protect the facts.** Compare numbers, dates, names, amounts and commitments before and after. If any differ, undo the change. A plain-English pass keeps the meaning. If the request also asks to change an amount, a date or an obligation (a shorter notice period, a dropped fee), do not fold it into the clause. Show the plain-English version with the original terms intact, and list the requested change as a separate, clearly marked edit that is not applied until the person who owns the clause confirms it. Show the original terms next to it.
9. **Report.** List the changes by type with a count, show the before and after for the biggest three, and list anything you flagged but did not change.

## Output

The fixed text, then a short change report: reader and spelling used, target length against actual length, average sentence length before and after, jargon handled, and any flagged items left alone. Save the fixed text beside the original, never over it.

## Checks

- The first sentence states the point or the action.
- No sentence over 30 words remains, unless flagged as fixed wording.
- Every specialist term is replaced or explained once, or marked as known to this reader.
- Numbers, dates, names and commitments match the original exactly.
- Any requested change to terms is a separate marked edit, with the original terms shown, awaiting the owner's confirmation.
- The spelling matches the owner's choice throughout.
- The original text is still available.
- Reviewer check: pick one sentence containing a number or date and confirm it matches the original word for word.
