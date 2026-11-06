# DORA metrics and AI measures

## What it is

DORA is the DevOps Research and Assessment programme, a long-running research effort now run within Google Cloud, which studies what separates teams that deliver software well from those that do not. Its annual reports and the book *Accelerate* by Nicole Forsgren, Jez Humble and Gene Kim describe a small set of measures, often called the four keys, that predict both delivery results and organisational outcomes. SHOTos uses them in the Check step for any work that ships software.

## The four keys

| Measure | What it asks | Direction |
|---|---|---|
| **Deployment frequency** | How often do we put a change into production? | More often is better |
| **Lead time for changes** | How long from a change being committed to it running in production? | Shorter is better |
| **Change failure rate** | What share of deployments cause a problem that needs a fix, a rollback or a patch? | Lower is better |
| **Time to restore service** | When a failure reaches users, how long until service is back? | Shorter is better |

The first two describe **throughput**. The last two describe **stability**. The research finding that matters most is that these move together: teams that deploy often and quickly also tend to break things less and recover sooner. Speed and safety are not a trade, provided the practices in [engineering-excellence.md](engineering-excellence.md) are in place.

More recent DORA reports add **reliability**: whether the service meets the expectations users have of it, such as availability and response time. Treat it as a fifth measure, set against an objective you have agreed, for example "the page loads in under two seconds for nine requests in ten". The numbers in that example are illustrative.

## Why it matters with agents in the loop

Agents raise the volume of change. The four keys tell you whether that volume is reaching users safely or only piling up. A rise in deployment frequency with a rise in change failure rate says the team is writing faster than it is checking. A fall in lead time with flat failure rate says the gain is real.

They also give a fair baseline. Take the measures before agents join the work and keep taking them. That is the only honest way to say whether the agents helped.

## How to measure each, simply

Start with whatever you can count today, even by hand. A rough number you trust beats a precise number nobody checks. Write down how you counted so that next month's number is comparable.

- **Deployment frequency.** Count production deployments per week from the pipeline's history or the release log. Report the count, not an average, if the number is small.
- **Lead time for changes.** For a sample of recent changes, record the time of the commit and the time it went live. Report the median, since a few slow outliers distort the mean. Version control and the pipeline already hold both timestamps.
- **Change failure rate.** Of the deployments in the period, count how many needed a rollback, hotfix or patch. Divide by the number of deployments. Agree in advance what counts as a failure, otherwise people argue about it afterwards.
- **Time to restore.** For each incident that reached users, record when it started and when service was back. Report the median. The incident log or the blameless review (see [continuous-delivery-and-devops.md](continuous-delivery-and-devops.md)) is the source.
- **Reliability.** Choose one or two user-facing measures, such as availability or a page-speed threshold, from monitoring.

If you have no pipeline history, begin with a spreadsheet: date, change, committed at, live at, failed yes or no. Four weeks of rows is a baseline.

## Extra measures for AI features

When a feature includes an AI component, add these, since the four keys do not see its quality or its cost.

- **Eval pass rate.** The share of cases in the eval set that pass the agreed checks. Report it for each release, and keep the set fixed so that numbers compare. See [evals-for-ai-output.md](evals-for-ai-output.md).
- **Cost per accepted task.** Total spend (model usage plus tool costs, and optionally the human time) divided by the number of outputs a person accepted. Raw cost per call hides waste when many outputs are rejected.
- **Latency.** How long users wait, as a median and as a slow-end figure such as the slowest tenth of requests.
- **Human edit rate.** The share of outputs a person changed before accepting. A falling edit rate over many samples is the evidence behind moving a task up the autonomy ladder; see [control 12, graduation](../rules/12-graduation.md).
- **Rejection and escalation rate.** How often outputs are thrown away or handed to a person.

## The trap: measures that become targets

When a measure becomes a target it stops being a good measure. This is Goodhart's law, and it applies hard here.

- Set a target for deployment frequency and people split changes into trivial ones to inflate the count.
- Set a target for change failure rate and people stop reporting failures.
- Set a target for lead time and people skip review.
- Set a target for eval pass rate and the eval set quietly gets easier.
- Compare teams by their numbers and each team starts defending its figures instead of improving its work.

The DORA researchers say plainly that the measures are for a team to understand and improve its own system, not for ranking people or teams. Use them as follows.

1. **Use trends, not thresholds.** Look at direction over months.
2. **Pair throughput with stability.** Never report one half alone.
3. **Keep the team as the audience.** The team reads the numbers first and chooses what to change.
4. **Ask "what is the constraint?"** If lead time is long, find where changes wait: review, testing, approval, the release window. Fix that, not the number.
5. **Keep the eval set sacred.** Changing cases to raise the rate is a decision for the owner, recorded with a reason.

## What good looks like

- A baseline taken before the work started, with the method written down.
- The same measures every period, reported together.
- Each figure sourced from a system or a log, not memory.
- A short note on what the team changed because of the numbers.
- Honest gaps: "not measured" when it is not measured.

## Anti-patterns

- **Dashboards without decisions.** Nobody acts on them.
- **Individual league tables.**
- **Precision theatre:** two decimal places on a sample of six.
- **Comparing teams** that work in different contexts.
- **Counting agent activity** (lines written, tasks started) instead of outcomes.
- **Reporting only the good measures.**

## How it maps to the steps and rules

- **Brief:** record the baseline, or record "not measured".
- **Check:** report the measures against the baseline and decide to scale, pivot or stop.
- **Hand over and Improve:** the receiving team keeps measuring, so improvement continues without the builders.
- **Rule 4, claim only what you can show:** every figure has a source; estimates are labelled.
- **Control 12, graduation:** human edit rate and acceptance counts are the evidence.

## A short example

Millbrook Rovers' volunteers maintain a booking site. In the brief they have no pipeline history, so they log changes by hand for a month: three deployments, a median of nine days from commit to live, one rollback. Three months after adding automated tests and an agent that drafts changes, the invented numbers are twelve deployments, a median of two days and one rollback. The coordinator reads this as better throughput with stable failures, but notes the sample is small and says so in the report. The AI-drafted reminder emails have an eval set of twenty cases. The pass rate rises from 14 to 18 passing, the human edit rate on a sample of forty sent reminders is about a third, and the cost per accepted reminder is a few pence. The coordinator keeps the task at draft-only until the edit rate has stayed low for much longer.

## Further reading

- Nicole Forsgren, Jez Humble and Gene Kim, *Accelerate*.
- The annual *State of DevOps* and *Accelerate State of DevOps* reports from DORA.
- Jez Humble and David Farley, *Continuous Delivery*.
- Betsy Beyer and others, *Site Reliability Engineering*, on service objectives.
- Charles Goodhart's observation and Marilyn Strathern's phrasing of it, widely discussed under "Goodhart's law".
