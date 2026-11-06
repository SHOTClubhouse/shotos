# Contributing

Thank you for helping. Three kinds of contribution are especially useful:

1. **A failure.** A case where an agent followed a SHOTos skill and still got it wrong, or where claim-check passed something false or failed something true. Open an issue with the report, the Claims block and what actually happened.
2. **An eval case.** A normal or contrary case for an existing skill, in `evals/cases.json`.
3. **A skill or pack.** Open an issue first, describing the job, who it is for and how you will show it works.

## Rules for every change

- Follow the [four controls](docs/controls.md) yourself. Say what you changed and how to check it.
- Every skill has a `SKILL.md`, a `README.md`, a worked example in `examples/` and at least one normal and one contrary case.
- Examples are invented. Never include real people, customers, private data or credentials.
- Plain British English. No em dashes.
- Run `python -m unittest discover -s tests` before opening a pull request.

## Sign-off

By contributing, you confirm the [Developer Certificate of Origin](https://developercertificate.org/): you wrote the contribution, or have the right to submit it under this repository's licences. Add `Signed-off-by: Your Name <you@example.com>` to each commit (`git commit -s`).
