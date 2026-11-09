---
name: verify-live-release
description: Verifies that an authorised website, document or download release is publicly available at the intended revision and that key user actions work. Use after a merge, deploy, publish or upload.
---

# Verify a live release

**Stage:** Track. **Rules:** 1 Stop at the boundaries, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Start with the owner's release record and the intended audience. For a website, reuse the visitor checks from `build-small-website` or `campaign-website`. A deployment job, the release listing or a preview can supply context. The proof comes from the destination the audience uses.

## Trigger and minimum inputs

Run it after an authorised merge, deploy, publish or upload, or when someone says a release is live. It needs the destination URL or location, the intended revision signal, the audience and the critical paths. With no revision signal, the identity check is unverified; say so and do not mark the release verified. Any runtime with a browser, fetch tool or file access can run it.

## Steps

1. Read the release record for the destination, intended revision, authorised scope and critical user paths. Choose a revision signal the intended audience can observe at that destination, such as a deployment marker, document revision or download checksum. A tag identifies the expected build. Verify that the destination actually serves it.
2. Open the intended URL with the audience's access and check the final destination after redirects. Use an anonymous session for a public release. Check the revision at that destination. A preview or signed-in session may help diagnose a mismatch, and is separate evidence. If the platform is still serving the previous revision, wait within the release window and report the observed revision and status.
3. Follow the agreed public paths. For websites, open the primary pages directly and exercise the intended journeys. Confirm the expected content and final destination so a fallback page with HTTP 200 cannot pass. For a critical action that sends, pays or writes live records, use the approved test environment or ask the authorised tester for a receipt. Treat that path as unverified until the agreed check runs. See the [signup example](signup-example.md). For downloads, fetch the asset, verify its digest when available and open the required contents. For documents, open the shared revision and check the agreed sections and audience access.
4. Record time, URL, revision evidence, result for each path and any unresolved item. Mark the release verified only when identity and every critical check pass at the environment and access level agreed in the release record. Record any test-only results separately from public read-back. Route a mismatch to the release owner with the observed evidence.

## Blockers and handoff

Stop and report if the destination needs access you do not have, the revision cannot be observed, or a critical path writes live records with no approved test or receipt. Mark those paths pending with the owner who can unblock them. Hand a mismatch to the release owner with the observed and expected revisions. Hand a public exposure concern to `public-exposure-check`. Rollback is the owner's decision.

## Output and checks

Use the [release record](template.md). Name the audience, expected and observed revisions, the result of each path and what blocks completion. Publication and rollback each follow the owning project's authority.
