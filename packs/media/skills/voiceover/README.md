# voiceover

**Script, consent, generate, listen back by transcript, fix, label, then ask before anyone hears it.**

The agent locks the script, checks it has the right to use the voice, generates the audio, and then transcribes what was actually said and compares it with the script. Mispronounced names, wrong numbers and dropped words show up as a list instead of being found by a customer.

It supports the Operate stage. It serves rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A cycle shop wants a 30-second voiceover for a video about its new servicing plan. The first take says "thirty-eight pounds" as "three hundred and eighty pounds" because the script read "£38/month", and it pronounces the shop's name, Northgate, as "North-gah-tay". If the agent only says "audio created", the video goes out with a price that is ten times too high.

## What the agent does differently

Without the skill, an agent can report the audio as done without hearing it. With the skill, it transcribes the take, finds the wrong price and the mispronounced name, fixes the script spelling and regenerates. See [the worked example](../../examples/voiceover/output.md).

## When to use it, and when not to

Use it for video voiceovers, narrated explainers, podcast intros and outros, on-hold or phone messages, and audio versions of written content.

Do not use it to imitate a real person without written consent, to fake a real call or statement, or where a real person should simply be recorded.

## Who it is for

- **Marketing leads:** voiceovers for product and social videos, checked before release.
- **Small business owners:** a phone greeting or a shop video without hiring a studio.
- **Trainers and coaches:** narrated lessons where every word matters.

## How to use it

Install the media pack as described in the [pack README](../../README.md). Then ask:

> Make a 30-second voiceover for our servicing plan video from this script. Warm, friendly British voice. Check every price and our name are said correctly before you show me.

## How it connects

- **Before:** [video-storyboard](../video-storyboard/README.md) sets the timing each line must fit.
- **Alongside:** [product-demo-video](../../../content/skills/product-demo-video/README.md) uses the voiceover over real capture.
- The rules behind it are in [docs/controls.md](../../../../docs/controls.md).

## Needs

- A text-to-speech model of your choice, available to the agent.
- A speech-to-text tool to transcribe the result for the listen-back check.
- Written consent for any cloned or custom voice of a real person.

## Tips and common mistakes

- Write numbers the way they should be spoken: "thirty-eight pounds a month", not "£38/month".
- Add phonetic spellings for names before the first take, not after.
- A transcript proves the words; a person should still listen once for tone.

## Limits

- Transcription can itself mishear. Treat a clean transcript as strong evidence, not proof, and have a person listen to anything important.
- Consent and labelling rules differ by country and change over time. The skill prompts the check; it is not legal advice.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/voiceover/input.md) and [output](../../examples/voiceover/output.md).
