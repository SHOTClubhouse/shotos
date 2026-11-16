# When the run is delegated to workers

Doing the work yourself in one session needs the pilot and the preflight checklist in [SKILL.md](SKILL.md) and nothing more. Add a production manifest only when you hand units of work to separate agents. Keep it in the task's working folder, for example `.work/<task>/manifest.json`, and check it before any worker starts:

```
python .shotos/tools/production_preflight.py check .work/<task>/manifest.json
```

In the SHOTos repository the tool is `tools/production_preflight.py`. If the tool is not available, say so and check the same points by hand against the list below.

1. **Reuse before you re-research.** Look for accepted inputs, templates and evidence by item ID and revision. A new session, a different tool or a fresh allowance is not a reason to repeat accepted work.
2. **Separate the fixed part from the judgement.** Counting, filling placeholders, ordering, comparing and rendering belong in a script or template: set `mechanical` to true and name the `transform`. Agents resolve claims, write for one reader and handle exceptions. If the whole batch is judgement, set `mechanical` to false and say why in `judgement_reason`.
3. **Freeze acceptance.** Write the acceptance revision and the source or template revision into the manifest. Acceptance covers the final output where it lives, any visual check, a repeat run that does no harm and one failure case. A generated file alone is not acceptance.
4. **Pilot every route.** Prove up to three units that between them cover every route about to scale. Record each accepted pilot with its evidence and the acceptance revision it passed.
5. **Set a finite budget.** Launches, calls and minutes. A launch budget above three needs a written `scale_reason` before the run, not after it.
6. **Give workers a short packet.** Owner, unit IDs, acceptance revision, source references, the one allowed operation, the evidence required, the budget and the stop boundary. Do not pass the whole conversation. Each worker returns a receipt: unit IDs, the revision it worked from, checks, failures and the next action.
7. **Admit one unit at a time.** Run `python .shotos/tools/production_preflight.py admit <manifest> --unit <id>` before each launch. A duplicate unit or an exhausted budget is refused. A reservation stands even if the launch fails: read its receipt before you retry.
8. **A changed rule resets acceptance.** If the common rule, template or data changes, stop launching, change it once, rerun the pilot and replay only what it touched. The tool refuses further admissions once the acceptance or source revision in the manifest differs from the one the ledger started with. Do not start a second repair run against the old rule.
9. **Finish on accepted output.** Count accepted items, first-pass acceptance, repairs, wall time, launches and human interventions. Volume, and agreement between agents, are not quality.

The tool checks declarations. It cannot tell whether a pilot was really reviewed, and it is not a spending cap on any account. Do not describe it as one.

## Example manifest (fictional)

Six club newsletters, two routes, both piloted and accepted.

```json
{
  "task": "spring-newsletter-batch",
  "owner": "Maya",
  "phase": "production",
  "acceptance_revision": "acceptance-2026-03-02",
  "source_revision": "template-r4",
  "mechanical": true,
  "transform": "scripts/fill_newsletter.py",
  "transform_tested": true,
  "retry_safe": true,
  "failure_tested": true,
  "units": ["club-a", "club-b", "club-c", "club-d", "club-e", "club-f"],
  "routes": ["standard-club", "club-with-sponsor"],
  "pilots": [
    {"route": "standard-club", "accepted": true, "evidence": ".work/spring/pilot-club-a.md", "acceptance_revision": "acceptance-2026-03-02"},
    {"route": "club-with-sponsor", "accepted": true, "evidence": ".work/spring/pilot-club-c.md", "acceptance_revision": "acceptance-2026-03-02"}
  ],
  "budget": {"max_launches": 6, "max_calls": 40, "max_minutes": 90},
  "scale_reason": "Six clubs, two routes, both piloted and accepted."
}
```

## Contrary case

One document, written by one agent in one session. No manifest, ledger or worker is needed. Use the ordinary pilot and checklist, or for three items or fewer, do the item and read it back.
