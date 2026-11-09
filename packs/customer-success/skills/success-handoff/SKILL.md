---
name: success-handoff
description: Finds the existing account or deal and prepares a sourced customer handoff with next actions and an acceptance record. Use when someone else needs to take over a customer account or a proposal is moving into delivery.
---

# Success handoff

Make a handoff that the receiver can act on and that cannot be mistaken for done until they have accepted it.

Stage: Own. Rules: 1 Stop at the boundaries, 4 Claim only what you can show.

## Context and handoff

Start from the account name or proposal reference. Find the permitted account record and follow its existing source links for commitments, last interaction and access restrictions. If more than one account or proposal matches and the choice changes the handoff, ask which one. An existing account record is enough to start. Use the available evidence to prepare a brief and record any missing information or access.

If the record already holds a brief or acceptance record for this account, continue that revision. Report its transfer status and the evidence still due, and do not offer or accept it again. If no proposal exists yet, route to `contextual-proposal`. If terms changed after acceptance, route the buyer reply to `email-reply` and carry the new revision as proposed until it is approved. Use the existing **Delivery handoff** section as the shared record. Verify the accepted revision or controlling agreement and each commitment against the cited evidence. When only a draft is available, carry its revision and proposed scope, record acceptance as pending and keep the account with its current owner. Resolve discrepancies using the latest authoritative agreement or observed account activity. Open mail or notes only to resolve a specific gap. Carry unresolved conflicts, access gaps and missing approvals into the brief with the person who can resolve them, or record that this person still needs to be named.

Use `enablement-plan` if the receiving team must prove an independent cycle. Keep acknowledgement and first action with the account.

## When not to use this

Use `onboarding-recovery` when onboarding has stalled and the current owner needs to restart it. Use this skill when responsibility needs to move. Draft a brief while a receiver is being confirmed. A live transfer needs the current owner's authority and the receiver's acceptance.

## Steps

1. **Name the account, the giver and the receiver.** Record the giver from the account record. Use the proposed receiver's name if known, otherwise record the role or leave it unassigned. A prepared brief can have an unassigned receiver. Offering or accepting a transfer requires a named person.
2. **Gather the facts, with sources.** Record each promise, contact role, delivery result and open issue once with its source and date. For an open issue, distinguish when it was raised from its agreed due date. Call it overdue only when the evidence gives a deadline that has passed. Keep dates in the form supplied until the year or calendar context is known. Open mail, notes or transcripts to close specific gaps. Link restricted records and include contact details only when the receiver needs them and is permitted to see them.
3. **Keep three fields separate** and never merge them:
   - **Lifecycle stage:** where the account is in its relationship (for example: pre-start, onboarding, live, renewal due). Based on what has happened.
   - **Health:** how it is going (healthy, at risk, unknown), with the evidence for the rating. If there is no evidence, write "unknown".
   - **Transfer status:** Prepared, Offered, Accepted or Completed (see below).
4. **Mark each fact** as stated by the customer, observed in a system, or inferred. Inferences are listed as hypotheses with what would confirm them.
5. **Write the brief** using [template.md](template.md): the account, what was promised, contacts, history, lifecycle stage, health with evidence, open issues, risks, the first three actions for the receiver and what is not known.
6. **Set the transfer status honestly.**
   - **Prepared:** the brief exists.
   - **Offered:** there is a dispatch receipt or a read-back of the authorised offer to the named receiver. If the giver reports dispatch and the evidence is unavailable, keep Prepared and record the report as unverified. The status stays Offered while acknowledgement is pending.
   - **Accepted:** the named receiver agreed to the offered revision in writing, confirmed scope, capacity and permitted access, and dated their first action. Keep Offered if their reply depends on an unresolved condition for taking on the work.
   - **Completed:** the customer has been told, ownership is changed in the system of record and the first action has been taken.
   Only the receiver can accept. The agent records the evidence and leaves the status decision to the authorised people. Confirm who can authorise dispatch, grant access and approve any rollout separately. Route missing authority to the relationship owner to identify the right decision maker. Their role alone does not give them dispatch, access or rollout authority. When the handoff is part of Own in a programme, acceptance of the brief and completion of an independent cycle have separate evidence.
7. **Name who owns each action during the transfer.** Read back the owner of record. Keep each open action with that owner unless the receiver or a named interim owner accepts responsibility for it. An accepted brief can precede the ownership update. Draft a customer introduction when useful and hold it until Accepted and authorised for dispatch.
8. **Read back.** Check every fact against its source, and check that no field is merged or marked beyond what the evidence shows.

## Output

The handoff brief and the acceptance record, both from the template. Save with the account's records.

## Checks

- Lifecycle stage, health and transfer status are separate fields.
- Every fact has a source; inferences are labelled.
- Health states its evidence or "unknown".
- Transfer status follows the evidence. Accepted points to the receiver's written confirmation of the offered revision. Completed points to the notification, ownership update and first action.
- No message to the customer was sent.
