# Guardrail: Productivity

## What it protects

People's time and attention, and the budget. An agent can make a lot of output quickly. If a person must read, check and correct all of it, the time saved in making is lost in reviewing. Productivity here means finished, accepted work per unit of human attention, not volume of text.

## Minimum practice

### 1. Right-size the route

- Write the route line first ([control 1](../01-route-the-work.md)) and use the lightest route that fits the risk. A one-line fix does not need a review packet; a bulk send does.
- Use the sizing section on each control card. Heavy process on small work trains people to skip the process.

### 2. Agree done once

- Agree acceptance before work ([control 5](../05-acceptance-first.md)). The most common source of lost time is rework from an unstated expectation.
- Keep the acceptance short: three to seven checks, one failure case.

### 3. Send people less, with more in it

- Give the owner a short, complete report: the result, the evidence, what was not checked and the decision needed, if any. No summary of the process.
- Only escalate a genuine decision. Absorb routine complexity, and note it in the record.
- Batch questions. Ask all of them at once, with the agent's recommended answer for each.

### 4. Keep context small

- One owning record per task. Pass the record, not the transcript ([control 11](../11-context-control.md)).
- Set a context budget: files to read, size to paste, number of sessions before the record is rewritten.
- Start a fresh session for a new task. Do not carry unrelated threads.

### 5. Reuse accepted work

- Keep accepted outputs, templates and eval sets in the project. Reuse them rather than regenerating.
- When a part has not changed, reuse its previous evidence and check only what changed.
- Script predictable repeated steps, and verify the result of the script; a green run alone proves little.

### 6. Measure what matters

Track a few numbers per task class, as labelled figures (see [control 10](../10-claim-discipline.md)):
- first-pass acceptance rate (the share accepted unedited, from the graduation log);
- review time per output;
- rework rate (how often an accepted output was later changed);
- tokens or spend per accepted output, if relevant.

Do not set targets on volume. Volume rewards the wrong behaviour.

## Checks

- Look at the last ten tasks. How many hours of human time went into review compared with making? If review dominates, check the sizing and the acceptance.
- Count the rework loops per task over a month. Falling is good; flat means acceptance is vague.
- `python .shotos/tools/graduation_log.py status` shows first-pass acceptance per class.
- Pick a task record. Can a new person find the current state and next action in under two minutes?
- Compare token or spend per accepted output over two periods, labelled as literal figures with their source.

## Controls and skills

| Control | How it applies |
|---|---|
| [1: route the work](../01-route-the-work.md) | The lightest route that fits the risk |
| [5: acceptance first](../05-acceptance-first.md) | Less rework |
| [11: context control](../11-context-control.md) | Small, owned context |
| [12: graduation](../12-graduation.md) | Moves routine work out of the person's review queue, with evidence |

Skills: `capture-the-problem` keeps the problem statement short and shared; `agree-acceptance` prevents rework; `evidence-handoff` makes pickup quick.

## Common failure

An office manager asks for a weekly summary and receives eight pages. She reads the first paragraph, skips the rest and stops trusting it. The remedy is to ask for a one-page summary with the three decisions needed, and to record that as the acceptance.
