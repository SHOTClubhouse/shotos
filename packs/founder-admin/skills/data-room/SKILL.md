---
name: data-room
description: "Builds and audits a due-diligence data room: standard categories, index, gaps, and who can see what. Use when preparing for a funding round, sale or audit, or asked what is in the data room. Changes no sharing settings."
---

# Data room

Make it easy for a reviewer to find what they need, and make sure nobody sees what they should not.

Stage: Own. Rules served: 1 (stop at the boundaries), 4 (claim only what you can show) and 3 (read back the real result).

## When not to use this

Skip it for a single document request. Do not use it to decide what the company should disclose; that is for the owner and legal adviser. Do not move, copy, delete or re-share files without the owner's yes.

## Standard categories

1. Company: incorporation, constitution or articles, structure chart, registers.
2. People: team list, contracts, option or equity records, policies, advisers.
3. Finance: accounts, management accounts, budget, tax filings, bank, debt, grants received.
4. Legal: material contracts, disputes, insurance, licences, compliance.
5. Intellectual property: ownership, assignments, trademarks, licences in and out, open-source use.
6. Product: description, roadmap, architecture summary, security.
7. Customers: customer list (redacted where needed), contracts, retention, feedback.
8. Commercial: market, pricing, pipeline, partners.
9. Data protection: register of processing, privacy notices, data processing agreements, breaches log, safeguarding where relevant.
10. Governance: board papers, minutes, advisory board.

Adapt to the situation; say what was added or dropped and why.

## Steps

1. **Define the purpose and the reader.** Round, sale, audit or grant. Who will see it, and what do they usually ask for. Ask the owner for a list of who is allowed in.
2. **Inventory.** Read the folder or index the owner points to. For each file: path, category, date, owner, version and sensitivity (public, restricted, confidential, personal data). Do not open files beyond what the task needs; for personal data, record that it exists, not its content.
3. **Build the index.** One line per file in category order, with a one-line description, date and status (current, draft, superseded). Mark duplicates and out-of-date versions.
4. **List what is missing.** Compare with the category list and the reader's likely requests. For each gap: what, why it matters, who holds it and whether it exists at all. Do not fabricate documents.
5. **Record access.** For each category or file: the people or groups allowed, from the owner's list. Show the intended access against the actual sharing settings where you can read them.
6. **Run the exposure check.** Flag anything confidential or personal that is visible to more people than intended: link sharing on, wide groups, public links, external editors, files containing personal data or credentials, and counterparties' confidential terms. Do not change a setting. Report each with the evidence and the suggested change.
7. **Report to the owner** with the index, gaps, access table and exposures. The owner or an authorised person makes the changes.
8. **Stop.** Do not share, move, rename or delete files, or invite anyone.

## Output

Use [template.md](template.md): purpose, index, gaps, access table and exposure findings. Save outside the room itself, for example `.work/data-room/audit.md`.

## Checks

- Every file in the index has a category, date and sensitivity.
- Gaps are listed and none filled with an invented document.
- Access is compared with the owner's intended list.
- Every exposure finding has evidence and a suggested change; no change was made.
- Personal data and credentials were recorded as present, not copied into the report.
