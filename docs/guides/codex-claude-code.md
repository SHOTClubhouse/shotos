# Use SHOTos in Codex or Claude Code

Start with one skill in the folder that owns your work. On Windows or Mac, you can copy it with the file manager. Use the installer when you want a pack, shared tools or the full setup.

## Copy one skill without a terminal

1. Download `decision-brief.zip` from the [latest GitHub release](https://github.com/SHOTClubhouse/shotos/releases/latest). On Windows, right-click and choose **Extract All**. On Mac, double-click the ZIP in Finder.
2. Open the project folder in File Explorer or Finder. Create the folders shown below if they are absent. On Mac, use **Command–Shift–.** to show dot folders. In Finder, **Go to Folder** can open a dot folder once it exists. If Finder refuses to create a dot folder, use the file explorer in your editor to create it, or use the [chat setup](chat-assistants.md).
3. Copy the whole extracted `decision-brief` folder, including its examples and resources. Check that `SKILL.md` sits directly inside it, without an extra wrapper.

| Tool | Final path inside the project |
| --- | --- |
| Codex | `.agents/skills/decision-brief/SKILL.md` |
| Claude Code | `.claude/skills/decision-brief/SKILL.md` |

4. Reopen the project in your tool and start a fresh chat. In Codex, look in the skills picker or name the skill explicitly. In Claude Code, invoke `/decision-brief`. Ask it to open `review-cycle.md` and work through the retail scenario. Check that it can find the installed example and cite the input it used.

For a shared agreement, add the [working agreement](../../templates/AGENTS.md) at the project root or merge its guidance into the existing file with the project owner's review. In Claude Code, reference it from the project's `CLAUDE.md` using `@AGENTS.md`. Manual copying gives you the selected skill and its files. Add other skills from the same release as needed. Keep one copy of each skill per project.

[Official Codex skill locations](https://developers.openai.com/codex/skills) · [Claude Code skills](https://code.claude.com/docs/en/skills)

## Install a pack or the full setup

Download and extract the source archive from the [release](https://github.com/SHOTClubhouse/shotos/releases/latest), or clone the repository. This route needs Git for cloning and Python 3.9 or later to run the installer. From your project folder, replace `PATH_TO_SHOTOS` with the location of the extracted source.

```sh
python "PATH_TO_SHOTOS/install.py" --runtime codex --scope project --pack exec-ops --dry-run
python "PATH_TO_SHOTOS/install.py" --runtime codex --scope project --pack exec-ops
```

Use `python3` if that is how Python runs on your Mac. For Claude Code change the runtime to `claude`. Add `--with-hook` if you have reviewed and want the optional Claude Code Stop hook. Add `--with-agents` if you want its role subagents. If your Codex client uses the documented shared skill folder only, choose `--runtime agents` for a fresh project install. Avoid installing both runtime variants into the same project.

Review the dry run before installing. Confirm skill loading in a fresh session before relying on it. The installer adds the portable tools and records; the manual route is useful when you only need a few skills. [Full pack and role setup](../full-pack.md)
