# Input

All names and details are invented for this example.

Request from Dominic Hale, finance lead at Harbourside Lettings: "Mei Tan runs the monthly landlord statements. She is on leave from the 14th and I need someone else, Jaswinder Gill, to be able to run it. Write the runbook from what Mei actually does."

**Mei's account (voice note, transcribed):** "I take the rent export from the accounts system on the 2nd working day, save it in the statements folder as rent-YYYY-MM.csv. Then I run the statement script. It makes one PDF per landlord in an output folder. I check the totals against the ledger report; they have to match to the penny. Then I upload the PDFs to the landlord portal. Landlords get an email from the portal when I press publish. I always do the publish on the 5th working day."

**Shell history, 4 and 5 November:**
- `python statements.py --month 2025-10 --input rent-2025-10.csv --out output/2025-10`
- `python statements.py --month 2025-10 --input rent-2025-10.csv --out output/2025-10` (second run, same day)

**Notes from last month's ticket:** the first run stopped at landlord 61 of 74 with "missing management fee rate for property 118". Mei added the rate to the fees sheet and re-ran. The portal publish button is irreversible once emails go out; PDFs can be withdrawn before then.

**Observed once (Jaswinder watched on 4 November):** export took 3 minutes; script took about 2 minutes; 74 PDFs created; ledger total 38,412.60 pounds matched the sum of statements.

**Not seen:** where the fees sheet lives (Mei said "the finance folder"), how she logs in to the portal, what happens if the script is run on a month with no export.

**Contacts sheet reference:** "Finance contacts" in the shared team handbook.
