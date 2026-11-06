# maturity-check

**A short self-assessment that says where you are on two public maps of AI use, and where in SHOTos to begin.**

The agent asks six questions, places you on Yegge's eight levels of AI-assisted development and the organisation on n8n's five-level AI maturity model, and names the step and first skills that fit. The level wording is in [docs/levels.md](../../docs/levels.md).

It belongs to the Brief step. It serves rule 4, Claim only what you can show, and rule 1, Stop at the boundaries, because it asks what an agent can do without asking you.

## The problem it solves

Millbrook Rovers youth club has one volunteer who runs several agents from the terminal and a committee that has never discussed AI. The volunteer is fast. Nobody else knows what the agents are allowed to do or who checks the output. Without a placement, the club either gives the volunteer a heavy process they do not need, or no process at all.

## What the agent does differently

It places the volunteer high on the first map and the club low on the second, says that the gap is where trouble will come from, and recommends starting at Build with a pilot, an independent review and labelled proof. See [examples/maturity-check/output.md](../../examples/maturity-check/output.md).

## When to use it, and when not to

Use it when someone asks "where are we with AI", when starting SHOTos, or before deciding how much autonomy to give an agent. Skip it when the next step is already clear.

## Who it is for

- **Solo founder or volunteer:** finds a proportionate first step.
- **Team lead:** sees the gap between individual speed and shared habits.
- **Enablement coach:** opens a conversation without a ranking.

## How to use it

> Run a maturity check on me and the club. I run three agents from the terminal. The club has no AI policy.

Answer the questions with an example each where you can.

## How it connects

- **Next:** whichever skills it names, for example [capture-the-problem](../capture-the-problem/README.md) or [pilot-before-scale](../pilot-before-scale/README.md).
- **Background:** [docs/levels.md](../../docs/levels.md) and [docs/prerequisites.md](../../docs/prerequisites.md).

**Needs:** Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 1 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 0 of 2, Sonnet 2 of 2, Opus 0 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Give a real example for each answer. A level claimed without one is marked low confidence.
- Treat a level as a description, not a target. Many small teams do well in the middle.

## Limits

- It rests on self-report and takes a few minutes. It is not an audit.
- The two maps are summaries in our words. Read the originals for their exact definitions.
- One person's answers do not describe a whole organisation.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/maturity-check/input.md) and [output](../../examples/maturity-check/output.md).
