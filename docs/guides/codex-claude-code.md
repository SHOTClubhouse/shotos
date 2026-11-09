# Use SHOTos in Codex or Claude Code

[See what the six stages give you](../framework.md#try-one-job-across-the-six-stages), then choose one job to try.

Start with one skill in the folder that owns your work. On Windows or Mac, you can copy it with the file manager. Use the installer when you want a pack, shared tools or the full setup. The steps below use Decision Brief. For another job, choose a ZIP from the [first-job guide](../running-it.md#choose-your-first-job), substitute its folder and skill name, and [run its sample](../running-it.md#run-the-sample-from-your-zip).

For a proposal and handoff, add both Contextual Proposal and Success Handoff to the same project. Follow the two short requests in the [fictional worked deal](../../packs/win-the-work/skills/contextual-proposal/worked-deal.md) and keep both outputs with the same account record.

## What needs what

- **Copying one skill folder:** a file manager and a project folder. No installer, Python or connector.
- **A pack, shared tools, role agents or the Stop hook:** the installer, with Python 3.9 or later.
- **Mail, slides, speech, images, video or a browser:** a connector or local program you set up yourself. See [connect your tools](../connect-your-tools.md).

## Copy one skill without a terminal

1. [Download `decision-brief.zip`](https://github.com/SHOTClubhouse/shotos/releases/latest/download/decision-brief.zip). On Windows, right-click and choose **Extract All**. On Mac, double-click the ZIP in Finder.
2. Open the project folder in File Explorer or Finder. Create the folders shown below if they are absent. On Mac, use **Command–Shift–.** to show dot folders. In Finder, **Go to Folder** can open a dot folder once it exists. If Finder refuses to create a dot folder, use the file explorer in your editor to create it, or use the [chat setup](chat-assistants.md).
3. Copy the whole extracted `decision-brief` folder into the right `skills` folder below. On Windows, you can also choose that `skills` folder as the **Extract All** destination. Check that `SKILL.md` sits directly inside `decision-brief`, with its examples and resources alongside it.

| Tool | Final path inside the project |
| --- | --- |
| Codex | `.agents/skills/decision-brief/SKILL.md` |
| Claude Code | `.claude/skills/decision-brief/SKILL.md` |

4. Open the project root in your tool and start a fresh session.
   - **Codex desktop.** For a new project, open the project picker above the composer and choose **New project**. Name it, use **Add folder** under **Source folders** to select the project root, then choose **Create project**. Review any folder trust prompt before continuing. In the new chat, type `$decision` and select **Decision Brief** from the project skill picker.
   - **Claude Code in VS Code.** With the [Claude Code extension](https://code.claude.com/docs/en/vs-code) installed, use **File → Open Folder** to open the project root. Open the Claude Code panel and type `/decision-brief` in its prompt box. Select the project skill there.
5. Ask the selected skill to read `review-cycle.md`, then use the [two retail prompts](chat-assistants.md#run-the-retail-scenario) in order. Check that it cites the installed scenario files and evidence IDs. Compare your result with the [retail check](chat-assistants.md#check-your-first-result).

Use the same installed skill for the [bank and startup exercises](chat-assistants.md#try-a-bank-or-startup-decision). If your ZIP predates a scenario's split input files, open the two linked evidence files from GitHub.

### If the assistant cannot open the sample

Check that the session is open at the project root and that the whole skill folder sits at the path above. Ask it to name the missing file. If the project cannot read that file under its current permissions, [use a chat with files](chat-assistants.md#chatgpt-projects-or-a-claude-chat-using-files). Extract the ZIP and attach the selected skill's instructions, template and sample input. Ask for the result in the reply and keep the worked answer for your review.

For a shared agreement, add the [working agreement](../../templates/AGENTS.md) at the project root or merge its guidance into the existing file with the project owner's review. In Claude Code, reference it from the project's `CLAUDE.md` using `@AGENTS.md`. Manual copying gives you the selected skill and its files. Add other skills from the same release as needed. Keep one copy of each skill per project.

To update a manually copied skill, extract the new release to a separate folder. Back up your old skill folder outside the project and any watched skills folders. Copy the complete new folder into the same installation location, then check it in a fresh session with the same fictional exercise. Review any custom templates or instructions before bringing them across. Keep project records and the working agreement in the project.

[Official Codex skill locations](https://developers.openai.com/codex/skills) · [Claude Code skills](https://code.claude.com/docs/en/skills)

## Install Executive Ops from Claude Code

You can add the whole Executive Ops pack from the Claude Code panel in VS Code.

1. Type `/plugins` to open **Manage plugins**. In **Marketplaces**, add `SHOTClubhouse/shotos`.
2. In **Plugins**, find **shotos-exec-ops** and choose **Install locally** for a first try in this repository.
3. Start a fresh session and select `/shotos-exec-ops:decision-brief`. Run the [two retail prompts](chat-assistants.md#run-the-retail-scenario), using the scenario files that come with the skill.

In a terminal-based Claude Code session, use `/plugin marketplace add SHOTClubhouse/shotos` followed by `/plugin install shotos-exec-ops@shotos`.

Executive Ops adds seven skills and no hooks. The separate Core plugin adds the role agents and the Stop hook. Use the installer if you want Core's project files with the hook as a separate choice. Keep each skill on one setup route in a project. For an exact GitHub release, use its ZIP or source archive.

[VS Code plugin controls](https://code.claude.com/docs/en/vs-code#manage-plugins) · [Claude Code plugin setup](https://code.claude.com/docs/en/discover-plugins)

## Install a pack or the full setup

Download and extract the source archive from the [release](https://github.com/SHOTClubhouse/shotos/releases/latest), or clone the repository. This route needs Git for cloning and Python 3.9 or later to run the installer. From your project folder, replace `PATH_TO_SHOTOS` with the location of the extracted source.

```sh
python "PATH_TO_SHOTOS/install.py" --runtime agents --scope project --pack exec-ops --dry-run
python "PATH_TO_SHOTOS/install.py" --runtime agents --scope project --pack exec-ops
```

Use `python3` if that is how Python runs on your Mac. For Claude Code change the runtime to `claude`. Add `--with-hook` if you have reviewed and want the optional Claude Code Stop hook. Add `--with-agents` if you want its role subagents. For an existing installer-managed Codex project, use the refresh steps below to keep its recorded runtime and skill folder.

Review the dry run before installing. It lists planned changes and writes nothing, so it is a safe way to see what the installer would do. After installing, `python "PATH_TO_SHOTOS/install.py" --status --scope project` reports what is in place.

To see which connectors and local programs your agent can reach, ask it to run the [connect-tools](../../packs/setup/skills/connect-tools/README.md) skill. It makes read-only calls and records the result in `.work/capabilities.md`. If it lists an existing skill in the other Codex folder, review that copy and choose one path before trying again. Confirm skill loading in a fresh session before relying on it. The installer adds the portable tools and records. The manual route is useful when you only need a few skills. [Full pack and role setup](../full-pack.md)

## Refresh an installed setup

Open the project that already has an installer-managed setup. Use the installer from the source revision you want and preview the file changes.

```sh
python "PATH_TO_SHOTOS/install.py" --refresh --scope project --dry-run
python "PATH_TO_SHOTOS/install.py" --refresh --scope project
python "PATH_TO_SHOTOS/install.py" --status --scope project
```

Refresh uses the runtime and packs already recorded. It updates matching managed files and adds new files from those packs. Review anything it reports as kept, including local edits, files removed locally, and files absent from the new source. Existing settings and your working records stay in place. Start a new session and run the same first-job check before relying on the refreshed setup.
