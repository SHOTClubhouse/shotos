# How SHOTos compares

Several good open projects help agents work in a more disciplined way. They overlap with SHOTos in places and differ in who they serve. You can use more than one: they do not conflict.

| | SHOTos | Superpowers | Spec Kit | BMAD Method |
|---|---|---|---|---|
| **Main audience** | Business and technical teams together: operations, sales, marketing, founders, product and engineering | Software engineers, across 16 coding agents including Claude Code, Codex, Gemini CLI and Antigravity (as stated in its README on 31 October 2026) | Software teams across many coding agents | Software teams that want a simulated team of agent roles |
| **Shape** | A five-step work loop, four rules and twelve controls, core skills and optional packs | A software development method as 15 skills (as stated in its README on 31 October 2026) that trigger automatically: brainstorming, git worktrees, writing and executing plans, subagent-driven development, test-driven development, code review, finishing a branch | A spec-driven flow: constitution, specify, plan, tasks, implement | Role-based agents (analyst, product manager, architect, developer and others) working through planned phases |
| **Non-software work** | First-class: proposals, inbox and daily brief, social, records, grants, customer notices | Not its focus | Not its focus | Not its focus |
| **Checks claims against evidence** | Partly: claim-check tests, after the fact, the files, commands, git state and receipts a report names, and a Stop hook challenges "done"; it cannot prove a claim the report never makes | A verification-before-completion skill and "evidence over claims" as a principle; the agent is asked to check, but no tool tests its claims | Not its focus | Not its focus |
| **External actions** | Drafts by default and a rule to ask for a yes before send, spend, delete, publish or deploy, with frozen approval manifests for high-risk work; these are instructions, and only your agent and tool permission settings can block an action | Not its focus | Not its focus | Not its focus |
| **Works without an agent** | Yes: templates work on paper | No | Partly: the spec documents | Partly: the documents |
| **Published evidence** | Paired outcome runs on Haiku, Sonnet and Opus, with and without SHOTos, including where it made no difference ([evidence](evidence.md)) | An eval harness in a separate repository, as stated in its README on 31 October 2026; no results published in the README | Check the project | Check the project |

Descriptions of other projects summarise their public README files as read on 31 October 2026. Superpowers is at <https://github.com/obra/superpowers>. Check each project directly for its current scope.

## When to use which

- **You are a software team and want stronger engineering habits inside Claude Code:** Superpowers is a strong choice. Add SHOTos for claim-check, the boundaries on external actions and the work loop around the code.
- **You want a spec-first flow for features across many coding agents:** Spec Kit fits. SHOTos's [specification by example](../ways-of-working/specification-by-example.md) and [agree-acceptance](../skills/agree-acceptance/README.md) produce the same kind of acceptance examples, and claim-check tests the agent's report at the end.
- **You want role agents planning a large build:** BMAD fits. SHOTos's [role agents](../agents/README.md) are lighter and are responsibilities rather than a simulated team.
- **Your work is not mostly code, or is a mix:** SHOTos is built for that. The same four rules apply to a board pack, a customer email, a proposal and a pull request.

## What SHOTos adds that the others do not focus on

- **One method for business and technical change**, from the first conversation to the team running it alone.
- **Checks after the fact, not only instruction.** claim-check and the Stop hook test what the agent says against files, commands and git, so "done" can be challenged. They test the claims a report makes; they do not stop an action in advance.
- **Boundaries on the outside world.** The rules tell the agent to ask for a named person's yes before it sends, posts, buys, deletes or publishes. They are instructions; your agent and tool permission settings are what block an action. Autonomy is earned task by task through the [graduation ladder](../rules/12-graduation.md).
- **Packs for the rest of the business**, from a bakery's social posts to a COO's board pack.
