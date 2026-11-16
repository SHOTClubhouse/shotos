# Releasing

SHOTos uses [semantic versioning](https://semver.org/). From 1.0, a change that alters what a rule or skill asks of the agent is a minor version at least, and the changelog says how.

SHOTos does not use GitHub Actions. Every check runs on a maintainer's machine through the local gate, and a script cuts the release.

## Who may cut a release

- **Patch or minor:** any maintainer, when the gate card for the release commit is GO and an independent review of the changes is clean. The reviewer is someone, or an agent, that did not write the changes.
- **Major:** only the owner. A change that breaks the four controls, the Claims block format or the claim-check exit codes is a major release ([Governance](GOVERNANCE.md)). The release script refuses it and says it needs the owner.

## Cut a release

1. Start from `main` as it is on GitHub, with nothing uncommitted: `git switch main`, `git pull`.
2. Set `SHOTOS_DENYLIST` to the private denylist file. Without it the gate cannot check for private terms and its card cannot be used for a release.
3. Install the test dependency once: `python -m pip install PyYAML==6.0.3`.
4. Run the full gate: `python tools/local_gate.py --release`. It writes a card to `.work/gate/` and prints it. Read the "What a person should look at" list. Fix anything marked FAIL and run it again.
5. If skills changed, check them against the normal requests and failure cases they are meant to handle, using the [skill quality gate](skills/skill-quality-gate/SKILL.md). If a rule, core skill or the installer changed, run the outcome evals (`evals/run_outcomes.py`) on at least one model. Keep both records with the review.
6. See what the release would do: `python tools/release.py`. This is a dry run. It checks the card, picks the version, shows the changelog section and rehearses the ZIP build. Nothing changes.
7. To write the changelog yourself, put the text in a file and pass `--notes FILE`. Otherwise each commit subject since the last release becomes one line. Pass `--minor` to make a release minor when the script would choose a patch.
8. Publish: `python tools/release.py --publish --review "who reviewed it, or a link"`.

## What the release script does

The dry run stops after the first three steps. `--publish` does them all.

1. **Checks the card.** The card for HEAD must say GO and "For release: yes". A fast card, a card made without the denylist or a card made with uncommitted changes is not enough.
2. **Picks the version.** A change to what a rule or skill asks of the agent (rules, agents, the Stop hook, templates, or any skill file other than its README) is a minor release. Anything else is a patch. Each optional pack with shipped changes gets a new version too, so hosted Claude Code installs pick up the update. Unchanged packs keep their version. [Claude Code plugin versioning](https://code.claude.com/docs/en/plugins-reference#version)
3. **Refuses a major.** It stops if a rule in [the four rules](docs/controls.md) was renamed or removed, if the promise in [Governance](GOVERNANCE.md) changed, if claim-check judges a standard Claims block differently from the last release or changes its exit codes, or if a commit message starts with `BREAKING:`.
4. **Commits the release.** It updates `.claude-plugin/plugin.json`, `CITATION.cff`, `CHANGELOG.md` and the changed pack manifests, then commits them as "Release SHOTos vX.Y.Z" with the reviewer named in the message.
5. **Checks the commit.** It runs `python tools/check_release_versions.py PREVIOUS_TAG` and scans the release commit for private terms.
6. **Builds the ZIPs.** It runs `python tools/package_skills.py --all-packs --out dist/vX.Y.Z --source-commit COMMIT` against the release commit, so the ZIPs link to that source. It stops first if ignored files sit in a folder the ZIPs are built from. It also runs `claude plugin validate .` when the Claude Code CLI is installed.
7. **Publishes.** It pushes `main`, tags the release `vX.Y.Z`, and creates the GitHub release with the changelog section as its notes and every ZIP attached, using the `gh` CLI.
8. **Reads it back.** It runs `python tools/verify_release.py vX.Y.Z --assets dist/vX.Y.Z`. That matches each archive's skill instructions to the checkout, downloads every public ZIP to compare SHA-256 hashes, and checks the tagged guides.

If a step fails, fix the cause and run the same command again. The script carries on from the release commit it already made. After publishing, open both setup guides from the GitHub release to check their rendered links.

For the first stable release after v1.7.0, also run the version check against v1.6.0. Some optional packs changed between those releases while keeping their marketplace version.
