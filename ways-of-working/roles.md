# Roles: analyst, designer, engineer and QA

## What it is

Four responsibilities recur in almost every piece of work that someone will rely on: understanding the need (business analysis), shaping how it is used (UX design), building it (engineering) and checking it (quality assurance). SHOTos treats these as **responsibilities, not headcount.** In a large organisation they may be four teams. In a team of three, one person may carry two or three of them in a single afternoon. In a solo founder's week, one person carries all four, and the useful discipline is to wear one hat at a time.

This page says what each responsibility owns, what it checks before handing on, and what changes when an agent does part of it.

## Why it matters with agents in the loop

An agent can do all four jobs in one sitting, so the handoffs between them quietly disappear. The same session that understood the need also designed, built and checked the result, and its checking is shaped by its building. That is the author marking their own work. Keeping the roles distinct, even when one session or one person fills several, restores the checks that handoffs used to provide.

It also helps with briefing. "Act as the analyst, then stop" gives an agent a bounded job and a clear exit. The access levels in [control 3](../rules/03-mode-contract.md) follow the same idea: an agent briefed to read and propose does not change anything, one briefed to change the project stays inside it, and none of them accepts its own output.

## The business analyst responsibility

**Owns:** the problem statement, the users and decision-makers, the scope and its boundaries, the baseline measures, and the acceptance examples.

**Checks before handing on:**

- The problem is stated without a solution inside it.
- The user and the person who accepts are both named.
- What is out of scope is written down.
- The examples include at least one that should fail. See [specification-by-example.md](specification-by-example.md).
- Open questions have a named person to answer them.
- The baseline exists, or is recorded as not measured.

**Typical outputs:** a problem statement, an example map, an acceptance card.

## The UX designer responsibility

**Owns:** how a person will meet the thing: the flow, the wording, the layout, the states when something goes wrong, and access for people with different needs. UX here means the whole experience of use, whether the thing is a screen, a form, a letter or a process.

**Checks before handing on:**

- The main task can be done by the intended user without help, as shown by watching a real person or a close stand-in try it.
- Empty, loading, error and "no permission" states are designed, not left blank.
- Wording uses the user's own terms and is plain.
- Text is legible, colour is not the only signal, and it works with a keyboard and a screen reader.
- It works at the sizes and on the devices people actually use.
- Nothing asks for data it does not need.

**Typical outputs:** a flow sketch, a prototype or mock-up, wording, a list of states.

## The engineer responsibility

**Owns:** building the thing to the agreed examples, in small changes, with tests, and keeping it understandable and secure. See [engineering-excellence.md](engineering-excellence.md).

**Checks before handing on:**

- Tests exist for every agreed example, and were seen to fail before the change and pass after.
- The change is small enough to review and does only what was asked.
- The pipeline is green, including security checks and, where output varies, evals.
- No secret, personal data or credential has been added to the repository or the logs.
- It runs in a real or staging environment and can be undone.
- Notes for the next person: what changed, why, and what is not done.

**Typical outputs:** a small change with tests, a release note, a runbook entry.

## The QA responsibility

**Owns:** the independent view of whether the work meets the agreed acceptance and survives the cases nobody listed. QA is not only testing at the end; it begins in the example conversation, where the tester asks "how will we know?".

**Checks before handing on:**

- Every acceptance example was run against the real result, and the evidence is recorded.
- The case that should fail does fail in the right way.
- Exploratory testing was done: odd inputs, wrong order, missing data, a slow connection, a user who does not read.
- Regression: what used to work still does.
- The report says what was tested and what was not, in plain words.
- Defects are reported with steps to reproduce, not only a complaint.

**Typical outputs:** a test report, a list of defects, a go or no-go recommendation. The recommendation goes to the owner. QA does not accept on the owner's behalf.

## When one person carries several roles

- **Say which hat is on.** At the top of a working session, name the role. When you change, say so.
- **Separate the hats in time.** Do the analysis, take a break or switch task, then come back to check with a different hat. A fresh read finds more than a continuous one.
- **Keep one independent check** for anything that matters. The author cannot be the only reader. Use a colleague or an independent session given only the acceptance and the result. See [control 7](../rules/07-independent-review.md).
- **Size the checks to the risk.** A typo fix does not need four roles. A change to payments does.
- **Write down who held which role** on the task record so the next person knows what was checked and by whom.

## Briefing an agent in a role

A good brief for a role includes the responsibility, the inputs it may use, the output it must produce, the point where it stops and the thing it must not do. For example: "Act as the analyst. Read the attached interview notes. Produce a problem statement and five acceptance examples, one of which should fail. Do not propose a solution. Stop and wait for the owner." That is a bounded job with a handoff.

## What good looks like

- The need, the experience, the build and the check each have a named holder on each piece of work, even when it is the same person.
- Handoffs carry written evidence, not "it should be fine".
- The tester sees the examples before the code is written.
- Someone other than the builder has looked at the result.

## Anti-patterns

- **Role as job title,** so work sits waiting until "the analyst" is free.
- **QA as a gate at the very end,** where fixes are most expensive.
- **The builder is the only tester.**
- **An agent playing all four roles in one pass** and reporting a single confident summary.
- **Design as decoration,** added after the build.
- **Analysis as paperwork,** written once and never read.

## How it maps to the steps and rules

- **Brief:** mainly the analyst and designer responsibilities.
- **Build:** engineer and QA, with the designer checking the live experience.
- **Check:** analyst and QA, comparing with the baseline.
- **Hand over:** all four are handed to the receiving team, who may combine them.
- **Rule 2:** the analyst's examples are the acceptance.
- **Rule 3:** the engineer and QA read back the real result.
- **Control 7:** QA is the independent view sized to the risk.

## A short example

Millbrook Rovers wants a form for parents to sign up for a holiday camp. Priya (an invented volunteer) is the only person on the project. In the morning she wears the analyst hat and writes the problem, the five examples and the one that should fail: a sign-up with no emergency contact is refused. After lunch she wears the designer hat and sketches the form on paper, then asks a parent to try it, which shows the "allergies" box is missed. In the afternoon she asks an agent, as engineer, to build the form to the examples. The next day she uses the QA hat with a fresh view: she runs each example against the live form, tries the form on a phone and on a slow connection, and finds a date field that accepts a past date. She records what she tested, fixes the date field and asks the club chair to accept.

## Further reading

- *A Guide to the Business Analysis Body of Knowledge (BABOK Guide)*, International Institute of Business Analysis.
- Alan Cooper and others, *About Face*.
- Don Norman, *The Design of Everyday Things*.
- Lisa Crispin and Janet Gregory, *Agile Testing*.
- Elisabeth Hendrickson, *Explore It!*.
- Gojko Adzic, *Specification by Example*.
