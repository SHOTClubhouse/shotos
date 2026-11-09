---
name: signal-engine
description: Sets up and checks an Apps Script engine that scores mail under one Gmail label and sends the owner a daily digest. Use when newsletters, alerts or RSS need a digest. Pilot first; no replies, forwards or deletes.
---

# Set up and run the signal engine

Stage: Operate. Rules served: 1 Stop at the boundaries, 3 Read back the real result. The script is `Code.gs` in the SHOTos repository at `packs/automations/scripts/signal-engine/`, or in `.shotos/packs/automations/scripts/signal-engine/` in a project where SHOTos is installed; read the README beside it first.

## Context and handoff

Confirm the source label, the Gmail filter that feeds it (the script has no sender list of its own, so the filter decides which senders it reads), the destination and the replay window. Check the same message ID twice before relying on a schedule.

Use `mode-ladder` before enabling a scheduled run. Keep the processed-ID record and failure log with the approved automation. Rehearse with a test label and a fixture sheet before the real label; real mail content never goes into the repo, this record or the chat.

## If used on its own

If `Code.gs`, its README or `mode-ladder` is not in the project, do not write the script from memory or describe steps as if it were installed.

- Give the person a small request: owner, label, the Gmail filter that decides which senders reach it, digest recipient, what a good digest looks like and who can open the sheet. Add that the engine starts as a dry run, then a pilot of three messages, and nothing is scheduled without the owner's yes.
- You cannot paste into Apps Script, approve permissions or open their mailbox. Report "not installed", "dry run done" or "pilot done" only on evidence they paste, such as the Log tab or the Sent-mail digest reference.
- If they ask for replies, forwards, deletion or a digest to several people, say this engine does not do that and stop.
- API keys go in Script Properties, set by the person. Never ask for one in chat.

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
7. **Read back the real result.** Open the Queue tab, the Processed tab and the owner's Sent mail, using read-only checks only. Check three things: each queued item matches its source message; the owner's Sent mail holds exactly one digest, addressed to the configured recipient (`DIGEST_TO`, or the owner's address if blank), with its "Digest reference" line; no mail changed (no new labels, nothing archived or deleted). Sent mail proves the digest was sent to that address, once. Only the recipient's own confirmation proves receipt. If the recipient's receipt matters and nobody has confirmed it, record it as unverified; do not contact them or open their mailbox to find out, and leave any later confirmation to the owner. Rerun `collectSignals` and confirm no duplicate rows (idempotence).
8. **Optional AI scoring.** Only if the owner wants it. The key goes in Script Properties by the person; never ask for it in chat, never write it in a file. Compare ten items with and without AI and let the owner decide whether it earns its place.
9. **Owner accepts.** Show the pilot evidence. Wait for a yes.
10. **Schedule.** Only after the yes: `disablePilotMode`, then `installTriggers`. Confirm the trigger list and the mode, and record the date, the owner and how to switch off (`removeTriggers`, `enableDryRunMode`).
11. **Recover safely.** If a digest run stops or `PENDING_DIGEST` is set, do not resend, and leave the marker in place while delivery is uncertain. First confirm the earlier execution has ended. Then look for the exact digest reference from the marker in the owner's Sent mail, or get confirmation of that reference from the configured recipient (`DIGEST_TO`, or the owner's address if blank). Do not open the recipient's mailbox. The exact reference in Sent proves the digest was sent, not received; recipient confirmation proves receipt. Either is enough evidence of send to prevent a duplicate, so with either, and the owner's go-ahead to change state, mark the listed item keys `digested` and clear `PENDING_DIGEST`. Use no recipient mailbox and make no contact for verification. Absence of a Sent match alone never proves it was not sent. Clear the marker and rerun only with positive proof it was never sent (for example the earlier execution's log shows it failed before sending) and the owner's go-ahead. With neither proof, stop, report what is unknown and keep the marker. Follow the README steps exactly. After an outage, `collectSignals` can be rerun: processed IDs make it skip finished work. If the Log shows repeated errors or lock skips, `removeTriggers`, `enableDryRunMode` and tell the owner.
12. **First week check.** After a week, review the Log for errors and lock skips, and tune the Priorities with the owner.

## Output

A filled [template.md](template.md): acceptance, settings, pilot evidence and the schedule decision. Keep it with the project and give its location, the spreadsheet location, the mode, the trigger state and the next owner in the handoff.

## Checks

- Nothing is scheduled before the pilot is read back and the owner has said yes.
- Pilot proof is one digest in the script owner's Sent mail, with the exact reference and the configured recipient; receipt by the recipient is reported as unverified unless they have confirmed it unprompted, and no recipient mailbox was opened and no one was contacted for it.
- No API key appears in chat, code, sheet or log.
- The digest goes to one address, the owner's unless the owner sets `DIGEST_TO`; no step sends mail to anyone else.
- The report separates installed, executed (pilot ran) and accepted (owner said yes).
- A rerun adds no duplicate Queue rows and no second digest for the same items.
- `PENDING_DIGEST` is cleared only after the earlier run has ended and the exact digest reference is found in the owner's Sent mail or confirmed by the recipient; no recipient mailbox was opened, and an uncertain case keeps the marker and no rerun.
- If a dry run shows zero messages or obviously wrong items, the skill stops and fixes rather than going live.
