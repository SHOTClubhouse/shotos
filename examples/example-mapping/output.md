# Example map

**Story:** As a parent with more than one child at the club, I want to pay a lower fee for my second and later children, so that membership costs less for larger families.
**Person who can answer questions:** the committee, through the treasurer. The March minutes do not give the details.
**Date:** not recorded

## Rules and examples
### Rule 1: a discount applies to a sibling's registration when another child from the same family is already registered for the season
Source: found in the March minutes ("sibling discount approved, details to follow"). The amount is not in the minutes.

| Example | Follows or breaks the rule | Expected result | Status |
|---|---|---|---|
| Aisha (under-8s) registers first, then her brother Tom (under-12s) registers two weeks later | Follows | Tom is recognised as a sibling at the second registration | draft |
| A family registers both children in the same session | Follows | Both children are recognised; which one is discounted is an open question | draft |
| Two unrelated children are registered by the same parent email (a childminder) | Edge | Not siblings; no discount unless the family relationship is declared | draft |

### Rule 2: the discount amount
Source: to confirm. Two readings exist.

| Example | Reading A (treasurer): 10% off the second child | Reading B (registrar): 15 pounds off from the third child | Status |
|---|---|---|---|
| Two children: under-8s (60) and under-12s (85) | Second child is the cheaper one if we discount the cheaper, or the later one: 6.00 or 8.50 off | No discount | draft: depends on questions 2 and 3 |
| Three children: 60, 85, 110 | 10% off the second child, and nothing stated for the third | 15 off the third: 95 for the third child | draft |
| Four children: 60, 85, 110, 110 | Not stated | 15 off each of the third and fourth: 30 off in total | draft |

The two readings give different totals for the same family. For three children, A saves 6.00 to 11.00 and B saves 15.00, depending on which child counts as "second".

### Rule 3: who counts as a sibling
Source: to confirm.

| Example | Follows or breaks the rule | Expected result | Status |
|---|---|---|---|
| Two full siblings, same address | Follows | Siblings | draft |
| Step-siblings, same address | Edge | Unknown | draft |
| Cousins living in the same house | Edge | Unknown | draft |
| Siblings at different addresses (separated parents) | Edge | Unknown | draft |

## Open questions
| Question | Who can answer | Blocks building? |
|---|---|---|
| Is the discount 10% off the second child, or 15 pounds off from the third child, or something else? | Committee, through the treasurer | Yes |
| Is the discount taken from the youngest, the oldest, the cheapest or the latest-registered child? | Committee | Yes |
| Do step-siblings and cousins in the same house count? | Committee | Yes for these cases only |
| If a parent registers a second child late, is the first child's fee refunded or adjusted? | Treasurer | No, if the answer is "no refunds" |
| Is the discount on the card payment total or listed as its own line on the receipt? | Treasurer | No |

## Size check
The story is vague, not large. Four of five questions are about one decision the committee has not written down. Pause the build until the committee settles the amount. Rules 1 and 3 can proceed once the question about step-siblings is answered.

## Settled checks (Given / When / Then)
None are settled yet. These are drafts to confirm once the committee decides:

1. Given Aisha is registered for the season, when her brother Tom is registered two weeks later using the same family account, then the form recognises him as a sibling.
2. Given two unrelated children share a parent email, when the second is registered without a declared family relationship, then no discount is applied.

## Must fail or refuse
Given a family with five children (never seen at the club), when the form is completed, then the form does not guess a discount; it asks the registrar to review the registration.
