# Input

All data below is invented for this example.

Request from the owner of Northgate Cycles: "Are we shipping faster or just breaking more? I want a straight view for the booking tool, last ten weeks (1 September to 9 November). Include the AI summary feature that writes the weekly workshop schedule."

**Git and deploy log (production deploys, from the release log):** 31 deploys in ten weeks. Per week: 2, 3, 3, 4, 3, 3, 4, 3, 3, 3 (sums to 31).

**Lead time sample (first commit to live), 12 changes picked from the log, in hours:** 6, 9, 11, 14, 20, 22, 26, 30, 48, 52, 75, 140.

**Failed deploys (needed a hotfix, rollback or revert within 24 hours):** 4 of 31. Reasons in the notes: wrong date format in an email (hotfix), calendar sync timeout (rollback), missing mobile layout fix (hotfix), a config value left from testing (rollback).

**Incident notes:**
- 14 Sep, double bookings for 25 minutes: detected 16:05, restored 16:30.
- 3 Oct, calendar sync down: detected 09:10, restored 11:40.
- 28 Oct, wrong-date emails sent to 12 customers: detected 13:00, restored 13:50.

**AI summary feature (weekly schedule drafts):**
- Eval run on 6 November: 38 of 40 cases passed.
- Provider usage export: 62 pounds in total for the ten weeks. Staff note: 70 drafts were produced; 49 were accepted without edits, 15 accepted after edits, 6 rejected and redone by hand.
- Latency from logs: median 4.1 seconds, 95th percentile 11.8 seconds.
- Staff time reviewing is not logged.

The owner adds: "I was thinking of putting a target of five deploys a week on the whiteboard."
