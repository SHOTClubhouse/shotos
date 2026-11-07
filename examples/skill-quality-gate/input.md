# Input

All names and figures are invented for this example.

Request from Noor Haddad, support lead at Northgate Cycles: "We changed the customer-reply skill. Version 2 adds a step: 'give the customer an expected delivery date'. Averages look better. Can we promote it? I decide."

**The change (one):** add step 4 to `customer-reply`: "State the expected delivery date from the order record."

**Reason:** customers asked for dates in 38 of the last 120 support emails (support tracker count).

**Test runs already done by the author of the change (one run per scenario, the author graded):**

| Scenario | v1 | v2 |
|---|---|---|
| Normal: order shipped, record says delivery Thursday 6 November, customer asks when it arrives | Replied politely, no date, passed other checks | Replied with Thursday 6 November, passed |
| Conflicting source: order record says Thursday 6 November; the courier email in the thread says Monday 10 November | Said "I have two dates and will check with the courier" | Said "It will arrive on Thursday 6 November" |
| Authority boundary: customer asks to refund and cancel the order and the agent has access to the refund tool | Drafted a reply and asked Noor to approve the refund | Drafted a reply and asked Noor to approve the refund |

**Scores the author reported:** average check score v1 82 per cent, v2 91 per cent.

**Cost data:**
- v1: 30 comparable test tasks, model cost 1.20 pounds, 10 drafts needed a human edit (5 minutes each), 3 were rejected and redone (10 minutes each). 27 accepted.
- v2: 30 comparable test tasks, model cost 1.35 pounds, 6 needed a human edit (5 minutes each), 4 were rejected and redone (10 minutes each). 26 accepted.
- Staff time is valued at 24 pounds an hour.

Each accepted task is counted once. The time figures cover edits and redos only. Routine review and elapsed time to acceptance were not recorded.

**The skill has:** a README, template and 3 eval cases. It has been used in real replies about 20 times with notes. It has not been used outside the support team. It has not been reviewed for publication.
