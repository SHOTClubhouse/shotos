# group-sharing

**Decide whether a post belongs in a community group, draft text that suits that group, and leave the posting to a person.**

For each group the skill checks the written rules, the audience and when you last shared there. It gives a decision (share, ask the admin first, do not share) with the rule quoted, then writes a different short text for each group that is a yes. It supports the Build step and serves rule 1, Stop at the boundaries, and rule 4, Claim only what you can show.

## The problem it solves

A community choir (fictional) has a spring concert. The secretary pastes the same advert into twelve local groups on one afternoon. Three groups ban promotion and remove the post, one admin blocks the account, and the concert is not mentioned where it would have been welcome. Two groups see the identical text twice, a week apart.

## What the agent does differently

It asks for each group's rules instead of assuming them. It marks two groups "do not share" with the rule quoted, one "ask the admin first", and picks the four that fit. It writes four different texts, each in a member's voice, with only the details the group allows. The secretary posts them and logs the links.

## When to use it, and when not to

Use it for events, volunteer calls and local notices that might suit community groups.

Do not use it to post at volume, to join groups for promotion, or when the post identifies a child without recorded consent.

## Who it is for

- **Club or society secretary:** fewer removed posts.
- **Small business owner:** local goodwill instead of complaints.
- **Volunteer coordinator:** targeted calls for helpers.
- **Group admin:** a way to see why a post suits the group.

## How to use it

> We have a spring concert on 14 April. Here are the rules of the five local groups we belong to and the dates we last shared in each. Tell me where to share, draft different text for each, and I will post them myself.

## How it connects

- Pack overview: [packs/social](../../README.md).
- Uses an approved caption from [caption-options](../caption-options/README.md).
- Results feed [insights-review](../insights-review/README.md).

## Needs

The group rules (pasted), the dates of earlier shares, and a person to post. Nothing else beyond the agent.

## Evidence

Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 4 of 4, Sonnet 4 of 4, Opus 4 of 4. Without: Haiku 4 of 4, Sonnet 4 of 4, Opus 4 of 4. See [evidence](../../../../docs/evidence.md) for how to read this.

## Tips

- Ask the admin before the first promotional share. A short message earns more trust than a removed post.
- Offer something useful to members, not only an advert.
- Reply to comments on your own shares. People remember who showed up.

## Limits

- Group rules change and may be unwritten. The agent works from what you paste.
- The agent cannot see which groups you belong to.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/group-sharing/input.md) and [output](../../examples/group-sharing/output.md).
