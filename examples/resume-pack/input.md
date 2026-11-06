# Input

All names and details are invented for this example.

The session is at 90 per cent of its context. The task: move tenant-deposit reminder emails at Harbourside Lettings from a spreadsheet to a database table, with a draft email generated for each reminder. Owner: Dominic Hale, finance lead. Work is in the `deposit-reminders` repository on branch `feature/reminders-table`.

Facts from the session:

- Task file `.work/deposit-reminders/task.md` lists the acceptance: every reminder in the spreadsheet appears once in the table; draft emails never send automatically; the finance lead approves each batch.
- Done and tested: the new table definition file `migrations/0004_reminders.sql` was written and checked by a dry run on the test database. It has not been applied to the live database.
- Done and tested: `import_reminders.py` reads the spreadsheet and loads 212 rows into the test database; duplicates are skipped. The test passes.
- Written but not tested: `draft_emails.py`, which creates draft emails in a folder. No test yet.
- The live database credentials are in the team password manager. During the session the agent was shown a connection string with the password in it; it must not appear in the pack.
- The agent assumed the reminder date column should be a date and not a text field. Dominic has not confirmed.
- One tenant row in the spreadsheet has a note: "Mrs. Okafor, disputed, call first". The sample test data includes tenants' names and phone numbers.
- Uncommitted: `draft_emails.py` and a new test file `tests/test_drafts.py` (empty).
- Dominic said on a call, "Don't send anything until I have seen ten of the drafts."
- A lesson: the first import run created duplicates because the spreadsheet had trailing spaces in the tenant reference. Trimming spaces fixed it.
