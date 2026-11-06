# Connect your tools

SHOTos skills hold the method: what to do, in what order, what to check and when to stop. They do not contain accounts or integrations. The work itself is done with whatever tools your agent can reach. So what works on day one depends on what you connect.

## What works straight after install

Most of SHOTos needs nothing beyond the agent, Python and git:

- every core skill, the four rules, claim-check and the Stop hook;
- writing, analysis and planning skills: proposals, decision briefs, explainers, plain-English checks, NUDGE and LEAP, evidence packs, runbooks;
- anything that reads and writes files in your project, such as Markdown, CSV, spreadsheets and code.

Some skills need a tool for one of their steps. Without it, the agent still does the method and stops at the step it cannot do. For example, it writes and checks the voiceover script, then tells you it has no voice tool. It does not pretend.

## Connect what you need

Connect only what your work needs, read-only first. Every option below uses your own account and credentials; SHOTos ships none.

| To do this | Connect one of these | How | Skills that use it |
|---|---|---|---|
| **Make slides locally** (PowerPoint) | Python with `python-pptx`, and LibreOffice to render slides as images for checking | `pip install python-pptx`; install LibreOffice; the agent renders with `soffice --headless --convert-to pdf` | [slide-deck](../packs/content/skills/slide-deck/README.md), [proposal-factory](../packs/win-the-work/skills/proposal-factory/README.md) |
| **Make slides in Google Slides** | Google's Slides MCP server, a Google Workspace connector in your agent, or the Slides API with your own Google Cloud credentials | Follow [Google's guide to configuring the Slides MCP server](https://developers.google.com/workspace/slides/api/guides/configure-mcp-server) (it uses OAuth; check Google's current docs, as this is changing); in Claude apps, add the Google Drive connector | [slide-deck](../packs/content/skills/slide-deck/README.md), [contextual-proposal](../packs/win-the-work/skills/contextual-proposal/README.md) |
| **Speech and voiceovers** | ElevenLabs (hosted MCP server), or any text-to-speech service your agent can call | Add the ElevenLabs hosted MCP server at `https://api.elevenlabs.io/v1/mcp` in your agent's MCP settings; it signs in with OAuth. The older local server ([elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp)) is deprecated. Check the provider's current docs before you rely on either | [voiceover](../packs/media/skills/voiceover/README.md) |
| **Check what a voiceover says** | A speech-to-text tool: ElevenLabs transcription through the same server, or another transcription service | As above | [voiceover](../packs/media/skills/voiceover/README.md), [meeting-notes](../packs/exec-ops/skills/meeting-notes/README.md) |
| **Images** | An image model your agent can call: the image tools built into Codex or ChatGPT, Gemini, or several models through a model router | Depends on the provider; most need an API key in an environment variable or an MCP server | [image-create](../packs/media/skills/image-create/README.md) |
| **Video** | A video model your agent can call, directly or through a router, plus a local editor such as `ffmpeg` to stitch | Provider key or MCP server; `ffmpeg` installed locally | [video-storyboard](../packs/media/skills/video-storyboard/README.md) |
| **Browser work and real screenshots** | Playwright | In Claude Code: `claude mcp add playwright npx @playwright/mcp@latest` | [product-demo-video](../packs/content/skills/product-demo-video/README.md), [public-exposure-check](../packs/trust/skills/public-exposure-check/README.md) |
| **Mail and calendar** | A Gmail or Outlook connector or MCP server, read-only first, with draft creation rather than sending | In Claude apps, add the Gmail and Google Calendar connectors; elsewhere, the provider's MCP server | [daily-brief](../packs/exec-ops/skills/daily-brief/README.md), [inbox-triage](../packs/exec-ops/skills/inbox-triage/README.md), [email-reply](../packs/win-the-work/skills/email-reply/README.md) |
| **Documents and sheets** | Google Drive, Docs and Sheets connectors, or local Office files | Connector in your agent, or files in the project | [weekly-exec-brief](../packs/exec-ops/skills/weekly-exec-brief/README.md), [data-room](../packs/founder-admin/skills/data-room/README.md) |
| **Scheduled automations** | A Google account, for Apps Script | Copy the scripts in [automations](../packs/automations/README.md) into a new Apps Script project | [signal-engine](../packs/automations/skills/signal-engine/README.md), [batch-document-factory](../packs/automations/skills/batch-document-factory/README.md) |

Product names and set-up steps change. Check each provider's own documentation for the current way to connect.

## Check what your agent can reach

After connecting, ask your agent to run the [connect-tools](../packs/setup/skills/connect-tools/README.md) skill:

> Check which tools you can reach for SHOTos and write the capability list.

It lists what is connected, tests each one with a harmless read-only call, and writes `.work/capabilities.md`: what works, what is missing, and which skills are affected. Other skills read that file, so they can tell you early when a step needs a tool you have not connected.

## The safe way to connect anything

- Read-only first. Add write access only after you have seen the agent read correctly.
- Drafts, not sends. Choose connector settings that create drafts rather than sending or publishing.
- Keep keys out of the project. Use the runtime's secret handling or environment variables, never `AGENTS.md`, a skill or a committed file.
- A test account or folder for the first runs.
- Remove access you no longer use.
