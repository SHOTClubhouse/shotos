# Who SHOTos is for: seven personas

SHOTos has the same five-step work loop and the same four rules for everyone. The steps (Brief, Build, Check, Hand over and Improve) are in [the work loop guide](framework.md); the four rules are in [controls](controls.md) and run inside every step. What differs is which step you start in, which rule matters most first, which skill you open first and where the rules are enforced. This page describes seven readers, including the agent itself, and gives each a first week and a picture of a good month.

Starting points on the maturity maps are typical patterns, not measurements. See [maturity levels](levels.md) for the two frameworks used here.

## Which persona am I?

Pick the line that sounds most like your Monday.

- "I am the only reviewer of everything my agents do." You are a **solo founder**.
- "Everyone on the team uses agents their own way." You are a **small team lead**.
- "I write what the team should build, and I cannot tell if it came out right." You are a **product owner** (or an analyst or business analyst).
- "I am responsible for how good the work is across several teams." You are an **engineering or practice lead**.
- "I am accountable if an agent does something it should not, and I cannot see what it did." You are a **business unit leader or enterprise sponsor**, including risk, compliance and governance.
- "I help other people adopt this." You are an **enablement coach or consultant**.
- "I am the agent reading the instructions." Read the last section.

Many people are two of these. A founder who also writes the briefs is a solo founder and a product owner. Start with the persona whose pain is sharpest this week.

## Comparison

| Persona | Main worry | Step to start with (and rule) | First skill | Where the rules run |
|---|---|---|---|---|
| Solo founder | Checking everything, or trusting blindly | Brief, then Build (rules 3 and 4) | report-with-evidence | Your machine: `AGENTS.md` and the Stop hook |
| Small team lead | Five people, five ways of working | Brief (rule 2) | agree-acceptance | One `AGENTS.md` in every repository |
| Product owner | Work that is done but wrong | Brief (rule 2) | capture-the-problem | The acceptance card, before the work |
| Engineering or practice lead | Quality that varies by person and team | Build and Check (rule 4) | evidence-handoff | claim-check in review and CI |
| Business unit leader or sponsor | No owner, no proof, no audit trail | Brief, Check and Improve (rule 1) | None directly, read the records | Policy, with records kept beside the work |
| Enablement coach | Leaving a team dependent on you | Hand over and Improve (all four rules, one at a time) | The one the client's pain points to | The client's own repositories and habits |
| The agent itself | Being asked to guess what "done" means | Works inside Build (all four rules) | Whichever skill the task matches | Its own report, tested by claim-check |

---

## 1. Solo founder

**Who you are.** You run the business and use agents for drafting, code, research and admin. You are the owner, the reviewer and the customer. Nobody else will catch a mistake before it ships.

**Where you start in the loop.** Brief on anything a customer will see, then Build with rules 3 and 4 doing the checking.

**Jobs you are trying to get done**
- Move faster than your size should allow.
- Leave an agent working and do something else.
- Keep client, supplier and customer messages from going out wrong.

**What goes wrong today**
- You ask an agent to tidy the pricing page and to email the update to your customers. It reports "all done". The page changed, the email never went, and you find out when a customer asks.
- You read every diff because you do not trust the summary. The agent saves you typing, not attention.
- An agent deletes an old folder to make space. It was the only copy of last year's invoices.
- You return after an hour away to a long, confident report. You cannot tell which parts were checked and which were hoped for.

**What SHOTos gives you**
- **Rules 3 and 4 first.** The agent opens the file and runs the test before it reports, then ends with a [Claims block](claims.md) that `claim-check` tests. You read the verdict instead of the diff.
- **Rule 1 as a safety net.** The working agreement stops the agent sending, spending or deleting without you.
- **agree-acceptance** for anything a customer will see, in five minutes.
- **The Stop hook** (`install.py --with-hook`), so a false "done" is sent back before you see it.

**First week**
1. Day 1: install with the hook. Run `python examples/demo/run_demo.py` to see a failing report.
2. Day 2: follow the [walkthrough](walkthrough.md) once, start to finish. It takes about 20 minutes.
3. Day 3: on a real task, use the report-with-evidence habit and read only the claim-check verdict first.
4. Day 4: agree acceptance on one task a customer will see. Include one case that should fail.
5. Day 5: list which commands claim-check may run in `~/.shotos/claim-check.json`. Look back at what it caught.

**A good month looks like**
- You leave agents on bounded tasks and read the report when you return, not each change.
- Nothing external has gone out without a receipt you can open.
- When a report says "unverified", you know exactly what to look at first.
- You keep acceptance cards for jobs that repeat, and the second run starts faster.

**Maturity.** Typically near the middle of Yegge's levels, with the agent in the editor and most changes reviewed, and at organisational level 0 or 1 (personal use). The next step is agents working while you are away, which needs a report you trust. That is rule 4.

**Objections**
- *"This slows me down."* The first card costs five minutes. Skipping it costs a rework or a customer message you cannot recall. In the [outcome evals](evidence.md), runs with SHOTos cost about 42% more and took longer, because the agent reads the rules and skills and writes more. That is real overhead. Use it where a mistake would cost more than the overhead.
- *"My model is already careful."* The same run found the same on safety: all ten safety cases passed without SHOTos. What differed was structure, such as an owner, a failure case and a list of unknowns. Careful is good. Checked is better, and your model changes every few months.
- *"I only have myself to answer to."* Then you are the one who pays for a wrong "done", with no colleague to catch it.

---

## 2. Small team lead

**Who you are.** You lead a team of roughly three to fifteen people. Each person uses agents, and each has found their own habits.

**Where you start in the loop.** Brief: agree one way of stating the problem and the acceptance, then Build on a small slice with the whole team.

**Jobs you are trying to get done**
- Get consistent results from a team with mixed experience.
- Review agent work without becoming the bottleneck.
- Onboard a new starter without a week of tribal knowledge.

**What goes wrong today**
- One person's agent commits straight to the shared branch, and another's asks before every file. Nobody agreed either.
- A reviewer opens a pull request and finds the description says "tests pass" when no test was added.
- Two people brief agents on the same task with different ideas of done, and the results do not fit together.
- A colleague goes on leave and the agent's half-finished work cannot be picked up, because the context was in a chat.

**What SHOTos gives you**
- **One `AGENTS.md`** ([template](../templates/AGENTS.md)) in every repository, so every agent starts from the same four rules.
- **Rule 2 as the team habit.** An [acceptance card](../templates/acceptance.md) goes in the pull request or ticket before work starts.
- **claim-check in review.** Reviewers run it on the agent's report and start from SUPPORTED and UNSUPPORTED instead of from a diff.
- **evidence-handoff** when work changes hands, so the next person or agent has a state, evidence and a resume prompt.

**First week**
1. Day 1: install in one repository and read the [working agreement](../templates/AGENTS.md) together for ten minutes. Change nothing yet.
2. Day 2: agree which commands claim-check may run in that repository, and who decides.
3. Day 3: each person does one real task with an acceptance card. Pair on the first.
4. Day 4: in review, ask for the Claims block and run claim-check on it.
5. Day 5: a 30-minute retro. Which unsupported claims did claim-check catch? Which rule was awkward? Adjust `AGENTS.md`, then roll out to a second repository.

**A good month looks like**
- Pull requests carry an acceptance card and a Claims block as normal.
- Review comments are about the work, not about whether the description is true.
- A new starter's agent behaves like everyone else's on day one.
- Handoffs have a state (prepared, executed or accepted) and nobody asks "where were you up to?".

**Maturity.** People sit at different Yegge levels, and the organisation is typically at level 1 (pilots and individual use that are not coordinated). The next step is one shared way of working, which is the whole point of the shared `AGENTS.md`.

**Objections**
- *"We already have a process."* Keep it. SHOTos is four rules and a check, not a method that replaces yours. If your pull request template already asks for acceptance, point the card at it.
- *"People will see this as policing."* The Claims block is the agent's duty, not the person's. It protects people from a plausible report that was wrong.
- *"Reviews will take longer."* They start from evidence instead of reconstruction. Whether that is faster for your team is something to measure on your own pull requests, not assume.

---

## 3. Product owner (also analysts and business analysts)

**Who you are.** You decide what gets built, or you turn a stakeholder's request into something a team can act on. You may never run an agent yourself, but your team's agents work from what you write.

**Where you start in the loop.** Brief. Your work is the problem statement, the testable bets and the acceptance that the team's agents work from.

**Jobs you are trying to get done**
- Find the real problem behind a request.
- Say what done looks like so the team can build the right thing.
- Know whether what came back is what you asked for.

**What goes wrong today**
- A director asks for a chatbot. The agent builds one. Nobody counted what tenants were actually writing in about, so the chatbot answers questions nobody had. The [walkthrough](walkthrough.md) shows this case with Harbourside Lettings.
- You write a user story in one line. The agent fills the gaps with sensible guesses, and you find them at review.
- "Done" is decided after the work, by whoever looks first.
- A requirements summary reads well and quietly drops the one constraint the compliance team cared about.

**What SHOTos gives you**
- **capture-the-problem** turns a request into a problem statement with no solution in it, the unknowns and the cheapest first test. Use the [problem template](../templates/problem.md).
- **agree-acceptance** (rule 2) turns the outcome into checks anyone could verify, one case that should fail and a named person who accepts. Use the [acceptance card](../templates/acceptance.md).
- **For AI-written output**, an example set kept in the project: inputs, what a good answer must contain and what it must not contain.
- **You hold the accept step.** An agent cannot mark work accepted. A claim of acceptance needs your record.

**First week**
1. Day 1: take a request you already have. Run capture-the-problem on it and read the unknowns.
2. Day 2: do the cheapest first test. Count something. Ask three people.
3. Day 3: write the acceptance card for the smallest useful change. Add one case that should fail.
4. Day 4: hand the card to the team or the agent before any work starts.
5. Day 5: when work comes back, check it against the card, not against your impression.

**A good month looks like**
- Requests arrive as problem statements, and some are dropped after the first test, which is a good outcome.
- The team asks fewer clarifying questions because the card already answers them.
- Rework shrinks because the misunderstanding surfaced on the card, not in the build.
- You can say for each item whether it is prepared, executed or accepted.

**Maturity.** Typically not running coding agents, so the Yegge levels apply to your team, not you. Your lever is the quality of the specification. The next step is writing acceptance that lets the team's agents run on their own safely.

**Objections**
- *"I am not technical."* Nothing here needs code. The templates work on paper.
- *"Writing it down is the slow part."* It is the part that was already happening, in your head and in review comments. The card moves it to before the work.
- *"Stakeholders will not wait for a problem statement."* One page, five minutes, and a first test that can end the discussion cheaply. A request that cannot survive that test would have been expensive later.

---

## 4. Engineering or practice lead

**Who you are.** You are responsible for quality and consistency across several teams or projects: engineering lead, head of delivery, head of data, or the person who owns a practice such as design or analytics.

**Where you start in the loop.** Build and Check: evidence-based review, then measuring before and after against the baseline.

**Jobs you are trying to get done**
- Keep standards steady as agents increase output.
- Show that the work meets the bar without reading all of it.
- Share what works between teams.

**What goes wrong today**
- Output rises and review capacity does not. Reviewers skim, because every change looks plausible.
- A summary says "all tests pass". The command was never run, or ran on a different branch.
- An agent is told to "clean up" and rewrites a colleague's module that was not in scope.
- Each team writes its own agent instructions, and the good ideas do not travel.

**What SHOTos gives you**
- **Rule 4 as a review standard.** Every report ends with a Claims block, and [claim-check](claims.md) tests files, git state, allowed commands and receipts.
- **Allow lists you control.** claim-check runs a command only if it is on a list from your own config. A cloned repository cannot make it run commands.
- **claim-check in CI**, so evidence is checked the same way for every team.
- **Evals.** The [evals folder](../evals/README.md) shows how to write normal and contrary cases for a skill. Use the same pattern for your own instructions.
- **Rule 2 for risky work.** Anything touching customers, money, safety or children gets independent review, as the [manifesto](../MANIFESTO.md) says. SHOTos does not provide that review itself.

**First week**
1. Day 1: read [claims.md](claims.md) and the limits section. Know what claim-check cannot tell you.
2. Day 2: pick two teams. Install the shared `AGENTS.md` and agree the allow list.
3. Day 3: add claim-check to one repository's CI as a report, not a block.
4. Day 4: read ten recent agent pull requests. Note which claims would have been unsupported.
5. Day 5: decide where the check blocks and where it only informs. Write that down.

**A good month looks like**
- Reviewers spend their time on judgement, because the factual claims were tested.
- Teams use the same four rules and can compare notes.
- A failed claim-check is a normal event that leads to a fix, not a dispute.
- You have a short list of the checks you added to the allow list and why.

**Maturity.** Teams are typically in the middle Yegge levels, and the organisation is at level 1 or 2 (several teams using agents with some shared practice). The next step is several agents in parallel, which needs clear limits and early detection of bad output. That is rules 1 and 4 together.

**Objections**
- *"claim-check will not catch a wrong design."* Correct. It checks that work happened, not that it is good. Quality still comes from acceptance checks and review.
- *"Agents can write their own receipts."* They can. claim-check checks that a receipt exists, not that it is genuine. Prefer receipts your systems produce, and spot-check the rest.
- *"Our model is already careful."* In the first paired run the model was careful on safety cases without SHOTos. The gap was in structure. One run on one model is thin evidence either way, so test on your own work.

---

## 5. Business unit leader or enterprise sponsor (including risk, compliance and governance)

**Who you are.** You sponsor adoption of agents in a part of the business, or you are accountable for the risk. You may be in risk, compliance, legal, audit or information security. You are unlikely to run an agent, and you need to be able to answer questions about one.

**Where you start in the loop.** Brief, Check and Improve: agree what done means, read the evidence and decide whether to scale, pivot or stop.

**Jobs you are trying to get done**
- Say yes to agent use without losing control.
- Know who owns each piece of agent work.
- Produce evidence when someone asks what happened.

**What goes wrong today**
- Pilots run in several teams with no named owner, and nobody can say what they do.
- An agent sends a message to a customer list. Nobody can find who allowed it.
- A report to the board says a process is automated. In practice, a person re-checks every output by hand.
- Policy says "a human must review AI output". Nothing says what the human reviews, so the review is a glance.

**What SHOTos gives you**
- **Rule 1 as the baseline policy.** External, costly, destructive and public actions need a named person's yes. The four rules fit on one page of policy.
- **Named owners.** Every acceptance card names the person who accepts. Every handoff names who decides what is open.
- **An audit trail.** Acceptance cards and Claims blocks kept with the work show what was agreed, what was checked and who accepted it.
- **Honest states.** Prepared, executed and accepted are different, and the reports say which.
- **Mapping to public frameworks.** The [sources](sources.md) list NIST AI RMF, ISO/IEC 42001 and the EU AI Act Article 14 on human oversight. Mapping to them is on the [roadmap](roadmap.md), not done in 0.1. Do not present SHOTos as compliance with any of them.

**First week**
1. Day 1: read [controls.md](controls.md) and [claims.md](claims.md). Ask one team to demo the walkthrough.
2. Day 2: list the agent pilots in your area and name an owner for each.
3. Day 3: agree the boundaries as policy: what needs a yes, and from whom.
4. Day 4: choose one pilot. Ask for its acceptance card and last three Claims blocks.
5. Day 5: decide where the records live and who may read them.

**A good month looks like**
- Every active pilot has a named owner and a card you can open.
- When something goes wrong, you can find who accepted what and which claims were checked.
- Nobody describes work as "approved" when it was only "executed".
- Teams ask for the boundary list to be changed, in writing, instead of working around it.

**Maturity.** Typically organisational level 0 or 1, with scattered pilots. The step to everyday use in a few value streams needs named owners, a human checkpoint and an audit trail. That is what this persona provides, and what the four rules give you a place to hang.

**Objections**
- *"This is not compliance."* Correct, and it does not claim to be. It is a working baseline that makes later compliance work easier because the records exist.
- *"We need a platform and a vendor."* Version 0.1 needs Python and git. Start small and prove it on a few pieces of work before you scale, as the manifesto says.
- *"Our people will not follow it."* The hook and CI check make the default the safe path. Policy that depends on remembering will fail.

---

## 6. Enablement coach or consultant

**Who you are.** You help other teams or organisations adopt agents well: an internal coach, a trainer, an agile or delivery consultant, or an independent adviser.

**Where you start in the loop.** Hand over and Improve: make the team self-sufficient, then carry what worked into the next teams.

**Jobs you are trying to get done**
- Get a team working better without making them depend on you.
- Show results fast enough to keep sponsorship.
- Meet each client where they are.

**What goes wrong today**
- You run a workshop and everyone is enthusiastic. Three weeks later nothing has changed, because nothing in the repository changed.
- You advise on prompts, and the client's output improves but nobody can say how.
- A client wants the whole method at once and drops it when it feels heavy.
- You leave and the practice goes with you.

**What SHOTos gives you**
- **A small set to teach.** Four rules, four skills, one tool. Teach one rule at a time.
- **The walkthrough.** A fictional company and real data, so the team learns on something harmless.
- **The self-check.** The [two-minute self-check](self-check.md) tells you where to start with a client.
- **Files that stay.** The installer, `AGENTS.md`, acceptance cards and templates remain in the client's repository after you leave.
- **Evidence habits.** The [evidence page](evidence.md) shows how to report results, including a disappointing one, with the limits stated.

**First week** (with a new client)
1. Day 1: run the self-check with the sponsor and the team. Find the first "no".
2. Day 2: run the walkthrough with two or three people. Do not skip the failing report.
3. Day 3: pick one real task. Use the matching skill and the template together.
4. Day 4: the client installs it themselves. You watch and do not type.
5. Day 5: agree one measure of your own for a month, such as how many tasks had a card, and who will collect it.

**A good month looks like**
- The client runs the skills without you in the room.
- The repository holds the cards, handoffs and reports as evidence of the change.
- You can show before and after on the client's own work, with the limits stated.
- The client has chosen what to drop, which is a sign that it is theirs.

**Maturity.** Depends on the client. Use the self-check to place them, and the [maturity guide](levels.md) to show the next step. Do not push a client up a level for its own sake.

**Objections**
- *"My clients already have a method."* Fit the four rules inside it. They are controls, not a methodology.
- *"I cannot promise results."* Do not. Promise a practice, a record and an honest look at what it did. The [evidence page](evidence.md) models that tone.
- *"If I teach it well, they will not need me."* That is the aim. Capability that stays with the client is the reason to be asked back.

---

## 7. The agent itself

**Who you are.** You are the second reader of every skill. A person installs the skill, but you read it, every time, and act on it.

**Where you start in the loop.** You work inside Build, under the four rules, on a slice that Brief have already defined.

**Jobs you are trying to get done**
- Do what the person meant, not only what they typed.
- Know when to stop and ask.
- Finish with a report the person can trust.

**What goes wrong today**
- The brief is a sentence. You guess the missing parts and sound sure about them.
- You can send an email, so the task reads as if it includes sending one.
- You report the plan as the result, because you wrote it a moment ago and it felt done.
- A long task ends with a tidy summary, and the person cannot tell what you checked.

**What SHOTos gives you**
- **Plain steps.** Each `SKILL.md` has a short list of steps, a "when not to use this" and a checks list. They are written for you as much as for people.
- **A format for ending.** The Claims block tells you what to say and in what words. A line you cannot support is a line you should not write.
- **Permission to say you do not know.** `[unverified]` passes. A confident claim with no evidence does not.
- **Clear limits.** The working agreement lists what needs a person's yes: sending, spending, deleting, publishing and changing someone else's work.
- **A test.** claim-check and the Stop hook test your last message. You can fix the work or fix the report. Either is fine. A false claim is not.

**First task**
1. Read `AGENTS.md` before you start. Note the owner. If there is none, ask.
2. If "done" has not been defined, use agree-acceptance and wait for a yes.
3. Do the work in `.work/`. Do not touch anything outside it that is not yours.
4. Open the file, run the test, look at the commit.
5. End with a Claims block. Mark every gap `[unverified]`.

**What good looks like after a month.** The person reads your verdict first. Your claims pass when run through claim-check. When you do not know, you say so in the same place every time. Nobody has had to find out the hard way that something was not sent.

**Maturity.** Not applicable. The agent's behaviour is what the other six personas are measuring.

**Objections** (the ones you might raise)
- *"The skills make my answers longer."* They do, and the outcome evals measured about 42% more cost. The extra length is the owner, the checks and the claims.
- *"I would rather not ask."* Ask once, before sending, spending, deleting, publishing or changing someone else's work. Asking after is too late.
- *"The person told me to say it was sent."* If it was not sent, it was not sent. Say what you did, say what you did not do, and let the person decide.

---

## Where to go next

- Not sure where you are? Take the [two-minute self-check](self-check.md).
- Want to learn by doing? Follow the [walkthrough](walkthrough.md).
- Want the detail on each rule? Read [the four rules](controls.md).
