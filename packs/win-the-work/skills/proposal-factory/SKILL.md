---
name: proposal-factory
description: Produces many tailored proposals from one master plus per-reader variables, with a three-item pilot, claim checks and rendered inspection. Use when five or more similar proposals are needed and one-off-or-factory has approved a factory. Never sends.
---

# Proposal factory

Make many proposals that each read as written for their reader, without copying one proposal many times, and without sending any of them.

Stage: Operate. Rules served: 3 (read back the real result), 4 (claim only what you can show) and 1 (nothing is sent). Applies control 9, pilot before scale (`rules/09-pilot-before-scale.md` (in the SHOTos repository, or `.shotos/rules/09-pilot-before-scale.md` where SHOTos is installed)).

## Context and handoff

Read the approved reusable master, segment rules, buyer-specific sources and any existing batch record. Include a varied pilot with a missing or contradictory field.

Use `contextual-proposal` for exceptions that need judgement. Save every variant against its originating deal, record the pilot decision there, and keep the price basis and approvals per deal.

## When not to use this

Skip it for fewer than five items, for proposals that differ in substance rather than in reader detail, or when `one-off-or-factory` has not recommended a factory. Then use `contextual-proposal` for each one.

## Steps

1. **Confirm the decision.** Read the decision record from `one-off-or-factory`. If none exists, or it says author directly, stop and run that skill first. Take the three pilot items, their accepted outputs and the accepted revision of each from it. If the decision record lacks the owner's acceptance or the accepted outputs, stop and ask the owner; do not rerun the pilot to fill the gap. A direct-authoring decision is a stop, not a prompt to rerun until the factory wins.
2. **Build a reusable master.** Extract the approved blocks and reusable assets from an accepted proposal. Remove the earlier buyer's data, quotes, pricing exceptions, metadata and imagery unless the owner approves their use for this segment. Give the master a revision. Compare it with the master the accepted pilot outputs were made from. If it is the same revision, or differs only in ways that touch no pilot item, keep the accepted outputs. If the master differs, or the owner has not confirmed it, record the difference and take it to the owner in step 5. Fixed claims must apply to every buyer in scope. Keep recipient-specific terms and evidence in each deal.
3. **Define the variables.** For each: name, where it appears, where its value comes from, and the check on it. Typical: reader name and role, organisation name, their stated priority, the opening problem in their words, the local evidence, the price basis, the next step. A variable with no source for a given reader is left empty and flagged, never invented.
4. **Collect reader data.** Use one row per deal or prospect ID, with each value, source, source revision and status. Research the facts that change the proposal. Hold an item if a required value or approval is missing, including permission for a buyer-specific asset.
5. **Confirm the pilot of three.** Reuse the three items from the decision record, including the least typical, and add a reader only if one is missing or contradictory. Do not run a second pilot. For each item, match its accepted output to the deal ID, master revision, source revision and agreed acceptance. Where all four still match, keep the accepted output and its review status. Produce, check and render again only an item whose master, relevant source or agreed acceptance changed, or that has no accepted output, and have the owner accept or reject it and note edits. Fix the master or the variable list from what any edits show; if that changes the master, recheck the items it touches. Do not run the rest until all three are accepted at the owner-confirmed master revision. Stop if acceptance or evidence for a pilot item is missing, or the owner has not signed off the master revision.
6. **Run the batch** in groups after the owner confirms the exact pilot and master. On a restart, match each output to the deal ID, master revision and approved input revision. Reuse checked results that still match and carry forward their current review status. A checked draft can remain ready for owner review. Flag changed or owner-edited outputs and create a separate revision for affected drafts. Reopen approval if the reusable terms or scope changed. See the [restart example](restart-example.md).
7. **Check every item.** Per item: claim ledger lines for the variable parts (new claims only), asset register lines for any reader-specific image, names and numbers checked against the reader sheet, no leftover placeholders from other readers, no copied sentence that mentions another organisation, and a rendered look at every page or slide.
8. **Write the batch report** using [template.md](template.md): per item, status (draft, ready for review, rejected), open flags and what was edited; totals; time spent against the decision record's estimate.
9. **Stop.** Nothing is sent. The report lists items ready for review and the owner decides which to send.

## Output

The master, the reader sheet, one file per reader and the batch report. Save under the project, for example `.work/proposal-factory/`.

## Checks

- A decision record and an owner-accepted pilot of three exist before the batch; the pilot was reused, not repeated.
- Only pilot items whose master, relevant source or acceptance changed were redone, and the reason is recorded.
- Every variable value has a source and status; unknown values are blank and flagged.
- No item contains another reader's information, in copy, assets, metadata or the rendered file.
- Each output and review belongs to the same deal, master revision and input revision.
- Every item was rendered and every page or slide looked at.
- The batch report separates ready for review from rejected and says that nothing was sent.
