---
name: slide-deck
description: "Builds a presented or read deck, such as a pitch, board update or training: one message per slide, sourced numbers, every slide rendered and checked. Use for general decks; a named-reader proposal is contextual-proposal, many tailored decks proposal-factory."
---

# Build a slide deck that has been looked at

Produce a deck whose story holds up as headlines alone, whose numbers are sourced, and whose every slide has been seen as rendered.

**Stage:** Operate. **Rules served:** rule 2 (agree acceptance first), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the decision brief and one approved visual reference. Choose the narrative from the audience’s decision and verify every figure against source.

Use `claims-audit` for unsupported promises. Keep the editable deck, source notes and render check together.

Name the approved source brief (file, revision and owner) in the first line of the output and cite it for every claim. Anything not in the brief is a question for the owner. If `.work/capabilities.md` exists, read the section for this runtime. If the editor or renderer is missing, say so first, deliver the storyline, as in step 1, and mark the check pending.

## When not to use this

Do not use it for a long document that nobody will present; write a document instead. For many decks tailored from one master, use the `proposal-factory` skill. For a reader-specific sales proposal, start with the `contextual-proposal` skill.

## Steps

1. **Check the editor and renderer first.** Read the relevant runtime section in `.work/capabilities.md` if it exists. If the intended editor or renderer is unavailable, prepare a storyboard or editable draft as the tools allow. State what was produced and which check is pending.
2. **Agree the reader and the ask.** Who will see it, in what setting (presented, sent to read, on a screen in a shop), and the one thing they should decide or do afterwards. Agree the length and the owner who accepts it.
3. **Gather the material.** Collect the facts, figures, images and brand guide. Note the source and date of every number. Anything without a source is a question for the owner, not a slide.
4. **Write the storyline first.** Write one message per slide and read the headlines in order. Keep observed results, proposed targets and the decision request distinct. A quote can support a cost, while the expected outcome may still be a hypothesis. Show the storyline to the owner before building when the deck matters.
5. **Build in an editable format.** Use the owner's editor and approved visual reference. Give each slide one message. Choose a visual that supports it, such as a chart with units and a target for a service comparison. Move detail to notes or an appendix.
6. **Source every number.** Each figure on a slide carries a footnote or a notes-line source. Label illustrative figures as illustrative. Never round a number in a way that changes its meaning.
7. **Render and look at every slide.** Open the actual deck revision in its intended renderer. Check for overflow, overlap, contrast, stretched images, inconsistent figures and placeholders. Verify chart units and labels against the source. Record the renderer, revision and slides inspected. A storyboard image only verifies that image.
8. **Fix and recheck.** Fix every problem found and render again. Repeat until a full pass finds nothing, or report what remains.
9. **Write speaker notes** where the deck will be presented: what to say, the one point to land, and the source of each figure.
10. **Hand over for approval.** Present the deck link or file, the storyline, the source list and the rendered check. Do not share it more widely, send it or present it on the owner's behalf without their yes.

## Output

An editable deck, a storyline (one line per slide), a source list for every number, the rendered check with the defects found and fixed, and speaker notes where needed. A PDF export only if the owner asks for one to send.

## Checks

- The slide titles, read in order, make the argument without the bodies.
- Every number has a source and date, or an illustrative label.
- Every slide was rendered and looked at after the last change.
- No text overflows, no placeholder is left empty, and figures agree across slides.
- The deck is in an editable native format.
- Nothing was shared or sent without the owner's yes.
- Reviewer check: open the deck at a slide with a number and confirm the source line and the cited brief agree.
