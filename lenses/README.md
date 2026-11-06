# Review lenses

A lens is a perspective that comments on work in the conversation. It asks the questions a particular kind of reviewer would ask and says what it notices. It never changes a fact, and it never puts its voice into the work itself.

## What a lens is

Think of a lens as a seat at the table. When you bring in the sceptic lens, someone at the table asks "what is the cheapest way this fails?". When you bring in the customer lens, someone asks "would the person who receives this understand it, and do they want it?". The answer arrives as a short comment, set apart from the work.

Seven lenses ship here:

| Lens | What it brings |
|---|---|
| [lead](lead.md) | The one accountable voice that pulls the comments together and names the next action |
| [sceptic](sceptic.md) | The failure, and the evidence that is missing |
| [voice-of-reason](voice-of-reason.md) | The sensible, slightly anxious check on risk, spend and compliance |
| [customer](customer.md) | The end user's view |
| [care](care.md) | What the work is costing the people doing it |
| [commercial](commercial.md) | Money, value, price and who pays |
| [connector](connector.md) | Links to other work, people and earlier decisions |

## How they appear in the conversation

Each lens drops into the agent's reply as a short quote block that starts with its marker and name, set apart from the work:

| Lens | Default marker |
|---|---|
| lead | 🧭 |
| sceptic | 🔍 |
| voice-of-reason | 🛑 |
| customer | 🙋 |
| care | 🫶 |
| commercial | 💷 |
| connector | 🧩 |

Example, on a draft price-change email:

> 🔍 **Sceptic:** The "save 20%" line has no source. It is the sentence members will remember, so check it first.

> 🙋 **Customer:** The new price is in paragraph four. Put it, and the date it starts, in the first line.

> 🧭 **Lead:** Source the saving, move the price up, then send the draft to the owner. Nothing has been sent.

Where emoji do not render, use a text marker such as `[sceptic]`. The work itself, the email in this example, never carries the lenses.

### Switching them on for every session

Add this to your project's `AGENTS.md` (or `CLAUDE.md`) so the agent uses lenses without being asked:

```
## Review lenses
On substantial replies, add one to four review lenses from lenses/ as quote blocks that start
with the lens marker and name, chosen for the risk. The lead lens closes with the next action.
Lenses comment in the conversation only; deliverables stay plain. "Lenses off" turns them off
until I turn them back on.
```

With a [cast](cast-template.md), replace the default markers and names with your characters.

## How to ask for one or several

Name the lens in the request:

- "Review this proposal with the sceptic lens."
- "Give me the customer and commercial lenses on this pricing page."
- "Run the lead lens at the end and tell me the next action."

Without a name, the lead lens speaks by default. It decides which other lenses are worth hearing from on this piece of work.

## How lenses differ from role agents

[Role agents](../agents/README.md) do a task. A business analyst writes the acceptance card; a QA lead runs checks and issues a verdict. Each has tools, an output and a Claims block.

A lens does not do a task. It comments. It has no tools of its own and produces no file. Its comment is an opinion about work someone else did.

## How to size use

- Small work: one lens, usually the lead, or none at all.
- Substantial work: two to four lenses, chosen for the risk. A customer-facing price change might get customer, commercial and voice-of-reason, with the lead to close.
- Do not use all seven on everything. More lenses make a longer reply, not a better one.

## What a lens is not

Lens commentary is not evidence that another agent ran. If the sceptic lens says "the figure is unsourced", that is one perspective from the same model that did the work. It is a prompt to check, and it does not replace an independent review by a separate agent or person where the risk calls for one. Agreement among lenses is not authority; only the named owner approves.

A lens also does not decide anything that belongs to the owner. It cannot approve a send, spend, deletion, deployment or publication.

## Making them yours

The lens files are neutral. If you would rather hear them as characters, map your own onto the lenses with [the cast template](cast-template.md). There is a complete invented cast in [the cast example](cast-example.md). Characters change tone; they never change facts, and "lenses off" turns them off.
