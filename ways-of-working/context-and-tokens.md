# Context and tokens

## What it is

An agent reads and writes in units called tokens, and it can hold only so many in view at once; that limit is its context window. Everything the agent knows about the task right now has to fit: your instructions, the files it has read, the output of the tools it has run and the conversation so far. Spend is usually counted in tokens too. Managing context means deciding what goes in the window, what stays out and what is written down for later. It is the working discipline behind [control 11, context control](../rules/11-context-control.md).

## Why it matters with agents in the loop

A crowded context makes agents worse, not just dearer. Important instructions get buried, old and new information conflict, and the agent may follow a stale line from early in the session. Long sessions drift: the agent forgets a constraint, repeats work or confidently restates something that was true an hour ago. The fix is not a bigger window. It is putting less in, putting it in the right place and saving the state so a fresh session can pick up cleanly.

Cost matters as well. Each call pays for the whole context again. A bloated context taxes every step after it.

## The practice

### Keep instruction files short

The file an agent reads at the start of every session (often called `AGENTS.md` or similar) is read every time. Every line costs tokens on every task and competes for attention. Keep it to what is true for nearly every task:

- The boundaries (what needs a yes).
- How to find things: where the task records live, where the tests are run.
- The few conventions that matter, such as naming and language.
- Pointers to longer material, not the material itself.

If a line applies to one kind of task, move it to a skill or a note that is loaded for that task. Review the file when it grows. A page is a good target; more than two pages is a warning. See the [AGENTS.md template](../templates/AGENTS.md) for a starting point.

### Load skills on demand

A skill is a packaged set of instructions for one kind of job. Keep the skill list as short descriptions, and load the full text only when the task needs it. Ten skills in full, loaded at the start, spend tokens on nine that are not used. The description of each skill should say what it does and when to use it, so that the right one is picked.

### Save large outputs to files

When a tool returns a long log, a big table, a web page or a search result, do not leave it in the conversation. Save it to a file in the task folder and work from the file: read the part you need, search it, summarise it. Keep the file path in the task record. This keeps the context small and the evidence intact, since the original is still there if someone wants to check.

Ask for what you need. "List the failing tests and the first error of each" costs far less than "show the whole log".

### One owning record per piece of work

Each piece of work has one task record that holds the goal, the acceptance, the state, the decisions, the evidence links and the next step. The record, not the chat, is the source of truth. A new session reads the record and starts where the last one stopped. Do not scatter state across several notes; the one place is the one that stays current. See [records-and-filing.md](records-and-filing.md).

Keep the record about the work, not about people. Do not copy private or personal information into it, and keep secrets out entirely.

### Hand off before the context fills

Do not wait for the window to fill or for the system to compress it automatically. At natural breaks (the end of a stage, before a long run, when the conversation has wandered), update the task record and write a short handoff:

1. The goal and the acceptance.
2. What is done, with evidence links.
3. What is not done, and why.
4. Decisions made and the reason.
5. Blockers and open questions, with the named person.
6. The exact next step.

Then start a fresh session from the record. A clear handoff costs a few hundred words and saves rereading the whole conversation. See the [handoff template](../templates/handoff.md).

Metadata-only continuity is enough for most handoffs: say what was decided and where the files are, without pasting the conversation.

### Reset, do not argue

If the agent has gone down a wrong path, or the session has become muddled, start a new one from the record rather than correcting at length. Ten corrections in one conversation leave ten corrections' worth of noise behind.

### Measure cost per accepted task

Count what you spend against what you got. **Cost per accepted task** is the total spend divided by the number of outputs a person accepted. It makes waste visible: output that was rejected still cost money. Record, for each task class:

- Tokens or spend per run.
- The share accepted without edits.
- Time from request to acceptance.

Compare across routes and instruction versions (see [model-and-tool-routing.md](model-and-tool-routing.md) and [evals-for-ai-output.md](evals-for-ai-output.md)). A cheaper run that is accepted half as often is not cheaper. A high-cost task that is always accepted may be fine. Set a budget for a long task before starting and tell the owner when you are near it.

## What good looks like

- The standing instruction file fits on a page or two and has been pruned lately.
- Skills are listed briefly and loaded only when needed.
- Long outputs live in files and the conversation stays light.
- Every task has one record that someone new to the task could continue from.
- Handoffs are written before the window fills, not after it breaks.
- The team can state its cost per accepted task for each class of work.

## Anti-patterns

- **A manual in the instruction file.** Everything the team has ever learned, loaded on every run.
- **Pasting whole documents** into the conversation when a path would do.
- **Never starting afresh:** one huge session that holds three tasks and forgets two.
- **Copy-pasted state** in four places that disagree.
- **Secrets in instruction files** or in task records.
- **Counting cost per call** and ignoring rework.
- **Relying on automatic compression** to keep what matters.

## How it maps to the stages and rules

- **Scope:** one task record starts with the problem statement.
- **Operate:** short context, outputs in files, handoffs at breaks.
- **Track:** cost per accepted task is a measure.
- **Own:** the receiving team inherits records, not chat history.
- **Control 11:** context control is this page in policy form.
- **Rule 3:** read the file, not a recollection of it.
- **Rule 4:** claims cite the file or log where the evidence lives.

## A short example

Millbrook Rovers' volunteer coordinator runs an agent over a season's worth of fixture emails. The first session reads fifty emails into the conversation and gets slow and confused. For the second attempt she makes a task folder with a record. The agent saves the emails as files, extracts fixtures into a table, and writes a one-page summary of what it found and what it was unsure about. Halfway through, she asks for a handoff, starts a fresh session and gives it only the record and the table. The second session picks up in a minute. At the end she compares: the first attempt used about three times the tokens (an invented figure for illustration) and produced a table with errors; the second produced a table she accepted after two edits. She notes the accepted-task cost and keeps the method.

## Further reading

- Public documentation from your agent tool on instruction files, memory and context management.
- Public guides on prompt caching and context windows from model providers.
- David Allen, *Getting Things Done*, on keeping one trusted record.
- Gerald Weinberg, *The Psychology of Computer Programming*, on keeping working state outside the head.
- Anne Lamott, *Bird by Bird*, for the case for short first drafts.
