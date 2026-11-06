# Security

## Reporting a problem

Please report security issues privately through GitHub's private vulnerability reporting on this repository. If the reporting button is unavailable, email [liam@shotclubhouse.com](mailto:liam@shotclubhouse.com). Do not open a public issue for an unpatched vulnerability. We aim to reply within five working days.

## How SHOTos limits risk

- **Install is a script, not instructions for an agent.** An agent told to follow a document from the internet can be told to do anything. `install.py` only copies files from this repository, shows its plan with `--dry-run`, records what it created and removes exactly that with `--uninstall`. If you ask an agent to install SHOTos, ask it to run the script, and read the dry run first.
- **claim-check never runs a command because a report or a repository asks it to.** Commands run only from your own `~/.shotos/claim-check.json`, a config you name with `--config`, `--allow-command`, or a project config you explicitly trust with `--trust-project-config`. The Stop hook ignores commands in a project's config, so a cloned repository cannot use it to run code.
- **Option injection is refused.** The `base` setting must name a real commit, and anything starting with `-` is rejected.
- **claim-check stays inside the workspace.** It refuses paths outside the folder it was given.
- **Install stays inside the project.** It refuses any path that leads outside the folder through a symlink, before writing anything.
- **Uninstall only removes what install created.** The manifest records paths relative to the project, uninstall refuses anything outside it, and any file you changed after install is kept.
- **No network, no telemetry.** Nothing in this version sends data anywhere.
- **Forks.** Install from this repository or a fork you have read. A modified installer or hook runs with your permissions.
