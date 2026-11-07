#!/usr/bin/env python3
"""Summarise a SHOTos accepted-work ledger without changing the CSV."""

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median

MEASURES = {
    "model_cost_usd": "Model spend per accepted (USD)",
    "run_minutes": "Agent run minutes per accepted",
    "review_minutes": "Review minutes per accepted",
    "rework_minutes": "Rework minutes per accepted",
}
REQUIRED = {"task_id", "work_type", "condition", "attempt", "accepted", "reviewer_role", "evidence_reference", *MEASURES}
OPTIONAL = ("defects_at_review", "defects_after_acceptance", "accepted_elapsed_minutes", "handoff_pickup_minutes")
STATUSES = {"": False, "no": False, "pending": False, "false": False, "yes": True, "true": True}


@dataclass
class Attempt:
    number: int
    accepted: bool
    measures: dict
    model: str


def recorded_number(value):
    if not value:
        return None
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError("measure must be a number or blank") from error
    if not result.is_finite() or result < 0:
        raise ValueError("measure must be finite and non-negative")
    return result


def read_ledger(path):
    groups = defaultdict(lambda: defaultdict(list))
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError("missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            fields = {key: (row[key] or "").strip() for key in REQUIRED}
            key = (fields["work_type"], fields["condition"])
            task = fields["task_id"]
            status = fields["accepted"].casefold()
            try:
                if None in row or not all((*key, task)):
                    raise ValueError("expected a task ID, work type and condition")
                if status not in STATUSES:
                    raise ValueError("accepted must be yes, no, pending, true, false or blank")
                if STATUSES[status] and not (fields["reviewer_role"] and fields["evidence_reference"]):
                    raise ValueError("acceptance requires a reviewer role and evidence reference")
                number = int(fields["attempt"])
                measures = {name: recorded_number(fields[name]) for name in MEASURES}
                for name in OPTIONAL:
                    value = recorded_number((row.get(name) or "").strip())
                    if value is not None and name.startswith("defects_") and value != value.to_integral_value():
                        raise ValueError(f"{name} must be a whole count")
                    if value is not None and name in {"defects_after_acceptance", "accepted_elapsed_minutes"} and not STATUSES[status]:
                        raise ValueError(f"{name} belongs on the accepted attempt")
                    measures[name] = value
            except ValueError as error:
                raise ValueError(f"line {reader.line_num}: {error}") from error
            groups[key][task].append(Attempt(number, STATUSES[status], measures, (row.get("model") or "").strip()))
    if not groups:
        raise ValueError("ledger has no attempts")
    return groups


def measured_median(attempts, name):
    values = [attempt.measures[name] for attempt in attempts if attempt.measures[name] is not None]
    if not values:
        return "unmeasured" if attempts else "n/a"
    return f"{median(values):.1f} ({len(values)}/{len(attempts)})"


def print_table(rows):
    for row in rows:
        cells = [str(value).replace("|", r"\|").replace("\n", " ") for value in row]
        print("| " + " | ".join(cells) + " |")


def summarise(groups, *, matched_only=False):
    headers = ["Work type", "Condition", "Tasks", "Attempts", "Accepted", "First-pass accepted", *MEASURES.values()]
    rows = [headers, ["---"] * len(headers)]
    tasks_by_work = defaultdict(list)
    quality_headers = ["Work type", "Condition", "Recorded models", "First-review defects", "Defects after acceptance",
                       "Minutes to acceptance", "Handoff pickup minutes"]
    quality = [quality_headers, ["---"] * len(quality_headers)]
    for (work, _), tasks in groups.items():
        tasks_by_work[work].append(set(tasks))
        for attempts in tasks.values():
            attempts.sort(key=lambda attempt: attempt.number)
            if [attempt.number for attempt in attempts] != list(range(1, len(attempts) + 1)):
                raise ValueError("each task needs unique, consecutive attempts starting at 1 within its condition")
            if sum(attempt.accepted for attempt in attempts) > 1:
                raise ValueError("a task can be accepted once per condition")
            if any(attempt.accepted for attempt in attempts[:-1]):
                raise ValueError("acceptance must be the final attempt for a task in its condition")
    shared_tasks = {work: set.intersection(*conditions) for work, conditions in tasks_by_work.items()
                    if len(conditions) > 1}
    if matched_only and not any(shared_tasks.values()):
        raise ValueError("no task IDs appear in every condition for a work type with at least two conditions")
    for (work, condition), tasks in sorted(groups.items()):
        if matched_only:
            tasks = {key: history for key, history in tasks.items() if key in shared_tasks.get(work, set())}
        if not tasks:
            continue
        attempts = [attempt for history in tasks.values() for attempt in history]
        completed = [attempt for attempt in attempts if attempt.accepted]
        accepted = len(completed)
        first = [history[0] for history in tasks.values()]
        first_pass = sum(attempt.accepted for attempt in first)
        row = [work, condition, len(tasks), len(attempts), accepted, f"{first_pass}/{len(tasks)}"]
        for name in MEASURES:
            values = [attempt.measures[name] for attempt in attempts]
            if not accepted:
                row.append("n/a")
            elif any(value is None for value in values):
                row.append("unmeasured")
            else:
                places = 4 if name == "model_cost_usd" else 1
                row.append(f"{sum(values) / accepted:.{places}f}")
        rows.append(row)
        models = ", ".join(sorted({attempt.model or "unknown" for attempt in attempts}))
        quality.append([work, condition, models, measured_median(first, OPTIONAL[0]),
                        *(measured_median(completed, name) for name in OPTIONAL[1:])])
    if matched_only:
        print("Matched task IDs only. Check that inputs and acceptance criteria are comparable.\n")
    print_table(rows)
    print("\nQuality and lead time. Medians show the measured sample in brackets.\n")
    print_table(quality)
    for work, shared in sorted(shared_tasks.items()):
        print(f"\n{work}: {len(shared)} task ID(s) appear in every condition.")
    print("\nPer-accepted figures include all recorded attempts, including work still open or abandoned.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--matched-only", action="store_true", help="include task IDs present in every compared condition")
    args = parser.parse_args()
    try:
        summarise(read_ledger(args.ledger), matched_only=args.matched_only)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Could not summarise ledger: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
