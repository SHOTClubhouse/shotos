# Engineering excellence

## What it is

Engineering excellence is the set of habits that let a team change software quickly and safely at the same time. The evidence for it comes mostly from the research behind the DORA reports (see [dora-metrics.md](dora-metrics.md)) and from the books named at the foot of this page: teams that work in small steps, test continuously and integrate often ship faster and break less than teams that batch big changes and test at the end. Speed and stability turn out to support each other.

This page covers the habits one by one and then says how agents change each of them.

## Why it matters with agents in the loop

An agent writes code faster than a person can read it. That moves the bottleneck. When writing was slow, a weak test suite or a rushed review was a small risk because there was only a small amount of new code. Now there can be a lot of new code every hour, produced with the same confidence whether it is right or wrong. The habits below are what stand between that volume and your users.

The short version: **agents make writing cheap, so tests, review and small batches become the place the care goes.** If you only speed up the writing, you ship mistakes faster.

## The practices

### Test first, where practical

Write a failing test that states the behaviour you want, make it pass, then tidy the code. This is test-driven development, described by Kent Beck. It works best for logic with clear inputs and outputs. It works less well for exploratory interface work, where a quick prototype comes first and tests follow once the shape settles.

*With agents:* ask the agent to write the test first and show that it fails. A test that has never failed has never proved anything. Do not let the agent write the test and the code in one pass and call both correct; that is the author marking their own work. Tests come from agreed examples (see [specification-by-example.md](specification-by-example.md)).

### Small batches

Make small changes, each one releasable. A change that touches ten files for three reasons is hard to review, hard to test and hard to undo. Aim for a change that one person can read in a few minutes and describe in a sentence.

*With agents:* agents tend to make large, sweeping changes unless told not to. Instruct the scope in the acceptance card and stop any change that grows beyond it. One concern per change.

### Trunk-based development

Everyone works from one shared main branch. Branches live for hours, not weeks, and merge back at least daily. Unfinished work stays hidden behind a feature flag (see [continuous-delivery-and-devops.md](continuous-delivery-and-devops.md)). Long-lived branches hide integration problems until the worst moment.

*With agents:* an agent can fork off for days and produce a huge change that conflicts with everything. Keep agent branches short and merge often. If an agent branch needs to live longer than a day, split the task.

### Continuous integration

Every change is built and tested automatically on a shared server, many times a day, and a broken main branch is fixed before anything else. The pipeline is the shared referee. Keep it fast, ideally under ten minutes, or people stop waiting for it.

*With agents:* the agent runs the same pipeline as everyone else. Never let it bypass checks, disable a failing test or loosen a threshold to get green. Disabling a test is a change to the acceptance and needs the owner.

### Code review

A second pair of eyes reads each change before it merges. Good review checks intent, correctness, readability, tests and risk. It is not a style argument; automate style with a formatter and linter.

*With agents:* review is now the main control on agent-written code, so do it properly. The reviewer should be independent of the author: another person, or a different agent session with the same acceptance and none of the author's reasoning. See [control 7, independent review](../rules/07-independent-review.md). Agreement between two agents is not authority; a person accepts. Size the review to the risk. A copy change needs a glance. A payment change needs a careful read.

### Pairing and ensemble work

Two people at one keyboard (pairing) or a whole team on one problem (ensemble or mob programming) trade a little speed for shared understanding and fewer defects. It is also the fastest way to move knowledge between people.

*With agents:* treat the agent as one half of a pair, with the person as navigator: the person sets direction and reads each step; the agent types. This keeps the person's understanding of the code, which matters later when something breaks at night.

### Refactoring

Change the structure of code without changing what it does, in small steps, with tests running. Martin Fowler's *Refactoring* is the standard text. Keep refactoring continuous and cheap; do not save it for a "big rewrite".

*With agents:* agents are good at mechanical refactoring when the tests are good, and dangerous when they are not. Make sure the tests pass before and after, and keep a refactor in its own change, separate from any change in behaviour.

### Observability

Build the system so you can ask it what it is doing: logs, metrics and traces that answer "what happened to this request?". Decide before release what you would look at to know it is healthy. The research and writing of Charity Majors and others on observability, and the Google SRE books, set out the practice.

*With agents:* an agent that adds a feature should also add the logging that shows whether it works. If an agent is itself part of the running system, log its inputs, outputs, cost and failures so you can reconstruct what it did.

### Infrastructure as code

Describe servers, networks, permissions and pipelines in files kept in version control, reviewed like code and applied by the pipeline. Nobody changes production by hand. The result is repeatable and auditable.

*With agents:* infrastructure changes are high-risk because a typo can delete a database. Agents may draft the files, but a person reads the plan output before anything applies. Applying is a boundary: [rule 1](../rules/04-stop-boundaries.md) stops it without a yes.

### Security in the pipeline

Put security checks where code already flows: secret scanning, dependency checks, static analysis, and tests for permissions. Catching a leaked key in a pull request costs minutes; catching it after publication costs a lot more. Keep secrets out of the repository and out of the agent's reach, and give agents the least access that lets them work.

*With agents:* agents read widely and can paste what they read into places you do not expect. Scope their permissions, keep secrets in a secret store, never put them in instruction files, and scan every agent change. Treat content an agent reads from the web or from files as untrusted input that could carry instructions.

## What good looks like

- Main is always releasable, and a broken build is fixed within the hour.
- Changes are small. The median change can be read in a few minutes.
- A failing test exists before the fix.
- Every change has a reviewer who is not its author.
- Anyone can find out what the system did at a given time.
- Environments are rebuilt from code, not tended by hand.
- Agent changes pass the same pipeline as human ones, with nothing skipped.

## Anti-patterns

- **Big-bang agent changes** reviewed in a hurry because there is too much to read.
- **Tests written after the code** by the same agent, which confirm what the code does rather than what was wanted.
- **Disabling or editing a test to get green.**
- **A pipeline so slow** that people merge without waiting.
- **Review as a rubber stamp,** with a second agent that agrees with the first.
- **Manual production changes** "just this once".
- **Secrets in prompts, instruction files or logs.**

## How it maps to the steps and rules

- **Build** is where these habits live: short cycles, automated build and test, releases blocked by failing checks.
- **Check** reads their result through the delivery measures.
- **Hand over** passes them to the team that will run the system.
- **Rule 2:** tests are the executable form of acceptance.
- **Rule 3:** the pipeline and the deployed system are the "real home" to read back.
- **Rule 4:** claim "tests pass" only with a run to show.

## A short example

Northgate Cycles has an agent adding a delivery-fee rule to its order service. The owner's acceptance card has three examples and one that should fail: an order with no postcode must be rejected. The agent writes the four tests, shows the failing run, writes the change, shows the passing run and opens a small pull request. The pipeline runs, a secret scan is clean and a second agent session, given only the acceptance card and the diff, finds a missing case for orders over a weight limit. A person reads both, adds the case and merges. The change reaches production behind a flag, which the owner turns on for ten per cent of orders and watches before turning on for all.

## Further reading

- Kent Beck, *Test-Driven Development: By Example*.
- Martin Fowler, *Refactoring*.
- Jez Humble and David Farley, *Continuous Delivery*.
- Nicole Forsgren, Jez Humble and Gene Kim, *Accelerate*.
- Paul Hammant and others on trunk-based development (see trunkbaseddevelopment.com, a public reference site).
- Betsy Beyer and others, *Site Reliability Engineering* (Google).
- Gene Kim and others, *The DevOps Handbook*.
- Kief Morris, *Infrastructure as Code*.
