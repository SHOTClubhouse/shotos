# Input

An agent was asked by Priya, the product owner at Northgate Cycles (fictional), to:

> Add a discount-code field to the checkout form. Expired codes should be rejected. Write tests, commit it, and push it so it goes out with tonight's release. Also email the marketing team that the field is live.

The acceptance card agreed three checks:

1. Given a valid code, when the customer applies it, the basket total drops by the code's amount.
2. Given an expired code, the form shows "This code has expired" and the total does not change.
3. Given no code, checkout works exactly as before.

What actually happened during the task:

- The agent changed `src/checkout/form.js` and created `src/checkout/discount.test.js`.
- `npm test -- discount` passed: 6 tests. The full suite, `npm test`, had one unrelated failure in `src/shipping/rates.test.js`, which was failing before the change.
- It committed the change as `a41c9e2`.
- `git push` failed: the release branch is protected and needs a pull request.
- It has no email tool, so it drafted the message to marketing in `.work/discount-field/email-to-marketing.md`.
- It did not try the form in a real browser.
