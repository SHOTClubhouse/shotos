---
name: cross-agent-review
description: Pairs lead and independent reviewer from different models with the same acceptance card and evidence. Use for risky or external work. Their agreement is not approval; name the actual owner who can authorise a send.
---

# Cross-agent review

One agent reviewing its own work is a second look by the same eyes. A reviewer from a different model or runtime has different habits and blind spots, so it catches different things. Use one when the risk justifies the cost.

**Step:** Build. **Rules:** 3 Read back the real result; 4 Claim only what you can show. Detail: `rules/07-independent-review.md` (in the SHOTos repository, or `.shotos/rules/07-independent-review.md` where SHOTos is installed).

## When not to use this

Skip it for low-risk, easily reversed work. A second agent costs time and money, and a review of a trivial change teaches nothing. Do not use it as a substitute for the owner's decision.

## Steps

1. **Check the risk calls for it.** Use the route from [route-the-work](../route-the-work/README.md). Medium risk or above, or any `external`, `money`, `personal-data`, `legal` or `irreversible` tag, means yes. If the route is low risk, say why a review is not needed.
2. **Choose the reviewer from a different model or runtime.** For example, if the lead is Claude Code, the reviewer is Codex, or the reverse; or a different model through the same tool. Same model with a fresh session is better than none, but say it is weaker. Say which is which in the record.
3. **Prepare one packet for both agents.** It holds:
   - the acceptance card ([agree-acceptance](../agree-acceptance/README.md)), unchanged;
   - the evidence: the real output, the inputs, test results, links or file paths;
   - the boundaries: what neither agent may do (no sending, spending, deleting, deploying or publishing).
4. **Keep the reviewer independent.** Do not tell the reviewer the lead's conclusion, or which parts the lead is unsure about, until its first report is in. Give the reviewer read-only access unless the owner has agreed otherwise.
5. **Ask the reviewer for findings with evidence.** Each finding has: what is wrong, where (file, line, record, quote), the check it fails, and how to verify it. A feeling that something looks off is a question, not a finding. The reviewer also lists what it checked and found fine, and what it could not check.
6. **The lead responds to each finding:** accept and fix, dispute with evidence, or pass to the owner. The lead does not delete findings. Disputes go to the owner with both sides.
7. **Read back after fixes.** Re-check the fixed items in their real home. The reviewer looks again at what changed.
8. **The owner decides.** Both agents agreeing is not authority, and neither is a clean review. Name the actual decision owner; if unknown, say "owner not identified" and do not send. Report to the owner: what was reviewed, by whom, findings and outcomes, disagreements, what was not checked, and a recommendation. The owner's yes or no is recorded. Say in the report that both agents got the same acceptance card and the same evidence, and name them.
9. **Record it.** Use [template.md](template.md) with the work, for example `.work/<task>/review.md`.

## Output

A review record on [template.md](template.md).

## Checks

- Lead and reviewer differ in model or runtime, or the weaker case is stated.
- Both had the same acceptance card and evidence.
- Each finding has evidence and a way to verify it.
- Disagreements are reported, not smoothed.
- The record says what was not checked, and the owner's decision is written down.
