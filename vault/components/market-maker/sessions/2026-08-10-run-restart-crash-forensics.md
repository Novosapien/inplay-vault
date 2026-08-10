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

1. **Build the engine hardening** — unknown-order cancel-reject must
   drain loudly, not kill the process (`src/mm/venue/engine.py`). Code
   only; deploy coordinated with Hasan's work.
2. Clear the JETS 18.65 blocker (George/Rob call).
3. Merge trading-service PR #2 (hygiene). Mirror this note's decisions/
   questions into the working docs.
4. **STANDING RULE from George at session close: hands off the gateway,
   Centrifugo, and cloud architecture — Hasan is mid-isolation-work.**
