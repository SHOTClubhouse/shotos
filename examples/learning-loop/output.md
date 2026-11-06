# Lesson record 0001: quotes using an out-of-date price list

**Status:** Proposed and tested on paper; awaiting Ines Calder's decision
**Task class or area:** `workshop-quote-draft`
**Raised by / date:** Ines Calder (owner), October review
**Owner of the instruction (can change it):** Ines Calder

## 1. Observe
Of 12 quotes drafted in October, 9 were accepted unedited and 3 were edited because the price was wrong (6, 14 and 22 October): full service 89 instead of 95 pounds, brake bleed 40 instead of 45, tyre change 15 instead of 18. All three items changed price in September. The nine quotes for items that did not change were correct. One further case on 9 October, a customer asking for last year's full service price, was correctly answered at 89 pounds and accepted. Source: Tariq's review log. Sample is small: 12.

## 2. Diagnose
| Possible cause | Shown, suspected or ruled out | What showed it |
|---|---|---|
| Input wrong or missing | Shown | The shared folder holds two lists, 2024 and 2025 |
| Instruction unclear or conflicting | Shown | "Quote from the workshop price list" does not say which one |
| Skill lacked a step | Suspected | No step to confirm which list is current |
| Model slip | Not ruled out | Cannot tell from three cases; the pattern fits an ambiguous instruction better |
| Reviewer standard changed | Ruled out | Tariq caught all three and the other nine were right |
| World changed | Shown | Prices changed on 1 September; only the changed items were wrong |

## 3. Propose
One change: in the quoting instructions, replace "quote from the workshop price list" with "quote from the price list marked current (`workshop-prices-2025.pdf`); say which list and date you used". This replaces the ambiguous sentence and adds a line showing the source. It could make things worse in September 2026 when the current list changes, if nobody updates the file name in the instruction. Note this in the review.

Ines's draft, "Never use any price list that is not dated this year", is not proposed as written, for the reason in the contrary case below.

## 4. Test
- Evidence: 3 wrong quotes of 12, all on items changed in September, cause shown by the folder contents and the wording. Strength: moderate; small sample, clear mechanism.
- Test that would have caught the event: Input: "Quote a full service." Folder contains the 2024 and 2025 lists. Must contain: 95 pounds and the name of the 2025 list. Must not contain: 89. Add two more cases for the brake bleed (45, not 40) and the tyre change (18, not 15).
- Contrary case: a customer asks "What did a full service cost last year?" The agent should answer 89 pounds from the 2024 list and label it as last year's price, not refuse. Ines's draft rule ("never use a list not dated this year") would block this correct answer, which happened on 9 October.
- Result of old versus new on the cases: not run in this draft. Run the four cases on the current and the changed instructions before promotion, using [skill-quality-gate](../../skills/skill-quality-gate/README.md).

## 5. Authority
Approved by: pending. Ines Calder owns the instruction file and decides. No other person's yes is needed; this does not touch a boundary or privacy rule.

## 6. Promotion record (to complete on approval)
- Rule as promoted: draft above, with the date and list named in each quote.
- Supersedes: the sentence "quote from the workshop price list" in the March version of the instructions.
- Review date: three months after promotion; also review when the prices change next, and rename the current list at that time.
- Where the eval cases now live: the project's evals folder, three normal cases and the last-year contrary case.

## 7. Review (filled in on the review date)
Events since, what changed, decision: keep | change | remove. By (name, date):
