---
name: eval-set
description: "Builds a small eval set for AI output: 5 to 20 real examples, what each answer must and must not contain, one failing case, how to grade. Use when relying on AI-written text or classifications, or changing their prompt."
---

# Build an eval set

For output that varies, "it looked fine when I tried it" is not a test. An eval set is a short list of real inputs with written expectations, so every change to the prompt or the model can be checked against the same cases.

**Stage:** Hypothesise (reused in Operate and Track). **Rules:** 2 Agree acceptance first; 3 Read back the real result.

## Context and handoff

Read the acceptance card and actual recurring failure patterns. Include a normal case, an incomplete case and a boundary case where relevant.

Use `example-mapping` to resolve unclear rules. Store the cases and grading conditions beside the work they check.

## When not to use this

Skip it when the output is deterministic and ordinary tests already cover it, or for a one-off task where nobody will repeat the run. Do not invent inputs when real ones exist.

## Steps

1. **Name the task and the owner.** One sentence on what the AI produces, and the person who decides what a good answer is.
2. **Collect real inputs.** Take 5 to 20 examples from actual work: past emails, tickets, documents, records. Remove names, contact details and anything private before they are saved in the project. If you only have a few real cases, start with those and say so rather than padding with invented ones.
3. **Cover the spread.** Include easy cases, awkward ones, an input with missing information, an input that tries to steer the AI off its job, and at least one case where the right answer is to refuse, ask a question or say "I don't know".
4. **Write expectations for each case.** For each input list:
   - `must contain`: facts, points or actions the answer needs, written as short phrases or alternatives separated by `|`.
   - `must not contain`: things that would make the answer wrong or unsafe, such as an invented figure, a promise, a name, a refund.
   - `notes`: why this case is here.
5. **Include at least one case that should fail.** Add an input where the current prompt or model is known or expected to go wrong, or a deliberately wrong answer the grader should reject. A set that every version passes is not testing anything.
6. **Store it in the project.** Save as JSON (for graders that read it) or markdown (for reading). Keep it next to the work, for example `evals/<task>.json`. Do not leave it in the chat.
7. **Say how to grade it.**
   - Automatic first: check `must contain` and `must not contain` with case-insensitive text matching. Say it is crude and can be fooled.
   - Then a person reads a sample, at least the failures and every case that passed only barely.
   - Record for each run: date, model and prompt version, cases passed, cases failed, and who read the sample.
   - Pass bar: state it before the run (for example "every must-not case passes and at least 80% of the rest").
8. **Keep it alive.** Add every real failure found later as a new case. Remove cases that no longer describe the work, and say why.

## Output

Use [template.md](template.md). Save it with the work, for example `evals/<task>.json` or `evals/<task>.md`.

## Checks

- Between 5 and 20 cases, drawn from real examples with private details removed.
- Each case has must contain, must not contain and a note.
- At least one case should fail or refuse.
- Grading method and pass bar are written before the first run.
- The set lives in the project, not only in the conversation.
