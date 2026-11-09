# research-and-assemble

**Gather facts with their sources, keep fact, inference and guess apart, write the piece, then check every claim against its source before anyone relies on it.**

The agent keeps a source log while it researches, marks each item as fact, inference or guess, notes conflicts and gaps, assembles the output with source references, and then goes back through every claim and checks it against the source.

It belongs to the Operate stage. It serves rule 4, Claim only what you can show, and rule 3, Read back the real result.

## The problem it solves

Northgate Cycles wants a one-page briefing on whether to start selling electric bikes, to read before a supplier meeting. A quick agent run gives a confident page: "the UK e-bike market grew 12% last year" and "most buyers want a 100 km range". Neither has a source. One came from an old press release, and the other from a forum post that the agent turned into a trend.

## What the agent does differently

It records each fact with the quote, source and date, and finds the 12% figure comes from a trade body release two years old, for a different category. It marks the range claim as a guess because only one forum thread supports it. After writing the briefing it goes back through each claim and softens or removes those that do not match the source. See [examples/research-and-assemble/output.md](../../examples/research-and-assemble/output.md).

## When to use it, and when not to

Use it for briefings, comparisons, reports and proposals built from outside material. Skip it for a quick lookup you will check at once.

## Who it is for

- **Owner or manager:** a briefing you can trust when you walk into a meeting.
- **Analyst or researcher:** a source log you can hand to someone else.
- **Anyone using an agent for desk research:** protects against confident, unsourced text.

## How to use it

> Research whether Northgate Cycles should start selling e-bikes. Use only the public pages and files I list. Keep a source log and check the claims at the end.

Read the handover note first, then the log entries behind the claims that matter most. The [source authority example](source-authority-example.md) shows how to handle a headline that conflicts with the applicable evidence.

## How it connects

- **Before:** [route-the-work](../route-the-work/README.md) sizes the risk, and [agree-acceptance](../agree-acceptance/README.md) fixes what the briefing must contain.
- **After:** [label-the-proof](../label-the-proof/README.md) labels each part of the result, and [cross-agent-review](../cross-agent-review/README.md) adds a second agent's check where the risk justifies it.
- **Rules:** [docs/controls.md](../../docs/controls.md).

**Needs:** Web access or the files you provide, depending on the sources. No logins, and no contact with anyone, are needed or allowed.

## Tips

- Two sources that quote each other are one source.
- Put the date next to every figure. Old numbers look the same as new ones on a page.
- If you cannot find something, write "not found". It is a result.

## Limits

- The check against sources is only as good as the source. A wrong source gives a wrong, well-sourced claim.
- The agent cannot see pages behind a login or paywall.
- Reading a source again is not the same as an expert reading it.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/research-and-assemble/input.md) and [output](../../examples/research-and-assemble/output.md).
