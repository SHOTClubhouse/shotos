# Role agents

Role agents are Claude Code subagent definitions. Each one describes a responsibility in the work, with the tools it may use and the things it must never do.

## Responsibilities, not headcount

A role is something that must be done, not a person or a separate process. On a small task one agent, or one person, can hold several roles in turn: write the acceptance card, build the slice, then check it. The roles exist so that the work is done on purpose and so that checking is not left to the same eyes that built.

Use a separate agent when you need a separate view. The business analyst should not also be the person who accepts the work. The reviewer who checks a change should not be the engineer who wrote it. For a small, resolved change, one agent doing the whole job with a one-line acceptance check is fine.

## The agents

| Agent | Stage | When to use | Tools | Authority |
|---|---|---|---|---|
| [business-analyst](business-analyst.md) | Scope | A request is vague or "done" is undefined | Read, Grep, Glob, Write | Writes the acceptance card; never builds |
| [ux-designer](ux-designer.md) | Scope, Hypothesise | Before building anything a person reads, clicks or fills in | Read, Grep, Glob, Write | Writes the design note; never builds the final thing |
| [engineer](engineer.md) | Operate | Scope and acceptance are agreed | Read, Grep, Glob, Bash, Write, Edit | Changes the project within the card; prepares, never sends |
| [qa-lead](qa-lead.md) | Track | Work is claimed done, before the owner is asked to accept | Read, Grep, Glob, Bash | Read-only plus running checks; gives a verdict, not acceptance |
| [security-reviewer](security-reviewer.md) | Track | Secrets, access, external connections or personal data are involved | Read, Grep, Glob | Read-only; reports findings |
| [sceptic-reviewer](sceptic-reviewer.md) | Hypothesise, Track | Before committing to a plan, or before a claim goes outside | Read, Grep, Glob | Read-only; recommends, does not decide |
| [data-steward](data-steward.md) | Scope, Track | Any task touching personal data, children's data or special-category data | Read, Grep, Glob | Read-only; flags, does not approve a use |
| [release-manager](release-manager.md) | Own | Reviewed work is ready to leave the project | Read, Grep, Glob, Write | Writes the frozen manifest; never executes without a yes |
| [enablement-coach](enablement-coach.md) | Sustain and Scale | A process works but only one person can run it | Read, Grep, Glob, Write, Edit | Writes runbooks and matrices; never declares a team ready |

Every agent ends its report with a Claims block in the format of [the claims guide](../docs/claims.md) and works inside the [four rules](../docs/controls.md). No agent can accept work. Only a named person accepts.

## Install

For Claude Code, copy the files into your project's `.claude/agents/` folder (or your user-level agents folder to use them everywhere):

```
mkdir -p .claude/agents
cp agents/*.md .claude/agents/
```

Remove `README.md` from the copy if you prefer, since Claude Code reads every markdown file in that folder as an agent. Or use the installer:

```
python install.py --with-agents
```

Then ask for an agent by name, for example: "Use the qa-lead agent to check this against `.work/weekly-report/acceptance.md`."

## Use with other runtimes

The body of each file is plain instructions. For another runtime, paste the body (everything below the frontmatter) into the system prompt, the custom instructions field or the project's agent file. The `tools` line is a Claude Code setting; in another runtime, apply the same limits by hand: read-only agents should be given no write or run access, and no agent should be able to send, spend, delete, deploy or publish on its own.

## Pairing

Pair roles by risk, not by habit. A small internal change needs the engineer and a quick check. A change that touches data or access adds the security reviewer or the data steward. Anything that goes outside the project adds the release manager and the owner's yes. The matching review lenses, which add perspective without taking on a task, are in [lenses](../lenses/README.md).
