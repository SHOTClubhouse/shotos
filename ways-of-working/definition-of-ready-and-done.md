# Definition of ready and definition of done

## What it is

A **definition of ready** is the short list of things that must be true before work starts. A **definition of done** is the list of checks that must pass before work counts as finished. Both are agreed by the team and written down, so nobody argues about them halfway through. The idea comes from agile and Scrum practice; the Scrum Guide treats a definition of done as a shared commitment to quality.

SHOTos uses both. The definition of ready sits at the start of Operate. The definition of done is what the acceptance checks of [rule 2](../rules/05-acceptance-first.md) are measured against.

## Why it matters with agents in the loop

Agents start fast. If nobody has said what "ready" means, they begin on a vague request and produce a confident answer to the wrong question. If nobody has said what "done" means, the agent decides, and it usually decides when the output looks finished. Looking finished is not the same as being checked.

A written definition of done also gives the agent something to read back against ([rule 3](../rules/06-read-back.md)) and gives the reviewer something to check that is not the agent's own opinion.

## The practice, step by step

1. **Write a short definition of ready** and keep it to one screen.
2. **Write a definition of done per type of output**, since a slide deck and a code change do not finish the same way.
3. **Attach both to the task** before starting, in the acceptance card or the task record.
4. **Have the owner confirm** them. A named person, not "the team".
5. **At the end, check against the list**, tick each item with the evidence, and say which items were not checked.
6. **Review the lists** every few weeks. Add a check when something slipped through; remove one that never finds anything.

## Definition of ready

Work is ready to start when:

- There is a named owner who will accept it.
- The outcome is stated in one sentence, with no solution inside it.
- The reader or user is named, and what they will do with the output.
- The examples or checks are agreed, including at least one that should fail. See [specification-by-example.md](specification-by-example.md).
- The inputs exist and are reachable: the data, the access, the source material.
- The boundaries are written: what the agent may not send, spend, delete, publish or change without a yes.
- Open questions are answered, or recorded as open with a named person to answer them.
- The work is small enough to finish in one sitting, or has been split.

If one of these is missing, the next step is to supply it, not to start anyway.

## Definition of done by type of output

Every type shares three checks: **the acceptance checks pass, the result was read back in its real home, and the claims in the report are backed by evidence.** Beyond those, each type has its own.

### Written document

- The reader and purpose are in the first paragraph.
- Every figure, date and name was checked against its source.
- The document opens and prints in the format it will be used in; headings and numbering are correct.
- Terms are used the same way throughout.
- Someone other than the author has read it start to finish.

### Slide deck

- Open the finished file and view every slide as rendered, not only the outline.
- No text overflows, overlaps or runs off a slide; images are sharp and in proportion.
- Each slide makes one point; the order tells a story without the speaker.
- Numbers on slides match the source; sources are noted.
- It opens in the tool the audience will use, with fonts that exist there.

### Email or message

- The recipient list is correct and was confirmed by the owner.
- The first sentence says what the reader needs to know or do.
- Names, dates, amounts and links were checked.
- Nothing is in it that the sender would not say aloud to the reader.
- It is a draft until a named person approves sending.

### Code change

- Tests for the change exist, and were seen to fail before the change and pass after.
- The full test suite passes in the pipeline, not only on one machine.
- Another person, or an independent reviewer, has read the diff.
- Security checks, secrets scans and dependency checks are clean or the findings are recorded.
- Logging or monitoring will show if it misbehaves; there is a way to undo it.
- It runs in the real or staging environment, not only in a test harness.

### Data or analysis

- The source and date of the data are stated.
- Counts reconcile: rows in equal rows out, with exclusions explained.
- A second method or a spot check by hand agrees with the result on a sample.
- Assumptions and limits are written beside the result.
- Charts show the axis, units and sample size.
- Nothing personal is in the output that the reader should not see.

### Image

- Open the file and look at it at the size it will be shown.
- Subject, text, spelling and proportions are right; any lettering is legible.
- It has the rights and licence needed for the use, and sources are recorded.
- It exports in the format and dimensions the destination needs.
- It does not contain anything the owner did not approve, such as a real person's face or a logo.

### Video

- Watch it from start to end at normal speed with sound.
- Captions or subtitles exist and match the audio.
- Music, footage and voices are licensed or owned; the credits are accurate.
- It plays on the platform and device it will be used on.
- Facts spoken or shown were checked.

### Automation or script

- It ran on a small sample first, with the output inspected by a person. See [records-and-filing.md](records-and-filing.md) for keeping the evidence.
- It can be run in a safe "dry" mode that shows what it would do without doing it.
- It stops on error instead of continuing silently.
- Anything it deletes, sends or spends is behind an owner's yes.
- The schedule, the account it runs as and who gets alerts are written down.
- There is a documented way to switch it off.

### Customer handoff

- The recipient has what they need to run it without the builder: how to use it, how to get help, who owns it now.
- Open issues and known limits are listed in plain words.
- Access has been granted and tested by the recipient.
- The handoff record shows what was checked and what was not. See the [evidence-handoff skill](../skills/evidence-handoff/README.md) and the [handoff template](../templates/handoff.md).
- The customer's owner has accepted in writing.

### Anything published

For every output that goes to a public or shared place: **read it back in its real home.** Open the published page, the sent message in the recipient's view, the shared folder as the audience sees it. A file that looks right on your machine can be wrong where it lives.

## What good looks like

- The lists are short, specific and used. A list nobody reads is decoration.
- The agent quotes the list in its final report and says which items it checked and which it could not.
- When something slips through, the list changes.

## Anti-patterns

- **A generic checklist** pasted on every task regardless of type.
- **Done means merged,** or sent, with no read-back.
- **The agent marks itself done.** Acceptance belongs to a person.
- **Ready means the ticket exists.** A title is not a specification.
- **Gold-plating.** Checks added until nothing ever finishes. Keep to the risk.

## How it maps to the stages and rules

- **Scope** ends with an agreed definition of ready and done.
- **Hypothesise** turns done into examples.
- **Operate** works to them; **Track** reports against them.
- **Rules 2, 3 and 4:** agreed first, checked on the real result, claimed only with evidence.

## A short example

Harbourside Lettings asks an agent to produce a six-slide deck for a landlord meeting. The definition of ready is not met: the owner is named but the audience is not. The agent asks, learns it is five landlords who care about void periods, and writes that down. At the end, the agent exports the deck, opens each slide as an image, finds that slide four's chart label is cut off, fixes it, checks the figures against the lettings report and tells the owner which of the checks it ran. The owner opens the deck in the meeting software on the real laptop before accepting.

## Further reading

- Ken Schwaber and Jeff Sutherland, *The Scrum Guide*.
- Mike Cohn, *User Stories Applied*.
- Gojko Adzic, *Specification by Example*.
- Jez Humble and David Farley, *Continuous Delivery*.
