# Guardrail: Data governance and risk

## What it protects

Information about people, and the organisation's duty to handle it properly. An agent that reads, summarises and moves data quickly can also move the wrong data to the wrong place quickly. Children's data and special-category data need the most care, because harm from a mistake is hardest to repair.

## Minimum practice

### 1. Classify data before using it

Place each source in one class. When in doubt, use the higher class. Use your organisation's own classifications. Record the approved source, purpose and destination on the [task data access card](../../templates/data-access.md).

| Class | Examples (invented) | Agent may | Needs |
|---|---|---|---|
| **Public** | Published opening hours, a public price list | Use freely, with source | Nothing special |
| **Internal** | Meeting notes, draft plans, internal procedures | Use inside the project; share only inside the organisation | Mark as internal in outputs |
| **Confidential** | Contracts, customer lists, financial results, staff records | Use only for the named task; no copying outside the project | Owner's yes to use; minimum fields only |
| **Special category** | Health, religion, ethnicity, union membership, sexual orientation, biometrics used to identify someone | Use only where the task cannot be done without it | Named approver, stated lawful basis, independent review, no external output |
| **Children's data** | Any data about under-18s, such as names, ages, photos, results or contact details | Use only where essential and approved by a responsible adult | Named safeguarding lead, parent or guardian consent where required, minimum fields, no external output without sign-off |

Criminal offence data has separate rules under the UK GDPR. Route it to the responsible data owner before use. [ICO guidance on criminal offence data](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/criminal-offence-data/what-is-criminal-offence-data/)

The classes tie to risk tags in [control 2](../02-evidence-based-risk.md): `personal-data`, `special-category` and `children` are added when evidence in the task triggers them.

### 2. Know the basis and the consent

- Record why the data is being used and who allowed it, in the task record ([control 11](../11-context-control.md)).
- Use data only for the purpose it was collected for. If the task needs a new purpose, ask the owner first.
- For people who gave consent, record what they agreed to and when. Consent for a newsletter is not consent to be named in a case study.
- For children, record who consented on their behalf and for what.
- Honour withdrawal: when someone asks to be removed, remove them from drafts, lists and future runs, and record that you did.

### 3. Minimise

- Pass the agent only the fields the task needs. A reminder list needs a name and a date, not a date of birth.
- Prefer identifiers over names when a task allows it, and keep the lookup separate.
- Do not paste personal data into prompts, skills, examples or committed files. Test with invented data.

### 4. Retain and delete on purpose

- Say how long each kind of working file may be kept. A suggested start: working copies of confidential data for the length of the task plus 30 days; special-category and children's data deleted at task end unless a named person records why they are kept.
- Task records keep metadata and references, not the data ([control 11](../11-context-control.md)).
- Deleting is a boundary action ([control 4](../04-stop-boundaries.md)); the owner approves the list.

### 5. Check for public exposure before anything leaves

Before publishing, sharing or committing anything external:
- Search the output for names, emails, phone numbers and addresses that should not be there.
- Check images and documents for hidden detail: metadata, comments, tracked changes, hidden sheets and file names.
- Check that sharing settings are what you meant, not "anyone with the link" by default.
- Check that aggregated figures cannot identify an individual, such as a count of one in a small group.
- For children's data, a second person looks at the output before it goes.

## Checks

- Pick any three recent outputs. Each has its data class noted and no data above the class the reader is cleared for.
- Search the repository and task records for email addresses, phone numbers and names of private individuals. None present, except invented test data.
- Run a withdrawal test: remove one test person and check they are absent from the next run.
- Check the oldest working file. Does it have a reason to still exist?
- Open the sharing settings on the last five shared documents. Each matches the plan.
- Ask the agent, "what is the most sensitive data in this task?" It names the class and where it appears.

## Controls and skills

| Control | How it applies |
|---|---|
| [2: evidence-based risk](../02-evidence-based-risk.md) | Finds the data classes and tags them with evidence |
| [4: stop boundaries](../04-stop-boundaries.md) | Sending, publishing and deleting need the owner's yes |
| [11: context control](../11-context-control.md) | Keeps data out of records and out of long contexts |
| [8: two-session execution](../08-two-session-execution.md) | Freezes exactly which records go where |

Skills: `capture-the-problem` records the data involved at Scope; `evidence-handoff` passes references instead of data.

## Common failure

An analyst pastes a list of members with dates of birth into a prompt "to save time" and the summary then carries a child's age into a public post. The fix is not a better prompt. It is the class table, the minimum-fields habit and the exposure check.
