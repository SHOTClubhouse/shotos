# What SHOTos covers, and what it does not

A plain map of where SHOTos is strong, where it is thin, and what it leaves out on purpose. It is updated with each release.

## Covered well

| Area | What you get |
|---|---|
| Delivering change | The six stages with exit checks, and 28 core skills from problem to rollout |
| Keeping agents honest | Four rules, twelve controls, claim-check and the Stop hook |
| Engineering practice | Specification by example, Definition of Done, engineering excellence, continuous delivery, DORA, role agents |
| Winning work | LEAP and NUDGE, proposals, factories, outreach, replies |
| Running the week | Daily brief, inbox triage, meeting notes, weekly brief, decision briefs, advisory sessions |
| Trust and safety | Claims audit, public-exposure check, children's and sensitive data, frozen approval manifests for bulk actions |

## Covered, with limits

| Area | What is covered | The limit |
|---|---|---|
| **Transcripts** | [meeting-notes](../packs/exec-ops/skills/meeting-notes/README.md) turns any transcript into notes with a dedup ledger; [voiceover](../packs/media/skills/voiceover/README.md) transcribes audio to check it | SHOTos does not transcribe recordings itself. You connect a transcription tool, or bring the transcript |
| **Translation** | [translate](../packs/writing/skills/translate/README.md) keeps names, numbers and meaning, back-translates key passages and flags what a fluent person must check | Not live interpretation. Not a substitute for a qualified translator on contracts, medical or safety material |
| **Social posts** | Account set-up, weekly plan, captions, publishing through an approval manifest, engagement review, group sharing, monthly insights | No automated posting, liking, following or commenting, on purpose. No paid advertising. Posting needs a person or your own scheduling tool |
| **Images, video, voice** | Briefs, rights and consent, inspection of the real output, labelling | SHOTos ships no media model. You connect one ([connect your tools](connect-your-tools.md)) |
| **Slides and documents** | Storyline first, sourced numbers, rendered check of every slide | Needs PowerPoint tooling locally or a Google Slides connector |
| **Websites and campaign pages** | [Build a Small Website](../packs/content/skills/build-small-website/README.md), [Campaign Website](../packs/content/skills/campaign-website/README.md) and [Verify a Live Release](../packs/setup/skills/verify-live-release/README.md) cover visitor journeys, previews and public read-back | Ongoing site maintenance, search strategy and formal accessibility audits need their own process. |
| **Tenders and supplier selection** | [RFP Authoring](../packs/win-the-work/skills/rfp-authoring/README.md) gives buyers a response schedule and panel scorecard. [Bid Response](../packs/win-the-work/skills/bid-response/README.md) gives suppliers a compliance and approval record. | The buyer owns the award decision and any required procurement or legal review. |
| **Automations** | [Two Google Apps Script automations](../packs/automations/README.md) with automated checks for batch preflight, document receipts, digest recovery and sheet writes | Checks use simulated Google services. Validate an approved pilot in your own account. |
| **Measurement** | Baselines, evidence packs, DORA, cost per accepted task | No dashboard; the numbers live in your files and tools |

## Not covered yet

These are common needs SHOTos does not have a skill for. The core skills and the four rules still apply to them.

- **Finance:** bookkeeping, invoicing, forecasting and cash flow.
- **People:** recruitment, onboarding new staff, performance reviews and rotas.
- **Legal:** contract drafting and review. Skills here would only ever prepare material for a lawyer.
- **Customer support desks:** ticket triage and help-centre maintenance at volume.
- **Events:** planning, ticketing and running the day.
- **Data analysis:** a general skill for spreadsheets and dashboards beyond the baseline and evidence pack.

## Left out on purpose

- **Autonomous external actions by default.** Actions that send, post, buy, delete or publish need authority. The signal engine's scheduled digest requires separate setup and approval. Use the [graduation ladder](../rules/12-graduation.md) to record any authority granted for recurring work.
- **Automated social engagement.** Bots that like, follow or comment break platform terms and damage trust.
- **Bundled credentials or accounts.** You bring and control your own.
- **Named-model rankings.** Model lines change monthly; [model routing](../ways-of-working/model-and-tool-routing.md) gives the method instead.
- **Any real organisation's data.** Every example is invented.

## Needs more focus next

- **Other runtimes.** Codex, Gemini, Antigravity, ChatGPT and the Claude app upload need the same outcome runs as Claude Code.
- **Live automation runs.** The two Apps Script automations need a recorded end-to-end run.
- **macOS and Linux.** [Release CI](https://github.com/SHOTClubhouse/shotos/commit/69b752f1f4087e049ef7b0bdf34feec28759809c/checks) covers Windows, macOS and Linux.
- **Rule 1 in practice.** The first outcome runs showed an agent asking permission for something the owner had already asked for. Rule 1 now says a clear request is the yes for what it names. The next runs check that the fix holds without losing caution where it matters.

Suggest a gap, or a skill to fill one, through [CONTRIBUTING.md](../CONTRIBUTING.md).
