# account-setup

**Build or audit a social profile against your brand guide, then hand the owner exact edits to apply.**

The agent looks at the live profile (not memory), checks name, bio, link, profile image, highlights or pinned posts, contact details and admin access, and returns a pass or fix for each with the evidence. It supports the Brief step and serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

Millbrook Rovers youth club (a fictional club) has an account that three volunteers have run over four years. The bio still lists last season's training night, the link goes to a page that no longer exists, the profile image is cropped badly, and one person holds the only login. Nobody knows what "on brand" means because the guide lives on a laptop. Posts look fine; the front door does not.

## What the agent does differently

It asks for the brand guide first, or agrees a stand-in. It inspects the live profile and cites what it saw. It checks the link opens and that there are two admins with two-step sign-in. For a club with children it also checks message and tagging settings and keeps names and locations out of the bio. It writes replacement text ready to paste and does not touch the account.

## When to use it, and when not to

Use it when creating an account, after a rebrand, before a campaign, or once a year as a health check.

Do not use it to write posts, or to let the agent log in and edit.

## Who it is for

- **Volunteer running a club account:** a checklist that does not depend on memory.
- **Small business owner:** a consistent front door on every platform.
- **Marketing lead:** a dated record of what was checked and fixed.
- **Safeguarding lead:** confirmation that message and tagging settings match policy.

## How to use it

> Audit our Instagram profile against our brand guide. Here is the profile link and the guide. Give me exact text for anything that needs changing, and do not touch the account.

## How it connects

- Next: [content-calendar](../content-calendar/README.md) once the profile is right.
- Controls: [docs/controls.md](../../../../docs/controls.md).
- Pack overview: [packs/social](../../README.md).

## Needs

The profile link or screenshots, and the brand guide or a stand-in. Nothing else beyond the agent.

## Evidence

Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 3 of 3, Sonnet 3 of 3, Opus 3 of 3. Without: Haiku 2 of 3, Sonnet 1 of 3, Opus 2 of 3. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips

- Screenshots with dates are fine if the agent cannot open the profile.
- Fix the link and the bio first; they are what new people see.
- Keep the audit with the brand guide and repeat it each season.

## Limits

- Platform limits and layouts change. The agent says "check the current limit" and does not guess.
- It cannot see private settings unless you show them.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/account-setup/input.md) and [output](../../examples/account-setup/output.md).
