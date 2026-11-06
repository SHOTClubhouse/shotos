# The SHOTos framework

Use this guide to take one initiative from an agreed problem through an independently operated first cycle and into a controlled rollout. The [worked walkthrough](walkthrough.md) shows the same initiative across all six stages.

SHOTos is six delivery stages: **S**cope, **H**ypothesise, **O**perate, **T**rack, **o** Own, and **s** Sustain and Scale. Every stage ends with something you can see and measure. Inside every stage, on every agent task, the [four rules](controls.md) apply.

![The six SHOTos stages](images/six-stages.svg)

```
 S  Scope ──► H  Hypothesise ──► O  Operate ──► T  Track ──┬──► o  Own ──► s  Sustain and Scale ──► next team
 Know your     Call your          Play it        Prove it   │    Own it      Go again, bigger
 ground        shot               out                       ├── pivot ──► back to Hypothesise
                                                            ├── stop ───► record why, and close
                                                            └── hold ───► collect the missing evidence

 Inside every stage, on every agent task: 1 Stop at the boundaries · 2 Agree acceptance first
                                          3 Read back the real result · 4 Claim only what you can show
```

Two things set the shape:

- **Every stage has an exit check.** You do not move on because time has passed. You move on because the output exists and someone has accepted it.
- **Own comes before scale.** A result that only works while its builders are in the room is not ready to copy. The team that will run it has to be able to run it first.

The stages work for business change, technical change, or both at once. Below, each stage has a business side and a technical side, and in practice most work has both.

## Run a programme

![Source evidence, acceptance checks and authority feed the programme record. The next person gets the checked result, the gaps and a named decision owner.](images/context-to-decision.svg)

Keep one [programme record](../templates/programme.md) in the existing project. Name the sponsor who can change scope or authorise rollout, the delivery lead who runs the pilot, and the receiving lead who accepts operational ownership. For each stage, record the named decision owner, the artefact links, the gate decision and date, and the next action. Mark missing evidence and the person who can resolve it.

| Stage | Start from | Pass forward | Decision owner |
|---|---|---|---|
| Scope | A problem or opportunity worth understanding | An agreed problem, boundaries and a baseline or a plan to measure it | Sponsor or problem owner |
| Hypothesise | The agreed scope and baseline | One testable bet, an experiment and agreed acceptance checks | Experiment owner |
| Operate | An agreed experiment and permission for the pilot | A bounded run, its outputs and evidence of what actually happened | Pilot owner |
| Track | The pilot record and baseline | A recorded decision to move to Own, pivot, stop or hold for evidence | Sponsor or delegated decider |
| Own | A decision to continue and a named receiving lead | A runbook, named owners and evidence from an independent cycle | Receiving lead |
| Sustain and Scale | Accepted ownership and a sponsor's rollout decision | An operated first wave, local baselines and an improvement cadence | Rollout sponsor, with each local owner accepting their wave |

The current authority sets the boundary for each run. A draft run checks an artefact. A live run checks the effect of an authorised action. Record separate authority for a live run, external action, operational transfer or wider rollout when those become relevant. If a gate fails, record what happened and where the work returns. Use the [decision record](../skills/decision-record/template.md) to capture those choices.

## S: Scope. "Know your ground."

Understand the situation before changing it. Most wasted effort starts with a solution chosen before anyone wrote down the problem.

| | What you do |
|---|---|
| **Business** | Talk to the people who feel the problem and the people who decide. Map how the work flows today and where it waits, gets handed over or gets redone. Write down the situation, the problem, what it causes and what is needed. Agree with the sponsor what is in scope and, just as important, what is not. |
| **Technical** | Look at what exists: the systems, tools and data, how changes reach production today, how much is tested, and what is fragile. Check whether the data a change depends on is good enough to use. |
| **Agents help by** | Turning interview notes and messy requests into a problem statement, counting and categorising existing data, and drafting the flow map for people to correct. |

**Output:** a problem statement with no solution in it, a map of who is affected and who decides, baseline measures of how things are today (or "not measured", honestly), and an agreed definition of ready and done.

**Exit check:** the owner has confirmed the problem statement, and a baseline or a dated plan to collect it has a named owner.

**SHOTos assets:** [capture-the-problem](../skills/capture-the-problem/README.md), [stakeholder-map](../skills/stakeholder-map/README.md), [baseline](../skills/baseline/README.md), [maturity-check](../skills/maturity-check/README.md) and the [problem template](../templates/problem.md).

**Run this stage.** Use the [problem brief](../templates/problem.md) and [baseline worksheet](../skills/baseline/template.md). Record the source and window for each measure, the people affected, the decision owner and the limits of the first slice. If a baseline is missing, agree who will collect it and by when. Hypothesise can draft a bet while that measurement is open. Operate starts once the comparison baseline and acceptance checks are usable. See the [worked baseline](../examples/baseline/output.md) and [Harbourside findings](../examples/walkthrough/reference/2-findings.md).

## H: Hypothesise. "Call your shot."

Turn the problem into bets you can test, and agree how you will know before you build anything.

| | What you do |
|---|---|
| **Business** | Write each idea as "We believe that X will result in Y, and we will know because Z changes." Work through concrete examples with the people who will use the result, and agree the success criteria before any building starts. |
| **Technical** | Express the expected behaviour as examples (Given, When, Then) that become automated tests. Where the output varies, as AI output does, build a set of example inputs with what a good answer must and must not contain, and keep it as the eval set. Run short spikes or prototypes to find out whether something is feasible before committing to it. |
| **Agents help by** | Drafting examples and edge cases, proposing cases that should fail, and assembling the eval set from real examples. |

**Output:** a prioritised list of testable hypotheses, the eval set, and a plan for the first experiment.

**Exit check:** the owner agrees the measure and acceptance checks. If the baseline is open, record its owner and due date. Verify it before live operation.

**SHOTos assets:** [agree-acceptance](../skills/agree-acceptance/README.md), [hypothesis-card](../skills/hypothesis-card/README.md), [example-mapping](../skills/example-mapping/README.md), [eval-set](../skills/eval-set/README.md), [experiment-plan](../skills/experiment-plan/README.md), the [acceptance card](../templates/acceptance.md) and [specification by example](../ways-of-working/specification-by-example.md).

**Run this stage.** Choose one change using the [hypothesis card](../skills/hypothesis-card/template.md). Specify the target, a guard measure, a stop result, the sample and the time box in the [experiment plan](../skills/experiment-plan/template.md). Use the acceptance card to agree one normal case and one case that must fail safely. For variable AI outputs, freeze the [evaluation set](../skills/eval-set/template.md) before running the comparison. See the [worked hypothesis](../examples/hypothesis-card/output.md) and [Harbourside acceptance card](../examples/walkthrough/reference/3-acceptance.md).

## O: Operate. "Play it out."

Deliver the smallest real piece into real use, working alongside the people who will own it.

| | What you do |
|---|---|
| **Business** | A small team delivers one real use case with the people who do the work today. Show progress regularly to the people affected, and report against the hypothesis, not against activity. |
| **Technical** | Short cycles with automated build, test and deployment. Releases blocked by failing tests, and by failing evals where AI output is involved. Infrastructure described in code. Prove the riskiest part first. |
| **Agents help by** | Doing much of the building, testing and drafting, inside the four rules: stopping at the boundaries, working to the agreed acceptance, reading back the real result and claiming only what they can show. |

**Output:** a working result in real use, a written playbook of how it was done, and a regular show-and-tell.

**Exit check:** the acceptance checks pass on the real result, and every claim of progress is backed by evidence.

**SHOTos assets:** [route-the-work](../skills/route-the-work/README.md), [pilot-before-scale](../skills/pilot-before-scale/README.md), [cross-agent-review](../skills/cross-agent-review/README.md), [research-and-assemble](../skills/research-and-assemble/README.md), [label-the-proof](../skills/label-the-proof/README.md), [report-with-evidence](../skills/report-with-evidence/README.md), [claim-check](claims.md), the Claude Code Stop hook and the [role agents](../agents/README.md).

**Run this stage.** For a batch, use the [pilot log](../skills/pilot-before-scale/template.md) to select up to three varied items and record preflight, recovery, the stop condition and the result. Read back the output in the tool where it lives and link the proof to each acceptance check. Record drafted, reviewed and executed actions separately. If a required source fact or permission is missing, park that item and record who resolves it. See the [worked pilot](../examples/pilot-before-scale/output.md) and [Harbourside draft report](../examples/walkthrough/reference/4-report.md).

## T: Track. "Prove it."

Measure what changed against the baseline, then decide.

| | What you do |
|---|---|
| **Business** | Compare before and after against the baseline from Scope. Write a short report of the value actually realised, and hold a retrospective on how the work went. |
| **Technical** | For software delivery, track the four DORA measures: deployment frequency, lead time for changes, change failure rate and time to restore. Add eval scores, cost and response times for AI features, defects found after release, and monitoring of the live system. |
| **Agents help by** | Gathering the numbers, comparing them with the baseline and drafting the report, with every figure sourced. |

**Output:** an evidence pack and a decision by the sponsor or named delegate to proceed to Own, pivot, stop or hold for evidence.

**Exit check:** the decision is made by a named person, on the evidence, and written down. Stopping is a valid result. A pivot goes back to Hypothesise. A hold records the missing evidence, its owner and the next review.

**SHOTos assets:** [evidence-pack](../skills/evidence-pack/README.md), [delivery-metrics](../skills/delivery-metrics/README.md), [decision-record](../skills/decision-record/README.md), [progress-wrap-up](../skills/progress-wrap-up/README.md), [retrospective](../skills/retrospective/README.md), and claim-check for agent work.

**Run this stage.** Fill the [evidence pack](../skills/evidence-pack/template.md) with the baseline and observed result over comparable windows. Include the denominator, guard measures, exceptions and what could not be measured. Use the [decision record](../skills/decision-record/template.md) to capture the owner's decision and why. Where the run produced only drafts, record draft quality separately and hold the impact decision until live outcome evidence exists. See the [worked evidence pack](../examples/evidence-pack/output.md) and [worked decision](../examples/decision-record/output.md).

## o: Own. "Own it."

Make the team that will run the result self-sufficient before anyone copies it elsewhere.

| | What you do |
|---|---|
| **Business** | Train the people who will run it, and train some of them to train others. Build a small network of people who champion the new way of working, and write down how the work is now done. |
| **Technical** | Pair with the team until they can make changes and release on their own. Hand over runbooks, templates and the standard way to do common tasks. |
| **Agents help by** | Drafting runbooks and guides from what was actually done, and handing work over with its state and evidence intact. |

**Output:** a team that runs it without outside help, and a capability matrix showing who can do what.

**Exit check:** the team has run at least one full cycle, including a release or a reporting period, without the people who built it.

**SHOTos assets:** [evidence-handoff](../skills/evidence-handoff/README.md), [runbook](../skills/runbook/README.md), [enablement-plan](../skills/enablement-plan/README.md) (with a capability matrix), [resume-pack](../skills/resume-pack/README.md) and the [handoff template](../templates/handoff.md).

**Run this stage.** Give the receiving lead the accepted pilot decision, [handoff](../templates/handoff.md), [runbook](../skills/runbook/template.md) and [capability matrix](../skills/enablement-plan/template.md). Agree what a full cycle and a common exception look like before the exit run. The receiving team runs the cycle using its own access, handles or escalates the exception, and records the output. The receiving lead signs off the evidence. If the builders had to intervene, record what the team needs and repeat the exit run. See the [worked enablement plan](../examples/enablement-plan/output.md) and [worked runbook](../examples/runbook/output.md).

## s: Sustain and Scale. "Go again, bigger."

Take what worked to the next team, and keep improving.

| | What you do |
|---|---|
| **Business** | Move people who have done it into the next teams, start a community of practice, put light governance around the way of working, and keep a continuous improvement loop running. |
| **Technical** | Turn what worked into reusable templates and shared platforms, use agents and automation to speed up each new rollout, and monitor in production. |
| **Agents help by** | Applying the same rules and templates in every new team, so the second and third rollouts start from the first one's evidence. |

**Output:** a rollout plan across teams, reusable assets, and a standing improvement cadence.

**Exit check:** the current workflow has a maintainer and review date. When the sponsor approves expansion, the next team starts at Scope with its own baseline.

**SHOTos assets:** [rollout-plan](../skills/rollout-plan/README.md), [learning-loop](../skills/learning-loop/README.md), [skill-quality-gate](../skills/skill-quality-gate/README.md), [graduation-ladder](../skills/graduation-ladder/README.md) and the [setup pack](../packs/setup/README.md).

**Run this stage.** Use the [rollout plan](../skills/rollout-plan/template.md) to link the Track decision and Own sign-off. Specify what each team can reuse, what it must validate locally, who supports it, and when a wave pauses. Start one receiving team at Scope with its own baseline, permissions and owner. Keep a named maintainer and review date for the original workflow, and use the [learning log](../skills/learning-loop/template.md) to test changes before updating the shared kit. See the [worked rollout plan](../examples/rollout-plan/output.md) and [worked learning loop](../examples/learning-loop/output.md).

## Three illustrative examples

These are made-up examples to show the shape of each stage. The numbers are hypotheses a team might set, not results anyone has achieved.

### Business: an insurer trials AI triage of claims

| Stage | What happens |
|---|---|
| Scope | Claims take nine days on average. Mapping the flow shows where claims wait and get handed back and forth. |
| Hypothesise | "AI triage of low-risk claims will cut handling time by 30% with no rise in errors." Fifty past claims, with the decisions people made, become the eval set. |
| Operate | A squad of three delivers triage for one claim type in eight weeks, showing progress to the claims director every fortnight. |
| Track | Compare handling time, agreement with human decisions and cost per claim against the baseline. The director decides whether to prepare for Own, pivot or stop. |
| Own | Claims handlers learn to review the AI's calls, and the in-house team runs the evals itself. |
| Sustain and Scale | The approach moves to the next claim type, with one experienced person joining each new team. |

### Technical: a retailer moves to continuous delivery

| Stage | What happens |
|---|---|
| Scope | Releases are monthly, much of the testing is manual and releases are often rolled back. |
| Hypothesise | "Automated regression tests on checkout will let us release weekly with fewer incidents." The product owner and engineers write the scenarios together. |
| Operate | The checkout team gets a pipeline first, with automated tests and feature flags. |
| Track | The four DORA measures, before and after. |
| Own | Engineers from outside the team pair with the checkout team until they run the pipeline themselves, then hand over runbooks. |
| Sustain and Scale | The pipeline becomes a template for the other teams, and an internal guild keeps it improving. |

### Community: a grassroots sports club

| Stage | What happens |
|---|---|
| Scope | Volunteer coaches have no shared session structure, and many players stop playing around age 13. The club records attendance and a simple skills check as its baseline. |
| Hypothesise | "Structured sessions will improve skills scores by 10% and reduce drop-out over twelve weeks." |
| Operate | One age group runs the structured sessions for a term. |
| Track | Re-test the skills check and compare attendance and retention with the baseline. |
| Own | The volunteer coaches run the sessions themselves, led by a club champion. |
| Sustain and Scale | Start one more age group at Scope with its own baseline. Use that wave's results to decide whether to invite a neighbouring club. |

The [Harbourside walkthrough](walkthrough.md) follows one fictional lettings workflow across all six stages, with sample data for the initial pilot and a worked decision path for Track, Own and Sustain and Scale.

## Where the stages come from

The stages draw on public practice: build, measure and learn from lean product development; specification by example and behaviour-driven development; the DORA research on software delivery; product thinking over project thinking; and Team Topologies on how teams own their work and how enabling teams step back. What SHOTos adds is an exit check for every stage, ownership before scale, and the four rules that keep agent work honest inside each stage. Sources are listed in [sources.md](sources.md).
