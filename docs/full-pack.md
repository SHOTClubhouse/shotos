# Run the full SHOTos pack

If you have one job in mind, use the [first-job chooser](running-it.md#choose-your-first-job) to find the skill ZIP or pack. Use this guide when you want the full set of skills and team resources.

Install from the checkout into the project that owns the work. Preview first and replace `PATH_TO_SHOTOS` with the checkout path.

```sh
python "PATH_TO_SHOTOS/install.py" --runtime all --scope project --all-packs --dry-run
python "PATH_TO_SHOTOS/install.py" --runtime all --scope project --all-packs
```

Project installs include all 88 skills when you select `--all-packs`, the working agreement, programme and work records, nine role definitions and seven review lenses. Each installed skill has its own fictional input and output. An existing `AGENTS.md` points to the installed agreement. Claude Code can also register the nine definitions as native subagents with `--with-agents`. For other setups, select the appropriate runtime in the installer or give the model the agreement and the relevant role or skill as project instructions.

## From the request to the saved result

1. **Find the task and its sources.** Reuse the existing issue, deal, document or task record. Open the relevant source and latest decision. Check audience, owner, constraints, authority and freshness. Resolve only gaps that affect the decision.
2. **Route it.** Pick the stage and the primary skill from the request. Read its `SKILL.md` and open a linked template or a shipped example when it helps answer a question. Follow a named skill only when its trigger applies. If the skill is absent, use the available guidance and mark any unmet dependency.
3. **Agree the result.** Reuse the acceptance checks already agreed, or write them in the task record. Name the person who accepts the result. Keep the intended destination and permitted actions visible.
4. **Build and read back.** Work in the owning project. Review the saved result against the source and acceptance. Use an independent reviewer where the work calls for one and the runtime supports that separation.
5. **File and hand over.** Drafts and temporary material stay in `.work/<task>/` or the project's approved working location. Put accepted work in the existing system of record. Keep one canonical output and link it from the task with its version, proof and next action. For work across stages, link the task from the programme record.

Use `.shotos/templates/work-record.md` when a task has no suitable record. Use `.shotos/templates/programme.md` for decisions across stages. Keep private inputs in their authorised location and share their evidence by reference where permitted.

## Which persona starts the work

Audience personas describe who needs the outcome. Execution roles describe responsibilities. Review lenses pose questions from different perspectives. A team can use all three without assigning another agent.

| Audience persona | First useful route | What stays with the work |
| --- | --- | --- |
| Solo founder | `nudge-qualify` → `contextual-proposal` → `claims-audit`, then `success-handoff` when delivery changes hands | Deal record with the approved offer, buyer acceptance and receiving lead's next action |
| Small team lead | `agree-acceptance` → relevant delivery skill → `evidence-handoff` | Task checks, reviewed result and named next action |
| Product owner or analyst | `capture-the-problem` → `example-mapping` → `agree-acceptance` | Problem, examples and acceptance beside the issue |
| Engineering or practice lead | `route-the-work` → delivery → `cross-agent-review` or `delivery-metrics` | Change, tests, review and evidence in the repository |
| Business unit leader or sponsor | `decision-brief` → `evidence-pack` → `decision-record` | Options, evidence, decision owner and dated decision |
| Enablement coach or consultant | `runbook` → `enablement-plan` → `rollout-plan` | Observed independent cycle and approved next wave |
| Agent | `route-the-work` → task skill → `report-with-evidence` | Saved artefact, claims, open checks and next action |

For a concrete starting task in marketing, HR, analysis, product or your first role on a team, use [the first jobs by role](personas.md#pick-a-first-job-by-role).

## Who does each part

The project roles are in `.shotos/agents/`. They can be held by people, assigned to supported subagents, or used as a perspective by the same model. Record which happened.

| Role | Takes in | Passes forward |
| --- | --- | --- |
| Business analyst | Request, examples and constraints | Acceptance card for the designer or engineer |
| UX designer | Acceptance card and user context | Proposed interaction and design checks for the engineer and QA lead |
| Engineer | Approved scope and design | Changed artefact and verification evidence for QA |
| QA lead | Acceptance, artefact and receipts | Findings and a verification verdict for the owner |
| Security reviewer | Data flow, access and external actions | Findings for the owner and release manager |
| Sceptic reviewer | Material claim or decision and its sources | Failure cases and missing proof for the lead or analyst |
| Data steward | Sources, permissions and proposed use | Data restrictions and gaps for security review and the owner |
| Release manager | Accepted work and applicable reviews | Exact action manifest and receipt plan for owner approval |
| Enablement coach | Runbook, receiving team and pilot evidence | Observed independent cycle and open support needs for the receiving lead |

Use the cards in `.shotos/lenses/` when a perspective can change the decision. **Lead** combines findings. **Sceptic** tests failure. **Voice of reason** checks risk and authority. **Customer** tests usefulness. **Care** checks the burden on people. **Commercial** tests value and commitments. **Connector** checks links to prior work. Use the cast template there if you want to give the lenses names and voices. Keep lens commentary in conversation and keep deliverables in the owner's voice. Only a person with the relevant authority accepts work or approves action.

## Try it with a real task

> Read our existing account record and check the last onboarding milestone. Prepare a handoff using the installed SHOTos agreement. Keep ownership unchanged until there is a named receiver and written acceptance. Save the draft and evidence with the account, then show me the next decision.

The agent should open `success-handoff`, use `onboarding-recovery` only if there is a stalled milestone to resolve, and preserve the source links and transfer status. If you switch models, provide the same saved task record and source links. Check the same acceptance and output location on either run. Tool access, native agent support and authority depend on the runtime and project setup.

## Improve the pack from real work

Keep a lesson beside the original task when someone has to correct a material claim, recover a handoff or repeat work. Use the `learning-loop` skill and its lesson template. Record what happened and how you know, then decide whether the gap belongs to this task, one skill, a shared instruction or the runtime. Fix the smallest shared source that owns the problem. Keep customer facts, transcripts and identifying details in the approved project record. Use a fictional case to carry the general lesson into SHOTos.

Turn a consequential miss into a fictional example someone else can run. Preserve the original failure, the expected decision and the check that would catch a regression. Use `skill-quality-gate` when a change affects behaviour. Check the case that exposed the gap and a case where the proposed rule would be wrong. Check the installed copy when the change concerns setup or linked resources. Record the old and new revisions, the check result, remaining limits and the person who decides whether to promote the change. After promotion, use the same record to see whether the problem recurs.

Use the accepted-work ledger beside your task records. Start with first-pass acceptance, material defects, minutes spent reviewing or reworking, and the time it takes someone else to pick up the task. Track model spend if the runtime reports it. Count from the first request to a named person's acceptance and include reruns. Keep task types and acceptance criteria comparable before making a performance claim.

**Example from maintaining SHOTos.** A worked example could be opened in the repository and was missing from an uploaded skill ZIP. That was a packaging problem. The fix was to ship each skill's existing fictional input and output through both packaging routes. The check opens those files in a fresh project install and in the ZIP. This verifies availability. A separate run is needed to show how an agent uses them.
