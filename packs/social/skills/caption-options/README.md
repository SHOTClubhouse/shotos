# caption-options

**Five caption choices and platform variants from a photo or brief, with every fact checked.**

The agent lists the facts it may use, writes options A to E that differ in approach, adds length, hashtag and alt-text variants per platform, and removes claims the owner cannot back. It supports the Operate stage and serves rule 4, Claim only what you can show, and rule 1, Stop at the boundaries.

## The problem it solves

Fernleigh Bakery (a fictional shop) photographs a tray of cinnamon buns. The first draft says "the best buns in town, baked fresh every morning, only a few left!" The owner bakes at 5am but the buns in the photo were made yesterday, and there are forty left. A customer posts a correction in the comments. A second photo shows a child at the counter, and nobody has asked the parents.

## What the agent does differently

It builds a facts list first, with sources, and asks for what is missing: when were these baked, how many are left, what is the price. It drops "best in town". It declines to caption the child's photo without recorded consent and suggests another image. It gives five genuinely different options and the alt text for the image, so the owner picks rather than edits from nothing.

## When to use it, and when not to

Use it for any post that needs words: a photo, an event, a notice, a thank-you.

Do not use it to publish, to invent facts, or to caption an image of a child without consent.

## Who it is for

- **Shop or studio owner:** quick choices in your voice.
- **Volunteer:** fewer mistakes in public.
- **Marketing lead:** a claim check you can show to a manager.
- **Accessibility-minded team:** alt text as a standard part of every post.

## How to use it

> Write caption options for this photo of Saturday's cinnamon buns for Instagram and Facebook. Facts: baked this morning, £2.80 each, 40 available until 2pm. Our voice is warm and short.

## How it connects

- Before: [content-calendar](../content-calendar/README.md) supplies the slot.
- After: [publish-with-manifest](../publish-with-manifest/README.md) takes the approved caption.
- Pack overview: [packs/social](../../README.md).

## Needs

The photo or brief, the facts, and your voice or a few past posts. Nothing else beyond the agent.

## Evidence

Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 4 of 4, Sonnet 4 of 4, Opus 4 of 4. Without: Haiku 1 of 4, Sonnet 1 of 4, Opus 2 of 4. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips

- Give the agent the awkward facts too (prices, limits, dates) so it does not guess.
- Read alt text aloud; it should make sense to someone who cannot see the picture.
- Keep hashtags few and specific.

## Limits

- The agent can read a photo but cannot verify what it shows beyond what is visible. A species, a score or a name comes from you.
- Platform character limits and hashtag habits change. Check the current limit when it matters.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/caption-options/input.md) and [output](../../examples/caption-options/output.md).
