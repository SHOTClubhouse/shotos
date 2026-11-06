# file-naming

**Name files so they sort, say what they are and show their version, and show the rename plan before changing anything.**

This skill names files in the spirit of ISO 15489 records management: a date, an owner, a subject and a version, in the pattern `YYYY-MM-DD_owner_subject_vNN.ext`. It says when to drop parts, how to handle versions, when a status word helps, and it shows a rename plan, with a collision check, before any file changes.

It supports the Build step. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show (a name should not claim more than the file is).

## The problem it solves

Northgate Cycles keeps `Final.docx`, `Final2.docx`, `final_REAL.docx` and `Copy of Final.docx` in one folder. Nobody knows which was sent to the supplier. A naming convention with dates and versions would have told them, and a rename plan would have shown that two of the four are identical before anyone touched a file.

## When to use it, and when not to

Use it when creating files that others or future agents must find, when a folder has inconsistent names, or when versions are piling up.

Skip it for files a tool names itself and expects to find by that name, such as `package.json`, `README.md` or a build output. Do not rename files that other documents link to without listing those links first.

## Who it is for

- Office managers and administrators with shared folders.
- Agents producing files that people must find later.
- Anyone handing a folder to a colleague or an auditor.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Our supplier folder is a mess of Final and Final2 files. Propose a naming scheme and show me the rename plan. Do not rename anything yet.

You get the pattern, the rules for dropping parts, and a table of current name, proposed name and reason, with any collisions marked. Nothing is renamed until you say yes.

## How it connects

- **Related:** [filing-and-dedupe](../filing-and-dedupe/README.md) decides which folder a file belongs in; this skill decides what it is called.
- **Related:** [work-folder](../work-folder/README.md) uses the same pattern for task folders.
- **Rules:** [10, claim-discipline](../../../../rules/10-claim-discipline.md) is why a status word such as final must be earned.

## Needs

Nothing beyond the agent, plus read and write access to the one project folder it is working in. No connectors.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 3, Sonnet 3 of 3, Opus 2 of 3. Without: Haiku 1 of 3, Sonnet 1 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips and common mistakes

- Use ISO dates, year first, so the folder sorts by time.
- Use lower case, hyphens inside a part and underscores between parts.
- Keep names under about 60 characters.
- Add `final` only when the owner has accepted the file, and keep one final per set.

## Limits

- Renaming breaks links, scripts and references that use the old name; the plan lists the ones it can see, not all of them.
- The pattern is a convention, not a standard to certify against.
- The date it uses is the document date; if it cannot tell, the plan says so and asks.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/file-naming/input.md) and [output](../../examples/file-naming/output.md).
