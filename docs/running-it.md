# Where to run SHOTos

SHOTos is files: rules, skills, templates and small Python tools. It runs wherever an agent or assistant can read instructions. Some places give you more of it than others.

## Can I use it with...

| Where | Can you use it? | How | What you get |
|---|---|---|---|
| **Claude app or claude.ai** (no terminal) | Yes | Make skill zips with `python tools/package_skills.py --pack <name>`, then upload each under Settings, Capabilities, Skills. Paste the [AGENTS.md template](../templates/AGENTS.md) into a Project's instructions | The skills and the four rules. Connectors from the app (Google Drive, Gmail, Calendar) give the exec and content skills real data. No claim-check hook |
| **Claude Code** (terminal, VS Code or desktop) | Yes, fully | `python install.py --runtime claude --scope project --with-hook --with-agents --pack <name>` for everything, or the plugin marketplace for the skills only. The plugin route does not install `AGENTS.md` or the `@AGENTS.md` import, so the four rules need the installer or a pasted copy of [AGENTS.md](../templates/AGENTS.md) | With the installer: skills, packs, role agents, rules, claim-check and the Stop hook. With plugins: the skills |
| **ChatGPT** | Partly | Put the [AGENTS.md template](../templates/AGENTS.md) in a Project's or custom GPT's instructions and add the `SKILL.md` files you need as project files. If your ChatGPT plan offers skills, the same zips may upload; check your plan | The method and the rules as instructions. No hook, no role agents |
| **Codex** (CLI or app) | Yes | `python install.py --runtime codex --scope user --pack <name>`, and copy the AGENTS.md template into each project | Skills and rules. Run claim-check yourself on reports |
| **Gemini CLI** | Yes | `python install.py --runtime gemini --scope project --pack <name>`. It puts the skills in `.gemini/skills`, copies `AGENTS.md` and adds `@AGENTS.md` to `GEMINI.md`, so the same four rules load | Skills and rules. Run claim-check yourself. Not live-tested: on 3 November 2026 the Gemini CLI refused to start for a free individual account and pointed to Antigravity |
| **Antigravity** | Yes | `python install.py --runtime antigravity --scope project --pack <name>`. It puts the skills in `.agents/skills`, copies `AGENTS.md` and adds `@AGENTS.md` to `GEMINI.md`. User scope installs to `~/.gemini/config/skills`, the global folder the Antigravity docs give | Skills and rules. Not live-tested: the paths follow the Antigravity docs, and the Antigravity CLI was not installed on the test machine | Skills and rules. Run claim-check yourself |
| **PowerShell** | Yes, as the terminal | PowerShell is where you run the installer and claim-check, and where you start Claude Code, Codex or Gemini CLI. It is not an agent itself | Same as the agent you run in it |
| **macOS or Linux terminal** | Yes | Same commands in Terminal, iTerm or any shell: `python3 install.py ...` | Same as on Windows. The automated tests pass in CI on both; a live agent run has only been done on Windows |
| **No agent at all** | Yes | Print or copy the [templates](../templates/) | The method on paper |

## Recommendation

| If you are | Use |
|---|---|
| Not technical, or new to agents | The **Claude app** with uploaded skills and your Google connectors, or **Claude Code in VS Code** if you are happy to install it |
| Comfortable in a terminal | **Claude Code**: it is the only place where everything SHOTos ships works, including the Stop hook |
| A team that uses several tools, or Codex, Gemini or Antigravity | `--runtime all`, so every tool loads the same rules and skills, and add claim-check to your review |
| Doing work that matters | **Two runtimes:** one leads, a different one reviews. See [multi-agent patterns](multi-agent-patterns.md) |

## One canon for every runtime

Use more than one tool and want them to behave the same? Run `python install.py --runtime all --scope project --pack <name>`. It writes one `AGENTS.md`, which is the single source of the four rules, and points every tool at it:

- **Claude Code** reads `CLAUDE.md`, which gets one line, `@AGENTS.md`.
- **Gemini CLI and Antigravity** read `GEMINI.md`, which gets the same line.
- **Codex** reads `AGENTS.md` itself.

The skills go in `.claude/skills` for Claude Code and in `.agents/skills` for Codex, Gemini CLI and Antigravity, which all read that shared folder. Edit `AGENTS.md` once and every tool follows it. Uninstall removes exactly what the install added. Live runs have only been done on Claude Code so far; the other tools' folders follow their own documentation, and Codex's `.agents/skills` support rests on strings in its binary, not on a session.

## Terminals

The tools need only Python 3.9 or later and git. The Stop hook also needs `sh`, which Git for Windows provides.

- **Windows:** PowerShell or Windows Terminal works for `install.py`, `package_skills.py` and `claim-check`. Install Git for Windows too: the Stop hook runs through `sh`, which comes with it.
- **macOS:** Terminal or iTerm with zsh. Use `python3` if `python` is not found.
- **Linux:** any shell.

## What works where

| Feature | Claude Code | Claude app | Codex | Gemini CLI, Antigravity | ChatGPT |
|---|---|---|---|---|---|
| Skills | Yes | Yes, uploaded as zips | Yes | Yes, from the project folder | As project files or instructions |
| Four rules (`AGENTS.md`) | Yes, loaded automatically | Paste into Project instructions | Yes, read natively | Yes, through `GEMINI.md` or natively | Paste into instructions |
| claim-check by hand | Yes | Run it in a terminal on the report | Yes | Yes | Run it in a terminal on the report |
| claim-check Stop hook | Yes | No | No | No | No |
| Role agents | Yes, `--with-agents` | Paste an agent's body into a Project | Paste as instructions | Paste as instructions | Paste as instructions |
| Review lenses | Yes | Yes | Yes | Yes | Yes |
| Connectors (mail, drive, slides, speech) | Your MCP servers and connectors | The app's connectors | Your MCP servers | Your MCP servers or extensions | ChatGPT's connectors |

To connect slides, speech, images, mail and the browser, see [connect your tools](connect-your-tools.md).

## Permissions to start with

Whatever you use, start with the agent asking before it runs commands or edits outside the project. Then allow specific safe commands, such as your test command, `git status` and `python .shotos/tools/claim_check.py`, as you build trust. Never allow sending, posting, spending, deleting or publishing in advance. See [prerequisites](prerequisites.md) for what each permission means, and the [graduation ladder](../rules/12-graduation.md) for earning more autonomy one task class at a time.

Tested so far: live runs with Claude Code on Windows, and the automated tests in CI on Windows, macOS and Linux. The Claude app upload, Codex, Gemini, Antigravity and ChatGPT, and live runs on macOS and Linux, are on the [roadmap](roadmap.md) for testing.
