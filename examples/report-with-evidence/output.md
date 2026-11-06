The discount-code field is built and committed, but it is **not live yet**. The push was refused because the release branch needs a pull request, and the email to marketing is a draft, not sent.

## Against the acceptance card

| Check | Result | Evidence |
|---|---|---|
| 1. A valid code reduces the total | Passes | `test_valid_code_reduces_total` in `discount.test.js` |
| 2. An expired code shows "This code has expired" and the total does not change | Passes | `test_expired_code_message` and `test_expired_code_total_unchanged` |
| 3. No code: checkout works as before | Passes in tests | `test_no_code_unchanged`. Not tried in a real browser |

## What needs you

1. **Open the pull request** so this can go out tonight. The branch is `feature/discount-code`, commit `a41c9e2`. I cannot merge into the protected release branch.
2. **Send, or change, the email to marketing.** The draft is in `.work/discount-field/email-to-marketing.md`. It says the field is live, so only send it after the release is out.
3. **Know about one failure I did not cause:** `src/shipping/rates.test.js` was already failing before my change. It will block the full suite in CI.

## Claims
- [file] changed: src/checkout/form.js
- [file] created: src/checkout/discount.test.js
- [file] created: .work/discount-field/email-to-marketing.md
- [command] passes: npm test -- discount
- [git] committed: a41c9e2
- [unverified] not pushed: the release branch is protected and needs a pull request
- [unverified] email to marketing not sent: drafted only, no email tool
- [unverified] not tried in a real browser, desktop or mobile
- [unverified] the full suite does not pass: src/shipping/rates.test.js was failing before this change
