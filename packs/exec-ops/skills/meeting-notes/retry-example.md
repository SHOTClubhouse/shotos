# Retry an incomplete meeting-notes batch

This example uses fictional recording IDs and notes.

## First attempt

The ledger is complete through 09:00 UTC. The owner authorises processing through 11:00 UTC. The source lists M17 and M18 at the same start time. Both are in scope.

M17 has a transcript and verified note and rolling entry. Record M17 as processed. M18 has a transcript, but writing its rolling entry failed after the per-meeting note was saved. Record M18 as pending and retain 09:00 UTC as the completed checkpoint.

## Retry

Start from 09:00 UTC and match both IDs. Leave M17's verified entry intact. Open M18's saved note, verify its source and reconcile the rolling entry under M18. Read both outputs back, then record M18 as processed. If the source listing through 11:00 UTC is complete, save and read back 11:00 UTC as the completed checkpoint.

If a page still fails or another recording remains pending, keep the earlier checkpoint and name the gap. The operator should be able to find exactly one entry per recording ID.

## A source is corrected later

The approved source supplies revision 2 of M17. The original note assigned the review to Sam. The corrected speaker map and timestamped transcript attribute the commitment to Alex.

Open M17's existing note and rolling entry. Record the correction and revision 2 in the same entry. If the action was already assigned elsewhere, flag the change to the owner and keep that external update pending their authority. Read back the corrected note and ledger. M17 keeps one row with the checked revision.

A 90-second recording the owner flags as the decision confirmation stays in scope, even when the usual filter skips recordings under three minutes.
