# Releasing

SHOTos uses [semantic versioning](https://semver.org/). From 1.0, a change that alters what a rule or skill asks of the agent is a minor version at least, and the changelog says how.

## Checklist for every release

1. All tests pass on Python 3.9 and the latest Python: `python -m unittest discover -s tests`.
2. The demo runs: `python examples/demo/run_demo.py`.
3. `claude plugin validate .` passes.
4. Any skill that changed has been re-run through `evals/run_paired.py`, and [docs/evidence.md](docs/evidence.md) is updated, including results that got worse.
5. Versions match in `.claude-plugin/plugin.json`, `CITATION.cff` and `CHANGELOG.md`.
6. Build the skill zips for the Claude app with `python tools/package_skills.py --all-packs --out dist/skills`, and attach them to the GitHub release.
7. Run the outcome evals (`evals/run_outcomes.py`) on at least one model if any rule, core skill or the installer changed, and update [docs/evidence.md](docs/evidence.md).
8. Tag the release `vX.Y.Z`, and paste the changelog section into the GitHub release notes.
