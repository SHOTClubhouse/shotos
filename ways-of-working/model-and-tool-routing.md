# Model and tool routing

## What it is

Routing is choosing the right kind of worker and tool for each job instead of using one for everything. Some jobs need judgement, some need careful building, some are mechanical and some need a fresh pair of eyes. A model that is excellent at the first may be wasteful at the third, and a cheap one may be unsafe for the first. This page describes **classes** of model and tool, not named products, because the names and the rankings change every few months while the shape of the choice does not.

## Why it matters with agents in the loop

The cost of an agent task is not only the price per call. It is the price of the calls, the time, the rework when a weak choice fails, and the risk when a mistake gets through. Using the strongest option everywhere is expensive and slow. Using the cheapest everywhere produces plausible errors. Routing is how you spend care where it counts. It also supports [control 1, route the work](../rules/01-route-the-work.md): name the asset, job, risk, reader, route and proof on one line before you start.

## The classes of job

### Judgement

Deciding what matters, what to build, how to trade off, what a reader needs, whether an argument holds. Ambiguous, high stakes, hard to check by rule.

*Route to:* the strongest available model, with the owner's involvement. Give it the problem statement, the audience and the constraints. Expect to read and challenge the answer.

### Building

Producing a document, code, a design or an analysis to an agreed specification. The work is long and detailed, with clear acceptance.

*Route to:* a capable model with the acceptance card and the tools it needs. Build in small steps with checks in between. For code, a model with strong coding ability and access to the repository and test runner.

### Mechanical work

Renaming files, reformatting, extracting fields, converting formats, applying one rule to many items. Repetitive, well-defined, checkable by a script.

*Route to:* a smaller, cheaper model, or better still, a script. Prove the approach on three items, then run the rest (see [control 9, pilot before scale](../rules/09-pilot-before-scale.md)). Check the results by counts and spot checks.

### Independent review

Checking someone else's work against the acceptance. The value is independence, which means a different session, and where the risk justifies it, a different model, without access to the author's reasoning.

*Route to:* a capable model given only the acceptance, the evidence and the output. Size the review to the risk. See [control 7](../rules/07-independent-review.md).

## Start high, then step down

When you take on a new kind of task, start with a stronger option than you think you need. Get it right, with the checks passing and the owner satisfied. Then try the next step down on the same cases and compare using your eval set (see [evals-for-ai-output.md](evals-for-ai-output.md)). If the cheaper option passes the same cases at the same quality, move to it and record the choice. If it fails, stay where you were.

Starting low and moving up is false economy: you spend the time and risk learning that the cheap option cannot do it, and you may not notice the failure.

## Retest when models change

Models are updated, replaced and retired. A route that worked last quarter can quietly get worse or better. Keep the eval set and the cost record, and run them:

- When the provider announces a new version or retires an old one.
- When you change the instructions, tools or data.
- When quality complaints appear.
- On a regular schedule, even if nothing seems to have changed.

Record the model, version, date and result with each run. Do not rely on a general reputation ("this one is good at writing") for a decision your own cases could settle.

## Choosing tools

Use the least powerful tool that does the job:

- **Read-only access** before write access.
- **A script** for exact, repeated work; scripts do the same thing every time and can be reviewed.
- **Search and retrieval** for facts held elsewhere, so the model reads the source instead of recalling it.
- **A sandbox or draft area** for anything that could change shared state.
- **Connectors with narrow permissions,** scoped to one folder, one mailbox label or one project.
- **A human step** where the action cannot be undone.

Capability is separate from authority: that an agent can use a tool does not mean it may. See [control 3, the mode contract](../rules/03-mode-contract.md).

## Choosing output formats

Match the format to what happens next to the output.

- **Editable native formats first.** If the reader will change it, give them the format their tool edits: a word-processor document, a spreadsheet, slides, plain text or markdown. The people who maintain it can then maintain it.
- **HTML** for something that will be viewed on screen with links and layout, such as a report page or a prototype.
- **PDF only for sending.** A PDF is for a final copy that must not change, such as something emailed to a customer. Keep the editable source beside it.
- **Plain text or markdown** for notes, instructions and anything a script or another agent will read.
- **Structured formats** (CSV, JSON) for data going to another tool.
- **Do not produce a document nobody asked for.** An answer in the chat is often enough.

Always open the output in the format and tool it will be used in. See [definition-of-ready-and-done.md](definition-of-ready-and-done.md).

## Browser automation for real screenshots

When the output is visual (a web page, a slide deck exported to images, a form), the proof is a picture of the real thing. Use browser automation such as Playwright to load the page in a real browser, at the sizes users have, and capture screenshots. Then look at them. A model's description of a page is not the page. Automation also finds broken links, overflowing text and layout problems that code review misses. The screenshots go in the evidence folder for the task.

Automation is read-only by default: it looks, it does not click "buy", "send" or "delete". Anything that submits a form or posts to a live site waits for the owner.

## What good looks like

- Each job class has a stated default route, written once for the team.
- The route is chosen before work begins and recorded in the route line.
- Cheap options are used where the eval set shows they pass.
- Strong options are used where judgement or risk requires them.
- Choices are retested on a schedule and when things change.
- Outputs are in the format their next reader can use, and were checked there.

## Anti-patterns

- **One model for everything.**
- **The cheapest model on the highest-risk task.**
- **Leaderboard routing:** choosing by a public ranking instead of your own cases.
- **The author reviewing its own work.**
- **A PDF where an editable file was needed.**
- **Describing a page instead of looking at it.**
- **Giving a tool write access because it might be useful.**

## How it maps to the steps and rules

- **Brief:** note which jobs are judgement and which mechanical.
- **Brief:** build the eval set that makes routing testable.
- **Build:** use the routes; pilot mechanical runs on three items first.
- **Check:** record cost per accepted task by route.
- **Improve:** carry the route table to the next team and retest it.
- **Control 1:** the route line is written before the work.
- **Rule 3:** use browser automation to read back the real visual result.
- **Rule 4:** state which route produced which claim.

## A short example

Northgate Cycles needs three things in one week: a new returns policy page, product descriptions for two hundred items and a check of the new page before it goes live. The owner routes the policy wording as judgement: the strongest model drafts, a person decides. The descriptions are mechanical: a smaller model, piloted on three items, with a check script for length and banned phrases. The page check is independent review: a separate session reads only the acceptance and the finished page, and a browser script captures screenshots at phone and desktop width. The reviewer finds the returns window is stated as 30 days in the header and 28 in the footer. Six months later, when the provider retires the model used for descriptions, the team re-runs its twenty-case eval set on a replacement and compares cost and pass rate before switching.

## Further reading

- Jez Humble and David Farley, *Continuous Delivery*, on automated checks.
- Chip Huyen, *AI Engineering*, on model selection and evaluation.
- Public documentation for Playwright and for the agent tools you use.
- Daniel Kahneman, *Thinking, Fast and Slow*, on when quick judgement is unreliable.
- Provider documentation on model versions and retirement schedules.
