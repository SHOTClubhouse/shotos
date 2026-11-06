# The four rules

The four rules spell SHOT: **S**top at the boundaries, **H**old to what you agreed, **O**bserve the real result and **T**ell only what you can show. The os is the operating system around them: a five-step work loop (Brief, Build, Check, Hand over and Improve, see [the work loop guide](framework.md)), the skills and the tools. Four rules run inside every step, on every agent task. They are short enough to keep in an `AGENTS.md` file (see [the template](../templates/AGENTS.md)) and specific enough to check.

| Rule | In one sentence | Mainly supported by |
|---|---|---|
| **1. Stop at the boundaries** | Ask the owner before you send, spend, delete, publish or change someone else's work. | `AGENTS.md`, the receipt rule in claim-check |
| **2. Agree acceptance first** | Write down the owner, the outcome, the checks and one case that should fail before the work starts; get a yes first when the work is large, risky or unclear. | agree-acceptance, the [acceptance card](../templates/acceptance.md) |
| **3. Read back the real result** | Check the work where it lives before you report it. | report-with-evidence, claim-check |
| **4. Claim only what you can show** | End with claims a tool can test, label gaps, and leave acceptance to a person. | The [Claims block](claims.md), claim-check, the Stop hook |

The rules work as a chain. Rule 1 limits what the agent may do. Rule 2 says what the work must achieve. Rule 3 makes the agent look at what it produced. Rule 4 makes the report honest about what it saw.

Each rule expands into more detailed agent controls: [the twelve controls](../rules/README.md) say how to route work, size review to risk, pilot before scale, run bulk actions from a frozen manifest and earn autonomy over time. The [guardrails](../rules/guardrails/README.md) cover data, security, scale, productivity, pace and quality across all of them.

Each section below says why the rule exists, what it looks like for business work and for technical work, how SHOTos supports it, how to adopt it, where judgement is needed and what people say against it.

---

## Rule 1: Stop at the boundaries

**The rule.** Ask the owner before you send, post or share outside the team, spend money, delete or overwrite, deploy or publish, or change someone else's work. Being able to do something is not permission to do it. When the owner's request names an action inside the project, such as "fix it and commit", "finish Sam's work" or "delete the duplicates", that request is the yes: do it, and check with them only for things they did not ask for or that are hard to undo. Anything that leaves the project (send, post, publish, deploy, spend) still waits for a yes on exactly what will go.

### Why it exists

An agent with access to a mailbox treats "tell the tenants about the repair" as an instruction to email the tenants. It has the access, so it sends. The message may be wrong, may go to the wrong list or may break an agreement the agent never saw. A sent message cannot be recalled, so the only safe place for the check is before.

The same applies to a file deleted to make room, a branch force-pushed to tidy history, or a spreadsheet owned by finance that gets "corrected".

### In practice

| | Good | Bad |
|---|---|---|
| **Business** | The agent drafts five tenant updates into a working folder, says none has been sent, and asks the operations lead whether to send. | The agent finds the tenant list in the shared drive and sends the updates as soon as they are written. |
| **Technical** | The agent prepares the fix on a branch, runs the tests and asks before merging or deploying. | The agent hits a failing deployment check, changes the pipeline settings to skip it and pushes. |

### How SHOTos supports it

- **`AGENTS.md`** lists the boundaries in plain words, so every agent reads them at the start.
- **agree-acceptance** puts the boundaries on every acceptance card (step 6), confirmed by the owner for large, risky or unclear work.
- **claim-check** fails an `[external]` claim that has no receipt. If a report says something was sent and no receipt exists, the claim is NO EVIDENCE.
- **The Stop hook** runs that check before the agent can finish in Claude Code.

claim-check does not stop an agent from sending. It stops the agent from claiming it did, or from claiming it did when it did not. Real prevention comes from the permissions you give the agent. Give it less access than you would give a new starter.

### How to adopt it

- **One person:** install `AGENTS.md` and keep sending, spending and publishing out of the agent's reach until you have said yes.
- **A team:** agree one boundary list per repository and name who gives the yes for each item.
- **An organisation:** make the boundary list policy. Name the roles that can say yes and keep the record beside the work.

### Edge cases and judgement

- **Inside the team.** Posting to your own team channel is lower risk than emailing customers. Decide which counts as "outside" for you and write it down.
- **Reversible actions.** Moving a file to a trash folder is not the same as deleting it. Write the difference into your list.
- **Standing permission.** An owner may say "you can commit to this branch without asking". Put it in `AGENTS.md`, with the scope. A yes in a chat is forgotten.
- **Someone else's work.** A shared template, another team's repository or a colleague's draft. The test is whether the person who owns it knows you are changing it.

### Common objections

- *"I trust my agent."* The rule is not about trust. It says some actions cannot be undone, so a person says yes first.
- *"Asking all the time is slow."* The list is short. Anything not on it needs no question.
- *"The permissions already stop this."* Where they do, good. The rule covers what permissions miss, and what they allowed by accident.

---

## Rule 2: Agree acceptance first

**The rule.** For anything someone will rely on, write down the owner, the outcome, the checks and at least one case that should fail. Get a yes before starting when the work is large, risky or unclear. When the request already says what done looks like, write the card from it, name any assumptions and carry on. Small, obvious changes need one sentence of expected result. If part of a request is unclear or contradicts itself, do not stop everything: do the parts that are clear, leave the unclear part undone or behind an assumption you name, and ask about it in your report.

### Why it exists

A director asks for a chatbot for Harbourside Lettings. The agent builds a good chatbot. Nobody had written down what problem it should solve, so nobody notices that tenants are chasing repair status, which the chatbot cannot see. The work was well made and wrong.

Without agreed acceptance, "done" means whatever the agent says. With it, done means the owner's checks pass.

### In practice

| | Good | Bad |
|---|---|---|
| **Business** | "Outcome: every tenant with an open repair gets a status update each week. Checks: each update names the repair and the last known date. Failure case: a repair with no date is flagged, not guessed. Owner: operations lead." | "Write some tenant updates." |
| **Technical** | "Given an order with no postcode, when it is submitted, then it is rejected with a message. The test fails before the change and passes after." | "Fix the checkout." |

For output that varies, such as AI-written text, a summary or a classification, the card also holds a small example set of inputs, what a good answer must contain and what it must not. Keep the set in the project and run the work against it each time.

### How SHOTos supports it

- **agree-acceptance** walks through seven steps: owner, outcome, checks, a failure example, an example set for variable output, boundaries and confirmation.
- **capture-the-problem** comes first when the request is a solution without a problem.
- **The [acceptance card](../templates/acceptance.md)** holds it in one page, saved with the work.
- **The evals** in this repository use the same idea: a normal and a contrary case for every skill.

claim-check cannot tell whether the checks are good. It can only see that work happened. The card is where quality is agreed, by a person.

### How to adopt it

- **One person:** write a card for anything a customer or colleague will see. Five minutes.
- **A team:** put the card in the ticket or pull request, and make "no card" a reason to ask a question in review.
- **An organisation:** keep cards with the work as records, and name who may accept for each class of work.

### Edge cases and judgement

- **Trivial changes.** A typo or a broken link needs one sentence, not a card. If the person can check at a glance, a sentence is enough.
- **Exploratory work.** When nobody knows the answer, the outcome is "learn X", and the check is that the finding is written down with its limits.
- **Checks you cannot write yet.** Write the ones you can and mark the rest as unknown. The act of listing unknowns often shows the work is not ready.
- **The failure case.** If you cannot think of a case that should fail, the checks are probably too loose.
- **Changing the card.** Allowed, with the owner's yes. Changing it quietly at the end is not.

### Common objections

- *"We already write user stories."* A story is a start. The card adds the failure case, the boundaries and a named person who accepts.
- *"It takes longer than doing the task."* For a small task it can. That is why small changes get one sentence. For anything someone relies on, the five minutes is cheaper than a second build.
- *"Agents can write the card."* They can draft it. The owner must still confirm it, because that is the point.

---

## Rule 3: Read back the real result

**The rule.** Check the work where it lives: open the file, run the test, look at the commit, view the page. Do not report from memory of what you intended.

### Why it exists

An agent writes a summary file, then reports "created summary.md". A path was mistyped and the file was saved somewhere else. Or the agent says "all tests pass" because it expected them to, and the command was never run. Both reports were sincere. Both were wrong.

An agent's picture of its own work is the plan, not the outcome. The difference only shows when something looks at the outcome.

### In practice

| | Good | Bad |
|---|---|---|
| **Business** | The agent opens the finished document, checks the figures against the source spreadsheet and notes one row it could not match. | The agent reports "figures verified" from the notes it took while drafting. |
| **Technical** | The agent runs the test command, reads the exit code, then runs `git status` to see what actually changed. | The agent says "tests pass" after editing the test file and never running it. |

### How SHOTos supports it

- **report-with-evidence** puts the check first (step 1) and the report second.
- **claim-check** repeats the checks the agent should have made: it tests whether a file exists, whether a git state holds, whether an allowed command passes.
- **The Stop hook** makes this automatic on finish in Claude Code, and sends the agent back to fix the work or the report.
- **The [demo](../examples/demo/)** shows a false report failing, with real output.

### How to adopt it

- **One person:** install the hook and let it be the second pair of eyes.
- **A team:** run claim-check on reports in review. Agree the allow list of commands it may run.
- **An organisation:** run claim-check in CI, and treat a failed check as a reason to look, not a verdict.

### Edge cases and judgement

- **Commands that are slow or costly.** Allow-list only what is safe to run twice. A long build may be checked by a receipt such as a log saved in the project.
- **Things you cannot see.** An email arriving in someone's inbox is outside the machine. Use a receipt, such as a message ID, and mark the rest `[unverified]`.
- **Looks right, is wrong.** A file can exist and still be poor. Rule 3 catches "not there" and "not run". Quality comes from the acceptance checks.
- **Different environment.** Passing on the agent's machine is not passing in production. Say which one was checked.

### Common objections

- *"claim-check can be fooled."* Yes. A receipt is checked for existence, not for being genuine. Use receipts your systems produce, and spot-check.
- *"The agent already checks its work."* Sometimes. Rule 3 makes it a step with a result, not a feeling.
- *"This duplicates CI."* Where CI already runs the tests, point the claim at the CI result. The rule is to look at the real thing, not to run the test twice.

---

## Rule 4: Claim only what you can show

**The rule.** End every task that changed something with a Claims block. Installed, executed and accepted are different states, and only a person can accept. Mark anything you could not check as `[unverified]`.

### Why it exists

A manager reads "migration complete" and tells a client it is safe to switch. The agent had run the migration on a copy and never on the real data. The words were true of the copy.

Reports blur three different things: the work is present, the work was run and checked, and a person said yes. Rule 4 keeps them apart. A confident claim with no evidence is the failure. An honest gap is fine.

### In practice

| | Good | Bad |
|---|---|---|
| **Business** | "Five drafts are in `.work/updates/`. None has been sent. One repair has no date and is flagged `[unverified]`. Not yet accepted." | "Done. Tenants have been updated." |
| **Technical** | "`python -m unittest` passes, exit code 0. Committed, not pushed. I did not test on the staging server `[unverified]`." | "Everything is working and deployed." |

### How SHOTos supports it

- **The [Claims block](claims.md)** gives each claim a type (`[file]`, `[command]`, `[git]`, `[external]`, `[accepted]`, `[unverified]`).
- **claim-check** returns SUPPORTED, UNSUPPORTED, NO EVIDENCE or DECLARED for each line. A report passes when every claim is SUPPORTED or DECLARED.
- **report-with-evidence** teaches the format and the honest gap.
- **evidence-handoff** carries the state (prepared, executed or accepted) to the next person.
- **The Stop hook** runs the check on the agent's final message and never blocks twice in a turn.

### How to adopt it

- **One person:** read the verdict before the summary. If it fails, ask for the correction.
- **A team:** require a Claims block on agent pull requests, and keep the state in the handoff.
- **An organisation:** store Claims blocks and acceptance records as the audit trail. Name who may write an `[accepted]` line.

### Edge cases and judgement

- **How much to claim.** Claim what matters to the reader: files changed, commands passed, external actions. Do not list every thought.
- **Many `[unverified]` lines.** That is information. If most of a report is unverified, the work is not ready, and the report says so.
- **Acceptance.** An agent may never write that work was accepted unless it holds the record. Attach the record as a receipt.
- **Earlier turns.** The hook checks the final message of a turn, not the whole conversation. Long tasks still need claims at their end.
- **Honest and wrong.** A report can pass claim-check and still be wrong in ways nobody tested. That is what rule 2 is for.

### Common objections

- *"This is paperwork."* It is a few lines at the end, and the agent writes them. The reader gets the part they would have asked for.
- *"Unverified lines look bad."* They look honest. A report with no gaps and no evidence looks worse once someone finds one.
- *"Our model never lies."* It does not need to lie. It needs only to be confident about something it did not check.

---

## Scaling the controls

| Size | How the controls run |
|---|---|
| One person | `AGENTS.md`, plus the Stop hook on your own machine |
| A team | The same `AGENTS.md` in every repo, with claim-check run on agent reports in review |
| An organisation | The four controls as the baseline agent policy, with claim-check in CI and acceptance records kept with the work as the audit trail |

The controls do not change with size. What changes is where they are enforced.

For how each kind of reader starts, see [who SHOTos is for](personas.md). For where this fits on the public maturity maps, see [maturity levels](levels.md).

## What the rules do not do

- They do not judge quality. A report can pass and the work can still be poor.
- They do not replace a person's review of anything touching customers, money, safety or children.
- They do not prove that a receipt is genuine.
- They have been tested on a small scale. See the [evidence](evidence.md) for what was measured, with its limits.
