---
name: work-folder
description: "Sets up a git-ignored .work/ folder for each task's acceptance card, notes, scratch and outputs, and closes it out: move outputs home, archive what must be kept, delete the rest after a yes. Use when starting or finishing a multi-file task."
---

# Keep work in progress in one place

Stage: Operate. Rules: 3 (read back the real result) and control 11 (one owning record).

Work in progress needs a home that is not the project's real source and not the chat. A `.work/` folder gives it one, and git ignores it.

## When not to use this

Skip it for a quick answer or a single small edit with no working files. Finished sources do not live here.

## Steps

1. **Find the project root.** Use the folder that holds the repository. If there is no repository, use the project folder the owner names.
2. **Check for an existing `.work/` folder.** If one exists, read its top level first and reuse it. Do not create a second one.
3. **Make git ignore it.** Look at `.gitignore`. If `.work/` is missing, add the one line when the request asked you to set up or use `.work/`, and say you did; otherwise show the line and wait for a yes before editing. After the edit, confirm with `git status` that the folder no longer appears as untracked. If the project has no git, say so and carry on.
4. **Open one folder per task.** Name it `YYYY-MM-DD_subject` (for example `.work/2026-03-04_price-list-update/`). Inside it create:
   - `acceptance.md`: the card from agree-acceptance, with a named owner.
   - `notes.md`: decisions, questions and the running state in short lines, newest at the bottom.
   - `scratch/`: throwaway files you may delete without asking the owner.
   - `outputs/`: files meant to leave the folder.
5. **Keep secrets out.** Never write a password, key, token or full personal record into any file here. Record that a credential is needed and where the owner keeps it. If you find one already present, report its file and line and do not copy it anywhere. Say it should be rotated if it was ever committed or shared.
6. **Keep one task per folder.** If new work does not belong to an open task, open another folder rather than adding to the old one.
7. **Close out when finished.** List three groups: files that move to a named permanent location (with the destination), files to archive, and files to delete (scratch only). Show the list. If the request already asked for the close-out or the move, that is the yes for it; otherwise move or delete only after the owner says yes. Never delete anything in `outputs/` unless the request named that file or the owner says yes for it.
8. **Leave a closing line in `notes.md`.** State the date, who accepted the work and where the outputs went.

## Output

A `.work/<task>/` folder using [template.md](template.md), then at the end a close-out list.

## Checks

- `git status` shows `.work/` is not tracked or untracked.
- Every task folder has an `acceptance.md` that names an owner.
- No file in the folder contains a credential or a full personal record.
- The close-out list was shown, and no move or deletion happened beyond what the request named or the owner approved.
