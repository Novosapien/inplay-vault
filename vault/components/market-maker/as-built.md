# The Market Maker — As Built

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The authoritative description of how the machine is ACTUALLY
> built — for agents working on it and for humans reading it. Key equations
> as implemented, the key sections of the machine, and where each lives in
> code. Updated 2026-08-06.
>
> **Authority chain:** [[market-maker/decisions]] (dated rulings) outranks
> the **v1.3 Build Spec** (`standards/MM-build-spec-v1.3.html`), which
> outranks the CTS/PTS standards (historical context). This document
> describes the result — where the build deviates from the spec, the
> deviation is named here and sourced there.
>
> **Maintenance rule:** a session that changes the machine updates this
> document (part of the session loop in [[market-maker/working-guide]]).
> Repo-side detail lives in `inplay-market-maker/docs/BUILD-LOG.md`
> (traceability matrix, session log); this document is the shape and the
> mathematics.

Repo: `inplay-market-maker` (Python 3.12, `src/mm/`), 534 tests, ruff +
`mypy --strict` clean. The Sportradar publisher lives in
`inplay-sportradar-service` (`app/workers/mm_publisher/`), 577 tests.

---

## 1 · The machine in one paragraph

The market maker prices 170 team securities (32 NFL + 138 NCAA) and rests
two-sided limit-order ladders around its own fair price on tZERO's book.
Everything is an **event**: inputs arrive as envelopes, an acceptor
validates, deduplicates and journals them, and every engine downstream is a
pure function of the accepted stream — so replaying the journal reproduces
every price, every order and every suspension **byte-identically**. One
process, one journal, one writer. A 1-second runtime loop is the only code
that reads a clock.

## 2 · The core shape — events, the journal, replay

**Section: `mm/events/` (§7.1–§7.5, §1.6-4).**

- **Envelope (§7.1)** — `events/envelope.py`. Every input is an
  `EventEnvelope`: type, idempotency key, provider/receive times, payload,
  and a canonical payload hash (`sort_keys`, compact separators). The
  constructor **rejects binary floats anywhere in the payload** — §1.6-3:
  all numbers are `decimal.Decimal` or exact strings, end to end.
- **Acceptor (§7.2–§7.4)** — `events/acceptor.py`. The pipeline order is
  fixed: validate (Business Validated, §3.2.1 sum check at the door) →
  dedup → journal → sequence. Outcomes: `ACCEPTED` (gets the next Accepted
  Event Sequence), `DUPLICATE` (same key, same hash — quiet), `CONFLICT`
  (same key, **different** hash — a data-integrity alarm, §7.3),
  `REJECTED` (audited with the reason).
- **Idempotency keys (§7.3)** — `events/idempotency.py`. The load-bearing
  ones:

  | Event | Key basis |
  |---|---|
  | `PROBABILITY_UPDATE` | source · game · `last_updated` (stands in for the provider sequence SR lacks — D-2) |
  | `OFFICIAL_RESULT` | source · game · result version (always `1`; a correction is version 2, a new fact) |
  | `EXECUTION` | venue · **client order id** · exec id — ✂ supersedes the spec's key; tZERO recycles ExecIDs (proven by incident) |
  | `VALUATION_SWEEP` | the scheduled instant alone (a late sweep keeps its slot's identity) |

- **Journal** — `events/journal.py`. Append-only JSONL, fsync per accepted
  event, **one writer by design** (`[second-writer]` is a stop condition —
  this is why the engine is a VM process, not Cloud Run, and why there is
  no hot standby). ⚠ N31: group commit is designed-not-built; the fsync is
  the machine's throughput ceiling.
- **Determinism (§1.6-4)** — no wall-clock reads inside any engine, no
  map-iteration-order dependence, no unseeded randomness (every draw is a
  SHA-256 over named context, §5.7.3). `acceptor.replay()` rebuilds all
  state; replay equality is proven on a real captured game.

## 3 · Data in — the four paths

**Section: `mm/adapters/` · `mm/poller/` · the service's `mm_publisher/`.**

1. **Sportradar readings over the bus** (the 05-08c ingestion ruling; built
   and drilled 06-08b). The **sportradar service** polls SR per game at
   tiered cadence and publishes each reading on **JetStream** (stream
   `SR_PROBABILITIES`, subjects `sr.probabilities.reading.{game}`, week
   retention). ⭐ **Every successful fetch publishes** — a poll that finds
   nothing new re-offers the newest reading under a fresh `Fetched-At`
   header: the body dedups at the MM (§7.3), the header is the liveness
   proof (E38). `Nats-Msg-Id` = `{game}:{last_updated}:{fetched_at}` — one
   publish attempt, so the bus dedups retries, never deliberate re-offers.
   The MM side: a durable subscription (`mm-engine`) feeds a queue;
   `poller/consumer.py` drains one submission per call; **acks flush only
   after the tick journalled the batch** (pop → journal → ack — a crash
   anywhere costs a redelivery, never a loss). Malformed messages are
   acked away and counted (poison must not jam the durable).
   `adapters/sportradar.py` builds the envelope — the SAME envelope the
   file path builds, enforced by a shared constructor and proven
   1,089/1,089 on the real capture.
2. **File replay** — `load_timeline` + `timeline_to_submissions`
   (`parse_float=str`; a binary float never exists). The test harness and
   the certification tool. The in-engine poller (`poller/worker.py`) still
   owns this path plus the heartbeat; **it retires from live wiring at
   go-live** (George, 06-08b).
3. **Edwin's daily reference file** — `adapters/reference_feed.py`. One
   JSON file, all 170 teams, 06:00 ET daily: `expected_remaining_wins`
   (**T**), `sigma`, `games_remaining`, `effective_time`, `revision`.
   The reader returns every violation at once. Transport is decided
   (upload page; bucket stores the file, database the rows) but not built
   — N19; the §7.3 event type for T is open — N23.
4. **Venue events** — the gateway publishes acks/fills/cancels on
   `order.mm1.>`; `adapters/gateway.py` translates to envelopes; the tick
   drains the subscription to empty every pass.

**Finals (N16):** nothing else in the platform publishes "game X is
final" — the MM mints `OFFICIAL_RESULT` version 1 itself, from a reading
whose SR status is `ended`/`closed`, outcome from the score. Both minting
paths share one constructor (`adapters/sportradar.py::result_envelope`).
A changed score under the same key raises a loud CONFLICT — §3.1.3 wants a
human, never an overwrite.

**Discovery:** the Sport Schedule endpoint (same entitlement as the
timeline) → the day's games touching the 170, daily, kickoffs converted to
the scheduler's monotonic clock once at the edge.

**Poll tiers** (γ the vault's numbers, `poller/scheduler.py` both repos):
LIVE **~2 s** (SR's measured median update gap is 4 s) · PRE_KICKOFF
**15 s** (interim, George's 10–30 range) · OVERNIGHT **30 min** ·
POST_GAME **10 min** through 1 h (the correction watch), then never.

## 4 · The valuation engine — what a share is worth

**Section: `mm/valuation/` (spec Ch 3).**

The Reference Price (§3.1.1):

    RP = ROF + Σ GEV(g) + RAV + EAV

realized on-field + expected value of unfinished games + realized and
expected off-field. **✂ The on-field leg is superseded** by Edwin's 28-07
formula (`reference_price.py::on_field_value`):

    on-field = $5 × ( T − Σ p_ref(g) + Σ x_g )        over g ∈ G

Start from the season's expected wins **T** (Edwin's file), subtract what T
assumed about every game that has kicked off since T's timestamp (the
frozen pregame probability `p_ref`), add what those games are actually
doing (the live probability `x`). `G` is a **set**: a game enters at
kickoff and leaves when a new T absorbs it. `p_ref` freezes **at kickoff**
(the closing pregame number — George's interim ruling, N22).

Per-game expected value (§3.1.2) and settlement (§3.1.3, §11.3):

    GEV(g) = P_win × $5.00 + P_tie × $2.50        (P_tie = 0 pending S6)
    realized: win $5.00 · tie $2.50 · loss $0.00
    FSV = realized on-field + realized off-field   (what a share pays)

**One reading, one event, two teams:** a probability reading is a fact
about a GAME (§7.3 keys it per game); the engine fans it out to both
securities, and the pair's values always sum to the game's full $5.00.

**Off-field (§3.6): mocked.** RAV/EAV arrive as static construction
inputs; the methodology is unbuilt.

**Freshness → status → confidence (§3.3–§3.5, `freshness.py`):**

- ⭐ **The E38 deviation — observation age, not reading age.** SR sends no
  heartbeat (`last_updated` moves only when the number moves; halftime is
  a measured 2,862 s gap), so §3.3.1's live bands run on **time since the
  last successful fetch**: a fetch confirms the number. Fetches landing →
  CURRENT at full status **through halftime and every stoppage**; true
  silence ages through Warning >5 s · Degraded >10 s · **Invalid at
  20 s → suspend**. Pregame stays on reading age (§3.3.2, permitted age
  from time-to-kickoff). Band values are Edwin's, unchanged — E38 takes
  the deviation to him with the measurement.
- **Status (§3.4):** most restrictive condition controls; demotions are
  instant, promotions earn one rung per served 10 s dwell (§3.4.1).
  **Invalid gates the cycle before any state is touched** — including σ²,
  because a dead feed's frozen price reads as CALM and would tighten the
  book into §2.3's danger case.
- **Confidence (§3.5):** 0–100, advisory, never touches the price; the
  status caps it.

## 5 · The position engine — inventory into a skew

**Section: `mm/position/` (spec Ch 4).**

    NP  = OpeningPosition + Σ fills + CorporateAdjustments      §4.1
    PR  = NP ÷ ReferenceFloat                                   §4.3
    EP  = NP + pending buy exposure − pending sell exposure     §4.4
    IA  = −Clamp( PR × S, −M, +M )       S = $1.00, M = $0.25   §4.5
    RM  = RP + IA        (floored by §5.4's MEV machinery)      §4.6

Reference Float = issued − treasury: **900,000 NFL / 1,000,000 NCAA**
(IPO Requirements v2, gospel; the unoffered NCAA 100k is N21). Pending
exposure includes Partially Filled remainders, and **exposure begins at
the decision to send** (intent registers before the wire — the gateway
never acks receipt). ⚠ Known holes, both external: the opening position
has **no publisher** (E27 — it is the entire day-one book) and the skew
**saturates at 25 % of float** (N20 — no distribution tool). Inventory
never prevents quoting (§4.1) — deliberately, we are the mandated buyer.

## 6 · The quoting engine — RM into a resting book

**Section: `mm/quotes/` (spec Ch 5, re-cut by the ASMM-1 adoption 30-07b:
Edwin's volatility-driven width replaced §5.2's state-classifier table).**

**σ² — the volatility number** (`volatility.py`), an exponentially-decayed
variance rate per security:

    r  = |RP − RP_prev| ÷ tick
    V ← V · exp(−ln2 · Δt ÷ h)            decay, half-life h = 20 s
    v  = r² ÷ Δt
    V ← v  if v > V   else  ½V + ½v       asymmetric: spikes land whole
    σ² = clamp(V · H, 0.05, 400)          horizon H = 30 s, in ticks²

**Width** (`width.py`):

    risk_width  = γ·σ² + C                γ = 0.02 · C = (2/γ)·ln(1+γ/k)
                                          k = 1.2 → C ≈ 1.653 ticks
    price_scale = clamp(RP ÷ $65, 0.6, 1.6)
    width       = ceil( clamp(risk_width, min, max) + extra·price_scale )
    bid_off     = ⌊width ÷ 2⌋ · ask_off = width − bid_off

The extra (0–3 ticks) is seeded, added never max'd, and only IT scales
with price. ⚠ **The equation has no wide end** (σ² ceiling caps width at
~$0.13 while overnight indication is $2.50–$5.00) — the per-state width
floor slot exists (`state_floor_ticks`) awaiting Edwin's E31 values.
Cold start: first σ² reads at the ceiling — wide-when-ignorant.

**Ladder** (`ladder.py`, §5.3/§5.4/§5.6 + the adopted shape):

    levels = 3–6, step = 1–4 ticks        drawn, seeded
    bid₁ = ⌊RM − bid_off·tick⌋ · ask₁ = ⌈RM + ask_off·tick⌉   outward
    walk outward by step; every price in [$0.01, MEV]; dedupe

A book that cannot be two-sided inside the bounds returns **Suspended — a
typed result, not an exception**.

**Quantities** (`quantity.py` + `variation.py`, §5.7):

    base_i = 10,000 × 0.72^i              i = 0 at the inside
    EPR    = clamp(EP ÷ RF, ±0.50)
    buy    = base × (1 − EPR) · sell = base × (1 + EPR)
    final  = clamp( round500( pre × VF ), 1,000, 15,000 )

VF is §5.7.3's seeded variation — SHA-256 over named context, byte-exact
against the spec's golden fixture, keyed on the Quote Version so replay
reproduces every draw.

**Publish or hold** (`quotes/engine.py`, §5.8/§5.10): republish only on
material change (IA moves ≥ $0.005, quantity basis moves ≥ 500 sh);
materiality is judged on the **pre-variation** shape (fresh random sizes
are never a reason to publish). The ASMM-1 dwell only permits a reshape —
it never forces one (N26). The §5.10 check battery runs every cycle; the
Quote Version increments **only on publish**. The whole chain carries the
triggering Accepted Event Sequence (§7.5) — event → RP → book is traceable.

## 7 · Market state — permission to quote

**Section: `mm/market_state/` (spec Ch 6).**

Four states — Stable / Active / Defensive / Suspended — per security.
§6.3's condition mapping in §6.2's precedence; demotions instant,
promotions one rung per served 10 s dwell (Suspended → Defensive is
dwell-free). The **kill switch is a journalled event** (`MANUAL_CONTROL`,
keyed on Control Action ID): global and per-security suspension replay
identically. A suspended security sweeps its resting orders **every
suspended cycle** (an order acked mid-suspension is caught next cycle).
⚠ Active/Defensive quote identically today — their widening is E31's
floor. ⚠ §6.3 vs §6.4.1 disagree on Recovery Ready (E37); the stricter is
implemented.

## 8 · The venue leg — the book onto tZERO

**Section: `mm/venue/` (spec Ch 8).**

- **Venue State Record** (`venue/engine.py`): every order's state incl.
  `DONE_FOR_DAY` (venue fact — the session ends 23:59 ET and DAY orders
  expire; the spec's table lacked it). Feeds PBE/PSE (§4.4).
- **The reconciler** (`venue/reconciler.py`) implements **rest-until-gone**
  (Edwin, 23-07 / N10): a still-wanted price is left alone, never topped
  up; a price move is one cancel-replace carrying the remainder
  (`CumQty + LeavesQty`); post-first ordering (N12); no replace ever
  relies on queue priority (§8.3). §5.9 replenishment is unbuilt — E17.
- **Sync** (`venue/sync.py`): register intent BEFORE publish (exposure
  never understates). ClOrdIDs mint deterministically: `MM` + 16 hex of a
  SHA-256 over pipe-joined context — no dots (the id becomes a NATS
  subject token).
- **Transport** (`venue/nats_transport.py`): one queue, one writer task,
  strict FIFO; a dead writer raises on the next publish. Time-in-force is
  **DAY** behind one constant (E36: the book vanishes nightly — Edwin's
  call which way it ships). The gateway's dead-man sweeps our book after
  4 s of heartbeat silence; its MM governor (50 msg/s, Hasan's
  placeholder) REJECTS over-limit messages.
- Wire-proven 02-08: the five-phase loopback test against the real gateway
  binary (heartbeat · post · move · kill switch · dead-man).

## 9 · The runtime — the only clock owner

**Section: `mm/runtime/` (loop.py · compose.py · `python -m mm.runtime`).**

The 1 s tick, in order: **beat** (first, inside the poller — the dead-man
is counting) → poll due games (pull path) → **drain bus readings** (the
observation stamp is taken from each message's `Fetched-At` BEFORE the
accept verdict — a duplicate IS the confirmation) → drain venue answers →
daily discovery if due → the **§3.1.4 sweep**. After the tick, `run()`
flushes the readings' batched acks.

The sweep is an **event** (`VALUATION_SWEEP`, N28): portfolio-wide, one
per 2.0 s fixed slot, minted by a producer because the engines read no
clock — replay consumes the emitted sweeps. A stall emits ONE sweep
carrying the missed count, never a backlog. The sweep carries the
`observations` map (game → last successful fetch) — feed health, journalled,
so replay reproduces the same suspensions.

Boot order (load-bearing): connect → beat → build → **replay the
journal** → reconcile → tick. Replay is synchronous inside the gateway's
30 s boot grace — which is why **§10.3 checkpoints are required before the
season** (every deploy is a restart; the journal grows all season).

Composition (`compose.py`): every construction decision in one file. Two
modes — `loopback` (real gateway + real NATS + real TEAM_BINDINGS,
synthetic T — proves plumbing, never prices) and `live` (**refuses to
start and names its gates**: S1/S7 entitlement · the go-live ingestion
switch · N19 file delivery).

## 10 · What is real, what is mocked, what is gated

| Real and proven | Mocked / interim | Gated / unbuilt |
|---|---|---|
| Event core, journal, replay equality on a real game | Off-field RAV/EAV (§3.6) — static inputs | Live mode (S1/S7 · go-live switch · N19) |
| Valuation with Edwin's on-field leg (his unit tests pass) | `p_tie = 0` (S6 interim) | §10.3 checkpoints (required pre-season) |
| Position/skew (Ch 4), quoting chain (Ch 5), market state (Ch 6) | Pre-kickoff tier 15 s (George's 10–30 range) | §5.5 public-book checks, §5.9 replenishment (E17) |
| Venue sync wire-proven vs the real gateway | E31 width values (mechanisms built, numbers Edwin's) | Ch 9 IPO · Ch 11 settlement · §10 recovery |
| The full bus path, drilled end to end 06-08 | | Opening position publisher (E27) · boot-reconcile healer |

## 11 · Where things live

| Piece | Code |
|---|---|
| Envelope · acceptor · journal · keys | `mm/events/` |
| SR adapters (file + wire, finals) | `mm/adapters/sportradar.py` |
| Edwin's file reader | `mm/adapters/reference_feed.py` |
| Gateway event adapter | `mm/adapters/gateway.py` |
| Valuation (RP, on-field, freshness) | `mm/valuation/` |
| Position (NP, PR, IA, RM) | `mm/position/` |
| Quoting (σ², width, ladder, sizes, publish) | `mm/quotes/` |
| Market state + kill switch | `mm/market_state/engine.py` |
| Venue record, reconciler, sync, transport | `mm/venue/` |
| Poller (pull path + heartbeat + tiers) | `mm/poller/worker.py`, `scheduler` in both repos |
| Bus consumer (durable, acks, poison) | `mm/poller/consumer.py` |
| Runtime (tick, sweep, boot) + composition | `mm/runtime/` |
| The 170 universe (ticker = security id) | `mm/universe.py` |
| The 170 sr-id → ticker bindings (verified) | `mm/bindings.py` |
| Every configurable number + status | `mm/config/dictionary.py` |
| Service-side publisher | `inplay-sportradar-service/src/app/workers/mm_publisher/` |

## 12 · Key numbers

Every number lives in [[market-maker/parameters]] with a status
(✅ confirmed · 🟡 proposed · 🔴 TBD) and in code only via
`mm/config/dictionary.py` (§1.6-5). The load-bearing set: $5.00/win ·
$2.50/tie ✅ · floats 900k/1M ✅ · S=$1.00, M=$0.25 ✅ (N20 caveat) ·
live bands 5/10/20 s ✅-values/🟡-basis (E38) · γ=0.02, k=1.2, h=20 s,
H=30 s, σ²∈[0.05,400] 🟡 (E31) · base 10,000 × 0.72^i, clamp
[1,000, 15,000] 🟡 · tick 1 s, sweep 2.0 s ✅ · tiers 2 s/15 s/30 min/
10 min (LIVE ✅ · PRE 🟡 · slow tiers George's) · dead-man 4 s (Hasan's
placeholder, N15).
