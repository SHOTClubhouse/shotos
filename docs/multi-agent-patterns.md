# Working with more than one agent

One agent doing everything is the simplest set-up and the right default. Add a second agent only when it buys something you can name: an independent check, a cheaper model for bulk work, a capability the first one lacks, or time saved by running in parallel. Every pattern below keeps the [four rules](controls.md): one named person owns the result, every agent gets the same acceptance card, and nobody claims more than they can show.

The patterns are runtime-neutral. The examples use runtimes people commonly mix today: Claude Code, Codex, Gemini (for example in Antigravity), and image or video models reached through a model router (for example MiniMax models). Swap in whatever you use.

## Pattern 1: one does, one checks

The most useful pairing. A lead agent does the work; a reviewer from a different model or runtime checks it against the same acceptance card.

| Work | Lead | Reviewer checks |
|---|---|---|
| A document or proposal | Claude writes the draft | Codex checks every claim against its source, the acceptance checks and the plain-English rules |
| Code | Codex makes the change and runs the tests | Claude reviews the diff, the tests and the read-back of the running result |
| An image | An image model generates from the brief | A second model looks at the rendered image against the brief: likeness, text, brand, rights, anything that should not be there |
| A slide deck | One agent builds it | Another inspects every rendered slide, not the source file |

How to run it:

1. Write the acceptance card first ([agree-acceptance](../skills/agree-acceptance/README.md)).
2. Give the lead the card and the inputs. The lead finishes with a Claims block.
3. Give the reviewer the card, the inputs, the output and the Claims block. Not the lead's reasoning: you want an independent read, not agreement.
4. The reviewer reports findings with evidence, ranked by severity.
5. The lead fixes, or argues back with evidence.
6. **The owner decides.** Two agents agreeing is not authority. Agreement only tells you two models made the same judgement, sometimes the same mistake.

Size it to risk ([rule card 7](../rules/07-independent-review.md)). A one-line fix needs no reviewer. Anything going to customers, touching money, safety or children's data, or published under your name gets one.

## Pattern 2: one researches, one holds the context

Research is wide and cheap per item: reading many pages, extracting facts. Context is narrow and expensive: knowing your situation, your reader and what was decided. Splitting them saves cost and keeps the main conversation clean.

- **The researcher** runs on a smaller, cheaper model (for example Haiku, or a MiniMax text model). It gets a tight brief: the question, the sources allowed, the output format (each fact with its source and date), and a stop condition. It never sees private context it does not need.
- **The context holder** runs on the strongest model you have. It holds the acceptance card, the owner's situation and the decisions so far. It takes the researcher's sourced facts, judges what matters, and writes the output.
- **The hand-over is a file, not a chat.** The researcher writes `.work/<task>/research.md`; the context holder reads it. Every fact keeps its source so the context holder can check the ones that matter.

Watch for: the researcher's guesses being promoted to facts on the way across. The [label-the-proof](../skills/label-the-proof/README.md) labels (literal, inferred, illustrative) travel with each item.

## Pattern 3: the factory

When you need many similar items (fifty tailored proposals, two hundred product descriptions, a document per branch), a factory uses different agents for different jobs:

| Station | Agent | Job |
|---|---|---|
| Brief | Strong model, with the owner | Writes the master, the variables per item and the acceptance checks |
| Research | Small model, many in parallel | Gathers the per-item facts, each with a source |
| Assemble | Mid model or a script | Fills the master for each item |
| Check | A different model from the assembler | Checks each item against the acceptance checks and the claim sources |
| Inspect | A person, on a sample | Looks at rendered output for a sample of items |
| Release | A person | Approves the frozen manifest of what goes out ([rule card 8](../rules/08-two-session-execution.md)) |

Two rules decide whether to build a factory at all:

- **Pilot first.** Run three items end to end before running fifty ([rule card 9](../rules/09-pilot-before-scale.md)).
- **One-off unless proven.** Write items directly unless the pilot shows the factory gives better accepted quality or lower total cost, rework included. Factories often cost more than they save on small batches.

The [automations pack](../packs/automations/README.md) ships a batch document factory as working Google Apps Script, with these controls in the code.

## Pattern 4: creative production across models

Images, video and voice need models a text agent does not have, so creative work naturally spans several. The text agent leads; the media models make; a different model inspects.

```
 Lead agent (Claude Code)          Maker (media model)                 Inspector (a different model)
 brief, references, rights   ──►   image: an image model, or several   ──►  looks at the rendered output
 check, prompt, acceptance         through a router (for example            against the brief: text, hands,
                                   MiniMax models), Gemini or Codex         likeness, logos, consistency
                                   video: a video model, shot by shot       across shots, words in the audio
                                   voice: a text-to-speech model       ◄──  defect list back to the lead
                                                                             (fix, regenerate, look again)
                                          │
                                          ▼
                           A person approves before anything is published
```

1. **The lead writes the brief and the acceptance.** Purpose, size, style, what must and must not appear, and the rights and likeness check ([image-create](../packs/media/skills/image-create/README.md), [video-storyboard](../packs/media/skills/video-storyboard/README.md), [voiceover](../packs/media/skills/voiceover/README.md)).
2. **The maker generates a small set.** Two to four images, one take per shot, two voice takes. If you use a router, record which model made which file.
3. **A different model inspects the real output.** It opens the rendered image or frames, or a transcript of the audio, and lists defects against the brief. Using a different model from the maker catches more, because a model tends to accept its own mistakes.
4. **The lead fixes and regenerates**, up to a set number of rounds, then reports what remains.
5. **A person looks once and approves.** Generated media is never published on an agent's say-so.

For consistent characters across many images or shots, keep one reference sheet and pass it to every generation, and have the inspector compare each new output with the sheet.

## Pattern 5: parallel workers under a supervisor

Several agents work on independent pieces at once, each in its own folder or branch, with a supervisor that assigns work, enforces time and cost limits and collects results. Use it for genuinely independent pieces only; if the pieces depend on each other, run them in order.

- Each worker gets a bounded brief: scope, files it may touch, acceptance, stop condition.
- Workers never edit the same file.
- The supervisor integrates and runs the checks; a person accepts.
- Set explicit limits: number of workers, time, cost.

## Choosing the runtime for each job

| Job | Reasonable choice |
|---|---|
| Judgement, the acceptance card, final writing | The strongest model you have |
| Code changes with tests | A coding agent in the repository (Claude Code or Codex) |
| Bulk research and extraction | A small, cheap model |
| Images and short video | An image or video model, through a router if you use several, always followed by an inspection of the actual output |
| Independent review | A different model or runtime from the one that did the work |

No ranking of named models is given here, because model lines change monthly. See [model and tool routing](../ways-of-working/model-and-tool-routing.md) and test on your own work.

## What every pattern shares

- One owner, named before work starts.
- The same acceptance card for every agent.
- Hand-overs by file in `.work/`, with sources.
- A Claims block from every agent, checked rather than believed.
- External actions (send, post, publish, spend, delete) only after a person's yes.
