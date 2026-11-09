# stakeholder-map

**Find out who is affected, who decides and who can block the work, and mark how well you know each fact.**

This skill makes the agent produce a map of people and organisations. Each has a goal, an influence and a stance. Every link carries one of five labels: confirmed, reported, proposed, historic or unresolved. Two records are joined only on two independent identifiers.

It belongs to the Scope stage. It serves rule 4, Claim only what you can show, and rule 1, Stop at the boundaries.

## The problem it solves

Harbourside Lettings wants to move tenant repairs onto a new portal. The operations lead says the landlords' association is "fine with it". A landlord said so to a branch manager, who told the operations lead, who mentioned it to the finance director. The remarks arrive separately, and it looks as if three people agree. It was one conversation, retold. Meanwhile a "J. Okafor" in the repairs log and a "Jide Okafor" on the contractor list are treated as one person because the names are close.

## What the agent does differently

It counts the landlord conversation once, labels it `reported`, and lists the people who passed it on. It keeps the two Okafor records apart until a second identifier matches. The result is in [examples/stakeholder-map/output.md](../../examples/stakeholder-map/output.md).

## When to use it, and when not to

Use it at the start of a change, a project or a deal, and whenever you are about to merge records from different places. Skip it for work that touches only you and one reader.

## Who it is for

- **Project lead or founder:** sees who can block before they do.
- **Account or customer manager:** keeps a clear record of what each contact wants.
- **Anyone using an agent on research:** stops hearsay turning into fact.

## How to use it

> Before we start the portal move, build a stakeholder map from these notes. Label what is confirmed and what is only reported.

Paste or point to the notes. Read the map, correct the labels and decide who to speak to. The agent does not contact anyone.

## How it connects

- **Before:** [capture-the-problem](../capture-the-problem/README.md) says what the work is for.
- **After:** [baseline](../baseline/README.md) records how things are today, and [agree-acceptance](../agree-acceptance/README.md) names the person who accepts the result.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent.

## Tips

- Prefer a role to a full personal profile. Goal and stance are all you need.
- Put the date on every `historic` line. Stance changes.
- Ask "who would be upset to hear about this late?" to find the person who could stop it.

## Limits

- The map is only as good as the notes. It cannot find people nobody mentioned.
- Stance is a judgement. Mark it `unknown` rather than inferring it from tone.
- The skill does not check identity against outside systems.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/stakeholder-map/input.md) and [output](../../examples/stakeholder-map/output.md).
