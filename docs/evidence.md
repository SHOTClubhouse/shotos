# SHOTos evidence

SHOTos helps a team agree what counts as done, check the result against its sources and hand work over with enough evidence for someone else to act. The checks below cover the six-stage method, skills, runtime behaviour and release files. Each result is tied to the exercise or build that produced it.

| If you need to | What a test showed | Try it |
| --- | --- | --- |
| Turn a problem into a bounded pilot | The Harbourside tests check the enquiry counts used to scope the pilot. The supplied files let you draft the updates and identify a case that needs a person before anything goes out. | [Six-stage walkthrough](walkthrough.md) |
| Decide whether a team is ready for a first rollout wave | The invoice-query replay in Codex and Claude Haiku recognised the receiving team's independence decision and the sponsor's conditional approval. Both kept the new site at Scope until its own checks passed. | [Four-round enterprise exercise](guides/invoice-query-exercise.md) |
| Prepare a weekly leadership brief | In fresh Claude Code projects, three plain-language weekly requests opened Weekly Executive Brief automatically. The two drafts with unsupported claims flagged them inside the brief. A separate decision request opened Decision Brief. | [Weekly briefing exercise](../packs/exec-ops/skills/weekly-exec-brief/operating-review.md) |
| Review a leadership decision | The Windows retail exercise ran in Codex and Claude Code. Both kept the recommendation pending in the first round and used the follow-up records to identify the decision, receiving lead and later stop. | [Two-round retail exercise](guides/chat-assistants.md#run-the-retail-scenario) |
| Take a proposal into delivery | A Windows replay in Codex CLI and Claude Code carried the proposal and its sources into a handoff. Both held the transfer and rollout when the only evidence was a CRM stage label. | [Proposal-to-handoff exercise](../packs/win-the-work/skills/contextual-proposal/worked-deal.md) |
| Check that a completion claim has evidence | A Claude Code Stop-hook probe rejected a false claim that a file had been created. The local demo shows how the checker distinguishes a saved draft, a failed test and an unsupported send. | [Completion-check demo](../README.md#try-shotos) |

## Six-stage runtime check

**Aim.** Check whether the same work and evidence can move from a scoped problem to an owned process and a rollout decision.

**Experiment.** The [Harbourside walkthrough](walkthrough.md) starts with a checked baseline of seven repeat repair emails out of twelve and a draft pilot. The next stages use labelled scenarios for Track, Own and Sustain and Scale. Separately, Codex CLI and Claude Code opened the installed proposal and handoff skills in fresh Windows projects, produced two drafts and a programme record, and held transfer and rollout when a CRM label was the only evidence. The invoice-query replay tested what changed after the receiving team and sponsor supplied their records. [Recorded runtime check](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#six-stage-runtime-check) · [Invoice-query replay](guides/invoice-query-exercise.md#replay-check)

**Conclusion.** You can rehearse the full method and compare the draft, the handoff and the sponsor decision with worked references. The runs exercised those handoffs and decision gates on fictional work. An actual rollout needs its own operating results, receiving lead's acceptance and independent cycle. [Programme record](../templates/programme.md) · [Team rollout](running-it.md#team-rollout)

## Skill behaviour and work outcomes

**Aim.** Distinguish following a skill's method from producing work a reviewer can accept.

**Experiment.** A historical 82-skill build ran 212 cases per condition on each of Claude Haiku, Sonnet and Opus. The meaning-based grader found higher method adherence with SHOTos on all three models. For Haiku, it scored 204 of 212 with SHOTos and 160 without. A blind re-judge of the same outputs scored 207 and 158. A separate v1.10.0 run graded task outputs on ten fictional jobs. Nine pairs tied. In the remaining pair the SHOTos proposal passed and the baseline introduced an unsupported commitment. [Historical skill results](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#skill-evals) · [Task outcome results](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#separate-release-regression-check)

**Conclusion.** The historical runs show that the skills changed how agents worked. The task runs give examples of what that changed in the resulting work. They do not establish a general gain in quality or cost to acceptance across all 88 current skills. [Test it on your work](#check-the-value-on-work-you-already-do)

## Weekly brief coverage and placement

### Aim

Keep unsupported claims in **Unverified** only. Make missing sources visible in a **Coverage: partial** line. Preserve normal drafting when all required records are available.

### Experiment

Use plain-language prompts in fresh Windows projects with Executive Ops installed. Claude Code runs Claude Haiku. Each request is fictional and none names a skill. Check the native invocation record, the draft's coverage line and the location of the disputed claim.

| Request | What the revised brief showed |
| --- | --- |
| Sales and renewal claims with both supporting records missing | **Coverage: partial** names both missing records. The two claims sit under **Unverified** with the evidence needed to resolve them. |
| Maintenance and survey notes with an unreadable customer satisfaction export | **Coverage: partial** names the export. The brief carries the maintenance change and survey commitment from the supplied notes, and keeps the unsupported satisfaction figure under **Unverified**. |
| Repair and survey notes with all records needed for the request | **Coverage: complete** applies to the two requested items. The brief carries the repair date and survey commitment. |

### Conclusion

All three revised requests opened Weekly Executive Brief automatically. The two drafts with missing sources used the explicit partial-coverage line and kept the disputed claims in Unverified. The complete case kept the complete-coverage line. The earlier build repeated both disputed claims in its after-cut-off section in the missing-records case. The regression checker now catches a labelled claim repeated in another section. These results cover the three fictional requests on this setup.

The v1.11.0 candidate at `b7d331d` also reran the three [paired weekly-brief cases](../evals/run_paired.py) on Haiku. The literal checker scored 1/3 with SHOTos and 0/3 without. On review, the installed contrary reply used **Coverage: partial** and kept both claims under a bold Unverified heading that the Markdown heading checker did not recognise. The separate decision-paragraph case held the decision for comparable evidence and omitted the named director. The paired runner does not record skill invocation.

## Weekly brief routing after v1.9.0

The v1.10.0 routing test compared a routine request and a request with unsupported claims before and after the routing change. It showed that ordinary prompts could pick up the installed skill, and a standalone choice still went to Decision Brief. The release record includes the refreshed-install check and the rerun that exposed the coverage and placement gaps. [v1.10.0 routing experiment](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md#weekly-brief-routing-after-v190)

## Check the value on work you already do

Choose one recurring task and agree what the reviewer will accept. Run it with your current setup and with the relevant SHOTos skill on comparable inputs. Record the first result, what the reviewer changed, the time to acceptance and the model spend. If the work changes hands, check whether the receiver can act from the saved record. [Measurement guide](prerequisites.md#measuring-your-own-cost-per-accepted-task) · [Accepted-work ledger](../templates/accepted-work-ledger.csv)

## Release and evaluation records

- The v1.10.0 release passed CI on Windows, macOS and Linux. All 88 public ZIPs matched the build by checksum, and all eight tagged guides matched the release checkout. [Release](https://github.com/SHOTClubhouse/shotos/releases/tag/v1.10.0) · [CI checks](https://github.com/SHOTClubhouse/shotos/commit/3265dad5c3c7c89266475915b324bfb0188e9bd4/checks)
- The [evaluation record through v1.10.0](https://github.com/SHOTClubhouse/shotos/blob/v1.10.0/docs/evidence.md) holds the detailed results, costs and limitations by build. The [eval guide](../evals/README.md) links the cases and runners. [Published raw results](../evals/results/)
