# Continuous delivery and DevOps

## What it is

Continuous delivery means keeping software in a state where it could be released at any time, and making release a routine, low-drama act. DevOps is the wider habit of the people who build a system also running it, so the feedback from live use reaches the people who can fix things. Jez Humble and David Farley set out continuous delivery in *Continuous Delivery*. The DORA research (see [dora-metrics.md](dora-metrics.md)) found that teams who do it well ship more often and recover faster, and they are not less stable for it.

## Why it matters with agents in the loop

Agents increase the number of changes. If releasing a change is slow, manual or frightening, the changes pile up and the risk of each release grows. A fast, automated and reversible path to production is what makes a high rate of change safe. Without it, agent speed becomes a queue of unreleased work.

It also sets the boundary clearly. An agent may prepare a release. A person decides whether it goes to users. Deploying is on the list of things [rule 1](../rules/04-stop-boundaries.md) stops without a yes.

## The practices

### The deployment pipeline

A pipeline is the automatic path a change takes from commit to production: build, run tests, run security checks, deploy to a test environment, run checks again, then release. Each step either passes or stops the line. Build once, then promote the same build through the environments, so what you tested is what you ship.

Good pipelines are fast, give clear failure messages and are the only way to production. If people can bypass it, they will, and then it protects nothing.

*With agents:* include evals as a pipeline step for any feature whose output varies, and block the release when the pass rate falls below the agreed bar (see [evals-for-ai-output.md](evals-for-ai-output.md)). Do not let an agent edit the pipeline definition without the same review as other code.

### Feature flags

A feature flag is a switch in the code that turns a feature on or off without a new deployment. Flags let you merge unfinished work safely, release to a small group first and switch something off in seconds when it misbehaves. Pete Hodgson's writing on feature toggles is the best known guide.

Flags need housekeeping. Each flag should have an owner and a removal date. Old flags are clutter, and a few have caused serious incidents when they were left in unknown states.

### Deploy is not release

**Deploying** puts the new code on the servers. **Releasing** makes the feature available to users. Keeping them separate lowers the risk of both. You can deploy at any hour because nothing changes for users until you turn the flag on. You can release gradually: first the team, then a small percentage, then everyone, watching the health measures at each step.

### Rollback and roll forward

Know before you release how you will undo it. For a flagged feature, undo means switching the flag off. For a code change, undo means redeploying the previous build, which only works if that build is still available and the data changes were compatible. Data changes are the hard part: make them in steps that work with both old and new code, so that either can run.

Practise it. A rollback you have never tried is a hope, not a plan. Rolling forward with a quick fix is sometimes faster; decide the rule in advance, not during an incident.

### You build it, you run it

This phrase is Werner Vogels' description of Amazon's approach. The team that builds a service is also on the hook for it in live use. Operating your own work changes what you build: you add logging, alerts and graceful failure because you are the one woken by their absence.

For small teams it does not mean a night rota for everyone. It means the team owns the health of what it ships, has the access to look at it and has a named way for users to reach it.

*With agents:* if an agent is part of the running system, a named person owns it. An agent that sends, spends or changes things in production without a named human owner is a boundary breach waiting to happen.

### Blameless incident review

When something goes wrong, run a short review soon after, focused on how the system allowed the failure rather than on who made the mistake. The idea comes from safety-critical industries and was popularised in software by John Allspaw and the Google SRE books. People who fear blame hide what happened; people who do not fear it tell you.

A useful review writes down:

1. What happened, in time order, with evidence.
2. How it was noticed and how long that took.
3. What made it possible: the missing test, the unclear permission, the confusing screen.
4. What helped.
5. A small number of changes, each with a named owner and a date.

It does not end with "be more careful". That is not a change.

*With agents:* include the agent's inputs, outputs and permissions in the timeline. Ask what the instruction file said, what the agent could reach and what check would have caught it. The fix is usually a smaller permission, a clearer boundary or a new eval case.

## What good looks like

- Every change goes through the same automated pipeline.
- Deployment is boring and happens often, including to production.
- Features are released by flag, in stages, with a watched health signal.
- Rollback is rehearsed and takes minutes.
- The team that builds a service watches it and answers for it.
- After an incident there is a written review and its actions get done.

## Anti-patterns

- **Release trains with big batches** that make each release a gamble.
- **Manual deployment steps** that exist only in someone's head.
- **Deploy equals release,** so every deployment is a user-facing event.
- **Flags that never get removed.**
- **A rollback plan that has never been run.**
- **Throwing it over the wall** to a separate operations team who did not see it built.
- **Blame in the review,** or a review with no follow-up.
- **An agent with deploy rights** and no named human owner.

## How it maps to the steps and rules

- **Build:** pipelines, flags and small releases are how a small real piece reaches real use.
- **Check:** the DORA measures describe how well this path works.
- **Hand over:** the receiving team must run a release and a rollback without the builders.
- **Improve:** shared pipelines and templates are reused by the next team.
- **Rule 1:** production deploys and publishing wait for the owner's yes.
- **Rule 3:** read back the live result, not only the pipeline's green tick.
- **Rule 4:** say "deployed" only with a record of the deployment, and "released" only when users can see it.

## A short example

Harbourside Lettings runs a small web app where tenants report repairs. The team adds a "photo upload" feature. It merges daily behind a flag called `photo_upload`, owned by the product owner, with a removal date in the flag list. On Tuesday the pipeline deploys the build to production with the flag off. On Wednesday the owner turns it on for staff, then for ten per cent of tenants, watching the error rate and upload size. Uploads of large phone photos slow the page, so the owner switches the flag off in under a minute. The team writes a short blameless review: no test covered large files and the staging data had only small ones. The follow-up adds a large-file case to the examples and a size limit to the code. The flag goes back on the next day.

## Further reading

- Jez Humble and David Farley, *Continuous Delivery*.
- Nicole Forsgren, Jez Humble and Gene Kim, *Accelerate*.
- Gene Kim, Kevin Behr and George Spafford, *The Phoenix Project*.
- Gene Kim and others, *The DevOps Handbook*.
- Betsy Beyer and others, *Site Reliability Engineering* (Google).
- Pete Hodgson, "Feature Toggles" (article on martinfowler.com).
- Sidney Dekker, *The Field Guide to Understanding 'Human Error'*.
