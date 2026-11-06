# Roadmap

Each item ships when it has evidence behind it, not before.

## Done in 1.0

- The five-step work loop, four rules, twelve agent controls and six guardrails.
- 28 core skills covering every step, and 12 packs with 54 more.
- Ways of working, role agents, review lenses and a cast file.
- Installer support for packs and role agents, and a Claude Code plugin per pack.
- Outcome evals: ten realistic synthetic tasks, graded on what the agent produced, run with and without SHOTos on three Claude models.

## Next

- **Accepted-work study:** run matched multi-step jobs with and without SHOTos, using the same inputs, tools, model and blind acceptance checks. Include an initial draft, a reviewer correction, a changed requirement and pickup by a second person or session. Count attempts, total model spend, elapsed time, reviewer minutes, rework, handoff pickup and defects after acceptance. Publish the task fixtures, reviewer rubric and all results, including a null or worse result. Start with proposals, inherited code and executive handoffs, then repeat on real team work with private data removed from the public record. [Measurement sheet](../templates/accepted-work-ledger.csv).
- **Other runtimes:** the same outcome evals on Codex and Gemini (including Antigravity), published whatever they show.
- **More platforms:** live agent runs of claim-check, the hook and the installer on macOS and Linux. The automated tests already run in CI on all three.
- **Remaining skill misses:** in the 3 November run, Haiku missed eight cases (daily-brief-02, file-naming-01, learning-loop-02, maturity-check-02, mode-ladder-03, one-off-or-factory-01, pilot-before-scale-01, route-the-work-02), Sonnet missed retrospective-02 and Opus missed file-naming-01 and one-off-or-factory-01. Repeat each to see which are steady.
- **Independent skill cases:** new cases written after the skills are frozen, plus repeats of the 212, since the current cases shaped the fixes they now pass.
- **Live automation runs:** the two Apps Script automations run end to end in a test Google account, with the read-back recorded.
- **Repeated runs:** more repeats per task, so differences between conditions can be told apart from run-to-run variation.

## Later

- **Enterprise bridge:** how the controls map to NIST AI RMF, ISO/IEC 42001 and EU AI Act human-oversight duties.
- **Community packs:** a review process and quality gate for packs written by others.
- **Translations** of the method, templates and guides.
