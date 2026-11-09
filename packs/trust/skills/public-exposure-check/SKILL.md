---
name: public-exposure-check
description: Checks a repo, site, folder or document for secrets, personal data, internal paths and over-wide sharing before it goes public. Use when publishing or sharing outside the team. Never rotates, deletes or unshares without a yes.
---

# Check before it goes public

Stage: Track. Rules: 1 (stop at the boundaries) and 3 (read back the real result).

Once a file or key is public, it cannot be taken back. Look first.

## Context and handoff

Read the exact artefact or revision, intended audience, current permissions and any existing public disclosures. Inspect its metadata and linked material.

Use `sensitive-data-check` for restricted content. Record findings and the publish decision privately without reproducing sensitive values.

## When not to use this

Skip things that will stay private. This is not a penetration test and not a review of a live service.

## Steps

1. **Fix the target and the audience.** Name what will be shared (repository, folder, site, document), who will see it, and who owns it. Record the exact revision checked (commit hash, document revision or folder snapshot date) so the go or hold applies to that revision only. Ask if either is unclear.
2. **Search for secrets.** Look for API keys, tokens, passwords, private keys, connection strings, `.env` files and credentials in config, scripts, notebooks and examples. For a repository, search the history as well as the current files. Record each as a finding with file and line (or commit), but never copy the secret value into your report; show the first four characters at most.
3. **Search for personal data.** Look for names with emails, phone numbers, addresses, dates of birth, account numbers, health or children's details, photos of people, and exported spreadsheets. Note the file, the type of data and a rough size. Do not reproduce it.
4. **Search for internal detail.** Look for local file paths, internal server names, private URLs, customer or client names, staff names where not intended, internal notes, comments such as "do not share", and metadata such as author fields or tracked changes.
5. **Check what should not be included.** Look for build output, backups, logs, temporary files, `.work/` folders, large data exports and test fixtures built from real data.
6. **Check the sharing setting.** For a document or folder, record who can currently see or edit it: named people, anyone in the organisation, anyone with the link, or public. Compare with the intended audience.
7. **Rate and report.** For each finding give severity (urgent, fix before sharing, review), location, what it is and the suggested action. Put first any real credential that is, or may have been, exposed: say it should be rotated now, whatever else happens.
8. **Recommend go or hold and stop.** Say hold if any urgent or fix-before-sharing finding remains. Do not remove, rotate, rewrite history or change sharing yourself; ask the owner for a yes for each action.

## Output

Use [template.md](template.md): a findings table, an urgent rotation list and a go or hold line.

## Checks

- Secrets were searched in history as well as current files, or the report says history was not available.
- No secret value or personal record is reproduced in the report.
- Every finding has a location and a suggested action.
- Anything that may need rotating is stated first.
- The report names the revision checked, and says the result must be repeated if the content changes before release.
- Each finding has a stable number, so the owner can answer yes, no or accepted against it.
- Nothing was changed, and a go or hold recommendation is given.
