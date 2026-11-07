# mode-ladder

**Right-size the effort: choose Quick, Standard, Thorough or Team of agents from the work's size, risk and uncertainty. A bigger setting never grants more authority.**

This skill picks one of four effort levels for a session or task and says why. Quick is the lean default for small, safe work. Standard adds project context and acceptance examples. Thorough uses a model capable of the agreed checks, relevant research and one bounded independent review. Team of agents runs several independent workers under a deterministic supervisor with set worker, time and cost limits. The choice is stated in one line and can be changed.

It supports the Scope stage. It serves rule 1, Stop at the boundaries, and controls [03, mode-contract](../../../../rules/03-mode-contract.md) and [11, context-control](../../../../rules/11-context-control.md).

## The problem it solves

Harbourside Lettings uses the strongest model and a large context for everything, including renaming a file. The monthly bill is high and answers are slow. A week later the same team uses a small model for a tenancy-law summary and misses a clause. Sizing each task by risk puts effort where it is needed, and the method stays the same either way.

## When to use it, and when not to

Use it at the start of a session or task, when a task's risk or difficulty changes, when a session has grown too big for its job, and when a team lead wants to write down a default.

Skip it for a one-line question. Do not use it to decide whether a task is allowed; authority comes from the owner, not the level.

## Who it is for

- Team leads setting a default for agent sessions.
- Anyone who pays for model use and wants the effort to fit the task.
- Engineers and analysts deciding how much help a task needs.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> I need to rename about forty files and then write a design for moving our booking system to a new provider. What effort level should each part use?

You get a level for each task, the reason, what the level sets (model, context, review, parallel work), what it does not change, and any decision that still needs the owner's confirmation.

To adopt it as team policy, ask: "Write our default effort levels and who may raise them, using the mode-ladder skill."

## How it connects

- **Related:** [config-as-code](../config-as-code/README.md) keeps the agreed default in the shared repository.
- **Rules:** [03, mode-contract](../../../../rules/03-mode-contract.md), [07, independent-review](../../../../rules/07-independent-review.md) and [11, context-control](../../../../rules/11-context-control.md).
- **Team of agents:** only after [09, pilot-before-scale](../../../../rules/09-pilot-before-scale.md) shows a small run works.

## Needs

Nothing beyond the agent. Knowing which models and tools are available helps; if not known, the skill names the level and leaves the model choice to the owner.

**Evidence:** The 3 November version ran once per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 1 of 3, Opus 1 of 3. The current instructions add a case for retaining an accepted result when the required connector is unavailable. See [evidence](../../../../docs/evidence.md) for the evaluation history.

## Tips and common mistakes

- Start at the lowest level that fits and move up when the task shows it needs more.
- Move down again when the hard part is done.
- Treat Team of agents as a pattern for one job, not a way of working.
- Say the level at the top of the task record so a reviewer knows what to expect.

## Limits

- Model names and prices change; the skill describes classes of model, not products.
- A higher level does not make weak acceptance checks good.
- A Team of agents adds cost and coordination; it is not a way around a limit on time or money.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/mode-ladder/input.md) and [output](../../examples/mode-ladder/output.md).
