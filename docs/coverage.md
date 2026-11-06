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
| **Automations** | Two complete Google Apps Script automations with safe defaults, syntax-checked | Not yet run in a live Google account |
| **Measurement** | Baselines, evidence packs, DORA, cost per accepted task | No dashboard; the numbers live in your files and tools |

## Not covered yet

These are common needs SHOTos does not have a skill for. The core skills and the four rules still apply to them.

- **Finance:** bookkeeping, invoicing, forecasting and cash flow.
- **People:** recruitment, onboarding new staff, performance reviews and rotas.
- **Legal:** contract drafting and review. Skills here would only ever prepare material for a lawyer.
- **Customer support desks:** ticket triage and help-centre maintenance at volume.
- **Websites:** building and maintaining a site, search optimisation and accessibility audits.
- **Events:** planning, ticketing and running the day.
- **Procurement:** supplier selection and tendering.
- **Data analysis:** a general skill for spreadsheets and dashboards beyond the baseline and evidence pack.

## Left out on purpose

- **Autonomous external actions by default.** By default nothing sends, posts, buys, deletes or publishes on its own. The one scheduled send is the signal engine's daily digest to the owner's own address. Beyond that, autonomy is earned per task class through the [graduation ladder](../rules/12-graduation.md), where the owner writes down what the agent may do unprompted.
- **Automated social engagement.** Bots that like, follow or comment break platform terms and damage trust.
- **Bundled credentials or accounts.** You bring and control your own.
- **Named-model rankings.** Model lines change monthly; [model routing](../ways-of-working/model-and-tool-routing.md) gives the method instead.
- **Any real organisation's data.** Every example is invented.

## Needs more focus next

- **Evidence for the packs.** Earlier versions of all 82 skills ran in the paired evaluation. Changes after that run need their own evidence. See [evidence](evidence.md).
- **Other runtimes.** Codex, Gemini, Antigravity, ChatGPT and the Claude app upload need the same outcome runs as Claude Code.
- **Live automation runs.** The two Apps Script automations need a recorded end-to-end run.
- **macOS and Linux.** The v1.1.0 automated test matrix passed on Windows, macOS and Linux. Live runtime coverage is recorded separately.
- **Rule 1 in practice.** The first outcome runs showed an agent asking permission for something the owner had already asked for. Rule 1 now says a clear request is the yes for what it names. The next runs check that the fix holds without losing caution where it matters.

Suggest a gap, or a skill to fill one, through [CONTRIBUTING.md](../CONTRIBUTING.md).
