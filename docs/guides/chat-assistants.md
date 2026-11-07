# Use SHOTos in ChatGPT or Claude without a terminal

Start with one skill and a fictional example. You can download, unpack and add the files with a browser and file manager on Windows or Mac.

The walkthrough below uses Decision Brief. To try a different job, pick its ZIP from the [first-job guide](../running-it.md#choose-your-first-job) and substitute its skill name in the setup steps. For a file-based chat, use its `SKILL.md`, relevant template and example input. Then use the [sample prompt and review checks](../running-it.md#run-the-sample-from-your-zip).

## Claude with Skills enabled

1. [Download `decision-brief.zip`](https://github.com/SHOTClubhouse/shotos/releases/latest/download/decision-brief.zip). Keep the ZIP intact for this route.
2. Open **Customize → Skills**, choose **+ → Create skill → Upload a skill**, then select the ZIP and enable the skill. If the menu is unavailable, check the workspace settings for skills and file creation, or use the file route below.
3. Start a fresh chat and ask Claude to use Decision Brief and its bundled `template.md` and `review-cycle.md`. Follow the two prompts below and check which scenario files and evidence IDs it cites. [Official Claude instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## ChatGPT Projects, or a Claude chat using files

1. Download the same ZIP. Use **Extract All** in Windows File Explorer or double-click it in Mac Finder.
2. Add `SKILL.md`, `template.md` and `review-cycle.md` to a ChatGPT Project or attach them directly to a fresh chat. In ChatGPT desktop, use **+ → Add photos & files**. Check the attachments before sending. If some are missing, open the picker again and add those files separately.
3. Follow the two prompts below. For a reusable project, you can also add the [working agreement](../../templates/AGENTS.md) to the project instructions. The same file approach works in a Claude Project or chat. If your app cannot upload Markdown, paste the relevant text or attach it as a text file.

## Run the retail scenario

For the first message, attach or paste the [initial evidence](../../packs/exec-ops/skills/decision-brief/scenarios/retail-trial-initial.md) as the only scenario input. If you installed the skill, ask it to open `scenarios/retail-trial-initial.md` and limit its reads to that file and the skill instructions and templates.

> Use Decision Brief. Draft a one-page decision brief from retail-trial-initial.md (R1–R3). Cite the records and keep decision and handoff status tied to the evidence available now. Wait for the follow-up.

Once you have the brief, attach or paste the [follow-up records](../../packs/exec-ops/skills/decision-brief/scenarios/retail-trial-follow-up.md), or ask it to open the installed `scenarios/retail-trial-follow-up.md`.

> Read retail-trial-follow-up.md (R4–R6). Update the decision, handoff and independent-cycle statuses. Cite the record that supports each update.

Keep the worked answer for your own review. If your ZIP contains only the original combined scenario, use the two linked input files above.

A ChatGPT Project uses the files as context. Some eligible ChatGPT workspace agents also offer **Add skill** in the agent builder. Use that native option where your workspace allows it, and verify that the agent can open the scenario before relying on it. [ChatGPT Projects](https://learn.chatgpt.com/docs/projects) · [Workspace agent skill setup](https://developers.openai.com/cookbook/articles/chatgpt-agents-sales-meeting-prep#3-enabling-skills-and-memories-for-consistent-customized-outputs)

## Check your first result

Look for a named decider, dated evidence, an explicit decision and a handoff state that matches its receipt. If the assistant cannot see a supporting file, give it that file and repeat the check. A file upload provides instructions and examples. Tools, connectors and approval settings depend on the workspace.

For the retail example, R1–R3 support a conditional recommendation to extend the trial to one evening site, subject to a local baseline and existing staffing. R4 records the conditional approval, R5 records the receiving lead's acceptance, and R6 records a later decision to stop at that site after overtime rose. The independent cycle passes because the receiving operator ran the review without help from the original operator and the director accepted the review record. Wider rollout remains unauthorised.

## Try a bank or startup decision

Use the same setup in a fresh chat. Open the initial evidence first. After you have the brief, add the follow-up records. Open the worked answer yourself to check the result.

### Bank operations

1. Attach or open the [initial evidence](../../packs/exec-ops/skills/decision-brief/scenarios/bank-remediation-initial.md). Ask for the closure options and what evidence the service owner would need.
2. Add the [follow-up records](../../packs/exec-ops/skills/decision-brief/scenarios/bank-remediation-follow-up.md). Ask whether the closure request changes the decision, handoff or independent-cycle status.
3. Compare with the [worked bank review](../../packs/exec-ops/skills/decision-brief/scenarios/bank-remediation.md).

### Startup proposal

1. Attach or open the [initial evidence](../../packs/exec-ops/skills/decision-brief/scenarios/startup-proposal-initial.md). Ask for the founder's decision brief, one buyer-facing sentence and the corresponding private working-sheet entry.
2. Add the [follow-up records](../../packs/exec-ops/skills/decision-brief/scenarios/startup-proposal-follow-up.md). Ask what the founder authorised, what the operator accepted and whether the next review was independent.
3. Compare with the [worked startup review](../../packs/exec-ops/skills/decision-brief/scenarios/startup-proposal.md).
