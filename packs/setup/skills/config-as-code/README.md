# config-as-code

**Keep a team's agent instructions and skills in one repository, review changes like code, install from it, and check for drift before every sync.**

This skill treats shared agent instructions, skills and settings as code. One repository is the shared version. Each person installs from it into their own tools. A drift check reports differences between what is installed and the repository before any sync, and useful local improvements come back through a reviewed change. Nothing is overwritten without showing the difference first.

It supports the Sustain and Scale stage. It serves rule 3, Read back the real result, and control [03, mode-contract](../../../../rules/03-mode-contract.md): capability is separate from authority.

## The problem it solves

Northgate Cycles has an agent set up on two laptops. One person edits a skill in their installed copy and forgets; another syncs from the repository and wipes the edit. Three weeks later the agent behaves differently on each machine and nobody knows why. With one repository, a drift check and a reviewed route back, the difference is visible before it hurts.

## When to use it, and when not to

Use it when instructions, skills or settings live in more than one place, when more than one person or machine uses them, or after someone edits an installed copy that might be worth keeping.

Skip it for a personal tweak you do not want to keep. Do not use it to copy secrets, tokens or machine-specific paths into a shared repository.

## Who it is for

- Teams running the same agent set-up on several machines or for several people.
- Team leads who want changes to agent behaviour reviewed.
- Maintainers of a shared skill library.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Check whether my installed agent files have drifted from our team repository. Show me the differences. Do not change either side.

You get a drift report listing files only in the repository, only installed and changed in both, with the difference for each. For each one you choose install, propose back, or keep local. Only then does anything change.

## How it connects

- **Related:** [skill-audit](../skill-audit/README.md) checks the skills in the repository for wiring.
- **Related:** [mode-ladder](../mode-ladder/README.md) is one of the team defaults worth keeping in the repository.
- **Rules:** [03, mode-contract](../../../../rules/03-mode-contract.md) and [04, stop-boundaries](../../../../rules/04-stop-boundaries.md).

## Needs

Nothing beyond the agent, plus read access to the repository and the installed location, and write access only for the step the owner approves. Git is assumed for the repository.

## Tips and common mistakes

- Check for drift before every install, not after.
- Send local improvements back one at a time with a message that says why, and have a teammate review them.
- Keep secrets and machine-specific values out of the repository; use a local, ignored settings file.
- Keep a log of each install so it can be undone.

## Limits

- It compares files, not behaviour. Two identical files can still act differently if a setting elsewhere changed.
- It does not merge conflicting edits; the owner decides line by line.
- Installed locations differ between agents; the owner must name the correct one.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/config-as-code/input.md) and [output](../../examples/config-as-code/output.md).
