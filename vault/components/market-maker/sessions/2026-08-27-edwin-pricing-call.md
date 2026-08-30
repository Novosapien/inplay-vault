---
description: "The 27-08 Edwin pricing call: the seed verified against his live LSU numbers, the forward re-rate gap found, and the futures rebase proposed as the answer"
---

# 2026-08-27: Edwin's pricing call — the seed verifies, the tail does not

> **Who:** George + Claude · call with Edwin, Cody, Troy, Kevin
> **Type:** call (ingest + analysis) — same day as the earnings rulings
> **Refs:** [[27-08-2026-mm-pricing-catchup]] ·
> [[market-maker/systems/expected-wins-pipeline]] · `E51` `E52` `N73`

## What we did

- Ingested the 27-08 pricing catch-up. Analysed it against the pipeline
  design and the seed we built the same day.
- Checked Edwin's spoken numbers against our seed file.
- Found one gap between his expectation and our build. Proposed a fix that
  needs no new model.

## What we learned

### The seed is correct — verified against numbers Edwin quoted live

He worked LSU through on the call. Every number matches our seed file:

| Quantity | Edwin, on the call | Our seed |
|---|---|---|
| IPO price | "$59 or 59.53" | 59.54 listed |
| Expected wins | "8.55" | 8.5452 |
| On-field baked in | "$42.75" | 42.73 |
| Reference price | — | 60.87 (= his sheet's IPO EV 60.874) |

This is the strongest check the seed has had. The numbers come from his
own de-vig code, and they reproduce what he says out loud.

### He described our absorber, unprompted

Edwin: "a win to LSU is not going to be worth $5 more a share because part
of that is already baked into the price." He put the move at **47 cents to
$1.50** for a heavy favourite.

Our rule gives exactly that. A 90.6% favourite that wins moves
`$5 × (1 − 0.906) = $0.47`. A 70% favourite moves `$5 × 0.30 = $1.50`.
The absorber is his model. No change needed.

### ⚠ The gap: he expects the tail to re-rate at once

Edwin on LSU losing to Jacksonville State: "that share could go down 10 or
$15."

Our absorber alone gives `$5 × (0 − 0.906) = −$4.53`. The other $5 to $10
is the re-rate of the games still to play — layer 3, which we deferred.
**His mental model includes the far-tail re-rate. Our build does not.**

### ⭐ The fix needs no model — it is the rebase we already specced

Edwin wants InPlay-owned probabilities, not Sportradar ones. His mechanism:
"we can extrapolate what the point spreads are… into a fair value win
percentage", and "the point spreads come out like Sunday for the next week."

Point spreads only cover the next week. So spreads alone re-rate one game
at a time, and a week-1 shock never reaches week 10. That does not produce
his $10 to $15.

**The whole-season futures line does.** A bookmaker cuts LSU's season win
total after a bad loss — from 8.5 to about 6.5. Re-de-vig that line and
expected wins fall about 2 wins, so the price falls about $10. That is his
number, from market data alone. It needs no Elo engine and no internal
probabilities, so §1.5 stays intact.

This is §7 of the pipeline page, already designed:

    EXPECTED_WINS_REBASE:  E ← devig(new snapshot) − banked

**What it needs: a weekly win-totals snapshot instead of a single one.**
Same source as the seed, pulled every week.

### ⚠ His spoken off-field numbers disagree with his own sheet

| Team | Edwin, on the call | His sheet (our seed) |
|---|---|---|
| Dallas Cowboys | "like 30 bucks" | 24.07 |
| Carolina Panthers | "12 bucks or 14 bucks" | 19.22 |

The spread he describes is far wider than the sheet's — about 2.2× top to
bottom, against the sheet's 1.25×. Off-field is roughly 30% of a share's
price, so this is material. **He offered to send the popularity file.**
Take it, and re-seed off-field from it.

### Confirmed, no action

- **Off-field actual is trading volume.** George asked directly. Edwin
  confirmed.
- **Off-field expected is his popularity model** — socials, prime-time
  games, market size.
- **The season resets.** Edwin: "what I've designed is a reset." No
  multi-year value. Settlement at season end stands.
- **Games remaining drive the re-rate size.** A win with 11 games left
  matters more than a win with 1 left.

### New scope, not ours alone

Cody and Edwin want InPlay's own market data stored, queryable and
resold — "our first proprietary market data set." The data is our venue
prints. The earnings report reads the same prints. One store serves both.
Logged as `N73`.

### E34 stays open, and the call sharpened it

Troy asked what the maker does when a participant pushes the price $5.
Edwin answered that the market corrects itself. Our analysis says the
maker's `IA` band is ±$0.25, so the market cannot move the price that far.
The two positions still disagree. Nothing changed; the disagreement is now
on record from both sides.

## What went wrong / got stuck

- Edwin promised a new formula "today" (27-08). It has not arrived. It may
  supersede parts of this analysis, so hold the layer-3 build until it
  lands or he confirms the rebase.
- The app shows 1,000,000 NCAA shares available on the IPO lot. It should
  show the remaining float. George to check with the app team. Not a market
  maker defect.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- 📝 The seed is verified against Edwin's live LSU numbers. It stands.
- 📝 The absorber matches his model exactly. No change.
- 🟡 Proposed: the weekly futures rebase answers the forward re-rate,
  with no internal model. Needs his ruling — `E52`.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **E51(d) updated** — his spoken off-field numbers disagree with his
  sheet. Request the popularity file he offered.
- **E52 opened** — the forward re-rate: the $10–15 expectation, the rebase
  proposal, the weekly win-totals feed, the point-spread question, and his
  promised formula.
- **N73 opened** — the market data store for our own venue prints.

## The production check (read-only, same session)

George asked for a live check, with care — the system is in production. No
restarts, no writes, no config changes. Only `ps`, `ls`, and `cat`.

**What runs.** VM `inplay-market-maker` (project `inplay-497712`, zone
`us-east4-a`, n2-standard-2, no external IP, IAP-only SSH). Two processes:
`mm.runtime` up ~7 hours on journal `supervised47`; `snt.runtime` up 5
days. `MM_MODE=supervised` · `MM_READINGS=bus` · `MM_CONFIG_VERSION=CFG-0045`
· `MM_PRIOR_RUN_DIR=/var/lib/mm/supervised46` (anchors carried across the
cutover, per F2) · `MM_BOOT_HEAL=off`.

**The maker quotes 138 NCAA books**, from
`/home/georgewestbrook/supervised-inputs-138-ncaa.json`. NFL tickers are
NOT in `MM_SECURITIES`.

⭐ **The seed is verified against production.** Our seed file reproduces
the live file for all 138 tickers:

| Difference | max | median |
|---|---|---|
| expected wins | 0.0005 | 0.0002 |
| off-field | $0.005 | $0.0025 |
| **reference price** | **$0.0061** | $0.0026 |

The only difference is precision — the live file rounds to 3 decimal
places, our seed carries full precision. **Nothing needs deploying.**

⚠ **Correction to an earlier claim in this session.** We first compared
against `docs/supervised-inputs-2026-08-07.json` and reported that our seed
would move live books by up to $6.74. That file is a **stale 7-ticker NFL
artefact** in the repo and is not what runs. The real comparison is above.

⭐ **The real hole, now measured.** `t_effective_time` is
`2026-08-11T22:00:00.000Z` for all 138 teams. **Expected wins have been
static for 16 days and no path exists to update them.**
`realized_on_field_total` and `realized_off_field` are both `0.00`.

Saturday still prices correctly — the engine holds each finished game in G
with its result pinned. **But the first regenerate of that file without
absorption drops every winning team by $5.** The absorber is the critical
path, not an improvement.

**The off-field discrepancy is NFL-only.** The live NCAA file uses the same
off-field source as our seed. The wider numbers Edwin quoted (Dallas ~$30)
appear only in the old NFL file. Nothing is mispriced today, because NFL
books are not quoted. Settle it before NFL secondary opens.

## Next

- Build the absorb path. It is the only thing between us and a broken price
  after the first file regenerate.
- Send `E51` and `E52` to Edwin as one message. Ask for the popularity file
  and a weekly win-totals snapshot in the same message.
- Add NFL to the universe and settle its off-field source before NFL
  secondary opens.
