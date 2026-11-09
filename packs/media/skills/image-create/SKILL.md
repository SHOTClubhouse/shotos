---
name: image-create
description: Creates an image from a brief, then inspects the result and fixes problems, with rights, likeness, alt text and AI-label checks. Use when a blog hero, social image, slide image or mock-up is needed. Drafts only; publishing needs a yes.
---

# Create an image you have looked at and cleared

Produce an image that fits its job, has been looked at after generation, and is cleared for use.

**Stage:** Operate. **Rules served:** rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the actual subject, audience, destination crop, brand or style references and rights. Use references to settle composition before choosing a generation route.

Use `explainer` if the image must teach a sequence. For a campaign graphic, agree one message and the destination first. Use editable layout for copy-heavy graphics and retain the editable master. Read the [campaign graphics checks](campaign-graphics.md) when the same design will ship in several sizes.

## When not to use this

Do not use it for photographs presented as real events, for images of real people without recorded written consent, or for copying another creator's style or characters. Do not use it for a quick throwaway sketch where nobody will rely on the result.

## Steps

1. **Check the tools first.** If `.work/capabilities.md` exists, read it. For a text-led or vector graphic, use the project's layout tool. If a generated image is needed and no image model is available, say so, do the steps that need no tool, and say how to connect it (see the connect-your-tools guide at `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` where SHOTos is installed). With no image tool, still deliver the written brief, the rights note and a layout or art-direction spec a designer can follow, and mark the image as not made.
2. **Write the brief.** Capture the job (where it will appear and what it must help the reader do), each channel it will appear on with its size, ratio and safe area (check the platform's current specification; do not rely on remembered sizes), the style, any text that must appear, and the owner who accepts it.
3. **Agree references and source assets.** For every supplied photo, logo, screenshot or reference, record its file name, who made it, the licence or permission to use it and, for any person shown, the consent that covers this use. Mark anything without that record "not cleared" and do not build on it. Describe style in words rather than naming a living artist or a copyrighted character.
4. **Run the rights and likeness check before generating.** No real, identifiable person without their written consent. No borrowed character, logo or trademark without rights. No children's likeness drawn from a real child. If the brief needs any of these, stop and ask the owner.
5. **Build the first design.** For an editable graphic, use the approved layout and copy. If generating an image, ask the chosen model for two to four options and keep the prompt, model and settings with the work.
6. **Look at the actual image.** Open each output and check it against the brief: subject, composition, text spelling, hands and faces, extra limbs or objects, stray logos or watermarks, and the crop at every size it will be used. Describe what you see, not what you asked for.
7. **Fix and regenerate.** List each defect, adjust the prompt or edit, regenerate and look again. Stop after a set number of rounds (three unless the owner says otherwise) and report what remains.
8. **Write alt text.** For an informative image, describe the information it adds. For an image used as a link or button, describe the action. Put the essential values and relationships from a complex graphic in nearby text. For a decorative web image, use an empty alt attribute so the page can skip it. Follow the [W3C images tutorial](https://www.w3.org/WAI/tutorials/images/).
9. **Label where required.** Check whether the channel or the owner's policy requires an AI-generated label. If so, add it. If unsure, add it and say so.
10. **Hand over for approval.** Present the chosen image, the prompt log, the alt text and the rights check. Do not publish, post or upload to a live page without the owner's yes.

## Output

A folder with the chosen image, the prompt and model log, the alt text, the rights and likeness note, the label decision and a one-line defect log. The owner's approval is recorded separately.

## Checks

- The agent looked at the rendered image and described what it saw.
- No real person, borrowed character or logo appears, or written rights are on file.
- Any text in the image is spelled correctly.
- The text alternative fits the role of the image, including an empty alt attribute for a decorative web image.
- The AI label decision is recorded.
- Every supplied source asset has a recorded origin and permission, or is marked not cleared and unused.
- Each destination channel has its own checked size or crop.
- Nothing was published without the owner's yes.
