---
name: route-the-work
description: "Writes a one-line route (asset, job, risk, reader, route, proof) and chooses who does the work: direct, a skill, a role agent or a reviewer. Use when starting any task others will rely on."
---

# Route the work

Decide how the work will be done before doing it. A one-line route stops small jobs getting heavy process and stops risky jobs getting none.

**Stage:** Operate (any stage may use it). **Rules:** 1 Stop at the boundaries; 4 Claim only what you can show. Detail: `rules/01-route-the-work.md` (in the SHOTos repository, or `.shotos/rules/01-route-the-work.md` where SHOTos is installed) and `rules/02-evidence-based-risk.md` (in the SHOTos repository, or `.shotos/rules/02-evidence-based-risk.md` where SHOTos is installed).

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
   - **A skill:** use the matching skill when one exists, for example [agree-acceptance](../agree-acceptance/README.md) before building or [eval-set](../eval-set/README.md) for varying output.
   - **A role agent:** a separate agent with a narrow job and limited access, for work that needs a distinct role, such as testing or security review.
   - **An independent reviewer:** a second agent from a different model or runtime, for medium and high risk. See [cross-agent-review](../cross-agent-review/README.md).
   - When two routes fit, take the lighter one and say what would make you move to the heavier one.
3. **Add a risk tag only when evidence triggers it.** Look at the asset, the data and the action. Add a tag when you can point to the evidence: `personal-data` (the files contain names, health or children's records), `money` (the action spends, refunds or invoices), `external` (it goes to people outside the team), `irreversible` (it deletes, overwrites or publishes), `legal` (a contract, a regulatory claim). Write the evidence beside the tag. Do not add a tag because the topic sounds serious.
4. **Raise the route when a tag appears.** One tag usually needs a named human decision before the action; two or more, or `irreversible` with `external`, need an independent reviewer as well.
5. **Name the stop point.** Say the first action that needs the owner's yes. Sending, posting, spending, deleting, deploying and publishing always do.
6. **Show the line to the person** if the route is anything other than direct, and wait for a change or a yes.
7. **Revisit the line** if what you find while working changes the risk. Say so and re-route; do not carry on under the old line.

## Output

One line in the reply or saved with the work, for example at the top of `.work/<task>/route.md`. [template.md](template.md) holds the line and the tag table.

## Checks

- All six parts are filled in.
- Each risk tag has evidence next to it, and no tag is there without evidence.
- The route is the lightest one that fits the risk, with a stated trigger for a heavier one.
- The first action that needs the owner's yes is named.
