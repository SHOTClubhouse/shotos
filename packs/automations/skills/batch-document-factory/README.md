# batch-document-factory

**A guided, safe setup for a free Apps Script that makes one Google Doc or Slides file per sheet row from a master template.**

The skill walks an agent and a person through checking the template and the data, a dry run, a sample of three documents read back against the source, and only then the full batch with its self-scheduling continuation.

It supports the Operate stage. It serves rule 1, Stop at the boundaries, rule 3, Read back the real result, and control 9, [pilot before scale](../../../../rules/09-pilot-before-scale.md).

## The problem it solves

Northgate Cycles (a fictional shop) needs a service reminder letter for each of 180 customers. Someone suggests a script. Without a method, the script runs on all 180 rows, a placeholder is misspelt in the template, and 180 letters say "Dear {{first_name}}". Or a customer record contains a note that should never reach a letter, and it does. Or the output folder is shared with the whole company and every letter is visible.

## What the agent does differently

It checks the template tokens against the columns first, agrees banned terms, and recommends a private output folder. It runs a dry run that creates nothing, then three real documents that a person opens and compares with the source rows. Only then does it run the batch, and afterwards it reconciles counts. It never sends the letters; that step belongs to the owner.

## When to use it, and when not to

Use it when the same document is needed for dozens or hundreds of rows, or when a batch already made needs a rerun, retry or audit.

Do not use it for a handful of documents, for text nobody has approved, or to send or share anything.

## Who it is for

- **Operations lead:** quotes, letters, certificates and onboarding packs without copy and paste.
- **Small business owner:** the same polish for every customer.
- **Admin team:** a Report tab that shows what was made, what was blocked and why.
- **Enablement coach:** a worked example of pilot before scale.

## How to use it

Install the pack (see the [pack README](../../README.md)). Then ask:

> I have a service reminder letter template in Google Docs and a sheet of 180 customers. Set up the batch document factory. Make three first so I can check them, and do not send anything.

You get an acceptance record, a template and data check, steps to follow in your browser, and a read-back after the sample.

## How it connects

- The script and its setup steps: [scripts/batch-document-factory/README.md](../../scripts/batch-document-factory/README.md).
- Sister skill for mail: [signal-engine](../signal-engine/README.md).
- Controls behind it: [docs/controls.md](../../../../docs/controls.md).
- Before: [agree-acceptance](../../../../skills/agree-acceptance/README.md). After: [evidence-handoff](../../../../skills/evidence-handoff/README.md).

## Needs

A Google account, a master template (Google Doc or Slides), a sheet of rows, and a person to paste the script and approve permissions.

## Tips

- Rename placeholders to plain words: `{{first_name}}`, not `{{Customer First Name (formal)}}`.
- Keep a private output folder until the sample is accepted.
- Banned terms are a safety net for data, not a replacement for reading the sample.
- To redo a row, clear its `done` cell; the old document is kept and recorded.

## Limits

- The agent cannot run the script in your account; a person runs each step and reports back.
- The script's check proves placeholders were replaced, not that the content is right.
- Google run-time quotas apply; large batches use the continuation trigger.
- The script was not run in a live account by its author; your dry run and sample are the real test.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/batch-document-factory/input.md) and [output](../../examples/batch-document-factory/output.md).
