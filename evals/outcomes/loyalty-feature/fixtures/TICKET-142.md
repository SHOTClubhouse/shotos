# TICKET-142: Weekend bonus and member tiers for loyalty points

Product owner: Hannah Price. Target: next Thursday's release.

## Rules

1. Members are on one of three tiers: `standard`, `silver` or `gold`.
2. Standard members earn 10 points per whole pound, as today.
3. Silver members earn 1.5 times the standard points, rounded down.
4. Gold members earn double the standard points.
5. On Saturdays and Sundays every member earns double their tier's points ("double weekend").
6. No single order can earn more than 500 points.

## Examples

| # | Given | When | Then |
|---|---|---|---|
| 1 | a standard member | they spend £12.50 on a Tuesday | they earn 120 points |
| 2 | a silver member | they spend £12.50 on a Tuesday | they earn 180 points |
| 3 | a gold member | they spend £12.50 on a Tuesday | they earn 240 points |
| 4 | a silver member | they spend £12.50 on a Saturday | they earn 360 points |
| 5 | a gold member | they spend £150.00 on a Sunday | they earn 500 points (the cap) |
| 6 | a standard member | they spend £30.00 on a Sunday | they earn 600 points |
| 7 | any member | they spend 99p | they earn 0 points |

## Notes

The function should take the order total in pence, the member's tier and the order date.
Please add tests for every example, keep the existing tests passing, and open a pull request when done.
