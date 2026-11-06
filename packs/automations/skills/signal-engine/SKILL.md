---
name: signal-engine
description: Sets up and checks an Apps Script engine that scores mail under one Gmail label and sends the owner a daily digest. Use when newsletters, alerts or RSS need a digest. Pilot first; no replies, forwards or deletes.
---

# Set up and run the signal engine

Stage: Operate. Rules served: 1 Stop at the boundaries, 3 Read back the real result. The script is `Code.gs` in the SHOTos repository at `packs/automations/scripts/signal-engine/`, or in `.shotos/packs/automations/scripts/signal-engine/` in a project where SHOTos is installed; read the README beside it first.

## Context and handoff

Confirm the source labels, allowlisted senders, destination and replay window. Check the same message ID twice before relying on a schedule.

Use `mode-ladder` before enabling a scheduled run. Keep the cursor and failure log with the approved automation.

## When not to use this

- The person wants replies, forwards, auto-labelling or deletion of mail. The script does none of that and this skill will not add it.
- The mail is private correspondence rather than newsletters and alerts. Do not point the engine at a personal or client label.
- Several people need the digest. It sends to one address, the owner's by default. Forwarding is a separate, human decision.

## Steps

1. **Agree acceptance.** Write down who the owner is, which label, what a good digest looks like (for example "the five items I would have wanted to read, in my top three topics") and what the engine must not do. Use [template.md](template.md).
2. **Check the ground.** Ask: does the label exist, what filter feeds it, roughly how many messages a day. Say plainly that the script reads mail content and stores titles, links and snippets in a sheet, and ask who else can open that sheet.
3. **Prepare the files.** Read `Code.gs` and `appsscript.json`. Set `LABEL_NAME` and any limits. Draft the Priorities rows (keyword, weight) with the owner; ask for their real topics rather than inventing them.
4. **Person installs.** The agent cannot paste into Apps Script or approve permissions. Give the person the numbered steps from the script README and wait. They must confirm that `setup` ran and the four tabs exist.
5. **Dry run.** Ask the person to run `collectSignals` in dry-run mode (the default) and `sendDigest`. Read the Log tab with them. Confirm: messages found, items extracted, plausible scores, nothing in Queue or Processed, no email sent. If the label is empty or items look wrong, fix before moving on.
6. **Pilot of three.** Run `enablePilotMode`, then `enableLiveMode`, then `collectSignals` and `sendDigest`. Three messages at most are processed.
7. **Read back the real result.** Open the Queue tab, the Processed tab and the owner's inbox. Check three things: each queued item matches its source message; the digest arrived once and only to the owner; no mail changed (no new labels, nothing archived or deleted). Rerun `collectSignals` and confirm no duplicate rows (idempotence).
8. **Optional AI scoring.** Only if the owner wants it. The key goes in Script Properties by the person; never ask for it in chat, never write it in a file. Compare ten items with and without AI and let the owner decide whether it earns its place.
9. **Owner accepts.** Show the pilot evidence. Wait for a yes.
10. **Schedule.** Only after the yes: `disablePilotMode`, then `installTriggers`. Confirm the trigger list and the mode, and record the date, the owner and how to switch off (`removeTriggers`, `enableDryRunMode`).
11. **First week check.** After a week, review the Log for errors and lock skips, and tune the Priorities with the owner.

## Output

A filled [template.md](template.md): acceptance, settings, pilot evidence and the schedule decision. Keep it with the project.

## Checks

- Nothing is scheduled before the pilot is read back and the owner has said yes.
- No API key appears in chat, code, sheet or log.
- The digest goes to one address, the owner's unless the owner sets `DIGEST_TO`; no step sends mail to anyone else.
- The report separates installed, executed (pilot ran) and accepted (owner said yes).
- If a dry run shows zero messages or obviously wrong items, the skill stops and fixes rather than going live.
