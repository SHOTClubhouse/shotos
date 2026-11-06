# connect-tools

**Find out which tools your agent can really use, prove each with a harmless test, and write down what is missing and how to connect it.**

SHOTos skills hold the method; the tools do the work. This skill checks which tools are connected (slides, documents, mail, calendar, speech, transcription, images, video, browser, local Python and git), tests each with a read-only call, and writes `.work/capabilities.md`. Skills read that file, so a voiceover or a slide deck tells you at the start that a tool is missing, rather than failing halfway through.

It works in any stage and is usually run first. It serves rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A café owner installs SHOTos and asks for a voiceover for their opening-hours video. Nothing for speech is connected. Without a check, the agent writes the script and then says "voiceover created", or stalls with a vague error. With the check done first, it says on the first line: "Speech is not connected. I can write and check the script now; to make the audio, connect a text-to-speech service such as ElevenLabs."

## What the agent does differently

Without the skill, an agent assumes tools exist and finds out mid-task. With it, it lists what it has, tests each tool safely, and records evidence. See [the worked example](../../examples/connect-tools/output.md).

## When to use it, and when not to

Use it after installing SHOTos, after connecting a new tool, and whenever a skill stops because something is missing.

Do not use it to create accounts or credentials, or to test a tool by doing real work with it.

## Who it is for

- **Anyone installing SHOTos:** a two-minute check of what will work today.
- **Small business owners:** a plain list of what to connect next, in order.
- **Team and platform leads:** a record of which tools each set-up can reach.

## How to use it

Install the setup pack as described in the [pack README](../../README.md). Then ask:

> Check which tools you can reach for SHOTos and write the capability list.

## How it connects

- **Guide:** the [connect-your-tools guide](../../../../docs/connect-your-tools.md) says how to connect each tool.
- **Alongside:** [mode-ladder](../mode-ladder/README.md) and [skill-audit](../skill-audit/README.md) in this pack.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent. It checks for everything else.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Rerun it after connecting anything new; the file is only as current as its date.
- "Connected, not tested" is an honest status when the only test would cost credits.

## Limits

- It proves access, not quality. A connected image model can still make poor images; the media skills inspect the output.
- Tools and connectors change. Check the provider's documentation for the current set-up.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/connect-tools/input.md) and [output](../../examples/connect-tools/output.md).
