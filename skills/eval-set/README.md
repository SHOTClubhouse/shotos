# eval-set

**A short list of real inputs with written expectations, so AI output that varies can be checked the same way every time.**

The agent builds an eval set of 5 to 20 cases from real examples. Each has must-contain and must-not-contain content, and at least one case should fail or refuse. It is stored in the project as JSON or markdown, with a grading method and a pass bar written before the first run.

It belongs to the Hypothesise stage and is reused in later stages. It serves rule 2, Agree acceptance first, and rule 3, Read back the real result.

## The problem it solves

Northgate Cycles uses an AI tool to draft replies to customer emails. It reads well on the three emails the owner tried. A month later the tool tells a customer a refund is "already on its way" when no refund has been issued. Nobody had written down what a good reply must not say.

## What the agent does differently

It takes twelve real, anonymised emails from the support inbox, writes what each reply must contain (the return address, the 30-day window) and must not contain (any promise of a refund), adds a case with missing order details where the right reply is a question, and adds one case that the current prompt is known to get wrong. See [examples/eval-set/output.md](../../examples/eval-set/output.md).

## When to use it, and when not to

Use it before relying on AI-written text, summaries or classifications, and each time the prompt or model changes. Skip it for deterministic output that ordinary tests cover.

## Who it is for

- **Team lead or owner:** a standing check on an AI tool in daily use.
- **Developer or prompt writer:** a way to see whether a prompt change helped.
- **Anyone approving an AI rollout:** evidence of what was tested.

## How to use it

> Build an eval set for our AI email replies from the anonymised emails in `data/support-sample/`. Include a case that should fail, and tell me how to grade it.

Read the cases, correct the expectations and agree the pass bar before the first run.

## How it connects

- **Before:** [agree-acceptance](../agree-acceptance/README.md) fixes the wider card; this skill is the example set within it.
- **After:** [pilot-before-scale](../pilot-before-scale/README.md) uses the set on a handful of live items, and [report-with-evidence](../report-with-evidence/README.md) reports the run.
- **Rules:** see [docs/controls.md](../../docs/controls.md).

**Needs:** Nothing beyond the agent. If real examples live in a mailbox or helpdesk, the agent needs read access to an export of them.

## Tips

- Real inputs beat invented ones. Start with a small real set rather than a large made-up one.
- Write the must-not list first. It is usually shorter and more important.
- Each time the tool fails in real use, add that case.

## Limits

- Text matching is crude. A good answer can miss a phrase, and a bad one can include it. A person must read the failures and a sample of passes.
- Twelve cases cannot prove quality. They catch regressions and known failures.
- Removing private details can change how an input reads. Check one case by hand.

Files: [SKILL.md](SKILL.md), [template.md](template.md), [example input](../../examples/eval-set/input.md) and [output](../../examples/eval-set/output.md).
