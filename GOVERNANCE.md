# Governance

SHOTos is maintained by SHOT Clubhouse Limited. Liam McDowell created it and is the lead maintainer.

## How decisions are made

- **Day to day:** every change goes through the local gate (`python tools/local_gate.py`), not GitHub Actions. Maintainers review and merge pull requests whose gate card is GO and that follow [CONTRIBUTING.md](CONTRIBUTING.md).
- **Releases:** a maintainer may cut a patch or minor release with `tools/release.py` when the gate card is GO and an independent review is clean. Anything that breaks the four controls is a major release and needs the owner, the lead maintainer. See [Releasing](RELEASING.md).
- **What goes in:** a new skill, control or pack needs an issue first, a worked example, normal and contrary eval cases, and evidence that it changes behaviour. "It sounds useful" is not enough.
- **Disagreements:** these are settled in the open, on the issue or pull request. If they cannot be settled, the lead maintainer decides and records the reason.
- **Becoming a maintainer:** contributors who have made several accepted contributions and reviewed others' work may be invited by the existing maintainers.

## What will not change without a major version

The four controls, the Claims block format and the claim-check exit codes. Anything that breaks them needs a major release and a migration note.
