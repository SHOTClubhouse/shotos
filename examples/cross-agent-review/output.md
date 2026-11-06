# Cross-agent review record

**Work reviewed:** rents for 64 tenancies (`rents-2026.xlsx`) and the tenant letter (`letter-draft.docx`)
**Owner (decides):** the owner of Harbourside Lettings
**Date:** not recorded
**Why a review is needed:** the letters go to 64 tenants outside the team, and a rent above a contractual cap is a breach. Tags: `money`, `external`, `legal`, `personal-data`. Route: lead agent plus an independent reviewer

## Who did what
| Role | Model or runtime | Access |
|---|---|---|
| Lead | Claude Code | Read and write in the project |
| Reviewer | Codex, a different runtime and model | Read-only |

## Packet given to both
- Acceptance card: the three checks and the refuse case above, unchanged
- Evidence: `rents-2026.xlsx`, `agreements/`, the CPI source (3.4%), `letter-draft.docx`
- Boundaries: nothing is sent, and no file is changed by the reviewer
- The reviewer was not shown the lead's "all within caps" claim until its own report was in

## Findings
| # | Finding | Where | Check it fails | How to verify | Lead's response | Outcome |
|---|---|---|---|---|---|---|
| 1 | Row 31: flat 3% cap, new rent 721 is exactly 3% on 700 and passes. Row 52: flat 3% cap, 640 to 668 is 4.4%, over the cap. Maximum under the agreement is 659.20 | Rents sheet, row 52; agreement for row 52, clause 4.2 ("increase not to exceed three per cent") | Card check 1 | Compute 640 x 1.03 and compare with 668 | Accept. The lead applied the CPI rule to a flat-3% agreement | Fixed to 659.20. Reviewer rechecked: correct |
| 2 | Row 47: CPI is 3.4% and 5% is higher, so the cap is 3.4%. 1,100 x 1.034 = 1,137.40, which is within the cap | Row 47 | Card check 1 | Compute 1,100 x 1.034 | No action; included so the owner can see it was checked | Passes |
| 3 | Row 58 has no agreement on file, but a new rent has been calculated | Row 58; `agreements/` has 63 PDFs | Card refuse case | Count the PDFs; search for the tenancy ID | Accept. The lead calculated from the previous year's rule without the agreement | Row 58 cleared and marked "no agreement on file, owner to find it" |
| 4 | The letter states a one-month notice period for every tenant. Two agreements (rows 9 and 22) say two months | Letter, notice paragraph; agreements for rows 9 and 22, clause 7 | Card check 2 | Read clause 7 in both PDFs | Disputed in part: the lead says the letters are templates. Reviewer says the template must change for these two | Passed to the owner. Both sides below |
| 5 | The CPI figure of 3.4% is from a release the reviewer could open, but it names a month the lead did not give | CPI source | Not a card check | Compare the release month with the month in the agreements | Lead to confirm the month | Open |

## Checked and found fine
- The other rows were recomputed independently from the agreements and agree with the sheet
- The effective date and old rents in the letter match the sheet for the 10 letters sampled

## Could not be checked
- Whether the letter wording meets housing law. The reviewer is not able to judge that, and says so. A person with housing law knowledge should read it
- Whether the CPI release is the one each agreement names

## Disagreements between lead and reviewer
Notice period. Lead: one month is the default in the template and the two exceptions are rare. Reviewer: the agreements for rows 9 and 22 say two months, so the letters for those tenants would give too little notice and could void the increase. Both agree the fix is cheap: use a different paragraph for those two. The owner decides whether to change the template or write those two by hand.

## Owner's decision
Waiting. Nothing has been sent. The agents agreeing on all other rows is not a reason to send; the owner reads the rows and the letter first.
