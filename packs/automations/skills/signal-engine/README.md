# signal-engine

**A guided, safe setup for a free Apps Script that turns newsletters and alerts into one scored daily digest.**

The skill walks an agent and a person through installing the signal engine, proving it in dry-run mode, running a three-message pilot, reading the result back in the sheet and the inbox, and only then putting it on a schedule.

It supports the Build step. It serves rule 1, Stop at the boundaries, and rule 3, Read back the real result.

## The problem it solves

The owner of Harbourside Lettings (a fictional agency) subscribes to planning-law newsletters, a property-portal alert and two local news feeds. Forty messages arrive each day, and the useful five are buried. Someone suggests an automation. Without a method, the script goes live on day one, scores things oddly, and the owner finds out when an important alert is missing. Or it is pointed at the wrong label and starts storing private tenant mail in a shared sheet.

## What the agent does differently

It writes down the label, the owner and what a good digest looks like before anything runs. It hands the pasting and the permission approval to the person, because it cannot do them. It reads the dry-run log with the person, runs three messages for real, then checks the queue, the processed list and the inbox, and reruns to prove no duplicates appear. Scheduling comes last and needs a yes.

## When to use it, and when not to

Use it for a new install, a change (new label, new priorities, AI scoring), or a health check of an engine already running.

Do not use it to add replying, forwarding, auto-labelling or deleting. The script never does these. Do not use it on private correspondence.

## Who it is for

- **Small business owner:** a quiet daily read instead of a crowded inbox.
- **Operations lead:** a repeatable setup you can hand to a colleague.
- **Researcher or analyst:** alerts scored against your topics.
- **Enablement coach:** a worked example of dry run, pilot and read-back on a real tool.

## How to use it

Install the pack (see the [pack README](../../README.md)). Then ask:

> Set up the signal engine for my "Signals" label. My priorities are lease law changes, council planning notices and rental yield. Walk me through it and do not schedule anything until I have seen three real items.

You get an acceptance record, exact steps for you to follow in your browser, and a check at each step.

## How it connects

- The script and its setup steps: [scripts/signal-engine/README.md](../../scripts/signal-engine/README.md).
- Sister skill for documents: [batch-document-factory](../batch-document-factory/README.md).
- Controls behind it: [docs/controls.md](../../../../docs/controls.md).
- Before: [agree-acceptance](../../../../skills/agree-acceptance/README.md). After: [report-with-evidence](../../../../skills/report-with-evidence/README.md).

## Needs

A Google account and a person to paste the script and approve permissions. Optional: an AI provider key, stored in Script Properties by the person.

## Evidence

Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 4 of 4, Sonnet 4 of 4, Opus 4 of 4. Without: Haiku 4 of 4, Sonnet 2 of 4, Opus 3 of 4. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips

- Start with fewer than ten keywords. Add more when the digest misses something.
- Use negative weights for noise such as "sponsored".
- Keep the label narrow; a broad label produces a noisy digest.
- If the digest is empty on day one, check the label and filter before changing scores.

## Limits

- The agent cannot run the script in your account. The pilot is something the person does and reports.
- Extraction works best on plain-text newsletters with links.
- Google quotas apply.
- The script was not run in a live account by its author; your dry run and pilot are the real test.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/signal-engine/input.md) and [output](../../examples/signal-engine/output.md).
