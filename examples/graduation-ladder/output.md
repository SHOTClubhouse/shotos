# Graduation standing: two task classes

Read from the status output Dominic supplied. I have not run the tool myself in this answer; please re-run `python .shotos/tools/graduation_log.py status` before you record a decision.

## Class 1: weekly-arrears-summary

**Owner (reviews outputs):** Dominic Hale
**Risk:** standard (a figure goes to the directors; it does not leave the company). Confirm that you agree it is not high-risk.
**Date of standing:** as of the supplied status

### From the log
| Accepted unedited | Accepted edited | Rejected | Total | Unedited rate | Current rung |
|---|---|---|---|---|---|
| 52 | 1 | 1 | 54 | 96.3% | 1 |

### Against the bar
Rung 2 needs at least 95 per cent unedited over at least 50 samples. 96.3 per cent over 54 passes both parts. Rung 3 is not near: it needs 98 per cent over 200.

### What the edits and rejections were
One typo edit. One rejection where the export was cut off and the total was too low, caught by comparing with the ledger. The rejection matters more than the rate: the agent produced a plausible wrong total, and the only defence was your check.

### Recommendation
Promote to rung 2, run automatically and notify, with a condition: the Monday run compares its total with the ledger report before it produces the summary, and flags a mismatch as an exception instead of drafting. Without that check, rung 2 would remove the only thing that caught the cut-off export. The rung 2 run may produce and save the summary and notify you; it does not email the directors. Sending from your account is outside the project and stays behind your yes unless you grant a standing permission for exactly that email and recipients.

### Decision (named person)
Decision:
Decided by (name, role):
Date:

### If rung 2 is granted
Exceptions that trigger a notice: ledger mismatch, a smaller row count than the previous week, or an empty section. Who is notified: Dominic Hale, straight away. Return to rung 1 at once if any exception reaches the directors, or if the unedited rate over the latest 20 outputs falls below 95 per cent.

### Next review
End of next quarter. Restart the count after any change to the export, the skill or the model.

## Class 2: landlord-dispute-letter

**Risk:** high-risk (it leaves the company, may affect legal rights, and one rejection quoted a clause that does not exist).

### From the log
| Accepted unedited | Accepted edited | Rejected | Total | Unedited rate | Current rung |
|---|---|---|---|---|---|
| 12 | 6 | 1 | 19 | 63.2% | 1 |

### Against the bar
63.2 per cent over 19 is below the rung 2 bar of 95 per cent over 50 on both rate and sample size. The class is also high-risk, so it stays at rung 1 unless a named person explicitly promotes it, with the reason written down. A good rate would not change that.

### Recommendation
Stay at rung 1. Letters stay as drafts. The agent does not send them to landlords. A fabricated clause is a material factual failure, and it is the kind of failure that rate alone hides. Consider a gate on the letter skill: see [skill-quality-gate](../../skills/skill-quality-gate/README.md).

### Decision (named person)
Decision:
Decided by (name, role):
Date:
For a high-risk class: explicit promotion reason (none recommended):

### Next review
After 50 reviewed letters or a change to the skill.
