# LEAP and NUDGE in a CRM

**Start with the [qualification sheet](qualification-sheet.csv); export only reviewed rows to a CRM.** The three platform CSVs are header templates, not files to upload unchanged. They contain no people or deals. The CRM owner must fill account-specific fields, map custom properties, test a small import and read back the result. The agent may prepare the file but does not import it without the owner's instruction.

## Which file to use

| Destination | Template | Use it for |
|---|---|---|
| HubSpot Deals | [hubspot-deals.csv](hubspot-deals.csv) | A deal in an existing HubSpot pipeline. |
| Salesforce Leads | [salesforce-leads.csv](salesforce-leads.csv) | An early person or organisation before an Opportunity exists. |
| Salesforce Opportunities | [salesforce-opportunities.csv](salesforce-opportunities.csv) | A qualified opportunity linked to an existing Account. |

Keep the CRM's own stage separate from the **LEAP stage**. Map `Pipeline` and `Deal stage` to values that already exist in that HubSpot account. Map Salesforce `Lead Status` or `StageName` to that organisation's values. LEAP is a separate custom field, so the same method can sit on top of different sales pipelines. NUDGE scores evidence; they are not forecast probabilities.

## Prepare the import

1. Copy a header template and fill it from the reviewed qualification sheet. Use one row per actual CRM record. Do not invent contacts, budget, value, dates or approval.
2. Have the CRM administrator create the SHOTos custom properties used by the destination template, or rename the headers and map them to equivalent existing fields. Use numeric 0 to 15 for NUDGE score, text or a controlled option for decision (`go`, `pause`, `walk away`), and a yes/no field for proposal readiness. Keep the evidence URL as a link to the source record with appropriate access.
3. For HubSpot, supply `Deal name`, `Pipeline` and `Deal stage` for new deals. Pipeline and stage must match existing account options. Use `Record ID` when updating existing deals to avoid duplicates; decide whether the import creates, updates or both before running it.
4. For Salesforce Leads, fill `Company` and `Last Name` and map `Lead Status` to an existing value. For Salesforce Opportunities, fill `Name`, `CloseDate`, `StageName` and the **existing** `AccountId`. Do not guess a close date merely to make an early lead fit the Opportunity object. Salesforce Data Loader supports Opportunity CSV field mapping; availability depends on edition and permissions.
5. Test with a small set in a sandbox or controlled import. Inspect the field mapping, duplicates, errors and resulting records. Record the import receipt and the CRM owner's acceptance before a larger batch.

**No live CRM import has been tested for these templates.** The headers and route follow the vendor documentation below. Each account has its own properties, required fields, picklists, permissions and deduplication rules, so a filled file still needs local validation.

## Vendor documentation checked 6 November 2026

- [HubSpot: format import files](https://knowledge.hubspot.com/import-and-export/set-up-your-import-file) documents required new-deal fields, existing pipeline/stage values and identifiers for updates.
- [Salesforce: import Opportunities](https://help.salesforce.com/s/articleView?id=000384984&language=en_US&type=1) documents `Name`, `CloseDate`, `StageName`, `AccountId` and Data Loader mapping.
- [Salesforce: lead import field mapping](https://help.salesforce.com/s/articleView?id=sf.field_mapping_for_importing_leads.htm&language=en_US&type=5) documents Lead CSV labels.
- [Salesforce: pre-import checklist](https://help.salesforce.com/s/articleView?id=sf.essentials_import_checklist.htm&language=en_US&type=5) covers required Lead fields and creating custom fields before import.
