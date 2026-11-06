---
name: voiceover
description: Creates spoken audio from a script, such as a voiceover, narration or phone message. Checks consent for real or cloned voices, then transcribes the result against the script. Use when a voiceover is needed. Drafts only; publishing needs a yes.
---

# Create a voiceover you have listened back to

Produce spoken audio that says exactly what the script says, in a voice you have the right to use, checked before anyone hears it.

**Step:** Build. **Rules served:** rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## When not to use this

Do not use it to imitate a real person's voice without their written consent, to make audio that pretends to be a real call or a real statement, or to voice anything for a child's likeness without parental consent. For a recording of a real person speaking, record them instead.

## Steps

1. **Check the tools first.** If `.work/capabilities.md` exists, read it. If the tool this skill needs (a speech model or a transcription tool) is missing, say so at the start, do the steps that need no tool, and say how to connect it (see the connect-your-tools guide at `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` where SHOTos is installed).
2. **Agree the job.** Where it will be heard (video, website, phone line, podcast), the length, the tone, the language and accent, and who accepts it.
3. **Lock the script.** Get the final words before generating. Mark names, numbers, brand words and anything easy to mispronounce, with a phonetic spelling for each.
4. **Check consent for the voice.** A stock synthetic voice from the model's library needs nothing more. A cloned or custom voice of a real person needs that person's written consent for this use. If consent is missing, stop and ask the owner.
5. **Generate.** Use the speech model the owner chooses. Generate two takes if the model allows it. Keep the model name, voice, settings and script version with the work.
6. **Listen back by transcript.** Transcribe the generated audio with a speech-to-text tool and compare it with the script word by word. List every word that differs, every number said wrongly, and every name mispronounced.
7. **Check timing and sound.** Measure the length against the target. Note long pauses, clipped endings, background noise and any sudden change in volume.
8. **Fix and regenerate.** Adjust the phonetic spellings, punctuation for pacing, or settings. Regenerate only the parts that failed where the tool allows. Stop after three rounds unless the owner says otherwise, and report what remains.
9. **Label where required.** If the channel, the law or the owner's policy requires synthetic speech to be disclosed, add the disclosure in the description, credits or the audio itself.
10. **Hand over for approval.** Present the chosen take, the transcript comparison, the timing, the consent note and the label decision. Do not publish, upload to a live page or connect to a phone line without the owner's yes.

## Output

A folder with the audio file, the locked script, the transcript of the audio, a word-by-word difference list (empty when it passes), the length, the model and voice log, the consent note and the label decision.

## Checks

- A transcript of the actual audio matches the script, or every difference is listed.
- Every name and number in the script is said correctly.
- The length is within the agreed target.
- Consent is on file for any real or cloned voice.
- The synthetic-speech label decision is recorded.
- Nothing was published without the owner's yes.
