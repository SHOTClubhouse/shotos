---
name: mode-ladder
description: Picks an effort level (Quick, Standard, Thorough, Team of agents) from the work's size, risk and uncertainty. Use when starting work, when risk changes, or when writing a team policy. A bigger level never grants more authority.
---

# Right-size the effort

Stage: Scope. Rules: 1 (stop at the boundaries) and controls 3 (mode contract) and 11 (context control).

Effort should follow the work. A larger setting buys more thinking, more context and more checking; it never buys more permission.

## When not to use this

Skip it for a one-line question. Do not use the level to decide what is allowed; authority comes from the owner and is set per task under control 3.

## How to size a task

Score the task on three questions before choosing a level:

- **Size:** how many steps, files, documents or people does it touch?
- **Risk:** what does a mistake cost, and can it be undone? Personal data, money, legal wording and anything customer-facing raise risk.
- **Uncertainty:** is the goal clear and the method known, or is the problem new?

## The four levels

- **Quick.** Small and fast model, little context, the person's usual tools. For small, well understood, low-risk, reversible work such as renaming, summarising or drafting a short message. Review: one observable check.
- **Standard.** Mid-range model plus the project's context. Acceptance examples first, a short plan, the work, a read-back. For ordinary document, product or code work with a clear goal. Review: the acceptance examples, run against the real result.
- **Thorough.** Strongest available model, the research the task needs, and the context of related decisions. For hard design, difficult trade-offs, unfamiliar domains and choices that are costly to reverse. Review: one bounded independent review (control 7) sized to the risk.
- **Team of agents.** Several independent workers, each with its own task, under a deterministic supervisor (a script or fixed procedure, not another agent's judgement). Set worker count, time limit and cost limit up front. For work that splits into independent parts, such as checking fifty documents. Run a pilot of three units or fewer first (control 9).

## What each level sets

| | Model choice | Context loaded | Review | Parallel work |
|---|---|---|---|---|
| Quick | Small | Minimal | One check | None |
| Standard | Mid-range | Project context | Acceptance examples | None, or one helper |
| Thorough | Strongest | Project plus related decisions | One bounded independent review | Only if the task splits |
| Team of agents | Fits each worker's job | Only what each worker needs | Pilot, then sampled spot-checks | Many, within set limits |

## What never changes with the level

The six stages, the four rules, acceptance first, read-back and the stop boundaries. The owner keeps authority over sending, spending, deleting, deploying and publishing at every level. A bigger setting never grants more authority.

## Using it as team policy

A team lead can adopt this as written. Agree the default level for routine work (usually Quick or Standard), name who may raise it, and set the cost limit above which a person must approve a Team of agents run. Keep the policy in the shared configuration (see config-as-code) so everyone starts from the same default.

## Steps

1. **Describe the task in one line,** including the reader or user and what going wrong would cost.
2. **Pick the lowest level that fits** (use these four names, not the model's own effort settings) the size, risk and uncertainty. Clear, routine, low cost of error and reversible: Quick. Several steps or shared things touched: Standard. Hard, new or costly to reverse: Thorough. Many independent parts: Team of agents, after a pilot.
3. **Say what the level changes:** model class, context, review, helpers, and the expected cost.
4. **Set limits for a Team of agents:** workers, time, spending, who watches, and the stop condition. If asked for no limits, or for agents to decide for themselves when to send, say no: the limits are set per task, the first run is a pilot of three units or fewer, and every send stays with the owner.
5. **State the choice in one line** and ask the owner to confirm or change it.
6. **Re-check at checkpoints.** Move up if the task proves harder or riskier; move down when the hard part is done. Record each change in the task record.

## Output

One line per task: level, reason, what changes, what does not. Use [template.md](template.md).

## Checks

- The level is the lowest one that fits, with a reason tied to size, risk or uncertainty.
- The reply states that authority and the method are unchanged by the level.
- Thorough includes one bounded independent review.
- Team of agents states worker, time and cost limits and a pilot, and the supervisor is deterministic.
