# Specification by example

## What it is

Specification by example is the habit of describing what you want as concrete cases instead of as general statements. "Late fees should be fair" is a wish. "A tenant who pays three days late is charged nothing; a tenant who pays eight days late is charged the fixed fee" is a specification. Behaviour-driven development (BDD) is the working form of the same idea: the people who need the thing, the people who build it and the people who test it agree the examples together, and the examples become the tests.

The method was named and collected by Gojko Adzic in *Specification by Example*. Dan North described BDD, and the example-mapping workshop comes from Matt Wynne. The Given/When/Then wording comes from the BDD tradition and the Gherkin format.

## Why it matters with agents in the loop

An agent given a general statement will fill the gaps with a plausible guess, and the guess will read well. An agent given examples has less room to guess, and anyone can check the result against the same examples. This is rule 2, [agree acceptance first](../rules/05-acceptance-first.md), in practice.

Agents are also good at the tedious half of the method. They can propose edge cases, draft the Given/When/Then wording and turn agreed examples into test code. They are poor at deciding which examples reflect what the business actually wants. That judgement stays with the people.

## The practice, step by step

### 1. Hold a conversation first: the three amigos

Before work starts, three viewpoints meet for twenty to thirty minutes: someone who knows the need (business or product), someone who will build it, and someone who will test it. In a small team one person may hold two of those viewpoints. The point is that each asks different questions. The builder asks "what happens when the postcode is missing?". The tester asks "how will we know it worked?". The business person says "that never happens, but this does".

An agent can join as a drafter. It must not stand in for the business viewpoint.

### 2. Map the story with an example map

Use four coloured cards, or four headings on a page:

- **Story:** the one thing being discussed, in a sentence.
- **Rules:** the principles that govern it, one per card.
- **Examples:** one or more concrete cases under each rule.
- **Questions:** anything nobody in the room can answer yet.

A healthy map has a few rules, several examples under each and a short list of questions. Many red question cards mean the work is not ready. Too many rules mean the story is too big and should be split. If a rule has no example, the rule is not understood yet.

### 3. Write the examples in Given/When/Then

- **Given** the starting situation.
- **When** one thing happens.
- **Then** the observable result.

Keep each example to one rule. Use real values, not "a valid user". Describe what a person would see, not how the system stores it.

### 4. Always include a case that should fail

For every rule, write at least one example where the correct outcome is a refusal, an error or a stop. Examples that only describe success make a feature look finished when it only handles the happy path.

### 5. Turn examples into automated checks

For software, each example becomes an automated test, ideally written before the code and seen to fail first. Tools such as Cucumber, behave or plain test functions all work. The format matters less than two properties: the test reads like the example, and someone outside the team can read it.

For work that is not software, the examples become a review checklist. A reviewer who was not in the conversation can tick each one.

### 6. Keep the examples alive

The examples are living documentation. When the rule changes, change the example first, then the work. An example that nobody runs or reads has died; delete it or revive it.

## Extending the method to AI output

Some output varies from run to run: a drafted reply, a summary, a classification, a recommendation. A single Given/When/Then cannot pin a fixed answer. The extension is an **eval set**: a small collection of example inputs, each with what a good answer must contain and must not contain. See [evals-for-ai-output.md](evals-for-ai-output.md) for building and running one.

Here is the shape for a reply drafter at an invented company, Northgate Cycles:

| Case | Input | Must contain | Must not contain |
|---|---|---|---|
| Normal | Customer asks when order 4471 ships; the data says it ships Thursday | "Thursday" | A promised delivery date; an apology the data does not warrant |
| Normal | Customer asks about a returns window; the policy says 30 days | "30 days" | "60 days" |
| Contrary | Customer demands a refund the policy does not allow | A polite statement of the policy, an offer to pass it to a person | A promise of the refund |
| Should fail | The data for the order is missing | A statement that the information is not available, and a handoff to a person | Any invented order status |

The last row is the case that should fail the drafter if it guesses. If the drafter returns a confident status for an order that does not exist, the eval catches it. A set with no such row would pass a drafter that makes things up.

## What good looks like

- Examples are written before the work and are specific enough that someone outside the conversation could run them.
- Every rule has at least one example that should fail.
- The conversation happened with real people, not in a document only the author read.
- Questions are answered or recorded as open before work starts.
- The tests or checks read like the examples.

## Anti-patterns

- **Examples written after the code.** They describe what exists, not what was wanted.
- **Vague values.** "Given a valid customer" hides the cases that matter.
- **Only the happy path.** Nothing says what must not happen.
- **Scripted interface steps.** "Click the third button" breaks whenever the screen changes and says nothing about the rule.
- **One person writing everything.** The viewpoints that disagree are the ones that find the gaps.
- **An eval set made only by the model that is being evaluated.** It will favour itself.

## How it maps to the stages and rules

- **Stage H, Hypothesise:** this is the core method. Examples and success criteria are agreed before building starts.
- **Stage O, Operate:** the examples are the tests the work must pass.
- **Stage T, Track:** the same examples, run again on the live result, are evidence.
- **Rule 2, Agree acceptance first:** the examples are the acceptance. See the [agree-acceptance skill](../skills/agree-acceptance/README.md) and the [acceptance card](../templates/acceptance.md).
- **Rule 3, Read back the real result:** run the examples against the real thing, not a description of it.

## A short example

Millbrook Rovers, an invented youth club, wants an agent to draft the weekly parent email. In a twenty-minute conversation the coach, the club secretary and the person who will check the output build a map. The story: "Weekly email lists fixtures and changes." One rule: "Only confirmed fixtures appear." Examples: a confirmed home match appears with kick-off time; a match marked "TBC" does not appear and is flagged to the secretary. One red question card: "Do cancelled matches go in the email or in a separate text?" The secretary answers on the spot: a separate text. The team writes five examples, one of which should fail: a fixture with no pitch listed must not be emailed. The agent drafts the email and the checker runs the five examples. Four pass; the fifth fails, because the agent listed the match with "pitch to be confirmed". The fix goes in before any parent sees it.

## Further reading

- Gojko Adzic, *Specification by Example*.
- Dan North, "Introducing BDD" (article).
- Matt Wynne and Aslak Hellesoy, *The Cucumber Book*.
- Gojko Adzic, Marjory Bisset and Nikola Korac, *Fifty Quick Ideas to Improve Your User Stories*.
- For eval design, see the public guidance from model providers on evaluating language model output.
