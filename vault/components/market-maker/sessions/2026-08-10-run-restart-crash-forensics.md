---
description: "Ops+forensics session: two engine crashes traced to a gateway restart, the MD empty-book break, the never-mock app ruling, and the fixes shipped."
---

# 2026-08-10 — the run, the crash, and the empty-book feed: a full-stack forensics day

> **Type:** live ops + forensics session. George + Claude.
> **Docs touched:** this note. Working docs NOT updated in this session —
> the vault branch carries another session's uncommitted work, so this
> note records everything and the mirroring into decisions/open-questions
> is owed.
> **Repo state at close:** engine `supervised8` / CFG-0007 + poker RUNNING
> on the MM VM · gateway restarted 11:56Z (see below) · app changes pushed
> to `inplay-app` `feat/home-rework` · trading-service PR #2 open.

---

## What we did

1. **Started the run** George asked for: engine was already up
   (supervised5, 3 days), poker restarted. Fills flowed on EAGL only.
2. **Diagnosed the five dead books:** the supervised5 engine's record had
   diverged from the venue (constant `UNKNOWN ORDER` cancel-rejects), so
   it reposted nothing. Clean restart on `supervised6`/CFG-0005 fixed all
   six books; poker filled all six evenly.
3. **Chased "the app shows one price / mock ladders"** end to end:
   NATS → bridge → Centrifugo all healthy. Two false leads (below), then
   the real answer arrived by crash.
4. **The engine CRASHED at 10:04:53Z.** Root cause chain, fully verified:
   - Another session (George's user, IAP SSH) swapped the gateway binary
     and ran `systemctl restart fix-gateway` at 10:04:48 — Hasan's
     gateway/isolation work.
   - The FIX session dropped; a poker order died unacked
     (`SESSION_DOWN` local reject); the poker's cleanup cancel drew a
     local `UNKNOWN_ORDER` cancel-reject.
   - The engine treats a cancel-reject for an untracked order as a fatal
     alarm → `UnknownVenueOrder` raise → dead. Dead-man swept the book.
   - George's "the books look seriously wrong" was the swept market,
     honestly rendered.
5. **Restarted after the crash** (`supervised7`/CFG-0006 + poker): five
   books came back. JETS did not — see the stale-ask blocker below.
6. **Found the feed publishing EMPTY books** while the venue book was
   full (poker filling at real prices; published PATR frame 0 bids × 1
   ask). The 10:04 gateway restart had left the MD session's book
   rebuild broken (sequence-gap floods, no clean snapshot).
7. **Fixed it with an ordered restart** (the safe sequence): stop poker →
   stop engine → restart gateway (11:56Z, MD resubscribed fresh) → engine
   on `supervised8`/CFG-0007 → poker. Verified live: PATR publishing
   6 bids × 5 asks; five books two-sided; poker filling all five.
8. **App work (George's ruling: "we never ever ever want to show mock
   data"):** removed every generated-ladder fallback from `inplay-app`
   (`OrderBookCard.tsx` + the game page's inline book — now wired to the
   real `useOrderBook`), honest "No live order book available" empty
   state, policy comments at both former fallback sites. Pushed to
   `feat/home-rework` (`51af564`), tsc clean. NOTE: George's device runs
   the prerelease OTA channel — these changes are not on it yet.

## What we learned

- **The deployed trading service was AHEAD of git main.** `day-change-v1`
  (built 08-07 from a local tree) already carried the book-token `kind`
  param AND the quote-side clears. Reading the repo said the opposite and
  produced a wrong diagnosis for an hour. PR #2
  (`feat/order-book-tokens` → main) is pure catch-up hygiene; no deploy.
- **A gateway restart is fatal to the engine while anything shares the MM
  user id.** Rejected poker orders are never admitted (only acks admit),
  so their cancel-rejects arrive untracked → deliberate-alarm raise. The
  hardening (drain-and-count unknown cancel-rejects instead of dying) is
  designed but NOT built.
- **A gateway restart can also silently break the MD book rebuild** — the
  feed published near-empty frames for ~2 h while OE worked perfectly.
  Judge the feed against the journal, not just freshness: a fresh frame
  can still be wrong.
- **The sell-band cuts both ways:** with the MM book swept, a stale
  third-party ask at 18.65 became JETS's best ask, and the venue's 10%
  band now rejects every MM bid (~45.29) as "aggressive BUY above the
  ASK". The band that protects against crossing also blocks re-entry
  after a sweep. Neither the MM nor the poker can clear it (both would
  violate the same band).
- **Centrifugo's `market` namespace logs nothing for healthy activity**
  and retains frames for only 60 s — an idle-but-working path is
  indistinguishable from a dead one in the logs. The synthetic-client
  probe (mint HS256 tokens from the node's secret, connect, subscribe)
  is the reliable check; it proved the whole app path good in minutes.
- **The app's demo-book generator produced pixel-convincing fakes**
  (even 5/10¢ rungs, sizes ≈ 800/(i+1)) — George could not tell it from
  venue data. That is what "honest fake" looks like at its worst; hence
  the never-mock ruling.

## What went wrong / got stuck

- **Two wrong diagnoses shipped to George before the right one:** (1)
  "the deployed service ignores kind=book" — falsified by pulling the
  Cloud Build source archives; (2) "the app can't subscribe" — falsified
  by the synthetic client. Both came from trusting a stale local repo /
  absence-of-logs. The build-source archive and the synthetic client were
  the decisive instruments.
- **Cross-session collision:** the gateway redeploy at 10:04 happened
  under the same user while this session's engine+poker were live, with
  no coordination. It cost the crash, the sweep, ~2 h of broken MD, and
  the whole forensics chase.
- The vault + Vercel previews on `feat/home-rework` were already failing
  before this session's pushes (pre-existing, Aug 07).

## Decisions made (owed to decisions.md)

- **"We never ever ever want to show mock data"** (George) — the app must
  render venue data or an honest empty state. Implemented for the order
  book; the wider demo-price surfaces remain (product decision open).
- Gateway restarts require the ordered sequence: poker down → engine
  down → gateway → engine → poker (this session proved both failure
  modes of violating it).

## Late addition (same session) — Edwin wants the taker to SHORT

George, relaying Edwin: SNT-1 must be able to go short. First filed as
"venue-gated — no path"; **George corrected it and the code proved him
right: the platform already shorts live via FIX side 5** (app maps it,
gateway sends it, service layer charges full-notional collateral with a
1,000/security QA borrow reserve; flatten-first model — long and short
are exclusive). The 08-09 sell rule turns out to govern side-2 sells
only. Recorded in [[market-maker/decisions]] `2026-08-10` (with the
correction), the taker requirements addendum (T-O06/T-O08 flagged ✎⛔),
E26 extended, and **T16 opened** — narrowed to the house-account
side-5 specifics: borrow backing and size, whether short-while-long is
a venue or service check (SNT-1 bypasses the service), margin, IPLP
entitlement. Builds after E26 + T16 answer.

**George's mechanism ruling (same conversation): never straddle zero** —
clear longs before shorting, clear shorts before going long, no order
crossing zero. Filed as **T-O10** for the taker. "Probably the maker as
well" → **N34**: for a two-sided quoter flatten-first is non-trivial (a
flat MM's asks would be side-5 resting beside side-1 bids), three design
options recorded, goes to the Edwin round with E26.

## Late addition 2 — the taker's account exists

George supplied it end-of-session: **AccID `4963224393`**, login
`hasan.ahmed+MT@novosapien.ai` (Hasan-created; credential off-vault).
T-I01 ⛔ → 🟡; the shared-account hole closes on deploy. Owed: the
numeric platform user id, and IPLP-vs-retail classification (T-I02,
E33/T13). Recorded in decisions `2026-08-10b`.

## Late addition 3 — T-S05 BUILT (George approved after the explanation)

The plain-terms explanation landed ("we can consume this from the
venue, which is tZERO") and T-S05 was built the same hour:
`snt/reconcile.py` — venue position (`position.{userId}`, tag 9383) vs
our tally; a mismatch surviving the 5 s grace fires the journaled halt
with both numbers printed; the venue figure is never adopted (T15).
Halt is bot-wide (deliberate deviation, stricter). 10 tests, 638 green,
ruff + mypy-strict clean. The 09-08 base was also committed and the
branch pushed (`7e2b54d`, `2de7775`). ⚠ First run on the new account
will correctly halt against the assumed float — set `float_shares` to
the account's real holding first (recorded in the requirements
addendum `2026-08-10b`).

## Late addition 4 — the float SEEDED, PR #12 open

George: allocate the float. Done via the gateway's `35=UPT`
position-transfer endpoint (one-way, non-idempotent — sent once per
ticker, all `UPTa`-accepted): 5,000 shares × five tickers on account
`4963224393`, cost at mid. JETS excluded (band-blocked). MM PR #12
opened carrying the whole taker branch. The taker is now deployable:
account + user id + real float + reconciliation all in place.

## Late addition 5 — SNT-1's FIRST LIVE RUNS, and T-S05's first catch

Two QA runs on the taker's own account, both this session:

**Run 1 (25 seconds, a triumph disguised as a failure):** the bot sent
ONE order — sell 12 EAGL @ 77.81, filled — and **T-S05 halted it**
(`venue=4988 ours=5000`). The halt was a TRUE POSITIVE: the gateway
carries the ClOrdID only in the order SUBJECT, the taker read the body,
so every fill was dropped and the tally was blind. The reconciler
caught a genuinely blind bot on its first trade. Two more findings:
the gateway REQUIRES the MM ClOrdID prefix on its namespace (SNT's
untested `SN` prefix would have rejected everything — now `MMSN`), and
`snt.control.{bot_id}` is NOT granted to the NATS user (kill switch
dead in QA — **grant needed from Hasan**; the taker must NEVER publish
MM heartbeats — the dead-man latch is global).

**Run 2 (15 min, the fixes in):** subject-id fallback + env-tunable
float (`SNT_FLOAT_OVERRIDES=IPTCEAGL:4988` — pinned to the venue's
truth). Boot clean, fills folding both ways across the books at the
MM's touch, **T-S05 silent = verifying every fill against the venue**.

Deploy shape used: git bundle → VM worktree `~/snt-checkout`, env in
`~/snt2.env`, journal `/var/lib/mm/snt2`. Commits `20f6a51`, `f9ae1f3`,
`0570bf5` on the branch; PR #12 carries it all.

## Late addition 6 — Hasan's handover, and the JETS correction

Hasan's gateway handover (2026-08-10) landed end of session. What it
corrects and adds:

- ✂ **The JETS "stale 18.65 ask" was a FOSSIL QUOTE, not a real
  order** — his probe showed the book EMPTY; the 18.65 lived in
  `market:quote:*` because an empty-side snapshot never publishes.
  The probe-buy option is DEAD (nothing to buy); the venue's band
  anchoring on 18.65 is venue-side reference staleness → **Rob**.
- His unpushed-but-DEPLOYED commit `d001dd5` makes UNKNOWN ORDER
  terminal (kills the phantom re-cancel loop). ⚠ NOT in the repo —
  any gateway build until he pushes it is a rollback.
- MM governor now 1500/300; account 1797733477 maxOrdRate 2500 (was
  100 — the MM ran 17x under its design peak all along); the account
  is on the IPLM MPID. The VM is a STATEFUL MIG — never `instances
  stop` it (autohealing recreates; happened twice today).
- Manual PATR orders `TQB383165`/`TQA383165` (79.50x25 / 80.10x25)
  rest on the MM account — cancel when no longer needed.
- His ranked backlog: 4a fossil quotes → MM egress not namespaced →
  FIX wire log OFF → book depth capped at 10 → the SPOF.

**Built on his permission (gateway PR #2, code-only, DO-NOT-DEPLOY
until d001dd5 lands):** the 4a fossil-quote fix (cleared flags on the
snapshot path + Redis HDEL) · `POST /md/book-resubscribe` (the
empty-book heal without the restart that killed the engine) · the
gap-log rate limit.

**The taker's full run completed: 67 sends, 67 fills, 0 rejects, 0
reconcile alarms** over 15 minutes across the five books.

## Late addition 7 — the gateway DEPLOYED (session close)

Hasan pushed his UNKNOWN-ORDER fix as `005fdd8` (his own
reimplementation matched ours line-for-shape; our hold branch deleted).
Combined main (his fix + PR #2's three) built, 11 packages green,
deployed 22:32Z per his documented procedure with both bots STOPPED
first. Verified live: both FIX sessions re-logged in ~1 s;
`POST /md/book-resubscribe` exercised on JETS (old id closed, fresh
subscription accepted); the fossil fix proved itself on boot — the
JETS empty snapshot (`bid=0 ask=0 last=18.65`) now publishes cleared
and the Redis fossil is purged. ⭐ **18.65 is JETS's LAST-TRADE price**
— the venue band anchors on it; resetting that reference is Rob's.

**State at close:** engine + taker STOPPED (next: `supervised10`/
CFG-0009; taker needs only a fresh `SNT_CONFIG_VERSION`). Gateway
running `main@005fdd8`-equivalent. Books empty post-sweep.

## Questions opened (owed to open-questions.md)

- **JETS stale ask 18.65** — who clears it: probe buy from a non-MM
  identity, or Rob busts it venue-side? Until then JETS cannot quote
  bids.
- Dead-man sweep at 11:55 reported `sent=101 stillResting=80` — did the
  supervised8 boot reconcile actually clean the leftovers? Verify before
  trusting the book.
- Does Hasan's isolation work change the MM's transport contract
  (`gateway.orders.mm.*`, rate limits, dead-man)? Coordinate before the
  next engine deploy.

## Next

1. ~~Engine hardening~~ **BUILT** — MM PR #11 (`fix/cancel-reject-drain`):
   an untracked cancel-reject drains loudly instead of killing the
   process; 611 tests + ruff + mypy-strict green. Awaiting review/merge;
   deploy coordinated with Hasan's gateway work. Residual gap named in
   the PR: a no-symbol local ORDER_REJECTED for a foreign order still
   raises.
2. ~~Trading-service PR #2~~ **MERGED** (hygiene; no deploy — the code
   was already live as `day-change-v1`).
3. **The no-mock order book SHIPPED to prerelease** (`inplay-app`
   `4da4e0d` on `prerelease`, EAS OTA triggered). Verify on George's
   device after the OTA lands.
4. **The gateway MD-rebuild fix is HASAN'S** (George, session close):
   Hasan will send a note on what he is doing. Hand him this note's
   findings — the MD rebuild fails under churn, and the OE-side
   "sequence gap detected" flood is a separate signal.
5. Clear the JETS 18.65 blocker (George/Rob call).
6. Mirror this note's decisions/questions into the working docs.
7. **STANDING RULE from George: hands off the LIVE gateway, Centrifugo,
   and cloud architecture — Hasan is mid-isolation-work.** Engine and
   poker are STOPPED; next run needs `supervised9` + CFG-0008.
