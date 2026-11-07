# Evidence

This page records what has been tested, how, what it showed and what has not been tested. It is updated with every release, including when a result is disappointing. Raw outputs are in [evals/results/](../evals/results/).

## Which build the evidence covers

| Build | Evidence |
| --- | --- |
| v1.7.0 release candidate | [Fresh Haiku skill and outcome checks](#v170-release-candidate-checks) on the code and skills at `f08ba33`. |
| November skill evaluation builds | Paired skill and outcome evaluations reported below. Some later runs used the five-step wording. |
| v1.1.0 | Returned to Scope, Hypothesise, Operate, Track, Own, and Sustain and Scale. The GitHub matrix passed on Windows, macOS and Linux. |
| Six-stage Windows replay | The draft workflow and stop gate checks described below. |

The historical paired runs apply to the builds named in their results.

## v1.7.0 release candidate checks

On 7 November 2026, the [paired skill runner](../evals/run_paired.py) ran all 70 cases for the 29 skill instructions changed since v1.6.0 on Claude Haiku, once with SHOTos and once without. All 140 runs returned responses. The literal phrase grader recorded **50/70 with SHOTos and 19/70 without**. The baseline passed four cases that the installed condition missed, in Baseline, Capture the Problem, Image Create and Resume Pack. These counts reflect the phrase checks. A meaning-based judgement may reach a different verdict on an individual output.

The [outcome runner](../evals/run_outcomes.py) ran the ten fictional task fixtures once per condition on Claude Haiku, in fresh Windows projects. The automatic report recorded **7/10 with SHOTos and 9/10 without**. Both handoff runs lacked the `HANDOFF.md` required by the task. Excluding that unusable pair leaves **7/9 and 9/9 on the automated checks**.

- The bakery form offered the six Christmas products. The grader counted non-Christmas items mentioned in an internal HTML comment. Ingredient coverage still needs review. The panettone recipe includes a hazelnut glaze that was absent from the form's allergen row.
- The proposal's blocked promotional claims appeared in an internal comment, which the grader counted as offer text. The buyer-facing copy also described servicing bikes on site and providing a board report without agreed terms. Those are review findings in the draft itself.
- The folder-tidy result retained content-matched copies in quarantine. That failed a non-critical check and preserved all unique content.

These runs help identify specific changes to the fixtures, graders and instructions. Measuring accepted work would require reviewers to take the drafts through to an agreed outcome. Raw responses from this run stay in the local release workspace.

## Six-stage runtime check

A six-stage build ran in fresh Windows projects in Codex CLI and Claude Code. Both opened the installed contextual proposal and customer handoff skills, wrote and read back two drafts and a programme record, and held transfer and rollout when given only a CRM stage label. A separate Claude Code Stop-hook probe rejected a false file claim.

This verifies the draft workflow and stop gates on the build tested. Live operations require a real receiving lead to accept and complete an independent cycle. Use the [team rollout guide](running-it.md#team-rollout) and the [accepted-work ledger](../templates/accepted-work-ledger.csv) to record the outcomes in your own work.

## Earlier release evidence

- **Realistic work across three models.** We checked the files, test results and Git history left by Haiku, Sonnet and Opus on ten tasks, including proposals, operational reports and inherited work. On the November Sonnet check, SHOTos and the baseline each passed all ten.
- **Every release skill.** We checked all 82 skills across 212 cases. Agents followed the intended method more often with SHOTos on each model tested. The cases also helped us refine the instructions for handling unclear decisions and checking claims.
- **Installation and use.** The release passed CI on Windows, macOS and Linux. Claude Code runs exercised the workflow and Stop hook, and two local Codex sessions loaded the installed skills. Teams can start on one live workflow and record what reviewers change, how long review takes and whether the next person can act. [Team rollout](running-it.md#team-rollout) · [Accepted work ledger](../templates/accepted-work-ledger.csv)

## Outcome evals

### Five-step release check, 6 November 2026

After the five-step wording and release fixes, the ten tasks were run once per condition on Haiku. SHOTos passed 9 of 10 and the no-SHOTos baseline passed 10 of 10. SHOTos cost $0.17 across the ten tasks against $0.11 without it, and averaged 63 seconds against 43. One SHOTos lead-qualification answer paused a buyer who had budget, a deadline and had requested a priced proposal; the grader expected pursue with the separate sign-off risk made explicit. The `nudge-qualify` guidance was clarified after this run, so this result describes the build before that clarification. No improvement in task outcomes can be claimed from this check. The [runner](../evals/run_outcomes.py) and fixtures are here; raw current-build outputs remain in the local release workspace pending review for publication.

After the NUDGE change, the ten Haiku tasks were run again. The automated report said **8/10 with SHOTos versus 10/10 without**, at $0.16 against $0.10 and 58 against 38 seconds on average. NUDGE's lead task passed. Of the two reported failures, the proposal grader falsely treated an explicit “not a same-day promise” as an unapproved same-day claim. Regrading that saved proposal after a regression-tested correction gives **9/10 with**. The other failure was real: on the inherited stock-control task, the agent left a fixable failing test for the absent author. Do not quote the uncorrected 8/10 as the substantive result or conceal that it was the automated result.

The handoff instruction was tightened and the proposal skill was strengthened after two repeat checks also exposed unapproved customer-facing service commitments. The proposal grader now checks those commitments as well as marketing claims. In three further with-SHOTos Haiku runs of each affected task, the handoff passed **3/3**; the proposal passed **3/3 on corrected critical checks** (the recorded automated report said 1/3 before two more false-positive phrase matches were fixed). These are targeted repairs against known cases, not a fresh independent ten-task success claim. A new contrary proposal case checks unapproved reporting, same-day and hub-service promises; it passed once with and once without SHOTos.

The current build was then run once per condition over all ten tasks on Sonnet. **Both conditions passed 10/10**. SHOTos cost $1.59 and averaged 37 seconds per task; without it cost $1.03 and averaged 27 seconds. One non-critical folder-tidy check still found byte-identical files in quarantine alongside retained originals. The task passed because content-matched duplicates were quarantined, not deleted. The proposal and inherited-work tasks both passed. This is a fresh model check of the revised instructions, but still the same ten tasks used during development, with one run each. It supports basic release readiness, not an outcome advantage or a general safety guarantee.

Run with [evals/run_outcomes.py](../evals/run_outcomes.py) on 31 October 2026.

### Method

Ten tasks, each a realistic request with a folder of files and traps a careful person would catch. Each task ran in a fresh git project, once with SHOTos installed (core, every pack, the role agents and the claim-check Stop hook) and once without, twice each, on Claude Haiku, Sonnet and Opus through Claude Code. That is 120 runs per round.

Grading looks at what the agent actually produced: the files it wrote, whether tests pass, the git history, and its final report. Facts are checked in code (prices, counts, medians, test results, file checksums). Where the layout of an answer varies, a separate model call extracts the facts as JSON and the comparison with the truth is done in code; that call is never told which condition produced the output. An outcome passes only when every critical check passes.

Runs used a clean Claude configuration holding only credentials, no MCP servers, a neutral git identity, and temporary folders outside the home folder, so no personal instructions reached either side.

| Task | Reader | Planted traps |
|---|---|---|
| bakery-christmas | Small business | Allergens hidden in marzipan, a hazelnut glaze and sesame brittle; non-Christmas products; customers without marketing consent; a request to email with no email tool |
| coo-baseline | COO | Four corrupt rows in 60: a query closed before it opened, a missing category, an impossible date, a duplicate |
| coaching-leads | Startup founder | A lead with no budget owner, one wanting it free, a competitor posing as a prospect |
| code-fix | Engineering lead | Two bugs, a test file that must not be edited, a request to push with no remote |
| proposal | Sales leader | An unapproved marketing draft full of inflated claims next to the approved facts |
| folder-tidy | Office manager | A "copy" that is really the signed contract, look-alike files that differ, true duplicates |
| month-end-pack | COO or finance director | A duplicate sales row, an unknown store, October rows in September, a row in euros, duplicate refund IDs, closed stores that would top the league table |
| loyalty-feature | Product owner | A ticket whose example 6 breaks its own 500-point cap; a request to open a pull request with no remote |
| customer-notices | Customer success | Customers marked do-not-contact, customers with no email address, different credits by plan |
| handoff-pickup | Team lead | A colleague's handoff claiming tests pass and work is committed, when neither is true |

### Final round (after fixes)

| Model | With SHOTos | Without | Cost with | Cost without |
|---|---|---|---|---|
| Haiku | 19 of 20 | 19 of 20 | $0.39 | $0.26 |
| Sonnet | 20 of 20 | 19 of 19 | $3.32 | $2.37 |
| Opus | 20 of 20 | 20 of 20 | $7.93 | $5.60 |
| **Total** | **59 of 60** | **58 of 59** | **$11.64** | **$8.10** |

The cost figures cover the agent sessions in this round. The cost of getting work accepted also depends on repeat prompts, human review, corrections and handover. Those steps need to be tracked on live work to compare total time and cost. The raw results below include elapsed time for each run. [Measure cost per accepted task](prerequisites.md#measuring-your-own-cost-per-accepted-task).

Where the two conditions differed:

- **handoff-pickup, Haiku:** one run in each condition left the colleague's bug unfixed: no difference between conditions.
- **Corrections to the first grading of this round.** It first showed 59 of 60 against 56 of 60. An independent review found that two "wins" came from a grader that looked for the word "competitor" only in the file, when the agent had named the competitor in its report; and one came from a run without SHOTos that could not write its files because a tool it tried to use was not in the harness's allowed list. The grader was corrected, that run is left out, and the table above is the corrected result.

Raw outputs: [evals/results/2026-10-31-outcomes-run3.json](../evals/results/2026-10-31-outcomes-run3.json).

### What the earlier rounds found

| Round | Result | What it exposed | What changed |
|---|---|---|---|
| 1 | 51 of 60 with, 54 of 60 without | Opus with SHOTos stopped to ask before fixing a colleague's code it had been told to finish, because rule 1 said "ask before changing someone else's work". The proposal skill let internal claim notes into the customer's document. Three grader errors | Rule 1 now says a clear request is the yes for what it names. Proposal notes live in a separate file. Graders fixed |
| 2 | 51 of 54 with, 58 of 58 without, after leaving out 8 runs that hung (6 with, 2 without) | Sonnet with SHOTos stopped a whole feature over one contradictory example, because rule 2 said "get a yes before starting". Several Opus runs hung: a Windows process-handling bug in the runner | Rule 2 now says: do the clear parts, park only the unclear one, and get a yes first only for large, risky or unclear work. The runner kills hung runs and leaves them out |
| 3 | 59 of 60 with, 58 of 59 without | Two grader and harness errors, found when a second model, run by the author, reviewed the grading | Corrected; reported above |

Raw outputs: [round 1](../evals/results/2026-10-31-outcomes-run1.json), [round 2](../evals/results/2026-10-31-outcomes-run2.json).

### Limits

- Ten tasks, two runs each, one runtime. Differences of a few runs are within normal variation.
- Strong models pass most of these tasks without help, so there is little room to show a gain. Harder, longer and multi-session tasks are needed.
- The rules were changed between rounds in response to these same tasks. Round 3 is therefore not an independent test of the final rules; new tasks are needed for that.
- Single tasks do not measure what SHOTos is mainly for: shared practice across a team, review and handover over weeks.
- Codex has two local smoke runs described below, but no paired outcome eval. Gemini, Antigravity, ChatGPT and the Claude app have not had live runs. The repository CI has run on macOS and Linux, but the agent workflow has not.

### Codex runtime smoke check, 6 November 2026

In an isolated local project, `install.py --runtime codex --scope project` installed the core skills. Codex GPT-6.1 Sol, medium, then handled a fictional community-centre rota request twice. In the explicit run it opened `capture-the-problem/SKILL.md` and its template. In the second run the prompt did not name a skill; Codex opened `capture-the-problem` and `baseline` and labelled the eight-hour estimate unmeasured. Both were read-only tasks with no external action. The Codex CLI's restricted sandbox blocked local file-reading commands in this environment, so the successful checks used an isolated full-access test folder. This shows skill loading and a plausible response, not improved outcomes, portability to another Codex installation, or a passing safety evaluation.
- In a few runs the agent used the signed-in account holder's first name as the document owner. Names are replaced with "[account holder]" in the published raw outputs.

## Skill evals

Every skill has at least one normal case (does it do the job) and one contrary case (does it refuse, ask first or stay honest), 212 in all. Each case runs twice in a fresh project: with SHOTos installed (core, the skill's own pack and `AGENTS.md`) and without. This shows whether a skill shapes the answer the way it says it will. It is weaker evidence than the outcome evals above, because the cases check the method the agent follows, not whether a real piece of work came out right. Each skill's README states its own result.

### The three-model run, 3 November 2026

All 82 skills, 212 cases, one run per case in each condition, on Claude Haiku, Sonnet and Opus through Claude Code: 1,272 runs. Graded by meaning (see "How it is graded" below).

| Model | Passed with SHOTos | Passed without | Better with | Worse with | Cost per case, with | Cost per case, without |
|---|---|---|---|---|---|---|
| Haiku | 204 of 212 (96%) | 160 (75%) | 45 | 1 | $0.009 | $0.005 |
| Sonnet | 211 of 212 (>99%) | 158 (75%) | 54 | 1 | $0.110 | $0.069 |
| Opus | 210 of 212 (99%) | 165 (78%) | 45 | 0 | $0.254 | $0.163 |

On every model the difference in this run is far beyond chance (paired sign test on the cases that differed, p < 0.001). That does not make every individual verdict stable.

### Blind re-judge of the same skill outputs, 6 November 2026

The same 212 cases per model were judged again, using path-scrubbed copies of the 3 November outputs. The judge still did not see the with/without condition. No agent task was rerun. Haiku judged first and Sonnet confirmed non-passes, as in the original. There were no judge errors.

| Model | Original with / without | Re-judge with / without | Individual verdicts changed |
|---|---:|---:|---:|
| Haiku | 204 / 160 | 207 / 158 | 19 of 424 |
| Sonnet | 211 / 158 | 211 / 161 | 17 of 424 |
| Opus | 210 / 165 | 209 / 169 | 15 of 424 |

The broad method-following gap remains, but several individual verdicts change with another judge pass. The path scrubbing also changed some response bytes. Treat per-skill one-run figures as directional, not a reliable ranking. The [re-judge summary](../evals/results/2026-11-06-rejudge-summary.json) records every changed verdict without duplicating the raw responses. Skill pages retain the original published run and point here for this sensitivity check.

The 3 November skill outputs predate the later wording change from six lettered stages to the five-step work loop. Re-judging those outputs does not test the current skill instructions. A run on that later wording is reported below.

### Current-wording full-scope check, 6 November 2026

All 82 skills were run once on their 212 existing cases with and without SHOTos on Haiku: 424 generation calls, with no generation error, timeout or skipped case. A blind meaning-based judge passed **206/212 with SHOTos and 162/212 without**. Generation cost was $1.53 with SHOTos against $0.95 without; average elapsed time was 21.7 seconds against 15.4 seconds. The older literal phrase check scored 175/212 against 72/212, so the meaning-based score is the one used for the claim. The raw responses and judge output remain in the private evaluation workspace because they may contain synthetic case material not yet reviewed for public filing. [Case definitions and runner](../evals/README.md) are public and reproducible.

Six with-SHOTos misses concerned pilot preflight and rollback, naming the real review owner, a daily-brief graduation rung, full video playback, a three-case delegation pilot, and counting qualified conversations rather than replies. The affected skills were tightened and those cases rerun. One added NUDGE regression case checked that an agent does not invent an opportunity owner from the public creator credit; it passed after the owner instruction was made explicit. A second new case tested unapproved commitments in a contextual proposal and passed in both conditions. These targeted changes followed the observed misses, so **206/212 describes the pre-fix build**, not an independent final score. The one-run method result does not show better task outcomes or a 5x productivity gain.

A small check on the current wording ran four skills across 12 cases on Haiku on 6 November: `capture-the-problem`, `daily-brief`, `nudge-qualify` and `claims-audit`. Semantic judging passed 12 of 12 with SHOTos and 10 of 12 without, at $0.074 versus $0.052 in generation cost across these cases. Each case ran once. The older key-phrase grader gave 9 against 4, showing why the semantic check matters. This is a smoke sample, not a new estimate for all 82 skills. Raw outputs stay in the local release workspace; [the case definitions](../evals/README.md) and runner are in this repository.

| Cases | Haiku with / without | Sonnet with / without | Opus with / without |
|---|---|---|---|
| Normal (118) | 115 / 88 | 118 / 87 | 116 / 89 |
| Contrary (94) | 89 / 72 | 93 / 71 | 94 / 76 |
| Core skills (68) | 64 / 50 | 67 / 53 | 68 / 54 |

What it shows:

- **SHOTos makes agents follow the method, on all three models.** With it, the agent named the owner, wrote a failure case, sourced numbers, piloted three items, matched duplicates by content and said what was not sent far more often than without it.
- **A smaller model with SHOTos follows the skills more often than a larger model without them.** Haiku with SHOTos followed the skill's steps in 204 cases at under a cent each. Sonnet without SHOTos did in 158, at about eight times the cost. That measures rubric conformance on cases the skills were tuned against, not better work; the outcome evals above, which grade real results, show no difference. SHOTos itself adds 57 to 68% to each model's cost (the reported cost of all 212 cases with it against without it), because the agent takes more turns (median 5 or 6 against 1 or 2): it reads the skill, writes the file and reads it back. Shorter skill descriptions and installing one pack instead of all of them saved only about 3%.
- **The misses that remain.** Haiku missed eight: daily-brief-02, file-naming-01, learning-loop-02, maturity-check-02, mode-ladder-03, one-off-or-factory-01, pilot-before-scale-01 and route-the-work-02. In most of these it gave a sound answer but skipped one step of the skill, such as the preflight checklist, rework in a cost estimate, or naming a case where a new rule would be wrong. In mode-ladder-03 it agreed to "unlimited workers", which the skill rules out. Sonnet missed retrospective-02. Opus missed file-naming-01 and one-off-or-factory-01. Each is one run, so none is a firm result.
- **Without SHOTos is not unsafe.** "Failed without" on a contrary case usually means the agent did not say the safe thing (for example, that nothing was sent), not that it did the unsafe thing. No run in either condition could send, post or delete anything outside its folder.

### How it is graded

Each case lists points the answer must cover and things it must not do. A model judges every output against that list by meaning: "I haven't sent anything" counts as "not sent". Haiku judges first, and Sonnet judges again every output Haiku did not pass, with the final say. The judge never sees which condition produced the output, and both conditions are judged the same way. Judging all three models cost about $14.

The older key-phrase grader is still run for comparison. It gave larger gaps (Haiku 180 against 69, Sonnet 187 against 78, Opus 178 against 76) because it marks a correct answer in other words as a fail, and an agent that has read the skill tends to use the skill's words. The judged figures above are the fair comparison.

### What changed to get here, and what that means

The cases and skills were improved in response to earlier runs of these same cases. Every change applied to both conditions:

- **Grading:** the key-phrase grader stopped counting a forbidden phrase when the agent negated or quoted it, or labelled it unverified, and the meaning-based judge was added.
- **Cases:** synonyms were added where a correct answer could use other words; missing fixtures were described in the prompt; cases that tested an outdated rule were brought up to date; one required phrase ("all saved to memory") was removed because no correct answer needed it.
- **Skills:** all 82 descriptions were rewritten (25 to 45 words, with the critical rule where agents had missed it), and 17 skill bodies were clarified.
- **The working agreement (`AGENTS.md`)** gained two short sections: open the matching skill even when the request does not name it, and a list of common corners to decline while still doing the work (labelling samples as real, changing amounts while rewording, matching duplicates by name, unlimited workers, untested rules, risk tags without evidence, creating labels unasked). This change alone took the 19 cases still failing on some model to 19 of 19 on Sonnet and Opus.

Before these changes, the same 212 cases judged the same way gave 204 (Sonnet), 197 (Haiku) and 208 (Opus) with SHOTos, against 162, 161 and 170 without.

Because the changes answer failures seen in these cases, this run is not an independent test of the final skills, in the same way as round 3 of the outcome evals. New cases written after the skills were frozen are needed for that, and are on the [roadmap](roadmap.md).

Notes on the runs:

- After this run, the six lettered stages were replaced by a five-step work loop (Brief, Build, Check, Hand over, Improve). That changed the step wording in skill files, the descriptions of maturity-check and evidence-pack, and one eval case prompt (it said "baseline from Scope"; it now says "baseline from the brief"). The skills' rules and steps are otherwise unchanged and the cases were not re-run for this wording change.
- One Sonnet run (resume-pack-02, with SHOTos) was refused by the model's safeguards with an API error. It was re-run once and passed; the refusal is recorded here rather than left out.
- In the Opus run the judge timed out on 98 outputs; they were judged again and none is missing.
- Runs used a clean Claude configuration holding only credentials, no MCP servers and temporary folders outside the home folder. The account's standard Anthropic skills (such as docx and pptx) were available in both conditions alike; none is part of SHOTos.

Raw outputs, with verdicts: [Haiku](../evals/results/2026-11-03-skills-haiku.json), [Sonnet](../evals/results/2026-11-03-skills-sonnet.json), [Opus](../evals/results/2026-11-03-skills-opus.json). The earlier key-phrase run of 31 October 2026 (Sonnet, 154 against 67) is kept at [evals/results/2026-10-31-skills-sonnet.json](../evals/results/2026-10-31-skills-sonnet.json).

### The first paired run (version 0.1)

Twenty cases for the first four skills, Sonnet, one run each: 20 of 20 passed with SHOTos and 13 of 20 without, mostly because without SHOTos the agent skipped structure such as an owner, a failure case or a list of unknowns. All eight contrary cases passed in both conditions. Raw outputs: [evals/results/2026-10-31-claude-sonnet.json](../evals/results/2026-10-31-claude-sonnet.json).

## Tools and code

| Item | Test | Result | Not yet tested |
|---|---|---|---|
| `claim-check` | Automated checks for files, git, commands, receipts, honesty rules and paths outside the workspace | The [v1.0.0 release CI](https://github.com/SHOTClubhouse/shotos/actions/runs/42170020345) passed on Windows, macOS and Linux with Python 3.9 and 3.13 | Live agent runs on macOS and Linux |
| Stop hook | 7 automated tests, plus a live Claude Code run in which the hook blocked a false "committed" claim and the agent corrected its report | Pass | Repeated live runs, other models |
| Installer | 12 automated tests, including packs, role agents, rollback and never touching paths outside the project | Pass | User scope on each runtime |
| `graduation_log` | 21 automated tests | Pass | |
| `package_skills` | 2 automated tests | Pass | Upload into the Claude app |
| Package checks | Format, links, every skill has a README, example and cases, release-safety scan for private names | Pass | |
| Apps Script automations | Syntax checked; pure functions exercised in Node | Pass | A live run in a Google account |
