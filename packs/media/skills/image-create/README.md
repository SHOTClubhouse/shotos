# image-create

**Brief, references, generate, look at the real output, fix, clear rights and likeness, add alt text, then ask before it goes anywhere.**

The agent writes the brief with the owner, checks rights and likeness before it generates, produces a few options, and then opens each one and checks it against the brief. It fixes defects, writes alt text, decides on the AI label and hands the image over for approval.

It supports the Build step. It serves rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A letting agency wants a hero image for a blog post on tenancy deposits. The first output has a house with a door that has two handles, a sign with gibberish text, and a figure that looks like a well-known television presenter. If the agent only says "image created", the post goes live with all three.

## What the agent does differently

Without the skill, an agent can report an image as done without opening it. With the skill, it describes the output, finds the gibberish text and the lookalike, regenerates and records the fixes. See [the worked example](../../examples/image-create/output.md).

## When to use it, and when not to

Use it for blog heroes, social images, slide visuals and product mock-ups that someone will publish.

Do not use it for photographs presented as real events, for images of real people, or for copying another creator's style or characters. Do not use it for a quick throwaway sketch where nobody will rely on the result.

## Who it is for

- **Marketing leads:** images that are checked before they go out.
- **Small business owners:** a clear record of how an image was made.
- **Editors:** alt text and labelling handled with the image.

## How to use it

Install the media pack as described in the [pack README](../../README.md). Then ask:

> Create a hero image for our blog post about tenancy deposits. Landscape, 16:9, flat illustration, no people. Check it properly and give me alt text.

## How it connects

- **Before:** [written-content](../../../content/skills/written-content/README.md) and [explainer](../../../content/skills/explainer/README.md) say where an image would show the mechanism.
- **After:** [video-storyboard](../video-storyboard/README.md) uses the same rights and consistency checks for moving images.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

- An image model of your choice, available to the agent.
- Optional: an image editor for crops and fixes.
- Reference images, with written permission to use them.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 3 of 3, Sonnet 2 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Say what the image is for before you say what it looks like.
- Ask for no text in the image and add text afterwards in your editor.
- Keep the prompt log. You will need it if anyone asks how the image was made.

## Limits

- The agent can only check what it can see. Ask a person to view important images.
- A rights check is a prompt to think, not legal advice.
- Labelling rules differ by channel and country and change over time.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/image-create/input.md) and [output](../../examples/image-create/output.md).
