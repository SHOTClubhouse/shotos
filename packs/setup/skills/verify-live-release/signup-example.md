# Verify a release with a live signup action

A fictional workshop site is publishing a booking page. The release owner agreed that the anonymous page, visible booking form and successful confirmation are critical checks. The confirmation check must be evidenced in production. The verifier has approval to read the public site.

| Record | Evidence |
| --- | --- |
| V1 | The public marker serves the intended revision, and the anonymous booking page and form load. |
| V2 | The preview environment accepts a test booking. The live form creates a real booking and sends a confirmation message. The verifier has no approved live test identity or permission to submit. |
| V3 | Later, the release owner supplies the authorised live test receipt. It matches the intended revision, the booking request and the confirmation. |

> Record the release status after V1 and V2. Then update it after V3. Identify the evidence for each user path and which environment produced it.

After V1 and V2, public identity and read-only paths pass. The critical live confirmation is pending. Keep the preview result separately and route the live check to the release owner. After verifying V3, record the authorised production check and close the release verification if the other checks still apply.
