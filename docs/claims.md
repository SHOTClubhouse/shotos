# The Claims block

Every task that changes something ends with a Claims block. Place the actual block in the report outside a code fence. Each line is one claim that a person or `claim-check` can test.

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
- [authorised] owner approved this action and revision | receipt: path/to/approval
- [offered] authorised offer dispatched to the receiver | receipt: path/to/dispatch
- [accepted] who accepted it | receipt: path/to/the record
- [completed] handoff close-out and first action | receipt: path/to/close-out
- [independent] receiving team ran a full cycle | receipt: path/to/cycle-record
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

Put each status claim in the Claims block. The checker reads those lines and checks that a referenced receipt exists and contains data. The reviewer must check the receipt's origin and contents against the claim. A passing block does not verify status assertions made only in the surrounding prose.

| Work status | Required evidence |
| --- | --- |
| Draft or Prepared | Saved artefact and its current version |
| Authorised | A named owner approved the exact action and revision |
| Offered | Dispatch receipt or read-back for the authorised offer |
| Accepted | Written acknowledgement by the named receiver with scope, capacity, access and a dated first action |
| Completed | The customer notification, owner update and first action are recorded |
| Independent cycle | The receiving team runs a full cycle on its own and its lead signs off |

For file creation and deletion, pass a starting commit with `--base` when you have one. The checker can then compare the path with the starting tree. Without a starting commit, it can check only whether the path exists now. Untracked files are outside the starting commit.

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

`base` is the commit the work started from. It lets `claim-check` see changes that were already committed. It must name a real commit, and anything that looks like an option is refused.

## What claim-check cannot tell you

- **Quality.** A file that exists may still be wrong. That is what the acceptance checks are for.
- **Genuine receipts.** A receipt is checked for existence only. An agent could write its own. Use receipts your systems produce, such as a message ID or a deployment log, and spot-check them.
- **Earlier turns.** The Stop hook checks the agent's final message in each turn.
