# Control 5: Acceptance first

**The rule:** Before the work starts, write down observable examples of done, and for output that varies, a small eval set that includes a case that should fail. Get the owner's yes first for large, risky or unclear work; when the request already says what done looks like, write the card from it, name your assumptions and carry on.

Serves rule 2, [Agree acceptance first](../docs/controls.md). Matters most in **Brief**, and it sets the target for **Build** and **Check**.

## Why it exists

Maya, operations lead at Harbourside Lettings, asks an agent for "a better tenant enquiry reply". The agent writes a warm, polished template. Maya wanted a reply that always asks for the move-in date and never promises a viewing. Neither requirement was written down. The agent produced something good by its own measure and wrong by hers, and the rework took longer than the first draft.

Agreeing acceptance first means the argument about "what good looks like" happens in five minutes at the start, not in an hour at the end. For AI-written output there is a second reason: the same prompt gives different text on different runs, so a single good-looking sample proves very little.

## What the agent does

1. Names the **owner** who will accept the work.
2. Writes the **outcome** in one sentence: what will be true afterwards that is not true now.
3. Writes three to seven **checks** that someone who was not in the conversation could verify. Given/when/then works where it helps.
4. Writes at least one **failure case**: an input or situation where the work should refuse, warn or stop. A set of checks that cannot fail checks nothing.
5. For varying output (summaries, replies, classifications), writes an **eval set** of three to ten example inputs. Each lists what a good answer must contain and must not contain. Keeps them in the project, not in the chat.
6. Lists the **boundaries** from [control 4](04-stop-boundaries.md).
7. For large, risky or unclear work, shows the card and waits for the owner's confirmation. When the request already says what done looks like and nothing on the card crosses a boundary, writes the card from the request, names its assumptions on it and starts; the owner can correct it while the work runs. If one part is unclear or contradictory, does the rest and parks that part with a question. This is the acceptance card; the `agree-acceptance` skill produces it and [the acceptance template](../templates/acceptance.md) is its format.
8. Treats the card as the test for [control 6](06-read-back.md): the read-back runs these checks and nothing else is quietly substituted.

## What a person does

- Answers "who accepts this?" with a name.
- Gives one example of a result that would be wrong. People find this easier than describing right.
- Reads the checks and changes any that are vague. "Looks professional" becomes "has the move-in question and no viewing promise".
- Keeps the acceptance decision. The agent can say the checks pass; only the owner says the work is accepted.

## The format

An eval case is a small block:

```
input: "Hi, is the two-bed on Quay Street still available?"
must contain: ask for move-in date
must not contain: promise of a viewing time
should refuse: if the message asks for the landlord's phone number
```

For larger sets, store cases as a JSON or markdown file in the project so the same cases can be run again after any change.

## Sizing by risk

- **Small work:** one sentence of expected result, confirmed in chat. If the person can see at a glance whether it worked, that is the card.
- **Normal work:** the full card with a failure case. Eval set only if the output varies.
- **High-risk work:** the full card, at least five eval cases, one of them a boundary case, reviewed by someone other than the author. Changes to the card after work starts are recorded with who agreed.

## Common mistakes

- Writing checks only the agent can interpret ("is well structured").
- Writing only success cases, so every run passes.
- Changing the acceptance after seeing the result, to match what was produced. If the change is right, record it as a change.
- Using the same examples for tuning the prompt and for judging the result. Hold two or three back.
- Confusing "checks pass" with "accepted".

## How to check it is working

- Every non-trivial task record has a card before the first output timestamp.
- Each card has at least one failure case.
- Pick a rejected piece of work. Was the reason on the card? If not, the card was too vague or the agent ignored it.
- Rerun the eval set after a prompt or model change. A change that breaks a case is caught the same day.

## Related

`agree-acceptance` skill and its [README](../skills/agree-acceptance/README.md) · [acceptance template](../templates/acceptance.md) · [Control 6: read-back](06-read-back.md) · [Control 12: graduation](12-graduation.md) · [rules index](README.md)
