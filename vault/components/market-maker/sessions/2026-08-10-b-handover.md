---
description: "Comprehensive handover for the 10-08 session: crashes, the feed outage, the no-mock ruling, shorts, the taker's first live runs, and the gateway deploy."
---

# 2026-08-10b — HANDOVER: the full session, end to end

> **Type:** handover — the single entry point for the next session,
> human or AI. Read this, then the working guide's §1 order.
> **Narrative companion:**
> [[market-maker/sessions/2026-08-10-run-restart-crash-forensics]]
> (seven dated late-additions, the WHY of everything below).

## 0 · The session in two sentences

It started as "start a run with the maker and the poker so we can test
it" and became: two live crash investigations, a market-data outage, a
no-mock-data policy shipped to devices, the taker's account stood up
and seeded, T-S05 built and proven against the venue, SNT-1's first
live trading runs, and a coordinated gateway fix-and-deploy with Hasan.
**Every layer of the stack — venue, gateway, feed, app, maker, taker —
was broken somewhere this morning; every break is now diagnosed,
fixed, and verified except the two that belong to Rob.**

---

## 1 · The morning: runs, crashes, and the feed

1. **The run started; five of six books were dead.** The supervised5
   engine's record had diverged from the venue (constant
   `UNKNOWN ORDER` cancel-rejects — the phantom-order loop), so it
   reposted nothing. A clean restart on a fresh journal
   (`supervised6`/CFG-0005) fixed all six; the poker filled them
   evenly.
2. **Crash #1 (10:04:53Z).** Another session (Hasan's gateway work)
   swapped the gateway binary and restarted it mid-churn. The dropped
   FIX session orphaned a poker order (`SESSION_DOWN` local reject);
   the poker's cleanup cancel drew a local `UNKNOWN_ORDER`
   cancel-reject; the engine treats a cancel-reject for an untracked
   order as fatal → `UnknownVenueOrder` raise → dead → the dead-man
   swept the whole book. George's "the books look seriously wrong" was
   a swept market, honestly rendered.
3. **The feed break.** After that restart the MD side published
   fresh-timestamped but EMPTY books for ~2 hours while the venue's
   matching engine held full ladders (poker fills at correct ladder
   prices proved the ladders existed). The cure was a fresh
   subscription, which at the time meant another gateway restart.
4. **The ordered-restart rule** (now a recorded decision): bots down →
   engine down → gateway → engine → poker. Both failure modes of
   violating it happened live today.
5. The engine was restarted through supervised6→9 (CFG-0005→0008),
   each on a fresh journal per the redeploy rule.

## 2 · The app and the no-mock ruling

- George's JETS screenshot was the app's demo generator,
  pixel-for-pixel (even 10¢ rungs, sizes ≈ 800/(i+1) — `generateOrderBook`).
- **The ruling: "we never ever ever want to show mock data."**
  Implemented: every generated-ladder fallback deleted from
  `OrderBookCard.tsx` and the game page's inline book; both now render
  real venue depth via `useOrderBook` or an honest "No live order book
  available." Policy comments guard both former fallback sites and
  point at the trading service for empty-ladder diagnosis.
- Shipped: `inplay-app` `feat/home-rework` (`51af564`) and
  cherry-picked to **`prerelease` (`4da4e0d`), EAS OTA triggered** —
  on George's device channel.
- Two wrong diagnoses made and corrected en route (both recorded):
  (a) **the deployed trading service was AHEAD of its git repo** —
  book-channel tokens and quote-side clears were already live in
  `day-change-v1`; trading-service PR #2 was merged as pure repo
  catch-up, nothing deployed; (b) "the app can't subscribe" — killed
  by a synthetic Centrifugo client (minted HS256 tokens from the
  node's secret, connected, subscribed, received frames) that proved
  the entire path healthy. The empty frames were the GATEWAY's MD
  break (§1.3), not the app.
- Also fixed en route: the failed Vercel deployment George saw was the
  `feat/home-rework` preview, already failing before this session.

## 3 · Shorts

- **Edwin wants the taker to short** (via George). First filed as
  venue-gated; George corrected it and the code proved him right:
  **the platform already shorts live via FIX side 5** — the app maps
  it (`venueOrders.ts`), the gateway sends it (`SideSellShort=5`), the
  service charges full-notional collateral with a **1,000
  shares/security borrow reserve on QA** (T-M06; production 5M/5M).
  The 08-09 sell rule (`Pos − livS`, whole-order reject) governs
  side-2 sells only. The platform model: **flatten first, then
  short** — long and short are exclusive states.
- **George's mechanism ruling → T-O10: never straddle zero.** Longs
  cleared before any short, shorts cleared before any long, no single
  order crossing zero, side 5 never resting beside a long or a live
  side-2 sell.
- **The maker's own shorts → N34, position taken:** the MM CAN short
  as a last-resort backstop ("usually never gonna happen but we're
  probably gonna need it") — asks flip side 2 → side 5 exactly at
  flat; the inventory floor (E27 sizing) makes flat rare; the
  rationale is that a no-short MM that runs dry quotes one-sided.
  Edwin confirms in the E26 round.
- Gates: **E26** (Edwin's rules: when, how deep, how covered, the
  E33/T13 disclosure leg — a house bot short against retail longs) and
  **T16** (Rob: who backs the borrow, per-book size, which checks are
  venue-side — the taker bypasses the trading service, so only venue
  checks bind it; margin; IPLP entitlement).

## 4 · The taker: from "account exists" to trading live

1. **Identity completed:** venue account `4963224393` (from George) ·
   platform user id `385656921832584863` (Zitadel lookup,
   cross-validated: the same query returns the MM's known id for the
   +mm alias) · login `hasan.ahmed+MT@novosapien.ai`. Credential kept
   OFF-vault; Secret Manager at deploy time.
2. **Float made real:** 5,000 shares × five tickers seeded via the
   gateway's `35=UPT` position-transfer (one-way, NON-idempotent —
   sent exactly once each, all `UPTa`-accepted). Cost basis at mid:
   EAGL 389,025 · PATR 398,975 · GIAN 305,475 · COWB 380,900 ·
   STEE 331,725. JETS excluded (band-blocked, §6). This resolves
   E39's QA mechanism; Edwin still owes the production numbers and the
   tilt's cost-basis ruling.
3. **T-S05 built** (after the plain-terms explanation George asked
   for): `snt/reconcile.py` — venue position (`position.{userId}`,
   tag 9383) vs our tally; a mismatch surviving the 5 s grace fires
   the SAME journaled halt as the kill switch, both numbers printed,
   live orders swept; the venue figure is NEVER adopted (T15: 9383's
   liveness unconfirmed). Bot-wide halt — deliberately stricter than
   the per-book requirement. Float env-tunable (`SNT_FLOAT_SHARES`,
   `SNT_FLOAT_OVERRIDES=SYM:QTY,…`).
4. **Run 1 (25 seconds): T-S05's first act was a TRUE POSITIVE.** One
   trade (sell 12 EAGL @ 77.81, filled), then
   `RECONCILE HALT venue=4988 ours=5000`. Root cause: the gateway
   carries the ClOrdID only in the order SUBJECT
   (`order.{user}.{clOrdId}`) — the taker read the body, dropped every
   fill, and was flying blind. Fixed same hour
   (`with_subject_order_id`, the same fallback the MM adapter uses).
5. **Run 2 (15 minutes): 67 sends, 67 fills, 0 rejects, 0 reconcile
   alarms.** Both sides, five books, Edwin's size distribution (min 6,
   median 28, max 140), ~1 order/book/min in PRE_KICKOFF, nibbling
   the touch by design (90% at the touch, 10% sweep ≤3 ticks, size ≤
   half the touch).
6. **Wire facts now encoded in the code:**
   - The MM namespace REQUIRES the `MM` ClOrdID prefix
     (`MM_PREFIX_REQUIRED`) — the taker mints **`MMSN` + 14 hex**;
     the untested `SN` prefix would have had every order rejected.
   - The taker **never publishes MM heartbeats** — the dead-man latch
     is GLOBAL; a second beater would mask the engine's death.
   - `snt.control.{bot_id}` is **NOT granted** on NATS → the kill
     switch (T-R01) is dead in QA runs; process-kill is the interim
     stop. Grant owed by Hasan.
7. **Deploy shape used:** git bundle → VM (`~/kit/*.bundle`, the VM's
   origin is a bundle, no GitHub egress) → worktree `~/snt-checkout` →
   env `~/snt2.env` → journal `/var/lib/mm/snt2`. Next run needs only
   a fresh `SNT_CONFIG_VERSION`.

## 5 · The gateway: Hasan's handover, our fixes, the deploy

- **Hasan's handover** (filed in the narrative note) corrected the
  record: the JETS "stale 18.65 ask" was a **fossil quote** — the book
  is EMPTY; 18.65 is JETS's **last-trade price** (confirmed at deploy:
  the snapshot logs `bid=0 ask=0 last=18.65`). The probe-buy idea is
  dead — there is nothing to buy. The venue band anchoring on 18.65 is
  venue-side reference staleness → **Rob resets it**. His handover
  also: the VM is a **stateful MIG — never `instances stop` it**; MM
  governor now 1500/300; account `1797733477` maxOrdRate raised
  100 → 2500 (the MM ran 17× under its design peak all along — prime
  suspect for the replace-churn's rejects); the account is on the
  IPLM MPID; deploy procedure = cross-compile, scp, swap, restart.
- **Built on his permission (gateway PR #2, merged):**
  1. **Fossil-quote fix (his 4a, his spec):** empty-side snapshots now
     publish with `QuoteCleared` flags (a depth-1 35=W is the venue's
     whole statement — absence means EMPTY, unlike incrementals) and
     the Redis write HDELs cleared sides. Verified live at deploy: the
     JETS fossil purged on boot.
  2. **`POST /md/book-resubscribe`** — the heal for §1.3 without the
     restart that killed the engine: closes with the EXACT opening
     MDReqID (venue rule), reopens fresh; `{"symbol":"X"}` or `{}` for
     all. Exercised live on JETS: `MDB-IPTCJETS-94` → `-181`.
  3. **Gap-log rate limit** — first of a streak + every 100th (the
     flood was one WARN per message for hours; NOTE it logs from the
     OE adapter, not MD — two separate signals).
- **The d001dd5 saga:** Hasan's UNKNOWN-ORDER fix was deployed but
  unpushed (binary/repo divergence, again). We held our deploy,
  reimplemented it from his description as a fallback, then he pushed
  the real thing (`005fdd8` — same shape, plus a named constant and
  his own test) and our fallback was deleted.
- **DEPLOYED 22:32Z** from `main@005fdd8` (his fix + our three), both
  bots stopped first per the ordered rule. Both FIX sessions
  re-logged in ~1 s, 170 MD subs, verified live.
- **Engine hardening — MM PR #11** (`fix/cancel-reject-drain`): an
  untracked cancel-reject drains loudly (counted, both ids logged)
  instead of killing the process — the crash-#1 class is gone once
  merged and deployed. 611 tests + ruff + mypy-strict green. Named
  residual gap in the PR: a no-symbol local ORDER_REJECTED for a
  foreign order still raises.

## 6 · Current live state (session close)

| Thing | State |
|---|---|
| Gateway | UP, `main@005fdd8`-equivalent binary, both sessions on, binary=repo |
| MM engine | STOPPED. Next run: `supervised10` + **CFG-0009**, fresh journal |
| Taker | STOPPED (self-bounded runs only so far). Next: fresh `SNT_CONFIG_VERSION` |
| Books | EMPTY post-sweep (the honest truth, and the app now shows it honestly) |
| Taker account | long 5,000 × EAGL/PATR/GIAN/COWB/STEE (EAGL 4,988 after run 1's sell 12) |
| JETS | unquotable — venue band anchored on last-trade 18.65 (Rob) |
| App prerelease | no-mock order book OTA'd (`4da4e0d`) |
| Hasan's manual PATR orders | `TQB383165`/`TQA383165` rest on the MM account — cancel when done |

## 7 · Repos, branches, PRs

| Repo | State |
|---|---|
| `inplay-market-maker` | main `b42aa65` clean · **PR #11** (engine hardening) + **PR #12** (the whole taker: `7e2b54d` float/gate/hardening → `2de7775` T-S05 → `20f6a51` MMSN → `f9ae1f3` test → `0570bf5` subject-id + env float) — both await George |
| `inplay-fix-gateway-go` | main `005fdd8` — MERGED (our PR #2 + Hasan's fix) and **DEPLOYED** |
| `inplay-trading-service` | main — PR #2 merged (repo catch-up; deployed `day-change-v1` was already ahead) |
| `inplay-app` | `prerelease` `4da4e0d` (OTA'd) · `feat/home-rework` `51af564` |
| `inplay-vault` | `docs/t0-plain-english-guide`, uncommitted doc updates (this session's + the prior SNT session's), UNPUSHED — George's standing call |

## 8 · What the next session does

**Taker (unblocked, in order):**
1. **T-F07** — derive the activity state from a real game schedule.
   One design call first: the schedule source.
2. **Proper deployment** — install `deploy/snt-1.service`, env into
   Secret Manager, stop hand-running bounded sessions.
3. George reviews/merges PRs #11 + #12.

**Queued behind rulings:** the shorts build (T-O10 + side-5 — wiring
is small, risk rules are the substance) behind E26 + T16.

**MM (separate session, per George):** R-Q09 crossing guard (most
urgent live-money item) · R-Q08 ask gate + the N34 side-flip ·
replace-churn diagnosis — revisit AFTER Hasan's rate-limit raise,
which likely caused the churn's rejects all along.

## 9 · Owed to people (consolidated)

- **Hasan:** `snt.control.{bot_id}` NATS grant (+ ideally a dedicated
  taker NATS user) · IPLP-vs-retail classification of `4963224393` ·
  MT sub into `INPLAY_VENUE_PLACE_SUBS` if app-side trading on that
  login is wanted · cancel his manual PATR orders when done · his own
  backlog: MM egress namespacing, FIX wire log OFF, book depth cap 10,
  the SPOF.
- **Rob (tZERO):** reset the JETS band/reference (18.65 last-trade,
  empty book) · T15 (is 9383 live — bounds T-S05's trust) · T16
  (side-5 mechanics, both house accounts) · T14 (session roll) · the
  IPLP slot.
- **Edwin:** E39 (production float + tilt cost basis) · E32 (SNT
  rulings) · E26 + N34 confirm (shorts, both bots) · the standing
  E-round.
- **George:** PRs #11/#12 · push the vault + sportradar branches ·
  keep/drop MM `requirements.md`.

## 10 · Corrections recorded today (do not re-learn these wrong)

1. The JETS 18.65 was NEVER a resting order — last-trade fossil; the
   probe-buy idea is dead.
2. The deployed trading service was AHEAD of its repo — check
   deployment provenance (Cloud Build source archives) before
   diagnosing from git.
3. The 08-09 sell rule governs side-2 sells only — the platform
   shorts via side 5, live in the app today.
4. The gateway VM is a stateful MIG — `instances stop` gets it
   deleted and recreated by autohealing.
5. "Sequence gap detected" is an OE-adapter signal, not MD — the two
   morning floods were separate problems.
6. A fresh-timestamped feed frame can still be WRONG — judge the feed
   against the journal, not its clock.
