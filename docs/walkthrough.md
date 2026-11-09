# Walkthrough: can better updates cut repeat repair emails?

Harbourside Lettings, a fictional property management firm, wants fewer tenants chasing repair updates. Follow the [six stages](framework.md) to count the problem, try a small change and decide whether another office could use it. The supplied files let you prepare and check drafts. The later results and decisions are examples for practice.

## Try it in a chat

Open a fresh chat in your AI assistant. Attach the relevant [walkthrough files](../examples/walkthrough/data/) as each step calls for them. Save your counts, checks and decisions in one [shared record](../templates/programme.md). Use the linked sample outputs to check your work after each step. To install a skill first, follow the [setup guide](guides/chat-assistants.md).

## 1. Scope

> Read the attached meeting notes and explain the problem the team needs to solve.

The managing director asked for a chatbot. First, find out why people are writing in. Start by counting the enquiries. Compare with the [sample problem statement](../examples/walkthrough/reference/1-problem.md).

> Use the attached enquiries file to count emails by category. Count an email as a repeat if the tenant has already written about the same category.

The answer is in the data: half of the 20 emails are repeats, and the 12 repair emails cover only 5 repair issues. Tenants are chasing status, not reporting new problems. A chatbot that cannot see repair status would not fix that. Compare with [2-findings.md](../examples/walkthrough/reference/2-findings.md). The numbers in the reference are checked against the data by the test suite.

Record the period, the count of repair emails and repeat repair emails, and the operations lead as the proposed workflow owner. The baseline for this experiment is **7 repeat repair emails out of 12 repair emails**. The broader inbox count of 10 repeats out of 20 emails is a separate measure. Use the [baseline worksheet](../skills/baseline/template.md).

## 2. Hypothesise

> Test the idea that a weekly status update for open repairs reduces repeat repair emails. Agree the pilot and the acceptance checks before drafting.

In the [hypothesis card](../skills/hypothesis-card/template.md), use 7 of 12 as the starting rate. For this exercise, propose a target of 40% or fewer repeat repair emails over a comparable window, with zero unauthorised sends and zero disclosures to the wrong tenant. Record the raw counts as well as the rate so small changes in volume are visible. Keep the target marked as proposed until the operations lead agrees it.

Use the [reference acceptance card](../examples/walkthrough/reference/3-acceptance.md) for the draft checks. Each repair gets one draft. A missing next date must produce an exception for a person. A person checks and sends any live update.

## 3. Operate

> Use the attached open repairs list to draft the agreed updates. Hold back any draft that needs a date someone still has to confirm.

The [sample report](../examples/walkthrough/reference/4-report.md) records five drafts. One is held back because the lock repair has no next date. Check the drafts against the repair list and record who will find the missing date. For a live trial, use the [pilot log](../skills/pilot-before-scale/template.md) to start with up to three different cases, including one with a missing date. The operations lead reviews the drafts and decides whether to run the trial.

## 4. Track

![Seven of twelve repair emails were repeats. Five drafts were prepared and one was held back. The team needs to measure what happens after approved updates go out.](images/harbourside-track-decision.svg)

> Tell the operations lead what changed against the starting count. Recommend handing the work over, trying a different idea, waiting for more information or stopping.

Record the draft checks. To find out whether the updates work, count the repair emails again over a similar period after approved updates go out.

**Example result.** Suppose the first week produced **4 repeat repair emails out of 12**. The logs show that every send was approved and went to the right tenant. The share of repeat emails falls from about 58% to 33%. Record how many emails you counted and whether the mix of repairs changed. The operations lead could ask the receiving team to run the next week on its own. If repeat emails stay above the target, try a different idea. If an update goes to the wrong tenant or goes out without approval, stop and find out why. [Results worksheet](../skills/evidence-pack/template.md) · [Decision record](../skills/decision-record/template.md)

## 5. Own

> Hand the workflow over to the operations lead and agree what the receiving team must do in an independent weekly cycle.

Start with the [reference handoff](../examples/walkthrough/reference/5-handoff.md). It records draft work awaiting acceptance. Add the Track decision once it exists. Use the [runbook](../skills/runbook/template.md) and [enablement plan](../skills/enablement-plan/template.md) to agree who gets the repair list, who checks and sends the drafts, who resolves missing dates and who records the chaser counts.

**Example handover.** The receiving team runs the weekly process with its own access. It holds back a draft with a missing date, asks the repair coordinator to check and records what happened. The operations lead reviews the log and takes ownership once the team has done a full week on its own. If the team needs help from the person who set it up, improve the instructions or training and try another week.

## 6. Sustain and Scale

> Plan how the next office would try this. Name its lead, what it will measure first and who decides when it can start.

**Example rollout.** The sponsor approves one office to prepare a trial. Share the instructions, review checklist and way of counting repeat emails. The local lead checks access and repair data, counts its own repeat emails and agrees a trial before sending any updates. Pause if an update goes out without approval, information goes to the wrong person or the local team needs help to run a full week. Keep reviewing the first office's process and record what the next office should do differently. [Rollout plan](../skills/rollout-plan/template.md) · [Learning log](../skills/learning-loop/template.md)
