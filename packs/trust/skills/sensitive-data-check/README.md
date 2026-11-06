# sensitive-data-check

**Check work that touches special-category or children's data, and stop and escalate when consent is missing.**

This skill reviews work that handles special-category data (such as health, ethnicity, religion, biometrics) or children's data. It checks data minimisation, lawful basis and consent recorded, parental consent for children, retention, who can see the data, images of children and the safeguarding escalation path. When consent is missing, it stops and escalates to the named person instead of carrying on.

It supports the Scope stage. It serves rule 1, Stop at the boundaries, and rule 4, Claim only what you can show.

## The problem it solves

Millbrook Rovers youth club wants to add a medical-conditions field and team photos to its sign-up form. A well-meaning volunteer would build it and publish it. The questions that matter come first: is each field needed, who agreed to it, did a parent consent for each child, who can read it, how long is it kept, and who does a coach tell if a photo raises a worry. The check gets those answered, or stops the work.

## When to use it, and when not to

Use it when work collects, stores, shares or publishes health details, other special-category data, anything about children, or images of children. Use it at the start of the work and again before release.

Skip it for work that holds no personal data at all. It is not legal advice and it does not replace a data protection officer or a designated safeguarding lead.

## Who it is for

- Clubs, schools and charities working with young people.
- Product owners adding a form, upload or profile field.
- Agents asked to build, move or publish records about people.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> We are adding a medical conditions field and team photos to our junior sign-up form. Run a sensitive data check before we build it.

You get a checklist with each item marked met, not met or unknown, and a decision: proceed, proceed after fixes, or stop and escalate. If consent is missing, you get the name of who to escalate to and nothing is built or published.

## How it connects

- **Before:** [quarantine](../../../records/skills/quarantine/README.md) holds files that may contain this kind of data.
- **Related:** [public-exposure-check](../public-exposure-check/README.md) checks the same work before it is shared.
- **Rules:** [04, stop-boundaries](../../../../rules/04-stop-boundaries.md) and the data governance guardrail in [rules/guardrails/README.md](../../../../rules/guardrails/README.md).

## Needs

Nothing beyond the agent. It needs the plan or design, and whatever consent records and policies exist. It does not see systems it has not been given.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 1 of 3, Sonnet 3 of 3, Opus 3 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Ask for the consent record itself, not a statement that consent exists.
- Collect less: if a field does not change a decision, drop it.
- Name the person who handles safeguarding concerns before the work starts.
- Remember that a photo of a child is personal data and may reveal more than the name.

## Limits

- It checks that the questions have answers. It cannot judge whether a legal basis is sound; the data protection lead decides.
- Rules differ by country and by organisation. The skill names the checks, not the law.
- It cannot confirm consent that was given outside the records it is shown.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/sensitive-data-check/input.md) and [output](../../examples/sensitive-data-check/output.md).
