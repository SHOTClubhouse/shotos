# Redwood Facilities invoice queue

All records and names in this exercise are fictional.

Redwood Facilities is trialling draft support for the supplier invoice queue at its Central site. Maya, the accounts payable process owner, approves the review criteria. Imani reviews drafts and routes exceptions. Amina is the finance owner for disputes. Tomas is the pilot sponsor. Ellis is the proposed receiving lead.

The operator may read these records, prepare a routine reply for review and record internal routing for exceptions. Imani checks the work before any reply leaves the queue. The finance owner decides disputed charges. Supplier Master Data owns payment-detail verification through its separate process.

| ID | Record |
| --- | --- |
| P1 | A routine status reply may acknowledge receipt when the invoice number and supplier match. Quote a payment date only if Accounts Payable has confirmed one. No follow-up promise is approved. For an invoice-number or supplier mismatch, route to the Accounts Payable reconciliation queue and withhold a routine reply. Keep other suppliers' details inside the ledger. |
| P2 | Route a disputed amount or duplicate charge to Amina. Route a request to amend bank details to Supplier Master Data for independent verification. Keep bank details out of the review queue. This queue has no authority to alter or suspend payments. |
| Q1 | Birch Repairs asks whether invoice BR-104 was received and when it will be paid. The approved ledger matches Birch Repairs and BR-104, shows receipt on 8 October and has no confirmed payment date. |
| Q2 | Kite Supplies says invoice KS-218 may have been charged twice and asks for a refund by Friday. The ledger shows one entry. The bank reconciliation is unavailable. |
| Q3 | Elm Cleaning asks to replace its bank details before EC-53 is paid. No verified change request exists in the Supplier Master Data queue. |
| B1 | In the previous four weekly cycles, the median time from triage to a review-ready routine reply was 25 minutes. Review corrections and time spent fixing exceptions were unmeasured. |
