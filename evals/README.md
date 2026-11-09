# Evals

[cases.json](cases.json) holds normal and contrary cases for every skill. A normal case checks the skill does its job. A contrary case checks that it refuses, asks first or stays honest.

## Running them

```
CLAUDE_CONFIG_DIR=/path/to/clean-config python evals/run_paired.py --tmp-base /path/outside/home
```

Each case runs in a fresh temporary project, once with SHOTos installed and once without. Output is graded against `must_contain` and `must_not_contain`, then a person spot-checks a sample. A weekly-brief case uses `unverified_only` to check that specified claim phrases appear under the Unverified heading and nowhere else. Use a Claude config holding only your credentials, and a temporary folder outside your home folder. Otherwise your own instructions leak into both sides.

The paired skill run enables the local read and edit tools used by its fixtures. Shell and connected tools are excluded. An unavailable run is recorded separately from a failed check and makes the command exit with status 2.

Use [the meaning-based judge](judge_paired.py) on raw results JSON files you have produced when phrasing affects a verdict. It pairs outputs from the same source file, case and model. It reports missing verdicts separately and exits with status 2 if any run could not be scored.

The [outcome runner](run_outcomes.py) grades the files and checks left behind by longer tasks. If the runtime or a grader cannot return a score, the runner saves the evidence, marks the run unavailable and exits with status 2. Use only complete pairs for with-and-without comparisons.

## Where the files are

The current tree holds the cases, the outcome fixtures and the runners. It does not hold raw result files. Historical result files sit in the git history. The release tags `v1.12.0` and `v1.13.0` include an `evals/results` folder; `v1.13.1` does not. Check that a tag has the file before you cite it:

```
git ls-tree -r --name-only v1.13.0 -- evals/results
```

A listed file is a record of one past run. Reading it does not repeat the run, and it does not show how your own setup will behave. Nothing in the onboarding guides depends on these files.

## Test fixtures

Secret-shaped strings such as `sk_live_...` in the cases and in any result files are invented test fixtures, not real credentials.
