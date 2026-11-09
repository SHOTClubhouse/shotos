---
name: quarantine
description: Moves doubtful files (unknown owner, personal data, duplicates, unclear rights) into a quarantine folder with a register instead of deleting. Use when a tidy-up finds a file you cannot safely classify. Never takes files from their owner.
---

# Quarantine instead of delete

Stage: Operate. Rules: 1 (stop at the boundaries) and 4 (claim only what you can show).

When you cannot tell whether a file is wanted, safe or yours to remove, move it somewhere visible and ask. Deleting loses information; leaving it in place spreads risk.

## Context and handoff

Read the duplicate proof, current paths and approved quarantine location. Verify the retained copy before moving anything.

Use `filing-and-dedupe` if identity is unresolved. Keep a reversible move log with original paths and checksums. Keep the register in the quarantine folder itself and give its path in the handoff, so the reviewer finds it without the chat.

## When not to use this

Skip files that are clearly owned, wanted and safe. Do not quarantine something outside the scope you were given, and never use quarantine to take a file away from its owner.

## Steps

1. **Decide whether the file is doubtful.** If asked to delete a file permanently and it may hold personal data, quarantine it instead and say so: deletion waits for the owner's confirmation once they know what it holds and that it is not the only copy. Use these triggers: owner unknown; may hold personal data (names with phone numbers, emails, health or children's details); may be a duplicate you cannot prove; rights or origin unclear (photos or documents with no source); or you cannot tell what it is.
2. **Find or create the quarantine folder.** Use `_quarantine/` at the root of the folder being tidied. Check for any sync or share rule you can see on it. If you cannot tell, say so in the register.
3. **Record before moving.** Add a register row first: file (original path), why (one plain sentence), found by (agent or person), date, decision needed (keep and file, keep and protect, delete, ask the owner), and owner (a named person who decides).
4. **Move, do not copy or delete.** If the register already lists the file or the destination name is taken, update that row or add a numbered suffix; never overwrite or add a second row. Keep the original name and add the original path to the register. Do not open personal files beyond what you need to classify them; never copy their contents into the register.
5. **Set a review date.** Propose a date within a month. Record it in the register header. Tell the owner the date and who reviews.
6. **Report.** List the files moved, the reasons, the register path, the review date, who reviews, and any that need urgent attention, for example personal data in a shared folder. After the move, read the quarantine folder back against the register: every row has a file and every file has a row.
7. **At the review.** Ask the owner for a decision on each row. Execute only decisions that are recorded, and ask for an explicit yes before any deletion. Log what changed.

## Output

A populated `_quarantine/` folder and a register, using [template.md](template.md).

## Checks

- Every quarantined file has a register row with all columns filled in.
- The register says why in a form someone else can check.
- No file was deleted, and the register holds no personal data itself.
- A review date and a named reviewer are set.
- A rerun adds no duplicate rows and overwrites nothing.
