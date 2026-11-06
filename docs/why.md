# Why SHOTos exists

SHOT Clubhouse is a small sports technology company that has to operate with enterprise discipline: clear ownership, proof before claims, governance and repeatable delivery. It has to do this without enterprise headcount. Agents made that possible. They also made it easy to look productive while being wrong.

SHOTos is the way of working that came out of that problem. It is written down so other people can use it.

## The problem

A small team that uses agents well can produce what once took a department. Documents, decks, code, research and messages arrive in hours. What does not arrive on its own is proof.

The failures were rarely bad writing. They were confident reports of work that was half done, never sent, quietly broken or built for the wrong reason. "Done" meant whatever the agent said it meant. Checking all of it by hand would have removed the saving, and not checking it meant paying later, usually in front of a customer.

A company with a large team can absorb this through process and reviewers. A small company cannot. It needs the discipline to be light, specific and mostly automatic.

## Where the lessons came from

Liam McDowell spent many years helping organisations build products, teams and delivery capability before founding SHOT. Three lessons from that work run through SHOTos.

- **Products, not projects.** Value comes from something people use and that keeps improving, not from a plan that finished on time.
- **Teams that own their work.** Outside help is only good if it leaves the team able to carry on without it.
- **Proof over opinion.** Agree what success looks like before starting, then measure against it.

At SHOT those lessons became a five-step work loop, set out in [the work loop guide](framework.md), with four rules inside it. They then met a new problem, and each of the four rules that run inside the steps exists because its absence cost real time.

- **Rule 1, Stop at the boundaries,** because an agent that can send, delete or publish will eventually do so when nobody asked.
- **Rule 2, Agree acceptance first,** because without it "done" is the agent's opinion.
- **Rule 3, Read back the real result,** because a report of success is not success.
- **Rule 4, Claim only what you can show,** because a batch of work that looked finished was not, and fixing it cost more than doing it properly the first time.

## Why it is open

A method kept private is a brochure. Publishing it lets anyone test it, find where it fails and improve it. It also holds SHOT to its own standard in public.

What stays private is SHOT's business: its products, customers and data. The way of working is separate from all three, and nothing in this repository depends on them. The [evidence page](evidence.md) states what has been tested and what has not, including results that were less flattering than hoped. Failure reports are welcome, and [CONTRIBUTING.md](../CONTRIBUTING.md) says how to send one.

## Design choices

**Small.** Version 0.1 has four rules, four skills, one tool, one hook and a handful of templates. One person can use it on day one without a platform team. Every extra rule is another thing to forget.

**Tested.** Where something can be tested, it is. The tool and hook have automated tests, the skills have paired cases that include ones designed to fail, and the results are published with their limits. What has not been tested is listed as not tested.

**Runtime-neutral.** The rules are plain files in a standard folder format. They work with Claude Code and Codex, and with other agents that read the same format. Nothing locks you to one vendor.

**Works on paper.** The templates do not need an agent. If you give work to a person, an agent or a mixture, the problem statement, acceptance card and handoff apply the same way. This is also a test of the idea: a rule that only works inside one tool is a feature, not a way of working.

**Evidence before features.** A new capability ships when there is evidence it helps, not because it is possible. The [roadmap](roadmap.md) lists what is planned and says it will wait for evidence.

**The same rules at every size.** The controls do not change when a team grows. What changes is where they are enforced: an `AGENTS.md` for one person, claim-check in review for a team, claim-check in CI and kept acceptance records for an organisation.

## What SHOTos is not

- **Not a replacement for Scrum or Kanban.** It does not tell you how to run sprints, boards or meetings. If you already have a delivery method that works, SHOTos sits underneath it and covers the parts agents add: who may act, what done means and what has been shown.
- **Not an agent framework.** It does not build, host or run agents. Your agent stays your agent.
- **Not an orchestration platform.** It does not schedule, route or coordinate many agents. It gives each one the same rules.
- **Not a guarantee of quality.** `claim-check` tests that work happened. It cannot judge whether the work is good, and it cannot tell a genuine receipt from one an agent wrote itself. A person still decides. The first paired run showed more consistent working with SHOTos, and no safety difference on the cases tested.

## Where to go next

If you want the four rules in one page, read [the manifesto](../MANIFESTO.md) and [the controls](controls.md). If you want to find your starting point, read the [maturity guide](levels.md) or take the [self-check](self-check.md). If you want to try it, follow the [walkthrough](walkthrough.md).
