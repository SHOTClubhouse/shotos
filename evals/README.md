# Evals

[cases.json](cases.json) holds normal and contrary cases for every skill. A normal case checks the skill does its job. A contrary case checks that it refuses, asks first or stays honest.

## Running them

```
CLAUDE_CONFIG_DIR=/path/to/clean-config python evals/run_paired.py --tmp-base /path/outside/home
```

Each case runs in a fresh temporary project, once with SHOTos installed and once without. Output is graded against `must_contain` and `must_not_contain`, then a person spot-checks a sample. Use a Claude config holding only your credentials, and a temporary folder outside your home folder. Otherwise your own instructions leak into both sides.

The paired skill run enables the local read and edit tools used by its fixtures. Shell and connected tools are excluded. An unavailable run is recorded separately from a failed check and makes the command exit with status 2.

Use [the meaning-based judge](judge_paired.py) on raw results JSON files when phrasing affects a verdict. It pairs outputs from the same source file, case and model. It reports missing verdicts separately and exits with status 2 if any run could not be scored.

The [outcome runner](run_outcomes.py) grades the files and checks left behind by longer tasks. If the runtime or a grader cannot return a score, the runner saves the evidence, marks the run unavailable and exits with status 2. Use only complete pairs for with-and-without comparisons.

## Results

Secret-shaped strings such as `sk_live_...` in the cases and results are invented test fixtures, not real credentials.

The first results are in [docs/evidence.md](../docs/evidence.md), with raw outputs in [results/](results/). Codex runs are still to do.
