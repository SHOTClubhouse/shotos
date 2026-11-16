#!/usr/bin/env python3
"""production-preflight: check a delegated batch plan and admit worker units one at a time.

Control 9 (pilot before scale) for a run handed to separate agents. Keep the
manifest in the task's working folder and check it before any worker starts:

    python tools/production_preflight.py check .work/<task>/manifest.json
    python tools/production_preflight.py admit .work/<task>/manifest.json --unit <id>

`check` refuses a plan with no owner, no finite budget, a production phase
without an accepted pilot for every route at the current acceptance revision,
or a launch budget above three with no written reason.

`admit` reserves one unit in a ledger beside the manifest
(<manifest>.admissions.json) before that unit's worker starts. It refuses a unit
already admitted, a unit that would exceed max_launches, and any admission after
the acceptance or source revision has changed since the first one. A
reservation stands even if the launch then fails: read its receipt before you
retry.

The tool checks declarations. It cannot tell whether a pilot was really
reviewed, and it is not a spending cap on any account. Standard library only.
It changes nothing except its own ledger.

Exit codes: 0 pass, 2 refused.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

PILOT_LIMIT = 3
BUDGET_KEYS = ("max_launches", "max_calls", "max_minutes")
REQUIRED = ("task", "owner", "acceptance_revision", "source_revision")


def positive(value) -> bool:
    return type(value) is int and value >= 1


def validate(plan: dict) -> list:
    """Every reason the plan cannot start, in plain words. Empty means it passes."""
    errors = []
    for key in REQUIRED:
        if not isinstance(plan.get(key), str) or not plan[key].strip():
            errors.append(f"{key} is required")
    phase = plan.get("phase")
    if phase not in ("pilot", "production"):
        errors.append("phase must be pilot or production")
    units = plan.get("units")
    if not isinstance(units, list) or not units or any(not isinstance(u, str) or not u.strip() for u in units):
        errors.append("units must be a non-empty list of unit IDs")
        units = []
    elif len(units) != len(set(units)):
        errors.append("unit IDs must not repeat")
    budget = plan.get("budget") if isinstance(plan.get("budget"), dict) else {}
    for key in BUDGET_KEYS:
        if not positive(budget.get(key)):
            errors.append(f"budget.{key} must be a whole number of 1 or more")
    launches = budget.get("max_launches") if positive(budget.get("max_launches")) else 0
    if phase == "pilot" and (len(units) > PILOT_LIMIT or launches > PILOT_LIMIT):
        errors.append("a pilot is limited to three units and three launches")
    if launches > PILOT_LIMIT and not str(plan.get("scale_reason") or "").strip():
        errors.append("a launch budget above three needs a scale_reason written before the run")
    if plan.get("mechanical") is True:
        if not plan.get("transform"):
            errors.append("mechanical work needs a transform: the script or template that does it")
        if phase == "production" and not all(plan.get(k) is True for k in ("transform_tested", "retry_safe",
                                                                           "failure_tested")):
            errors.append("production needs a transform that is tested, safe to retry and proved on a failure case")
    elif plan.get("mechanical") is not False or not str(plan.get("judgement_reason") or "").strip():
        errors.append("set mechanical to true, or set it to false and give judgement_reason")
    if phase == "production":
        routes = plan.get("routes")
        pilots = plan.get("pilots") if isinstance(plan.get("pilots"), list) else []
        if not isinstance(routes, list) or not routes:
            errors.append("production needs a list of routes")
        else:
            accepted = {p.get("route") for p in pilots if isinstance(p, dict) and p.get("accepted") is True
                        and p.get("evidence") and p.get("acceptance_revision") == plan.get("acceptance_revision")}
            missing = [str(route) for route in routes if route not in accepted]
            if missing:
                errors.append("no accepted pilot evidence at this acceptance revision for route(s): "
                              + ", ".join(missing))
    return errors


def ledger_path(manifest: Path) -> Path:
    return manifest.with_name(manifest.name + ".admissions.json")


def admit(manifest: Path, plan: dict, unit: str) -> dict:
    """Reserve one unit, or raise ValueError with the reason it was refused."""
    if unit not in plan["units"]:
        raise ValueError(f"unit {unit} is not in this manifest")
    lock = manifest.with_name(manifest.name + ".lock")
    ledger = ledger_path(manifest)
    try:
        os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        raise ValueError(f"another admission holds {lock.name}; if no admission is running, check the ledger "
                         "and delete the lock") from None
    try:
        if ledger.exists():
            state = json.loads(ledger.read_text(encoding="utf-8"))
        else:
            state = {"task": plan["task"], "acceptance_revision": plan["acceptance_revision"],
                     "source_revision": plan["source_revision"], "units": []}
        if not isinstance(state, dict) or state.get("task") != plan["task"] or not isinstance(state.get("units"), list):
            raise ValueError("the admission ledger does not belong to this task")
        for key in ("acceptance_revision", "source_revision"):
            if state.get(key) != plan[key]:
                raise ValueError(f"{key} changed from {state.get(key)} to {plan[key]} after admissions started; "
                                 "stop, rerun the pilot and start a new ledger")
        if unit in state["units"]:
            raise ValueError(f"unit {unit} was already admitted; read its receipt before an explicit retry")
        if len(state["units"]) >= plan["budget"]["max_launches"]:
            raise ValueError(f"launch budget exhausted: {len(state['units'])} of {plan['budget']['max_launches']} used")
        state["units"].append(unit)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=manifest.parent, delete=False,
                                         suffix=".tmp") as out:
            json.dump(state, out, indent=1)
        os.replace(out.name, ledger)
        return state
    finally:
        lock.unlink()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("check", "admit"))
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--unit", help="the unit to admit (admit only)")
    args = parser.parse_args(argv)
    try:
        manifest = args.manifest.resolve(strict=True)
        plan = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(plan, dict):
            raise ValueError("the manifest must be a JSON object")
        errors = validate(plan)
        if errors:
            raise ValueError("; ".join(errors))
        result = {"status": "pass", "action": args.action, "task": plan["task"]}
        if args.action == "admit":
            if not args.unit:
                raise ValueError("--unit is required for admit")
            state = admit(manifest, plan, args.unit)
            result.update(unit=args.unit, admitted=len(state["units"]),
                          max_launches=plan["budget"]["max_launches"])
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "refused", "reason": str(error)}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
