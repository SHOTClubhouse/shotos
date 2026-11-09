# Maturity levels: where you are and what SHOTos unlocks

Most people climb from "AI suggests" to "AI does" faster than they build the habits that make "AI does" safe. SHOTos covers those habits. This guide maps two public frameworks onto the four rules, shows what changes as you climb, and says where each kind of reader usually starts and when to stop.

Two public frameworks describe how far people and organisations have come with AI. SHOTos uses both as maps. It does not replace them, and it does not own them. Read the sources for their exact wording; the summaries below are ours.

- **Practice depth:** Steve Yegge's eight levels of AI-assisted development, from no AI (1) to running a custom orchestrator for many agents (8). [Summary by Augment Code](https://www.augmentcode.com/guides/steve-yegge-8-levels-ai-assisted-development).
- **Organisational reach:** five levels of AI maturity across an organisation, from untracked personal use (0) to an AI-native business (4). [n8n, AI maturity framework](https://blog.n8n.io/ai-maturity-the-5-level-framework/).

Climbing is not the goal for its own sake. Small teams often get most of their return in the middle of both maps.

## The eight levels of AI-assisted development

This map is about one person's practice. In our words:

1. **No AI.** You write everything yourself.
2. **An agent in the editor, asking permission.** The agent proposes changes and you approve every action and review every change.
3. **An agent in the editor, trusted more.** You let it work with fewer approvals, mostly on changes inside one file or a small area.
4. **Watching the agent, not the changes.** The agent works across many files. You follow what it is doing through the conversation instead of reading each change.
5. **Command line first.** The agent works from the terminal, often while you do something else, and comes back with finished work to review.
6. **Several agents in parallel.** You run a few agents at once, each on its own bounded task.
7. **Ten or more agents, run by hand.** You juggle many agents yourself. Duplicated work, drifting specifications and reviews that become rubber stamps are the typical failures.
8. **Your own orchestrator.** You build the machinery (a shared task queue, a coordinator, checkpoints) that assigns and tracks the work of many agents.

The exact boundaries between the middle levels vary by author. What matters here is the direction: each step hands the agent more freedom and gives you less chance to notice a mistake as it happens.

## The five levels of organisational AI maturity

This map is about a whole organisation. In our words:

- **Level 0, awareness.** People use AI tools on personal accounts with no visibility or policy. Sometimes called shadow AI.
- **Level 1, experimental.** Sanctioned pilots run in individual departments. Rules are written after incidents, and the pilots are not connected to the main business systems.
- **Level 2, operational.** AI is part of real workflows across functions, connected to business systems, with usage tracked, measured value and defined human checkpoints.
- **Level 3, systemic.** AI is mission-critical. Several agents coordinate work and governance runs continuously across the organisation.
- **Level 4, AI-native.** AI shapes the strategy and the business model itself. Very few organisations are here.

The first map is how a person works. The second is how far the organisation has made that safe and repeatable. A team can sit high on the first and low on the second, which is the usual cause of trouble: the individuals are fast and nothing else has caught up.

## What the bottleneck becomes

At the early levels, the slow part is producing the work. By the middle levels the agent produces more than you can comfortably read. The bottleneck then moves, and it moves in four ways.

**Specifying.** An agent given a vague request produces a confident answer to the wrong question. The more you delegate, the more the quality of the brief decides the quality of the result. Writing down the problem and what done looks like stops being optional.

**Verifying.** You cannot read everything an agent produces, and a summary of success is not success. Checking has to move from reading every change to testing claims against evidence: the file exists, the test passes, the commit is there, the message was actually sent.

**Governing.** Once several agents or several teams are involved, the questions change. Who owns this output? What may an agent do without asking? Where is the record? These are not technical questions, and tools alone do not answer them.

**Cost.** Autonomy spends tokens and attention. A long unattended run, or several in parallel, costs more than a short supervised one. Unchecked work costs more again when it has to be redone. Count the cost of accepted work, not generated work. The [prerequisites guide](prerequisites.md) shows how to measure it.

SHOTos is aimed at exactly these four pressures, and mostly at the three that people forget: specifying, verifying and governing.

## Which rule or asset helps at each step

| Step you are taking | What it needs | Rule | SHOTos asset |
|---|---|---|---|
| From approving every action to reading results | Knowing what "right" looks like before you start | Rule 2, Agree acceptance first | `agree-acceptance` skill, [acceptance card](../templates/acceptance.md) |
| From unclear requests to clear ones | The problem written down apart from the solution | Rule 2, Agree acceptance first | `capture-the-problem` skill, [problem template](../templates/problem.md) |
| From watching the agent to leaving it working | A report you can trust when you come back | Rules 3 and 4, Read back the real result and Claim only what you can show | `report-with-evidence` skill, `claim-check`, the Stop hook |
| From trusting to bounded freedom | Clear limits the agent cannot talk its way past | Rule 1, Stop at the boundaries | Boundaries in [AGENTS.md](../templates/AGENTS.md) |
| From one agent to several | Every agent following the same written rules, and bad output caught early | Rules 1, 2 and 4 together | One shared `AGENTS.md`, claim-check in review |
| From one session to the next, or one person to the next | Work that can be picked up without asking anyone | Rule 4, Claim only what you can show | `evidence-handoff` skill, [handoff template](../templates/handoff.md) |
| From personal use to organisational use | Named owners, human checkpoints, an audit trail | All four, as a baseline policy | [The four rules](controls.md), acceptance cards kept with the work |
| From pilots to continuous governance | Quality checks that run without a person asking | Rules 3 and 4 | claim-check in CI today; wider controls are on the [roadmap](roadmap.md) |

The rules are the controls inside every stage. How a team or organisation climbs is the job of the stages: Track records whether to move to Own, pivot, stop or hold for evidence. The receiving team demonstrates ownership before the sponsor authorises rollout. See [the stage guide](framework.md).

If a row has no asset yet, the roadmap says so. SHOTos does not claim to cover levels it has not been tested at.

## By persona

Each persona below shows a typical start, a sensible target, how SHOTos helps, the signs you have arrived and a reason to stop. For fuller descriptions of each person, see [personas](personas.md). Starting points are typical patterns, not measurements; yours may differ.

### Solo founder

**Typical start.** An agent in the editor or the terminal, with the founder reviewing most changes and tired of it. Roughly levels 3 to 5 on the practice map, and level 0 or 1 on the organisational one, because nobody else is involved.

**Target.** Agents working alone on bounded tasks while you do something else, with reports that hold up when you return. Roughly levels 5 to 6.

**How SHOTos gets you there.**
- Agree a short acceptance card before any task that matters. You are the only reviewer, so the card is also your memory.
- Install the core skills. In Claude Code, you can add the Stop hook. The hook runs `claim-check` when the agent tries to finish and sends it back if a claim fails.
- Put the boundaries in `AGENTS.md` so the agent asks before it sends, spends, deletes or publishes.

**Signs you have arrived.**
- You leave a task running and trust the report enough to act on it.
- When a report is wrong, the check catches it before you do.
- You can say, for any piece of work, whether it is installed, executed or accepted.

**Why not climb further.** Running many agents in parallel or building an orchestrator adds supervision work, and for one person that work is the thing you lack. A founder with one dependable agent and a clear card usually gets more done than one juggling six.

### Small team lead

**Typical start.** Every person has their own way of working with agents, their own prompts and their own sense of what "done" means. A mix of levels 3 to 6, and organisational level 1 or 2.

**Target.** One shared way of working in every repository, and reviews that start from evidence instead of a re-read of everything.

**How SHOTos gets you there.**
- Put the same `AGENTS.md` in every repository, so every agent follows the same four rules.
- Agree which commands `claim-check` may run, and run it on agent reports during review.
- Use the handoff note when work moves between people, so the next person starts from the state, not a guess.

**Signs you have arrived.**
- A new team member can read one file and know what agents may and may not do.
- Review comments are about the work, not about whether it was done.
- Two people's agent reports look alike and can be compared.

**Why not climb further.** A team of five rarely needs an orchestration layer. Agreeing the rules and keeping them are the hard parts, and they are cheaper than new machinery.

### Product owner or analyst

**Typical start.** Not running coding agents at all, or only using chat for drafting. The work that arrives from the team is "done" when someone says so, and the problem is sometimes clear only after the build.

**Target.** Writing the problem and the acceptance that lets the team's agents run safely. This is a shift in role more than a climb up the practice map.

**How SHOTos gets you there.**
- Use `capture-the-problem` to turn a request into a problem statement with a cheap first test.
- Use `agree-acceptance` to write checks, including one that should fail, before work starts.
- Keep the acceptance card with the work so accepted means something a person can point to.

**Signs you have arrived.**
- Work lands right first time more often, and rework is traceable to a missing check, not a mystery.
- Disagreements about "done" are settled by reading the card.
- You can say who accepted what.

**Why not climb further.** You do not need to run agents yourself to add most of the value. Clear problems and clear acceptance are your contribution.

### Engineering or practice lead

**Typical start.** Responsible for how a group builds. Individuals are fast with agents, and there are loose conventions but no common standard. Practice levels vary widely; organisational level 1 or 2.

**Target.** A repeatable baseline across teams: shared rules, evidence-based review, and a record of what agents did.

**How SHOTos gets you there.**
- Adopt the four rules as the baseline agent policy and publish it in the repositories.
- Run `claim-check` in CI and review, with an allow list you control.
- Keep acceptance cards and handoffs with the work as the trail an audit would ask for.

**Signs you have arrived.**
- The baseline holds across teams without you chasing it.
- Incidents are traced to a missing rule or check, and the rule is then added.
- Review time goes into judgement, not into finding out what happened.

**Why not climb further.** Add controls when an incident or a measured gap calls for one. The [roadmap](roadmap.md) lists later controls, and each ships only with evidence.

### Business unit leader or enterprise sponsor

**Typical start.** Scattered pilots, often with no named owner and no proof they work. Organisational level 1, sometimes called pilot purgatory.

**Target.** Everyday use in a few value streams, governed, with owners and a trail: organisational level 2 in those streams. Level 3 is for a later stage, one value stream at a time, not the whole business at once.

**How SHOTos gets you there.**
- Use the four rules as a baseline policy that a governance function can read in a few minutes.
- Require a named owner and an acceptance record for each agent workflow you sponsor.
- Start with one team, show the record, then widen.

**Signs you have arrived.**
- You can name the owner of each agent workflow.
- You can show what was checked and who accepted it.
- The cost of accepted work is known for the workflows you run.

**Why not climb further.** Organisation-wide AI-native operation is a large change with its own risks. The sensible aim is a handful of well-owned workflows with evidence behind them. The enterprise bridge to external standards is on the roadmap, and nothing here is a claim of compliance.

### Enablement coach

**Typical start.** Asked to help a team or a department "get better at AI", usually with enthusiasm in some people and caution in others.

**Target.** Teams that can run the method without you, which is the point of enablement.

**How SHOTos gets you there.**
- Use the two-minute [self-check](self-check.md) to place a team and name its next step.
- Run the [walkthrough](walkthrough.md) with a team on their own material.
- Leave behind the templates and the `AGENTS.md`, so the practice stays after you do.

**Signs you have arrived.**
- The team runs acceptance cards and handoffs without prompting.
- They can explain why each rule exists.
- They ask you for fewer things each month.

**Why not climb further.** Your measure is capability left behind, not the level a team reaches. A team that stays at a steady middle level with good habits is a success.

### The agent itself

**Typical start.** An agent reads `AGENTS.md` and the skills at the start of a task, and has whatever autonomy the runtime grants. It is the persona whose level is set by others.

**Target.** To work inside the four rules without being reminded, and to report in a way a person or a tool can check.

**How SHOTos gets there.**
- Stop and ask at the boundaries, whatever the runtime would allow.
- Work to the acceptance card and observe the real result before reporting.
- End with a Claims block, mark gaps `[unverified]` and leave acceptance to a person.

**Signs it has arrived.** Its reports pass `claim-check`, its gaps are labelled and it asks when a boundary is near.

**Why not climb further.** More freedom without more evidence only makes mistakes larger. The agent earns freedom one task type at a time, through a record of accepted work.

## Teams and organisations moving together

Individuals climb quickly. Organisations do not, and they should not be pushed to. Three habits help.

**One team at a time.** Pick one team with a real task, apply the rules, and keep the record. Show other teams the result. Copying a working example is faster and safer than announcing a policy.

**Owner before scale.** Every workflow needs a named person who answers for it before it runs more widely. If nobody will own it, it does not scale. The manifesto says the same: if nobody will run it, maintain it or answer for it, it does not ship.

**Match the controls to the risk.** A one-line fix needs one check. Anything touching customers, money, safety or children needs more, and independent review. Do not apply the heaviest process everywhere because the lightest is uncomfortable.

When the first team's record is solid, the next team adopts the same four rules and the same templates. The controls do not change with size. What changes is where they are enforced.

## A note on starting points

The starting points in this guide are typical patterns, not measurements. We have not surveyed anyone, and we publish no figures for how many people sit at which level. Both source frameworks are also simplifications; real teams straddle levels, and a person can be at level 6 on one task and level 3 on another.

Use the maps to ask a better question than "how advanced are we?". Ask what the next step needs, and whether the rule that supports it is already in place. If you want a quick read, take the [self-check](self-check.md).
