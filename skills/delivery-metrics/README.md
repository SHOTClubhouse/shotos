# delivery-metrics

**Measure the four DORA delivery keys, plus AI-feature measures, from records you already have, and read them without turning them into targets.**

The agent reads git history, deploy logs and incident notes, computes deployment frequency, lead time for changes, change failure rate and time to restore, and shows the count behind each number. For an AI feature it adds eval pass rate, cost per accepted task, latency and human edit rate. It then offers questions to ask, and states plainly that the numbers describe the system and not people.

It supports the Check step and serves rule 3, Read back the real result, and rule 4, Claim only what you can show. The four keys come from the DORA research programme.

## The problem it solves

A small team at a fictional firm, Northgate Cycles, ships a booking tool every week or so. The owner asks "are we getting faster?" Nobody knows. One developer says releases feel slow; another says they break more often. Without numbers the argument never ends, and with careless numbers (a release count on a wall chart) people start shipping tiny changes to hit it.

The skill takes ten weeks of history, shows 31 deploys, a median lead time, 4 failed deploys and the three incidents behind them, and ends with questions rather than a target.

## When to use it, and when not to

Use it at the Check step, at a regular review, or when a team wants a shared view of delivery. Do not use it for a team with no deploy history, to rank people, or to set targets on a single key.

## Who it is for

- **Engineering or practice lead:** a shared baseline from data the team already holds.
- **Small team lead:** a way to see whether changes help without new tooling.
- **Product owner:** a plain view of speed and stability together.
- **Solo founder:** a quick check that shipping fast is not breaking things.

## How to use it

Ask:

> Compute delivery metrics for the booking tool for the last ten weeks from the git tags, deploy log and incident notes. Include the AI summary feature.

You get one page on [template.md](template.md) with sources, counts and gaps.

## How it connects

- **Feeds:** [evidence-pack](../evidence-pack/README.md) uses these figures. [retrospective](../retrospective/README.md) and [learning-loop](../learning-loop/README.md) use the trends.
- **Related:** [skill-quality-gate](../skill-quality-gate/README.md) covers cost per accepted outcome for a skill; this skill covers it for a feature.

## Needs

Read access to the repository, deploy log, incident notes and (for AI features) eval results and usage export. Nothing beyond the agent otherwise.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 1 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Write down what counts as a deploy and a failure before counting.
- Always show the count: "3 in 41" beats "7 per cent".
- Use trends over eight or more weeks.
- Never put a target on one key. Teams will improve the number, not the work.
- Count rejected and redone AI outputs in the cost per accepted task.

## Limits

- Git history shows merges, not always deploys; check the deploy log.
- Few events means no trend.
- The numbers show where to look. They do not explain why.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/delivery-metrics/input.md) and [output](../../examples/delivery-metrics/output.md).
