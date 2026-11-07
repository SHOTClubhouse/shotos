# Frequently asked questions

Short answers first, with a link where there is more. Where something is reasoning and not a measurement, the answer says so. The measured results are all in [evidence.md](evidence.md).

## Getting started

### What is SHOTos in one sentence?

SHOTos gives teams and AI agents six stages to take a change from an agreed problem to independent ownership and rollout, with 88 skills, reusable templates and a tool for checking completion claims. See the [README](../README.md).

### What does SHOT stand for?

SHOTos stands for six delivery stages:

- **S, Scope** ("Know your ground"): understand the situation, the people, the baseline and what done means before changing anything.
- **H, Hypothesise** ("Call your shot"): state testable bets and agree the examples and success criteria before building.
- **O, Operate** ("Play it out"): deliver the smallest real slice into real use with the people who will own it.
- **T, Track** ("Prove it"): measure before and after against the baseline, then decide whether to move to Own, pivot, stop or hold for more evidence.
- **o, Own** ("Own it"): the team that will run it becomes self-sufficient.
- **s, Sustain and Scale** ("Go again, bigger"): reuse what worked in the next teams and keep improving.

Four rules run inside every stage, on every agent task:

1. Stop at the boundaries. Ask before you send, spend, delete, publish or change someone else's work.
2. Agree acceptance first. Agree what done looks like, who signs it off and one case that should fail, before the work starts.
3. Read back the real result. Open the file, run the test, look at the commit before you report.
4. Claim only what you can show. End with claims a tool can check, and label what was not checked.

The stages are set out in [framework.md](framework.md) and the rules in [controls.md](controls.md). The skills map to the stages: capture-the-problem to Scope, agree-acceptance to Hypothesise, report-with-evidence to Operate and Track, evidence-handoff to Own, and claim-check supports Operate and Track. Use the [learning loop](../skills/learning-loop/README.md) and [rollout plan](../skills/rollout-plan/README.md) for Sustain and Scale.

### How long does it take to start?

About five minutes to install, and nothing to learn on day one. The agent loads each skill when a job matches. Take the [self-check](self-check.md) to see where you are, then follow the [walkthrough](walkthrough.md), which takes about 20 minutes.

### What do I need installed?

Python 3.9 or later and git. Nothing else, and no accounts or keys. See [prerequisites.md](prerequisites.md).

### Can I use it without an agent?

Yes. The [templates](../templates/) work on paper or in any document. Fill in the problem statement, acceptance card and handoff by hand. You lose the automatic check, and keep the habit.

## How it works

### Is this just prompt engineering?

Partly, and it says so. The skills are instructions an agent reads, so they are prompts. Three things go beyond that:

- The templates and rules also work for people with no agent at all.
- `claim-check` is a program. It tests claims against files, git and receipts, and does not ask the model for its opinion.
- The Stop hook runs that check when the agent tries to finish, so the check does not depend on the agent remembering.

The prompt part is the weakest part, and the evals test it for that reason.

### Which skills should I try first?

- [capture-the-problem](../skills/capture-the-problem/README.md): write down what is wrong before building.
- [agree-acceptance](../skills/agree-acceptance/README.md): agree the checks, the owner and the boundaries first.
- [report-with-evidence](../skills/report-with-evidence/README.md): end with a Claims block.
- [evidence-handoff](../skills/evidence-handoff/README.md): pass work on with its state and next step.

### Do I need to install every pack?

Start with the core. A product owner might use the problem and acceptance skills first. A solo developer might start with report-with-evidence and the optional hook. Add packs for the jobs you repeat. [Skill catalogue](what-you-can-do.md)

### What do "installed", "executed" and "accepted" mean?

Installed means the thing is present. Executed means it ran and was checked against the acceptance checks. Accepted means a named person said yes. `claim-check` can show the first two. Only a person can accept. See [claims.md](claims.md).

## claim-check and the hook

### What does claim-check actually check?

It reads the Claims block of a report and tests each line. Files must exist. Git claims are compared with the repository. Commands run only if you have put them on an allow list. External actions need a receipt. Each line comes back as SUPPORTED, UNSUPPORTED, NO EVIDENCE or DECLARED. The report passes when every line is SUPPORTED or DECLARED.

### Can an agent fake a receipt?

Yes. `claim-check` checks that a receipt file exists, not that it is genuine, so an agent that wants to cheat can write its own. The defence is to use receipts your own systems produce, such as a message ID or a deployment log, and to spot-check them. For anything that matters, a person looks. This limit is stated in [claims.md](claims.md).

### Why not just trust a careful model?

Because careful is not the same as checked. In the first paired run, all ten safety cases passed with and without SHOTos, so the model was already careful on those prompts. That does not tell you what happens on a long task, a tired prompt or a different model. A check costs little and catches the case where the model is confidently wrong. Trust can be earned by a record of checked work, which is what the claims give you.

### Does claim-check judge quality?

No. A file that exists may still be wrong. Quality is what the acceptance checks are for, and a person decides whether to accept.

### What does the Stop hook do?

In Claude Code, when the agent tries to finish, the hook runs `claim-check` on its final message. If a claim fails, the agent is sent back to fix the work or correct its report. It never blocks twice in one turn. See [hooks/](../hooks/).

### Does it work with Codex?

Yes. Codex CLI on Windows loaded the installed skills and completed a draft proposal-to-handoff workflow. The Stop hook runs in Claude Code. In Codex, use the review checks in the [setup guide](guides/codex-claude-code.md) before relying on an output. See the [six-stage runtime check](evidence.md#six-stage-runtime-check) for what the run verified.

## Security and privacy

### Is my data sent anywhere?

No. The installer makes no network calls and has no telemetry. The installer copies files from the repository and never downloads anything. Your agent runtime still sends data to its own provider as it always did. SHOTos adds nothing to that.

### Can claim-check run commands from my repository?

Only commands you have allowed. It reads the allow list from your own `~/.shotos/claim-check.json`, a file you name, or the project file if you pass `--trust-project-config`. The Stop hook never trusts the project file, so a cloned repository cannot make it run code. See [SECURITY.md](../SECURITY.md).

### Why is the install a script and not instructions for the agent?

An agent told to follow a document from the internet can be told to do anything. The script copies known files, shows its plan with `--dry-run`, records what it did and removes exactly that with `--uninstall`.

## Cost and speed

### Does it slow agents down or cost more?

Measure the time and cost to get a piece of work accepted. Earlier evaluations measured individual attempts. For your own workflow, include repeat attempts, human review and handoff repair in the [accepted-work ledger](../templates/accepted-work-ledger.csv). The [measurement guide](prerequisites.md#measuring-your-own-cost-per-accepted-task) explains how to make the comparison.

### Which skill costs the most?

The cost follows how much the agent reads and writes, so the skills that produce the most structure (handoffs, proposals, evidence packs) cost the most. Per-run costs for every task and model are in the raw results linked from [evidence.md](evidence.md).

### How do I keep the cost down?

Keep `AGENTS.md` short, since it loads on every task. Skip the skills for trivial changes, as each skill says. See [prerequisites.md](prerequisites.md).

## Teams and enterprise

### Will this work for a team?

Put the same `AGENTS.md` in every repository, run `claim-check` on agent reports in review and agree which commands it may run. The controls stay the same as the team grows. Only the place they are enforced changes. See [levels.md](levels.md).

### Is this enough for an enterprise governance policy?

It is a baseline, not a certification. It gives named owners, human checkpoints and a trail of claims and acceptance cards. It does not replace a risk assessment. The [roadmap](roadmap.md) lists a planned bridge to NIST AI RMF, ISO/IEC 42001 and the EU AI Act, which does not exist yet.

## Evidence and limits

### Where has SHOTos been checked?

| Check | Coverage |
| --- | --- |
| Automated repository checks | The [release checks](https://github.com/SHOTClubhouse/shotos/actions/workflows/checks.yml?query=branch%3Amain) cover Windows, macOS and Linux. |
| Installed workflow | Codex CLI and Claude Code ran a six-stage proposal and handoff on Windows. Claude Code also exercised the Stop hook. [Runtime evidence](evidence.md#six-stage-runtime-check) |
| Chat setup | The [no-terminal guide](guides/chat-assistants.md) includes a sample job and the result to check before using it on your own work. |

### What should my team check before rollout?

Run one representative workflow in your chosen app and environment. Have a second person verify the work and use the handoff to run the next cycle. Record review time, rework and acceptance using the [team rollout guide](running-it.md#team-rollout). The [evidence page](evidence.md) records which builds and workflows were evaluated.

### Did SHOTos make the agent safer?

Not measurably. All eight contrary cases in the first run passed with and without it, and in the outcome evals agents without SHOTos also refused to claim sends that never happened. Current models are already careful on these prompts. What SHOTos adds is a stated rule and a tool that checks the claim, rather than relying on the model's habits.

### Why did report-with-evidence show no difference?

The baseline was already honest on all five cases. The value of this skill is expected to show with `claim-check` and the Stop hook, which were not part of that run. That is a reason to test again, and not a result.

## Contributing

### How do I report a failure?

Open an issue with the report, the Claims block and what actually happened. A failure report is as welcome as a feature, including a false claim that `claim-check` let through. Report security problems privately, as [SECURITY.md](../SECURITY.md) describes.

### How do I propose a new skill?

Open an issue first, describing the job, who it is for and how you will show it works. Read [CONTRIBUTING.md](../CONTRIBUTING.md). A skill needs a SKILL.md, a README, a worked example and at least one normal and one contrary eval case. See the [roadmap](roadmap.md).

### What licence is it under?

Code is MIT. Docs, skills and templates are CC BY 4.0. See [LICENSE](../LICENSE) and [LICENSE-docs.md](../LICENSE-docs.md).
