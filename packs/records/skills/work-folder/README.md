# work-folder

**Keep work in progress in one ignored `.work/` folder, one owning folder per task, with nothing secret in it.**

This skill sets up a local `.work/` folder that git ignores, and gives every task one owning folder inside it holding the acceptance card, notes, scratch files and outputs. When the task is finished, it lists what moves out, what is archived and what is deleted, and waits for the owner's yes before moving anything.

It supports the Build step. It serves rule 3, Read back the real result, and control [11, context-control](../../../../rules/11-context-control.md): one owning record per task.

## The problem it solves

Harbourside Lettings has three people and an agent working in the same repository. Draft tenancy letters, half-finished spreadsheets, a pasted API key in a notes file and two copies of the same price list sit next to the real source files. Someone commits the notes file by accident, and nobody can tell which draft is current. With one owning folder per task, git ignoring the whole area and a rule against secrets, drafts stay out of history and each task has one place to look.

## When to use it, and when not to

Use it when starting a task that will produce more than one file, when a project has scratch files scattered through it, or when work in progress keeps appearing in commits.

Skip it for a one-line answer or a single small edit with no working files. Do not use it as a place to store the finished source of the project; sources stay where the project keeps them.

## Who it is for

- Anyone running an agent in a git repository who wants drafts kept out of history.
- Team leads who want each task to have one findable home.
- Solo founders who lose track of which draft is current.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Set up a work folder for this repository, and open a task folder for the March price list update.

You get a `.work/` folder, a git ignore entry (shown to you before it is written), and a task folder with an acceptance card and a notes file. At the end of the task you get a close-out list to approve.

## How it connects

- **Before:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) writes the card that goes in the task folder.
- **Related:** [file-naming](../file-naming/README.md) names the files inside, and [quarantine](../quarantine/README.md) holds anything doubtful.
- **After:** [evidence-handoff](../../../../skills/evidence-handoff/README.md) records what was accepted when the task closes.

## Needs

Nothing beyond the agent, plus read and write access to the one project folder it is working in. No connectors.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Name the task folder with a date and a short subject so the list sorts itself.
- Put the owner's name in the acceptance card, not only in the folder name.
- Check the ignore rule worked with `git status` before writing the first file.
- Log a secret's existence by name only, never its value.

## Limits

- Git ignoring a folder does not make it private. Anyone with the machine or a backup can read it.
- The skill cannot detect a secret it does not recognise; scan before the close-out.
- It does not manage shared drives; a synced folder is a different risk.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/work-folder/input.md) and [output](../../examples/work-folder/output.md).
