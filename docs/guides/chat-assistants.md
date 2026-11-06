# Use SHOTos in ChatGPT or Claude without a terminal

Start with one skill and a fictional example. You can download, unpack and add the files with a browser and file manager on Windows or Mac.

## Claude with Skills enabled

1. Download `decision-brief.zip` from the [latest GitHub release](https://github.com/SHOTClubhouse/shotos/releases/latest). Keep the ZIP intact for this route.
2. Open **Customize → Skills**, choose **+ → Create skill → Upload a skill**, then select the ZIP and enable the skill. If the menu is unavailable, check the workspace settings for skills and file creation, or use the file route below.
3. Start a fresh chat and ask Claude to use Decision Brief and open its bundled `template.md`, `review-cycle.md` and `scenarios/retail-trial.md`. Use the prompt below and check which scenario file and evidence IDs it cites. [Official Claude instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## ChatGPT Projects, or a Claude chat using files

1. Download the same ZIP. Use **Extract All** in Windows File Explorer or double-click it in Mac Finder.
2. Add `SKILL.md`, `template.md`, `review-cycle.md` and `scenarios/retail-trial.md` to a ChatGPT Project or attach them directly to a fresh chat. In ChatGPT desktop, use **+ → Add photos & files**. After selecting the files, check that all four appear before sending. If some are missing, open the picker again and add those files separately.
3. Run the prompt below. For a reusable project, you can also add the [working agreement](../../templates/AGENTS.md) to the project instructions. The same file approach works in a Claude Project or chat. If your app cannot upload Markdown, paste the relevant text or attach it as a text file.

> Read SKILL.md, template.md, review-cycle.md and retail-trial.md. Draft the first decision brief from R1–R3. Then use R4–R6 to explain which statuses change and which evidence changes each one.

A ChatGPT Project uses the files as context. Some eligible ChatGPT workspace agents also offer **Add skill** in the agent builder. Use that native option where your workspace allows it, and verify that the agent can open the scenario before relying on it. [ChatGPT Projects](https://learn.chatgpt.com/docs/projects) · [Workspace agent skill setup](https://developers.openai.com/cookbook/articles/chatgpt-agents-sales-meeting-prep#3-enabling-skills-and-memories-for-consistent-customized-outputs)

## Check your first result

Look for a named decider, dated evidence, an explicit decision and a handoff state that matches its receipt. If the assistant cannot see a supporting file, give it that file and repeat the check. A file upload provides instructions and examples. Tools, connectors and approval settings depend on the workspace.

For the retail example, R1–R3 support a conditional recommendation to extend the trial to one evening site, subject to a local baseline and existing staffing. R4 records the conditional approval, R5 records the receiving lead's acceptance, and R6 records a later decision to stop at that site after overtime rose. The independent cycle passes because the receiving operator ran the review without help from the original operator and the director accepted the review record. Wider rollout remains unauthorised.
