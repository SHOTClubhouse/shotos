---
name: proposal-factory
description: Produces many tailored proposals from one master plus per-reader variables, with a three-item pilot, claim checks and rendered inspection. Use when five or more similar proposals are needed and one-off-or-factory has approved a factory. Never sends.
---

# Proposal factory

Make many proposals that each read as written for their reader, without copying one proposal many times, and without sending any of them.

Stage: Operate. Rules served: 3 (read back the real result), 4 (claim only what you can show) and 1 (nothing is sent). Applies control 9, pilot before scale (`rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed)).

## Context and handoff

Read the approved master, segment rules and buyer-specific sources. Include a varied pilot with a missing or contradictory field.

Use `contextual-proposal` for exceptions that need judgement. Save every variant against its originating deal and record the pilot decision.

## When not to use this

Skip it for fewer than five items, for proposals that differ in substance rather than in reader detail, or when `one-off-or-factory` has not recommended a factory. Then use `contextual-proposal` for each one.

## Steps

1. **Confirm the decision.** Ask for the decision record from `one-off-or-factory`. If none exists, run that skill first.
2. **Build the master.** One accepted proposal (from `contextual-proposal`) with every reader-specific part marked as a variable. Fixed parts are claims and assets already ledgered and accepted.
3. **Define the variables.** For each: name, where it appears, where its value comes from, and the check on it. Typical: reader name and role, organisation name, their stated priority, the opening problem in their words, the local evidence, the price basis, the next step. A variable with no source for a given reader is left empty and flagged, never invented.
4. **Collect reader data.** One row per reader in a sheet: each variable's value, its source and its status (confirmed, reported, inferred, unknown). Research per reader as in `contextual-proposal` but shorter.
5. **Run a pilot of three.** Pick three readers, including the least typical. Produce, check and render all three. The owner accepts or rejects each and notes edits. Fix the master or the variable list from what the edits show. Do not run the rest until the three pass.
6. **Run the batch** in groups, not all at once, after the owner confirms the pilot.
7. **Check every item.** Per item: claim ledger lines for the variable parts (new claims only), asset register lines for any reader-specific image, names and numbers checked against the reader sheet, no leftover placeholders from other readers, no copied sentence that mentions another organisation, and a rendered look at every page or slide.
8. **Write the batch report** using [template.md](template.md): per item, status (draft, ready for review, rejected), open flags and what was edited; totals; time spent against the decision record's estimate.
9. **Stop.** Nothing is sent. The report lists items ready for review and the owner decides which to send.

## Output

The master, the reader sheet, one file per reader and the batch report. Save under the project, for example `.work/proposal-factory/`.

## Checks

- A decision record and a passed pilot of three exist before the batch.
- Every variable value has a source and status; unknown values are blank and flagged.
- No item contains another reader's name, number or phrase.
- Every item was rendered and every page or slide looked at.
- The batch report separates ready for review from rejected and says that nothing was sent.
