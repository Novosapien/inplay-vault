---
description: "The short-edit bug traced to venue reason-0 overloading, the app fix shipped OTA, and the gateway TTL binary deployed in the post-slate window — plus the reason-0 phantom-order finding at the gateway"
---

# 2026-08-15 — the gateway TTL deploy (and the reason-0 disease, both editions)

> **Who:** George + Claude (app session, crossed into trading ops)
> **Type:** bug forensics + build + deploy
> **Refs:** inplay-app `d0e3940` · inplay-fix-gateway-go PR #6 (`main@a41e540`) ·
> app spec: the 2026-08-15 short-edit bug report

## What we did

1. **Traced the short-edit bug end to end.** A user edited a resting
   IPTCBUCC short (the Bucs played the 14-08 slate); the app sometimes
   stuck on "Updating…", sometimes flashed a GREEN "order already
   filled" and dropped the row — which came back on every cold start.
   Gateway logs held the wire truth:
   `reason=0 responseTo=2 text="FAILSRISK[...]: SHORTLIST[IPLY] Out of stock: IPTCBUCC [1000 < 1000 + 1000]"`
   — tZERO re-runs the borrow check when a short is RESIZED, the
   IPTCBUCC borrow pool was fully used by the user's own short, and the
   venue wraps that refusal in CxlRejReason=0 ("Too Late"). The app's
   reducer treated reason 0 as proof of a fill and deleted a live order.
2. **Shipped the app fix** (inplay-app `d0e3940` → `prerelease` OTA):
   reason 0 never removes an order; the open list reconciles from the
   server; "filled" only ever comes from an actual EXECUTION; replace
   rejects branch on `cxlRejResponseTo` and say "couldn't update";
   borrow exhaustion gets named copy (`short_borrow`); replace_rejected
   + too_late_filled joined the red-tone toasts; the `stale_after_replace`
   re-key was implemented in the reducer. 69 reducer assertions green.
3. **Built + merged the gateway TTL** (gateway PR #6, merged
   `main@a41e540`): `RequestRegistry.ExpireStale` + a 5 s sweep; an
   in-flight 35=F/35=G the venue never answers now expires at 30 s with
   a local `REQUEST_TIMEOUT` reject instead of pinning the order
   REQUEST_IN_FLIGHT until a gateway restart.
4. **Deployed the gateway binary in the post-slate window**
   (02:47–02:51Z, ~4.5 min outage; all three 14-08 games final ~2.5 h
   earlier, next slate Sat afternoon — R11 honoured; George's explicit
   go in-session, superseding his 14-08 ~22:30Z freeze for the gateway).
   Ordered ceremony held: taker halted via NATS as the `admin` user
   (3 cancels swept) → `snt-1` stopped → engine SIGTERM clean stop at
   tick 19,607 → 4× `cancel_all` (~1,800 cancels) → binary swap
   (backup `gateway-go.bak-124991e-pre-ttl`, new sha `737a6888…`) →
   restart → engine up as **supervised30/CFG-0028** (same code
   `main@ed921ca`; relaunched with the captured live environ) → taker up
   as **SNT-CFG-0020 / journal snt17** (same code `step4b-wash@5b10d68`,
   env backup `env.bak-2026-08-15`), booted straight to AUTO.
5. **Verified end to end:** both FIX sessions logged on, 180 MD symbols
   resubscribed, MM re-quoting (1,816 open and climbing), heartbeats at
   ~220 ms silence, dead-man armed/unlatched, no new-binary errors. The
   new binary also carries gateway **#5** (`GET /orders/mm`) — deployed
   as a passenger.

## What we learned

- ⭐ **tZERO overloads CxlRejReason=0 as a catch-all for its whole risk
  stack.** One 6-hour window showed reason 0 wrapping "ORDER IS DEAD",
  "Illegal Replace Qty[DMA]", a DTBP breach, and the SHORTLIST borrow
  failure — the real cause lives ONLY in the Tag 58 free text. Any
  consumer that reads reason 0 as "the order filled" is wrong on this
  venue, full stop.
- ⭐ **The reason-0 disease has a GATEWAY edition.** During the
  pre-swap sweeps, ~702 tracked MM orders answered every cancel with
  `reason=0 "ORDER DEAD[DMA]"` — already dead at the venue (the 14-08
  22:13Z dead-man fire), but the gateway retires tracker rows only on
  reason=1 (UNKNOWN_ORDER), so the sweeps re-cancelled them forever.
  The restart flushed most via the Redis rehydrate; **~211 phantoms
  remain** and the boot-grace dead-man sweep re-hit them (203 cancels,
  all refused reason-0). Follow-up PR owed: retire on reason 0 + ORDER
  DEAD text, symmetric with the UNKNOWN_ORDER path.
- The taker boot rebase earned its keep on its second cutover: adopted
  venue truth on IPTCNTMG (+1,547) and IPTCNCWP (−521), journalled and
  loud.
- Shorts are the only side that re-runs the borrow check on
  cancel/replace — which is why only short edits surfaced the app bug.
- `cancel_all` sweeps are rate-governed and bounded by `mmSweepTimeout`
  (30 s): a 2,273-order book needs several passes; plan sweeps in
  rounds, verify by the gauge, not the send count.
- The `nats` CLI lives only on `inplay-nats`; `admin` may publish
  `snt.control.snt-1` (halt/resume), `market-maker` may publish
  `gateway.orders.mm.>` (cancel_all). The 14-08 "no credentialed
  publisher" ceremony deviation is closed by this route: fetch the
  Secret Manager password at use time, publish from the NATS box.

## What went wrong / got stuck

- Sweeps 3 and 4 moved nothing — the frozen 702 were the reason-0
  phantoms above, not live orders. Diagnosed from the journal before
  proceeding; the venue book itself was clean.
- The gateway's known unexpected-execType drop (registry-first
  resolution in `handleExecutionReport`) is still open — deliberately
  NOT bundled into #6 (an eager Clear would orphan a legitimate
  out-of-order ack; needs venue-spec work). The TTL backstops the wedge.

## Decisions made *(mirror into [[market-maker/decisions]])*

- George: merge gateway #6 and deploy the gateway binary tonight
  (explicit in-session go — supersedes the 14-08 ~22:30Z freeze for the
  GATEWAY only; engine/taker restarted on unchanged code as part of the
  ceremony; publisher pools and all undeployed MM PRs remain frozen).
- App-side (recorded here for the cross-repo trail): reason 0 is never
  proof of a fill; "filled" requires an EXECUTION.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- Opened: should the gateway retire tracker rows on
  `reason=0 + "ORDER DEAD"` text the way it does on reason=1? (Proposed
  yes — follow-up PR; ~211 phantoms inflate the MM open-order gauge and
  every sweep until then.)
- Opened: the ~12 non-MM rows rehydrated vs ~20 pre-restart — most
  likely venue-dead user phantoms not present in Redis; worth a
  trading-service-side reconcile check on the next quiet slot.

## Next

- The reason-0 retirement follow-up PR on the gateway (small, shaped
  like the UNKNOWN_ORDER retire path).
- Verify on a tester device that the short edit now shows the red
  borrow message with the order still visible (app OTA `d0e3940`).
- George's call on lifting or keeping the 14-08 freeze for the still
  undeployed rows (MM #36, publisher #38 → prod, fix-set stack).
