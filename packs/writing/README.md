# writing pack

**Two checks that make a draft read like a person wrote it, in plain English, without changing a fact.**

The pack holds two checks. One makes text easier to read. The other finds the patterns that make text sound machine-written. Both report every change with a before and after, keep the original, and never alter a fact, a number or a name.

## Who it is for

- Anyone who writes for a reader and wants a second pass before it goes out.
- Teams who use an agent to draft and need the result to sound like them.
- Editors who want a repeatable checklist.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [plain-english-check](skills/plain-english-check/README.md) | Track | Checks and fixes a draft for plain English: answer first, short sentences, active verbs, explained jargon, length to suit the reader. |
| [translate](skills/translate/README.md) | Operate | Translates or localises text, transcripts and captions with a glossary, a numbers-and-names check, back-translation of key passages and flags for a fluent reviewer. |
| [ai-tell-check](skills/ai-tell-check/README.md) | Track | Finds the patterns that make text read as machine-written, reports each with its line and a fix, and never changes a fact. |

## Needs

- Nothing beyond the agent. Both skills work on pasted text or a file in the project.
- Optional: your own voice sample and your own list of banned words, kept in the project.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack writing --dry-run
python ../shotos/install.py --runtime claude --scope project --pack writing
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The skills follow the four rules in [docs/controls.md](../../docs/controls.md). Anything that publishes, sends or posts stops for the owner's yes under [rules/04-stop-boundaries.md](../../rules/04-stop-boundaries.md). The stages are described in [docs/framework.md](../../docs/framework.md).
