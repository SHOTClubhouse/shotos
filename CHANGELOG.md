# Changelog

## 1.0.0 (6 November 2026)

The full method, not only the rules.

- **Rules:** twelve agent controls as rule cards, and six guardrails (data governance, security, scale, productivity, pace, quality).
- **Ways of working:** specification by example, Definition of Ready and Done by output type, engineering excellence, continuous delivery and DevOps, DORA metrics, product over project, Team Topologies, roles, evals for AI output, records and filing, model and tool routing, context and tokens, and a glossary.
- **Core skills:** 24 new, for 28 in all, covering every step.
- **Packs:** twelve, with 54 skills. They are exec-ops, win-the-work (LEAP and NUDGE), founder-admin, customer-success, content, media, writing, social, automations (two complete Google Apps Script scripts, syntax-checked, not yet run in a live Google account), records, trust and setup. Each pack is also a Claude Code plugin.
- **Commercial templates:** LEAP and NUDGE quick references, a qualification sheet and mapping-ready HubSpot and Salesforce CSV headers. Live CRM import remains untested and account fields need mapping.
- **Measurement:** an accepted-work ledger and study protocol to test total rework, review and handoff cost, rather than treating one model run as the whole outcome.
- **Role agents and review lenses:** nine role agents for Claude Code, plus seven review lenses and a cast file for bringing your own characters.
- **Tools:**
  - `graduation_log.py` records acceptance per task class and reports the rung each class has earned.
  - The installer gains `--pack`, `--all-packs`, `--list-packs` and `--with-agents`.
- **Guides:**
  - Start-here guides for an enterprise operations leader, a small business and a startup founder.
  - Multi-agent patterns: one agent does and another checks, one researches while another holds context, and factories.
  - A comparison with other frameworks.
  - Four diagrams.
- **Outcome evals:** ten real tasks graded on the files, tests, git state and report each run produced. They are run with and without SHOTos on Haiku, Sonnet and Opus, with a paired sign test. These replace the keyword-graded pilot as the headline evidence.
- **Skill evals:** all 212 skill cases run with and without SHOTos on Haiku, Sonnet and Opus, graded by meaning with a model judge that is blind to the condition (`evals/judge_paired.py`). The runner installs the skill's own pack, stops after repeated timeouts and records runtime refusals.
- **More runtimes:** the installer adds `--runtime gemini`, `--runtime antigravity` and `--runtime all` (one command for Claude Code, Codex, Gemini CLI and Antigravity, with one `AGENTS.md`). Both put the skills where the runtime looks for them and add `@AGENTS.md` to `GEMINI.md`, so Claude Code, Codex, Gemini CLI and Antigravity all load the same four rules from one `AGENTS.md`. Install paths follow each tool's documentation; neither has had a live run yet.
- **Working agreement:** `AGENTS.md` tells the agent to open the matching skill even when the request does not name it, and lists common corners to decline while still doing the work.
- **Tests:** the package tests cover every pack skill, pack manifest, role agent and eval case.
- **Claim evidence:** `[git] committed` requires a starting commit and a newer descendant; a clean checkout alone no longer passes.
- **Stop hook:** checks all assistant text in the turn and refuses a completed-work report backed only by `[unverified]`.
- **Codex:** two local runtime smoke checks opened installed skills, one by explicit name and one by matching the task; no paired Codex outcome eval yet.
- **Skill archives:** every Claude-app zip now includes the licence and creator attribution notices.
- **Evidence:** a blind semantic re-judge of the same skill outputs is published alongside the original results; individual verdict variability is disclosed.

## 0.1.0 (internal development milestone; not publicly released)

Documentation:
- New personas guide: seven readers, each with jobs, what goes wrong today, a first week, a good month, maturity and objections.
- The four rules guide rewritten, with business and technical examples, adoption at three sizes and edge cases.
- Full product pages for each skill, a 30-question FAQ, and expanded maturity, why and prerequisites guides.

Fixes from the first independent release review:
- Uninstall records paths relative to the project, refuses anything outside it and keeps files you changed after install. A failed install rolls back, and invalid `settings.json` stops the install before any change.
- A `[git] committed` claim now fails when a claimed file was never committed.
- `base` must name a real commit; option-shaped values are refused.
- Commands are a trust decision: a project's own config cannot make claim-check or the Stop hook run them.
- The Stop hook only challenges completion language when the agent changed something that turn, and no longer reacts to everyday words such as "shared".
- Claude Code installs add `@AGENTS.md` to `CLAUDE.md`, so the four rules actually load.
- SHOTos is defined as a five-step work loop (Brief, Build, Check, Hand over, Improve), with the four rules running inside every step.

The initial 0.1.0 development baseline included:

- Four controls: stop at the boundaries, agree acceptance first, read back the real result, claim only what you can show.
- Four skills: capture-the-problem, agree-acceptance, report-with-evidence, evidence-handoff.
- `claim-check` tool, Claude Code Stop hook and deterministic installer, with automated tests (45 at this release).
- Templates, worked examples, eval cases, manifesto and maturity guide.
- claim-check understands real-world formatting: backticked paths, comments in brackets, several files on one line, numbered lists.
- Cross-platform hook launcher that finds a working Python 3.9 or later; project installs no longer write a machine-specific path.
- Walkthrough with a fictional company, data and reference outputs, checked by tests.
- Project installs add `.work/` to `.gitignore` (and remove it on uninstall), so the drafting folder the rules mention really is ignored.
- `AGENTS.md` points to where the Claims format is actually installed. Found by running the walkthrough live.
- Self-check, docs index, governance, support, releasing and issue templates.
- Paired-eval harness and first results on Claude Code: 20 of 20 cases passed with SHOTos, 13 of 20 without.
- Each skill now carries its own template, after the first eval run showed the handoff skill could not find a template stored outside its folder.
