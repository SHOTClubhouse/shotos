---
name: reconcile-before-batch-change
description: Compares authoritative records with a target snapshot and prepares a reviewable batch change plan. Use before updating memberships, entitlements or other repeated records. Holds ambiguous matches and stale targets.
---

# Reconcile records before a batch change

**Stage:** Hypothesise. **Rules:** 1 Stop at the boundaries, 2 Agree acceptance first, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Use the authoritative source, the current target and the exact approved plan if work already started. Route execution to the authorised operator. Use `pilot-before-scale` for an initial bounded run and `report-with-evidence` for completion.

## Steps

1. Name the source owner, target owner and reviewer. Record both snapshot versions, allowed keys and fields, and the proposed scope. Use only the fields needed to match and review.
2. Match on the agreed stable key or an approved mapping. Check key uniqueness in both datasets before proposing any change. Keep missing or duplicate keys, one-to-many matches, and conflicting mappings in a separate exception queue. Give each exception an owner and the evidence needed to resolve it.
3. For each unique match, compare the proposed value with the target. Mark identical values as unchanged. Hold a row if the current target differs from the expected prior value. For eligible changes, record the exact target ID, expected prior value, proposed value and evidence. Count every input row once.
4. Prepare the [review sheet](template.md). Bind approval to the plan revision, row IDs, expected prior values and intended values. Record whether approval covers the entire batch together or permits named rows to proceed independently. Use the whole batch as the approval scope if no narrower scope was agreed.
5. Give the operator the preflight, read-back and recovery checks. Before an authorised write, compare the latest target with the approved prior values. A mismatch holds the affected approval scope. Prepare a revised plan for approval or use the independently approved subset if the record permits it.
6. On a retry, read the current target and any execution receipts before planning more work. Mark a row verified applied only if the receipt and read-back agree. An already matching value without a receipt stays observed with origin unverified. Keep unchanged, drifted and ambiguous rows out of the retry plan. See the [interrupted batch exercise](retry-example.md).

## Output and checks

Produce the review and exception queue with exact counts and next owners. Save the sheet, receipts and read-back in the owning task folder and name its path in the handoff. Leave the target unchanged. Work on a fixture or copy of the target until the owner approves a live run; never put real credentials or full personal records in the sheet. An execution report needs per-row read-back and a record of any partial or unresolved result.
