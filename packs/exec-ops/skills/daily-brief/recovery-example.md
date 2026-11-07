# Recover a partial daily brief

This example uses fictional sources. Try it with the skill and templates from this folder.

## First attempt

The ledger is complete through Monday at 18:00 UTC. It already contains one insurance renewal row from broker thread B17. Tuesday's brief has an 08:00 UTC cutoff. Mail is available and B17 confirms the deadline moved to Thursday. The calendar returned a first page and then timed out.

The brief records the verified Thursday deadline on the existing renewal row. It says calendar coverage is partial and leaves any broker reply in the digest. The ledger's completed coverage stays at Monday 18:00 UTC.

## Retry

At 08:20 UTC, both sources are available. The operator reads from Monday 18:00 UTC through the new cutoff and checks today's current appointments. The window includes B17 again and a calendar change made at 07:40 UTC moving the renewal review to 11:00.

The operator matches B17 to the same renewal row and records the calendar change. After verifying the saved ledger, the operator sets completed coverage to Tuesday 08:20 UTC and reads it back. The digest has one renewal item and shows the 11:00 review.
