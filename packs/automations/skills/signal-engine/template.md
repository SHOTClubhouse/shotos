# Signal engine setup record

**Owner (accepts the digest):**
**Date:**

## Acceptance
- A good digest looks like:
- The engine must not: reply, forward, label, archive or delete mail; email anyone but the owner.

## Settings
- Label:
- Priorities (keyword, weight):
- AI scoring: off | on (key stored in Script Properties by the owner)
- Who can open the sheet:

## Dry run
- Date and result (messages found, items, scores plausible, nothing written or sent):

## Pilot (three messages)
- Queue rows match their source messages: yes | no
- Digest arrived once, to the owner only: yes | no
- Mail unchanged: yes | no
- Rerun created no duplicates: yes | no

## Decision
- Owner accepted the pilot: yes | no | changes needed
- Schedule installed (date, collect every N hours, digest hour):
- How to switch off: removeTriggers, then enableDryRunMode

## Recovery and handoff
- Sheet location (no keys):
- Current mode and trigger state:
- Open pending digest or errors, next owner:
- Test label or fixture used before the real label:
- If something fails: removeTriggers, enableDryRunMode, check the inbox before clearing PENDING_DIGEST

## Claims
- [unverified] anything not checked in the real account
