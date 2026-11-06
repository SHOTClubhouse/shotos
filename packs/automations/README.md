# Automations pack

**Two complete Google Apps Script automations, free on any Google account, plus the skills that set them up and run them safely.**

Apps Script runs inside your Google account, so there is nothing to host and no extra bill. The two scripts here are written for this repository and are small enough to read in one sitting. Each one starts in a safe mode, proves itself on a few items, and only then runs on a schedule.

## What is in it

| Skill | Stage | What it does |
|---|---|---|
| [signal-engine](skills/signal-engine/README.md) | Operate | Walks an agent and a person through setting up the signal engine: read mail under one label, score items against your priorities, queue them in a sheet and send one daily digest to you. |
| [batch-document-factory](skills/batch-document-factory/README.md) | Operate | Walks an agent and a person through setting up the document factory: one Google Doc or Slides file per sheet row, filled from a master template. |

| Script | Folder | Never does |
|---|---|---|
| Signal engine | [scripts/signal-engine](scripts/signal-engine/README.md) | Reply to, forward, label or delete mail. It emails only the digest address (`DIGEST_TO`), which is one configured address and is the owner's account by default. |
| Batch document factory | [scripts/batch-document-factory](scripts/batch-document-factory/README.md) | Send, share or delete anything. |

## Who it is for

- A small business owner who gets more newsletters and alerts than they can read.
- An operations lead who produces the same document for many people, such as letters, quotes, certificates or onboarding packs.
- Anyone who wants an automation they can read, change and switch off, with no subscription.

## How the skills keep it safe

Both skills follow the same order, which is control 9 (pilot before scale) and control 6 (read back) from the [twelve controls](../../rules/README.md), applied to a script:

1. Install the script and read what it will touch.
2. Run it in dry-run mode and read the log.
3. Run a pilot of three items, and read the real output in its real home (the sheet, the inbox, the generated document).
4. Ask the owner to accept the pilot.
5. Only then install the schedule.

An agent can write files and explain steps. It cannot paste code into your Google account or click "Allow" on the consent screen for you, so the person does those steps and the skill says exactly when.

## Needs

- A Google account (a personal account or Workspace).
- The person doing the setup, because pasting the script and approving permissions happen in their browser.
- For the optional AI scoring in the signal engine: an API key for an AI provider, stored in Script Properties only. The scoring is off by default.
- Apps Script has daily quotas. See the notes in each script README.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack automations --dry-run
python ../shotos/install.py --runtime claude --scope project --pack automations
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## Evidence

Earlier skill versions were tested in paired runs. See the [evidence by build](../../docs/evidence.md). The scripts have been syntax-checked with Node.js (`node --check`) and their text-handling functions exercised outside Google. They have not been run inside a live Google account by the author of this pack, so treat your own dry run and pilot as the real test.

Cases: [evals/packs/automations.json](../../evals/packs/automations.json).
