# Maintainers

| Name | Role | GitHub |
|---|---|---|
| Liam McDowell | Creator and lead maintainer | [@liammcdow](https://github.com/liammcdow) |

## How maintainers check and release changes

SHOTos does not run GitHub Actions. Checks, releases and the demo site all run from a maintainer's machine.

- **Before merging a pull request**, check out its branch and run `python tools/local_gate.py` with `SHOTOS_DENYLIST` set to the private denylist. Merge only when the card says GO and someone other than the author has reviewed the change.
- **Before pushing**, the pre-push hook runs the fast gate. Install it once with `python tools/install_hooks.py`.
- **To release**, follow [Releasing](RELEASING.md). A maintainer may cut a patch or minor release with `python tools/release.py --publish` when the gate card is GO and an independent review is clean. A major release needs the owner.
- **To publish the Northbank demo site**, run `python tools/publish_northbank.py` to build it into `.work/northbank/site` and look at it, then `python tools/publish_northbank.py --publish` from `main` to push it to the `gh-pages` branch.
- **To build the website**, run `python tools/build_site.py` with `SHOTOS_DENYLIST` set. It writes only the built files (landing page, role guides and the Northbank example) to `.work/site`, checks every link between pages and scans the output for private terms. Add `--serve` to look at it on `http://localhost:8765`. It exits 0 only when the sources are committed and the scan ran clean. The script publishes nothing; where the site is hosted is the owner's decision.

## Keep private terms out

The leak scan reads a private denylist kept outside the repository. Each line is a case-sensitive whole word or phrase, `i:` for case-insensitive, or `path:` for text that must never appear anywhere. Lines starting with `#` are comments. Point `SHOTOS_DENYLIST` at the file; `python tools/leak_scan.py` runs the scan on its own.

If a listed term must appear on purpose, add the file path and the denylist line number to `tools/leak-allowlist.txt`. Never write the term itself in the repository. If you reorder the denylist, update the line numbers in the allowlist.

## One setting the owner changes

The demo site used to be published by a workflow. It now comes from the `gh-pages` branch, so GitHub Pages must read that branch. In the repository on GitHub, open Settings, then Pages. Under "Build and deployment", set Source to "Deploy from a branch", then choose `gh-pages` and `/ (root)` and save. Do this after the first `--publish`, once the branch exists.
