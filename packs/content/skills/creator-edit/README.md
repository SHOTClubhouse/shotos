# creator-edit

**Improve a creator's draft without replacing their voice: keep most of their words, show every change, check the facts and risks, and leave the decision to them.**

The agent studies the creator's voice, edits lightly towards a keep target of 85 to 95 per cent of their wording, logs every change, checks facts, consistency and risk, and prepares a version for each channel. The creator approves the final.

It supports the Operate stage. It serves rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A local cycling blogger sends a newsletter draft and asks for a polish. A heavy edit would flatten her dry humour, change a figure she took from a council report, and drop a line about a sponsored product she forgot to disclose. She wants it to still sound like her.

## What the agent does differently

Without the skill, an agent rewrites the whole piece smoothly and she no longer recognises it. With the skill, 91 per cent of her words stay, the figure and the sponsor line are flagged for her, and each channel gets a version. See [the worked example](../../examples/creator-edit/output.md).

## When to use it, and when not to

Use it for newsletters, scripts, captions, articles and posts where the creator's voice matters.

Do not use it to ghost-write from nothing (use written-content), to rewrite in a different voice, or when the creator wants a full rewrite. Do not use it to post on the creator's behalf.

## Who it is for

- **Independent creators:** a polish that still sounds like you.
- **Editors:** a visible change log and risk flags.
- **Small publishers:** one edited text packaged for several channels.

## How to use it

Install the content pack as described in the [pack README](../../README.md). Then ask:

> Edit this newsletter draft but keep it in my voice, aiming to keep at least 85 per cent of my words. Show every change, flag facts and risks, and make a short version for Instagram. Don't post anything.

## How it connects

- **After:** [ai-tell-check](../../../writing/skills/ai-tell-check/README.md) catches machine-written patterns that creep in, and [plain-english-check](../../../writing/skills/plain-english-check/README.md) checks readability.
- **Alongside:** [written-content](../written-content/README.md) when the creator needs a draft written, and [press-release](../press-release/README.md) for announcements.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

Nothing beyond the agent. Optional: a document tool with tracked changes or comparison, and the channels' own scheduling tools, used only by the creator.

## Tips and common mistakes

- Paste a sample of earlier work so the agent can learn your voice.
- Say what must not change before it starts.
- Read the change log first, not the clean copy.

## Limits

- A keep rate counts words, not feel. Read the result aloud.
- Risk flags are prompts, not legal advice.
- The agent cannot confirm facts that are not in a source it can read.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/creator-edit/input.md) and [output](../../examples/creator-edit/output.md).
