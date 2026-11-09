# Capabilities

**Date:** 3 November
**Runtime:** Claude Code in VS Code on Windows

| Capability | Status | Tool | Test run and result |
|---|---|---|---|
| Python and git | works | Python 3.12, git 2.47 | `python --version` and `git --version` returned versions |
| Local slides (python-pptx, LibreOffice render) | missing | none | `import pptx` failed; `soffice` not found |
| Google Slides, Docs, Sheets, Drive | connected, not tested | Google Drive connector | No approved test target was named, so no call was made. No Slides tool is exposed by this connector |
| Mail (drafts only) | missing | none | No mail tool available |
| Calendar (read) | missing | none | No calendar tool available |
| Speech (text to speech) | missing | none | No speech tool available |
| Transcription (speech to text) | missing | none | No transcription tool available |
| Images | missing | none | No image tool available |
| Video and ffmpeg | missing | none | `ffmpeg -version` not found |
| Browser (Playwright) | missing | none | No browser tool available |
| Apps Script automations | not checked | n/a | Runs in the owner's Google account, outside this agent |

## Gaps and the skills they affect

| Missing capability | Skills affected | Step that will stop | How to connect |
|---|---|---|---|
| Local slides or Google Slides | slide-deck | Build and render steps | `pip install python-pptx` and install LibreOffice, or add Google's Slides MCP server |
| Speech and transcription | voiceover | Generate and listen-back steps | Add the ElevenLabs hosted MCP server in Claude Code's MCP settings |
| Video and ffmpeg | video-storyboard | Produce and stitch steps | A video model of your choice, and install ffmpeg |
| Images | image-create | Generate step | An image model your agent can call |

## What you can do today

- The Christmas order form: yes. It needs only files.
- The bank slides: the storyline, the numbers and the sources now; the deck itself once slides are connected. Quickest route: `pip install python-pptx` and install LibreOffice.
- The video and voiceover: the storyboard and script now; audio and video once speech and a video model are connected.

## Next connection to make

Local slides (python-pptx and LibreOffice): free, no account, and it unblocks the bank deck this week.

Nothing was sent, posted, published or bought during this check. File saved to `.work/capabilities.md` and read back.
