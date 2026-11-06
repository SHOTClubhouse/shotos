#!/usr/bin/env python3
"""Write each skill's Evidence line from a paired-run results file.

Reads a results JSON written by evals/run_paired.py and replaces the
"**Evidence:**" line in every tested skill's README with what the run showed:
cases passed with and without SHOTos, the model and the date. Skills with no
cases in the run are left alone, so a README never claims a run it did not have.

    python evals/update_evidence.py .work/evals/results-*.judged.json --date "3 November 2026"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^\*\*Evidence:?\*\*:?.*$", re.M)
SECTION = re.compile(r"^## Evidence\n\n((?:.+\n)+)", re.M)  # first paragraph under an "Evidence" heading


def readmes() -> dict:
    found = {p.name: p / "README.md" for p in (REPO / "skills").iterdir() if (p / "README.md").is_file()}
    for pack in (REPO / "packs").iterdir():
        for p in (pack / "skills").iterdir() if (pack / "skills").is_dir() else []:
            if (p / "README.md").is_file():
                found[p.name] = p / "README.md"
    return found


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results", nargs="+", help="one results file per model; judged files (judge_paired.py) are graded by meaning")
    parser.add_argument("--date", required=True, help="the run date as it should appear, e.g. '1 November 2026'")
    args = parser.parse_args(argv)
    results = [r for f in args.results for r in json.loads(Path(f).read_text(encoding="utf-8"))]
    judged = all("judge_pass" in r for r in results if not r.get("error"))
    key = "judge_pass" if judged else "pass"
    paths = readmes()
    changed = 0
    for skill in sorted({r["skill"] for r in results}):
        errored = [r for r in results if r["skill"] == skill and r.get("error")]
        rows = [r for r in results if r["skill"] == skill and not r.get("error") and r.get(key) is not None]
        if not rows:
            print(f"skip {skill}: every run errored")
            continue
        models = sorted({r["model"] for r in rows}, key=["haiku", "sonnet", "opus"].index)

        def tally(condition):
            parts = []
            for m in models:
                mine = [r for r in rows if r["model"] == m and r["condition"] == condition]
                parts.append(f"{m.capitalize()} {sum(bool(r[key]) for r in mine)} of {len(mine)}")
            return ", ".join(parts)

        line = (f"**Evidence:** Tested in a paired run on {args.date}, one run per case, graded "
                + ("by meaning" if judged else "by key phrases")
                + f". Cases passed with SHOTos: {tally('with')}. Without: {tally('without')}"
                + (f" ({len(errored)} run(s) failed to run and are left out)" if errored else "")
                + ". See [evidence]"
                f"({Path('docs/evidence.md').as_posix()}) for how to read this.")
        path = paths.get(skill)
        if not path:
            print(f"skip {skill}: no README found")
            continue
        rel = Path(*([".."] * (len(path.relative_to(REPO).parts) - 1))) / "docs" / "evidence.md"
        line = line.replace("(docs/evidence.md)", f"({rel.as_posix()})")
        text = path.read_text(encoding="utf-8")
        section = SECTION.search(text)
        if LINE.search(text):
            text = LINE.sub(lambda _: line, text, count=1)
        elif section:
            text = text[:section.start(1)] + line.replace("**Evidence:** ", "") + "\n" + text[section.end(1):]
        else:
            text = text.rstrip("\n") + "\n\n" + line + "\n"
        path.write_text(text, encoding="utf-8")
        changed += 1
    print(f"Updated {changed} README(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
