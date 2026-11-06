---
name: config-as-code
description: Keeps shared agent instructions, skills and settings in one reviewed repository and detects drift before syncing. Use when set-up lives on several machines or people, or after someone edits an installed copy. Never overwrites without showing the difference.
---

# Treat agent configuration as code

Stage: Sustain and Scale. Rules: 3 (read back the real result) and control 3 (capability is separate from authority).

If shared instructions, skills and settings can change in two places, they will. Make one repository the shared version, and let each person's tools be copies of it.

## Context and handoff

Read current tracked instructions, local overrides and the versions actually in use. Diff before applying any sync.

Use `skill-quality-gate` when a change affects behaviour. Record source revision and rollback in the configuration change.

## When not to use this

Skip personal tweaks that nobody else needs and nobody wants to keep. Never put secrets, tokens or machine-specific paths in the shared repository.

## Steps

1. **Name the two sides.** The shared repository, and the installed location the person's tool reads. Confirm both with the owner. Check that the repository has no uncommitted work, or say that it has. If asked to overwrite everything, or to copy a token or other secret into the repository, say so plainly: you will first list the differences and wait for a yes on each, and secrets never go into the repository.
2. **Check for drift first.** Compare installed files with the repository without changing either. List files only in the repository, files only in the installed copy, and files that differ, with the difference for each. Skip files marked as local (secrets, caches, history).
3. **Classify each difference.** Choose one:
   - **install:** the repository is right; update the installed copy.
   - **propose back:** the local change is an improvement; send it through a reviewed change.
   - **keep local:** it belongs to this machine only; add it to the local ignore list.
   - **conflict:** both changed; the owner decides.
4. **Show and stop.** Present the report and a proposed action for each difference. Wait for a yes per difference or for all. Never overwrite a file in either direction without showing its difference and getting a yes.
5. **Install.** For approved installs, copy from the repository to the installed location. Save the old installed file to a dated backup first so the change can be undone. Never install secrets.
6. **Propose back through review.** For a local improvement, put it on a branch or change request in the repository with a message that says why. A teammate reviews it as they would code. Do not merge or push to the shared branch without the owner's yes.
7. **Read back.** Check for drift again. Report that only explained differences remain, or list what is left and why.
8. **Log.** Record the date, who approved, what was installed or proposed, and where the backup is.

## Output

Use [template.md](template.md): a drift report, decisions and a log line.

## Checks

- Drift was checked before any change.
- Every overwrite had its difference shown and a yes recorded.
- Old installed files were backed up before being replaced.
- No secret or machine-specific path entered the repository.
- Local improvements went through a reviewed change, not a direct edit of the shared branch.
- A second drift check after the change shows only explained differences.
