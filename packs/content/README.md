# content pack

**Six skills for writing, presenting, explaining, announcing and demonstrating: every fact sourced, every quote approved, every publish step waiting for a yes.**

The six skills cover the content a team puts in front of outsiders. Each one drafts and checks. None publishes, posts or sends. Each has a fixed gate, a separate record of evidence or approvals, and a named person whose yes comes before anything leaves the project.

Use [campaign website](skills/campaign-website/README.md) for a preview with one primary action.

## Who it is for

- Founders, marketing leads and communications officers who publish papers, explainers, announcements, demos and creator content.
- Small teams who want an agent to draft and check, while a person approves and publishes.
- Creators who want help with their drafts while keeping their own voice.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [written-content](skills/written-content/README.md) | Operate | Papers, reports, one-pagers and blog posts on a six-part arc, every fact sourced, a fixed QA gate, and a separate publish step. |
| [explainer](skills/explainer/README.md) | Operate | Classifies the explainer (technical, business, external), drafts with worked examples, illustrates only where a picture shows the mechanism, runs a fixed QA gate, files it, publishes on a yes. |
| [press-release](skills/press-release/README.md) | Operate | Classifies the relationship before the headline, treats every quote as unsaid until approved, keeps evidence and approvals apart, adds a consent path for anything involving children. |
| [product-demo-video](skills/product-demo-video/README.md) | Operate | Scripts a walkthrough, captures real interactions on test data in the browser, adds chapters and subtitles, inspects the final render and checks that no real personal data appears. |
| [creator-edit](skills/creator-edit/README.md) | Operate | Edits a creator's draft while keeping 85 to 95 per cent of their own wording, checks facts, consistency and risk, packages per channel, and leaves final approval to the creator. |
| [slide-deck](skills/slide-deck/README.md) | Operate | Agrees the reader and the ask, writes one message per slide before designing, builds an editable deck, sources every number, and renders and looks at every slide before calling it ready. |

## Needs

- Nothing beyond the agent for drafting and checking.
- Playwright (or another browser automation tool that records video) for product-demo-video.
- Editing tools to trim a video, add chapters and attach subtitles, for product-demo-video.
- An image model of your choice, if an explainer needs an illustration.
- Optional: a document or file connector to read sources and file the result. Publishing tools are used only after the owner's yes.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack content --dry-run
python ../shotos/install.py --runtime claude --scope project --pack content
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The skills follow the four rules in [docs/controls.md](../../docs/controls.md). Anything that publishes, sends or posts stops for the owner's yes under [rules/04-stop-boundaries.md](../../rules/04-stop-boundaries.md). The stages are described in [docs/framework.md](../../docs/framework.md).
