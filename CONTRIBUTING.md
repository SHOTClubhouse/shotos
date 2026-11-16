# Contributing

Thank you for helping. Three kinds of contribution are especially useful:

1. **A failure.** A case where an agent followed a skill and gave the wrong result, or where claim-check returned the wrong verdict. Use the [failure report](.github/ISSUE_TEMPLATE/failure-report.md) with a fictional reproduction.
2. **An eval case.** A normal task or a contrary case that checks a tempting shortcut. Use the case file for the owning skill under [core](evals/core/) or [packs](evals/packs/). The [original cases](evals/cases.json) are also part of the runner.
3. **A skill or pack.** Open an issue first, describing the job, who it is for and how you will show it works.

## Rules for every change

- Follow the [four controls](docs/controls.md) yourself. Say what you changed and how to check it.
- Every skill has a `SKILL.md`, a `README.md`, a worked input and output in the relevant `examples/` directory and at least one normal and one contrary case.
- Examples are invented. Never include real people, customers, private data or credentials.
- Plain British English. No em dashes.

## Take a failure from report to fix

1. Write down the request, the evidence the agent had, the expected decision and the observed result. For example, a fictional receiver asked for access before accepting a handoff, and the agent advanced the status anyway.
2. Reproduce the behaviour with invented inputs. Use stable case IDs and keep any private transcript or source record in its original system. See [Security](SECURITY.md) for private vulnerability reports.
3. Fix the owning skill, template or tool. Update the worked example if it shows the older behaviour. In a case, check the decision and its evidence. Treat phrase counts as a first pass when wording can vary. [Eval instructions](evals/README.md)
4. Install the test dependency with `python -m pip install PyYAML==6.0.3`, then run the local gate before opening the pull request (see below). When changing bundled resources, open the installed copy or its ZIP and check the links. Describe what someone else can reproduce.

## Run the local gate

SHOTos has no GitHub Actions. Every change goes through the local gate on your own machine instead:

```
python tools/local_gate.py
```

It runs the unit tests, the demo, the JavaScript tests when Node.js is installed, a scan for private terms, the skill ZIP link check and the structure checks for each skill you changed. It writes a go/no-go card to `.work/gate/` and prints it. Paste the verdict and check lines into your pull request under "How to check it".

To run the quick checks before every push, install the hook once: `python tools/install_hooks.py`. The hook runs `python tools/local_gate.py --fast` and stops the push on a NO-GO.

The scan for private terms reads a denylist that maintainers keep outside the repository. Without it the gate warns and skips that check; a maintainer runs it before merging.

## Sign-off

By contributing, you confirm the [Developer Certificate of Origin](https://developercertificate.org/): you wrote the contribution, or have the right to submit it under this repository's licences. Add `Signed-off-by: Your Name <you@example.com>` to each commit (`git commit -s`).
