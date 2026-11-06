#!/usr/bin/env python3
"""Run each eval case with and without SHOTos, grade both, and record the results.

Each run happens in a fresh temporary project. "With" means SHOTos was installed
there by install.py (the core skills, the skill's own pack and AGENTS.md; --all-packs for every pack); "without" means an empty project.
Edits are allowed inside the temporary project only; shell commands are not.

For a fair baseline, run with a Claude config that holds nothing but your
credentials, so your own skills and instructions do not leak into either side:

    CLAUDE_CONFIG_DIR=/path/to/clean-config python evals/run_paired.py --tmp-base /path/outside/home --limit 4

Claude Code also reads CLAUDE.md files from parent folders, so put --tmp-base
outside your home folder. MCP servers are switched off for every run.

Results go to .work/evals/ as JSON and a Markdown table.
"""

from __future__ import annotations

import argparse
import datetime as dt
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
SKIP = {".claude", ".shotos", ".git", ".shotos-install.json", "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".gitignore"}


def project_text(root: Path) -> str:
    parts = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (set(path.relative_to(root).parts) & SKIP):
            try:
                parts.append(f"\n--- {path.name} ---\n" + path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                pass
    return "".join(parts)


NEGATION = re.compile(r"\b(not|no|never|nothing|none|neither|nor|without|unverified|unconfirmed)\b|n't\b")


def is_mention_or_negated(low: str, start: int, end: int) -> bool:
    # A forbidden phrase only counts when the agent uses it. It does not count when it is quoted
    # ('"due to the fact" became "because"') or negated earlier in the same clause ("I haven't
    # sent, scheduled or followed up anything"). Both rules apply to both conditions alike.
    line = low[:start].rsplit("\n", 1)[-1]
    if "[unverified]" in line or line.count('"') % 2 or line.count("“") > line.count("”") or line.count("`") % 2:
        return True
    clause = re.split(r"[.!?;:\n|]", low[max(0, start - 80):start])[-1]
    return bool(NEGATION.search(clause))


def uses(low: str, phrase: str) -> bool:
    return any(not is_mention_or_negated(low, m.start(), m.end()) for m in re.finditer(re.escape(phrase), low))


def grade(text: str, case: dict) -> dict:
    low = text.lower()
    missing = [m for m in case["must_contain"] if not any(alt.lower() in low for alt in m.split("|"))]
    found = [m for m in case["must_not_contain"] if any(uses(low, alt.lower()) for alt in m.split("|"))]
    return {"pass": not missing and not found, "missing": missing, "forbidden_found": found}


def packs_for(skill: str) -> list:
    return [p.parents[2].name for p in (REPO / "packs").glob(f"*/skills/{skill}/SKILL.md")]


STALLS = {"in_a_row": 0, "limit": 6}


def run_one(case: dict, condition: str, model: str, timeout: int, tmp_base: str | None, all_packs: bool = False) -> dict:
    if STALLS["in_a_row"] >= STALLS["limit"]:
        # The runtime has stopped answering (a usage limit, sleep or network loss). Skip rather than wait.
        return {"id": case["id"], "skill": case["skill"], "type": case["type"], "condition": condition, "model": model,
                "pass": False, "missing": [], "forbidden_found": [], "cost_usd": None, "turns": None, "seconds": 0,
                "output": "", "error": f"skipped after {STALLS['limit']} timeouts in a row"}
    with tempfile.TemporaryDirectory(dir=tmp_base) as tmp:
        root = Path(tmp)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        if condition == "with":
            # By default install the core plus the pack the skill belongs to, as the README advises.
            packs = ["--all-packs"] if all_packs else [a for p in packs_for(case["skill"]) for a in ("--pack", p)]
            subprocess.run([sys.executable, str(REPO / "install.py"), "--runtime", "claude", "--scope", "project",
                            *packs, "--target", str(root)], check=True, capture_output=True)
        started = dt.datetime.now()
        try:
            # The prompt goes in on stdin (the Windows claude shim cuts multi-line arguments), and git uses a
            # neutral identity so the operator's name never reaches the agent.
            empty = Path(tempfile.gettempdir()) / "shotos-eval-empty-gitconfig"
            empty.touch()
            env = {**os.environ, "GIT_CONFIG_GLOBAL": str(empty), "GIT_AUTHOR_NAME": "Eval",
                   "GIT_AUTHOR_EMAIL": "eval@example.com", "GIT_COMMITTER_NAME": "Eval",
                   "GIT_COMMITTER_EMAIL": "eval@example.com"}
            proc = subprocess.Popen([shutil.which("claude") or "claude", "-p", "--model", model, "--output-format", "json",
                                     "--permission-mode", "acceptEdits", "--no-session-persistence",
                                     "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}'],
                                    cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, encoding="utf-8", env=env)
            try:
                stdout, _ = proc.communicate(case["prompt"], timeout=timeout)
            except subprocess.TimeoutExpired:
                # On Windows, killing the claude shim alone leaves the real process holding the pipes open.
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
                else:
                    proc.kill()
                raise
            data = json.loads(stdout or "{}")
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            data = {"result": "", "error": str(error)}
        if data.get("is_error") and not data.get("error"):
            data["error"] = "runtime error: " + str(data.get("result", ""))[:200]
        stalled = "timed out" in str(data.get("error") or "")
        STALLS["in_a_row"] = STALLS["in_a_row"] + 1 if stalled else 0
        reply = data.get("result", "") or ""
        text = reply + project_text(root)
        result = grade(text, case)
        return {"id": case["id"], "skill": case["skill"], "type": case["type"], "condition": condition,
                "model": model, **result, "cost_usd": data.get("total_cost_usd"), "turns": data.get("num_turns"),
                "seconds": round((dt.datetime.now() - started).total_seconds(), 1),
                "output": text[:20000], "error": data.get("error")}


def summarise(results: list) -> str:
    rows = ["| Skill | Cases | Pass with SHOTos | Pass without | Cost with (USD) | Cost without (USD) |",
            "|---|---|---|---|---|---|"]
    for skill in sorted({r["skill"] for r in results}):
        mine = [r for r in results if r["skill"] == skill]
        w = [r for r in mine if r["condition"] == "with"]
        wo = [r for r in mine if r["condition"] == "without"]
        cost = lambda rs: round(sum(r["cost_usd"] or 0 for r in rs), 3)
        rows.append(f"| {skill} | {len(w)} | {sum(r['pass'] for r in w)}/{len(w)} | "
                    f"{sum(r['pass'] for r in wo)}/{len(wo)} | {cost(w)} | {cost(wo)} |")
    return "\n".join(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--ids", nargs="*", help="only these case ids")
    parser.add_argument("--limit", type=int, help="first N cases")
    parser.add_argument("--skills", nargs="*", help="only cases for these skills")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--all-packs", action="store_true", help="install every pack in the 'with' condition, not just the skill's own")
    parser.add_argument("--tmp-base", help="folder for the temporary projects; must not sit under any folder holding a CLAUDE.md or .claude/CLAUDE.md, or those instructions leak into both sides")
    args = parser.parse_args(argv)
    files = [REPO / "evals" / "cases.json"] + sorted((REPO / "evals").glob("core/*.json")) + sorted((REPO / "evals").glob("packs/*.json"))
    cases = [c for f in files for c in json.loads(f.read_text(encoding="utf-8"))["cases"]]
    if args.ids:
        cases = [c for c in cases if c["id"] in args.ids]
    if args.skills:
        cases = [c for c in cases if c["skill"] in args.skills]
    if args.limit:
        cases = cases[: args.limit]
    jobs = [(c, cond) for c in cases for cond in ("with", "without")]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda j: run_one(j[0], j[1], args.model, args.timeout, args.tmp_base, args.all_packs), jobs))
    out = REPO / ".work" / "evals"
    out.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (out / f"results-{stamp}.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    table = summarise(results)
    (out / f"summary-{stamp}.md").write_text(table + "\n", encoding="utf-8")
    print(table)
    for r in results:
        if not r["pass"]:
            print(f"FAIL {r['id']} {r['condition']}: missing {r['missing']} forbidden {r['forbidden_found']}"
                  + (f" error {r['error']}" if r.get("error") else ""))
    print(f"\nResults: {out / f'results-{stamp}.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
