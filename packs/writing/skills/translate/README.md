# translate

**Glossary first, translate for meaning, check every number and name, back-translate what matters, flag what a fluent person must review.**

The agent agrees the reader and purpose, fixes the terms that must not change, translates, and then checks the result against the source: numbers, dates, prices, names and links. It back-translates the sentences a reader will act on and flags anything public, legal, medical or safety-related for a fluent human reviewer.

It supports the Operate stage. It serves rule 2 (agree acceptance first), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## The problem it solves

A youth football club translates its summer camp letter into Polish and Portuguese for parents. The machine translation turns "drop-off 8.45am" into 8.45pm in one version, translates the club's name, and renders "no refunds after 1 June" as "refunds after 1 June". Parents act on all three.

## What the agent does differently

Without the skill, an agent translates and reports "done". With it, it builds a glossary, checks every time, date and name against the source, back-translates the refund line and catches the reversal. See [the worked example](../../examples/translate/output.md).

## When to use it, and when not to

Use it for letters, notices, captions and subtitles, meeting transcripts, product pages and internal documents going to readers in another language.

Do not use it as the only check for contracts, medical or safety instructions, or safeguarding material: a qualified translator signs those off.

## Who it is for

- **Clubs, schools and charities:** notices that every family can read.
- **Businesses selling abroad:** product pages and emails that keep prices and terms intact.
- **Teams with international meetings:** transcripts and notes in each person's language.

## How to use it

Install the writing pack as described in the [pack README](../../README.md). Then ask:

> Translate this camp letter into Polish and European Portuguese for parents. Keep the club name in English. Check every date, time and price, and tell me what a fluent parent should read before we send it.

## How it connects

- **Before:** [meeting-notes](../../../exec-ops/skills/meeting-notes/README.md) produces the transcript and notes to translate.
- **Alongside:** [plain-english-check](../plain-english-check/README.md) on the source first: clear English translates better.
- **After:** [caption-options](../../../social/skills/caption-options/README.md) for translated social posts, and [voiceover](../../../media/skills/voiceover/README.md) to voice a translated script.

## Needs

Nothing beyond the agent for most languages. A fluent person for review of anything public or high-stakes.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Fix the source first. Ambiguous English becomes wrong in every language.
- Write times in the target language's normal format, and check them twice.
- Keep one glossary per organisation and reuse it.

## Limits

- Quality varies by language. Less common languages need more human review.
- Back-translation catches meaning drift, not tone. A fluent reader judges tone.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/translate/input.md) and [output](../../examples/translate/output.md).
