# skill-audit

**Audit a collection of skills for wiring: valid frontmatter, a README, examples, eval cases, working links, no overlapping descriptions and an evidence status each. It does not judge business quality.**

This skill checks that every skill in a collection is wired up correctly. It checks the frontmatter, that a README, examples and eval cases exist, that links resolve, that no two descriptions would trigger for the same request (by comparing descriptions), and that each skill has an evidence status. It says clearly that it checks wiring, not whether the skill is good business practice.

It supports the Track stage. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

Northgate Cycles has grown a folder of twenty skills. Two of them describe nearly the same job, so the agent picks one at random. One has no examples. Another links to a file that was renamed. Nobody notices because each skill looked fine alone. An audit across the collection finds the collisions and gaps in an afternoon.

## When to use it, and when not to

Use it before releasing a collection, after adding or renaming skills, and on a schedule for a library that several people edit.

Skip it for a single skill you are still drafting. It does not tell you whether a skill is useful, correct or good for the business; that needs people using it and evidence from real runs.

## Who it is for

- Maintainers of a shared skill library.
- Team leads who let several people add skills.
- Anyone preparing a collection for release.

## How to use it

Install SHOTos as described in the [main README](../../../../README.md#install). Then ask:

> Audit the skills folder for wiring. Check frontmatter, README, examples, eval cases, links, description collisions and evidence status. Report only; change nothing.

You get a table of skills against checks, a list of collisions with the requests that would trigger both, a list of broken links and a summary line stating what the audit does and does not show.

## How it connects

- **Related:** [config-as-code](../config-as-code/README.md) keeps the audited collection in one source.
- **Format:** [docs/skill-format.md](../../../../docs/skill-format.md) defines what each skill must have.
- **Claims:** [10, claim-discipline](../../../../rules/10-claim-discipline.md): an evidence status is honest only if it matches the run history.

## Needs

Nothing beyond the agent, plus read access to the skills folder and its eval file. Optionally a short script to check links, which the agent can write.

## Tips and common mistakes

- Run it after every rename.
- For collisions, write a sample request that both descriptions would match; if you cannot, it may not be a collision.
- Keep evidence status to the three states the format allows.
- Do not fix findings in the audit run; log them and fix in a separate change.

## Limits

- It checks wiring only. A well-wired skill can still be wrong or useless.
- Collision checking by comparing descriptions is a judgement, not a measurement; confirm borderline pairs by testing real requests.
- It cannot tell whether eval cases are good, only that they exist and cover normal and contrary.

Files: [SKILL.md](SKILL.md) (for the agent), [template.md](template.md), [example input](../../examples/skill-audit/input.md) and [output](../../examples/skill-audit/output.md).
