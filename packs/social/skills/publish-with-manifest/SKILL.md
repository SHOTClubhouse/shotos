---
name: publish-with-manifest
description: Publishes social posts only through a frozen approval manifest approved by a named person, then reads each post back live. Use when approved captions and assets are ready to go out. Never publishes unapproved or changed items.
---

# Publish only what was approved, exactly as approved

Stage: Operate. Rules served: 1 Stop at the boundaries, 3 Read back the real result. Control 8, two-session execution: review and execution happen apart, joined by a frozen manifest. See `rules/08-two-session-execution.md` (in the SHOTos repository, or `.shotos/rules/08-two-session-execution.md` where SHOTos is installed).

## Context and handoff

Read the approved copy and assets, destination, time, owner and rollback plan. Freeze a per-item record before any action.

Use `public-exposure-check` for sensitive surfaces. Store the manifest and observed receipts together.

## When not to use this

- The captions are still being chosen. Use `caption-options` first.
- Nobody with authority will approve. Without an approver there is nothing to freeze.
- The person wants to publish "whatever looks good" in one go. This skill exists to prevent exactly that.

## Part 1: Prepare and freeze (review session)

1. **Gather the items.** For each post: an ID, the account and platform, the exact publish time with time zone, the final caption text, the asset file name, the alt text, link and any tags or locations. Check each asset's size, ratio and length against the platform's current specification for that format, and record who may authorise publishing on that account.
2. **Check consent and claims.** Any post showing or naming a child needs recorded parental or guardian consent covering this use; remove the item if not confirmed. Check the caption against the facts list from `caption-options`; the claims must still be true on the publish day.
3. **Compute checksums.** For every asset, compute a SHA-256 checksum from the exact file to be uploaded (for example `sha256sum file` or `Get-FileHash file -Algorithm SHA256`). Record it beside the file name. For the caption text, record a checksum too, so a changed comma is detectable.
4. **Write the manifest** with [template.md](template.md): one row per item with every field above, an approval column, and a manifest checksum covering the whole table.
5. **Ask a named person to approve.** The approver must hold authority over the account and the content; if they do not, ask who does. Show them the exact posts as they will appear. They approve per item (yes, no, change), with name and date. Anything not approved is excluded. Mark the manifest frozen. Any later edit means a new manifest and a new approval.

## Part 2: Execute (fresh step)

6. **Start fresh.** A new session or a person with only the manifest and the files, not the conversation that wrote the captions. Verify the manifest checksum and every asset checksum. If anything differs, stop and report; do not fix it silently.
7. **Check the gate.** Only items marked approved are eligible. Confirm the time has not passed, the account is the right one and the platform tool is reachable. If the agent has no publishing connector, it gives the person a checklist and the person posts each item.
8. **Publish one item at a time.** No extras, no reordering, no "while I'm here" posts. If an item fails, record the failure and stop that item; do not retry blindly or post a variant.
9. **Read back each post live.** Open the live post. Check the account, the text matches the approved caption exactly, the right image is attached (compare it visibly and, where possible, by downloading and hashing), the alt text, the link and the time. Record the post URL and what you checked.
10. **Write the receipt.** For each item: published, failed or skipped, with URL, time and read-back result. Separate "published" from "read back and matches". Report anything that does not match and leave removal or editing to the owner.

## Output

A frozen manifest from [template.md](template.md) and a receipt with one line per item. Keep both with the project.

## Checks

- Each published item appears in the manifest, approved, unchanged since approval.
- Checksums were verified before publishing.
- Every post was read back live and the result recorded.
- Items with children have recorded consent.
- Approval came from a person with authority over the account.
- Each asset was checked against its platform's format.
- The agent published nothing outside the manifest.
