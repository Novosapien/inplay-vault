---
description: "The Go maker's first run against a real venue — gateway_ops ported, four real defects found, and the market data feed dying under a 1,520-cancel sweep"
---

# 2026-08-20 (b) — The Go maker's first live venue run

> **Who:** George + AI session, with Hasan on the gateway and NATS.
> **Type:** build + live operations. Code changed, infrastructure changed, a real venue traded against.
> **Refs:** Go repo `feat/phase-3-ingestion` · `HANDOVER-to-venue-test.md` ·
> [[market-maker/go-port-findings|GP-17]] · `deploy/OBSERVABILITY-REDEPLOY.md` §2.2.
> **⚠ Ended with the market data feed down and the maker stopped.**

## What we did

**Ported `gateway_ops` — the boot healer's seam.** `GET /orders/mm`, X-Ops-Key
gated, fail-open at every step. It went in as its own package
(`internal/adapters/gatewayops`) because `adapters → runtime → poller → adapters`
is a real import cycle. 20 plants, four guards mutation-tested.

**Stood up a second maker box.** `inplay-market-maker-go` at `10.0.2.4`,
n2-standard-2, Debian 12, 50 GB pd-ssd journal disk to match the original.
Firewall rules 2089/2090 added for the new IP, since the existing grants were
pinned to `10.0.2.3/32`.

**Ran the Go maker against the real venue, four times.** Each run found
something. The last one is still the one that matters least — the first three
found defects.

**Corrected `docs/perf-gate.md` §0**, which still listed three blockers that
cleared on 20-08.

## What we learned

### ⭐ The boot healer works against a real venue

Its first true run, and the reason `gateway_ops` was ported today:

```
boot heal: HEALED — 1358 fetched · cancel-unknown 1358 · sent 1358 of 1358
           · fetch 54.4 ms · 3388.7 ms
```

It read the venue, judged all 1,358 orders as ours-but-unknown, and cancelled
every one. Earlier the same day it produced a correct **zero-cancel** read
against an empty book. Both halves of AC8 exercised live.

⚠ It only worked because Hasan fixed **egress rule 2087** that afternoon — the
rule was pinned to `10.0.1.2/32`, so packets to the new MM gateway were dropped
with no RST. I had eliminated ingress, host firewall, listener, subnet and
service account and never checked the egress direction. Hasan found it.

### ⭐ The reconciler is provably correct

Reconstructed every order's lifecycle from the venue's own FIX wire log:

```
82,195 execution reports across 180 symbols
final live orders: 1,520
orders per book:  6 → 51 books · 8 → 48 · 10 → 35 · 12 → 40
BOOKS THAT EVER HELD A DOUBLED (price,side) LEVEL: 0 — NONE
```

Not once did the maker hold two live orders at one price and side. Every book
stayed inside `MinLevels 3 / MaxLevels 6`. **The 08-08 doubled-levels defect
does not recur.** The wire log's 1,520 matched `/orders/mm`'s 1,520 exactly.

### ⚠ The dead-man was effectively off, and that is why books accumulated

Both gateways carried `MM_DEADMAN_TIMEOUT_MS=604800000` **and**
`MM_DEADMAN_BOOT_GRACE_MS=604800000` — seven days each. The boot grace had not
been noticed at all.

The maker has **no cancel-on-shutdown path**. So every stop left its whole book
resting and nothing swept it. Across four runs the venue accumulated books.

Restored to the 08-14 values (`10000` / `30000`) and proven immediately:

```
17:11:42  dead-man armed at boot with resting MM orders  restingMM=1520  grace=30s
17:12:12  DEAD-MAN FIRED — no MM heartbeat since gateway boot
          → 1,520 sweep cancels sent
venue: 1,520 sent · 1,520 execution reports · 1,520 CANCELLED · 0 rejects
```

## What went wrong

### 1 · ⚠⚠ Phase 4b's legs were wired at one end only

The first live boot died with SIGSEGV on the **first gateway message**.
`compose.go` built both legs and handed their DRAIN to `runtime.Options`, but
the `stack` literal never assigned `inbound`, `readings` or `venueSymbols` —
three fields, **zero assignments**. The engine drained two queues nothing could
fill, and `main.go:150` dereferenced a nil `*inboundLeg`.

⚠ **No test in `cmd/mm` had ever called `composition.build()`.** Every test
hand-builds a `&stack{...}` literal, and a literal a test wrote cannot catch the
composition failing to write one. `unwiredLegs()` had been emptied on the
strength of half a wiring.

Fixed, with `cmd/mm/compose_legs_test.go` driving the real `build()`.
Mutation-checked.

### 2 · ⚠⚠ A fresh journal does not produce fresh order ids

Two duplicate-ClOrdID storms, the second at **68% rejects** (3,740 of 5,471).

The mint is `sha256(security | context | side | slot | configVersion)` —
deterministic, no nonce, no run id, no timestamp. Wiping the journal changes
none of those inputs, so every boot under the same salt re-mints the identical
sequence and the venue refuses them.

⚠ **The rule was already written down and I broke it.** From
`deploy/OBSERVABILITY-REDEPLOY.md` §2.2, recorded after the **07-08
duplicate-reject deadlock**: *keep the journal → keep the version; take a fresh
journal → bump the version.* R-D06 bumps `MM_CONFIG_VERSION` on every deploy. I
redeployed three times without bumping.

Bumping to `CFG-0039-GO` took rejects to **zero**.

### 3 · ⚠⚠ A new durable replayed a week of history into a live engine

The readings leg had never bound — `readings 0 seen` for 47 minutes, fair value
frozen on the reviewed numbers. Two causes, both ours:

- `mm-engine` is Python's durable and could not be reused (`max waiting can not
  be updated`). Gave the Go maker its own name via `MM_READINGS_DURABLE`.
- ⚠ **The NATS grants were written for a PUSH consumer.** Our Go client is a
  PULL consumer, so `$JS.API.CONSUMER.MSG.NEXT` had never been granted to
  anyone. Recorded as **GP-17**.

Once Hasan granted it, the new durable — created with JetStream's default
**deliver-all** — began at the start of the stream:

```
16:42:19 → 16:43:28  (69 seconds)
  probability_update   28,592     provider timestamps = 2026-08-14
  official_result       6,636     ← historical game settlements
  ORDER_REPLACED        3,618     ← repricing a LIVE venue off them
```

**494,228 messages were still pending** when I stopped it — another ~16 minutes
of last week. ⚠ Our own code predicted this: *"If first-boot volume ever
matters, the policy is a construction-time choice HERE."* Python never met it
because `mm-engine` was created months ago and every boot resumes from a cursor.

Fixed: the deliver policy is explicit, `MM_READINGS_FROM_NEW` controls it,
default unchanged, and the boot log now states where a durable starts.

### 4 · ⚠⚠ A 1,520-cancel sweep killed the market data feed

The last and unresolved one. The dead-man swept 1,520 orders at 17:12:12. The
market data publisher `fix-md-v8` stopped at **17:12:20** and has not produced a
venue update since:

```
IPTCBILL  src_ts=17:12:20.796  seq=186485      IPTCGIAN  src_ts=17:12:20.939
IPTCBEAR  src_ts=17:12:20.795  seq=186478      IPTCEAGL  src_ts=17:12:20.582
IPTCBROW  src_ts=17:12:20.558  seq=186223      IPTCJETS  src_ts=17:12:20.265
IPTCVIKI / IPTCPANT / IPTCRAVE — no frame at all
```

Every book, the same second. The publisher keeps re-broadcasting the frozen
frame every ~25 s, so the panel shows **two-sided books that do not exist** —
the venue confirmed all 1,520 cancels. The panel is downstream via
`centrifugo-bridge.service` (NATS `market.book` → Centrifugo → panel), so it
shows the same frozen source.

⚠⚠ **This is the finding that matters for Saturday.** If a full-book sweep
blanks market data, then any dead-man fire during the IPO takes the app's prices
with it.

### 5 · My own errors, recorded

- Claimed the MM index under-reports our book. It does not — 1,520 = 1,520. I
  over-read an 8-vs-9 difference between two reads seconds apart.
- Asserted book levels were "not ours", then reversed, then reversed again.
  Only the wire log settled it. ⭐ **The lesson: on a moving engine, two reads
  taken seconds apart are not evidence. Quiesce first, or read the wire log.**
- Spent hours reasoning about who owned frozen price levels without ever
  testing whether the feed producing them was alive. It was not.
- Sent two Slack messages from the wrong account before noticing the connector
  is authenticated as Max, not George.

## Decisions made

- **`MM_BOT_ID=mm-2` for the new box** — ⚠ but bot id is NOT in the ClOrdID
  mint seed, so it does not separate orders. Only `MM_CONFIG_VERSION` does.
- **`MM_CONFIG_VERSION=CFG-0039-GO`** — R-D06's ceremony, and the only lever
  that separates the two engines' order ids. ⚠ It also re-salts every drawn
  price, so the Go maker's book is not price-comparable to Python's.
- **`MM_READINGS_DURABLE=mm-engine-go`** — a deliberate divergence from the pin,
  recorded at the call site. Python hardcodes one name because one engine ever
  existed.
- **Dead-man restored to 10 s / 30 s grace** on the MM gateway.
- **The IPO offering interaction is accepted risk until Saturday** — the
  dead-man does not distinguish the offering from MM quotes.

## Questions opened

- ⚠ **Why did `fix-md-v8` die under the sweep, and what is its capacity?**
  Unresolved. Owner: Hasan. Blocks trusting the panel.
- ⚠ **173 orders are stranded on FHINPLAY01** — the IPO offering, 900,000 shares
  each, one per book on 170 books. Cancel-affinity means only that session can
  cancel them, and the MM gateway warns a book carried across the service split
  is *"unsweepable from here"*.
- ⚠ **Push vs pull (GP-17)** — keep pull and record it, or move to the legacy
  API for a faithful push consumer? Unmeasured under load either way.
- ⚠ **The replace rate is a floor, not a ceiling.** Every number Hasan sized
  Redis against was taken with the readings leg dead. With probabilities moving
  fair value it goes up.

## Next

1. **Bring market data back** — decide whether to restart the retail gateway
   (⚠ it carries real retail traffic) or hand it to Hasan.
2. Deploy the deliver-policy fix, fresh run directory, bumped config version,
   and take a clean run with readings alive for the first time.
3. Then the real question this session never got to: **does the Go ladder match
   Python's geometry?** The quoting gate against the reference, not screenshots.
