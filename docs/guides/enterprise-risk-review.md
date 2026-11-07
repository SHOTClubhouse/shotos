# Review one AI-assisted workflow

Use this at a pilot decision when an operations lead, risk owner and receiving team need to see what the workflow can do, what may go wrong and who can stop it. Start with the organisation's existing risk register or review record. Link the work and evidence from there.

The table is a SHOTos interpretation of the four functions in NIST AI RMF 1.0. Use it to assemble evidence for the organisation's own review. The organisation's risk owner decides which controls and approvals apply. [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) · [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

| Risk review question | Records to inspect | Evidence from the fictional invoice pilot |
| --- | --- | --- |
| **Govern. Who owns the workflow and its boundaries?** | The [programme record](../../templates/programme.md) for the sponsor and decision, and the [mode contract](../../rules/03-mode-contract.md) for what the operator can do. | Maya owns the process. Imani reviews drafts. Tomas decides on expansion. Supplier Master Data verifies payment-detail changes. The pilot prepares drafts and internal routing. |
| **Map. What data, people and systems are affected?** | A [task data access card](../../templates/data-access.md) for allowed sources, fields, runtime and destination. Record what changes when the workflow moves to another site. | The agent works from the approved invoice ledger and queue policy. A supplier mismatch goes to Accounts Payable. Bank details stay in the approved system. East Yard has a different policy. |
| **Measure. What shows the workflow is fit for this use?** | The [acceptance card](../../templates/acceptance.md), [evidence pack](../../skills/evidence-pack/README.md) and [accepted-work ledger](../../templates/accepted-work-ledger.csv). Check ordinary cases and exceptions with a reviewer. | Check that a draft confirms receipt without promising a date, disputes go to the finance owner and payment-change requests follow the verification route. Keep time-to-draft and time-to-acceptance separate. |
| **Manage. What happens if a check fails or the work expands?** | The [runbook](../../skills/runbook/README.md), [enablement plan](../../skills/enablement-plan/README.md) and [rollout plan](../../skills/rollout-plan/README.md). Record the stop, recovery owner and evidence for restarting. | Pause the affected work on a policy or data boundary failure. Ellis completes an independent cycle. East Yard needs a local baseline, policy and reviewer before starting. |

## Put the decision in the existing record

1. Name the exact workflow, site, data scope, approved runtime and version of the pilot record.
2. Give each material risk an owner, the check that would expose it and the action to take if it fails. Link the existing policy and approved destination.
3. Record the reviewer's result and any missing evidence. The sponsor records continue, change, hold or stop, with conditions and the next review date.
4. Reopen the review if the data, tool, intended use or receiving team changes. Carry forward the evidence that still applies.

Follow the [four-round invoice exercise](invoice-query-exercise.md) to practise the review with fictional records. For a real pilot, keep approved evidence in its existing system and pass the review by reference.
