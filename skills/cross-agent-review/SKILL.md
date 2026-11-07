---
name: cross-agent-review
description: Pairs a lead agent with an independent reviewer from a different model, both given the same acceptance card and evidence. Use when work is medium or high risk or leaves the team. The owner decides.
---

# Cross-agent review

One agent reviewing its own work is a second look by the same eyes. A reviewer from a different model or runtime has different habits and blind spots, so it catches different things. Use one when the risk justifies the cost.

**Stage:** Operate. **Rules:** 3 Read back the real result; 4 Claim only what you can show. Detail: `rules/07-independent-review.md` (in the SHOTos repository, or `.shotos/rules/07-independent-review.md` where SHOTos is installed).

## Context and handoff

Give the reviewer the same acceptance and the exact artefact revision. Limit the evidence packet to sources and fields the reviewer is authorised to access. State whether another agent really ran and record disagreements.

Use `decision-record` when findings need a decision. Save both assessments and the final disposition together.

## When not to use this

Skip it for low-risk, easily reversed work. A second agent costs time and money, and a review of a trivial change teaches nothing. Do not use it as a substitute for the owner's decision.

## Steps

1. **Check the risk calls for it.** Use the route from `route-the-work`. Medium risk or above, or any `external`, `money`, `personal-data`, `legal` or `irreversible` tag, means yes. If the route is low risk, say why a review is not needed.
2. **Choose the reviewer from a different model or runtime.** For example, if the lead is Claude Code, the reviewer is Codex, or the reverse; or a different model through the same tool. Same model with a fresh session is better than none, but say it is weaker. Say which is which in the record.
3. **Prepare one approved packet for both roles.** It holds:
   - the acceptance card (`agree-acceptance`), unchanged;
   - the evidence: the exact output revision, the relevant input slices, results and source references. If an approved extract or aggregate leaves a check unverified, record the gap and route it to a reviewer who already has the necessary access;
   - the boundaries: what neither agent may do (no sending, spending, deleting, deploying or publishing).
4. **Keep the reviewer independent.** Do not tell the reviewer the lead's conclusion, or which parts the lead is unsure about, until its first report is in. Give the reviewer read-only access unless the owner has agreed otherwise.
5. **Ask the reviewer for findings with evidence.** Each finding has: what is wrong, where (file, line, record, quote), the check it fails, and how to verify it. A feeling that something looks off is a question, not a finding. The reviewer also lists what it checked and found fine, and what it could not check.
6. **The lead responds to each finding:** accept and fix, dispute with evidence, or pass to the owner. The lead does not delete findings. Disputes go to the owner with both sides.
7. **Read back after fixes.** Re-check the fixed items in their real home. The reviewer looks again at the changed revision and the checks it affects. Record which revision each result covers.
8. **The owner decides.** Both agents agreeing is not authority, and neither is a clean review. Report to the owner: what was reviewed, by whom, findings and outcomes, disagreements, what was not checked, and a recommendation. The owner's yes or no is recorded. Name both roles and state what each actually received and checked. Record any required review still pending. Use the [restricted review example](restricted-review-example.md).
9. **Record it.** Use [template.md](template.md) with the work, for example `.work/<task>/review.md`.

## Output

A review record on [template.md](template.md).

## Checks

- Lead and reviewer differ in model or runtime, or the weaker case is stated.
- Both had the same acceptance card and a shared approved packet. The record names checks that needed additional evidence and who could verify them.
- Each finding has evidence and a way to verify it.
- Disagreements are reported, not smoothed.
- The record says what was not checked, and the owner's decision is written down.
