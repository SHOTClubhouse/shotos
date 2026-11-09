---
name: route-the-work
description: "Writes a one-line route (asset, job, risk, reader, route, proof) and chooses who does the work: direct, a skill, a role agent or a reviewer. Use when starting any task others will rely on."
---

# Route the work

Decide how the work will be done before doing it. A one-line route stops small jobs getting heavy process and stops risky jobs getting none.

**Stage:** Operate (any stage may use it). **Rules:** 1 Stop at the boundaries; 4 Claim only what you can show. Detail: `rules/01-route-the-work.md` (in the SHOTos repository, or `.shotos/rules/01-route-the-work.md` where SHOTos is installed) and `rules/02-evidence-based-risk.md` (in the SHOTos repository, or `.shotos/rules/02-evidence-based-risk.md` where SHOTos is installed).

## Context and handoff

- **Business question:** how much care does this task need, and who should do and check it?
- **Use this when** starting any task others will rely on. It chooses the way of working; it does not define acceptance (`agree-acceptance`) or the behaviour (`example-mapping`).
- **Minimum context:** the requested outcome, the actual asset, the owner, the reader and the proof needed. Choose the shortest route with sufficient evidence.
- **Decision boundary:** the owner decides at the first send, spend, delete, deploy or publish. Authorised independent work carries on while a decision is pending.
- **Next step:** `agree-acceptance` for material work. With only this skill installed, use the steps and template below and record any missing review capability. Record the route in the owning task so the next session can use it.

## When not to use this

Skip it for a quick factual answer or a trivial edit the person will see at once. Write the line silently there and move on.

## Steps

1. **Write the route on one line** before starting:

   `Asset: ... | Job: ... | Risk: ... | Reader: ... | Route: ... | Proof: ...`

   - **Asset:** the thing being made or changed, and where it lives (file, record, system).
   - **Job:** what has to be true afterwards, in one clause.
   - **Risk:** low, medium or high, with the evidence-based tag (step 3).
   - **Reader:** who will rely on it, and what they will do with it.
   - **Route:** who or what does the work (step 2).
   - **Proof:** how the result will be checked in its real home.
2. **Choose the route, sized to the risk.**
   - **Direct:** the agent does it and shows the result. For low-risk, easily reversed work with one reader who will see it.
   - **A skill:** use the matching skill when one exists, for example `agree-acceptance` before building or `eval-set` for varying output.
   - **A role agent:** a separate agent with a narrow job and limited access, for work that needs a distinct role, such as testing or security review.
   - **An independent reviewer:** a qualified person who did not produce the work, or a second agent on a different model or runtime for the checks it can perform. Where independent review is required and unavailable, leave acceptance or the dependent action pending. See `cross-agent-review`.
   - When two routes fit, take the lighter one and say what would make you move to the heavier one.
3. **Add a risk tag only when evidence triggers it.** Look at the asset, the data and the action. Add a tag when you can point to the evidence: the eight tags in the table in `rules/02-evidence-based-risk.md`, which is the source: `personal-data`, `special-category`, `children`, `money`, `external`, `irreversible`, `secret` and `consequential`. Write the evidence beside the tag. Do not add a tag because the topic sounds serious.
4. **Raise the route when a tag appears.** One tag usually needs a named human decision before the action; two or more, or `irreversible` with `external`, need an independent reviewer as well.
5. **Name the stop point.** Say the first action that needs the owner's yes. Sending, posting, spending, deleting, deploying and publishing always do.
6. **Record the route and start the authorised work.** Surface the route when it affects the reader, proof or plan. Use the owner's request and any recorded approvals to identify what can start. Pause only the step with an unresolved decision, review or boundary approval, and complete independent authorised work while it is pending. See the [routing example](authorised-work-example.md).
7. **Revisit the line** if what you find while working changes the risk. Say so and re-route; do not carry on under the old line.

## Output

One line in the reply or saved with the work, for example at the top of `.work/<task>/route.md`. [template.md](template.md) holds the line and the tag table.

## Checks

- All six parts are filled in.
- Each risk tag has evidence next to it, and no tag is there without evidence.
- The route is the lightest one that fits the risk, with a stated trigger for a heavier one.
- The route names the first action still awaiting approval, if any, and the authorised work that can proceed.
