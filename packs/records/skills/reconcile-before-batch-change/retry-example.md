# Review an interrupted membership batch

All records are fictional. The target owner approved plan P7 for four rows as one batch. Each row was approved to move from Basic to Club. An operator's session ended during execution.

| Row | Current read-back | Receipt from the interrupted run |
| --- | --- | --- |
| M101 | Club | W1 names M101 and plan P7. It records Basic to Club. |
| M102 | Club | No receipt. A staff member might have changed the record separately. |
| M103 | Sponsor | No receipt. The approved prior value was Basic. |
| M104 | Basic | No receipt. |

> Prepare the recovery review. Identify what was verified, what is already matching, what drifted and what remains pending. Keep the target unchanged.

## Review key

| Row | Disposition |
| --- | --- |
| M101 | Verified applied. W1 and the current read-back agree. Keep it out of a retry. |
| M102 | Observed matching. The current value is Club and the origin is unverified. |
| M103 | Drifted. Record Sponsor and refer the change to the target owner. |
| M104 | Pending. Basic still matches the approved prior value. P7 does not authorise a separate retry for this row. |

Report one verified, one matching without attribution, one drifted and one pending. The target owner reviews the partial result and decides whether to approve a revised plan. The recovery reviewer leaves all four records untouched.
