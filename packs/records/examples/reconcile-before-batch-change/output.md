# Fictional membership review

| Source | Target | Outcome | Next action |
| --- | --- | --- | --- |
| S1 | T1 | Propose Basic to Club | Target owner reviews this exact change |
| S2 | T2 | Unchanged | Current and requested values both read Basic |
| S3 | T3 and T4 | Hold, duplicate target key | Target owner resolves M103 |
| S4 | None | Hold, missing target | Source owner confirms the ID and route |
| S5 | T5 | Hold, current value differs from expected prior value | Target owner resolves Sponsor versus Basic |

Five input rows yielded one proposed change, one unchanged and three held. No target write was made. The reviewer can approve S1 alone. Immediately before an authorised change, confirm T1 still reads Basic and that M101 is still unique. If either check fails, hold the row and notify the target owner. If applied, read back T1 as Club, record the result, and retain the prior Basic value with the authorised recovery instructions.
