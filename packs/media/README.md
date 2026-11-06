# media pack

**Three skills for making images, short videos and spoken audio that have been looked at or listened to, kept consistent and cleared for use.**

Generated images and video fail in ways that a quick glance misses: garbled text, extra limbs, characters that change between shots, borrowed likenesses, music without a licence. The pack makes the agent look at the real output, fix it, clear the rights and ask before anything is published.

## Who it is for

- Marketing leads and small business owners who make their own images and short videos with AI tools.
- Clubs, charities and teams who need a record that rights and consent were checked.
- Editors who want generated work inspected before it goes live.

## Skills

| Skill | Step | What it does |
|---|---|---|
| [image-create](skills/image-create/README.md) | Build | Brief, references, generate, then look at the actual output and fix it before use; rights and likeness check, alt text, AI label where required. |
| [video-storyboard](skills/video-storyboard/README.md) | Build | Storyboard to shot list to generated or filmed shots to a stitched cut, with consistent characters and settings and the full render checked. |
| [voiceover](skills/voiceover/README.md) | Build | Script to spoken audio with the voice model you choose: consent for any real or cloned voice, a listen-back by transcript against the script, fixes, and a synthetic-speech label where required. |

## Needs

- An image model, a video model and a text-to-speech model of your choice, available to the agent. SHOTos does not pick one for you.
- A speech-to-text tool, so the agent can check what the audio actually says.
- Editing tools for crops, stitching, audio and captions.
- Cameras and a person to film, if some shots are filmed rather than generated.
- Music and voice you own, have licensed or have written consent to use.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack media --dry-run
python ../shotos/install.py --runtime claude --scope project --pack media
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack to a project that already has SHOTos, run `python ../shotos/install.py --uninstall`, then install again with every pack you want. Files you changed are kept. If a changed file is in the way, the reinstall stops: move it aside (or keep your copy and skip that skill) before you reinstall.

As a Claude Code plugin:

```
/plugin marketplace add SHOTClubhouse/shotos
/plugin install shotos-media@shotos
```

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The skills follow the four rules in [docs/controls.md](../../docs/controls.md). Anything that publishes, sends or posts stops for the owner's yes under [rules/04-stop-boundaries.md](../../rules/04-stop-boundaries.md). The steps are described in [docs/framework.md](../../docs/framework.md).

**Evidence:** Cases written, not yet run. Eval cases are in [evals/packs/media.json](../../evals/packs/media.json).
