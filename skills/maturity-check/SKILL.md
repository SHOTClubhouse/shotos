---
name: maturity-check
description: Places a person on Yegge's eight AI-development levels and a team on n8n's five maturity levels, scoring evidence separately from self-report, then names the SHOTos step and skills to start with. Use when asked "where am I with AI" or before granting autonomy.
---

# Check where you are

Place the person and the organisation on two public maps, say honestly where the evidence is thin, and suggest where to start. The aim is a sensible first step, not a score.

**Step:** Brief (any step may use it). **Rules:** 4 Claim only what you can show; 1 Stop at the boundaries.

Use the wording in `docs/levels.md` in the SHOTos repository. The levels belong to their authors: Yegge's eight levels of AI-assisted development and n8n's five-level AI maturity framework. This skill summarises them and does not replace them.

## When not to use this

Skip it when the person has already said what they want to do and the route is clear. Do not use it to rank people or to judge a team in public. It is a conversation starter.

## Steps

1. **Ask the six questions below, one at a time or all together.** Take answers as given. Ask for an example when an answer is vague.
   1. How do you work with an AI agent today: not at all, in the editor with approvals, from the terminal, or several at once?
   2. How much of the agent's output do you read before it is used?
   3. When did you last find a mistake an agent made, and how?
   4. Is AI use in your organisation tracked, with rules, or personal and unrecorded?
   5. Is there a written definition of done that an agent works to?
   6. What is the riskiest thing an agent can do in your setup without asking you?
2. **Place the person on the eight levels.** Level 1 no AI; 2 an agent in the editor, asking permission; 3 the same, trusted more; 4 watching the agent, not the changes; 5 command line first; 6 several agents in parallel; 7 ten or more by hand; 8 your own orchestrator. Give the level, the answer that supports it and your confidence (high, medium, low). If answers point to two levels, give a range.
3. **Place the organisation on the five levels.** 0 awareness (personal tools, no visibility); 1 experimental (sanctioned pilots); 2 operational (in real workflows, tracked, with human checkpoints); 3 systemic (several agents, continuous governance); 4 AI-native. If only one person answered, say the placement describes their part of the organisation, not the whole.
4. **Name the gap.** The usual trouble is a person high on the first map and an organisation low on the second. Say which side is ahead and what could go wrong.
5. **Recommend where to start.** Use the table below as a default and adjust to the answers. Name the SHOTos step and two or three skills, and explain why they come first.
6. **Say what the check cannot tell you.** It rests on self-report. List which answers had no example behind them.

| Placement | Start at | First skills |
|---|---|---|
| Person at 1 to 3, organisation at 0 | Brief | [capture-the-problem](../capture-the-problem/README.md), [baseline](../baseline/README.md) |
| Person at 4 to 5, organisation at 0 or 1 | Brief | [agree-acceptance](../agree-acceptance/README.md), [route-the-work](../route-the-work/README.md) |
| Person at 6 to 8, organisation at 0 to 2 | Build | [pilot-before-scale](../pilot-before-scale/README.md), [cross-agent-review](../cross-agent-review/README.md), [label-the-proof](../label-the-proof/README.md) |
| Organisation at 2 or above | Track and Own | [report-with-evidence](../report-with-evidence/README.md), [evidence-handoff](../evidence-handoff/README.md) |

## Output

Use [template.md](template.md).

## Checks

- Each placement cites an answer and a confidence.
- The two maps are not collapsed into one number.
- The recommendation names a step and specific skills.
- Gaps in the evidence are listed.
