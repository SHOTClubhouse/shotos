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

## When not to use this

Do not use it for a long document that nobody will present; write a document instead. For many decks tailored from one master, use the `proposal-factory` skill. For a reader-specific sales proposal, start with the `contextual-proposal` skill.

## Steps

1. **Check the tools first.** If `.work/capabilities.md` exists, read it. If the slide tool this skill needs (python-pptx, LibreOffice or a Google Slides connection) is missing, say so at the start, do the steps that need no tool, and say how to connect it (see the connect-your-tools guide at `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` where SHOTos is installed).
2. **Agree the reader and the ask.** Who will see it, in what setting (presented, sent to read, on a screen in a shop), and the one thing they should decide or do afterwards. Agree the length and the owner who accepts it.
3. **Gather the material.** Collect the facts, figures, images and brand guide. Note the source and date of every number. Anything without a source is a question for the owner, not a slide.
4. **Write the storyline first.** One line per slide, written as the message the slide must land, not a topic ("Repairs now wait 9 days on average", not "Repairs"). Read the lines in order: they must make the argument on their own. Show the storyline to the owner before building when the deck matters.
5. **Build in an editable format.** Use the format the owner will edit and present from: Google Slides or PowerPoint. Use their template or brand guide if they have one. Put the message line as the slide title. One idea per slide; move detail to speaker notes or an appendix.
6. **Source every number.** Each figure on a slide carries a footnote or a notes-line source. Label illustrative figures as illustrative. Never round a number in a way that changes its meaning.
7. **Render and look at every slide.** Export or view each slide as an image and check it: text overflowing or cut off, overlapping shapes, unreadable contrast, images stretched or pixelated, typos, numbers that disagree between slides, empty placeholders. Describe what you see. A slide that looked fine in the source can break when rendered.
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
