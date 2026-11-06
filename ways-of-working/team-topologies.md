# Team topologies

## What it is

*Team Topologies* by Matthew Skelton and Manuel Pais is a practical model for shaping teams so that work flows. It starts from a simple limit: a team can only hold so much in its head, so the design of the teams should keep the load on each one manageable. It names four team types and three ways teams can work with each other. SHOTos borrows the model to explain who does what in the Own and Improve steps and where agents fit.

## Why it matters with agents in the loop

Agents do not remove the limit on how much a team can understand. They hide it for a while. An agent can touch a large codebase or a long process quickly, and the people who are supposed to be accountable for it may not understand it. Cognitive load is then carried by nobody, until something breaks.

Teams also need a clear answer to "who owns this agent's work?" The answer in this model is simple: **an agent is a tool of a team, not a member of it.** It has no authority, cannot accept work and cannot be held to account. The team is accountable for what its tools do.

## The four team types

### Stream-aligned team

A team aligned to a flow of work from a business domain: a product, a service, a customer path or a user group. It owns delivery end to end and can ship without waiting for other teams. Most teams should be of this type. Stream-aligned teams are who SHOTos hands to in the Hand over step.

### Enabling team

A team of specialists whose job is to help other teams gain a capability, then step back. They coach, pair, build examples and leave. An enabling team that stays forever has become a dependency. Its success is measured by how little it is needed afterwards.

### Complicated-subsystem team

A team that owns a part of the system that needs deep specialist knowledge, such as a pricing engine, a media-processing pipeline or a safety-critical calculation. The rest of the organisation uses it through a clear interface and does not have to understand the inside.

### Platform team

A team that provides internal services other teams use to deliver faster: a deployment pipeline, shared tooling, a data store or a standard way to run agents. A good platform is treated as a product with internal customers, and it is easier to use than to avoid. It reduces the load on stream-aligned teams.

## The three interaction modes

- **Collaboration.** Two teams work closely together for a defined time to discover something new. Expensive, so time-limited.
- **X-as-a-service.** One team provides something the other consumes with little interaction, through a clear interface and documentation. Cheapest when it works.
- **Facilitating.** One team helps another learn or overcome an obstacle. The enabling team's mode.

Name the mode between any two teams, and say when it will change. A long-running collaboration with no end is a sign that the boundary is wrong.

## Cognitive load

Skelton and Pais draw on cognitive load theory to name three kinds: the **intrinsic** load of the task itself, the **extraneous** load from awkward tools and unclear process, and the **germane** load of learning the domain, which is the load you want to spend your effort on. The goal is to cut the extraneous load, since it carries no value, and to keep the team's responsibilities small enough that the germane learning fits.

Signs that a team is overloaded: slow onboarding, a growing backlog of things nobody understands, frequent surprises, heroic individuals, and rules written because people could not hold the system in their heads.

*With agents:* agents can reduce extraneous load by handling routine, mechanical work. They can also add load: more output to review, more tools to configure and more things that can go wrong. Count the review burden when deciding how much to give an agent.

## Where agents sit

- **As tools of a team.** Each agent has a named owning team and a named person who accepts its work.
- **Not as teams.** An agent does not take a seat in the topology. It does not hold a pager, sign off a release or own a service.
- **Within the team's boundary.** The agent's permissions reflect the team's own, never wider. See [control 3, mode contract](../rules/03-mode-contract.md) on capability versus authority.
- **Platform capabilities.** A shared way to run agents, with logging, cost control and standard permissions, is a good job for a platform team.
- **Enabling-team knowledge.** How to brief, review and measure agents is a capability an enabling team can teach, then step back from.

## How SHOTos Hand over and Improve map to enabling teams

The **Hand over** step is the enabling pattern applied to a delivery team. Specialists pair with the receiving stream-aligned team, hand over runbooks, templates and the standard way of doing common tasks, and withdraw when the receiving team has run a full cycle without them. The exit check in the [framework](../docs/framework.md) says exactly that: the team has run at least one full cycle, including a release or reporting period, without the people who built it.

The **Improve** step then asks the enabling team to move on. People who have done the work move to the next team and begin at Brief with that team's own baseline. A community of practice keeps the shared learning. The platform parts, such as pipelines, templates and the agent setup, are offered as a service rather than rebuilt each time.

The mode changes through the steps: collaboration while building, facilitating during Own, then X-as-a-service for anything that stays shared.

## What good looks like

- Every team has a clear purpose and a size it can hold in its head.
- Each interaction between teams has a named mode and an expected end.
- Enabling support finishes; the receiving team is visibly more capable.
- The platform is easier than the alternative.
- Each agent has an owner, and the owner can explain what it did last week.

## Anti-patterns

- **Hand-offs between component teams** for every change, so nothing ships without three queues.
- **The permanent enabling team** that becomes a bottleneck.
- **A platform nobody asked for,** built on assumption.
- **Collaboration forever,** with blurred responsibilities.
- **Agents as invisible team members** whose output nobody owns.
- **Ignoring load.** Adding agent output to a team that cannot review it.

## How it maps to the steps and rules

- **Hand over:** facilitating handover to a stream-aligned team.
- **Improve:** enabling people move on; platform capabilities become service.
- **Rule 1:** authority stays with named people on the owning team.
- **Control 7:** independent review needs a reviewer from outside the author's session, which a team can arrange.
- **Control 12:** graduation is a team's decision about its tool, logged with evidence.

## A short example

Northgate Cycles has a small online shop team (stream-aligned). An external coach team (enabling) spends six weeks with them: pairing on the release process, writing a runbook, setting up an agent to draft product descriptions with a review step. The mode is facilitating. The coach team agrees the exit with the shop team's lead: the shop team must run one release and one month-end report without the coaches. They do, with two questions asked by message. The coaches leave. A small internal platform person then offers the pipeline and the agent setup as a service to a second team, who start at Brief with their own baseline.

## Further reading

- Matthew Skelton and Manuel Pais, *Team Topologies*.
- Nicole Forsgren, Jez Humble and Gene Kim, *Accelerate*.
- Melvin Conway's paper "How Do Committees Invent?", the source of Conway's law.
- Gene Kim and others, *The DevOps Handbook*.
- John Sweller's work on cognitive load theory.
