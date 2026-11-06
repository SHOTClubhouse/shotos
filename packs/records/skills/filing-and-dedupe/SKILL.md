---
name: filing-and-dedupe
description: Organises a folder by owner and category and finds duplicates by size and checksum, planning moves with an undo log. Use when a shared or inherited folder has no structure or may hold duplicates. Acts only after a yes.
---

# File and de-duplicate with a plan

Stage: Operate. Rules: 1 (stop at the boundaries) and 3 (read back the real result).

## Context and handoff

Inspect the actual folder and the canonical records. Match duplicates by content and verify which location the owner relies on.

Use `quarantine` for authorised relocation. Save a source-to-destination map and read back the result.

## When not to use this

Skip folders under a legal hold or audit. Do not tidy a folder that nobody has asked you to tidy, or that someone else owns.

## Steps

1. **Fix the scope.** Name the one folder, its owner and what is out of bounds. If the owner is unclear, ask.
2. **Take an inventory.** List every file with path, size, modified date and type. Do not open files beyond what classifying needs. Do not read personal records; note that they exist and send them to quarantine.
3. **Propose a structure.** Group by owner first, then category (for example `finance`, `people`, `operations`, `projects`, `reference`, `archive`). Keep it two or three levels deep. Show the tree with a count of files for each branch. Use the project's own structure if it has one.
4. **Find duplicates.** Group files by exact size first, then compute a checksum (SHA-256) for files that share a size. Files are duplicates only when size and checksum both match. Never treat matching names as duplicates; list same-name files with different checksums as a separate "same name, different content" group.
5. **Choose what to keep.** For each duplicate group, propose the copy to keep by owner and location, and say why. The others are candidates to move.
6. **Write the plan.** A table with one row per file: current path, action (move, rename, move to quarantine, remove), destination, reason, and the group it belongs to. Prefer a move to an `_archive` or quarantine folder over deletion. Mark any real deletion as needing its own yes.
7. **Show the plan and stop, unless the request already said yes.** Give the totals: files moved, files removed, space freed. Wait for a yes, and accept a yes for part of the plan. If the owner's request already asked for an action (for example "sort it into folders and delete the duplicates"), that is the yes for exactly that: moves into the agreed structure and removal of byte-identical duplicates confirmed by checksum. Still stop for anything the request did not cover, such as look-alike files that differ.
8. **Execute the approved rows only.** Move rather than delete. Write a change log with old path, new path, checksum and time for every action so each can be reversed.
9. **Read back.** Re-run the inventory and confirm counts match the plan: nothing missing, nothing extra, and the log is complete.

## Output

A structure proposal, a duplicate report, a plan table, and after approval a change log. Use [template.md](template.md) for the plan and log.

## Checks

- Duplicates were found by size and checksum, not by name.
- The plan was shown before any change, unless the request already named the action; only approved or requested rows were applied.
- No file was deleted where a move would do; any deletion was either named in the request or had its own yes.
- Every change is in the log with enough detail to undo it.
