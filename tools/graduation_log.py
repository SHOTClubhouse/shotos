#!/usr/bin/env python3
"""graduation-log: record how often a task class is accepted unedited, and
work out how much autonomy that class has earned.

Control 12 (graduation) in one tool. Each time a person reviews the agent's
work on a class of task, record the outcome:

    python tools/graduation_log.py record --class weekly-summary --outcome accepted-unedited --by "Sam Rivers"
    python tools/graduation_log.py record --class supplier-email --outcome rejected --by "Sam Rivers" --note "wrong tone" --high-risk
    python tools/graduation_log.py status
    python tools/graduation_log.py promote --class supplier-email --to 2 --by "Sam Rivers"

Rungs:

    1  draft only: a person reviews every output
    2  auto-run and notify: needs at least 95% accepted unedited over at least 50 samples
    3  silent, exceptions only: needs at least 200 samples in total and at least
       98% accepted unedited over the most recent window

Every record names the person who accepted or rejected the work (--by). A record
with no name is not counted, so status only reflects reviews a person owned.

The rate is measured over the most recent window (default 50 samples), so a
class that starts needing edits drops a rung. A class marked high-risk stays at
rung 1 until a named person records a promotion (promotion has no effect on a class
that is not high-risk, and the tool refuses it), and a promotion is only a
ceiling: the class still has to hold the rate to keep the rung.

The log is append-only JSONL, one event per line, at .work/graduation-log.jsonl
unless --log says otherwise. Standard library only. The tool never runs, sends
or changes anything outside its own log.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTCOMES = ("accepted-unedited", "accepted-edited", "rejected")
DEFAULT_LOG = ".work/graduation-log.jsonl"
DEFAULTS = {
    "window": 50,
    "rung2_rate": 0.95,
    "rung2_samples": 50,
    "rung3_rate": 0.98,
    "rung3_samples": 200,
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_event(log: Path, event: dict) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def read_events(log: Path) -> list:
    if not log.exists():
        return []
    events = []
    for number, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            raise SystemExit(f"{log}: line {number} is not valid JSON; fix or remove that line")
    return events


def evaluate(events: list, only_class=None, **overrides) -> list:
    """Work out samples, rate, rung and reason for each task class."""
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    classes = {}
    for event in events:
        name = event.get("class")
        if not name or (only_class and name != only_class):
            continue
        entry = classes.setdefault(name, {"outcomes": [], "high_risk": False, "promotion": None})
        if event.get("type") == "record":
            if event.get("high_risk"):
                entry["high_risk"] = True
            if str(event.get("by") or "").strip():  # unattributed records do not count
                entry["outcomes"].append(event.get("outcome"))
        elif event.get("type") == "promote":
            entry["promotion"] = event
    results = []
    for name in sorted(classes):
        entry = classes[name]
        outcomes = entry["outcomes"]
        recent = outcomes[-cfg["window"]:]
        samples = len(outcomes)
        rate = (recent.count("accepted-unedited") / len(recent)) if recent else 0.0
        if samples >= cfg["rung3_samples"] and rate >= cfg["rung3_rate"]:
            earned = 3
            why = (f"{rate:.0%} unedited over the last {len(recent)} of {samples} samples "
                   f"meets the rung 3 bar ({cfg['rung3_rate']:.0%} over {cfg['rung3_samples']}+)")
        elif samples >= cfg["rung2_samples"] and rate >= cfg["rung2_rate"]:
            earned = 2
            why = (f"{rate:.0%} unedited over the last {len(recent)} of {samples} samples "
                   f"meets the rung 2 bar ({cfg['rung2_rate']:.0%} over {cfg['rung2_samples']}+)")
        elif samples < cfg["rung2_samples"]:
            earned = 1
            why = f"only {samples} samples; rung 2 needs {cfg['rung2_samples']}"
        else:
            earned = 1
            why = (f"{rate:.0%} unedited over the last {len(recent)} samples is below the "
                   f"rung 2 bar ({cfg['rung2_rate']:.0%})")
        rung, ceiling = earned, None
        if entry["high_risk"]:
            promotion = entry["promotion"]
            ceiling = int(promotion["to"]) if promotion else 1
            if earned > ceiling:
                rung = ceiling
                if promotion:
                    why += f"; capped at rung {ceiling} by promotion from {promotion.get('by', 'unknown')}"
                else:
                    why += "; high-risk class stays at rung 1 until a person records a promotion"
            elif promotion and earned < int(promotion["to"]):
                why += f"; promoted to rung {promotion['to']} by {promotion.get('by', 'unknown')} but has not held the rate"
        results.append({
            "class": name, "samples": samples, "window_samples": len(recent),
            "unedited_rate": round(rate, 4), "earned_rung": earned, "rung": rung,
            "high_risk": entry["high_risk"], "ceiling": ceiling, "why": why,
        })
    return results


def cmd_record(args) -> int:
    by = args.by.strip()
    if not by:
        raise SystemExit("--by must name the person who accepted or rejected the work")
    event = {"type": "record", "ts": now(), "class": args.task_class, "outcome": args.outcome, "by": by}
    if args.note:
        event["note"] = args.note
    if args.high_risk:
        event["high_risk"] = True
    append_event(Path(args.log), event)
    print(f"recorded {args.outcome} for {args.task_class} (by {by})")
    return 0


def cmd_promote(args) -> int:
    if args.to not in (1, 2, 3):
        raise SystemExit("--to must be 1, 2 or 3")
    if not args.by.strip():
        raise SystemExit("--by must name the person who decided")
    log = Path(args.log)
    known = [e for e in read_events(log) if e.get("class") == args.task_class]
    if not any(e.get("type") == "record" and e.get("high_risk") for e in known):
        print(f"{args.task_class}: not marked high-risk, so promotion has no effect. "
              "Promotion only lifts the high-risk cap at rung 1; other classes earn rungs from the rate alone. "
              "Nothing was recorded.", file=sys.stderr)
        return 1
    append_event(log, {"type": "promote", "ts": now(), "class": args.task_class,
                                  "to": args.to, "by": args.by.strip()})
    print(f"{args.task_class}: ceiling set to rung {args.to} by {args.by.strip()}")
    return 0


def cmd_status(args) -> int:
    results = evaluate(read_events(Path(args.log)), args.task_class, window=args.window,
                       rung2_rate=args.rung2_rate, rung2_samples=args.rung2_samples,
                       rung3_rate=args.rung3_rate, rung3_samples=args.rung3_samples)
    if args.json:
        print(json.dumps({"classes": results}, indent=2))
        return 0
    if not results:
        print("no samples recorded")
        return 0
    for item in results:
        flag = " [high-risk]" if item["high_risk"] else ""
        print(f"{item['class']}{flag}: rung {item['rung']}, {item['samples']} samples, "
              f"{item['unedited_rate']:.0%} unedited (last {item['window_samples']})")
        print(f"  {item['why']}")
    return 0


def positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a whole number")
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Log task outcomes and work out earned autonomy.")
    parser.add_argument("--log", default=DEFAULT_LOG, help=f"log file (default {DEFAULT_LOG})")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record", help="record one reviewed outcome")
    record.add_argument("--class", dest="task_class", required=True)
    record.add_argument("--outcome", required=True, choices=OUTCOMES)
    record.add_argument("--by", required=True, help="who accepted or rejected the work")
    record.add_argument("--note")
    record.add_argument("--high-risk", action="store_true", help="mark this class high-risk (sticky)")
    record.set_defaults(func=cmd_record)

    promote = sub.add_parser("promote", help="record a named person's decision to raise a high-risk class's ceiling")
    promote.add_argument("--class", dest="task_class", required=True)
    promote.add_argument("--to", type=int, required=True)
    promote.add_argument("--by", required=True)
    promote.set_defaults(func=cmd_promote)

    status = sub.add_parser("status", help="show samples, rate and rung per class")
    status.add_argument("--class", dest="task_class")
    status.add_argument("--json", action="store_true")
    status.add_argument("--window", type=positive_int, default=DEFAULTS["window"])
    status.add_argument("--rung2-rate", type=float, default=DEFAULTS["rung2_rate"])
    status.add_argument("--rung2-samples", type=int, default=DEFAULTS["rung2_samples"])
    status.add_argument("--rung3-rate", type=float, default=DEFAULTS["rung3_rate"])
    status.add_argument("--rung3-samples", type=int, default=DEFAULTS["rung3_samples"])
    status.set_defaults(func=cmd_status)
    return parser


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
