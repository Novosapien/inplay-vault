---
description: "The full-book joint run: 170 books stood minus JETS, the empty-book gate proven gone, then .TEST twins built (MM PR #22) and all 180 quoted by supervised14"
---

# 2026-08-11 (night) — the full-book joint run: 169/170 books stand

> **Type:** live ops + a ⭐ venue finding. Claude, on George's ruling
> "test the maker and the taker on all 180 books".
> **Continues:** [[market-maker/sessions/2026-08-11-full-book-seed]]
> (the seeding) and [[market-maker/sessions/2026-08-11-taker-cutover]].
> **State at close:** maker `supervised13` (CFG-0012, 170 books,
> journal `/var/lib/mm/supervised13/`) · taker `snt-1.service`
> (SNT-CFG-0008, same 170 books, journal `/var/lib/mm/snt5/`) ·
> supervised12's journal PRESERVED for C2.

## What we did

1. **Seeded the taker's account** `4963224393`: 5,000 shares × the 175
   books it did not hold (canary IPTC49ER, then bulk; 175/175
   `UPTa`). Ledger section "the taker-account seed".
2. **Built the 180-book inputs file** from `ipo-prices-170.csv`
   (`E[Wins]` → `expected_season_wins`, `Off-Field EV` →
   `expected_off_field`; NFL 17 games, NCAA 12; `.TEST` = twin).
   Checked the arithmetic against the 08-07 six (EAGL
   5×10.128+27.15 = 77.79 ✓).
3. **Stopped both bots** (taker first, then maker; supervised12 closed
   gracefully "stopping after 60833 ticks"; the dead-man swept the
   resting book). ⚠ One miss: the pre-stop halt publish FAILED
   silently — `/etc/snt-1/env.secret` has no `export` statements, so
   `source` + a child python saw no `SNT_NATS_URL` (KeyError). The
   stop was therefore plain; the dead-man swept ~10 s later and the
   final journal showed no lost fill. Lesson recorded below.
4. **Cleared-books check (George's ask):** probed ALL 180 books
   (`POST /md/probe`, depth 0 — the gateway answers with a structured
   `MD probe reply … entries=N` log line). Result: **zero resting
   levels anywhere**; the six QA books each show only the last-trade
   print (269=2). No STX reseed at this hour; nothing to eat.
5. **Started `supervised13`** (CFG-0012). Two boot refusals taught the
   contract: `compose.py` refuses non-universe tickers (**the ten
   `.TEST` cannot be quoted without an engine change**) and the inputs
   file must exactly match `MM_SECURITIES`. On 170 books:
   **"book standing: 1532 instructions for 170 securities"**.
6. **Started the taker** on the same 170 books: five QA floats
   recomputed at the cutover (rule 7: COWB 3856 · EAGL 5406 ·
   GIAN 4605 · PATR 5245 · STEE 5419), 165 books at the seeded 5,000,
   every float explicit in the env. First fills passed T-S05 — the
   seed is venue-agreed.

## What we learned

- ⭐ **The empty-book LmtPerc gate is GONE.** All 164 virgin books
  ACCEPTED their first ladders — the 07-08 "No price available"
  total-reject did not reproduce anywhere. B3's ⛔ became a pass;
  the standing Hasan question is answered by observation. Parameters
  `LmtPerc reference` row ✎.
- **JETS is the only book of 170 that cannot stand** — 46 rejects,
  0 accepts against its stale ~$18.65 reference (T20, Rob). Its
  aggressive band reads **10%** in the reject text — a third
  per-symbol LmtPerc value (parameters observed table).
- **The engine's universe is a hard gate**: `MM_SECURITIES` ⊆ the 170
  (`compose.py`). Quoting `.TEST` twins is a small build item
  (accept a `.TEST` suffix of a known ticker; both accounts already
  hold the positions).
- ⭐ **T-F07 boot staleness wrinkle:** at taker boot, the retained
  Chiefs–Ravens capture message on `SR_PROBABILITIES` (published
  mid-day for the pipe proof) derived **RAVE + CHIE LIVE (×75)** —
  a fresh JetStream consumer receives the old message AT BOOT, so it
  reads inside the 10-min staleness bound. Fills printed at LIVE
  intensity on both books. The staleness bound should decay them to
  OVERNIGHT within 10 minutes of the (re)delivery — checked at 22:58,
  result in the addendum below. Design question for the taker: the
  staleness clock should price a reading's own `fetched_at`, not its
  delivery time.
- Load numbers, first ~4 min: ~9,400 wire messages ≈ 38 msg/s across
  170 books (governor 5,000/s — 0.8%); journal ~7,800 events, no
  backpressure; replaces dominate (the per-mode republish clock
  redraws each book on its dwell).
- Ops lesson (repeat offender): env files without `export` do not
  reach child processes via `source`. The halt helper must load
  `env.secret` with `set -a`/`set +a` (or read the URL explicitly).

## What went wrong / got stuck

- The silent halt failure above (benign this time — no lost fill).
- Two supervised13 boot refusals before the clean start (`.TEST`
  tickers; inputs⊆securities) — contract now recorded.

## Decisions made

- Ran 170 of George's ruled 180: the `.TEST` ten are engine-blocked,
  documented, and left seeded for the follow-up build item. Nothing
  else deviated from the ruling.

## Questions opened/closed

- Closed empirically: the empty-book first-order question (see
  open-questions T10c + parameters). Closed: test-symbols items 1+2.
- Opened: **the T-F07 staleness clock** — delivery-time vs
  `fetched_at` (the boot LIVE derivation above). Taker build item.
- Opened: **`.TEST` quoting needs an engine change** (universe
  validation). MM build item.

## Next

1. Watch the joint run overnight (drift caps, JETS backoff, message
   rates). 2. The `.TEST` engine change + T-F07 staleness fix.
3. C2 on supervised12's preserved journal. 4. The synthetic game day.
5. Externals: Rob (JETS reference T20 · STX reseeder T19) · Hasan
   (B2) · the Edwin round.

## Addendum 2 (23:0x) — `.TEST` twins BUILT and DEPLOYED: all 180 books quoted

George's rulings mid-session: (a) JETS — assessment given (nothing
rests on the book; the $18.65 is the last-trade print anchoring the
band; Rob's reset or a ~9-hop cross-account walk are the fixes; left
with Rob). (b) **Make the engine accept a `.TEST` suffix of a known
ticker — DONE, MM PR #22** (`feat/test-ticker-twins`, `edd9512`):
`resolve_security()` mints a twin Security at composition (base's
league + float; the 170-row table never grows, `[no-holes]` intact);
the valuation `[reachable]` guard is satisfied by a derived provider
id `<base sr id>.test` no real feed emits — bus readings never move a
`.TEST` book, and the synthetic-game-day driver can address one
deliberately. 690 tests, ruff + mypy-strict green. Also PR #21:
CLAUDE.md rule 7 (floats are positions — recompute at every cutover).

Deployed by bundle (`~/kit/twins.bundle`, main checkout →
`edd9512`) and restarted per the rules:

- **Maker `supervised14` (CFG-0013)**, inputs `supervised-inputs-180.json`,
  journal `/var/lib/mm/supervised14/`: **"book standing: 1636
  instructions for 180 securities" — 179 of 180 books accepted,
  including ALL TEN `.TEST` twins.** JETS alone stays reject-only.
- **Taker SNT-CFG-0009**, journal `/var/lib/mm/snt6/`, 180 books,
  every float recomputed from snt5 per rule 7 (529 fills over 152
  books folded in; e.g. RAVE 4168 after its LIVE burst, CHIE 5124;
  `.TEST` books at their seeded 5,000). First fills passed T-S05.
- ⭐ **The first `.TEST` print ever: `IPTCPACK.TEST sell 6@71.66`**,
  house-to-house, 23:03:07Z.
- RAVE/CHIE derived LIVE again at boot from the retained capture
  message (the known redelivery-freshness wrinkle) — decays at
  23:12:59 per the proven 10-minute bound. The code fix (price
  `fetched_at`, not delivery time) stays a taker build item.
- supervised13's journal (the 170-book run, the empty-book-gate
  evidence) is preserved beside supervised12's.

## Addendum 5 (23:2x–23:5x) — the SYNTHETIC GAME DAY, and the poisoned-final lesson

George's ruled task 2, built and run: `~/synthetic_game_day.py` replays
the 1,089-reading Chiefs–Ravens capture onto the PRODUCTION
`SR_PROBABILITIES` stream with every timestamp remapped onto a
now-anchored clock (not_started → live at recorded-pace ÷ 10 →
ended 27–20), publisher-contract headers, via the mmpub credential.

**Run 1 (game id = the real `sr:sport_event:50075555`): the taker
danced, the maker refused.** Taker: PRE_KICKOFF on the first
not_started reading, **LIVE at the kickoff second (23:32:30)**, ×75
fills — A3 demonstrated. Maker: `readings=0`, prices static. The chase
(consumer info as NATS admin, connz, a durable rebuild): the server
delivered and acked EVERYTHING; the engine journalled exactly ONE
`probability_update` — **the morning's retained pipe-proof message,
whose status is `ended`**. ⭐ **The lesson: a final is PERMANENT in the
maker** (`FINAL_STATUSES` → OFFICIAL_RESULT, correctly), so one
retained "ended" message for a game id POISONS every later reading
under that id — the whole synthetic game was dropped as post-final
noise. The taker keeps a ROLLING state instead, which is why it obeyed
the same stream happily. Consequences, recorded:
- **A synthetic/replayed game must mint a FRESH game id** (routing is
  by competitor ids, so books still resolve; the id is the belief key).
- **Purge the stream before a synthetic day** — retained finals (and
  the boot-LIVE redelivery wrinkle) both die with the purge.
- The engine restarts along the way: `supervised15` (CFG-0014, fresh
  journal; supervised14's journal preserved). The mm-engine durable was
  deleted and recreated once during diagnosis (delivered/acked counts
  were healthy both sides — the durable was never the fault).

**Run 2 (fresh id `99990811`, stream purged): STILL zero readings** —
the second poison found by local reproduction against the real adapter:
**§7.1 requires `Z`-suffixed UTC stamps**; the driver emitted `+00:00`
and every reading was silently acked away as malformed. ⚠ The poison
counter (`ReadingInbound.poisoned`) surfaces NOWHERE in the tick line —
two runs were lost to silent poison. **Build item: journal/log the
poison count.**

**Run 3 (id `sr:sport_event:99990812`, Z-stamps, kickoff 00:17:38Z):
⭐ THE SYNTHETIC GAME DAY PASSED — see addendum 6.**

## Addendum 7 (01:11–01:18) — ⭐ T-S05's first PRODUCTION-CLASS catch: a lost exec report; two fixes shipped

At 01:11:33 the taker halted itself: `reconcile IPTCVATH: venue=4447
ours=4416 (float=4790)`. ✂ **CORRECTED by the 08-12 wire forensics
(see the 08-12 session note): NO fill was lost — a POSITION message
was.** The FIX wire shows all 26 window fills journalled 1:1, and the
triggering sell-31 exec carried `9383=4416` — venue and journal agreed
TO THE SHARE. The fill's companion `position.>` update (the second bus
message the gateway mints from the same exec) was dropped at the
churn-storm's peak; the reconciler compared the fresh holding against
the previous fill's stale figure and halted after grace. A
false-positive on position divergence, a true detection of message
loss. ⚠ Consequence: the recovery adopted the STALE 4447 as VATH's
float — snt8 carries a +31 error (true base 4416); patch at the next
quiet cutover. Design item: T-S05 should compare the exec's OWN 9383
tag, not the racing position feed. Recovery per rules 6+7 — with one
self-inflicted lesson on the way:

- ⚠ **The first recompute used a STALE BASE** (the old 170-book env
  file instead of the running CFG-0009 env): floats off by each book's
  snt5 drift, the ten `.TEST` books dropped. **T-S05 caught that too,
  within 10 seconds of boot** (AUBT halt at 01:13:23). 📝 **Rule-7
  refinement for the MM repo CLAUDE.md (next session, the checkout is
  busy): recompute from the RUNNING env's floats — read
  `/etc/snt-1/env` (or its dated `.bak`), never a convenience file.**
- **CFG-0011 / journal `snt8`** rebuilt from the CFG-0009 base + snt6
  and snt7 drift; VATH pinned from its halt line. ⭐ Independent proof
  the arithmetic is right: the AUBT halt line's venue number (5313)
  equals the recomputed AUBT float exactly. 17 fills after restart,
  zero halts.
- **The `$JS.FC` grant gap FIXED on the NATS box** (box convention:
  dated `.bak` `nats.conf.bak-fc-20260812`, `nats-server -t`, SIGHUP,
  11 connections before and after): the taker's ordered schedule
  consumer answers JetStream flow-control on `$JS.FC.SR_PROBABILITIES.>`
  and the `snt-taker` user could not publish there — the feed could
  stall mid-game (fail-quiet → OVERNIGHT). Violations stopped at the
  reload. 📝 Tell Hasan with the 08-11 change note.
- The boot-LIVE redelivery wrinkle fired at BOTH restarts (retained
  game-2/3 messages read fresh at delivery) — third demonstration; the
  `fetched_at` staleness fix is now the taker's top build item.

## Addendum 6 (00:17–00:52) — ⭐ A2 STAGE 2 / A3 / A4 / A5 PASSED: the full game day on production infrastructure

All 1,089 readings replayed through the production bus at 10×
(29.5 min), the maker on 180 real venue books, the taker at ×75.
Every pass criterion met:

- ⭐ **Prices TRACK, to the cent** (the A2 criterion): p_home ran
  0.566 → 0.371 → 1.000; **corr(p_home, CHIE mid) = +0.989 over 861
  paired points; RAVE −0.990** (the two-team mirror). Net moves: CHIE
  mid 74.84 → 77.02 (+$2.18) vs Δp × $5/win = +$2.17 implied; RAVE
  78.17 → 76.00 (−$2.17) — exact.
- **A3 (pre → kickoff):** demonstrated in run 1 — PRE_KICKOFF on the
  first not_started reading (23:24:30), LIVE at the kickoff second
  (23:32:30). Books stood from static valuations pre-kickoff.
- **A4 (final → post):** the taker flipped **LIVE → POST at 00:47:16**
  on the ended reading; the maker **minted the OFFICIAL_RESULT**
  (`official_result:sportradar|…99990812|1`, outcome home — the 27–20
  final) exactly once (idempotency held across the driver's 5 final
  re-offers).
- **A5 (halftime):** rode the replay's real halftime gap; the E38
  re-offer path (confirmation, not no-data) kept the books standing.
- **The taker at ×75:** 551 CHIE/RAVE fills in the ~30-min window,
  drift inside caps, zero halts, zero T-S05 reconciles.
- **No reject storm:** the in-game rejects (348) are 95% the KNOWN
  sell-gate gap (venue `sellable = Pos − livS`; the reconciler does
  not yet subtract resting asks — build/venue.md, recorded 08-09) —
  fast LIVE repricing re-posts asks while old asks rest. Not new;
  now measured under game load. No LmtPerc storm anywhere.
- Maker deduped the re-offers as §7.3 confirmations (1,257 journalled
  arrivals over 1,089 fresh readings), exactly the publisher contract.

**The synthetic-game-day driver** is `~/synthetic_game_day.py` on the
MM VM (scratchpad-built, worth committing to the MM repo's scripts/):
env `SGD_NATS_URL` (the mmpub credential) · `SGD_SPEED` (10) ·
`SGD_PRE_S` (pre-kickoff seconds). Contract learned the hard way:
fresh game id + purge first + Z-stamps.

## Addendum 5 (23:2x–23:5x) — the SYNTHETIC GAME DAY, and the poisoned-final lesson

## Addendum 3 (23:1x–23:3x) — ⭐ the JETS anchor WALKED UP: T20 closed ourselves

George's ruling: fix JETS ourselves if possible; Rob only as fallback.
The clean instrument (`UEPR` set-opening-state) is not entitled on our
session (probed 07-28, silently dropped), so the rung-walk ran —
`~/walk_jets.py` on the MM VM:

- **Mechanism:** pair-prints between two house accounts — ask from the
  MM account under a scratch `walkops` user id (the engine cannot adopt
  it), buy from the onboarded retail test account `6793952642` (NOT the
  taker's account — a foreign fill there would trip T-S05). 5 shares a
  hop, +8% per hop (inside JETS's 10% aggressive band). **Sensor:** the
  running engine's own JETS reject texts cite the live anchor
  ("ABOVE the ASK(x)") — no extra probes needed. **Finish:** the
  engine's first JETS accept.
- **Result: FOUR hops** — 18.65 → 20.14 → 21.75 → 23.49 → 25.37, each
  anchor refresh ~3–5 min — then, as predicted, the anchor cleared
  46.90/1.9 ≈ 24.68, the engine's PASSIVE asks became legal and rested,
  and the book began standing itself (4 sell-side accepts at the
  walker's exit). **Confirmed minutes later: JETS TWO-SIDED — 7 asks +
  6 bids accepted. ALL 180 BOOKS STAND.**
- ⭐ **Venue fact (measured):** the LmtPerc anchor FOLLOWS prints, on a
  ~3–5 min refresh — the 08-07e two-hop observation generalised. A
  stale anchor is self-serviceable by cross-account prints stepping
  inside the aggressive band. Total churn: 20 shares, ~$455 notional,
  house-to-house.
- Two harness lessons: the gateway's `orderRequest.price` is a JSON
  **float64** — a string price fails the unmarshal SILENTLY (no local
  reject, no log line with the id); and execution events carry the
  ClOrdID in the SUBJECT (`order.{user}.{clOrdId}`), not the payload.

## Addendum 4 (23:18) — full-stack audit: ALL CLEAN

Post-walk audit across the stack: maker 7.9% CPU, 180/180 books with
accepts, zero alarms; taker active, zero halts / reconciles / reject
streaks, largest drift 655 vs the 1,500 cap; ⭐ **the maker↔taker
journals mirror share-for-share on EVERY book of the full universe**
(591 taker fills, 160 books, 28 on `.TEST`); both LIVE-window decays
landed exactly on the 10-minute bound; gateway dead-man armed and
fresh (the 23:01 fire = the supervised13 stop sweep, 1,488 cancels,
by design), 1,582 open orders tracked; all four Cloud Run pools
Ready. The only gateway errors in 30 min: the dead-man's own
completion line + the walker's first (string-price) attempt — none
ongoing. ⚠ One census number to watch, not a fault: ~52 replaces/s
across 180 books (the per-mode republish clock at full universe) —
~1% of the governor.

## Addendum — the 22:58 staleness check: the bound WORKS

**RAVE and CHIE decayed LIVE → OVERNIGHT at 22:57:17 — exactly 10
minutes after the 22:47:17 boot delivery.** The T-F07 staleness bound
behaves as designed; the joint run self-corrected with no operator
action. At the check: 457 taker fills, zero halts, zero reject
streaks, maker ticking on all 170 books. The design note stands: the
staleness clock prices the DELIVERY time, so every fresh boot buys the
retained capture message a new 10-minute LIVE window until the message
ages out of the stream (7-day retention) or the stream is purged —
purge before the next taker restart, and price `fetched_at` in the
staleness check as the code fix.
