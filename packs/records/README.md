# records pack

**Keep files findable and safe, for people and agents: a work folder, file naming, filing with de-duplication, and a quarantine for doubtful files.**

The pack covers the plain habits that stop a project folder turning into a mess: one ignored place for work in progress, names that carry a date, owner and version, a tidy structure found by evidence rather than guesswork, and a holding area with a register for files nobody can classify. Every change is shown as a plan first, and nothing is deleted without the owner's yes.

## Who it is for

- Office managers and administrators looking after shared folders.
- Small teams working with an agent in a git repository.
- Anyone who inherits a folder and needs to make it safe before using it.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [work-folder](skills/work-folder/README.md) | Operate | Sets up a git-ignored `.work/` folder with one owning folder per task, and closes tasks out with a list of what moves. |
| [file-naming](skills/file-naming/README.md) | Operate | Names files `YYYY-MM-DD_owner_subject_vNN.ext`, handles versions and status words, and shows a rename plan first. |
| [filing-and-dedupe](skills/filing-and-dedupe/README.md) | Operate | Proposes a structure by owner and category, finds duplicates by size and checksum, and executes an approved plan with a change log. |
| [quarantine](skills/quarantine/README.md) | Operate | Moves doubtful files to a quarantine folder with a register and a review date, instead of deleting. |

## Needs

Read and write access to the project folder, nothing else. No connectors are needed. Checksums need a command line tool or a short script. Without write access the skills produce the plan or register as text for a person to apply.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack records --dry-run
python ../shotos/install.py --runtime claude --scope project --pack records
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack to a project that already has SHOTos, run `python ../shotos/install.py --uninstall`, then install again with every pack you want. Files you changed are kept. If a changed file is in the way, the reinstall stops: move it aside (or keep your copy and skip that skill) before you reinstall.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

Each skill follows the four rules in [docs/controls.md](../../docs/controls.md): changes stop at the owner's yes, and results are read back. Quarantined files that hold personal data lead to [sensitive-data-check](../trust/skills/sensitive-data-check/README.md) in the trust pack. The stages are described in [docs/framework.md](../../docs/framework.md).

**Evidence:** Cases written, not yet run. Eval cases are in [evals/packs/records.json](../../evals/packs/records.json).
