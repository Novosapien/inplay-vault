---
description: "The 17-08 gateway restart lost fills on five live orders — the replace ack arrived after the restart and was discarded, and tZERO's logon enumeration was binned with it"
---

# 2026-08-17d — the gateway restart, and the enumeration we throw away

> **Component:** [[market-maker/market-maker]] · **Type:** live incident
> **Status at writing:** ONGOING — `lost_fills` 5 → 8 → 16 → 20 → 42.
> Fix is `inplay-fix-gateway-go` PR #13 (Hasan) plus the adoption change
> described in §4.

---

## 1 · What happened

Hasan deployed five gateway PRs at 16:02Z and restarted the gateway. The
maker was live and mid-quote-churn: the wire carried **76 `35=G`
cancel/replace requests in the 5 seconds before the restart**.

From 16:02:56 onward the gateway began discarding execution reports that
carried shares. By 16:40 it had lost **42 fills across 5 orders on 4
tickers**, with ~33,300 shares still resting on those orders.

Sampled one order: **7 share-carrying reports on the wire, 7 discarded.**
Once an order is untracked the loss is total, not partial.

## 2 · Root cause — corrected twice, so read this version

The first reading was "the boot prune deleted live orders". That is
close but wrong in an important way. The evidence:

```
16:02:35.902 WARN  pruned stale members from open-order index count=1982
16:02:35.903 INFO  rehydrated resting orders from index      count=3184
16:02:36.026 WARN  unknown order or invalid transition  clOrdId=MM3b751dd2cc35c9ba
```

and the wire, one second after logon:

```
35=8  11=MM3b751dd2cc35c9ba  41=MM11e423f183606de4  37=1552323
55=IPTCHFRG  54=2  38=11557  44=51.09  151=11557  14=0  32=0
```

`41=` present and `151=11557` — that is the **replace acknowledgement**,
describing an order working with 11,557 shares. The real sequence:

1. The maker replaces a quote at ~16:02:30.
2. The gateway marks the OLD order `REPLACED` and waits for the ack.
3. The gateway restarts at 16:02:35, **before the ack arrives**.
4. The boot prune drops the old order. `Replaced` is in
   `dfa.TerminalStates`, so this step is CORRECT.
5. The ack lands at 16:02:36 naming the NEW ClOrdID. The restarted
   gateway has an empty registry and has never seen it.
6. `tracker.ApplyExecutionReport` returns nil → discarded.
7. The order works at the venue with nothing on our side pointing at it.
   Every later fill dies the same way.

So the prune is not the defect. **The defect is that we discard an
execution report for an order we do not recognise.**

## 3 · ⭐ tZERO already enumerates our resting orders. We bin it.

At 16:02:36 tZERO sent execution reports for **13 orders**, including all
four that went on to bleed. The gateway discarded all 13.

This is the venue telling us, unprompted at logon, what it believes is
working. It is the reconciliation source we were about to go and build.

## 4 · The fix — and the one NOT to build

⛔ **Do not add Order Mass Status (`35=AF`).** It was proposed in-session
and is withdrawn. `35=AF` and `35=AI` have **never appeared on this
wire**, so it means an untested message plus a tZERO dependency, to fetch
data the venue already hands us at every logon.

✅ **Adopt, do not discard.** On an execution report for an unknown
ClOrdID where `151 > 0` (working at the venue), build the tracker row
from the report itself — it carries ClOrdID, OrderID (37), symbol (55),
side (54), quantity (38), price (44), leaves (151), cum (14) and account
(1) — then apply and publish normally.

That single change fixes three things at once:

- **the loss** — the fill reaches the maker;
- **cancellability** — `guardRequest` does `tracker.Get(origClOrdID)`, so
  an untracked order cannot be cancelled at all today;
- **boot recovery** — because the venue enumerates at every logon.

⚠ Hasan's PR #13 re-publishes the refused report, which fixes the loss.
It does not by itself create the tracker row, so without adoption the
next fill on the same order is unknown again — which is what 42 discards
across 5 orders looks like.

## 5 · What made it likely

The restart went in while the maker was live and churning. The ordered
ceremony (halt taker → stop engine → `cancel_all` → swap binary → engine
→ taker) exists precisely so nothing is in flight at the swap. Adoption
removes the sharp edge; quiescing first would have avoided it outright.

## 6 · Also corrected

- **The taker did NOT halt** and no alert fired. The 17-08 handover said
  it would have. It traded through the restart untouched — it was the
  MAKER's orders (`MM` prefix), not the taker's (`MMSN`).
- **`pending_request` discards: 0.** Production confirmation that
  `oe_adapter.go:474` was never the path, as ruled out earlier that day.
- The blast radius is NOT the 1,982 pruned entries. The prune was right
  about ~1,977 of them; only the in-flight replaces were harmed.

## 7 · Next

1. PR #13 + the §4 adoption change, one deploy (Hasan).
2. `458fc0b` on PR #8 must land BEFORE any "alert on any shares-carrying
   discard", or resend duplicates drive it to constant noise.
3. The 5 orphaned orders still need truing up, and cannot be cancelled
   until adoption ships. Venue OrderIDs: 1552323, 1552340, 1552334,
   1552336.
