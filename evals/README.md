# Evals

[cases.json](cases.json) holds normal and contrary cases for every skill. A normal case checks the skill does its job. A contrary case checks that it refuses, asks first or stays honest.

## Running them

```
CLAUDE_CONFIG_DIR=/path/to/clean-config python evals/run_paired.py --tmp-base /path/outside/home
```

Each case runs in a fresh temporary project, once with SHOTos installed and once without. Output is graded against `must_contain` and `must_not_contain`, then a person spot-checks a sample. Use a Claude config holding only your credentials, and a temporary folder outside your home folder. Otherwise your own instructions leak into both sides.

## Results

Secret-shaped strings such as `sk_live_...` in the cases and results are invented test fixtures, not real credentials.

The first results are in [docs/evidence.md](../docs/evidence.md), with raw outputs in [results/](results/). Codex runs are still to do.
