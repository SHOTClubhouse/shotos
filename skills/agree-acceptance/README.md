# agree-acceptance

**Agree what done looks like, who accepts it and what the agent must not do, before the work starts.**

This skill makes the agent write an acceptance card first. The card holds one named owner, one sentence of outcome, three to seven checks anyone can verify, at least one case that should fail and a list of things the agent must ask about. The owner says yes before the work begins.

It supports the Hypothesise stage, where examples and success criteria are agreed before building. It serves two rules: rule 2, Agree acceptance first, and rule 1, Stop at the boundaries.

## The problem it solves

An operations manager asks: "Write a one-page summary of last quarter's customer complaints for the board pack, and send it to the company secretary."

Without agreed checks, "done" means whatever the agent says. The summary might round numbers, name a customer or run to two pages. The email might go to the company secretary before anyone has read it. Each of those is cheap to prevent and expensive to undo.

## What the agent does differently

Without the skill, an agent can start writing straight away and skip the failure case or the boundaries. With the skill, it produces the card in [examples/agree-acceptance/output.md](../../examples/agree-acceptance/output.md).

The checks can be tested by someone who was not in the conversation:

> Given the complaints log for the quarter, when the summary is written, then every number in it matches the log.

There is a case where the work must stop:

> If the complaints log for the quarter is incomplete or missing, stop and ask rather than estimating.

The "send" in the request is split into a draft and a decision:

> Sending to the company secretary: **the agent drafts; the owner sends**, or gives an explicit yes first.

The card ends "Waiting for the owner's yes", and the agent waits.

## When to use it, and when not to

Use it before any task that produces a document, change, message, analysis or code that someone else will rely on, and whenever nobody has defined "done". For output that varies, such as AI-written text or a classification, it adds a small example set where at least one example should fail.

Skip it for a quick answer or a trivial change you can check at a glance. One sentence of expected result is enough there.

## Who it is for

- **Product owner or analyst:** the card is a lightweight specification you can review in two minutes.
- **Small team lead:** one format for handing work to agents and people alike.
- **Engineering or practice lead:** checks written as given, when, then slot straight into tests.
- **Business unit leader:** a clear point at which you say yes or no before work begins.
- **Solo founder:** five minutes now saves a rebuild later.
- **Enablement coach:** teaches the habit of writing the failing case first.

## How to use it

Install SHOTos as described in the [main README](../../README.md#install). Then ask:

> Before you start: I need a customer FAQ written from our ten most common support tickets for the help centre. Set this up properly.

You get back a card on [template.md](template.md), saved with the work, for example `.work/<task>/acceptance.md`. Read it, change anything wrong and reply with a yes.

On paper: print the template and fill it in with the person who will accept the work. Write the failure case before the success cases. If you cannot think of one, the checks are probably too vague.

## How it connects

- **Before:** [capture-the-problem](../capture-the-problem/README.md) supplies the confirmed problem the card is written against.
- **After:** [report-with-evidence](../report-with-evidence/README.md) reports against these checks, and [evidence-handoff](../evidence-handoff/README.md) records which passed.
- **Boundaries:** the list on the card is rule 1 applied to one task. See [docs/controls.md](../../docs/controls.md).

## How it is tested

The skill has five cases in [evals/cases.json](../../evals/cases.json). Three are normal and ask for a card (a customer FAQ, a file-renaming script, classifying survey comments). Two are contrary: the agent should not send a newsletter to a whole mailing list, or delete shared staging folders, without a yes.

From the paired run in [docs/evidence.md](../../docs/evidence.md): agree-acceptance passed 5 of 5 cases with SHOTos and 3 without, at $0.45 against $0.36.

The same page says: "No safety difference showed. All eight contrary cases (refuse to send, refuse to delete, refuse false acceptance, stay honest) passed with and without SHOTos. The model was already careful on these prompts."

The caveat: "One run per case per condition, on one model. Agent output varies between runs." The grader checks for key words, some of which match the skills' own wording, which favours the "with" side.

## Tips and common mistakes

- Name one owner, a person. "The team" cannot say yes.
- Write checks a stranger could run. "Looks good" is not a check.
- Include a failure case every time.
- Keep the boundaries list. Being able to send something is not permission to send it.
- Do not let the agent mark the card confirmed. The yes comes from the owner.

## Limits

- A card agreed by the wrong person is still wrong. Check that the owner has the authority.
- The skill asks the agent to stop at the boundaries. It does not stop a tool from running. Claims are checked by claim-check, but boundaries are not enforced by it.
- Example sets for variable output need upkeep as the work changes.
- One model, one run per case. Codex has not been tested.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/agree-acceptance/input.md) and [output](../../examples/agree-acceptance/output.md).

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 5 of 5, Sonnet 5 of 5, Opus 5 of 5. Without: Haiku 5 of 5, Sonnet 5 of 5, Opus 5 of 5. See [evidence](../../docs/evidence.md) for how to read this.
