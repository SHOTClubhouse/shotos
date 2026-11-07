# Releasing

SHOTos uses [semantic versioning](https://semver.org/). From 1.0, a change that alters what a rule or skill asks of the agent is a minor version at least, and the changelog says how.

## Checklist for every release

1. All tests pass for the Python versions in the [CI matrix](.github/workflows/checks.yml): `python -m unittest discover -s tests`.
2. The demo runs: `python examples/demo/run_demo.py`.
3. `claude plugin validate .` passes.
4. Any skill that changed has been re-run through `evals/run_paired.py`, and [docs/evidence.md](docs/evidence.md) is updated, including results that got worse.
5. Versions match in `.claude-plugin/plugin.json`, `CITATION.cff` and `CHANGELOG.md`. Compare each optional pack with the previous release. Bump the version in its `.claude-plugin/plugin.json` when its shipped contents change so hosted Claude Code installs pick up the update. Keep unchanged packs on their existing version. [Claude Code plugin versioning](https://code.claude.com/docs/en/plugins-reference#version)
6. Build the skill ZIPs from the clean release checkout with `python tools/package_skills.py --all-packs --out dist/skills --source-commit COMMIT`. Before building, check that `git status --porcelain --ignored` is empty. Use an empty output directory. Replace `COMMIT` with the full `git rev-parse HEAD` value for the release so the ZIPs link to that source. The tests build and read back every skill ZIP. Check the setup guides and fictional example in the Decision Brief ZIP before attaching the files.
7. Run the outcome evals (`evals/run_outcomes.py`) on at least one model if any rule, core skill or the installer changed, and update [docs/evidence.md](docs/evidence.md).
8. Tag the release `vX.Y.Z`, and paste the changelog section into the GitHub release notes.
9. After publishing, run `python tools/verify_release.py vX.Y.Z --assets dist/skills` from the clean release checkout. It matches each archive's skill instructions to the checkout, downloads every public ZIP to compare SHA-256 hashes, and checks the tagged guides. Open both setup guides from the GitHub release to check their rendered links.
