---
name: show-me
description: Chooses the smallest demonstration that lets a named reader see, compare or decide, from the real thing up to a working prototype, and labels what is real. Use for show-me requests, mock-ups, worked examples and before-and-after comparisons. Not for plain factual answers.
---

# Show me

Replace explanation with the smallest thing that makes the point visible. The demonstration is the answer. The prose only says what to notice and what decision is left.

**Stage:** Operate (any stage may use it). **Rules:** 2 Agree acceptance first; 3 Read back the real result; 4 Claim only what you can show. Detail: `rules/10-claim-discipline.md` (in the SHOTos repository, or `.shotos/rules/10-claim-discipline.md` where SHOTos is installed).

## Context and handoff

Read the reader, the one question they must answer and the current source (a live screen, a file, a record, a dataset). Those three decide the form. Keep the source pointer, the level chosen and the reason with the artefact.

Use `label-the-proof` for the labels. Hand over to `report-with-evidence` when the reader needs a finished report, and to `build-small-website` when they need a finished site. If a browser or renderer is missing, say the visual check was not done and stay at level 1 or 2 below.

## When not to use this

Skip it for a simple factual answer, or when the job is a finished document in a set format. Never put real people's details, children's data or credentials in a mock-up. Use invented data marked as illustrative.

## Steps

1. **Name the proof.** Write the reader, the one question, the claim the demonstration must prove and the source. If the reader or source is missing and cannot be inferred, state your assumption in one line and stay at the lowest level.
2. **Pick the lowest level that works.** Stop at the first one that lets the reader understand or decide:
   1. Show the existing thing: open the real screen, file or record and point at the part.
   2. Show a compact example: a worked example, comparison table, before-and-after, small diagram or calculation.
   3. Show a static artefact: an annotated screenshot, wireframe or one-page visual, when layout is the point.
   4. Show an interactive page: only when changing a state or trying a flow is itself the argument.
   5. Show a working prototype: only when behaviour cannot be judged from anything lighter.
3. **Build one idea.** One artefact, one main idea, one to three interactions at most. For anything on screen, check it at phone width and with a keyboard.
4. **Label it.** Mark each part literal, inferred or illustrative where the reader will see it. Never present a mock-up as built or a concept as agreed.
5. **Edit in place.** If the artefact already exists, change that file. Do not make a `v2` or a near-copy. Create a new file only when the artefact is genuinely new.
6. **Look at what the reader sees.** Open or render the result and check what it shows, not just the source text. Recompute every figure from the source.
7. **Hand over.** Show the result first. Then give one sentence on what to notice, up to three bullets (what it proves, what was inferred, the decision now needed) and the file path.
8. **Automate only a proven shape.** If the same demonstration has been made several times with predictable inputs, suggest moving the stable part into a template or script. Do not automate an idea that has not been proved.

## Output

The demonstration, a one-sentence pointer to what to notice and the three-bullet hand-over. [template.md](template.md) has the proof card to keep with it.

## Checks

- The reader, question and claim were written down before anything was built.
- The form is the lowest level that answers the question, or the card says why a higher level was needed.
- Every part is labelled literal, inferred or illustrative.
- No real personal data appears in the demonstration.
- The result was opened or rendered, or the missing check is stated.
- No near-copy of an existing file was created.
- Reviewer check: pick one figure in the demonstration and trace it to its source or its illustrative label.
