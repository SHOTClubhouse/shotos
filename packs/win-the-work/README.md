# Win the work

**Find, qualify, propose and agree new work, then hand it over cleanly, using two short methods: LEAP for the pipeline and NUDGE for qualification.**

This pack is for anyone who has to win customers, partners, funding or advisers and wants the evidence behind each deal to be visible. It gives an agent a repeatable way to run a pipeline, ask the right questions, research the reader, write the proposal and reply to the thread, without sending anything on your behalf.

## Who it is for

- Founders and sales leads who run a pipeline in a spreadsheet and lose track of what is real.
- Small teams that write many proposals and want each one argued for its reader.
- Account owners who need a clean handover from "we won it" to "we are delivering it".
- Anyone who wants an agent to draft outreach and replies and send nothing until they say yes to exactly what goes.

## The two methods

### LEAP: the pipeline

LEAP has four stages. Each has three sub-steps and an exit test, so a deal moves on because something is true, not because time has passed.

| Stage | Sub-steps | Exit test (short form) |
|---|---|---|
| **L**ead | warm, cold, target | A named person at a named organisation has agreed to a first conversation. |
| **E**xplore | meeting, discovery, define | The problem, the cost of leaving it and a definition of the work are written down and the buyer has seen them. |
| **A**gree | proposal, statement of work, gatekeepers | Scope, price and terms are accepted in writing by the person who can sign, and every gatekeeper is accounted for. |
| **P**lan | start date, handover, delivery | A start date, an owner and a handover packet exist, and delivery has been accepted into SHOTos Scope. |

### NUDGE: the five questions

NUDGE is how you qualify an opportunity, mainly during Explore and Agree. Score each question with evidence, mark unknowns as unknown.

| Letter | Question |
|---|---|
| **N**umbers | What are your numbers and theirs, and is the benefit mutual? |
| **U**nderstand | What are their challenges, and what does it cost them not to solve them? |
| **D**efinition | Is the work clearly defined and can it be delivered in the time and budget? |
| **G**atekeepers | Who can say yes or no, and what does each want personally? |
| **E**levate | What sets you apart, and what value do you add above the competition? |

## How they fit together

```
        LEAP: the pipeline
 ┌──────┐   ┌─────────┐   ┌───────┐   ┌──────┐
 │ Lead │ → │ Explore │ → │ Agree │ → │ Plan │ ──► handover packet ──► SHOTos S: Scope
 └──────┘   └────┬────┘   └───┬───┘   └──────┘                          (then H, O, T, o, s)
                 │            │
        NUDGE qualifies here and here
                 │            │
           ┌─────▼────────────▼─────┐
           │ N  U  D  G  E          │   go / pause / walk away,
           │ scored with evidence   │   plus the next question to ask
           └────────────────────────┘
```

NUDGE runs during **Explore** (is this worth a proposal?) and again during **Agree** (is it still safe to commit?). LEAP's **Plan** stage ends with a handover packet, and delivery then begins at SHOTos **Scope**, where the work is framed, owned and accepted like any other.

For a short handout, use the [LEAP quick reference](leap-quick-reference.md) or [NUDGE quick reference](nudge-quick-reference.md). The [qualification sheet and CRM header templates](crm/README.md) prepare data for HubSpot or Salesforce. Map fields to your account before importing.

## The skills

| Skill | SHOTos stage | What it does |
|---|---|---|
| [leap-pipeline](skills/leap-pipeline/README.md) | any (hands over to Scope) | Runs and reviews a pipeline through Lead, Explore, Agree and Plan; flags stalled deals with evidence; produces the handover packet. |
| [nudge-qualify](skills/nudge-qualify/README.md) | Scope | Scores an opportunity on the five NUDGE questions and recommends go, pause or walk away. |
| [relationship-map](skills/relationship-map/README.md) | Scope | Maps people, organisations, opportunities, evidence, owners and next actions for a market or account. |
| [contextual-proposal](skills/contextual-proposal/README.md) | Operate | Researches the reader, then writes a proposal argued for them, with a claim ledger and asset register. |
| [one-off-or-factory](skills/one-off-or-factory/README.md) | Hypothesise | Decides between writing one item directly and building a factory for many. |
| [proposal-factory](skills/proposal-factory/README.md) | Operate | Produces many tailored proposals from one master after a three-item pilot. Produces drafts and a review queue for authorised senders. |
| [outbound-prospecting](skills/outbound-prospecting/README.md) | Operate | Plans one testable segment, a batch of five, and drafts one message per contact for a person to send. |
| [email-reply](skills/email-reply/README.md) | Operate | Drafts a reply to a real thread in the owner's voice from a response map and verified context. |

## What this pack does not do on its own

It drafts. It does not send email, post, submit, buy or change a shared record without a named person's yes (rule 1, [Stop at the boundaries](../../docs/controls.md)). "Ready for review" never means "sent".

## Needs

Nothing beyond the agent for the core of every skill. Some skills work better with read access to a mailbox, a CRM export or a folder of past proposals; each skill README says which. No skill needs write access to any of them.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack win-the-work --dry-run
python ../shotos/install.py --runtime claude --scope project --pack win-the-work
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack, use the same runtime and scope and name the extra pack. Existing files are kept.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

Evidence: earlier skill versions were tested in paired runs. See the [evidence by build](../../docs/evidence.md). See [evals/packs/win-the-work.json](../../evals/packs/win-the-work.json).

