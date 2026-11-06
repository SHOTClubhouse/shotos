# product-demo-video

**Show the product as it really is: script it, capture it in the browser on test data, add chapters and subtitles, then inspect the render and the data before anyone sees it.**

The agent scripts the walkthrough, sets up a test environment, drives a real browser with a capture tool such as Playwright, adds chapters and subtitles, and assembles the cut. It then plays the render in full, inspects key frames, scans for personal data and reports the result.

It supports the Build step. It serves rule 3 (read back the real result), rule 4 (claim only what you can show) and rule 1 (stop at the boundaries).

## The problem it solves

A software team records a booking demo on its live system. A real customer's name and phone number appear in the second screen, a button that is not built yet is shown using a mock-up, and an email notification pops up in the corner. The video is already in a sales email before anyone notices.

## What the agent does differently

Without the skill, an agent can compose convincing screens that were never real. With the skill, every frame comes from a captured session on invented data, and the render and the data check are logged. See [the worked example](../../examples/product-demo-video/output.md).

## When to use it, and when not to

Use it when a working product needs a demo for customers, colleagues or a launch.

Do not use it for features that do not exist yet, for a stylised animation (use video-storyboard), or to record a live production system with real customer data on screen. Never fake a screen to cover a feature that does not work.

## Who it is for

- **Product owners:** demos that match the product.
- **Sales and success teams:** videos that carry no customer data.
- **Developers:** a repeatable capture script.

## How to use it

Install the content pack as described in the [pack README](../../README.md). Then ask:

> Make a 90-second demo video of our booking flow in the staging site using test data. Capture it with Playwright, add chapters and subtitles, inspect the render, check for personal data, and do not send it.

## How it connects

- **Before:** [agree-acceptance](../../../../skills/agree-acceptance/README.md) sets the checks.
- **Alongside:** [video-storyboard](../../../media/skills/video-storyboard/README.md) for animated or filmed videos, and [explainer](../explainer/README.md) for a written version.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

- Playwright (or another browser automation tool that can record video) installed.
- A test or staging environment with invented data.
- Editing tools to trim, add chapters and burn in or attach subtitles.
- Optional: a voice you have the right to use. Subtitles alone are fine.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 1 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Make the capture script re-runnable, so a fix means one command, not a re-record by hand.
- Seed test data with obviously invented names.
- Close other tabs and turn off notifications before capture.

## Limits

- Capture tools show what is on screen; they cannot read your mind about what is private. Check every frame.
- Frame inspection by an agent is only as good as the frames it can view. A person should watch the final video.
- A demo shows the happy path. Do not imply the product has no limits.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/product-demo-video/input.md) and [output](../../examples/product-demo-video/output.md).
