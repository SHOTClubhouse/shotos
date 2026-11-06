# Run SHOTos in your project

Start with the runtime your team already uses. The [quickstart](../README.md#install) takes you through the local demo, a preview of what the installer writes and a first task to try.

| Runtime | Setup | What it gives you |
|---|---|---|
| **Claude Code** | `--runtime claude --scope project` | Skills and project rules. Add `--with-hook` for the Stop hook and `--with-agents` for role agents. |
| **Codex** | `--runtime codex --scope project` | Skills in `.codex/skills` and rules in `AGENTS.md`. Run claim-check from a terminal. |
| **Gemini CLI** | `--runtime gemini --scope project` | Skills in `.gemini/skills` and an import of `AGENTS.md` in `GEMINI.md`. Verify skill loading in your runtime before adoption. |
| **Antigravity** | `--runtime antigravity --scope project` | Skills in `.agents/skills` and an import of `AGENTS.md` in `GEMINI.md`. Verify skill loading in your runtime before adoption. |
| **Several local runtimes** | `--runtime all --scope project` | Shared project rules and skills in the relevant runtime folders. Review the install plan for each tool your team uses. |
| **Other compatible local agents** | `--runtime agents --scope project` | The shared `.agents/skills` directory and project rules. |
| **Claude app** | Download individual skill ZIPs from the [release](https://github.com/SHOTClubhouse/shotos/releases/tag/v1.0.0) and upload them in a compatible setup. Add the [project rules](../templates/AGENTS.md) to your Project instructions. | Skills and written rules. |
| **ChatGPT or another assistant** | Add the [project rules](../templates/AGENTS.md) and the relevant skill files to a project or assistant that can read them. | The workflow as instructions and templates. |
| **Manual** | Copy the [templates](../templates/) into the tools you already use. | Briefs, checklists, decision records and handovers. |

Pass these flags to `python /path/to/shotos/install.py` from the project you want to configure. Add `--pack <name>` once per pack, `--list-packs` to see the options and `--dry-run` to preview the plan. Use `--scope user` for a skills-only install where supported. Claude Code's plugin marketplace is another way to install the skills. [Security and installer behaviour](../SECURITY.md)

## Team rollout

1. Pin a release and preview a project install in an isolated checkout. If the project already has an `AGENTS.md`, review the SHOTos rules and merge the ones you want into your existing instructions.
2. Choose one real workflow and a person who can accept the result. Start with read-only access to sources and a draft for review. Check that the agent opens the expected skill in a fresh session.
3. Check the output in the tool where it lives. Use claim-check for supported completion claims and review the quality of the result against your acceptance examples. Your agent runtime and connector settings control access, external actions and approvals.
4. Record the fixes the reviewer requested, their review time and whether the next owner could act. Expand to other workflows when the people doing the work find it useful. [Accepted work ledger](../templates/accepted-work-ledger.csv)

Claude Code has live workflow and Stop hook evidence. Codex has local skill-loading smoke evidence. The release test matrix covers Windows, macOS and Linux on Python 3.9 and 3.13. Validate the agent, connector access and approval path in your own environment before rolling it out. [Validation evidence](evidence.md) · [Connect your tools](connect-your-tools.md) · [Claim-check](claims.md)
