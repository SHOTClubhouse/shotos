# trust pack

**Checks before anything goes out: audit claims, check for public exposure, and check sensitive and children's data.**

The pack gives an agent and its owner three checks to run before a document, repository or form leaves the building. Each one lists findings with locations or evidence, ranks them, and proposes a fix. None of them changes, rotates, deletes, unshares or publishes anything without the owner's yes, and the sensitive-data check stops outright when consent is missing.

## Who it is for

- Founders, sales and marketing leads sending documents to customers or buyers.
- Small teams publishing repositories, sites or shared folders.
- Clubs, schools and charities that handle information about children.
- Anyone who wants an independent look at a document before it is sent.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [claims-audit](skills/claims-audit/README.md) | Track | Lists every factual claim in a public document with its source, status and proposed fix; numbers need a dated source. |
| [public-exposure-check](skills/public-exposure-check/README.md) | Track | Looks for secrets, personal data, internal paths and over-wide sharing before publishing; says what to rotate; changes nothing. |
| [sensitive-data-check](skills/sensitive-data-check/README.md) | Scope | Checks work on special-category or children's data for minimisation, consent, retention, access and safeguarding; stops when consent is missing. |

## Needs

Read access to the document, repository or folder being checked, plus any evidence the owner can provide: source files, consent records, sharing settings. No connectors are required. For shared documents, a connector that reads sharing settings makes the check faster; otherwise the owner supplies the list.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack trust --dry-run
git -C ../shotos rev-parse HEAD
python ../shotos/install.py --runtime claude --scope project --pack trust
python ../shotos/install.py --runtime claude --scope project --status
```

Write down the commit that `rev-parse` prints, or the release tag you meant to install, before you install. `--status` reads back the recorded runtime, scope and packs, and lists any installer-owned file that is missing or changed. It does not print the source revision, so the commit you noted is your record of which version you installed. A clean `--status` shows that the files match what the installer wrote, not that the skills work.

Handing the set-up to another runtime (for example from Claude to Codex)? Run the install again with `--runtime codex` or `--runtime agents` from the same checkout and commit, then run `--status` for that runtime. Each runtime keeps its own record, so check each one separately.

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The checks apply the four rules in [docs/controls.md](../../docs/controls.md), especially rule 4, Claim only what you can show, and rule 1, Stop at the boundaries. The data governance guardrail is in [rules/guardrails/README.md](../../rules/guardrails/README.md). Quarantined files from the [records pack](../records/README.md) often lead here.
