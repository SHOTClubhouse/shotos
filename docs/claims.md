# The Claims block

Every task that changes something ends with a Claims block. Each line is one claim that a person or `claim-check` can test.

```
## Claims
- [file] created: path/to/file
- [file] changed: path/to/file
- [file] deleted: path/to/file
- [command] passes: the exact command
- [git] committed: HEAD
- [git] pushed: branch-name
- [git] clean: working tree
- [external] sent: what and to whom | receipt: path/to/receipt
- [accepted] who accepted it | receipt: path/to/the record
- [unverified] anything not checked
```

## States

| State | Meaning |
|---|---|
| SUPPORTED | The evidence backs the claim |
| UNSUPPORTED | The evidence contradicts the claim |
| NO EVIDENCE | It cannot be checked here: no receipt, or a command not on the allow list |
| DECLARED | The agent said itself that it did not check this |

A report passes when every claim is SUPPORTED or DECLARED. An honest `[unverified]` line passes. A confident claim with no evidence fails.

## Installed, executed, accepted

- **Installed:** the thing is present.
- **Executed:** it ran and was checked against the acceptance checks.
- **Accepted:** a named person said yes.

`claim-check` can show installed and executed. Only a person can accept.

## Commands and trust

`claim-check` runs a command only if it is on an allow list you control, never because a report asks. Running a command is a trust decision, so the allow list comes from:

- **your own config**, `~/.shotos/claim-check.json`, which applies everywhere, including the Stop hook;
- **a config file you name** with `--config`;
- **the project's** `.shotos/claim-check.json`, but only when you pass `--trust-project-config`. A repository you cloned cannot make claim-check run its commands, and the Stop hook never trusts it.

```json
{ "allow_commands": ["python -m unittest"], "base": "main" }
```

`base` is the commit the work started from. It lets `claim-check` see changes that were already committed. A `[git] committed` claim needs a base and a newer descendant commit; a clean working tree alone does not show that this task was committed. Without a base, the claim is `NO EVIDENCE`. The base must name a real commit, and anything that looks like an option is refused.

## What claim-check cannot tell you

- **Quality.** A file that exists may still be wrong. That is what the acceptance checks are for.
- **Genuine receipts.** A receipt is checked for existence only. An agent could write its own. Use receipts your systems produce, such as a message ID or a deployment log, and spot-check them.
- **Hook scope.** The Stop hook checks assistant text since the last human message, including earlier text in that turn. It can still miss a false assertion phrased without a recognised completion word, or a prose claim not represented in a Claims block. Do not treat it as a full audit.
- **Exit codes.** `claim-check` exits 0 when every claim holds, 1 when a claim fails and 2 when it could not run at all (an unreadable report or config).
- **Where the hook acts.** Only in a project with a `.shotos` folder, or for a user with `~/.shotos/claim-check.json`. Installing the plugin alone never blocks anyone.
- **Commands time out after 100 seconds**, below the hook's 120 second limit, and report the claim as unsupported.
