# setup pack

**Run SHOTos itself: check which tools are connected, keep shared agent instructions in one reviewed repository, right-size the effort for each task, audit a skill collection, and verify a live release.**

The pack looks after the working set-up rather than any one piece of work. It keeps shared instructions and skills in one reviewed repository and reports drift before anything is synced, sets the effort for each task to match its size and risk without changing who decides, checks that a collection of skills is wired correctly, and confirms that an authorised release is live at the intended revision. Each skill reports and proposes; changes follow the owner's yes.

## Who it is for

- People who maintain a shared agent set-up or skill library.
- Team leads setting defaults for how agents are used.
- Solo operators who use agents on more than one machine.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [config-as-code](skills/config-as-code/README.md) | Sustain and Scale | Keeps a team's instructions and skills in one reviewed repository, installs from it, reports drift before any sync and brings local improvements back through review. |
| [mode-ladder](skills/mode-ladder/README.md) | Scope | Right-sizes effort (Quick, Standard, Thorough or Team of agents) from a task's size, risk and uncertainty; a bigger setting never grants more authority. |
| [skill-audit](skills/skill-audit/README.md) | Track | Checks a skill collection for frontmatter, README, examples, eval cases, links, description collisions and evidence status. Wiring only. |
| [verify-live-release](skills/verify-live-release/README.md) | Track | Verifies that an authorised website, document or download release is publicly available at the intended revision and that key user actions work. |
| [connect-tools](skills/connect-tools/README.md) | Any (run first) | Checks which tools the agent can really reach, tests each with a harmless call, and writes `.work/capabilities.md` with gaps, affected skills and how to connect them. |

## Needs

Read access to the source repository, the runtime folder and the skills folder. Write access only for steps the owner approves. Git is assumed for the source. No connectors are needed, except for verify-live-release, which needs a browser or fetch tool.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack setup --dry-run
git -C ../shotos rev-parse HEAD
python ../shotos/install.py --runtime claude --scope project --pack setup
python ../shotos/install.py --runtime claude --scope project --status
```

Write down the commit that `rev-parse` prints, or the release tag you meant to install, before you install. `--status` reads back the recorded runtime, scope and packs, and lists any installer-owned file that is missing or changed. It does not print the source revision, so the commit you noted is your record of which version you installed. A clean `--status` shows that the files match what the installer wrote, not that the skills work.

Handing the set-up to another runtime (for example from Claude to Codex)? Run the install again with `--runtime codex` or `--runtime agents` from the same checkout and commit, then run `--status` for that runtime. Each runtime keeps its own record, so check each one separately.

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The pack follows [docs/controls.md](../../docs/controls.md): the mode ladder applies control 3 (mode contract) and control 11 (context control), and the drift check applies rule 3, Read back the real result. The format the audit checks is in [docs/skill-format.md](../../docs/skill-format.md). Stages are described in [docs/framework.md](../../docs/framework.md).
