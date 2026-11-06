# Demo video plan and result (not sent)

**Owner who accepts it:** product manager. **Environment:** staging site, test account "Test Rider" with invented data.

## Script (excerpt)
| No. | Screen and action | Subtitle | Chapter |
|---|---|---|---|
| 1 | Home page, click "Book a service" | "Start from the home page." | Start |
| 2 | Choose "Standard service", pick Saturday | "Pick a service and a day." | Choose |
| 3 | Enter test details, pay with the test card | "Enter your details." | Pay |
| 4 | Confirmation page and test email | "You get a confirmation straight away." | Confirm |

## Step removed
**"Track your repair" is not in the video.** It does not exist yet, and a mock-up would show something the product cannot do. Alternative: end with a subtitle saying "Repair tracking is planned" if the owner wants to mention it, labelled as planned.

## Capture
Playwright script `capture-service-order`, fixed 1280 by 720 viewport, video recording on, run against staging. One failed run (the date picker did not load); fixed the wait in the script and re-ran. Idle waits on the payment step were sped up 2x and this is declared on screen.

## Inspection
Played at full length (58 seconds) and stepped through 14 key frames. Chapters at 0:00, 0:12, 0:30 and 0:46. Subtitles match the narration and the sync is within a line. One fault: at 0:41 a browser notification showed an unrelated email subject. Notifications turned off; re-captured.

## Personal data check
After re-capture: all names are invented, the email is on an example domain, the card number is the test card, no tokens or keys in the address bar, no private tabs. Clear.

## Status
Ready for the owner's approval. **Not sent to the sales list.** Sending is the owner's decision and waits for a yes.
