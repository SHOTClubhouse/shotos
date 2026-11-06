# Language

## What it is

A glossary of the words SHOTos uses, with the meaning each one carries here. Teams work better when a word means one thing. "Done" that means "I stopped" and "done" that means "the owner accepted it" are two different words that happen to look alike, and mixing them is how a report ends up saying more than the evidence supports. When in doubt, use the word as defined below, or say plainly what you mean.

## Why it matters with agents in the loop

Agents write reports fluently. Fluent language can claim more than was done. A careful glossary is one of the cheapest controls there is: if "executed" and "accepted" mean different things, an agent that says "executed" has not claimed acceptance, and a reader knows it. See [claims](../docs/claims.md) and [control 10, claim discipline](../rules/10-claim-discipline.md).

## Glossary

**Acceptance.** The agreed conditions under which a named person will say the work is done: the checks, including at least one case that should fail, and the boundaries. Written before the work starts. Also the act of that person saying yes. An agent never accepts its own work.

**Eval.** A test for output that varies. It checks a set of example inputs against what a good answer must and must not contain. See [evals-for-ai-output.md](evals-for-ai-output.md).

**Eval set.** The collection of eval cases for one piece of work, kept in version control and re-run when anything changes.

**Read-back.** Checking the actual result in its real home before reporting it: opening the published page, the sent message in the recipient's view, the deployed system, the file in the shared folder. Reading your own description of the work is not read-back.

**Claim.** A statement in a report that something is true, such as "tests pass", "the page is live" or "the email was sent". Each claim should be checkable. The [Claims block](../docs/claims.md) lists them.

**Evidence.** What a person or tool can look at to check a claim: a test run, a log line, a screenshot, a receipt, a file at a path. Evidence is separate from the claim and can be inspected by someone who was not there.

**Installed.** The setup exists in the place it should: the skill is in the folder, the hook is configured. It says nothing about whether it ran or worked.

**Executed.** The thing ran, and there is a record of the run. It does not say the result was correct.

**Accepted.** A named person checked the result against the agreed acceptance and said yes. Only this word means the work is done. Installed and executed are not accepted.

**Owner.** The one named person who decides whether work is accepted and who answers for the result. Not a team, not a role title, not an agent.

**Boundary.** An action that needs the owner's yes before anyone, human or agent, does it: sending, spending, deleting, publishing, deploying, or changing someone else's work. Rule 1.

**Pilot.** A first run on a small number of units (three or fewer), checked by a person, before running the rest. See [control 9](../rules/09-pilot-before-scale.md).

**Graduation.** The process by which a class of task earns more autonomy through logged acceptance, one rung at a time, and loses it again if quality drops. See [control 12](../rules/12-graduation.md).

**Route.** The choice of worker, tool and checks for a job, named before the work starts. See [model-and-tool-routing.md](model-and-tool-routing.md).

**Lens.** A particular viewpoint applied to a piece of work to see what a general reading misses, such as the customer's, the auditor's or the newcomer's. A lens changes what you notice, not what is true.

**Step.** One of the five parts of the SHOTos work loop: Brief, Build, Check, Hand over and Improve. Each has an exit check.

**Rule.** One of the four short statements that hold inside every step: stop at the boundaries, agree acceptance first, read back the real result, claim only what you can show.

**Control.** One of the twelve detailed agent controls that spell out the four rules, each in its own file under `rules/`.

**Guardrail.** One of the six concerns that cut across every step: data governance and risk, security, scale, productivity, pace and quality. A guardrail is something to keep in view, not a step.

**Pack.** A bundle of skills for one area of work, installed together.

**Skill.** A packaged set of instructions for one kind of job, with a purpose, steps, an output and checks. It lives in a folder with a `SKILL.md`. See [the skill format](../docs/skill-format.md).

**Hypothesis.** A testable bet written as "We believe that X will result in Y, and we will know because Z changes."

**Baseline.** The measure of how things are before a change, against which the result is compared. "Not measured" is a valid baseline entry when it is true.

**Draft.** Prepared but not sent, published or released. An agent produces drafts by default for anything that could act outside the project.

## Phrases to avoid

Some phrases claim more than anyone has shown. Replace them with a statement of what was checked.

| Avoid | Why | Say instead |
|---|---|---|
| "Fully tested" | Nothing is fully tested; it hides what was not covered | "These 14 checks ran and passed; these two were not run" |
| "Production-ready" (with no evidence) | Nobody can tell what ready means | "Passes the agreed acceptance, runs in staging, has a rollback; no load test yet" |
| "AI-verified" | A model agreeing with itself is not a check | "Reviewed by an independent session against the acceptance; accepted by [owner]" |
| "Zero defects" or "bug-free" | Absence of found defects is not absence of defects | "No defects found in these checks" |
| "Works" (alone) | Works for whom, where, how often | "Passes all five examples on the live page as of [date]" |
| "Done" (alone) | Could mean stopped, executed or accepted | "Executed; awaiting acceptance" or "Accepted by [owner] on [date]" |
| "Secure" | A claim about absence of risk | "Secret scan and dependency check clean; threat review not done" |
| "Guaranteed" | No agent output is | "Expected to, based on [evidence]" |
| "Approved" (by an agent) | Approval is a person's | "Passed the checks; awaiting approval" |
| "100% accurate" | Needs a defined test and sample | "Matched the source in 40 of 40 sampled rows" |
| "Sent" (with no receipt) | May only be drafted | "Sent; receipt attached" or "Drafted; not sent" |
| "Industry standard" or "best practice" | Appeals to authority without naming one | Name the source, or say why it suits this case |

The pattern behind the list: a good claim names what was checked, where, when and by whom, and says what was not checked.

## Using the words

- Use the defined word, not a near neighbour. Do not say "validated" when you mean "executed".
- Where a number is an estimate or an example, label it as one.
- Where content is quoted, say so. Where it is inferred, say so. Where it is invented to illustrate, say so. See [control 10](../rules/10-claim-discipline.md).
- If a reader would have to ask "who checked?" or "where?", the sentence is not finished.

## What good looks like

- A new team member can read a report and tell what was installed, what ran and what was accepted.
- Reports separate claims from evidence.
- Avoided phrases do not appear without the evidence beside them.

## Anti-patterns

- **"Done" as a mood.**
- **Hedged mush:** "should be fine", "looks good", with nothing behind it.
- **Adjectives in place of evidence:** "thorough", "comprehensive", "extensive".
- **Borrowed authority:** "as the model confirmed".
- **Words redefined quietly** halfway through a project.

## How it maps to the steps and rules

- **All steps:** the same words in every report.
- **Check:** the report's claims use these terms and cite evidence.
- **Hand over:** the handoff states which items are accepted and which are only executed.
- **Rule 4:** claim only what you can show; this page is the vocabulary for that.

## A short example

An agent finishes a script for Northgate Cycles that renames supplier files. The first draft of its report says: "The script is fully tested and production-ready." The owner asks, "Tested how?" The agent rewrites: "Executed on three sample files in a copy of the folder; all three renamed as expected (log at `.work/.../evidence/run1.log`). Not run on the full folder. Not accepted: awaiting your yes. It deletes nothing." Every word is now checkable, and the owner knows exactly what to approve.

## Further reading

- George Orwell, "Politics and the English Language" (essay).
- Gojko Adzic, *Specification by Example*, on a shared language for requirements.
- Eric Evans, *Domain-Driven Design*, on ubiquitous language.
- Nicole Forsgren, Jez Humble and Gene Kim, *Accelerate*, on measures with agreed definitions.
