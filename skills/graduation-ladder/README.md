# graduation-ladder

**Let a repeated agent task earn less supervision through a logged record of accepted work, class by class.**

The agent logs what a reviewer did with each output, reads the standing from `.shotos/tools/graduation_log.py`, and recommends a rung: draft only, run and notify, or run silently. The thresholds are 95 per cent accepted unedited over at least 50 samples for rung 2, and, for rung 3, at least 200 samples in total with at least 98 per cent accepted unedited over the most recent window (default 50). A class drops a rung when it falls below the bar. High-risk classes stay at rung 1 unless a named person promotes them.

It supports Sustain and Scale. It serves rule 1, Stop at the boundaries, and rule 4, Claim only what you can show. It is the practical form of control 12, graduation.

## The problem it solves

At a fictional firm, Harbourside Lettings, an agent drafts the weekly "rent arrears summary" for the finance lead. After a few good weeks someone says "just let it run". Without a record, nobody knows whether it was right 9 times in 10 or 99 in 100, and one wrong figure goes to a landlord.

With the ladder, the class `weekly-arrears-summary` starts at rung 1. After 54 reviewed outputs, 52 were accepted unedited (96 per cent), so it can be recommended for rung 2, with notice to the finance lead each week. A different class, `landlord-dispute-letter`, is high-risk and stays at rung 1 whatever its record.

## When to use it, and when not to

Use it when a repeated task could run with less supervision, and to review any class's standing. Skip it for one-off work. It never loosens the rule that sends, spending, deletion or publication need an owner's yes.

## Who it is for

- **Operations or business unit leader:** a clear basis for trusting an automation.
- **Engineering or practice lead:** a measurable way to relax review.
- **Small team lead:** know which tasks can run unattended and which cannot.
- **Governance or risk owner:** a record and a named promoter.

## How to use it

Log each reviewed output:

> After I review the arrears summary, record it: accepted unedited.

The agent runs `python .shotos/tools/graduation_log.py record --class weekly-arrears-summary --outcome accepted-unedited --by <name>`. To check the standing, ask:

> What rung is weekly-arrears-summary at, and should it move?

It runs `python .shotos/tools/graduation_log.py status --class weekly-arrears-summary`, shows the counts and recommends. You decide.

## How it connects

- **Before:** [skill-quality-gate](../skill-quality-gate/README.md) checks a skill before it earns a rung. [agree-acceptance](../agree-acceptance/README.md) defines accepted.
- **After:** [learning-loop](../learning-loop/README.md) turns the edits and rejections into improvements. [enablement-plan](../enablement-plan/README.md) prepares the team that reviews.
- **Control:** control 12, [graduation](../../rules/12-graduation.md), one of the [twelve controls](../../rules/README.md) behind the four rules.

## Needs

`.shotos/tools/graduation_log.py` in the repository (record and status commands) and Python. Without it the agent can describe the ladder but must say it cannot read the standing.

## Tips and common mistakes

- Keep classes narrow. "All emails" is too broad to mean anything.
- Log what the reviewer did, not what the agent thinks.
- A single serious error matters more than a rate; read the edits.
- Restart or re-review after changing the skill, model or data.
- High-risk means stay at rung 1 unless a named person writes down why not.

## Limits

- A rate shows past behaviour. It does not guarantee the next case.
- Counts can be gamed by reviewing carelessly. Sample some accepted outputs with a second reviewer.
- The tool records and reports. It does not enforce a rung; permissions do.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/graduation-ladder/input.md) and [output](../../examples/graduation-ladder/output.md).
