# Signal engine (Apps Script)

**Reads the mail under one Gmail label, scores each item against your priorities, queues the items in a sheet and emails you one digest a day.**

It reads mail and writes to a sheet. It does not reply to, forward, label, archive or delete anything. Its only outgoing email is the digest, which goes to `DIGEST_TO` (blank means the account that owns the script).

## What it does

1. Looks for messages under one label you choose (for example "Signals"), newer than seven days, oldest first, up to `MAX_PER_RUN` (60) per run. It pages through the label, so nothing past the first page is missed; the Log tab says how many messages are still waiting.
2. Pulls out the items in each message. An item is a link and the words around it. A message with no links becomes one item.
3. Scores each item: the sum of the weights of the keywords in your Priorities tab, with a title match counting double. Optionally adds an AI score from 0 to 10.
4. Writes the items to the Queue tab and records each message ID in the Processed tab, so a rerun skips finished work.
5. Once a day, emails the owner the top items and marks them as digested.
6. Removes old rows on a schedule you set.

## Files

- `Code.gs`: the script. Configuration is at the top.
- `appsscript.json`: the manifest (runtime, permissions and the Gmail advanced service).

## Setup

Time: about 15 minutes.

1. In Gmail, create a label (say "Signals") and a filter that applies it to the newsletters and alerts you want read. The script never creates labels itself.
2. Create a new Google Sheet. Open **Extensions > Apps Script**.
3. Replace the contents of `Code.gs` with this folder's `Code.gs`.
4. Open **Project Settings**, tick **Show "appsscript.json" manifest file in editor**, then replace its contents with this folder's `appsscript.json`.
5. Change `LABEL_NAME` at the top of `Code.gs` if your label is not "Signals". Save.
6. Run `setup`. Approve the permissions when Google asks. The script asks for: read your mail (`gmail.readonly`, through the Gmail advanced service), see your email address (`userinfo.email`, to find the default digest recipient), edit this spreadsheet, send the digest email, manage its own triggers and make web requests (only used for AI scoring). If you paste the manifest in by hand, check that **Services** lists Gmail.
7. Optional: set `DIGEST_TO` (in `CONFIG` or Script Properties) to send the digest to a different single address. Blank means your own account. Live mode stops with an error if no address can be found.
8. Open the new **Priorities** tab. Replace the sample rows with your own keywords and weights. A weight can be negative to push noise down.

## Modes

The script starts in **dry run**: it reads and scores with keywords, and writes only to the Log tab. Email and external AI scoring wait for live mode. Modes are Script Properties (Project Settings), switched by running a function:

| Run this | Effect |
|---|---|
| `enableDryRunMode` | Nothing is queued, marked or sent. The Log shows what would happen. |
| `enablePilotMode` / `disablePilotMode` | Limits each collect run to three messages. |
| `enableLiveMode` | Items are queued and digests are sent. |

Recommended order: dry run, then pilot plus live mode (three messages), then check the Queue tab and your digest, then remove the pilot limit, then install triggers.

## Functions to run by hand

| Function | Use |
|---|---|
| `setup` | Creates the tabs. Safe to run again. |
| `collectSignals` | Reads and scores new mail. |
| `sendDigest` | Sends today's digest (once per day). `sendDigestAgain` sends another. |
| `installTriggers` | Hourly collect and a daily digest around 07:00. |
| `removeTriggers` | Removes only this script's triggers. |

## Recover a pending digest

If a send or queue update is interrupted, both scheduled and manual sends pause while `PENDING_DIGEST` exists in Script Properties. The record contains a digest reference, date, recipient and queue item keys. Check that the earlier execution has finished, then look for that exact reference in the recipient's mailbox.

- If you confirm the digest arrived, mark its listed item keys `digested` in **Queue**, record the delivery time, and make sure `LAST_DIGEST_DATE` reflects the digest date. Then clear `PENDING_DIGEST`.
- If you verify it was never sent, clear `PENDING_DIGEST` and rerun the intended digest when ready.
- If delivery remains uncertain, leave the reservation in place while you investigate.

## Optional AI scoring

Off by default. To turn it on, add these in **Project Settings > Script Properties** (never in the code or the sheet):

- `AI_ENABLED` = `true`
- `AI_API_KEY` = your key
- `AI_ENDPOINT` = the direct HTTPS URL of an approved OpenAI-compatible chat completions endpoint
- `AI_MODEL` = a model name your provider accepts

The request carries the item's title and short snippet, and the configured priority keywords and weights. Review those fields before enabling the provider. The script waits up to 20 seconds for the endpoint and treats redirects as failures. If the provider fails, it falls back to keyword scores for that run and records the reason in the Log. Final score = keyword score + AI score x `AI_WEIGHT`.

## Safety design

- **Lock:** `LockService` stops two runs overlapping. A run that cannot get the lock logs and stops.
- **Idempotent:** processed message IDs, and a unique key for each queued item, make a rerun harmless.
- **Time budget:** a run stops starting new messages after five minutes; the rest wait for the next run.
- **Self-cleaning:** Queue rows after 30 days, Processed rows after 90, Log rows after 30 (change in `CONFIG`). `LOOKBACK_DAYS` must stay below the Processed retention.
- **Sheet writes:** mail and log text that looks like a formula is written as literal text. Retention cleanup writes the retained rows and clears the unused tail together.
- **Fixed recipient:** the digest goes to `DIGEST_TO`, or to the script owner's own address when that is blank. Nothing in mail or the sheet can change it. Live mode throws an error, after logging it, if the address is empty.
- **Backlog:** each run takes at most `MAX_PER_RUN` messages, oldest first. The rest wait for the next run and the Log tab records how many are left. Mail older than `LOOKBACK_DAYS` is not read, so raise that setting (and keep it below the Processed retention) if a long gap is possible.
- **Failures are loud:** an error is written to the Log tab and then rethrown, so a trigger run shows as failed in Apps Script and you get Google's standard failure email.
- **Untrusted text:** mail content is treated as data. The AI reply is reduced to one number and clamped to 0 to 10.

## Limits and honest caveats

- Apps Script quotas apply, for example a daily limit on emails sent and on web requests. A consumer account has lower limits than Workspace; see Google's current quota page.
- Item extraction is simple. It suits newsletters with links; it will not parse heavy HTML layouts perfectly.
- The script has been syntax-checked and its text functions tested outside Google. It has not been run in a live account by the author, so do your own dry run and pilot.
- Scopes: reading uses the Gmail advanced service on `gmail.readonly`, so the permission itself is read-only. If Google's consent screen shows a broader Gmail permission, stop and check before approving. Not yet confirmed in a live account: that the consent screen lists only read access.
- Mail contents go into your sheet. Share the sheet only with people who may read that mail.
