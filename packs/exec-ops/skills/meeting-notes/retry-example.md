# Retry an incomplete meeting-notes batch

This example uses fictional recording IDs and notes.

## First attempt

The ledger is complete through 09:00 UTC. The owner authorises processing through 11:00 UTC. The source lists M17 and M18 at the same start time. Both are in scope.

M17 has a transcript and verified note and rolling entry. Record M17 as processed. M18 has a transcript, but writing its rolling entry failed after the per-meeting note was saved. Record M18 as pending and retain 09:00 UTC as the completed checkpoint.

## Retry

Start from 09:00 UTC and match both IDs. Leave M17's verified entry intact. Open M18's saved note, verify its source and reconcile the rolling entry under M18. Read both outputs back, then record M18 as processed. If the source listing through 11:00 UTC is complete, save and read back 11:00 UTC as the completed checkpoint.

If a page still fails or another recording remains pending, keep the earlier checkpoint and name the gap. The operator should be able to find exactly one entry per recording ID.
