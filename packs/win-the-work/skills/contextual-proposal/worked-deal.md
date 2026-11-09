# From a club proposal to an accepted handoff

All names, dates, terms and receipts in this example are fictional. Read the [club proposal template](organisation-templates.md#independent-club) to see the structure used below.

Start with “Draft a proposal for North Quay Community Club for our attendance service.” Use the account name to find NQC-014. The discovery note gives you the buyer's goal and starting numbers. The offer record gives you the approved scope and terms. If you only have the discovery note, draft the buyer's need and leave the offer terms for approval.

Once the proposal is saved, “Prepare the North Quay handoff” is enough to start from the same deal record. Use the accepted revision if there is one. While buyer acceptance is pending, prepare the brief with the proposal marked as a draft and leave ownership with the current lead.

## Deal record NQC-014

This record stays with the account. Sales adds the proposal and approval evidence. Customer success uses the same record, then adds the handoff status and receipt.

| ID | Record |
| --- | --- |
| E1 | 2 November discovery note. North Quay Community Club's programme lead, Morgan Ellis, asked for a simpler way to record attendance for one Saturday group. In the prior four weeks, 2 of 4 registers were complete by Monday. |
| E2 | 3 November approval by Jordan Vale, supplier account owner. Jordan authorised P2 for dispatch. P2 offers four Saturday sessions from 14 November, one staff setup session before the first session and a review on 9 December for £480. The club continues to own its register and controls access. |
| E3 | 4 November dispatch receipt. Jordan sent authorised proposal P2 to Casey Doyle, the club treasurer and named budget approver. |
| E4 | 5 November buyer reply. Casey accepted P2 at £480 in writing. Morgan will confirm the club's register lead before setup. |
| E5 | 6 November handoff offer and dispatch receipt. Jordan authorised and shared brief H1 with Robin Hale, the proposed customer success lead, via the account record. Robin was given access to P2 and E1–E4. |
| E6 | 6 November receiving lead reply. Robin accepted H1, confirmed the scope, capacity and access, and agreed to contact Morgan on 9 November to confirm the register lead and book setup. |

## Where the files live

All three sit with NQC-014 in the account record, so the next person finds them from the account name alone.

| File | Holds | Who can edit |
| --- | --- | --- |
| P2, editable proposal document | The buyer copy below, with its revision label. | Jordan, as proposal owner. |
| W2, private working sheet | The ledger, asset register and status below. Never shared with the buyer. | Jordan and the supplier reviewer. |
| H1, handoff brief and acceptance record | The customer success handoff below. | Jordan until offered, then the receiving lead for the acceptance fields. |

A change to P2 after E4 gets a new revision (P3) and a new approval. It does not overwrite P2. Reply to the buyer about the change with `email-reply`, and keep the accepted P2 as the controlling revision until the buyer accepts P3.

## Working sheet W2 for proposal P2

Private to the supplier. The buyer copy uses only the approved rows.

| # | Claim, need or commitment | Source and approval | Status | Action or owner |
| --- | --- | --- | --- | --- |
| 1 | 2 of the last 4 registers were complete by Monday. | E1, stated by Morgan Ellis. Not observed in the register. | Buyer need, reported by the club | Say "according to the programme lead's discovery note". Do not present it as measured. |
| 2 | Four Saturday sessions from 14 November, one staff setup session, review on 9 December, £480, club owns the register and access. | E2, approved by Jordan Vale. | Approved offer | Retain. |
| 3 | The pilot will raise the number of registers complete by Monday. | No source and no approval. | Decision needed | Omit. P2 compares results with the baseline at the review and promises no improvement. |
| 4 | Supplier statements on data protection, safeguarding or storage of the register. | None. The record does not say who the register lists. | Decision needed | Omit. Ask Jordan to approve wording before any such sentence appears. P2 says only that the club owns the register and controls access. |
| 5 | Extra reporting, further sessions or support beyond setup. | None. | Not offered | Omit. |

**Asset register.** P2 uses no logo, photograph, quote or chart. Nothing is shown with unknown rights.

**Status.** Draft review and approval of P2: E2. Dispatch: E3. Buyer response: E4. Nothing in W2 is a commitment the buyer has seen.

## What the buyer sees in proposal P2

**Club priority.** Make the Saturday attendance register easier for the club to complete. Two of the last four registers were complete by Monday, according to the programme lead's discovery note.

**Pilot.** Cover one Saturday group across four sessions from 14 November. The supplier provides one staff setup session. The club owns the register and controls who can access it.

**Fee and review.** The fee is £480. At the 9 December review, compare the number of registers complete by Monday with the baseline of 2 out of 4.

**Decision requested.** Casey Doyle to accept P2 in writing. Morgan Ellis to confirm the club's register lead before setup.

## Delivery handoff on NQC-014

| Field | Entry |
| --- | --- |
| Current deal owner | Jordan Vale. |
| Accepted revision | P2, accepted by Casey Doyle on 5 November (E4). E2 authorises the offer and E3 records dispatch. |
| Agreed commitments | Supplier setup before the first session on 14 November. Four Saturday sessions for one group, £480 total. Club owns the register and access. Review on 9 December (E2, E4). |
| Open decision | Morgan Ellis to confirm the register lead before setup (E4). |
| Proposed receiving lead and first action | Robin Hale to contact Morgan on 9 November to confirm the lead and book setup. Share the commercial records and discovery note via the account record (E5, E6). |
| Customer success record | [H1](#customer-success-handoff-h1), accepted by Robin on 6 November (E6). |

## Customer success handoff H1

**Source record.** NQC-014, accepted proposal P2 (E4). Robin can read E1–E5 via the account record. Access to the club's attendance register remains with the club.

**Account stage.** Pre-start. The club accepted the offer and the first session is due on 14 November (E2, E4).

**Account health.** Unknown. The record has a baseline for register completion and no delivery observations yet.

**Transfer status.** Accepted on 6 November. Jordan offered H1 with a dispatch receipt (E5). Robin accepted H1 in writing, confirmed scope, capacity and permitted access, and dated the first action (E6). Robin owns that action. The system of record still shows Jordan as account owner until the ownership update is recorded.

**Next actions.** On 9 November, Robin contacts Morgan to confirm the register lead and book setup. Robin then records the setup date before the first session and schedules the 9 December review. Confirm the register lead before setup.

**Completion evidence still due.** Record the customer notification, the ownership update in the system of record and completion of the first action before moving the transfer to Completed.

## What each normal entry point returns on this record

| Prompt | Right result from NQC-014 |
| --- | --- |
| "Draft a proposal for North Quay Community Club for our attendance service." | Before P2 is drafted: a buyer draft from E1, W2 with rows 3 to 5 held back, and no sender named beyond Jordan's approval. Once P2 is accepted (E4): do not redraft. Report P2 as the accepted revision and route any change to a new revision. |
| "Prepare the North Quay handoff." | Before E5: H1 as Prepared, with proposed receiver Robin Hale, the account with Jordan, and the commitments from E2 and E4. After E6: report H1 as Accepted, not Completed, and list the three completion receipts still due. Do not offer or accept it again. |
| "What is the status of North Quay?" | Read the Delivery handoff table, quote the transfer status from the acceptance fields and name Robin's 9 November action as the next step. |
