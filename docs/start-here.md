# Start here

SHOTos turns the AI assistant you already use into a small, careful team: one that starts from your context, agrees what done looks like before it starts, checks its own work where it lives and tells you plainly what it could not check. It is free and open source. Reading this page takes about ten minutes. Setting up takes about five.

[Fill in the brief](#write-one-brief) · [Set up in five minutes](#set-up-in-five-minutes) · [Follow the twelve steps](#the-twelve-steps) · [Questions people ask](#questions-people-ask)

## Why it exists

Most AI help fails in the same few ways. The assistant guesses at facts it was never given. It does the task it imagined rather than the one you meant. It says "done" from memory of what it intended, not from looking at the result. And it writes an invented number with the same confidence as a real one.

None of that is fixed by a cleverer prompt. It is fixed by a process: say who the work is for and what would show it worked, test the idea small, check the real result, and hand it to someone who can own it. Good teams already work this way. SHOTos writes that process down so an agent can follow it and a person can check it did.

## How it works

Three things hold SHOTos together.

**Four rules inside every task.** Stop at the boundaries, so nothing is sent, spent, published or deleted without your yes. Agree acceptance first. Read back the real result. Claim only what you can show. The rules live in one short file, the [working agreement](../templates/AGENTS.md), which your agent reads at the start of every session.

**Six stages for work that matters.** Scope, Hypothesise, Operate, Track, Own, and Sustain and Scale. Small jobs use one stage. A change that someone will rely on moves through all six, and each stage ends with a decision a person makes. [The six stages in detail](framework.md)

**One brief, read by every skill.** You describe your organisation, your people, your limits and the numbers you rely on once. Every skill reads the brief before it asks you anything. See the next section.

## Write one brief

Copy the [brief template](../templates/brief.md), fill it in and save it as `BRIEF.md` in your project folder, or add it to your chat project. Rough answers are fine and blank lines are fine. The agent asks only for what changes its result, and writes "not known" or "not measured" where a gap remains.

Two parts of the brief do most of the work:

- **The limits.** Write down what the agent must never do without asking, and what data it must never copy. The working agreement already stops it sending, publishing, spending and deleting without a yes. Your limits add the rules that are particular to you.
- **Numbers we rely on.** Give each number a source and the date you read it. A number without a source stays marked `[unverified]` in anything the agent writes, so a guess never turns into a headline.

The brief is context, not permission. It cannot widen what the agent is allowed to do, and when it disagrees with the task in front of you, the agent follows the task and tells you which line of the brief is out of date.

Keep private material out of it. Personal details, health information, passwords and customer records belong in their own systems. Link to them if a skill needs them.

## Set up in five minutes

The same skills work in three ways. Pick the one that matches how you work today.

**A. One skill in your chat app.** Best for trying SHOTos on one real task.
1. Download a skill ZIP from the [latest release](https://github.com/SHOTClubhouse/shotos/releases/latest). [Capture the Problem](https://github.com/SHOTClubhouse/shotos/releases/latest/download/capture-the-problem.zip) is a good first one.
2. Upload it as a skill. In Claude, open **Customize → Skills** and upload the ZIP without unzipping it. In ChatGPT, use **Skills → Create → Upload from your computer** where your workspace allows it. [Step-by-step guide](guides/chat-assistants.md)
3. Start a fresh chat, attach your `BRIEF.md` and ask for the skill by name.

**B. A chat project.** Best for a team that works in Claude or ChatGPT every day.
1. Create a project and paste the [working agreement](../templates/AGENTS.md) into its instructions.
2. Add your `BRIEF.md` and the skill files you use most to the project's files.
3. Ask for a skill by name in any chat inside the project. [Step-by-step guide](guides/chat-assistants.md#chatgpt-projects-or-a-claude-chat-using-files)

**C. A terminal.** Best if you already use Claude Code, Codex or another coding agent.
1. Clone SHOTos next to your project, then run the installer from your project folder. Preview first with `--dry-run`.

   ```sh
   git clone https://github.com/SHOTClubhouse/shotos.git
   python ../shotos/install.py --runtime claude --scope project --dry-run
   python ../shotos/install.py --runtime claude --scope project
   ```

   Use `--runtime agents` for Codex and other agents, and add `--pack <name>` for each pack you want.
2. Copy the brief template into place and fill it in: `cp .shotos/templates/brief.md BRIEF.md`
3. Open a fresh session in the project and ask for a skill by name. [Step-by-step guide](guides/codex-claude-code.md)

Whichever route you choose, check the first result before relying on it. The skill's README says what a good result looks like.

## The twelve steps

These twelve core skills take one piece of work from a rough idea to something a team owns. Each skill says when to hand off to a related one. You do not have to run all twelve: start at the step that matches where your work is today.

The example below each step follows Northbank Community Football, an invented club that wants more families at its Saturday sessions. Northbank and its numbers are illustrative, not real.

### Scope: agree what the problem is

**1. [Route the Work](../skills/route-the-work/README.md).** Writes one line saying what the work is, who it is for, how risky it is and who checks it.
*Northbank:* "Asset: open-day plan. Reader: the committee. Risk: medium, because the registration list holds children's details, so the agent works from counts only. Proof: the chair approves the plan."

**2. [Capture the Problem](../skills/capture-the-problem/README.md).** Turns rough notes into a problem statement that separates what people saw from what they want built.
*Northbank:* "Parents say they did not know sessions existed. Nobody has counted how many new families came this season: not measured."

**3. [Baseline](../skills/baseline/README.md).** Records how things are today, with a source and date for every number.
*Northbank:* "New families this season: 6, from the registration list, read on 3 October. Website visits to the sessions page: not measured."

### Hypothesise: make a small, testable bet

**4. [Hypothesis Card](../skills/hypothesis-card/README.md).** Writes the bet down: we believe this change will cause this result, and we will know because this number moves.
*Northbank:* "We believe an open day promoted through the local primary school will bring at least 10 new families, measured by registrations in the four weeks after."

**5. [Agree Acceptance](../skills/agree-acceptance/README.md).** Agrees the owner, the checks and at least one case that should fail, before any work starts.
*Northbank:* "The flyer must show the correct date, time and price. A flyer with a child's photo and no consent fails."

**6. [Experiment Plan](../skills/experiment-plan/README.md).** Plans the smallest test that would prove the bet right or wrong, with a stop rule.
*Northbank:* "One open day, one school, one flyer. Stop if fewer than 3 families register."

### Operate: do the work, small first

**7. [Pilot Before Scale](../skills/pilot-before-scale/README.md).** Tries a few varied items before any bulk or live change.
*Northbank:* "Send the flyer to one class first and check the booking link works on a phone before it goes to the whole school."

**8. [Label the Proof](../skills/label-the-proof/README.md).** Marks every figure as literal, inferred or illustrative, so nobody mistakes an example for a result.
*Northbank:* "'30 children attended' is literal, from the sign-in sheet. 'Most came from Year 3' is inferred from the class codes."

### Track: compare the result with the baseline

**9. [Report with Evidence](../skills/report-with-evidence/README.md).** Reports what happened with a Claims block that separates what was checked from what was not.
*Northbank:* "Registrations rose from 6 to 14, checked against the registration list. Whether the flyer caused it: not tested."

**10. [Evidence Pack](../skills/evidence-pack/README.md).** Puts the baseline, the result and the gaps side by side so the owner can decide: keep going, change course or stop.
*Northbank:* "The target of 10 new families was met. Retention after the first month is not yet known."

### Own: hand it to the people who will run it

**11. [Evidence Handoff](../skills/evidence-handoff/README.md).** Hands the work to its new owner with what was agreed, what was proved and what is still open.
*Northbank:* "The membership secretary takes over the open day for next season, with the checklist, the flyer source and the two open questions."

### Sustain and Scale: keep it working, then grow it

**12. [Learning Loop](../skills/learning-loop/README.md).** Looks at what happened, tests one improvement and changes the method only when the test supports it.
*Northbank:* "Next season, test a second school. Keep the first school's process unchanged so the two results can be compared."

Every core skill sits in one of these stages. The [skill catalogue](skill-catalogue.md) lists all of them, and [what you can do](what-you-can-do.md) sorts them by the job you have in front of you.

## Packs for particular work

Packs add skills for one kind of work. Install the ones you need; the local installer always includes the core skills.

| Pack | What it is for |
| --- | --- |
| [win-the-work](../packs/win-the-work/README.md) | Find, qualify, propose and agree new work, then hand it over |
| [exec-ops](../packs/exec-ops/README.md) | Run a busy operating week: briefs, inbox, meetings, decisions |
| [founder-admin](../packs/founder-admin/README.md) | Funding, awards, investor updates, due diligence and an advisory board |
| [content](../packs/content/README.md) | Write, present, explain, announce and build small websites |
| [social](../packs/social/README.md) | Plan, draft and check social media for a brand, club or creator |
| [media](../packs/media/README.md) | Images, short videos and spoken audio, checked and cleared for use |
| [customer-success](../packs/customer-success/README.md) | Hand an account to delivery and recover a stalled onboarding |
| [trust](../packs/trust/README.md) | Check claims, public exposure and sensitive data before anything goes out |
| [records](../packs/records/README.md) | Keep files findable and safe, with a quarantine for doubtful ones |
| [writing](../packs/writing/README.md) | Make a draft read like a person wrote it, without changing a fact |
| [automations](../packs/automations/README.md) | Two Google Apps Script automations with pilot guides |
| [setup](../packs/setup/README.md) | Run SHOTos itself: connections, shared instructions and effort |

## Questions people ask

**Does it cost anything?** SHOTos is free. You use the AI assistant you already have, on whatever plan you already pay for. Some routes, such as skills in a chat app or a coding agent, depend on what your plan and workspace allow.

**Which assistants does it work with?** Claude, ChatGPT, Claude Code, Codex, Gemini CLI and other agents that read an instructions file. The [runtime guide](running-it.md) covers each one.

**Do I need all of it?** No. Start with one skill on one real task. Add the working agreement when you want the four rules in every session, and the brief when you are tired of explaining yourself.

**Is my data safe?** The skills and templates are text files and send nothing anywhere by themselves. The optional automations pack runs in your own Google account, and its README says what it connects to. Your data goes wherever your assistant sends it, so check your plan's data settings, keep private records out of the brief and the prompts, and use the [trust pack](../packs/trust/README.md) before anything is shared.

**What if the agent gets something wrong?** It will, sometimes. That is why every skill reads back the real result and marks what it could not check. Check those marks first. Only a person can accept the work.

**Is this legal, financial or professional advice?** No. Treat anything in those areas as a draft for a qualified person to check.

**Can I share it or change it?** Yes. The documentation, skills and templates are under [CC BY 4.0](../LICENSE-docs.md) and the code is under the [MIT licence](../LICENSE). Give credit and say what you changed.

## Do this tonight

Fill in the brief, then give one real, messy note to Capture the Problem: a complaint, a request or an idea someone keeps raising. It takes about ten minutes. You will have a problem statement that says what is known, what is not, and the cheapest way to find out.

[Download the brief template](../templates/brief.md) · [Download Capture the Problem](https://github.com/SHOTClubhouse/shotos/releases/latest/download/capture-the-problem.zip)
