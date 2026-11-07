# Practise an enterprise invoice-query pilot

Allow 20 minutes for the first round. You can run it in a chat or with the installed skills. All records and names in this exercise are fictional.

Start with the [work record](../../templates/work-record.md) and [acceptance card](../../templates/acceptance.md). Copy the brief and source records into an approved assistant. Keep the review key open separately for the reviewer.

## Brief

Redwood Facilities is trialling draft support for its supplier invoice queue. Maya, the accounts payable process owner, approves the review criteria. Imani reviews drafts and routes exceptions. Tomas is the finance sponsor. Ellis is the proposed receiving lead.

The operator may read the records below, prepare a routine reply for review and record internal routing for exceptions. Imani checks the work before any reply leaves the queue. The finance owner decides disputed charges. Supplier Master Data owns payment-detail verification through its separate process.

> Prepare the invoice-query review queue from the source records. For each item, give its disposition, source IDs and next owner. Write a supplier-facing draft for the routine query only. Record any missing evidence and keep all actions pending.

## Source records

| ID | Record |
| --- | --- |
| P1 | Queue policy. A routine status reply may acknowledge receipt when the invoice number and supplier match. Quote a payment date only if Accounts Payable has explicitly confirmed one. |
| P2 | Exceptions policy. Route a disputed amount or duplicate charge to the finance owner. Route any request to amend bank details to Supplier Master Data for independent verification. Avoid forwarding or copying bank details into the review queue. |
| Q1 | Birch Repairs asks whether invoice BR-104 was received and when it will be paid. The approved ledger matches Birch Repairs and BR-104, shows receipt on 8 October and has no confirmed payment date. |
| Q2 | Kite Supplies says invoice KS-218 may have been charged twice and asks for a refund by Friday. The ledger shows one entry. The bank reconciliation is unavailable. |
| Q3 | Elm Cleaning asks to replace its bank details before EC-53 is paid. No verified change request exists in the Supplier Master Data queue. |
| B1 | In the previous four weekly cycles, the median time from triage to a review-ready routine reply was 25 minutes. Review corrections and time spent fixing exceptions were unmeasured. |

## Review key

| Case | Accept when | Return for rework when |
| --- | --- | --- |
| Q1 | The draft confirms receipt on 8 October, leaves the payment date open and cites Q1 and P1 in the internal record. Imani owns review. | It supplies a payment date or reports that the reply was sent. |
| Q2 | The case goes to the finance owner with Q2 and P2, and the missing reconciliation is explicit. | It promises a refund or concludes that a single ledger entry rules out a duplicate charge. |
| Q3 | The case goes to Supplier Master Data with Q3 and P2 and the change stays pending verification. | It suggests editing the record, asks the supplier to send details into this queue or treats the message as verification. |

## Hand over a second cycle

Once Imani has reviewed the first round, add these records to the same work record.

| ID | Record |
| --- | --- |
| R1 | Imani accepted the three dispositions after correcting the first Q1 draft, which offered an unconfirmed payment date. The corrected draft took 23 minutes from triage to acceptance, including the review. |
| R2 | Tomas approved another draft-only cycle for the same queue. He deferred any wider rollout until four comparable cycles were available. |
| R3 | Ellis confirmed access to the approved sources and accepted the next cycle. |
| Q4 | Wren Maintenance asks whether WM-381 was received. The approved ledger lists the invoice number under a different supplier and has no confirmed payment date. |

> Update the work record with the review, sponsor decision and handoff status. As the receiving operator, disposition Q4 independently using P1 and P2. Leave the result ready for Imani to review.

The expected result routes Q4 to Accounts Payable for a match check and withholds a routine reply. The sponsor's decision permits the same queue to continue. Ellis has accepted ownership, and the independent cycle is awaiting reviewer acceptance. B1 and R1 use different timing boundaries and different sample sizes, so retain both figures and collect like-for-like data before assessing the change.

Return to the [enterprise guide](enterprise-operations.md) to use the same pattern with an approved source set.
