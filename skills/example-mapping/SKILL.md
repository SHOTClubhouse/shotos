---
name: example-mapping
description: "Runs an example-mapping session: story, rules, concrete examples, open questions, then settled examples as Given/When/Then. Use when building anything with business rules, or when a request is too vague to turn into checks."
---

# Map examples before building

Rules are abstract and people read them differently. Examples are concrete and expose the difference. Work through a change by rules, then examples, then questions, then write the settled examples as checks.

**Step:** Brief. **Rules:** 2 Agree acceptance first; 4 Claim only what you can show.

## When not to use this

Skip it for a change with no rules to speak of, such as correcting a typo, or when the owner has already supplied settled examples. Do not invent business rules to fill the map; an unknown rule becomes an open question.

## Steps

1. **State the story.** One sentence: who wants what, and why. Name the person who can answer questions about it. If nobody can, say so; the map will be mostly questions.
2. **List the rules.** Write each rule the change must follow as a short sentence. Include rules stated in the request, rules found in existing documents or code (cite where), and rules implied but not yet confirmed (mark them `to confirm`).
3. **Give examples for each rule.** For every rule, write at least two concrete cases with real values: one that follows the rule and one at its edge or that breaks it. Use names, amounts and dates, not "a customer" and "some amount".
4. **Collect open questions.** Whenever the rules or examples disagree, or an example cannot be settled from what you know, write a question instead of an answer. Keep each question to one sentence and say who could answer it.
5. **Check the size.** If one rule has more than about five examples, or there are more than a handful of open questions, say the story is too big or too vague and propose splitting it or pausing for answers.
6. **Convert settled examples to Given/When/Then.** Only examples the owner has confirmed (or that come straight from a source) become checks. Mark the rest `draft`.
   - Given a starting situation, when something happens, then this observable result.
7. **Add one case that must fail or refuse,** drawn from the edge examples.
8. **Hand over.** The settled checks go to [agree-acceptance](../agree-acceptance/README.md) for the owner's yes. The questions go to the people who can answer them. Do not start building until the blocking questions are answered.

## Output

Use [template.md](template.md). Save it with the work, for example `.work/<task>/example-map.md`.

## Checks

- Every rule has at least two examples with real values.
- Questions are written as questions, not turned into assumed answers.
- Only confirmed examples are written as checks, and one of them refuses or fails.
- The map says if the story should be split.
