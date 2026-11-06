# Records and filing

## What it is

Records are the evidence that work happened and what it produced: the brief, the acceptance, the drafts, the decisions, the final output and the proof it was checked. Filing is how you keep them findable. Good filing is dull and saves hours. The guiding public standard is ISO 15489, the international standard for records management, which asks that records be authentic, reliable, complete and usable for as long as they are needed. This page takes its spirit, not its paperwork.

## Why it matters with agents in the loop

Agents create files at speed: drafts, exports, logs, scratch notes, five versions of the same thing. Left alone, a folder fills with near-duplicates, and nobody can tell which is the real one. Agents also delete and overwrite with confidence. Clear places to put things, clear names and a firm habit about deleting are what keep the work trustworthy. This is also where [rule 1](../rules/04-stop-boundaries.md) bites: deleting is on the list of things an agent does not do without a yes.

## The practice

### A `.work/` folder for work in progress

Keep drafts, scratch files, intermediate outputs and logs in a local folder named `.work/` at the top of the project. Add `.work/` to the ignore file so that git never sees it. Work in progress stays out of the shared record until someone decides it belongs there. Anything worth keeping moves to its proper home when finished; the rest can be cleared at the end of the task.

The folder is also a safe default: an agent told to work in `.work/` cannot clutter the project or send half-finished things anywhere.

### One owning folder per piece of work

Give each piece of work one folder inside `.work/` (or one task record), named for the work and containing everything about it: the acceptance card, inputs, drafts, evidence and the final handoff. One piece of work, one owner, one place. If you must refer to something elsewhere, link to it from the task record; do not copy it. See [context-and-tokens.md](context-and-tokens.md) on the one owning record.

A simple layout:

```
.work/
  2025-03-12_ops_tenant-update/
    acceptance.md
    inputs/
    drafts/
    evidence/
    handoff.md
```

The date in this example is illustrative.

### Naming in the spirit of ISO 15489

A name should say what a file is, who owns it, when it began and which version it is, so that it sorts and can be found without opening it. A good pattern:

`YYYY-MM-DD_owner_subject_vNN.ext`

For example `2025-03-12_ops_tenant-update_v02.docx`.

Guidance:

- **Date first,** in year-month-day order, so a folder sorts by time.
- **Owner,** a short code for the team or person accountable.
- **Subject,** a few plain words, lower case, with hyphens inside the subject and underscores between the parts.
- **Version,** two digits, only when there is more than one.
- **No spaces or odd characters,** which break scripts and links.
- **No "final", "final2" or "new".** They stop being true the moment someone edits again.
- **Keep names short enough to read.** If a name needs more words, the subject is probably two things.

Agree the pattern once for the team, write it down in one place and apply it to new files. Do not rename a whole archive for the sake of tidiness unless someone owns the work and has said yes.

### Versions

- **Edit in place for small changes.** Fixing a typo, correcting a figure or tightening wording does not need a new file. Use the history that your editor or version control already keeps.
- **New version only for a new decision.** If the content changes because someone decided something different (new scope, new price, a different audience), save a new version and say why in a line at the top.
- **One current file.** Mark which version is current, and move older ones to an `archive` subfolder rather than leaving them beside it.
- **Do not create a copy to experiment on** unless the experiment is a different decision. Branch in version control if you need to.

### Duplicates

Before deleting anything because it looks like a duplicate:

1. **Compare by exact size and by checksum.** Two files with the same name or a similar name are not necessarily the same. Files with the same byte size and the same checksum (for example a SHA-256 value) are identical. Files with only the same size are candidates and still need the checksum.
2. **Look at where each is linked from.** A duplicate that a document or page points to is not safe to remove.
3. **Report the pairs and the proposed action.** List what you found, which one would be kept and why.
4. **Never delete without a yes** from the owner of the folder. Move first, delete later.

An agent may find and report duplicates. It does not remove them.

### A quarantine folder for doubtful files

When a file's origin, owner or purpose is unclear, do not guess and do not delete. Move it to a clearly named `_quarantine/` folder at the top of the owning area, with a note recording where it came from, when it was moved and why. Review the quarantine on a schedule, say monthly. Each item then gets one outcome: restored, filed properly, or deleted with the owner's yes.

Quarantine is also the place for files you suspect contain a secret or personal data that should not be where it is. Tell the owner promptly.

### Retention

Decide how long each kind of record is kept, and write it down. Keep records at least as long as a legal, contract or tax rule requires, and no longer than you need, especially personal data. A simple three-tier view:

- **Working files** in `.work/`: clear at the end of the task or after a short fixed period.
- **Task records and evidence:** keep as long as the work or product lives, and then for the period the rules require.
- **Decisions and acceptance:** keep with the product, since they explain why it is the way it is.

If you do not know the required period, record that as an open question for the owner. Do not make one up.

## What good looks like

- A newcomer can find the current version of anything within a minute.
- Each piece of work has one folder and one owner.
- Names sort in a useful order and say what the file is.
- Nothing is deleted on a guess.
- Old versions are archived, not scattered.
- Quarantine is small, dated and reviewed.

## Anti-patterns

- **The Downloads graveyard.** Files named "document (3)".
- **A copy per recipient** with edits that never merge.
- **"final_FINAL_v2".**
- **Deleting by name:** "these look the same".
- **An agent that tidies by itself** and removes something that was still in use.
- **Work in progress committed to the shared record** because it was in the way.
- **Evidence in the chat only.** If it is not in the task record, it will be lost.

## How it maps to the stages and rules

- **All stages:** the task record is where the problem statement, acceptance, evidence and decision live.
- **Track:** the evidence pack is built from filed records.
- **Own:** the handoff includes where everything is and who owns it.
- **Rule 1:** deleting, moving shared files and overwriting someone else's work wait for a yes.
- **Rule 3:** read back the file in its real home, and confirm it is the one you meant.
- **Rule 4:** claim "filed" only when the file is there; keep the receipt.

## A short example

An agent working for Harbourside Lettings is asked to tidy the shared "tenant letters" folder. It starts in a `.work/2025-03-12_ops_letters-tidy/` folder. It lists the files and finds nine that appear twice. Seven pairs match on size and checksum. Two pairs match on name only; their contents differ. The agent writes a table of the pairs, proposes keeping the oldest of each identical pair and flags the two different ones as separate documents. It deletes nothing. It moves three files with no clear owner into `_quarantine/` with a note and asks the operations lead for a yes on the seven deletions. The lead agrees to six and asks to keep one, because a template links to it. The agent applies exactly those six, records what was removed and reads the folder back to confirm.

## Further reading

- *ISO 15489-1, Information and documentation: Records management*, International Organization for Standardization.
- *ISO 8601*, the date and time format behind `YYYY-MM-DD`.
- David Allen, *Getting Things Done*, for the habit of one trusted place.
- Jez Humble and David Farley, *Continuous Delivery*, on keeping everything in version control.
