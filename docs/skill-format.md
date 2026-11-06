# How a SHOTos skill is built

Every skill, in the core set or a pack, has the same parts. This keeps each skill usable on its own and checkable by the tests.

```
skills/<skill-name>/            (core skills)
packs/<pack>/skills/<skill-name>/  (pack skills)
  SKILL.md      for the agent: frontmatter (name, description), when not to use it, steps, output, checks
  README.md     for people: what, why, when, who, how, step, rules it serves, evidence status, limits
  template.md   optional: the fill-in document the skill produces
  example.md    a worked example: an input and an output that meets the checks (fictional)
```

## Rules for every skill

- `name` in the frontmatter matches the folder name. `description` says what it does and when to use it, in under 1,024 characters.
- `SKILL.md` stays near one page. Put long detail in `template.md` or a linked file.
- Every skill names its **step** (Brief, Build, Check, Hand over, Improve, or "any") and the **rules** it serves.
- Every skill that can act outside the project (send, post, publish, buy, delete) drafts by default and stops for a person's yes.
- Every skill has at least one normal and one contrary eval case, in `evals/cases.json` for core skills or `evals/packs/<pack>.json` for packs.
- Every README has an **Evidence** line using one of these states:
  - **Tested in paired evals**, linking to the result.
  - **Cases written, not yet run.**
  - **Example only.**
- Examples are invented. No real people, customers, companies or private data.
- Requirements (connectors, permissions, local tools) are listed under **Needs** in the README, or "Nothing beyond the agent".

## Packs

A pack is a folder in `packs/` with a `README.md` (what the pack is for, who it is for, the skills in it and what it needs) and a `.claude-plugin/plugin.json`, so it can be installed on its own as a Claude Code plugin or with `install.py --pack <name>`.
