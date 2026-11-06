# Walkthrough: from "we need a chatbot" to a fix that works

This tutorial runs all four skills and claim-check on one made-up company. It takes about 20 minutes with an agent, or longer on paper. Harbourside Lettings is fictional: a lettings and property management firm with 120 staff. Any resemblance to a real company is a coincidence.

Everything you need is in [examples/walkthrough](../examples/walkthrough/): meeting notes, three weeks of enquiry data, the open repairs list and a reference output for each step. Your agent's answers will differ in wording. Compare them on substance.

## Set up

```
cp -r examples/walkthrough ~/harbourside && cd ~/harbourside
git init
python /path/to/shotos/install.py --runtime claude --scope project --with-hook
```

## 1. Brief: capture the problem

> Read data/notes.md and capture the problem before we decide anything.

The managing director asked for a chatbot. The skill turns that into a problem statement with no solution in it, marks what is not measured, and proposes the cheapest test: count the enquiries. Compare with [1-problem.md](../examples/walkthrough/reference/1-problem.md).

## 2. Brief: run the cheapest test

> Count data/enquiries.csv by category, and count repeat contacts: an email from a tenant who already wrote about the same category.

The answer is in the data: half of the 20 emails are repeats, and the 12 repair emails cover only 5 repair issues. Tenants are chasing status, not reporting new problems. A chatbot that cannot see repair status would not fix that. Compare with [2-findings.md](../examples/walkthrough/reference/2-findings.md). The numbers in the reference are checked against the data by the test suite.

## 3. Brief: agree acceptance

> The fix is a weekly status update for tenants with an open repair. Agree acceptance with me before drafting anything.

Note the boundary the data protection lead set: nothing goes to tenants without a person checking it. Compare with [3-acceptance.md](../examples/walkthrough/reference/3-acceptance.md).

## 4. Build: do the work and report with evidence

> Draft the updates as agreed.

The agent writes drafts to `.work/updates/` and ends with a Claims block. With the hook installed, claim-check tests the claims before the agent can finish. Try telling it to say the updates were sent, and watch the hook stop it. Compare with [4-report.md](../examples/walkthrough/reference/4-report.md).

## 5. Hand over: hand it over

> Hand this to the operations lead.

The handoff says the work is executed but not accepted, lists the two decisions that belong to people, and gives a resume prompt. Compare with [5-handoff.md](../examples/walkthrough/reference/5-handoff.md).

## What changed

The walkthrough covers Brief, Build and Hand over. In real life, Check would come next: count the chasers again after a month against the baseline of 10 repeats in 20 emails, then decide whether to keep the weekly updates, change them or stop. Improve would take the same approach to the next office.


The company nearly bought a chatbot for a problem it had not measured. One hour with the data showed that the real problem was tenants not being told about repairs. The fix costs nothing, the agent never contacted a tenant, and every claim it made was checked.
