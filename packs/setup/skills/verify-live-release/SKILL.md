---
name: verify-live-release
description: Verifies that an authorised website, document or download release is publicly available at the intended revision and that key user actions work. Use after a merge, deploy, publish or upload.
---

# Verify a live release

**Stage:** Track. Record the expected revision and the public result together.

1. Read the release record for the destination, intended revision, authorised scope and critical user paths. Choose a revision signal the intended audience can observe at that destination, such as a deployment marker, document revision or download checksum. A tag identifies the expected build. Verify that the destination actually serves it.
2. Open the intended URL with the audience's access and check the final destination after redirects. Use an anonymous session for a public release. Check the revision at that destination. A preview or signed-in session may help diagnose a mismatch, and is separate evidence. If the platform is still serving the previous revision, wait within the release window and report the observed revision and status.
3. Follow the agreed public paths. For websites, open the primary pages and exercise agreed read-only actions. For a critical action that sends, pays or writes live records, use the approved test environment or ask the authorised tester for a receipt. Treat that path as unverified until the agreed check runs. See the [signup example](signup-example.md). For downloads, fetch the asset, verify its digest when available and open the required contents. For documents, open the shared revision and check the agreed sections and audience access.
4. Record time, URL, revision evidence, result for each path and any unresolved item. Mark the release verified only when identity and every critical check pass at the environment and access level agreed in the release record. Record any test-only results separately from public read-back. Route a mismatch to the release owner with the observed evidence.

Use the [release record](template.md). Publication, verification and rollback each follow the owning project's authority.
