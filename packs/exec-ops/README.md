# exec-ops pack

**Skills for a founder, executive or anyone running a busy operating week with an agent.**

The pack turns the repeating parts of an operating week into short, checkable loops: a daily brief, a single inbox for rough notes, mail triage, meeting notes, a weekly briefing, decision briefs and advisory sessions. Each loop reads real signal, keeps one record up to date and reports only what needs a person. Drafts by default; nothing is sent, posted or deleted without the owner's yes on exactly what goes.

## Who it is for

- Founders and chief executives who lose track of dated obligations and open commitments.
- Chiefs of staff and executive assistants who run a leader's week.
- Leaders who chair advisory groups or boards and want the session prepared and the actions owned.
- Anyone who wants an agent to do the reading and drafting while a person keeps the decisions.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [daily-brief](skills/daily-brief/README.md) | Operate | Reconciles a ledger of dated obligations against fresh mail and calendar signal, drafts what needs drafting, and produces one digest of what needs a person. |
| [leaders-inbox](skills/leaders-inbox/README.md) | Scope | Reduces rough notes, links and ideas to meaning and source, then routes each to exactly one outcome. |
| [inbox-triage](skills/inbox-triage/README.md) | Operate | Classifies mail threads by action state, drafts replies from the real thread and flags slipped threads. |
| [meeting-notes](skills/meeting-notes/README.md) | Track | Turns new recordings or transcripts into structured notes, with a watermark ledger and one rolling file per person or organisation. |
| [weekly-exec-brief](skills/weekly-exec-brief/README.md) | Track | Writes an evidence-led weekly briefing: what changed, what needs deciding, what is unverified. |
| [decision-brief](skills/decision-brief/README.md) | Hypothesise | Sets out question, sourced facts, assumptions, options, a recommendation and what would change it. |
| [advisory-session](skills/advisory-session/README.md) | Own | Prepares and runs an advisory session and leaves one action record with one owner per action. |

## Executive Decision Review

Start with one recurring choice from the weekly brief. Use the [review cycle](skills/decision-brief/review-cycle.md) to connect the one-page decision brief, the owner's decision and the handoff. Use the next cycle to see whether another operator can run it from the evidence.

## Needs

Read-only access first, and drafts instead of sends, throughout.

- **Mail connector:** read threads and labels; create drafts. Sending is not needed and should stay off.
- **Calendar connector:** read events. Creating or changing events needs the owner's yes each time.
- **Document connector:** read and write the ledger, notes and briefs in a folder the owner names.
- **Transcript connector:** any source that returns a transcript, a recording list and times (used by meeting-notes). A pasted transcript works too.
- Without a connector, the skills work from pasted text and say which sources were unavailable.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack exec-ops --dry-run
python ../shotos/install.py --runtime claude --scope project --pack exec-ops
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

The loops follow the four rules in [docs/controls.md](../../docs/controls.md). Any task class that wants to run without a person in the loop earns that through [rules/12-graduation.md](../../rules/12-graduation.md). The stages are described in [docs/framework.md](../../docs/framework.md).
