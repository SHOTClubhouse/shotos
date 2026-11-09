---
name: skill-audit
description: "Audits a skill collection for wiring: frontmatter, README, examples, eval cases, links, and descriptions that would collide on the same request. Use when releasing, adding or renaming skills. Checks wiring, not usefulness."
---

# Audit the wiring of a skill collection

Stage: Track. Rules: 3 (read back the real result) and 4 (claim only what you can show).

This audit asks whether the skills are connected correctly. It does not ask whether they are good. Say that in the report.

## Context and handoff

Read the installed skill list, source versions and real task history. Compare declared behaviour with actual opened files and outcomes.

Use `skill-quality-gate` before promoting a change. File findings against the owning skill and its version.

## Trigger and minimum inputs

Run it before a release, after adding or renaming a skill, or on a schedule. It needs the collection folder and the eval file. With only a description of the collection, say the audit is from description and limited. Any runtime that can read files can run it.

## When not to use this

Skip a single skill still being drafted. Do not use this audit as proof that a skill works or is useful.

## Steps

1. **Fix the scope.** Name the collection folder and the eval file. List every skill folder found. If you are given a description of the collection instead of the files, audit from the description and say so. If a script cannot run, do the checks by reading the files and say that you did.
2. **Check the frontmatter** of each `SKILL.md`: starts and ends with `---`; has `name` equal to the folder name in kebab-case; has a one-line `description` of what it does and when to use it, under 1,024 characters.
3. **Check the files.** Each skill must have `SKILL.md` and `README.md`; at least one example with an input and an output; and, where the skill produces a fill-in document, a `template.md`.
4. **Check the eval cases.** Find the skill's cases in the eval file. Each skill needs at least one normal and one contrary case, and each case needs a prompt and must-contain terms. Report skills with none.
5. **Check the links.** Follow every relative markdown link in each README and `SKILL.md`. Report any that do not resolve, with the file and line.
6. **Check for collisions.** Compare every pair of descriptions. Where two overlap, write one realistic request that both would match and say which should win. Record the pair as a collision and suggest sharpening one description, merging, or adding a "when not to use this" line that points to the other. Do not rewrite descriptions in this run.
7. **Check the evidence status.** Each README must state one of: tested in paired evals (with a link to the result), cases written not yet run, or example only. Flag any that claim more than the history shows.
8. **Report.** Give a table of skills against checks (pass, fail, missing), the collision list, the broken links and the evidence-status flags. Finish with a plain line: "This audit checks wiring only. It does not show that any skill is correct, useful or good practice."
9. **Stop.** Make no fixes unless the owner asks, and then make them in a separate change.

## Output

Use [template.md](template.md). Save it where the owner keeps release notes, for example `.work/skill-audit.md`.

## Blockers and handoff

If the eval file or a skill folder cannot be read, mark those checks "not run" and say why; do not pass them. Hand each finding to the owner of the skill it names. Hand quality questions to `skill-quality-gate`.

## Checks

- Every skill in the folder appears in the table.
- Every failure names the file, and every collision names a sample request.
- The report contains the wiring-only statement.
- No file was changed.
