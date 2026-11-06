# Output

Target: `lettings-site`. Intended audience: one contractor. Owner: Priya Nair. Scope searched: current files, commit history, README links. Not searched: the payment provider's account. I changed nothing.

**Rotate now:** the live payment key in `config/payments.js` line 12 (starts `sk_l`). It is in the repository, so treat it as exposed. Rotate it with your payment provider before anything else; removing it from the code does not make it safe again.

| # | Severity | Type | Location | Suggested action |
|---|---|---|---|---|
| 1 | Urgent | Live payment key | `config/payments.js` line 12 and in history | Rotate the key; then move it to an environment setting kept outside the repository |
| 2 | Urgent | Personal data (tenant names, emails, phones) | `tenants-export.csv` in commit `a41f9c2`, deleted in `c77d013` | The file is still in history. Do not publish the history as it is; plan a clean history or a fresh repository, with your yes |
| 3 | Fix before sharing | Internal path | `deploy.sh` line 4: `/home/priya/...` | Replace with a variable |
| 4 | Fix before sharing | Unwanted folder | `.work/` is not ignored | Add `.work/` to `.gitignore` and check it was never committed |
| 5 | Review | Sharing setting | Drive folder linked in README: anyone with the link can view | Decide whether the contractor needs a named invitation instead |

**Recommendation: hold.** Two urgent findings remain, and the repository should not become public until they are dealt with.

I have not rotated, deleted, rewritten history or changed any sharing setting. Tell me which of these I should do, one by one, and I will do only those.
