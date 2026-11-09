# Run SHOTos in your project

Choose [Codex or Claude Code on Windows or Mac](guides/codex-claude-code.md), or [ChatGPT or Claude without a terminal](guides/chat-assistants.md). Start with the runtime your team already uses. [Try the method](../README.md#try-shotos) with an acceptance card or run the local demo. The [install guide](../README.md#install) shows how to preview what changes in your project.

## Choose your first job

Download one skill ZIP to try it with a file manager, or use the pack flag with the local installer. Core skills come with the local installer. Try the bundled example before adding your own material.

### Founder starting points

| Job | First skill ZIP | Local pack flag | What to check |
| --- | --- | --- | --- |
| Find the problem before you build | [Capture the Problem](https://github.com/SHOTClubhouse/shotos/releases/latest/download/capture-the-problem.zip) | Core | Repeated questions are a reported problem. The chatbot is a proposal. Enquiry volume and response time stay unmeasured. |
| Qualify an opportunity before pricing | [NUDGE Qualification](https://github.com/SHOTClubhouse/shotos/releases/latest/download/nudge-qualify.zip) | `--pack win-the-work` | Pause pricing until the scope, budget and buyer's authority are clearer. |
| Draft a buyer proposal | [Contextual Proposal](https://github.com/SHOTClubhouse/shotos/releases/latest/download/contextual-proposal.zip) | `--pack win-the-work` | The draft uses £38 per bike, up to 120 bikes. Keep the unsupported repair count and excluded photo in the private review notes. |
| Give an accepted deal to delivery | [Success Handoff](https://github.com/SHOTClubhouse/shotos/releases/latest/download/success-handoff.zip) | `--pack customer-success` | Carry over the signed scope and weekly report. Receiver acceptance and the question about keys stay open. |
| Build a small website | [Build a Small Website](https://github.com/SHOTClubhouse/shotos/releases/latest/download/build-small-website.zip) | `--pack content` | Home leads to weekly sessions. Open Day leads to a first-visit plan. The preview accurately describes how to join. |

### Enterprise starting points

| Job | First skill ZIP | Local pack flag | What to check |
| --- | --- | --- | --- |
| Prepare one leadership decision | [Decision Brief](https://github.com/SHOTClubhouse/shotos/releases/latest/download/decision-brief.zip) | `--pack exec-ops` | The two-round brief separates the recommendation, the director's approval and the later stop decision. |
| Turn several updates into a review agenda | [Weekly Executive Brief](https://github.com/SHOTClubhouse/shotos/releases/latest/download/weekly-exec-brief.zip) | `--pack exec-ops` | The earlier insurance renewal date appears as one decision. Missing portal evidence stays visible. |
| Plan a safe test of a batch change | [Pilot Before Scale](https://github.com/SHOTClubhouse/shotos/releases/latest/download/pilot-before-scale.zip) | Core | Pick a typical row, an awkward date and a blank value. Use an authorised copy for any workbook changes. Keep the full run pending. |
| Review the evidence from a pilot | [Evidence Pack](https://github.com/SHOTClubhouse/shotos/releases/latest/download/evidence-pack.zip) | Core | The review shows that one service target was met and another missed. Staff time stays unmeasured. |
| Train someone to take over a process | [Enablement Plan](https://github.com/SHOTClubhouse/shotos/releases/latest/download/enablement-plan.zip) | Core | The new team has a full Friday cycle to run independently, with a planted fault and a named reviewer. |

### Other starting points

| Job | First skill ZIP | Local pack flag | What to check |
| --- | --- | --- | --- |
| Plan a week of marketing | [Content Calendar](https://github.com/SHOTClubhouse/shotos/releases/latest/download/content-calendar.zip) | `--pack social` | Four slots fit the studio's capacity. Unverified claims and images with missing permission stay out of the plan. |
| Clarify an assignment before starting | [Agree Acceptance](https://github.com/SHOTClubhouse/shotos/releases/latest/download/agree-acceptance.zip) | Core | The card names who can accept the board summary and what to do if the complaints log is incomplete. |
| Turn a product request into testable examples | [Example Mapping](https://github.com/SHOTClubhouse/shotos/releases/latest/download/example-mapping.zip) | Core | The examples show how two interpretations of a sibling discount change the total. The committee owns the unresolved rule. |

### Run the sample from your ZIP

1. For a local project, [copy the selected skill](guides/codex-claude-code.md#copy-one-skill-without-a-terminal) and start a fresh session. For ChatGPT or Claude, [upload the skill or use a chat with files](guides/chat-assistants.md).
2. For Decision Brief, follow the [two-round retail exercise](guides/chat-assistants.md#run-the-retail-scenario). For other skills, ask the installed skill to open `example-input.md`. In a file-based chat, attach `SKILL.md`, `example-input.md` and `template.md` if included. Add any other file the skill needs for the sample. Keep `example-output.md` for your own review.
3. For a sample using `example-input.md`, use the prompt below. Compare the result with the check for your job and open the worked output to see where the two differ.

> Use the selected skill on example-input.md. Work from the supplied fictional sources. Return the first useful draft or preview. If we are using chat with files, put the result in your reply. Identify the sources you actually used. Name any evidence or decision still needed and who owns it. If a required input is missing, say which one. Keep live action pending.

If the local assistant finds the skill but cannot open its sample, [switch to the file route](guides/codex-claude-code.md#if-the-assistant-cannot-open-the-sample) with the same ZIP.

For your next run, replace the fictional input with the smallest set of records approved for your assistant. Keep the skill, expected result and checks the same. Save the accepted result and its sources together, with any open decision named.

If you already used the installer, run `python install.py --status --target <project-folder>` from the SHOTos checkout. It reads the manifest and shows the recorded runtime, scope, packs and any installer-owned files that changed or went missing. For a user-scope install, pass `--scope user` and leave out the project target. The check leaves files alone and covers installer-managed copies.

For a second job, add its skill ZIP or preview the additional pack with `--dry-run` and your existing runtime and scope. The installer adds missing packs. To update an installer-managed setup, use the desired source revision and [preview a refresh](guides/codex-claude-code.md#refresh-an-installed-setup). The release ZIPs match their tag. The default branch can include newer skills and guides. [Installer safeguards](../SECURITY.md)

Use the [full-pack guide](full-pack.md) when you want all 88 skills and the role and review resources. Project installs carry the portable role and lens cards. Use `--with-agents` to register native Claude Code subagents when applicable.

## Set up your runtime

![Try the acceptance card in chat, preview a project install, or run the local demo.](images/setup-first-run.svg)

| Runtime | Setup | What it gives you |
|---|---|---|
| **Claude Code** | `--runtime claude --scope project` | Skills and project rules. Add `--with-hook` for the Stop hook and `--with-agents` for role agents. |
| **Codex** | `--runtime agents --scope project` for a fresh install | Skills in `.agents/skills` and rules in `AGENTS.md`. If your project already uses the `codex` installer route, use refresh to keep its existing `.codex/skills` location. |
| **Gemini CLI** | `--runtime gemini --scope project` | Skills in `.gemini/skills` and an import of `AGENTS.md` in `GEMINI.md`. Verify skill loading in your runtime before adoption. |
| **Antigravity** | `--runtime antigravity --scope project` | Skills in `.agents/skills` and an import of `AGENTS.md` in `GEMINI.md`. Verify skill loading in your runtime before adoption. |
| **Several local runtimes** | `--runtime all --scope project` | Shared project rules and skills in the relevant runtime folders. Review the install plan for each tool your team uses. |
| **Other compatible local agents** | `--runtime agents --scope project` | The shared `.agents/skills` directory and project rules. |
| **Claude app** | Download a skill ZIP from GitHub Releases and [upload it through Customize](guides/chat-assistants.md#claude-with-skills-enabled). Add the [working agreement](../templates/AGENTS.md) to your Project instructions. | Skills and the six-stage working agreement. |
| **ChatGPT** | [Upload a skill](guides/chat-assistants.md#chatgpt-with-skills-enabled) when your workspace supports it, or [use project files](guides/chat-assistants.md#chatgpt-projects-or-a-claude-chat-using-files). | A native skill where enabled, or the workflow as instructions and templates. |
| **Another assistant** | Add the [project rules](../templates/AGENTS.md) and the relevant skill files to a project or assistant that can read them. | The workflow as instructions and templates. |
| **Manual** | Copy the [templates](../templates/) into the tools you already use. | Briefs, checklists, decision records and handovers. |

Pass these flags to `python /path/to/shotos/install.py` from the project you want to configure. Add `--pack <name>` once per pack, `--list-packs` to see the options and `--dry-run` to preview the plan. Use `--scope user` for a skills-only install where supported. Project installs include the programme record at `.shotos/templates/programme.md`. [Security and installer behaviour](../SECURITY.md)

## Use it with a chat assistant or manually

Keep the programme record where your team already works. Give the assistant the working agreement, the current record and the skill for the next decision. You can start with this instruction in any tool that can read the material you give it:

> Read the working agreement and programme record. Identify the current stage and its exit check. Link the evidence you can verify, name who makes the decision and leave any missing approval or measurement open. Continue the authorised work for this stage.

A document, spreadsheet, issue or CRM record can hold the programme. Use links to original evidence and keep access controls on the source.

## Team rollout

1. Preview a project install in an isolated checkout. If the project already has an `AGENTS.md`, the installer adds a line pointing to the installed agreement. Review that line alongside your local instructions.
2. Pick one workflow and start at Scope. Name the sponsor and use the [programme record](../templates/programme.md) to capture the baseline and the next gate. In a fresh session, confirm the agent opens the expected stage skill.
3. Progress through Hypothesise, Operate and Track. Review the work where it lives and use claim-check for supported completion claims. Your runtime and connectors enforce access and action permissions.
4. Use Own to verify one independent cycle with the receiving team. In Sustain and Scale, agree a first wave, local baseline and stop conditions. [Stage guide](framework.md) · [Walkthrough](walkthrough.md)

The local installers and optional Claude Code hook provide the tooling for this edition. Validate skill loading, connector access and approval paths in your environment before rolling out live work. [Connect your tools](connect-your-tools.md) · [Claim-check](claims.md)
