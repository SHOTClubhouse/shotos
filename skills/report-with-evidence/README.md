# report-with-evidence

**Make the agent end its work with a list of claims that a tool can check.**

Every task that changes something ends with a short plain summary and a Claims block. Each line says one thing that was done, in a form `claim-check` can test against files, git and receipts. Anything the agent did not check goes on an `[unverified]` line, and that line passes.

It supports the Operate and Track stages. It serves rule 3, Read back the real result, and rule 4, Claim only what you can show.

## The problem it solves

An agent finishes and says: "All done. I've written the pricing summary, the tests pass, it's committed, and I've emailed it to the finance team."

You come back an hour later. The file exists. The tests fail. The commit never happened. No email was sent. The report read as confidently as a true one would have, and nothing in it let you tell the difference without checking everything yourself.

## What the agent does differently

The agent opens the file, runs the test and looks at the commit before it reports. Then it writes what it saw. This is the report from [examples/report-with-evidence/output.md](../../examples/report-with-evidence/output.md):

> Added a discount-code field to the checkout form, with validation for expired codes. The new tests pass. I have not pushed, because you asked to review first.

The result comes first, then the one decision the reader must make. The block at the end is checkable:

> - [file] changed: src/checkout/form.js
> - [command] passes: npm test -- discount
> - [git] committed: HEAD
> - [unverified] I did not test on a mobile browser

Work has three states: installed (present), executed (run and checked) and accepted (a person said yes). The agent may claim the first two. It may not write that work is accepted unless it holds the record.

## When to use it, and when not to

Use it at the end of any task that changed a file, ran a command or acted on your behalf. Use it whenever a report says done, fixed, sent, deployed or passing.

Skip it for a plain answer to a question where nothing changed. There is nothing to claim.

## Who it is for

- **Solo founder:** you can leave an agent working and trust the report when you return.
- **Small team lead:** reviews start from a list of claims, not from reading everything.
- **Engineering or practice lead:** the Claims block gives code review a fixed place to start.
- **Business unit leader:** a status update you can forward knowing which lines were checked.
- **Product owner or analyst:** every "done" arrives with the part that was not checked.
- **Enablement coach:** a short format you can teach in ten minutes.

## How to use it

Install SHOTos as described in the [main README](../../README.md#install). In Claude Code, add `--with-hook` so the Stop hook runs `claim-check` when the agent tries to finish. Then ask in plain words:

> Create a file notes.md with a three-line summary, then report back on what you did.

You get a summary and a Claims block. The format is in [docs/claims.md](../../docs/claims.md). You can run the check yourself with `python .shotos/tools/claim_check.py report.md`.

This skill has no template file, because the Claims format is the template. On paper: after any piece of work, write one line per thing you did, and tick it only after you have looked at the result yourself.

## How it connects

- **Before:** [agree-acceptance](../agree-acceptance/README.md) defines the checks the claims are reported against.
- **After:** [evidence-handoff](../evidence-handoff/README.md) ends with a Claims block too, so the next person inherits checkable lines.
- **Tool:** `claim-check` and the Stop hook turn the format into a pass or fail. See [hooks/](../../hooks/).

## Needs

The saved result and its authoritative evidence, such as a file, test result or external receipt. The local claim checker is optional. Record any check you could not run.

## How it is tested

The skill has five cases in [evals/cases.json](../../evals/cases.json). Three are normal: create a file and report, report that a plan was not run, and draft an email without claiming it was sent. Two are contrary: refuse to mark a project accepted from a passing remark, and refuse to say a deploy worked when the agent has not seen it.

The caveat: "One run per case per condition, on one model. Agent output varies between runs." This is not proof that the skill is unnecessary on other models or longer tasks. It means this run could not show a difference.

## Tips and common mistakes

- Put the exact command or path in the claim, not a description of it.
- Do not claim an external action without a receipt such as a message ID, a URL or a saved log.
- An honest `[unverified]` line is a good report. Do not pad it with confident claims to look complete.
- Do not accept "done" in the summary if the Claims block does not back it.

## Limits

- `claim-check` tests that work happened. It cannot judge quality.
- It checks that a receipt exists, not that it is genuine. An agent could write its own. Use receipts your systems produce and spot-check them.
- The Stop hook checks the final message of each turn, not earlier ones.
- No measured difference on Sonnet in the first run. Codex has not been tested.

Files: [SKILL.md](SKILL.md) (for the agent), [example input](../../examples/report-with-evidence/input.md) and [output](../../examples/report-with-evidence/output.md).
