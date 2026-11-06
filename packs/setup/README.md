# setup pack

**Run SHOTos itself: check which tools are connected, keep shared agent instructions in one reviewed repository, right-size the effort for each task, and audit a skill collection.**

The pack looks after the working set-up rather than any one piece of work. It keeps shared instructions and skills in one reviewed repository and reports drift before anything is synced, sets the effort for each task to match its size and risk without changing who decides, and checks that a collection of skills is wired correctly. Each skill reports and proposes; changes follow the owner's yes.

## Who it is for

- People who maintain a shared agent set-up or skill library.
- Team leads setting defaults for how agents are used.
- Solo operators who use agents on more than one machine.

## Skills

| Skill | Step | What it does |
|---|---|---|
| [config-as-code](skills/config-as-code/README.md) | Improve | Keeps a team's instructions and skills in one reviewed repository, installs from it, reports drift before any sync and brings local improvements back through review. |
| [mode-ladder](skills/mode-ladder/README.md) | Brief | Right-sizes effort (Quick, Standard, Thorough or Team of agents) from a task's size, risk and uncertainty; a bigger setting never grants more authority. |
| [skill-audit](skills/skill-audit/README.md) | Check | Checks a skill collection for frontmatter, README, examples, eval cases, links, description collisions and evidence status. Wiring only. |
| [connect-tools](skills/connect-tools/README.md) | Any (run first) | Checks which tools the agent can really reach, tests each with a harmless call, and writes `.work/capabilities.md` with gaps, affected skills and how to connect them. |

## Needs

Read access to the source repository, the runtime folder and the skills folder. Write access only for steps the owner approves. Git is assumed for the source. No connectors are needed.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack setup --dry-run
python ../shotos/install.py --runtime claude --scope project --pack setup
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack to a project that already has SHOTos, run `python ../shotos/install.py --uninstall`, then install again with every pack you want. Files you changed are kept. If a changed file is in the way, the reinstall stops: move it aside (or keep your copy and skip that skill) before you reinstall.

As a Claude Code plugin:

```
/plugin marketplace add SHOTClubhouse/shotos
/plugin install shotos-setup@shotos
```

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The pack follows [docs/controls.md](../../docs/controls.md): the mode ladder applies control 3 (mode contract) and control 11 (context control), and the drift check applies rule 3, Read back the real result. The format the audit checks is in [docs/skill-format.md](../../docs/skill-format.md). Stages are described in [docs/framework.md](../../docs/framework.md).

**Evidence:** Cases written, not yet run. Eval cases are in [evals/packs/setup.json](../../evals/packs/setup.json).
