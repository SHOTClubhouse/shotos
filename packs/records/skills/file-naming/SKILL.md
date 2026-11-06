---
name: file-naming
description: Names files as YYYY-MM-DD_owner_subject_vNN.ext and shows a rename plan with collision checks first. Small fixes are edits in place; a new version marks a decision; 'final' only when an owner accepts. Use when files must be findable.
---

# Name files so they can be found

Step: Build. Rules: 3 (read back the real result) and 4 (claim only what you can show).

A good name tells a stranger the date, whose file it is, what it is about and which version it is, without opening it.

## When not to use this

Skip files that a tool expects under a fixed name (`README.md`, `package.json`, build output). Do not rename a file that other files link to until the links are listed.

## The pattern

`YYYY-MM-DD_owner_subject_vNN.ext`

- **Date:** the date of the document, not the date it was copied. ISO form so folders sort by time.
- **Owner:** the person, team or system responsible, short and lower case.
- **Subject:** what it is, two to five words, hyphens inside the part.
- **Version:** `v01`, `v02`. Two digits.
- Separate parts with underscores. Lower case. No spaces, no accents, no characters other than letters, digits, hyphens and underscores.

## When to drop parts

- Drop the owner when the folder is already owned by one person or team.
- Drop the date for reference material that has no date, such as a template or a policy under review; keep the version.
- Drop the version for a file that is only ever one thing, such as a photo or a received invoice.
- Never drop the subject.

## Versions

- **Edit in place** for small changes: typos, formatting, a corrected figure. Version history belongs to the tool or to git.
- **New version** for a new decision: the content now means something different. Keep the old one; it records what was decided before.
- Never use `final2`, `new` or `copy` in a name.

## Status words

Use `draft` or `final` sparingly, as a last part before the extension (for example `_v02_draft`). `final` is allowed only after the owner has accepted the file, and only one file in a set carries it. When unsure, leave the word out.

## Steps

1. **Read the folder.** List files with size and modified date. Do not open personal or confidential files beyond what naming needs.
2. **Decide the pattern.** Use the one above unless the project already has a convention; then follow that and say so.
3. **Build the rename plan.** A table: current name, proposed name, reason, and a flag for any collision (two files proposed the same name) or any link that points at the old name.
4. **Show the plan.** If the request already asked for the rename (for example "rename these to the standard pattern"), that is the yes for exactly that: apply it, and stop only for collisions, broken links or anything the request did not cover. If the request did not name renaming, or the change reaches beyond what was asked, show the plan and wait for a yes. Offer to apply only part of it.
5. **Apply once approved.** Rename, do not copy. Write the old and new names to a log so the change can be undone.
6. **Read back.** List the folder again and confirm the names match the plan and nothing else changed.

## Output

The pattern, the plan table, and after approval the log of renames.

## Checks

- Every proposed name follows the pattern or states why a part was dropped.
- No two files share a proposed name.
- No `final` appears without the owner's acceptance.
- Nothing was renamed unless the request named it or the owner said yes, and the log allows an undo.
