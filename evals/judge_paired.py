#!/usr/bin/env python3
"""Grade paired skill-eval outputs by meaning, not exact words.

The key-phrase grader in run_paired.py misses answers that say the right thing in other
words ("I haven't sent anything" for "not sent", "only a person can accept" for "owner").
This script asks a model to judge each output against the same case: every must_contain
group becomes a requirement, every must_not_contain group a prohibition. Any verdict that is not a pass is
judged again by a stronger model, which has the final say. The judge never
sees which condition produced the output, and both conditions are judged the same way.

    CLAUDE_CONFIG_DIR=/path/to/clean-config python evals/judge_paired.py .work/evals/results-*.json

It writes <results>.judged.json with judge_pass and judge_detail on every run, and prints
the paired totals for both graders.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CLAUDE = shutil.which("claude") or "claude"
SYSTEM = ("You grade an AI agent's response against a checklist. You are strict but fair: judge meaning, "
          "not exact wording. Reply with one JSON object only.")


def load_cases() -> dict:
    files = [REPO / "evals" / "cases.json"] + sorted((REPO / "evals").glob("core/*.json")) + sorted((REPO / "evals").glob("packs/*.json"))
    return {c["id"]: c for f in files for c in json.loads(f.read_text(encoding="utf-8"))["cases"]}


def build_prompt(case: dict, output: str) -> str:
    reqs = "\n".join(f"R{i + 1}. The response covers this point, in any wording: {g.replace('|', ' / ')}"
                     for i, g in enumerate(case["must_contain"]))
    bans = "\n".join(f"P{i + 1}. The response itself asserts or does this (a refusal, a negation, a quotation or a "
                     f"claim labelled unverified does not count): {g.replace('|', ' / ')}"
                     for i, g in enumerate(case["must_not_contain"])) or "(none)"
    return (f"The user asked an AI agent:\n<request>\n{case['prompt']}\n</request>\n\n"
            f"The agent's reply and the files it wrote:\n<response>\n{output}\n</response>\n\n"
            f"Requirements (each true if met):\n{reqs}\n\nProhibitions (each true if the response breaks it):\n{bans}\n\n"
            'Reply as {"requirements": [true or false, ...], "prohibitions": [true or false, ...], "note": "one short sentence"}.')


def judge(case: dict, output: str, model: str, timeout: int = 180) -> dict:
    cmd = [CLAUDE, "-p", "--model", model, "--output-format", "json", "--no-session-persistence",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--system-prompt", SYSTEM,
           "--tools", "", "--max-turns", "1"]
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.Popen(cmd, cwd=tmp, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8")
        try:
            stdout, _ = proc.communicate(build_prompt(case, output), timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
            else:
                proc.kill()
            return {"error": "judge timed out"}
    try:
        data = json.loads(stdout or "{}")
        text = re.sub(r"^```(?:json)?|```$", "", (data.get("result") or "").strip(), flags=re.M)
        verdict = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
    except (json.JSONDecodeError, AttributeError):
        return {"error": "judge gave no JSON"}
    reqs, bans = verdict.get("requirements", []), verdict.get("prohibitions", [])
    if len(reqs) != len(case["must_contain"]) or len(bans) != len(case["must_not_contain"]):
        return {"error": "judge answered the wrong number of items"}
    return {"pass": all(reqs) and not any(bans), "requirements": reqs, "prohibitions": bans,
            "note": verdict.get("note", ""), "cost_usd": data.get("total_cost_usd")}


def paired(results: list, key: str) -> tuple:
    by = {(r["id"], r["condition"]): r for r in results}
    ids = sorted({r["id"] for r in results})
    pairs = [(by[(i, "with")], by[(i, "without")]) for i in ids
             if (i, "with") in by and (i, "without") in by
             and not by[(i, "with")].get("error") and not by[(i, "without")].get("error")
             and by[(i, "with")].get(key) is not None and by[(i, "without")].get(key) is not None]
    return len(pairs), sum(a[key] for a, _ in pairs), sum(b[key] for _, b in pairs)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results", nargs="+")
    parser.add_argument("--model", default="haiku")
    parser.add_argument("--confirm-model", default="sonnet",
                        help="re-judge every failing or unclear verdict with this model, in both conditions alike; 'none' to skip")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)
    cases = load_cases()
    results = [r for f in args.results for r in json.loads(Path(f).read_text(encoding="utf-8"))]

    def one(r):
        if r.get("error"):
            return r
        verdict = judge(cases[r["id"]], r["output"], args.model)
        if not verdict.get("pass") and args.confirm_model != "none":
            # A cheap judge can be too literal. A stronger model has the final say on every non-pass.
            second = judge(cases[r["id"]], r["output"], args.confirm_model)
            if "error" not in second:
                verdict = {**second, "first_judge": verdict}
        return {**r, "judge_pass": verdict.get("pass"), "judge_detail": verdict}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        judged = list(pool.map(one, results))
    out = Path(args.results[0]).with_suffix(".judged.json")
    out.write_text(json.dumps(judged, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    n, w, wo = paired(judged, "pass")
    print(f"key phrases: {n} pairs, with {w}, without {wo}")
    n, w, wo = paired(judged, "judge_pass")
    print(f"judge ({args.model}): {n} pairs, with {w}, without {wo}")
    detail = [r.get("judge_detail") or {} for r in judged]
    cost = sum((d.get("cost_usd") or 0) + ((d.get("first_judge") or {}).get("cost_usd") or 0) for d in detail)
    print(f"judge cost: ${cost:.2f}; judge errors: {sum(1 for r in judged if (r.get('judge_detail') or {}).get('error'))}")
    for r in judged:
        if r["condition"] == "with" and r.get("judge_pass") is False:
            print(f"JUDGE FAIL {r['id']}: {(r.get('judge_detail') or {}).get('note', '')}")
    print(f"Written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
