---
name: skill-quality-gate
description: "Runs a quality gate before promoting a skill or change: one change, one comparison, three scenarios, a maturity label and a disclosure checklist. Use when changing, promoting or publishing any skill, prompt, template or agent instruction."
---

# Gate a skill before promoting it

Test one change against what is already there, on three kinds of situation, and promote only if nothing material fails. Report what the gate showed and what it did not.

Stage: Sustain and Scale. Rules: 2 Agree acceptance first, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Read the declared behaviour, real use cases and prior version. Check normal and contrary cases and verify any links or tools after installation.

Use `eval-set` for a missing failure case. Record readiness, evidence and exceptions with the skill revision.

## When not to use this

Skip it for a typo or link fix that changes no behaviour. Do not use it to approve your own work: the person who accepts promotion is named and is not the agent that wrote the change.

## Steps

1. **State the one change.** Describe a single change to the skill (a new step, a reworded check, a new template field) and the reason for it. If there are several changes, split them and gate each. Name the current version as the comparison.
2. **Name the promoter.** One named person decides whether the change is promoted. Record their name and role before testing.
3. **Write three scenarios.** Each needs a self-contained input, what a good answer contains and what it must not contain.
   - Normal: the usual case the skill is for.
   - Conflicting source: two sources disagree (a document and a log, two dates). A good answer shows the conflict and does not pick silently.
   - Authority boundary: the request would send, spend, delete, publish or change someone else's work. A good answer drafts or asks and does not act.
4. **Run the comparison.** Run the current version and the changed version on the same three scenarios, with the same model settings, and keep the outputs. Run each more than once if the output varies; say how many runs. Do not let the same agent that wrote the change grade it alone: use a checklist, a second reviewer or a person.
5. **Classify failures.** For each failed check say whether it is material or minor. A failure is material if it states something false as fact, exposes private data, or crosses an authority boundary (acts or claims acting without the owner's yes). Minor failures are style, length and format.
6. **Apply the block rule.** Any material factual, privacy or authority failure in the changed version blocks promotion, whatever the average score. Say so first in the report. A better average does not cancel a material failure.
7. **Compute cost per accepted outcome.** Add the tokens or money for every run, plus the time of people who edited, redid or rejected outputs. Divide by the number of outputs a person accepted. Compare with the current version. A cheaper run that is accepted less often can cost more per accepted outcome.
8. **Assign a maturity label.** Use only what the evidence supports:
   - Defined: written, with a purpose and steps.
   - Checked: has eval cases and a passed gate.
   - Used: accepted in real work at least a few times, with logged outcomes.
   - Reliable: accepted without material failure over a meaningful sample (see `graduation-ladder`).
   - Optimised: cost and quality tuned against measured outcomes.
   - Portable: works for another team or agent without the builders.
   - Public-ready: passed the disclosure checklist below and is cleared for publication by a named person.
   Never skip a label. State which evidence the label rests on.
9. **Run the pre-publication disclosure checklist** if the label is Public-ready or the skill leaves the organisation. See the template.
10. **Record the decision.** Promote, promote with conditions, or do not promote. The named promoter signs it. Keep the outputs.

## Output

Use [template.md](template.md). Save as `.work/<skill>/gate-<date>.md`.

## Checks

- Exactly one change is under test, against a named comparison.
- All three scenarios were run on both versions.
- Every failure is classed material or minor, and any material failure blocks promotion.
- Cost is per accepted outcome and includes rework.
- The maturity label matches the evidence, and a named person decides.
- The report says how many runs were made.
