# Ways of working

The [six stages](../docs/framework.md) say what to do: Scope, Hypothesise, Operate, Track, Own, and Sustain and Scale. The [four rules](../docs/controls.md) say how to behave inside each stage. These pages say how good teams actually do the work underneath. Most of the practice here is not new. It comes from public books, reports and years of teams learning what holds up, and each page credits its sources by name. What is new is the place of the agent: it writes more, faster and with more confidence than a person would, so the old checks matter more, not less.

Each page follows the same shape: what the practice is, why it matters with agents in the loop, the steps, what good looks like, the common ways it goes wrong, how it maps to the stages and rules, a short invented example and further reading. Read the page for the job you are about to do. You do not need to read them in order.

## The pages

| Page | What it covers | Read it if you are |
|---|---|---|
| [specification-by-example.md](specification-by-example.md) | Example mapping, Given/When/Then, three amigos, and eval sets for AI output | A product owner, analyst, tester or anyone agreeing what "done" means |
| [definition-of-ready-and-done.md](definition-of-ready-and-done.md) | When work can start, and the concrete checks that finish each kind of output | Anyone who accepts work, or hands it to an agent |
| [engineering-excellence.md](engineering-excellence.md) | Test-first, small batches, trunk-based development, review, refactoring, observability, security | An engineer, a tech lead, or a manager of either |
| [continuous-delivery-and-devops.md](continuous-delivery-and-devops.md) | Pipelines, feature flags, deploy versus release, rollback, running what you build | An engineer or operations lead who ships to real users |
| [dora-metrics.md](dora-metrics.md) | The four keys plus reliability, how to measure them simply, and AI measures | A team lead or sponsor who wants evidence for Track |
| [product-over-project.md](product-over-project.md) | Outcomes over output, long-lived teams, discovery with delivery | A sponsor, product owner or budget holder |
| [team-topologies.md](team-topologies.md) | Four team types, three interaction modes, cognitive load, where agents sit | A leader shaping teams, or a coach planning Own and Sustain |
| [roles.md](roles.md) | Analyst, designer, engineer and QA responsibilities, whoever carries them | Every small team, and anyone briefing an agent in a role |
| [evals-for-ai-output.md](evals-for-ai-output.md) | Building and running eval sets, paired runs, regression, cost per accepted task | Anyone whose work includes output that varies |
| [records-and-filing.md](records-and-filing.md) | The `.work/` folder, naming, versions, duplicates, quarantine, retention | Everyone who creates files, and anyone tidying them |
| [model-and-tool-routing.md](model-and-tool-routing.md) | Matching jobs to classes of model and tool, and choosing output formats | Anyone choosing how an agent should do a job |
| [context-and-tokens.md](context-and-tokens.md) | Short instruction files, on-demand skills, large outputs in files, handoffs | Anyone running long agent sessions or paying for them |
| [language.md](language.md) | The words SHOTos uses and what they mean, and phrases to avoid | Everyone, especially anyone writing a report |

## Where to start

- **A small team starting out:** read [definition-of-ready-and-done.md](definition-of-ready-and-done.md), [roles.md](roles.md) and [records-and-filing.md](records-and-filing.md) first. They cost the least to adopt and show results within a week.
- **A team that already ships software:** start with [engineering-excellence.md](engineering-excellence.md) and [evals-for-ai-output.md](evals-for-ai-output.md), then add [dora-metrics.md](dora-metrics.md) so that Track has numbers.
- **A leader or sponsor:** read [product-over-project.md](product-over-project.md) and [team-topologies.md](team-topologies.md), then [language.md](language.md) so that reports mean the same thing to everyone.

## A note on borrowing

These pages describe public practice in the author's own words. They are not a substitute for the books named at the foot of each page, which go much further. If a page and a book disagree, trust the book and the evidence from your own team.
