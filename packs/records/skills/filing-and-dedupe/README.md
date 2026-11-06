# filing-and-dedupe

**Organise a folder by owner and category, find duplicates by size and checksum, and act only after a yes.**

This skill proposes a folder structure by owner and category, finds duplicate files by exact size and checksum (never by name alone), proposes moves and removals as a plan, executes only after a yes, moves instead of deleting wherever it can, and logs every change so it can be undone.

It supports the Operate stage. It serves rule 1, Stop at the boundaries (no deletion without a yes), and rule 3, Read back the real result.

## The problem it solves

Millbrook Rovers youth club has a shared folder with 900 files. Three people each saved their own copy of the kit order, and the same fixtures list appears under five names. A tidy-up that deleted by name would have removed two different coaching rotas called `rota.xlsx`. Matching by size and checksum finds the true copies, and a plan makes the owner decide.

## When to use it, and when not to

Use it when a shared folder has grown without a structure, when you suspect duplicate files, or before archiving a project.

Skip it for a folder under a legal hold or an audit, where nothing may move. Do not run it on a folder you do not own or have not been asked to tidy.

## Who it is for

- Administrators of shared drives and club or office folders.
- Anyone inheriting a project folder.
- Agents asked to tidy a workspace.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Tidy the 2025-26 season folder. Propose a structure and find duplicates. Show me the plan; do not move or delete yet.

You get a proposed structure, a duplicate report (groups of identical files with size, checksum and locations), a plan of moves and removals, and a request for your yes. After the yes, changes are made and logged.

## How it connects

- **Related:** [file-naming](../file-naming/README.md) renames files once the structure is agreed.
- **Related:** [quarantine](../quarantine/README.md) holds anything the plan marks doubtful instead of deleting it.
- **Rules:** [04, stop-boundaries](../../../../rules/04-stop-boundaries.md) is why every removal waits for the owner.

## Needs

Nothing beyond the agent, plus read and write access to the one folder it is tidying and a way to compute checksums, for example a command line tool. No connectors.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Start with a read-only report; many folders need only a rename.
- Treat a checksum match as proof of identical content and a name match as no evidence at all.
- Pick which copy to keep by owner and location, not by modified date.
- Run on a copy of a very large folder first.

## Limits

- Two files with the same content may both be needed in different places; the plan asks rather than assumes.
- Near-duplicates (the same document saved twice with edits) are not found by checksums; they are raised as questions only.
- Cloud storage may hold its own versions and trash that this skill does not see.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/filing-and-dedupe/input.md) and [output](../../examples/filing-and-dedupe/output.md).
