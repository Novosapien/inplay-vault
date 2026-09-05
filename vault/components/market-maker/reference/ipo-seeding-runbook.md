---
description: "How the IPO offering is seeded and rested at tZERO — the access paths, the four phases, the 5 Sep procedure beside a live maker, and every trap two runs found"
---

# IPO Seeding — the runbook

> **Component:** [[market-maker/market-maker]]
> **Written:** 2026-08-20, from the run of 19–20 Aug that seeded all 170 team
> companies and rested the full $8.34bn offering.
> **Source session:** [[market-maker/sessions/2026-08-19-c-ipo-test-rig]] ·
> decisions [[market-maker/decisions]] 2026-08-19e
> **Scripts:** `inplay-market-maker/scripts/ipo/` (PR #58)

Read §2 before touching anything. Three of its traps cost real shares on the
first run, and two of them are silent.

---

## 1 · What "seeding the IPO" actually is

Two separate things, in this order:

1. **The maker HOLDS the float** — 900,000 per NFL team, 1,000,000 per NCAA
   team, 166,800,000 shares across 170 books. This is a *position* at tZERO and
   appears on no order book.
2. **The maker OFFERS it** — one resting sell per team at that team's listed IPO
   price. This is an *order*, and it is what participants buy from.

They are done by different mechanisms over different transports, which is the
single most confusing thing about the job. Holding without offering shows
nothing on any book; offering without holding is a naked short the venue will
reject.

⚠ **The app has its own IPO path and it is NOT this one.**
`inplay-trading-service`'s `ipo_engine.execute_ipo_buy` fills internally against
`asset_shards`, debits the wallet and never calls tZERO. The two legs are
independent. If both run, the venue ask and `assets.ipo_ask_price` must be the
same number or one share is on sale at two prices.

---

## 2 · The traps — read these first

| Trap | What happens | What to do |
|---|---|---|
| **`9387 TxfrCost` is a PRICE PER SHARE** | The spec writes `(TxfrCost / TxfrQty) = averagePrx`, which reads as a total. The venue disagrees. Measured on both MPIDs 19-08: 6 shares at 11.00 moved the basis by exactly 66.00. Sending the total at 900,000 shares is wrong by a factor of 900,000 | Send the **price**. `scripts/ipo/allocate.py --cost-unit` defaults to `per-share` |
| **UPT is one-way** | A positive transfer applies; a NEGATIVE one is accepted (`UPTa`, delta echoed) and **never moves the position**. Measured 05-08, re-confirmed 19-08 | To reduce a position use UEPR, never a negative UPT |
| **UEPR `Qto` is an ABSOLUTE OPENING balance** | `Qt (current) = Qto + session activity`, and UPT transfers land in *activity*. So `Qto = target` does NOT give `Qt = target` | Three steps: set `Qto=0` → read (that reading IS the activity) → set `Qto = target − activity` |
| **A `Qto=0` "no-op" is only a no-op on a symbol the account has never traded** | The route's doc says so; the qualifier is load-bearing. One such probe on 19-08 **destroyed 99,663 maker shares** | Read the position BEFORE any UEPR. Never probe with `Qto=0` on a live book |
| **TIF DAY dies silently at 00:01 ET** | 170 asks worth $8.34bn were gone from the venue at 04:01:34Z with **no `DONE_FOR_DAY`, no `39=3`, no execution report at all**. The gateway still reported `open_orders: 170`, so its tracker and the venue had fully diverged | Rest **GTD** with `expireTime` at the window close. ⚠ GTD across a boundary is still UNPROVEN — see §6 |
| **The dead-man sweeps the whole offering** | The gateway cancels every resting MM order when the maker heartbeat stops. It arms on a heartbeat OR on a restart that rehydrates orders, then fires after the grace | Raise `MM_DEADMAN_TIMEOUT_MS` and `MM_DEADMAN_BOOT_GRACE_MS` past the window while the maker is stopped. **Restore them before the maker runs again** |
| **Reading a position costs a VISIBLE order** | There is no query message — Request For Positions exists in neither tZERO spec. Tags 9383/9384 ride any execution report, including a plain `39=0` accept | Rest a 1-share order priced away from the market. ⚠ Participants can see it. Read **before** a window opens, never during |
| **The cost basis is an instruction, not a setting** | `9382 Eto` and `TxfrCost` may be re-derived by the venue at its own mark — one reversal landed $317.05 off, pricing at the last trade | **Plan on the quantity, read the basis back** |
| **On an EMPTY book the reads set the price-band anchor** (5 Sep) | The half-price read bids became the sell-side anchor; all 32 asks at the IPO price were refused `Passive SELL … 85 percent ABOVE the ASK(half price)`. A bid cannot move it: a BUY above the ask is *aggressive*, 3% band | Rest a **1-share passive SELL at 0.9 × IPO** (`read_positions.py --side sell --price-frac 0.9`), wait ~4 min, **cancel it** (`cancel_reads.py` — a resting hop counts against `Pos − livS`), rest the ask within seconds. Proper fix: tZERO sets an IPO Reference Price (T-item) |

---

## 3 · Access — two paths, and the credential trap

### Positions → the gateway's HTTP ops server

Not the admin proxy, not NATS. On the VM `inplay-fix-gateway` (10.0.1.2),
reached over IAP:

```bash
gcloud compute ssh inplay-fix-gateway --zone=us-east4-a \
  --project=inplay-497712 --tunnel-through-iap --command='
  K=$(sudo grep "^OPS_API_KEY=" /opt/fix-gateway/.env | cut -d= -f2-)
  curl -s -H "X-Ops-Key: $K" localhost:8080/positions/house'
```

Auth is the `X-Ops-Key` header; the value is `OPS_API_KEY` in
`/opt/fix-gateway/.env` (root-only). **Read it in place with sudo — never copy
it out.** An empty key disables the mutating routes rather than opening them.

| Route | Message | Use |
|---|---|---|
| `POST /position-transfer` | 35=UPT | add inventory (positive only) |
| `POST /position` | 35=UEPR | set the absolute opening quantity |
| `GET /positions/house` | — | the house book per bot and symbol |
| `GET /orders/mm` | — | open MM orders as the gateway sees them |
| `GET /quotes` | — | the venue's own top of book |
| `POST /orders/mm/prune` | — | retire stuck `PENDING_NEW` phantoms |

⚠ **UPT and UEPR replies never return to the caller.** `UPTa`/`UPTx`/`UEPRa`
land on the FIX session and in the log only, so an HTTP timeout says nothing
about whether the venue applied the change.

### Orders → NATS, and the credential is the trap

NATS is VPC-only and the gateway VM has no client library, so orders are
published over a raw socket from the VM (`natspub.py` in the session scratch;
worth committing next time).

| Subject | NATS user | Secret Manager |
|---|---|---|
| `gateway.orders.mm.new` / `.cancel` / `.cancel_all` | **`market-maker`** | `inplay-nats-mm-token` |
| `gateway.orders.new` (retail probes) | `trading-service` | `inplay-nats-trading-token` |

⚠ **`trading-service` and `admin` are both REFUSED** on `gateway.orders.mm.*`
with a `Permissions Violation`. This is not obvious and cost the first run
twenty minutes.

**ClOrdID rules:** must start with `MM` on the mm namespace
(`MM_PREFIX_REQUIRED`), at most 20 characters, no leading zero. Maker scheme is
`MM` + 16 hex of a SHA-256 seed; taker is `MMSN` + 14 hex.

### The wire log is the authoritative record

`/opt/fix-gateway/data/log/FIX.4.2-FHINPLAY01-TZFIXORDQA.messages.current.log`
(sudo; current session only). Everything the venue actually said is here and
frequently nowhere else.

### Identities

| | account | userId | botId |
|---|---|---|---|
| Maker | `1797733477` | `384925384799470102` | `mm-1` |
| Taker | `4963224393` | `385656921832584863` | `snt-1` |

Both trade as MPID **IPLM**; retail is **IPLY**. **Positions are PER ACCOUNT**,
so seeding the maker gives the taker nothing.

---

## 4 · The four phases

### Phase 0 — the price file

```bash
uv run python scripts/ipo/prices.py --source vault   # the v1.0 model
uv run python scripts/ipo/prices.py --source app     # teams.ts
```

`--source` has no default. The two agree on 137 of 170 tickers and differ on 33,
by up to $21.59. ⚠ Neither is necessarily what the app charges — that is
`assets.ipo_ask_price` in the trading-service database (**N51**, still unread).

Quantities are never a flag: they come from `mm.universe`.

### Phase 1 — READ every book first

**Do not skip this.** On 19-08 every one of the 170 books already held 79k–108k
shares from the maker's ordinary quoting — 17.8m in total. Adding the float
blindly overshoots every book by a different amount, and UPT cannot be undone.

One 1-share order per team, priced at half the IPO price so it rests without
crossing, GTD 2–4 minutes so it clears itself. Parse `9383`/`9384` off the
accept in the wire log.

### Phase 2 — transfer the DIFFERENCE

`float − held`, at the listed price, one UPT per book. Skip anything already at
or above its float. Ledger the intent BEFORE the wire call and resume off the
**intent**, not the success — a transfer can apply without answering.

### Phase 3 — rest the asks

One sell per team, side **2** (a long sale, never 5), at the listed price, **TIF
GTD** with `expireTime` at that league's window close:

| League | Window closes | `expireTime` |
|---|---|---|
| NCAA | 26 Aug 22:00 ET | `2026-08-27T02:00:00Z` |
| NFL | 6 Sep 22:00 ET | `2026-09-07T02:00:00Z` |

Dates are IPO Requirements v3 §1.1 — the same source the trading service derives
its market phase from, so the venue asks and the app cannot disagree about when a
window ends.

✅ **The venue accepts a single 900,000-share order.** No laddering is needed;
`--clip` exists only if that ever changes.

### Phase 4 — verify off the asks' own accepts

The sell's accept carries `9383`, so the offering reads the position backing it
— no second sweep of visible probe orders. Check every line is `39=0` with
leaves equal to the float and a position at or above it.

---

## 5 · Taking it down

`scripts/ipo/cancel_orders.py` reads the run's ledger and cancels each ClOrdID
precisely. Prefer that to `--sweep`: `cancel_all` is **global** and takes down
every resting MM order, including the maker's quotes once it is running.

⚠ **The ledgers are the only record of which ClOrdIDs were used.** The 19-08 run
kept them in `/tmp/ipo/` on the VM, which does not survive a reboot. Put them
somewhere durable.

---

## 6 · Still open

1. ~~**Does GTD survive the 00:01 ET boundary?**~~ ✅ **Yes — proved 05-09** (N78): the 32 NFL asks rested GTD across the 6 Sep 00:01 ET boundary and the venue's MD feed showed all 32 at 04:02Z and 11:15Z. Original text: Unproven. DAY definitively does
   not, and the vault's earlier belief that it did was an inference from silence.
   ⚠ **Prove this before an offering is left resting overnight** — one GTD order
   on a `.TEST` twin answers it and costs nothing.
2. **Which price set does the app charge?** (**N51**) `assets.ipo_ask_price` has
   still not been read.
3. **Why does `Eto` not apply as sent, and what price is the venue marking at?**
   (**N68**) It looks like the last traded price.
4. **The re-issue question.** Topping a traded book back to its float re-issues
   the shares that sold: the buyers keep theirs and the maker is whole again, so
   more shares exist than before. Right for a test, wrong for anything real.

---

## 7 · What the first run got wrong

Recorded because each one is cheap to repeat:

- **Seeded before reading.** Caught in the dry run only because the Eagles book
  turned out to be 59,702 in.
- **Sent `TxfrCost` as a total.** Would have set a basis 900,000× too high on
  all 170 lines, unfixable by UPT.
- **Probed a live account with `Qto=0`.** Destroyed 99,663 shares.
- **Rested DAY.** The whole offering vanished overnight with no message.
- **Read positions during the day.** 170 one-share bids appeared on public books
  and were noticed immediately.
- **Believed the gateway's order count.** It said 170 open while the venue held
  none.

---

## 8 · 5 Sep — an offering beside a LIVE maker (the NFL run)

The 19-08 procedure stops the maker for the whole offering. On 5 Sep the NCAA
maker had to run while the NFL offering rested. What made that safe, and what
the run found, is in the session note
[[market-maker/sessions/2026-09-05-power-up-and-nfl-offering]] and in
`scripts/ipo/README.md` §5 on `inplay-market-maker@feat/ipo-nfl-offering`:

- Post the offering under a **distinct `userId` and `botId`** on the maker's
  account. The maker adopts only acks on its own user id; the dead-man sweeps
  only its own bot. Never `cancel_all`; no gateway restart for the window.
- Removal is **UEPR** (`set_position.py --mode zero`), never UPT. Then the read,
  then `--mode target` (Qto = float − activity). On 5 Sep every read returned
  `9383=0` after the zero, so Qto was the full float.
- **The anchor trap** (§2, last row) cost the first 32 asks. The hop recipe
  rested all 32 on the second pass: 28,800,000 shares, $1,836,063,000, GTD
  `2026-09-07T02:00:00Z`, every accept `39=0` with `9383=900000`.

