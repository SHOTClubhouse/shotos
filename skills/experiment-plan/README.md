# experiment-plan

**Plan the cheapest test that could show your idea is wrong, and agree how it will be judged before it runs.**

The agent turns a hypothesis card into a plan: the riskiest assumption, the smallest method, the sample, the duration, the cost, the success and stop criteria, and the person who decides.

It belongs to the Hypothesise stage. It serves rule 2, Agree acceptance first, and rule 1, Stop at the boundaries.

## The problem it solves

Harbourside Lettings has a hypothesis that a repair-status chatbot will cut status calls. The supplier offers a three-month contract. The real risk is that tenants will not use a chatbot at all, and that can be tested for almost nothing before signing.

## What the agent does differently

It aims the test at that assumption. For two weeks, the repairs email gets a "check your repair status online" link to a plain page, and clicks are counted. It sets the success and stop numbers before the test, so the result cannot be argued into success afterwards. See [examples/experiment-plan/output.md](../../examples/experiment-plan/output.md).

## When to use it, and when not to

Use it between a hypothesis card and any build, purchase or rollout. Skip it when a quick lookup answers the question, or the work is required anyway.

## Who it is for

- **Founder or owner:** avoids paying for the full answer to find out the idea was weak.
- **Product or operations lead:** a one-page plan to attach to a request.
- **Delivery team:** a clear end date and decision point.

## How to use it

> Plan the smallest test for the chatbot hypothesis in `.work/chatbot/hypothesis.md`. Spend nothing on the supplier until the result is in.

Read the plan, change the criteria if needed, and confirm before the test starts.

## How it connects

- **Before:** [hypothesis-card](../hypothesis-card/README.md) and [baseline](../baseline/README.md).
- **After:** [pilot-before-scale](../pilot-before-scale/README.md) when the test is a limited run, and [report-with-evidence](../report-with-evidence/README.md) for the result.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent.

**Evidence:** Tested in a paired run on 3 November 2026, one run per case, graded by meaning. Cases passed with SHOTos: Haiku 2 of 2, Sonnet 2 of 2, Opus 2 of 2. Without: Haiku 1 of 2, Sonnet 1 of 2, Opus 2 of 2. See [evidence](../../docs/evidence.md) for how to read this.

## Tips

- Pick the test that could show you are wrong, not the one that is easiest to pass.
- Write the criteria down before anyone sees a number.
- A clear "stop" result is a good return on a small test.

## Limits

- Small samples show direction, not proof. The plan says so.
- The agent can plan a test but cannot run one that needs customers, money or live systems without the owner's yes.
- A short test misses slow effects.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/experiment-plan/input.md) and [output](../../examples/experiment-plan/output.md).
