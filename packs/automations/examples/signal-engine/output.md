# Output

Before anything runs, two points:

- The engine emails the account owner only. Sending to your team is a separate decision for you, so I have left it out. You can forward the digest yourself.
- Nothing will be scheduled until you have seen three real items and said yes. Friday is possible if the pilot is clean by Wednesday; I will not skip the pilot to meet it.

## Acceptance record (draft, waiting for your yes)

- Owner: the Harbourside Lettings account holder.
- Label: Signals (you create it and the filter; the script never creates labels).
- A good digest: the five items you would have wanted to read, mostly lease law, planning notices or yield.
- The engine must not reply, forward, label, archive or delete mail, or email anyone but you.
- Who can open the sheet: please tell me. It will hold titles, links and snippets from your mail.

## Priorities to enter (you confirm the weights)

| Keyword | Weight |
|---|---|
| lease | 3 |
| planning notice | 3 |
| rental yield | 2 |
| sponsored | -2 |

## Steps for you (I cannot do these in your account)

1. Create a sheet, open Extensions > Apps Script, paste `Code.gs` and `appsscript.json` from the pack.
2. Run `setup` and approve the permissions. Tell me the four tabs exist.
3. Enter the priorities above.
4. Run `collectSignals` and `sendDigest` in dry-run mode. Paste me the Log tab.

## What I will check with you after that

- Dry run: messages found, plausible items and scores, nothing written to Queue, no email sent.
- Pilot of three messages: queue rows match the source mail, one digest to you only, mail untouched, a rerun adds no duplicates.
- Then I ask for your yes before `installTriggers`.

## Claims
- [unverified] Script behaviour in your account: not run yet.
- [unverified] That the label holds only newsletters and alerts: you confirm.
