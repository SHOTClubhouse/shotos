# SHOTos

**Give your AI agent a clear brief, a way to check its work, and a handover someone can pick up.**

SHOTos is a free, open toolkit for teams that use AI to deliver work. Use the same workflow to draft a customer proposal, recover a stalled onboarding, prepare an executive brief or ship a software change. Start with one task in Claude Code or Codex, then add the skills you use as the work grows.

[Try the demo](#install) · [Find a skill](docs/what-you-can-do.md) · [Adopt it in a team](docs/running-it.md#team-rollout) · [Get v1.0.0](https://github.com/SHOTClubhouse/shotos/releases/tag/v1.0.0)

Created by [Liam McDowell](https://github.com/liammcdow). Published by SHOT Clubhouse Limited.

## What it looks like at work

Your account team needs a proposal for a four-week pilot. Give the agent the discovery notes, approved terms and the decision the customer needs to make. SHOTos gives it a method for turning those inputs into a proposal and a separate record of the claims, open decisions and approvals. Your reviewer can see what the price includes, which promises have evidence and who needs to approve the next step.

The same pattern works when a teammate takes over a project. The handover shows what is finished, where to find the result, which checks ran and who owns the next decision.

| I need to… | Start here | You get |
|---|---|---|
| Win a piece of work | [Win the work](packs/win-the-work/README.md) | LEAP for pipeline decisions, NUDGE for qualification, and a proposal shaped around the customer |
| Get an account unstuck | [Customer success](packs/customer-success/README.md) | An onboarding recovery plan or a handover with ownership and acceptance checks |
| Run the week | [Executive operations](packs/exec-ops/README.md) | Meeting actions, an inbox triage or a decision brief |
| Turn an idea into deliverable work | [Agree acceptance](skills/agree-acceptance/README.md) | A brief, examples of a passing result and a case that should fail |
| Check and hand over a result | [Evidence handoff](skills/evidence-handoff/README.md) | The artefacts, checks, open decisions and next action in one place |

## How it works

![The five steps in the SHOTos work loop: Brief, Build, Check, Hand over and Improve](docs/images/work-loop.svg)

**Brief** the outcome, owner and acceptance checks. **Build** the smallest useful result. **Check** the actual output against the brief. **Hand over** the result, evidence and next action. **Improve** the workflow from what you learn on real work.

Four rules apply throughout: **S**top at permission boundaries, **H**old to agreed acceptance, **O**bserve the result where it lives, and **T**ell people what you can show. The project instructions give the agent those rules. Skills provide steps and templates for particular jobs. The local **claim-check** tool tests specific claims against files, Git, trusted commands or supplied receipts. A person reviews quality and accepts the work. [Framework](docs/framework.md) · [Agent controls](rules/README.md) · [Claim format](docs/claims.md)

## Install

Try it in a fresh project. You need Git and Python 3.9 or later. Use `python3` if that is how Python is installed on your machine.

```sh
git clone --branch v1.0.0 --depth 1 https://github.com/SHOTClubhouse/shotos.git
python shotos/examples/demo/run_demo.py

mkdir shotos-sandbox
cd shotos-sandbox
python ../shotos/install.py --runtime codex --scope project --dry-run
python ../shotos/install.py --runtime codex --scope project
```

The demo shows how claim-check responds when an agent reports passing tests and a committed change that the project cannot confirm. It uses a temporary project and requires no AI account.

Open a new Codex session in `shotos-sandbox` and try:

> Our volunteer rota may take eight hours a week to manage. Help me write a brief with an owner, a first measurement and acceptance checks. Treat eight hours as an estimate.

Look for a clear problem, a way to measure today's baseline and a check a person can use to accept the result.

For **Claude Code**, replace `codex` with `claude` in both installer commands. Add `--with-hook` to both if you want the optional Stop hook to check completion reports. Add `--pack win-the-work` in both commands to try the proposal workflow. [Runtime and installation guide](docs/running-it.md)

## Choose your setup

| Setup | Use it for |
|---|---|
| **Project install** | A shared working agreement, the core skills and any packs you choose. Use `--pack <name>` once per pack. The installer previews changes with `--dry-run` and records what it adds for `--uninstall`. |
| **Claude Code plugins** | Install the skills via `/plugin marketplace add SHOTClubhouse/shotos` and `/plugin install shotos-core@shotos`. Use the project installer when you want the shared agreement or optional hook. |
| **Individual skill ZIPs** | Download a skill from the release for use in a compatible Claude app setup. |
| **Templates** | Copy the brief, decision or handover template into your existing workflow. |

Browse the [28 core skills and 54 pack skills](docs/what-you-can-do.md), [role guides](docs/personas.md), or [templates](templates/). For Gemini CLI, Antigravity and other setups, see the [runtime guide](docs/running-it.md).

## Use it on a team

Pin the release, start with one project and keep approval with the people who own the work. Your runtime and connectors enforce permissions. The optional Claude Code hook checks completion reports, and claim-check checks the evidence types described in its documentation. Run your own acceptance checks on the output before sending, deploying or transferring ownership.

The v1.0.0 source passed CI on Windows, macOS and Linux with Python 3.9 and 3.13. See the [team rollout guide](docs/running-it.md#team-rollout), [security model](SECURITY.md), [release CI](https://github.com/SHOTClubhouse/shotos/actions/runs/42170020345) and [validation evidence](docs/evidence.md).

## Explore and contribute

- Learn the method with the [worked walkthrough](docs/walkthrough.md) or see how it fits alongside [Superpowers, Spec Kit and other tools](docs/compare.md).
- Read the [FAQ](docs/faq.md), [docs index](docs/README.md) and [roadmap](docs/roadmap.md).
- Propose a skill or report a problem through [Contributing](CONTRIBUTING.md) and [Support](SUPPORT.md).
- Code is [MIT](LICENSE). Skills, docs and templates are [CC BY 4.0](LICENSE-docs.md). See [provenance](PROVENANCE.md) and [citation](CITATION.cff).
