# video-storyboard

**Storyboard to shot list to shots to a stitched cut, with the characters kept the same and the full render watched before anyone is shown it.**

The agent writes a storyboard and a consistency sheet, turns them into a shot list, makes a short pilot to check that the shots match, produces the rest and stitches the cut. It plays the final render in full, logs faults with time marks and clears music and voice rights before handing over.

It supports the Operate stage. It serves rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A youth cycling club wants a 45-second video on its safety rules. In the generated shots, the coach has a red jacket in shot two, a blue one in shot four and no helmet in shot five. The music was copied from a streaming playlist. Nobody watches the whole render until it is posted.

## What the agent does differently

Without the skill, shots are made one at a time and the cut is judged from a thumbnail. With the skill, a consistency sheet is reused in every prompt, a pilot is compared first, the final cut is watched end to end and the music has a licence on file. See [the worked example](../../examples/video-storyboard/output.md).

## When to use it, and when not to

Use it for short explainers, ads, social clips and training videos made from several shots.

Do not use it for a screen recording of a real product (use product-demo-video), for synthetic voices that imitate a real person, or for any video that presents generated footage as real events. Skip it for a one-shot clip with nothing to stitch.

## Who it is for

- **Marketing teams:** videos that look like one piece, not six.
- **Small clubs and charities:** a record that rights were cleared.
- **Producers:** a plain shot list and fault log.

## How to use it

Install the media pack as described in the [pack README](../../README.md). Then ask:

> Storyboard a 45-second safety video for Northgate Cycles with one coach character and a park setting. Make a shot list and a consistency sheet, do a pilot of the first two shots, and check the music rights. Do not post it.

## How it connects

- **Before:** [explainer](../../../content/skills/explainer/README.md) provides the script when the video explains something.
- **Alongside:** [image-create](../image-create/README.md) for stills and key frames, and [product-demo-video](../../../content/skills/product-demo-video/README.md) for real software walkthroughs.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

- A video model of your choice, or filming equipment and a person to film.
- Editing tools to stitch the cut, add audio and captions.
- A licensed or self-made music track and a voice you have the right to use.

## Tips and common mistakes

- Fix the character description before the first prompt and paste it unchanged every time.
- Make the pilot short. Fixing the sheet is cheaper than redoing ten shots.
- Watch the render with the sound on.

## Limits

- Current video models drift between shots. The pilot reduces this but does not remove it.
- The agent can only check what it can see or hear. A person should watch the final cut.
- A rights log is a record, not legal advice.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/video-storyboard/input.md) and [output](../../examples/video-storyboard/output.md).
