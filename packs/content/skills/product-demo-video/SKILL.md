---
name: product-demo-video
description: Makes a product demo video from real browser capture on test data, with chapters, subtitles and a personal-data check. Use when the software already works. Never fakes a screen; animation goes to video-storyboard. Drafts only.
---

# Make a product demo video from real capture

Produce a demo video that shows the product as it really is, using test data, checked before anyone sees it.

**Step:** Build. **Rules served:** rule 3 (read back the real result), rule 4 (claim only what you can show) and rule 1 (stop at the boundaries).

## When not to use this

Do not use it for features that do not exist yet, for a stylised animation (use video-storyboard), or to record a live production system with real customer data on screen. Never fake a screen to cover a feature that does not work.

## Steps

1. **Check the tools first.** If `.work/capabilities.md` exists, read it. If the tool this skill needs (a browser tool such as Playwright or ffmpeg) is missing, say so at the start, do the steps that need no tool, and say how to connect it (see the connect-your-tools guide at `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` where SHOTos is installed).
2. **Agree the brief.** Name the owner, the viewer, the one thing they should understand or do afterwards, the length, and where the video will be used.
3. **Prepare a safe environment.** Use a test or demo environment with invented data: fictional names, example email addresses, no real customers, no real children, no real payment details. If only production exists, stop and ask the owner for a test account.
4. **Script the walkthrough.** Write the flow as steps: the starting screen, each action, what the viewer should notice, and the words said or shown. Keep one story from start to a clear finish. Remove any step that needs a feature that does not work today.
5. **Capture the real interactions.** Drive the browser with a script, for example Playwright with video recording on and a fixed viewport. Capture the actual clicks, loads and results. Do not splice in mock-up screens, edited screenshots or reordered results. If a step fails, fix the product or the script, or cut the step.
6. **Add chapters and subtitles.** Write chapters with time marks at each major step, and subtitles that match the narration word for word. Keep lines short enough to read.
7. **Assemble the cut.** Trim waiting time, speed up only obvious waits and say so on screen if speed is changed. Do not hide errors that a user would meet.
8. **Inspect the final render.** Play it through at full length and also step through key frames. Check that every screen is real, that the story matches the script, that subtitles are in sync, and that nothing is cropped or blurred by mistake.
9. **Check personal data.** Scan every frame and the subtitles for real names, emails, phone numbers, addresses, faces, account numbers, API keys and tokens, and for browser tabs, bookmarks and notifications that show private information. Fix and re-render if anything appears.
10. **Hand over.** Give the owner the video, the script, the chapters, the subtitle file, the capture script and the inspection and data-check log. Publishing, posting or sending the video is the owner's decision and waits for a yes.

## Output

The rendered video, script, chapter list, subtitle file, capture script and an inspection log (what was checked, time marks of any faults, data check result). Use [template.md](template.md) for the script.

## Checks

- Every screen in the video came from a real capture of the working product.
- Only test data appears, and the data check is logged.
- Chapters and subtitles exist and match the final cut.
- The final render was played in full and key frames were inspected.
- Any change of speed is declared.
- Nothing was published or sent.
