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

The packet carries the text of each source, so the reviewer needs no access to the project folder. The builder refuses a source outside the scope folder, a source reached through a link, a source whose name or text looks like a secret, a missing revision and a packet over 128 KiB. `validate` refuses a packet with a missing or malformed request, acceptance list, source, evidence item or limitation, or with a source read at another revision. The packet identifies its scope by the folder's name, its full path and, when the folder is in a git repository, that repository's root commit, and `validate` refuses a packet whose scope does not match. It also reads every source again and refuses the packet if any text differs. So a packet built from another project, even one with the same folder name and identical text, or from a file that has changed since, cannot pass. The full path includes the name of your user folder, and it leaves the machine with the packet. `validate` prints the packet's SHA-256. Put that hash in the review record. The revision is the label you gave when building; `validate` cannot check it against version control.

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

The command receives the packet on standard input. It runs in an empty temporary folder with only the environment names you allow (`--allow-env NAME`), and it and anything it started are stopped at the time limit. The limit covers the output too: if the command exits while something it started still holds the output open, that is stopped at the limit as well, and the run reports exit code 124. On Windows the command runs only once it is inside a job object, which is how its whole tree is stopped; if that cannot be set up, the command is stopped before it runs and the run is refused with exit code 125 and no receipt. Output is capped at 1 MB as it is read; anything past that is dropped. The receipt records the command name, the packet hash, the exit code, the time, the output size and whether the output was cut, at the cap or by the time limit, never the text, and always says `"network_allowed": true` and `"sandboxed": false`.

This is process hygiene, not a sandbox. It does not block the network, or reads by absolute path or from the home folder. Use the reviewer tool's own read-only or no-tools mode too, and write down in the review record which controls were actually applied.

The tools cannot establish independence. Whether the reviewer was a different person, a different model or the same model in a fresh session stays a statement in the review record.
