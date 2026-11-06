---
name: label-the-proof
description: Labels each part of a report as literal, inferred or illustrative, and edits the one canonical file in place, never a new copy, since version history keeps the old one. Use when a reader could mistake an example for a result.
---

# Label the proof

A reader cannot tell a real figure from a made-up one unless the page says. Label every part by how you know it, and keep one canonical file so the labels stay true.

**Step:** Build (any step may use it). **Rules:** 4 Claim only what you can show; 3 Read back the real result. Detail: `rules/10-claim-discipline.md` (in the SHOTos repository, or `.shotos/rules/10-claim-discipline.md` where SHOTos is installed).

## When not to use this

Skip it for short chat answers and for text with no figures or factual claims. Do not label every adjective; label claims, numbers, quotes, screenshots and examples.

## Steps

1. **Find the claim-bearing parts.** List the figures, quotes, statuses, screenshots, tables, examples and conclusions in the artefact. Ignore connective prose.
2. **Give each part exactly one label.**
   - **Literal:** copied or computed directly from a source or the real system. You can point to where: a file path, a query, a document and page, a screen, a command and its output.
   - **Inferred:** reasoned from evidence. It names the evidence and the reasoning, and says how confident you are.
   - **Illustrative:** made up to show the idea (sample data, mock-ups, example numbers, a worked scenario). It is plainly marked as not real, in the place the reader will see it.
3. **Attach the pointer.** Next to each literal part, record where it came from and when it was read. For inferred parts, record the evidence. For illustrative parts, say what real thing it stands in for.
4. **Keep the three kinds apart.** Do not mix an illustrative number into a table of literal ones. Put illustrative material in its own block, or mark every cell. Do not turn an illustrative figure into a literal one by repeating it in a later section.
5. **Keep "installed", "run" and "accepted" apart.** If the artefact says something is installed, say whether it has been executed, and whether the owner has accepted the result. Each is a separate claim that needs its own proof.
6. **Say what you did not check.** Add a short list of items that are neither literal nor inferred because they could not be verified.
7. **Edit the canonical file in place.** Find the one file that owns the artefact (the report, the deck, the page) and change it there. Do not make `report-v2`, `report-final` or `report-copy`. If a snapshot is needed, use the version history of the tool or a dated archive, and say where it is. If asked to save under a new name so the old file stays untouched, say that version history does that job and edit the one canonical file. When you edit, update the labels in the same change.
8. **Read it back.** Open the saved file where it lives, not the draft in the chat, and confirm every label is present and each literal part matches its source.

## Output

The labelled artefact itself, with a short label key at the top and a "not checked" list at the end. [template.md](template.md) has the key and a label table for artefacts that cannot carry inline labels.

## Checks

- Every figure, quote, status and example has a label.
- Literal parts have a pointer to the source and date.
- Illustrative parts are plainly marked as not real.
- No illustrative figure appears unlabelled elsewhere.
- One canonical file was edited; no near-duplicate was created.
