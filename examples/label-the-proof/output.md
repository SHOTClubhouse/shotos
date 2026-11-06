# Committee dashboard, labelled

I edited `dashboard-final.xlsx`, which is the most recently modified file, in place. I did not create a new version. I could not confirm that it is the one you meant to be current, so please check. `dashboard.xlsx` and `dashboard-v2.xlsx` are untouched; if they are no longer needed, tell me and I will help move them to a dated archive folder. I will not delete them without your yes.

## Key
- **Literal:** from the register export or the club's own records. Pointer given.
- **Inferred:** reasoned from named evidence.
- **Illustrative:** made up to show the layout. Not real.

## Sheet 1, Attendance
Label: **literal.** Source: `register-export-oct.csv`, sessions from 1 to 31 October, read when this file was prepared.

| Group | Average per session |
|---|---|
| U8 | 18 |
| U10 | 22 |
| U12 | 15 |
| U14 | 11 |

## Sheet 2, "Membership by age group" chart
Label: **illustrative.** The values 30, 45, 38 and 20 are sample values, not counts from the club. I have put "ILLUSTRATIVE, NOT REAL DATA" in the chart title and removed the hidden "sample" marker, which nobody could see. Do not show this chart at the meeting. To replace it with real numbers, I need the number of unique players per age group; the October register has 112 unique players in total, but I have not split them by group yet.

## Sheet 3, "Projected membership next season: 160"
Label: **inferred.** Evidence: season-end totals of 131, 138 and 149 from `history.txt`. Reasoning: the totals rose by 7 and then 11, so a rise of about 10 to 15 looks plausible, giving 159 to 164. The 160 is a rounded value in that range. The cell was a typed number, not a formula; I have kept it, labelled it, and shown the working beside it. Confidence: low to medium. Three seasons is a short run, and nothing in the files says what will happen to numbers next season. Quote it as "about 160, estimated from three previous seasons", not as a count.

## Sheet 4, Status
- "New registration form: installed." Label: **literal.** It was set up last week.
- "Working." Label: **not supported as written.** The form was tested once by the administrator with a made-up entry. No real registration has come through it. I have changed the line to: "Installed. Tested once with a made-up entry. Not yet used for a real registration. Not accepted."

| Item | Installed? | Run? | Accepted by owner? |
|---|---|---|---|
| New registration form | Yes | Once, with a test entry | No |

## Not checked
- Whether `dashboard-final.xlsx` is the file the committee should see.
- Whether the register export covers every session in October. It has no gaps that I could find, but I have no list of expected sessions.
- The history totals in `history.txt` were not compared with older records.

## Where the file lives
`dashboard-final.xlsx` in the club folder is the canonical file for tonight. Earlier versions are the two other files in the same folder, not changed. The spreadsheet tool's version history is also available if you need an earlier state.
