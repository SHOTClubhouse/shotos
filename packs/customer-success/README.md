# customer-success pack

**Skills for handing an account to the person who will deliver for it, and for recovering an onboarding that has stalled.**

Both skills work from evidence, keep facts separate from opinions and draft any message for a person to send. They help a customer success lead, an account manager or a founder who is still doing both jobs.

## Who it is for

- Customer success and account managers who receive accounts from sales.
- Founders handing early customers to a first success hire.
- Delivery leads who find an onboarding has gone quiet.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [success-handoff](skills/success-handoff/README.md) | Own | Hands an account to the person who will deliver. Lifecycle stage, health and transfer status are kept separate; transfer is only complete once accepted. |
| [onboarding-recovery](skills/onboarding-recovery/README.md) | Operate | Diagnoses where a stalled onboarding stopped, proposes the smallest next step to first value with an owner and date, and drafts the message. |

## Needs

Read-only first, and drafts instead of sends, throughout.

- **Mail connector:** read threads with the customer; create drafts. Sending is not needed and should stay off.
- **Calendar connector:** read meetings held and booked.
- **Document connector:** read account notes, proposals and onboarding plans; write the handoff record where the owner names.
- **Transcript connector:** read call transcripts, optional. Pasted notes work too.
- Without a connector, the skills work from pasted text and name what they could not check.

## Install

From your own project folder, with SHOTos cloned next to it:

```
python ../shotos/install.py --runtime claude --scope project --pack customer-success --dry-run
python ../shotos/install.py --runtime claude --scope project --pack customer-success
```

Use `--runtime codex` or `--runtime agents` for other agents, and repeat `--pack` to add several packs at once. To add a pack to a project that already has SHOTos, run `python ../shotos/install.py --uninstall`, then install again with every pack you want. Files you changed are kept. If a changed file is in the way, the reinstall stops: move it aside (or keep your copy and skip that skill) before you reinstall.

Using the Claude app, ChatGPT or another chat assistant instead? See [where to run SHOTos](../../docs/running-it.md).

## How it connects

Both skills apply the four rules in [docs/controls.md](../../docs/controls.md). The handoff follows the same idea as [evidence-handoff](../../skills/evidence-handoff/README.md): say what is known, from where, and what is not. The stages are in [docs/framework.md](../../docs/framework.md). In the win-the-work pipeline, LEAP's Plan hands over into Scope, which is where a handoff starts.

**Evidence:** Cases written, not yet run. Eval cases are in [evals/packs/customer-success.json](../../evals/packs/customer-success.json).
