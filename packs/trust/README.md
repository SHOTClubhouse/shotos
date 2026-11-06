# trust pack

**Checks before anything goes out: audit claims, check for public exposure, and check sensitive and children's data.**

The pack gives an agent and its owner three checks to run before a document, repository or form leaves the building. Each one lists findings with locations or evidence, ranks them, and proposes a fix. None of them changes, rotates, deletes, unshares or publishes anything without the owner's yes, and the sensitive-data check stops outright when consent is missing.

## Who it is for

- Founders, sales and marketing leads sending documents to customers or buyers.
- Small teams publishing repositories, sites or shared folders.
- Clubs, schools and charities that handle information about children.
- Anyone who wants an independent look at a document before it is sent.

## Skills

| Skill | Step | What it does |
|---|---|---|
| [claims-audit](skills/claims-audit/README.md) | Check | Lists every factual claim in a public document with its source, status and proposed fix; numbers need a dated source. |
| [public-exposure-check](skills/public-exposure-check/README.md) | Check | Looks for secrets, personal data, internal paths and over-wide sharing before publishing; says what to rotate; changes nothing. |
| [sensitive-data-check](skills/sensitive-data-check/README.md) | Brief | Checks work on special-category or children's data for minimisation, consent, retention, access and safeguarding; stops when consent is missing. |

## Needs

Read access to the document, repository or folder being checked, plus any evidence the owner can provide: source files, consent records, sharing settings. No connectors are required. For shared documents, a connector that reads sharing settings makes the check faster; otherwise the owner supplies the list.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack trust --dry-run
python ../shotos/install.py --runtime claude --scope project --pack trust
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack to a project that already has SHOTos, run `python ../shotos/install.py --uninstall`, then install again with every pack you want. Files you changed are kept. If a changed file is in the way, the reinstall stops: move it aside (or keep your copy and skip that skill) before you reinstall.

As a Claude Code plugin:

```
/plugin marketplace add SHOTClubhouse/shotos
/plugin install shotos-trust@shotos
```

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The checks apply the four rules in [docs/controls.md](../../docs/controls.md), especially rule 4, Claim only what you can show, and rule 1, Stop at the boundaries. The data governance guardrail is in [rules/guardrails/README.md](../../rules/guardrails/README.md). Quarantined files from the [records pack](../records/README.md) often lead here.

**Evidence:** Cases written, not yet run. Eval cases are in [evals/packs/trust.json](../../evals/packs/trust.json).
