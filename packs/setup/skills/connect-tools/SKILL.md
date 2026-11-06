---
name: connect-tools
description: Tests which tools the agent can reach (slides, mail, calendar, speech, images, browser, git) with harmless read-only calls and writes .work/capabilities.md. Use when SHOTos is installed, a tool is connected, or a skill stops on a missing tool.
---

# Check what tools are connected

Find out, with evidence, which tools this agent can use, so skills fail early and honestly instead of halfway through.

**Stage:** any, first used in Scope. **Rules served:** rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## When not to use this

Do not use it to set up accounts or create credentials; that is the owner's job. Do not use it to test a tool by doing real work with it.

## Steps

1. **List what you have.** Write down every tool, connector and MCP server available to you in this session, and check for local tools: `python --version`, `git --version`, and whether `python-pptx`, LibreOffice (`soffice`), `ffmpeg` and Playwright are installed.
2. **Map them to capabilities.** For each capability on this list (local slides, Google Slides, speech, transcription, images, video and ffmpeg, browser, mail, calendar, documents, Apps Script), note which tool would serve it, or "none".
3. **Test each one read-only.** Make the smallest harmless call that proves access: list one folder, read one calendar day, list available voices, open a blank browser page, import `pptx`. Never send, post, publish, create live documents or generate paid media during the check. If the only possible test costs credits or creates something, mark it "connected, not tested" and say why.
4. **Record the evidence.** For each capability, write: status (works, connected not tested, missing), the tool, the test you ran and its result.
5. **Name the affected skills.** For each missing capability, list the skills that need it and the step that will stop.
6. **Say how to connect each missing tool.** Point to the matching row of the connect-your-tools guide: `docs/connect-your-tools.md` in the SHOTos repository, or `.shotos/docs/connect-your-tools.md` in a project where SHOTos is installed. If neither can be opened, give a one-line pointer per tool from the list above (for example: python-pptx and LibreOffice for local slides; a Google Slides or Drive connector for Google Slides; a text-to-speech service or its MCP server for speech; a speech-to-text tool for transcription; an image model for images; a video model plus ffmpeg for video; Playwright for browser work; a Gmail or Outlook connector for mail; a calendar connector for calendar; Drive, Docs and Sheets connectors for documents; a Google account for Apps Script). Do not connect anything yourself that needs the owner's account or credentials.
7. **Write the file.** Save `.work/capabilities.md` from [template.md](template.md), dated. Read it back to confirm it saved.

## Output

`.work/capabilities.md`: date, runtime, a capability table with status, tool and test evidence, the skills affected by each gap, and the next connection to make.

## Checks

- Every "works" entry has a test that actually ran, with its result.
- Nothing was sent, posted, published or bought during the check.
- Every gap names the skills it affects and how to connect it.
- The file exists and was read back.
