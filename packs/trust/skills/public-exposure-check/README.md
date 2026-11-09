# public-exposure-check

**Before publishing or sharing a repo, site, folder or document, look for secrets, personal data, internal paths and over-wide sharing, and report them without changing anything.**

This skill reads the thing about to be shared and looks for credentials and keys, personal data, internal paths and private names, files that should not be included, and sharing settings wider than intended. It reports each finding with its location and says urgently what should be rotated. It never rotates, deletes or unshares anything without the owner's yes.

It supports the Track stage. It serves rule 1, Stop at the boundaries, and rule 3, Read back the real result.

## The problem it solves

Harbourside Lettings is about to make a repository public so a contractor can read it. The history contains a payment provider key from an early test, a spreadsheet of tenant names, and a configuration file with an internal server path. Once the repository is public the key can be copied within minutes. A check before the switch finds all three and tells the owner which one to rotate first.

## When to use it, and when not to

Use it before making a repository public, publishing a site, sharing a folder or document by link, attaching files to a message to outsiders, or handing a project to another company.

Skip it for a private file that stays private. It is not a penetration test and it does not replace a security review of a live service.

## Who it is for

- Anyone about to publish or share something outside the team.
- Small teams without a security specialist.
- Agents asked to publish, deploy or send files.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Before I make this repository public, check it for secrets, personal data and internal paths. Report where each is. Do not change or delete anything.

You get a findings table with severity, location and what to do, an urgent list of anything that should be rotated, and a clear go or hold recommendation. Nothing is changed.

## How it connects

- **Related:** [claims-audit](../claims-audit/README.md) checks the same document for unsupported claims.
- **Related:** [sensitive-data-check](../sensitive-data-check/README.md) goes deeper when children's or special-category data appears.
- **Rules:** [04, stop-boundaries](../../../../rules/04-stop-boundaries.md): publish, rotate, delete and unshare are the owner's decisions.

## Needs

Nothing beyond the agent, plus read access to the item being checked. For a repository, read access to history helps. For shared documents, a way to read sharing settings, or a list from the owner.

## Tips and common mistakes

- Check the history, not just the current files; a deleted secret is still in history.
- Treat any real key found as exposed, and say rotate first, then clean.
- Look at filenames and metadata too: a file called `passwords` or an author field with a private name.
- Check the sharing setting last, then say who can see it now.

## Limits

- It finds what it recognises. A secret in an unusual format may be missed.
- It cannot see systems it has no access to, such as a cloud account's access rules.
- It reports; removing a secret from history is a separate task that needs the owner's yes.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/public-exposure-check/input.md) and [output](../../examples/public-exposure-check/output.md).
