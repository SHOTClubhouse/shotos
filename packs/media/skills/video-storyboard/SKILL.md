---
name: video-storyboard
description: "Takes a short video from idea to cut: storyboard, shot list, generated or filmed shots, consistency, stitching and rights checks. Use when making an explainer, ad or social video. Screen recordings of real software go to product-demo-video."
---

# Storyboard to a stitched, checked cut

Make a short video where the shots match each other, the rights are clear and the finished render has been watched in full.

**Stage:** Operate. **Rules served:** rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the audience action, approved script, duration, platform and available assets. Resolve what must be captured versus illustrated.

Use `voiceover` for timing or `product-demo-video` for live capture. Save the shot list and approved assets together.

## When not to use this

Do not use it for a screen recording of a real product (use product-demo-video), for synthetic voices that imitate a real person, or for any video that presents generated footage as real events. Skip it for a one-shot clip with nothing to stitch.

## Steps

1. **Check the tools first.** If `.work/capabilities.md` exists, read it. If the tool this skill needs (a video model or ffmpeg) is missing, say so at the start, do the steps that need no tool (the brief, storyboard, consistency sheet, shot list, rights log and an edit decision list a person can follow in any editor), mark the video as not made, and say how to connect it (see the connect-your-tools guide at `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` where SHOTos is installed).
2. **Write the brief.** Capture the audience, the one thing the viewer should do or understand, the length, the channel and the owner who accepts it. For each channel give the aspect ratio, maximum length, safe area for captions and whether sound is on by default (check the platform's current specification), and plan a separate cut where channels differ.
3. **Write the storyboard.** One line per beat: what we see, what we hear, how long. Keep it to the length in the brief.
4. **Write a consistency sheet.** Describe each character and setting once, in fixed words: age range, clothing, colours, props, place, time of day, lighting, camera style. Use this text unchanged in every shot prompt.
5. **Make the shot list.** Number each shot with the storyboard beat, the prompt or filming note, duration, and the shot it must match. Mark which shots are generated and which are filmed.
6. **Log supplied footage, images and music, then run the rights check before producing.** Record each supplied file's origin, licence or permission and who is shown. Mark anything without that record "not cleared" and leave it out of the cut. Music: licensed or created for this use, with the licence kept. Voice: the owner's own, a person who has consented in writing, or a stock voice with a licence; never a clone of a real person without their written consent. Likeness: no real people or borrowed characters without rights. Children: no identifiable child without the guardian's written consent.
7. **Produce a pilot first.** Make the first two or three shots only, then look at them side by side. Compare the character and the setting against the consistency sheet and fix the sheet or the prompts before making the rest.
8. **Produce the remaining shots.** Look at each shot as it arrives. Reject any with drift in faces, clothing, colours, text artefacts or objects that change between frames. Log each retake.
9. **Stitch the cut.** Assemble in order, add the audio and captions, and keep the project file.
10. **Watch the final render at full length.** Play it from first frame to last at normal speed with sound. Check continuity between shots, audio levels and sync, captions against the speech, and the end card. Record what you watched, with time marks for any fault.
11. **Hand over for approval.** Present the cut, the shot list, the consistency sheet, the rights log and the fault log. Do not publish, post or send without the owner's yes.

## Output

A folder with the storyboard, consistency sheet, shot list, rights log, the final render and a fault log with time marks. Use [template.md](template.md) for the shot list.

## Checks

- Every character and setting is described once and used unchanged across shots.
- A pilot of two or three shots was compared side by side before the rest were made.
- The final render was played through at full length and the log says so.
- Music and voice licences or consents are on file; no real person's voice or likeness is imitated.
- Captions match the speech.
- Every supplied clip, image and track has a recorded origin and permission, or is left out.
- Each channel has a cut at its own ratio and length, or the gap is stated.
- Nothing was published without the owner's yes.
