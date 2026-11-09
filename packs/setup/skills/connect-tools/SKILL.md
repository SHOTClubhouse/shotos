---
name: connect-tools
description: Tests which tools the agent can reach (slides, mail, calendar, speech, images, browser, git) with harmless read-only calls and writes .work/capabilities.md. Use when SHOTos is installed, a tool is connected, or a skill stops on a missing tool.
---

# Check what tools are connected

Find out, with evidence, which tools this agent can use, so skills fail early and honestly instead of halfway through.

**Stage:** any, first used in Scope. **Rules served:** rule 1 (stop at the boundaries), rule 3 (read back the real result) and rule 4 (claim only what you can show).

## Context and handoff

Read the task’s exact data needs, current connector inventory and any existing `.work/capabilities.md`. Check account, task scope and proof with a safe read before proposing writes. Use the task data access card at `templates/data-access.md` in the SHOTos repository or `.shotos/templates/data-access.md` in an installed project.

Use `mode-ladder` to choose authority. Record verified capabilities and gaps in the project setup notes.

## Trigger and minimum inputs

Run it on first install, after connecting or removing a tool, or when a skill stops on a missing capability. It needs the runtime name, the workspace and one approved read-only test target per connector (a test folder, test calendar or blank page). With none, record "connected, not tested" and carry on. Any runtime can use it, whether Claude Code, Codex or another agent.

## When not to use this

Do not use it to set up accounts or create credentials; that is the owner's job. Do not use it to test a tool by doing real work with it.

## Steps

1. **List the relevant tools.** Inventory the runtime on its first setup. When resolving a blocked job, refresh the affected capabilities. Include local tools or connectors that could meet the same need.
2. **Map them to capabilities.** For each capability on this list (local slides, Google Slides, speech, transcription, images, video and ffmpeg, browser, mail, calendar, documents, Apps Script), note which tool would serve it, or "none".
3. **Test each one read-only.** Make the smallest approved call that proves access: list one designated test folder, read an approved test calendar, list available voices, open a blank browser page or import `pptx`. Verify the account and intended scope first. If there is no approved test target, record the connector as connected, not tested. Reachability alone gives no permission to use live data. Never send, post, publish, create live documents or generate paid media during the check. If the only possible test costs credits or creates something, mark it "connected, not tested" and say why.
4. **Record the evidence.** For each capability, record status (works, connected not tested, missing), tool, scope tested, date and test result.
5. **Name the affected skills.** For each missing capability, list the skills that need it and the step that will stop.
6. **Route the gap.** Open `docs/connect-your-tools.md` or the installed `.shotos/docs/connect-your-tools.md` for the matching capability. If the guide is unavailable, name the tool category that would unblock the step. The owner handles credentials and account connections.
7. **Update the matching section.** Use [template.md](template.md) in `.work/capabilities.md`. Keep separate dated sections for distinct runtime and workspace scopes. A targeted check updates only the relevant rows. Read back the refreshed entries and retain other evidence.

## Output

`.work/capabilities.md` holds the runtime and scope, dated checks, affected skills and next connection. Refer to the section for the environment doing the work.

## Blockers and handoff

If a tool needs credentials, account access or spend, stop at that capability and name the owner who must act. Continue with the others. Hand the file to `mode-ladder` for routing and to any skill that listed a gap. State the first skill that can run today and the first that cannot.

## Checks

- Every "works" entry has a test that actually ran, with its result.
- A targeted refresh preserves checks from other runtime and workspace scopes.
- Nothing was sent, posted, published or bought during the check.
- Every gap names the skills it affects and how to connect it.
- The file exists and was read back.
