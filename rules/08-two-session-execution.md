# Control 8: Two-session execution

**The rule:** For high-risk actions, review and approve in one session, freeze the approved items into a manifest, and execute from that manifest in a fresh session only after a yes.

Serves rule 1, [Stop at the boundaries](../docs/controls.md). Matters most in **Operate** and **Own** when something external is about to happen.

## Why it exists

An agent at Harbourside Lettings is asked to send rent increase notices to 38 tenants. Over a long session it builds the list, drafts the notices, gets the owner's comments, changes the wording, drops two tenants and adds one. By the time the owner says "yes, go", the conversation holds five versions of the list and three versions of the text. The agent sends from the one it believes is latest. It was not.

When a session has been busy, the thing approved and the thing executed drift apart. Freezing the approved items into one file, then acting from that file in a clean session, removes the drift. The executing session knows nothing except the manifest, so it can do only what the manifest says.

## What the agent does

**Session A: review and prepare.**
1. Builds the items, drafts, targets and checks. Works with the owner until the owner is content.
2. Writes the **approval manifest**: exact items, exact targets, exact content or content references, and a checksum for each file or for the whole list.
3. Checks the manifest against the acceptance card, and shows it to the owner.
4. Stops. It does not execute.

**Owner:** reads the manifest and says "yes, execute manifest `renewals-2026-03`" or asks for changes. A change means a new manifest and a new checksum.

**Session B: execute.**
1. Starts fresh, with the manifest and the execution steps, and no memory of session A.
2. Recomputes the checksum. If it does not match the approved one, stops.
3. Executes exactly the listed items against exactly the listed targets, and nothing else.
4. Stops on the first unexpected result and reports, rather than adjusting.
5. Writes a receipt for each item and a summary, and reads back per [control 6](06-read-back.md).

## What a person does

- Reads the manifest itself, not a summary. Spot-checks at least one item end to end.
- Replies with the manifest name and the word yes. A vague approval is treated as no.
- Starts session B, or explicitly authorises it. The executor does not start itself.
- Reads the receipts and accepts the result.

## The format

The frozen approval manifest is a plain file, for example `.work/manifests/renewals-2026-03.md`:

```
manifest: renewals-2026-03
action: send email (one per row)
owner approving: Maya
prepared: session A, 2026-03-04
items:
  1. target: tenant 014 (address in contacts.csv) | content: drafts/014.txt | sha256: <hash>
  2. target: tenant 019 (address in contacts.csv) | content: drafts/019.txt | sha256: <hash>
  ...
excluded (do not send): tenant-023 (dispute), tenant-031 (notice already served)
total items: 38 | list checksum: <sha256 of this item list>
rollback or limits: none possible after send; pilot of 3 sent first and read back
approval: (blank until yes) "yes, execute manifest renewals-2026-03" by ________ at ________
```

A checksum can be produced with any standard tool; the point is that session B can recompute it.

## Sizing by risk

- **Small work:** not needed. Use [control 4](04-stop-boundaries.md) alone.
- **Normal external action** (a few messages, a single publish): a short list in the approval request, with exact targets, is enough. A manifest is optional.
- **High-risk work** (bulk sends, spend, deletes, deploys, anything on personal or children's data): the manifest and the two sessions are required, and the first run is a pilot of three or fewer under [control 9](09-pilot-before-scale.md).

## Common mistakes

- Making the manifest a description ("send the notices") instead of a list of exact items.
- Letting session B "fix" a typo it notices. It stops and returns to session A.
- Reusing an old manifest for a new batch.
- Approving verbally in a chat that session B cannot see. The approval is written in the manifest.
- Including secrets in the manifest. Reference where they live; do not paste them (see the [security guardrail](guardrails/security.md)).
- Skipping the checksum because "nothing changed".

## How to check it is working

- Every bulk or irreversible action in the last quarter has a manifest with a named approval and a matching receipt.
- Change one byte of a draft after approval and run session B. It refuses.
- Session B's logs show no tool call outside the manifest's targets.
- Receipts match the manifest item by item, with no extras.

## Related

[Control 4: stop boundaries](04-stop-boundaries.md) · [Control 9: pilot before scale](09-pilot-before-scale.md) · [Control 7: independent review](07-independent-review.md) · `evidence-handoff` skill · [rules index](README.md)
