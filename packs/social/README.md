# Social pack

**Seven skills for running social media with an agent, for any brand, club, creator or small business.** The agent plans, drafts and checks. A person approves and, for anything that touches an audience, a person or a frozen manifest does the publishing.

## Who it is for

- A club, charity or society that has one volunteer running the accounts.
- A small business owner who posts between other jobs.
- A creator who wants a steady calendar without losing their voice.
- A marketing lead who wants a record of what was approved and what went out.

Nothing in it is tied to one brand. The skills ask for your brand guide, your events and your assets, and they work from those.

## The skills

| Skill | Stage | What it does |
|---|---|---|
| [account-setup](skills/account-setup/README.md) | Scope | Builds or audits a profile: name, bio, link, profile image, highlights or pinned posts, checked against your brand guide. |
| [content-calendar](skills/content-calendar/README.md) | Hypothesise | Plans one week of posts from real events and available assets, with a set content mix (default 40% education, 40% community, 20% promotion). Each slot has an owner, an asset, a caption status and an approval status. |
| [caption-options](skills/caption-options/README.md) | Operate | Writes five caption options (A to E) and platform variants from a photo or brief, with facts checked and no claims you cannot back. |
| [publish-with-manifest](skills/publish-with-manifest/README.md) | Operate | Publishes only through a frozen approval manifest: exact posts, platforms, times, assets and checksums. Execution happens in a fresh step, then every post is read back live. |
| [engagement-review](skills/engagement-review/README.md) | Operate | Reviews comments, mentions and messages and proposes replies or actions for a person to approve. Never automates likes, follows, comments or messages. |
| [group-sharing](skills/group-sharing/README.md) | Operate | Decides whether a post suits a community group, drafts the share text, and leaves the posting to a person. |
| [insights-review](skills/insights-review/README.md) | Track | A monthly review of platform insights against the plan, which adjusts next month's content mix. |

## Children and consent

Any post that shows or names a child needs recorded parental or guardian consent before it is drafted for publication, planned in a calendar, or put in a manifest. "Recorded" means a person can point to where the consent is kept, what it covers and when it was given. The skills ask for this, mark unconfirmed assets as not usable, and stop rather than guess. Consent also needs to cover the platform and the kind of use. Where a message or comment comes from or concerns a child, or raises a safeguarding worry, the agent does not reply: it flags the item to the person responsible for safeguarding.

## What the pack never does

- Like, follow, comment or message on anyone's behalf. Platform terms and trust both forbid automation of these.
- Publish, schedule or post anything without a person's yes, and without a frozen manifest where the pack publishes.
- Invent events, results, quotes, statistics or testimonials.
- Share a post into a group; a person posts it.

## Needs

- Your brand guide, or a short description of your voice, colours and things you never say.
- Real events and available photos, with consent status for any that show people.
- Platform insight exports (CSV or screenshots with dates) for the monthly review.
- Optional: a scheduling tool or connector. Without one, the manifest is a checklist a person works through, and a person reads each post back.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack social --dry-run
python ../shotos/install.py --runtime claude --scope project --pack social
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## Evidence

Earlier skill versions were tested in paired runs. See the [evidence by build](../../docs/evidence.md). Cases: [evals/packs/social.json](../../evals/packs/social.json).
