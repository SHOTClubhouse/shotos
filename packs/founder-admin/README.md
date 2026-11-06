# Founder admin

**Find funding and recognition, keep investors informed, prepare for due diligence and set up an advisory board, with an agent that drafts by default and submits, pays or shares only after a yes on exactly what goes.**

This pack covers the admin that small organisations put off until it is urgent. Each skill turns a vague job into a short, checkable piece of work, with the evidence for every claim and a clear point where a person says yes.

## Who it is for

- Founders and directors of small companies, clubs and charities.
- Operations leads who run funding applications, investor reporting and legal housekeeping.
- Anyone preparing for a funding round, an audit or a board.

## The skills

| Skill | SHOTos stage | What it does |
|---|---|---|
| [grants-finder](skills/grants-finder/README.md) | Scope | Finds and screens grants: eligibility first, then evidence, then budget. Shortlist with deadlines and fit. Drafts applications; submits only after a yes on exactly what goes. |
| [awards-finder](skills/awards-finder/README.md) | Scope | Finds free-to-enter awards, screens eligibility and prepares evidence-backed entries. Pays or submits only after a yes on exactly what goes. |
| [investor-update](skills/investor-update/README.md) | Track | Drafts a monthly or quarterly investor update from approved material only, with every figure traceable. Drafts by default; sends only after a yes. |
| [data-room](skills/data-room/README.md) | Own | Builds and audits a due-diligence data room: standard categories, an index, what is missing, who may see what, and a check that nothing is shared more widely than intended. |
| [advisory-board-kit](skills/advisory-board-kit/README.md) | Hypothesise | Sets up an advisory board: roles, expectations, a terms summary for a lawyer to review, meeting rhythm, contribution map and what advisers may say publicly. |

## What this pack does not do on its own

It does not submit an application or an entry, pay a fee, send an update, share a folder, sign anything or give legal advice without a yes on exactly what goes (and it does not give legal advice at all). Each skill drafts and stops for a named person's yes (rule 1, [Stop at the boundaries](../../docs/controls.md)). Money, personal data and confidential documents are handled on the assumption that the person must approve each step.

## Needs

Nothing beyond the agent for the core of every skill. Some work better with read access to a folder of documents, an accounts export or a document store; each skill README says which. No skill needs permission to write to, send from or share any of them.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack founder-admin --dry-run
python ../shotos/install.py --runtime claude --scope project --pack founder-admin
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

Evidence: earlier skill versions were tested in paired runs. See the [evidence by build](../../docs/evidence.md). See [evals/packs/founder-admin.json](../../evals/packs/founder-admin.json).

