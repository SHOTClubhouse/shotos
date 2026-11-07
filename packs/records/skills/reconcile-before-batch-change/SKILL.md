---
name: reconcile-before-batch-change
description: Compares authoritative records with a target snapshot and prepares a reviewable batch change plan. Use before updating memberships, entitlements or other repeated records. Holds ambiguous matches and stale targets.
---

# Reconcile records before a batch change

**Stage:** Hypothesise. Give the owner a plan they can review against the source and target snapshots.

1. Name the source owner, target owner and reviewer. Record both snapshot versions, allowed keys and fields, and the proposed scope. Use only the fields needed to match and review.
2. Match on the agreed stable key or an approved mapping. Check key uniqueness in both datasets before proposing any change. Keep missing or duplicate keys, one-to-many matches, and conflicting mappings in a separate exception queue. Give each exception an owner and the evidence needed to resolve it.
3. For each unique match, compare the proposed value with the target. Mark identical values as unchanged. Hold a row if the current target differs from the expected prior value. For eligible changes, record the exact target ID, expected prior value, proposed value and evidence. Count every input row once.
4. Prepare the [review sheet](template.md). Name what approval covers, how the operator will confirm the target is still current, and what will halt the batch. Include the prior values or backup reference, the recovery owner and the checks that show whether an approved change landed.
5. Hand the reviewed plan to the authorised operator. For execution, use `pilot-before-scale` when available. Recheck the target revision or expected prior values immediately before writing. Hold drifted rows and ask the reviewer to approve an updated plan. Read back the affected rows before recording completion. This skill prepares the plan without writing to the target.

Keep ambiguous or unauthorised changes in the exception queue, with their next owner.
