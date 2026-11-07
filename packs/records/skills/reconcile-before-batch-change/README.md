# Reconcile Records Before a Batch Change

Use this Hypothesise skill before changing memberships, permissions or other repeated records. It gives the source owner, target owner and operator the same reviewable plan, with stable IDs, prior values, proposed values and held exceptions.

Use the [review sheet](template.md) to bind approval to the intended rows. After a failure, compare the current target with the exact approved plan and the earlier receipts before drafting a retry. A value that happens to match is evidence of the current state. Record the action as verified only when there is a corresponding receipt.

## Try it

Use the fictional [membership input](../../examples/reconcile-before-batch-change/input.md) and compare your plan with the [worked output](../../examples/reconcile-before-batch-change/output.md). Then use the [interrupted batch exercise](retry-example.md) to separate verified writes, drift, uncertain matches and work still pending.

**Needs:** Authoritative source and target snapshots, agreed match keys and scope, and the named target owner. Retry review also needs the approved revision and any execution receipts.

**Evidence:** Example only for the interrupted-batch workflow. The practice records are fictional and leave the target unchanged.
