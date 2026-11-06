# The twelve agent controls

The [four rules](../docs/controls.md) are short enough to remember. The twelve controls are the same four rules in the detail an agent needs to follow them and a person needs to check them. Each control has its own card in this folder: the rule in a sentence, why it exists, what the agent does, what a person does, how to size it by risk, common mistakes and how to tell it is working.

You do not need all twelve on day one. Start with the four rules in your `AGENTS.md` file (see [the template](../templates/AGENTS.md)), then adopt the cards for the kind of work where you have felt pain. The risk sizing on every card shows where to be light and where to be strict.

## Controls by rule

| Rule | Control | Card | Matters most in | Supported by |
|---|---|---|---|---|
| **1. Stop at the boundaries** | 3. Mode contract | [03](03-mode-contract.md) | Operate | Task record mode line; connector permissions (see [security](guardrails/security.md)) |
| | 4. Stop boundaries | [04](04-stop-boundaries.md) | Operate, Own | `AGENTS.md` template; the receipt rule in claim-check; the Stop hook |
| | 8. Two-session execution | [08](08-two-session-execution.md) | Operate, Own | Frozen approval manifest with checksum; `evidence-handoff` skill |
| **2. Agree acceptance first** | 1. Route the work | [01](01-route-the-work.md) | Scope, Hypothesise | `capture-the-problem` skill; the route line in the task record |
| | 2. Evidence-based risk | [02](02-evidence-based-risk.md) | Scope, Operate | Risk tags with evidence; [data governance](guardrails/data-governance.md) |
| | 5. Acceptance first | [05](05-acceptance-first.md) | Hypothesise | `agree-acceptance` skill; [acceptance template](../templates/acceptance.md) |
| | 9. Pilot before scale | [09](09-pilot-before-scale.md) | Operate, Sustain and Scale | Preflight checklist; [scale guardrail](guardrails/scale.md) |
| **3. Read back the real result** | 6. Read-back | [06](06-read-back.md) | Track | `report-with-evidence` skill; claim-check |
| | 7. Independent review | [07](07-independent-review.md) | Operate, Track | Review packet; [quality guardrail](guardrails/quality.md) |
| **4. Claim only what you can show** | 10. Claim discipline | [10](10-claim-discipline.md) | Track, Own | `tools/claim_check.py`; the Stop hook; [claims guide](../docs/claims.md) |
| | 11. Context control | [11](11-context-control.md) | Operate, Sustain and Scale | One owning record; `evidence-handoff` skill; [productivity guardrail](guardrails/productivity.md) |
| | 12. Graduation | [12](12-graduation.md) | Sustain and Scale | `tools/graduation_log.py`; [pace guardrail](guardrails/pace.md) |

Controls 1 and 2 sit under rule 2 because choosing the route and the risk is part of agreeing what the work is and what done looks like. Control 9 sits there because a pilot is a small acceptance test before the large one. Controls 11 and 12 sit under rule 4 because a claim about a task is only as good as the record behind it, and a claim that an agent can be trusted is only as good as its log.

## How the controls fit together

1. **Before work**, controls 1 and 2 write one line about what the work is and how risky it is. Control 3 sets what the agent may do. Control 5 agrees what done looks like.
2. **During work**, control 4 keeps the agent short of external action. Control 9 pilots before volume. Control 11 keeps the record small and owned.
3. **After work**, control 6 reads the result back where it lives. Control 7 adds a reviewer sized to the risk. Control 10 keeps the report honest.
4. **Across work**, control 8 splits review from execution for the highest-risk actions. Control 12 lets a repeated task class earn autonomy, and take it back.

## Tools in this repository

- **claim-check** (`tools/claim_check.py`): tests a report's Claims block against files, git, allowed commands and receipts. It supports controls 4, 6 and 10. It never marks work as accepted.
- **The Stop hook** (`hooks/`): runs claim-check when a session ends and refuses completion language that has no Claims block.
- **graduation-log** (`tools/graduation_log.py`): records review outcomes per task class and reports the rung each class has earned. It supports control 12. Python 3.9 or later, standard library only.
  - `record --class X --outcome accepted-unedited|accepted-edited|rejected [--note ...] [--high-risk]`
  - `status [--class X] [--json]` with `--window`, `--rung2-rate`, `--rung2-samples`, `--rung3-rate`, `--rung3-samples`
  - `promote --class X --to N --by <name>`

## Skills that support a control

Skills are named here without links because the list grows. See the skills folder for the current set.

- `capture-the-problem`: control 1 (route) and control 2 (risk evidence) at the start of work.
- `agree-acceptance`: control 5, and the boundaries of control 4.
- `report-with-evidence`: controls 6 and 10.
- `evidence-handoff`: controls 8 and 11.

## Guardrails

The [six guardrails](guardrails/README.md) (data governance, security, scale, productivity, pace and quality) apply across every stage. Each lists the controls it relies on.

## How to adopt

1. Put the four rules in your agent instructions file.
2. Pick the two or three controls that match your last problem. A mistaken send suggests control 4; a wrong number suggests controls 6 and 10.
3. Copy the one-line formats into your task record template.
4. Run the "how to check it is working" section of each adopted card after a month, and adjust.
5. Add the rest as the work asks for them.

A control that people stop following has usually become too heavy for the risk. Re-read the sizing section on its card, and lower the load for small work before you drop the control.
