# Output

I will set this up, but not as asked in three places.

- **No emailing.** The factory makes documents and does not send, share or delete anything. Emailing 180 customers is yours to do after you have read the letters.
- **Not all 180 at once.** I will run a dry run, then three real letters for you to open, then the full batch.
- **The notes column stays out for now.** Free-text notes can hold things a customer should never read. If you want notes in the letter, tell me which notes are meant for customers and I will add a separate placeholder after we check them.

## Acceptance record (draft, waiting for your yes)

- Owner: the Northgate Cycles manager.
- Expected: 180 letters, one per row, each with the right first name, bike and due date.
- Must not: send, share or delete anything.
- Output folder: a private folder. A copy made in a shared folder is visible to everyone who can see it.

## Template and data checks I will do

- The template has three tokens: `{{first_name}}`, `{{bike}}`, `{{due_date}}`. The sheet needs columns with exactly those names.
- Empty cells block a row. Duplicate customers and odd characters get listed for you.
- Banned terms: please give me words that must never appear (for example internal notes such as "complaint" or "owes").

## Steps

1. You paste the script and approve permissions (I cannot do this in your account), then run `setupFactory`.
2. `dryRun`: I read the Report tab with you. Nothing is created.
3. `runSample`: three letters. You open them and compare each with its sheet row.
4. If all three are right, you say yes, then `runBatch`.
5. I reconcile: 180 rows = done + blocked + error. Blocked rows are listed with reasons.

## Claims
- [unverified] Script behaviour in your account: not run yet.
- [unverified] That the template wording is approved: you confirm.
