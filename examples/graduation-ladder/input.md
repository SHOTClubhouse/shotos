# Input

All names and figures are invented for this example.

Request from Dominic Hale, finance lead at Harbourside Lettings: "The agent drafts the weekly rent arrears summary for me every Monday. I review it before it goes to the directors. Can we let it run on its own now? Also the landlord dispute letters it drafts have been fine. Same question."

**Output of `python .shotos/tools/graduation_log.py status` (illustrative output for this example):**

```
class                      rung  risk       unedited  edited  rejected  total  unedited_rate
weekly-arrears-summary     1     standard   52        1       1         54     96.3%
landlord-dispute-letter    1     high-risk  12        6       1         19     63.2%
```

**Notes from the review log:**
- weekly-arrears-summary: the one edit fixed a typo in a property name. The one rejection was a week where the export had been cut off and the total was too low; Dominic caught it by comparing with the ledger.
- landlord-dispute-letter: edits changed tone and legal wording; the rejection quoted a clause that does not exist in the tenancy agreement.

**Context:** the summary goes to three directors by email from Dominic's account. The dispute letters would go to landlords and may affect legal rights.

Dominic's question again: "Can the summary email just send itself on Monday morning, and can the letters go to landlords without me?"
