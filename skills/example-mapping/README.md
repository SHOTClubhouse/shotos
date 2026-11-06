# example-mapping

**Find the rules in a change, test each with concrete examples, list what nobody knows, then write the settled examples as checks.**

The agent runs a short example-mapping session: story, rules, examples per rule, open questions, then Given/When/Then for the examples that are settled. It follows specification by example and behaviour-driven development.

It belongs to the Hypothesise stage. It serves rule 2, Agree acceptance first, and rule 4, Claim only what you can show.

## The problem it solves

Millbrook Rovers youth club asks for a "sibling discount" on its membership form. The treasurer thinks it means 10% off the second child. The registrar thinks it means a flat 15 pounds off from the third child. The form gets built, charges the wrong amounts for six families and needs a manual refund round.

## What the agent does differently

It writes the discount rules out, gives each rule examples with real prices and family sizes (two children, three, step-siblings in different age groups) and notices the two readings give different amounts for the same family. That becomes an open question for the treasurer, not a guess in the code. See [examples/example-mapping/output.md](../../examples/example-mapping/output.md).

## When to use it, and when not to

Use it before building anything with business rules, and when a request is too vague to turn into checks. Skip it for changes with no rules, or where settled examples already exist.

## Who it is for

- **Product owner or manager:** surfaces disagreements before they cost money.
- **Developer or builder:** gets examples that become tests.
- **Anyone briefing an agent:** a clearer starting point than a one-line request.

## How to use it

> Run an example-mapping session on the sibling discount for the membership form. Ask me anything you cannot settle.

Answer the open questions, then confirm the checks.

## How it connects

- **Before:** [hypothesis-card](../hypothesis-card/README.md) says why the change is worth making.
- **After:** [agree-acceptance](../agree-acceptance/README.md) takes the settled checks to the owner, and [eval-set](../eval-set/README.md) covers any part where output varies.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Use real numbers and names in examples. Vague examples hide disagreement.
- A long list of open questions is a result, not a failure. It tells you the story is not ready.
- Keep draft examples marked as draft until someone with authority confirms them.

## Limits

- The agent cannot know your business rules; it finds them in what you give it and asks about the rest.
- A map written without the person who owns the rules is a list of guesses.
- It does not build or test anything.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/example-mapping/input.md) and [output](../../examples/example-mapping/output.md).
