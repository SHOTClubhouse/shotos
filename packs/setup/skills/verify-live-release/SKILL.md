---
name: verify-live-release
description: Verifies that an authorised website, document or download release is publicly available at the intended revision and that key user actions work. Use after a merge, deploy, publish or upload.
---

# Verify a live release

**Stage:** Track. Record the expected revision and the public result together.

1. Read the release record for the destination, intended revision, authorised scope and critical user paths. Choose an observable revision signal such as a deployment marker, signed tag, document revision or artifact checksum.
2. Open the public endpoint with the intended audience's access. Match the revision signal. If the platform is still serving the previous revision, wait within the release window and report the observed revision and status.
3. Follow the agreed public paths. For websites, open the primary pages and exercise the key action. For downloads, fetch the asset, verify its digest when available and open the required contents. For documents, open the shared revision and check the agreed sections and audience access.
4. Record time, URL, revision evidence, result for each path and any unresolved item. Mark the release verified only when identity and critical checks pass. Route a mismatch to the release owner with the observed evidence.

Use the [release record](template.md). Publication, verification and rollback each follow the owning project's authority.
