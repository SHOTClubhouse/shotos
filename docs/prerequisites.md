# Prerequisites, connections and choosing tools

## The core

| Need | Why |
|---|---|
| Python 3.9 or later | claim-check, the hook and the installer use only the standard library |
| git | claim-check reads git state to test claims about commits and changes |
| An agent runtime (optional) | Claude Code, Codex or any agent that reads `SKILL.md` folders. The templates also work on paper |

No accounts, API keys or connectors are needed. Nothing is sent over the network.

## Setup checklist by runtime

Run the installer with `--dry-run` first. It lists every file it would copy and changes nothing.

### Claude Code, this project

- [ ] Python 3.9 or later and git are installed, and the project is a git repository.
- [ ] From the project folder, run `python ../shotos/install.py --runtime claude --scope project --dry-run`, read the list, then run it again without `--dry-run`.
- [ ] Add `--with-hook` if you want claim-check to run when the agent tries to finish.
- [ ] Open `AGENTS.md`. If the installer created it, edit the boundaries to match your work. If you already had one, it was not touched.
- [ ] Check that `.work/` is in `.gitignore` and that `.shotos-install.json` exists.
- [ ] Start a task and ask for an acceptance card. Confirm the agent asks for a yes before it starts.

### Claude Code, all projects (user)

- [ ] Run `--runtime claude --scope user`. This installs the skills for every project on this machine.
- [ ] Everything in `.shotos/` is project-scoped, so it is not installed at user scope: the hook, claim-check, the graduation log, the rules, the templates, the connect-your-tools guide and the pack scripts. Skills that mention a `.shotos/` path fall back to the SHOTos repository. Run a project install where you want them.
- [ ] Add your own `AGENTS.md` to each project, because there is no shared one at user scope.

### Codex

- [ ] Run `--runtime codex --scope user`.
- [ ] Check that the installed skill folders appear where your Codex install reads skills.
- [ ] Copy the [AGENTS.md template](../templates/AGENTS.md) into each project by hand.
- [ ] The Stop hook is for Claude Code only. In Codex, run `claim-check` yourself on the agent's report.
- [ ] Codex has not yet been tested with the paired cases. Treat results as unproven until you have checked a few of your own.

### Other agents

- [ ] If your agent reads `.agents/skills`, run `--runtime agents --scope project`.
- [ ] If it reads skills from somewhere else, copy the skills you need from [skills/](../skills/) there by hand.
- [ ] If it reads neither, paste the rules from the [AGENTS.md template](../templates/AGENTS.md) into whatever instruction file it does read.
- [ ] Run `claim-check` by hand on its reports.

### No agent

- [ ] Print or copy the [templates](../templates/): problem, acceptance card and handoff.
- [ ] Fill in the acceptance card before work starts, whoever does it.
- [ ] End each piece of work with the Claims block described in [claims.md](claims.md), and have a person test each line.
- [ ] Python and git are still useful if you want to run `claim-check`, but the method works without them.

To undo any install, run the same command with `--uninstall`. It removes only what it added, and leaves files you changed.

## What each permission means

Agents ask for permission before they act. The names differ between runtimes, but the questions are the same. Grant the narrowest one that does the job.

| Permission | What it lets the agent do | Guidance |
|---|---|---|
| Read files | See your project and what is in it | Safe in a project you trust. Keep secrets out of the folder |
| Write or edit files | Change files in the project | Fine in a git repository, because you can see and undo the change |
| Run commands | Execute programs in your shell | Allow named commands, such as the test command, instead of everything |
| Network access | Fetch pages, call services | Allow when the task needs it, and say which sites |
| Read from a connected service | Read mail, files or records | Needs your credentials. Read-only first |
| Write to a connected service | Create or change records, drafts or files | Drafts and proposed edits first |
| Send, post, spend, delete, publish | Acts outside the project that others see or cannot reverse | Never granted in advance. This is rule 1: the agent asks every time |
| Skip all prompts | Removes the approval step | Keep for a throwaway folder with nothing you mind losing |

The claim-check allow list is separate. It names the commands claim-check may run when it tests a claim, and it is yours to set. A report cannot add to it.

## What packs need

Every pack states its requirements under **Needs** in its README and in each skill's README:

- **Connections:** for example, Google Drive, Docs, Sheets and Slides through an MCP connector, or a mail or calendar connector. You bring your own; SHOTos ships no credentials.
- **Permissions:** the narrowest scope that does the job. Read-only where possible, and drafts rather than sends.
- **Local tools:** for example, Playwright for browser work and screenshots, or local Office files for slides and documents.
- **Models:** which kind of model suits the task, as guidance rather than a requirement.
- **Cost:** a rough token budget, and how to keep it down.

## Connectors and credentials

Packs such as exec-ops, social and automations work best with mail, calendar, document or social connectors. Every one of them follows these habits.

- **Bring your own.** You create the account access, you hold the credential, and you can revoke it. SHOTos ships none and asks for none.
- **Narrowest scope.** Ask for the smallest permission that does the job. If a pack only needs to read one folder, it should not be given the whole drive.
- **Read-only first.** Start with read access. Add write access only after you have seen the agent read correctly.
- **Drafts, not sends.** Anything that reaches another person is prepared as a draft or a suggestion. A named person sends it. This is rule 1.
- **A separate account where you can.** A test or low-privilege account limits the harm of a mistake.
- **Keep credentials out of the project.** Do not put keys in `AGENTS.md`, skills, prompts or committed files. Use the runtime's own secret handling or environment variables.
- **Record what was used.** The handoff note lists which services were touched, so someone can review or revoke later.
- **Review and expire.** Remove access you no longer use.

## Choosing the right tool for the job

This is guidance, not a rule. Check it against your own results.

| Job | Good fit | Why |
|---|---|---|
| Writing, analysis, careful reasoning, long documents | A strong general model in your agent | Quality of judgement matters more than speed |
| Code changes and tests | A coding agent working in the repository | It can run the tests and read the git state |
| Images and visual drafts | An image-capable model, then a person looks at the result | Generated images must be inspected, not trusted |
| Slides and documents others will edit | The format they will edit in (Google Slides or Docs, PowerPoint or Word) | Keep the editable original; export a PDF only for sending |
| Visual explainers and one-off pages | HTML | Easy to share and inspect |
| Web research | An agent with search, plus source links in the output | Every fact keeps its source |
| Anything in a browser | Playwright or a browser-control tool | Real pages, real screenshots, checkable |
| Simple sorting, formatting and extraction | A small, fast model | Same result for a fraction of the cost |

## Choosing a model by job

SHOTos does not name a best model and publishes no benchmark of models. Model lines change often, so match the job to a class of model and test it on your own work.

- **Judgement and ambiguity.** Use the strongest model you have for writing the acceptance card, reviewing a plan, deciding between options and anything touching customers, money or safety.
- **Building and changing.** Use a mid-range model for routine code or document changes where the acceptance checks are clear and a test will catch a mistake.
- **Mechanical work.** Use a small, fast model for sorting, renaming, extraction and formatting, where the answer is easy to check.
- **Independent review.** Where a review matters, use a different model or a different runtime from the one that did the work, and give it the same acceptance card.
- **Start high, then step down.** Run a task type on a strong model first. Once the acceptance checks pass reliably, try a cheaper one on the same checks. Keep the cheaper one only if it passes.
- **Retest when models change.** A new model version is a new experiment. Run your acceptance cards again.

The paired run in the [evidence](evidence.md) used one model on one runtime. Do not assume the same result elsewhere.

## Keeping token use down

- Keep `AGENTS.md` short. It loads on every task.
- Skills load only when the job matches. Keep each `SKILL.md` to one page, with detail in separate files.
- Use a small model for mechanical work and a strong one for judgement.
- Prove a way of working on a few items before running it on hundreds.
- Save large outputs to files, not the conversation.

## Measuring your own cost per accepted task

Cost per generated draft is easy to count and not very useful. The number that matters is what it costs to get one piece of work a person accepts. SHOTos publishes no typical figure for this, because it depends on your tasks, your model and your prices. Measure yours.

1. **Pick a task type.** For example, a weekly report or a small code fix.
2. **Record cost per attempt.** Most runtimes show tokens or cost for a session. Note it for each run, or read it from your provider's usage page.
3. **Count attempts to acceptance.** Include reruns and fixes after review, not only the first try.
4. **Record who accepted it.** If nobody accepted it, it does not count.
5. **Divide.** Count each task once when a named reviewer accepts it. Divide total model and tool spend for all attempts, including abandoned work, by the number of accepted tasks. If none were accepted, report the totals and leave the per-accepted figure undefined.
6. **Report human time separately.** Include review and rework for all attempts, and divide those minutes by the same number of accepted tasks. Combine spend and human time into one cost only if you have an agreed labour rate. If you record elapsed time from request to acceptance, report it separately.
7. **Compare with and without.** Run a few tasks both ways, with acceptance cards and without. SHOTos may raise the cost of each run, as the [paired run](evidence.md) found, so check whether fewer reruns pay for it in your work.
8. **Review monthly.** Change one thing at a time, such as the model, the length of `AGENTS.md` or the acceptance checks, and see whether the number moves.

Keep the [accepted-work ledger](../templates/accepted-work-ledger.csv) beside the acceptance cards in your project. A small honest record beats a large estimated one.

Use one row per attempt and keep the task ID, work type and condition consistent across its attempts. Number attempts from 1. Record `yes` on the final attempt only, with the reviewer role and acceptance evidence. Use `no` or `pending` for other attempts. On the accepted row, record `accepted_elapsed_minutes` as the elapsed time from first request to acceptance, including waiting. Record first-review defects on the first attempt and later defects on the accepted attempt. Enter `0` for a measured zero and leave unknown values blank.

From the SHOTos checkout, run `python tools/summarise_accepted_work.py path/to/ledger.csv` to read results by work type and condition. It reports first-pass acceptance, spend, agent run time, review and rework per accepted result. A separate table shows recorded models and medians for defects, elapsed time and handoff pickup, with the measured sample beside each figure. Use `--matched-only` to include tasks present in every condition. A shared ID is a pairing check. Confirm the inputs, model choices and acceptance criteria before comparing results.

The [fictional proposal ledger](../examples/accepted-work-ledger.csv) gives two accepted tasks out of three in each condition. First-pass acceptance is two of three with the workflow and one of three without it. The cost totals include the third proposal, which was abandoned. Compare tasks with the same scope and acceptance checks before using a result to choose a workflow.
