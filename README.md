# SHOTos

**Give your AI agent a clear job, get work you can check, and hand it over with the evidence.**

SHOTos is an open-source delivery method for people and AI agents. Founders, operators, product teams and engineers can use it for one task or for a change another team needs to run. It gives you a way to agree what good looks like, check the work where it happened and make the next decision with evidence.

**Six-stage edition · 82 skills, 12 optional packs**

[Try it](#try-shotos) · [Follow a worked example](docs/walkthrough.md) · [Find a skill](docs/what-you-can-do.md) · [Choose your setup](docs/running-it.md)

| Start with | What you get |
| --- | --- |
| [A proposal](packs/win-the-work/skills/contextual-proposal/README.md) | A draft grounded in what you can deliver, with a record of claims and commitments to check before sharing |
| [A handoff](packs/customer-success/skills/success-handoff/README.md) | A brief the next person can act on, with the offer, acknowledgement and first action recorded separately |
| [A change across teams](docs/walkthrough.md) | A worked example of testing one change, handing it over and deciding whether to scale |

## Try SHOTos

**On work you already have.** Open the [acceptance card](templates/acceptance.md). Pick one task, name the person who can accept it and write down one check that should fail. Use this prompt in your usual assistant:

> Use this card for the task. Show me the saved result and what you checked. Leave anything you could not verify open for review.

**See the evidence check in action.** From this checkout, with Git and Python 3.9 or later:

```sh
python examples/demo/run_demo.py
```

The demo checks two reports about the same work. The pricing summary exists, the test fails and there is no send receipt. Claim-check flags the unsupported claims and accepts the corrected report. The summary itself still needs review.

![Six stages from Scope to Sustain and Scale. Track can continue to Own, return to Hypothesise, stop or hold for evidence. Scaling starts the next team at Scope.](docs/images/six-stages.svg)

## The six stages

| Stage | What you do | What you hand forward |
|---|---|---|
| **Scope** | Agree the problem, boundaries and how you will measure today | A problem brief and baseline |
| **Hypothesise** | Choose a testable bet and agree what counts as success | A hypothesis, experiment plan and acceptance checks |
| **Operate** | Run a bounded pilot with the people who will use it | The actual result, checks and exceptions |
| **Track** | Compare the outcome with the baseline and make a decision | Evidence and a decision to proceed to Own, pivot, stop or hold |
| **Own** | Give the receiving team the access, runbook and practice to run a full cycle | Evidence the team ran independently and a named lead accepted it |
| **Sustain and Scale** | Maintain the original workflow and start the next team at Scope | A supported rollout, local baselines and a review cadence |

Use the [framework](docs/framework.md) for the stage guides and the [programme record](templates/programme.md) to link the evidence and decisions. An everyday task uses the relevant stage and skill. A programme follows the gates across all six.

## What it looks like

A property manager wants fewer tenants chasing repair updates. Scope counts repeat contacts. Hypothesise sets a target and agrees checks for accurate, private updates. Operate drafts a small batch and flags the case with a missing date. Track compares repeat contacts after an authorised live run. Own asks the operations team to complete a weekly cycle without its builders. Sustain and Scale gives the next office the runbook and asks it to establish its own baseline.

The [Harbourside walkthrough](docs/walkthrough.md) includes data for the draft pilot and labelled scenarios for the later decisions.

## The four rules inside every stage

1. **Stop at the boundaries.** Get authority for actions that send, spend, publish, deploy or affect others.
2. **Agree acceptance first.** Name the owner, expected result and checks.
3. **Read back the real result.** Open the output, run the check or inspect the relevant system.
4. **Claim only what you can show.** Link the evidence and label what still needs verification.

The local [claim-check tool](docs/claims.md) tests supported completion claims against project evidence. A person accepts the work. Runtime and connector settings enforce permissions. [Rules and controls](docs/controls.md) · [Security](SECURITY.md)

## Install

Use Git and Python 3.9 or later. From a separate project directory, replace `PATH_TO_SHOTOS` with this checkout’s path:

```sh
python "PATH_TO_SHOTOS/install.py" --runtime codex --scope project --dry-run
python "PATH_TO_SHOTOS/install.py" --runtime codex --scope project
```

Open a fresh session in that project and ask:

> Use the Scope stage to write a brief for reducing repeat repair enquiries. I have a rough estimate but no measured baseline. Name the owner and propose the first measurement.

For Claude Code, use `--runtime claude` and add `--with-hook` if you want the optional completion check. For Gemini CLI, Antigravity and shared local setups, use the [runtime guide](docs/running-it.md). In a workspace that accepts project instructions, copy the [working agreement](templates/AGENTS.md), the [programme record](templates/programme.md) and the skills you need. The same templates work in a shared document.

## Pick the work you want to do

| Work | Start with |
|---|---|
| Qualify an opportunity or write a proposal | [Win the work](packs/win-the-work/README.md) |
| Run the week or prepare an executive decision | [Executive operations](packs/exec-ops/README.md) |
| Recover onboarding or transfer an account | [Customer success](packs/customer-success/README.md) |
| Define what good looks like before building | [Agree acceptance](skills/agree-acceptance/README.md) |
| Give another team the work and its evidence | [Evidence handoff](skills/evidence-handoff/README.md) |
| Prove a team can run the workflow and prepare the next wave | [Enablement plan](skills/enablement-plan/README.md) and [rollout plan](skills/rollout-plan/README.md) |

Browse the [28 core skills and 54 skills across optional packs](docs/what-you-can-do.md), [documentation](docs/README.md), [templates](templates/) and [examples](examples/README.md). See the [evidence](docs/evidence.md) for recorded checks and their scope.

## What you can use today

The six-stage guide, programme record and task templates work in a shared document or an assistant that can read them. On Windows, fresh Codex CLI and Claude Code projects opened the proposal and handoff skills, wrote the drafts and held the gates for unapproved action in a replay. Claude Code’s Stop hook also caught a deliberate false file claim. [Setup by runtime](docs/running-it.md) · [Validation scope](docs/evidence.md)

Created by Liam McDowell. Code is [MIT](LICENSE). Skills, docs and templates are [CC BY 4.0](LICENSE-docs.md). [Provenance and attribution](PROVENANCE.md)
