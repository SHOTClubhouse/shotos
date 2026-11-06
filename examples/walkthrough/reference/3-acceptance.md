# Acceptance card

**Task:** a weekly repair-status update for tenants with an open repair, drafted for a person to check and send
**Owner (accepts the work):** operations lead

## Outcome
Every tenant with an open repair hears what is happening once a week, before they need to chase.

## Checks
1. Given the open repairs list, when the weekly drafts are produced, then there is exactly one draft per open repair.
2. Each draft states the issue, the current status and the next date, using only facts from the repairs list.
3. No draft contains another tenant's details.
4. Drafts are saved to `.work/updates/` and nothing is sent.

## Must fail or refuse
If a repair has no status or next date in the list, the draft is marked "needs a person" instead of guessing.

## Boundaries: ask the owner first
- Sending anything to tenants: never. A person checks and sends.
- Using tenant data outside the company's own systems.

## Confirmed
Operations lead, 22 September.
