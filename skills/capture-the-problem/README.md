# capture-the-problem

**Write down what is actually wrong before anyone builds anything.**

This skill turns rough notes, a complaint or a request into a one-page problem statement. It names who has the problem, what it costs today, what nobody knows yet and the cheapest test. It then stops and hands the page to a named person to confirm.

It supports the Brief step and rule 2, Agree acceptance first, because you cannot agree what done looks like for a problem nobody has written down.

## The problem it solves

A sales lead tells an agent: "We need an AI chatbot on the website. People keep emailing the same questions and the team is drowning. Can you get one built this month?"

A helpful agent starts building. Nobody has counted the enquiries, checked how many repeat or looked at whether the answers are already on the site. The team might spend a month on a chatbot for a problem that a clearer menu would have fixed.

## What the agent does differently

Without the skill, an agent can give a sensible answer and still skip the structure: no owner, no list of unknowns, no first test. With the skill, it produces a statement like the one in [examples/capture-the-problem/output.md](../../examples/capture-the-problem/output.md).

It keeps what people observed apart from what they believe and what they asked for:

> - Observed: "People keep emailing the same questions." "The team is drowning."
> - Believed: a chatbot would reduce the load.
> - Asked for: an AI chatbot on the website this month.

It writes "not measured" where the notes give no number, and the problem itself contains no solution:

> The sales team spends time answering repeated prospect questions by email, which delays replies and takes time away from selling.

Then it proposes a test that could kill the idea:

> Tag the last 100 enquiry emails by question type (about two hours). If fewer than a third are repeats, a chatbot is the wrong fix.

The statement is marked "waiting for the head of sales". The agent does not start building.

## When to use it, and when not to

Use it at the start of anything non-trivial, when a request describes a solution without a problem, or when several people describe the same issue differently.

Skip it for a small, clear change that is cheap to undo, such as a typo, a broken link or a one-line config change. One of the eval cases checks this: asked to fix one misspelt word, the agent should fix it and not produce a problem statement.

## Who it is for

- **Solo founder:** stops you building the exciting answer to the wrong question.
- **Product owner or analyst:** a quick, honest first page before discovery work starts.
- **Small team lead:** gives people with different views the same page to argue over.
- **Business unit leader:** turns "we need a tool" requests into a problem and a cheap test before money moves.
- **Engineering or practice lead:** keeps solution-shaped tickets out of the backlog.
- **Enablement coach:** a ready exercise for teaching people to separate observation from belief.

## How to use it

Install SHOTos as described in the [main README](../../README.md#install). Then give the agent the request in plain words, for example:

> Here are notes from our sales lead: "People keep emailing the same questions and we need a chatbot this month." Help us get clear on the problem before we decide anything.

You get back a statement on [template.md](template.md), under one page, with the owner line left for a person to fill in.

On paper: print the template, copy the quotes in under "What we heard", and fill in each heading in order, following the steps in [SKILL.md](SKILL.md). The most useful lines are "What we don't know" and "Cheapest first test".

## How it connects

- **Next:** [agree-acceptance](../agree-acceptance/README.md) takes the confirmed problem and turns it into checks the work must pass.
- **Throughout:** [report-with-evidence](../report-with-evidence/README.md) makes the agent's own account of what it found checkable.
- **At the end:** [evidence-handoff](../evidence-handoff/README.md) passes the open unknowns to whoever runs the test.

## How it is tested

The skill has five cases in [evals/cases.json](../../evals/cases.json). Three are normal (a chatbot request, a slow session planner, wrong invoices). Two are contrary: a typo fix that should not trigger the skill, and a "40% churn because of pricing" claim that should be treated as unverified.

From the paired run in [docs/evidence.md](../../docs/evidence.md): capture-the-problem passed 5 of 5 cases with SHOTos and 2 without, at $0.39 against $0.29.

The caveats, quoted from that page: "One run per case per condition, on one model. Agent output varies between runs." Also: "The grader checks for key words and phrases, and some match the skills' own wording, which favours the 'with' side." The size of the gap should not be taken at face value.

## Tips and common mistakes

- Paste the original words, not your summary of them. The skill cannot separate observation from belief in a paraphrase.
- Reject a problem statement that hides a solution. "We lack a chatbot" is a solution in the wrong place.
- Make the test cheap enough to run this week. If it takes a month, it is a project.
- Have a person confirm the statement. An agent cannot confirm its own page.

## Limits

- The agent can only work from the notes it is given. It cannot tell you how many enquiries there were.
- A clear statement is not a correct one. The unknowns list is where the risk sits.
- Tested on one model, one run per case. Codex has not been tested.
- The skill proposes a test. It does not run it.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/capture-the-problem/input.md) and [output](../../examples/capture-the-problem/output.md).

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 5 of 5, Sonnet 5 of 5, Opus 5 of 5. Without: Haiku 4 of 5, Sonnet 4 of 5, Opus 5 of 5. See [evidence](../../docs/evidence.md) for how to read this.
