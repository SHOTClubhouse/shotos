# Output

Repository: `team-agent-setup` (clean). Installed location: Tom's laptop configuration folder. I have not changed either side.

| File | State | Proposed action |
|---|---|---|
| `skills/repair-quote/SKILL.md` | Differs: installed copy has one extra line, "Always add 20% VAT" | **Propose back, if you want it kept.** Difference below. Needs your decision, because it changes how every quote is written. |
| `settings.local.json` | Only on the laptop; holds an access token | **Keep local.** Do not copy to the repository. Add it to the local ignore list. |
| `skills/stock-check/SKILL.md` | Only in the repository (Aisha, Monday) | **Install** to your laptop. |

Difference for `skills/repair-quote/SKILL.md`:

```
+ Always add 20% VAT to the quote total.
```

Questions for you, Tom:

1. Is the VAT line right for every quote? If yes, I will put it on a branch as a change request with a message saying why, for a teammate to review. If it applies to only some customers, it should not go into the shared repository as written.
2. Shall I install `stock-check` on your laptop? I will back up the existing folder first.

Reply yes for each, and I will check for drift again afterwards to confirm the only remaining differences are the local settings file and the change awaiting review.
