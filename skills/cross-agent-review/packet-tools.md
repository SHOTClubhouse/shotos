# Build the packet and run the reviewer with the tools

Two optional tools make steps 3 and 4 of [SKILL.md](SKILL.md) easier to do carefully. They need Python 3.9 or later. In the SHOTos repository they are in `tools/`; where SHOTos is installed in a project they are in `.shotos/tools/`. If they are not available, build the packet by hand and say so in the review record.

Skip both for work the skill says needs no review. A one-line, low-risk change does not need a packet.

## Build the packet

Write a short spec in the task's working folder, for example `.work/<task>/spec.json` (fictional):

```json
{"request": "Check the volunteer rota against the rule card.",
 "acceptance": ["No one has more than 3 shifts."],
 "sources": ["rota.md"],
 "evidence": [{"source": "rule card", "text": "Maximum 3 shifts each."}],
 "limitations": ["The availability list was not supplied."]}
```

Then build and check it:

```
python .shotos/tools/review_packet.py build .work/<task>/spec.json --scope . --revision <exact commit or version> --out .work/<task>/packet.json
python .shotos/tools/review_packet.py validate .work/<task>/packet.json --scope .
```

The packet carries the text of each source, so the reviewer needs no access to the project folder. The builder refuses a source outside the scope folder, a source reached through a link, a source whose name or text looks like a secret, a missing revision and a packet over 128 KiB. `validate` refuses a packet used with a different folder or with a source read at another revision, and prints the packet's SHA-256. Put that hash in the review record.

The secret check is a safety net based on names and a simple pattern. It does not prove nothing sensitive remains. The owner still decides what the reviewer may see.

## Run a command-line reviewer

```
python .shotos/tools/run_contained.py --packet .work/<task>/packet.json --timeout 300 --receipt .work/<task>/receipt.json -- <reviewer command>
```

This is a dry run. It checks the packet and prints the command it would launch, the packet's size and hash, the environment names and the time limit. It launches nothing and writes nothing, not even the receipt.

The runner cannot block the network, so any reviewer it launches can send the packet anywhere, using credentials it finds under the home folder. Launch the reviewer only once the owner has agreed that the packet may leave the machine, by adding `--allow-network`:

```
python .shotos/tools/run_contained.py --allow-network --packet .work/<task>/packet.json --timeout 300 --receipt .work/<task>/receipt.json -- <reviewer command>
```

The command receives the packet on standard input. It runs in an empty temporary folder with only the environment names you allow (`--allow-env NAME`), and it and anything it started are stopped at the time limit. The receipt records the command name, the packet hash, the exit code, the time and the output size, never the text, and always says `"network_allowed": true` and `"sandboxed": false`.

This is process hygiene, not a sandbox. It does not block the network, or reads by absolute path or from the home folder. Use the reviewer tool's own read-only or no-tools mode too, and write down in the review record which controls were actually applied.

The tools cannot establish independence. Whether the reviewer was a different person, a different model or the same model in a fresh session stays a statement in the review record.
