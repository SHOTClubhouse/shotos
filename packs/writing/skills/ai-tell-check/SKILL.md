---
name: ai-tell-check
description: Finds and fixes machine-sounding patterns in a draft, such as em dash tics, stacked threes, empty intensifiers and overused words. Use when a draft is about to reach a reader. Keeps facts; clarity and jargon belong to plain-english-check.
---

# Find and fix machine-written patterns

Make a draft sound like a person wrote it, by finding the known patterns, fixing them and showing every change.

**Stage:** Track. **Rules served:** rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the intended audience, approved voice sample and source draft. Distinguish a specific phrasing problem from a mere stylistic preference.

Use `plain-english-check` if clarity is the issue. Save edits in the owning draft without changing meaning.

Cite the approved source brief or draft revision so fixes can be compared with it. If `.work/capabilities.md` exists, read the section for this runtime. If a file or diff tool is missing, say so first, report findings in chat with line numbers and mark the check pending.

## When not to use this

Do not use it to disguise authorship or to get past a rule that requires disclosure of AI use. Do not use it on quotations, legal text or text the owner has said must stay as written. Do not run it as the only check: a text can be free of these patterns and still be wrong.

## Steps

1. **Number the lines.** Work on a numbered copy so each finding can be located. Keep the original untouched.
2. **Scan for the patterns.** Check each of the seven below and record the line number and the exact words found.
3. **Em dash as a tic.** Any em dash used where a comma, full stop, colon or semicolon would do. One in a long text may be fine; a pattern of them is the finding. Follow the owner's rule on em dashes; if there is none, flag only repeated use.
4. **Stacked threes.** Three parallel adjectives, nouns or clauses in a row, such as "fast, simple and reliable". Also lists of fragments standing in for a sentence.
5. **Empty intensifiers and openers.** Words like "truly", "incredibly", "genuinely", "really" and "very" that add no information, and openers such as "In today's fast-moving world".
6. **Standalone declaratives.** A one-line paragraph or sentence added only for weight, such as "That matters." or "This changes everything."
7. **Overused words.** Search for the common set: tapestry, testament, pivotal, crucial, landscape, realm, navigate, foster, harness, unlock, streamline, holistic, comprehensive, vibrant, cutting-edge, underscore, showcase. Add any words the owner has banned. One use of a word is fine when it is the right word; repeated or decorative use is the finding.
8. **Fake balance.** "On one hand, on the other hand" with no conclusion, or "it depends" with no statement of what it depends on. Replace with the position the evidence supports.
9. **Repeating summary.** A closing paragraph that restates the body ("In summary", "In conclusion", "Overall"). Cut it, or replace it with the next step.
10. **Fix without changing facts.** For each finding, write the fix as a sentence with a verb and one idea. Compare every number, name, date and claim before and after. If anything differs, undo that fix.
11. **Report.** Give each finding as: line number, pattern, the words found, the fix. Then give counts per pattern before and after, and anything left because it was the right word.

## Output

A findings table (line, pattern, found, fix), the fixed draft saved beside the original, and counts per pattern before and after. State plainly that the check finds patterns, not authorship.

## Checks

- Each finding names a line and quotes the words found.
- Every fix keeps all facts, numbers, names and dates unchanged.
- No new factual claim is introduced; a replacement that needs one is a placeholder.
- No fix introduces a new stacked three, intensifier or standalone declarative.
- The original is kept and the fixed version is a separate file.
- The report does not claim the text is now undetectable or certified human.
- Reviewer check: pick one finding by line number and confirm the original words, the fix and unchanged facts against the source draft.
