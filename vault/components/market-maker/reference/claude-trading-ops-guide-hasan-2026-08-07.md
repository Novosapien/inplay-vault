# Driving the Trading Stack with Claude Code

**Operator guide — how to ask Claude to update buying power, read FIX logs, and query the order-entry and market-data services.**

Written 2026-08-07. Everything here was verified live against the running stack on that date.

---

## 1. The three surfaces, and which one reaches what

There is no single endpoint that does everything. Three doors, and knowing which one a request needs is most of the work.

| Surface | Where | Auth | Reaches |
|---|---|---|---|
| **Admin proxy** | Cloud Run, `https://inplay-admin-proxy-796178926251.us-east4.run.app` | `Authorization: Bearer <PROXY_API_KEY>` | Market data, orders, positions, NATS, Centrifugo, Redis, gateway health + logs |
| **FIX gateway** | GCE VM `inplay-fix-gateway`, `10.0.1.2:8080` | **None** — but VPC-only, so unreachable without SSH | Buying power, position transfer, MD probe, raw logs, restart |
| **Admin panel** | `https://inplay-admin-panel-trading.vercel.app` | Password login | Everything the proxy exposes, with a UI |

The critical asymmetry: **buying power is not on the proxy.** `POST /buying-power` exists only on the gateway's own HTTP server, which binds inside the VPC and has no authentication of its own. The only way in from a laptop is an IAP-tunnelled SSH session onto the VM, then curl against `localhost`. That is not an oversight to route around — it is the reason an unauthenticated endpoint that can rewrite an account's cash is safe to leave running.

```
Your laptop ──HTTPS+key──> Cloud Run proxy ──VPC──> gateway :8080   (market data, orders)
Your laptop ──gcloud SSH via IAP──> gateway VM ──> localhost:8080   (buying power, transfers)
```

---

## 2. Credentials

**No secret values are written in this document, and none should be.** Secrets rotate; a doc that pastes them is wrong the moment they do, and it turns a runbook into a leak the moment it is shared. Every credential below lives in GCP Secret Manager on project `inplay-497712`, and Claude fetches it at the moment of use.

```bash
gcloud secrets versions access latest --secret=<name> --project=inplay-497712
```

That one command shape fetches any of them. `gcloud secrets list --project=inplay-497712` shows the full set.

| What | Secret name |
|---|---|
| **Proxy API key** — the one you need most | `inplay-proxy-api-key` |
| NATS, as the proxy uses it (both users) | `inplay-nats-token` |
| NATS, per service | `inplay-nats-gateway-token`, `inplay-nats-mm-token`, `inplay-nats-trading-token`, `inplay-nats-admin-token`, `inplay-nats-centrifugo-token`, `inplay-nats-leaderboard-token`, `inplay-nats-sportradar-token`, `inplay-nats-ad-token` |
| Centrifugo API key / HMAC | `inplay-centrifugo-api-key`, `inplay-centrifugo-hmac` |
| Redis auth / CA / URL | `inplay-redis-auth`, `inplay-redis-ca-cert`, `inplay-redis-url` |
| tZERO REST (staging) | `tzero-staging-client-id`, `tzero-staging-client-secret` |
| tZERO REST (test) | `tzero-test-apikey`, `tzero-test-client-secret` |
| Admin API key | `inplay-admin-api-key` |
| Loadrunner token | `inplay-loadrunner-token` |

The tZERO REST credentials are a **different surface from the FIX session** and the two are not interchangeable. REST (`gateway-web-api-staging.tzero.com`) does account creation and account read; the FIX OE session does orders, account edit and position transfer. Everything in this guide except account *creation* goes over FIX.

**Prerequisite:** `gcloud` authenticated as `hasan.ahmed@novosapien.ai` with project `inplay-497712`. Check with `gcloud config list`. If Claude is being told "permission denied" on secret access, that is the auth, not the code.

The gateway's own FIX credentials — session host, ports, comp IDs — live in `/opt/fix-gateway/.env` on the VM, loaded by systemd via `EnvironmentFile`. They are not in Secret Manager and not in git. Read them over SSH when needed; never copy them into a file.

Admin panel login passwords are Vercel environment variables (`ADMIN_PASSWORD_HASH`, `GROUPS_PASSWORD_HASH`), stored hashed.

---

## 3. The account & position write commands

Three FIX messages change account or position state. They are **separate MsgTypes with separate entitlements** — the fact that one works tells you nothing about the others, which is exactly how we found out `UEPR` is dead while `UEAR` is live.

| Command | MsgType | Endpoint | State |
|---|---|---|---|
| **Buying power / risk limits** | `UEAR` | `POST /buying-power` | ✅ live |
| **Seed inventory** | `UPT` | `POST /position-transfer` | ✅ live, ⚠ one-way |
| **Set opening position** | `UEPR` | `POST /position` | ❌ silently dropped |

All three share one behaviour worth internalising: **the endpoint returns `202 Accepted` and a `clOrdId`, never the venue's answer.** The real reply lands asynchronously on the FIX session and goes to the log. A `202` means "sent", not "worked" — every one of these is a two-step operation.

---

### 3a. Update buying power — `UEAR`

Sets an account's cash (FIX tag 9255 `CASHo`) and day-trading buying power (9253 `DTBPo`) by sending one `35=UEAR` Edit Account Request over the live OE session.

**What to say to Claude:**

> "Set cash to 5,000,000 on account 9890898322"
> "Raise the max order rate on the MM account to 2000/sec"

**What Claude runs:**

```bash
gcloud compute ssh inplay-fix-gateway \
  --zone=us-east4-a --project=inplay-497712 --tunnel-through-iap \
  --command="curl -s -X POST localhost:8080/buying-power \
    -H 'Content-Type: application/json' \
    -d '{\"account\":\"9890898322\",\"cash\":5000000}'"
```

**Fields** — every one optional except `account`. Zero or omitted values are **not sent**, so cash can be set without touching DTBP:

| Field | FIX tag | Notes |
|---|---|---|
| `account` | — | **Required.** |
| `cash` | 9255 CASHo | Initial cash. |
| `dtbp` | 9253 DTBPo | Day-trading buying power. |
| `dtMult` | — | DTBP multiplier. |
| `maxOrdRate` | 8935 | IPLY default 100/sec — roughly 17× below what the market maker needs at full ladder. |
| `maxDupOrdRate` | 8936 | IPLY default 20/sec. A ladder re-anchor is duplicate-shaped, so the default clips it. |
| `stopWashTrades` | 8985 | Boolean pointer: **omit to leave alone**, since `false` is a meaningful value. |
| `streetCapacity` | 9282 | `A` Agency, `P` Principal, `R` Riskless. |
| `mpid` | 9251 | Add-only on `UAAR`; present here for completeness. |
| `mmType` | 9289 | The spec enumerates **no values** for this and there is no read-back. **Do not populate on a guess.** |

**Step 2 — read the answer.** tZERO replies `UEARa` (accept) or `UEARx` (reject) on the session, and it goes to the log, not to your curl:

```bash
gcloud compute ssh inplay-fix-gateway \
  --zone=us-east4-a --project=inplay-497712 --tunnel-through-iap \
  --command="sudo journalctl -u fix-gateway.service --since '2 min ago' --no-pager | grep -iE 'UEAR|<clOrdId>'"
```

On a rejection, **FIX tag 58 carries the reason**. That is the field to ask for by name — "what did tag 58 say" — rather than accepting "it was rejected". A healthy accept came back in 16ms when this was proven live on 2026-08-05.

---

### 3b. Seed inventory — `UPT` (position transfer)

The working inventory mechanism. Takes **signed deltas**, not absolute values.

**What to say to Claude:**

> "Seed 5,000 shares of IPTCEAGL into the MM account at $145"

**What Claude runs:**

```bash
gcloud compute ssh inplay-fix-gateway \
  --zone=us-east4-a --project=inplay-497712 --tunnel-through-iap \
  --command="curl -s -X POST localhost:8080/position-transfer \
    -H 'Content-Type: application/json' \
    -d '{\"account\":\"9890898322\",\"symbol\":\"IPTCEAGL\",\"txfrQty\":5000,\"txfrCost\":725000}'"
```

| Field | FIX tag | Rules |
|---|---|---|
| `account` | 1 | **Required.** |
| `symbol` | 55 | **Required.** |
| `txfrQty` | 9386 | **Required, non-zero.** No zero no-op exists here, unlike UEPR. |
| `txfrCost` | 9387 | **Required.** Must carry the **same sign** as `txfrQty`, and `txfrCost / txfrQty` — the average price — must be **> 0.00**. |
| `confirmTyp` | 9551 | Optional. 1 = administrator confirm, 2 = agent confirm. |

The gateway pre-validates all three constraints and refuses locally with a readable error before anything reaches the wire, so a malformed transfer costs nothing. `txfrCost` is the **total cost, not the price** — 5,000 shares at $145 is `txfrCost: 725000`. Getting that wrong sets a wrong basis on a position you cannot unwind.

> ⚠⚠ **CONTRADICTED BY MEASUREMENT, 2026-08-19.** The line above says `txfrCost` is the **total**. Probed live against the session wire log that afternoon, the venue treats **9387 as a PRICE PER SHARE**: 7 shares at `txfrCost=7.00` booked a basis of **49.00**, and a second transfer of 2 shares at 3.00 moved the basis by exactly **6.00**. The 05-08 probe used 1 share at 1.00 — the single quantity where a total and a per-share price are the same number, which is why this went unnoticed for two weeks. The spec's own `(TxfrCost / TxfrQty) = averagePrx` reads as a total, so the spec and the venue disagree and **one of them is wrong**. ⚠ The measurements were taken on an **IPLY** account; the unit is still unconfirmed on **IPLM**, where the maker lives. Settle it with one transfer of a distinctive quantity at a distinctive price into a throwaway symbol BEFORE any real seed — at 900,000 shares the wrong reading is wrong by a factor of 900,000, and UPT cannot be undone. See [[market-maker/decisions]] 2026-08-19e.


**`confirmTyp` is not a two-step commit.** The names imply one; the OMS does not implement it that way. Corrected 2026-08-05: each send is an independent transfer regardless of `confirmTyp` — sending 1 then 2 produced **two** transfers (position 2), not one confirmed transfer of 1. Different ClOrdIDs on the two messages were the tell.

**Reply:** `UPTa` accept / `UPTx` reject, in the log. The auto-generated ClOrdID is prefixed `T`.

> ⚠️ **One-way, and not idempotent.** Read §7 before using this in anger.

---

### 3c. Set opening position — `UEPR` (does not work)

Documented so you recognise it, not so you use it. `UEPR` sets a position's *opening* state — 9381 `Qto` and 9382 `Eto` as absolute carryover values rather than UPT's signed deltas, which would make a retry safe if it functioned.

```bash
# for reference only — this goes nowhere
curl -s -X POST localhost:8080/position \
  -H 'Content-Type: application/json' \
  -d '{"account":"3505873306","symbol":"IPTCCOWB","secTyp":"EQT","qto":0,"eto":0}'
```

| Field | FIX tag | Notes |
|---|---|---|
| `account`, `symbol` | 1, 55 | Required. |
| `qto` | 9381 | Opening quantity. Required — sent as a pointer so an omitted field errors rather than silently writing zero. |
| `eto` | 9382 | Opening equity. Same. |
| `secTyp` | 9388 | e.g. `EQT`. |

**Tested 2026-07-28 13:32 and it is not enabled on this session.** A well-formed no-op drew no `UEPRa`, no `UEPRx`, and — the telling part — no session Reject (`35=3`) and no Business Message Reject (`35=j`) either. An engine that understood the MsgType and refused it would say so. Silence means it is dropped before anything decides. The session stayed logged on throughout.

That is why entitlement has to be probed per MsgType, and why `UPT` was worth testing separately even after `UEPR` failed.

---

## 4. Check FIX logs

Two routes, and they show different things.

**Through the proxy** — the gateway's in-memory ring buffer. Fast, no SSH, but only recent lines and only what the gateway chose to buffer:

```bash
KEY=$(gcloud secrets versions access latest --secret=inplay-proxy-api-key --project=inplay-497712)
curl -s -H "Authorization: Bearer $KEY" \
  "https://inplay-admin-proxy-796178926251.us-east4.run.app/gateway/logs?lines=200"
```

**Over SSH** — the real systemd journal. Full history, filterable, and the only place to see the raw session:

```bash
gcloud compute ssh inplay-fix-gateway \
  --zone=us-east4-a --project=inplay-497712 --tunnel-through-iap \
  --command="sudo journalctl -u fix-gateway.service --since '30 min ago' --no-pager | tail -100"
```

Useful filters — say the symptom, not the grep, and let Claude pick:

| Looking for | Filter |
|---|---|
| One symbol's activity | `grep IPTCEAGL` |
| Account edit replies | `grep -iE 'UEAR'` |
| Position transfer replies | `grep -iE 'UPT'` |
| Rejections of any kind | `grep -iE 'reject|35=3|35=9'` |
| Book/depth activity | `grep -i book` |
| Session up/down | `grep -iE 'logon|logout|disconnect'` |

**Service state:** `systemctl status fix-gateway.service`, and `systemctl show -p ActiveEnterTimestamp --value fix-gateway.service` for when it last restarted — worth checking before trusting any "it's not working", because a config change only takes effect on restart.

---

## 5. Query the market-data service

All through the proxy, all `GET`, all safe to run freely.

```bash
KEY=$(gcloud secrets versions access latest --secret=inplay-proxy-api-key --project=inplay-497712)
BASE="https://inplay-admin-proxy-796178926251.us-east4.run.app"

curl -s -H "Authorization: Bearer $KEY" "$BASE/market/quotes"            # top of book, all symbols
curl -s -H "Authorization: Bearer $KEY" "$BASE/market/book/IPTCEAGL"     # full depth, one symbol
curl -s -H "Authorization: Bearer $KEY" "$BASE/market/supply"            # minted token supply
```

**`/market/quotes`** reads Redis, which the gateway writes on every quote. Each entry carries a `timestamp` — **check it**. A quote is only ever overwritten by a later quote, never cleared: when a venue snapshot comes back with both sides empty the gateway publishes nothing at all, so a symbol that goes quiet keeps its last price indefinitely. IPTCBILL currently shows an $89.17 bid stamped 2026-07-24 against an empty book. A price with no timestamp check is not a price.

**`/market/book/{symbol}`** returns the whole ladder. `retained: false` is a normal answer, not an error — it means nothing has been published for that symbol, which is the truth for most of the 170. Depth is never persisted: the gateway publishes on core NATS, the bridge relays to Centrifugo `market:book.{symbol}`, and that namespace retains the last frame for 60s. Since every message carries the whole book rather than a delta, the retained frame *is* the current book.

**`/market/supply`** is admin-set minted supply from Redis, plus live book totals from tZERO's public snapshot REST when `TZERO_MDT_BASE_URL` is configured — it currently is not, so those fields are absent. Writing supply is `POST /market/supply` with `{"supply": {"IPTCEAGL": 1000000}}`; a value of zero or less removes the entry.

**Reading depth from the source instead:** `GET /quotes` on the gateway itself (over SSH) is the same Redis data one hop earlier — useful only when you suspect the proxy, not the data.

---

## 6. Query and drive the order-entry service

### Submitting an order

```bash
curl -s -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  "$BASE/orders" -d '{
    "userId": "admin",
    "symbol": "IPTCEAGL",
    "side": 1,
    "quantity": 10,
    "price": 145.50,
    "clOrdId": "ADM12345",
    "timeInForce": 0
  }'
```

| Field | Rules |
|---|---|
| `side` | **Integer, not string.** 1 = buy, 2 = sell, 5 = sell short. |
| `clOrdId` | Max 20 chars, **no leading zeros**. Must be unique per order. |
| `timeInForce` | 0 DAY, 1 GTC, 3 IOC, 4 FOK, 6 GTD. |
| `quantity` / `price` | Both must be > 0. |
| `walletAddress` | Optional; becomes FIX tag 9829 for on-chain settlement. |

### Watching what came back

```bash
curl -s -H "Authorization: Bearer $KEY" "$BASE/orders/history?limit=50"      # recent execution reports
curl -s -H "Authorization: Bearer $KEY" "$BASE/positions/history?limit=50"   # recent position updates
curl -sN -H "Authorization: Bearer $KEY" "$BASE/orders/stream"               # live SSE feed
```

### Cancelling and replacing

Fully implemented — just not on the admin proxy, which is the one place you'd look first.

The gateway subscribes to two NATS subjects and turns them into FIX:

| Subject | FIX | Purpose |
|---|---|---|
| `gateway.orders.cancel` | `35=F` OrderCancelRequest | Cancel one resting order |
| `gateway.orders.replace` | `35=G` OrderCancelReplace | Amend price / quantity / TIF |
| `gateway.orders.mm.cancel_all` | — | Market-maker sweep; also fired by the dead-man watchdog |

**Through the trading service** (authenticated, per-user, the app's path):

```
POST /orders/{clOrdId}/cancel     → 202 { request_cl_ord_id }
POST /orders/{clOrdId}/replace    → 202 { request_cl_ord_id }
```

Gated on `require_trader` and ownership of the order, and only valid while the order is resting — anything else is `409 NOT_CANCELABLE`. Like every other write here it returns `202`: the outcome (`ORDER_CANCELLED` / `CANCEL_REJECTED`) arrives on `personal:orders#{sub}`, not in the response.

**Through NATS directly** — the route for an admin or MM order that no app user owns, since the REST path is ownership-gated. Publish to `gateway.orders.cancel`:

```json
{ "userId": "admin", "clOrdId": "C<new-id>", "origClOrdId": "ADM12345" }
```

> **The cancel carries its own ClOrdID.** `clOrdId` is a *new* id minted for the cancel request (the trading service prefixes them `C`); `origClOrdId` is the resting order you want gone. Putting the resting order's id in both fields is the classic way to get a `35=9` OrderCancelReject.

**The gap:** the admin proxy exposes no cancel route, so there is no one-line curl for it the way there is for `POST /orders`. Worth adding.

**Also stale:** the admin panel's cert checklist still marks cancel and cancel/replace as *"not yet implemented in gateway"*. That was true once; the gateway has both subscriptions now.

---

## 7. Things that do not undo

Read this section before asking for any of it.

**`POST /position-transfer` is one-way.** Measured 2026-08-05: positive transfers apply; negative transfers are *accepted* (`UPTa`) but never move the position, with or without `ConfirmTyp`. Reducing inventory means selling it in the market. It is also **not idempotent**, and the only position read-back is tag 9383 on an execution report — so a retry after a timeout silently double-seeds. Anything seeding at 170-symbol scale needs its own ClOrdID ledger.

**`POST /position` (UEPR) is dead.** Entitlement is per-MsgType on this session: `UEAR` is live, `UEPR` is not. It will accept your request and nothing will happen.

**Orders are real.** The OE session points at a live venue. There is a loopback toggle (`GET`/`POST /gateway/loopback`) — check it before assuming an order was simulated.

**Gateway restart drops all subscriptions.** The venue cancels everything on disconnect and replays from scratch on reconnect. `POST /gateway/restart` is a real interruption to the market-data feed, not a refresh.

---

## 8. How to phrase things

The pattern that works is **say the outcome, not the plumbing**. Claude can find the endpoint; what it cannot guess is which account, which symbol, and whether you meant it.

Good:
- "Set cash to 5M on the MM account and confirm tZERO accepted it"
- "Seed 5,000 IPTCEAGL at $145 into the MM account — check the basis came out right"
- "Is the book on IPTCPATR still 9 levels deep?"
- "Why did that order get rejected — check the logs"
- "What's the spread on every symbol that has a live quote?"

Ask for the confirmation explicitly, because the async replies make it easy to stop one step early. "And confirm it landed" is the difference between a `202` and knowing it worked.

Worth stating up front when true:
- **Which account.** There is more than one, and they are not interchangeable.
- **Whether it is a probe or an operation.** "Try a no-op first" is a real and useful instruction on anything that writes.
- **Whether you want it applied or just costed.** "What would it take to…" reads very differently from "do it".

---

## 9. Quick reference

**Gateway, over SSH** (`gcloud compute ssh inplay-fix-gateway --zone=us-east4-a --project=inplay-497712 --tunnel-through-iap --command="..."`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Session + subscription state |
| GET | `/logs?lines=N` | Ring-buffer log |
| GET | `/quotes` | Top of book from Redis |
| POST | `/buying-power` | **35=UEAR** — cash, DTBP, rate limits |
| POST | `/position-transfer` | **35=UPT** — seed inventory ⚠ one-way |
| POST | `/position` | 35=UEPR — not entitled, dead |
| POST | `/md/probe` | One MarketDataRequest, chosen depth/entry types |
| GET/POST | `/loopback` | Simulation toggle |
| POST | `/restart` | ⚠ drops all MD subscriptions |

**Proxy, over HTTPS + Bearer key** (`https://inplay-admin-proxy-796178926251.us-east4.run.app`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Gateway + NATS + Redis aggregate |
| GET | `/gateway/health`, `/gateway/logs?lines=` | Gateway passthrough |
| GET | `/market/quotes`, `/market/supply`, `/market/book/{symbol}` | Market data |
| POST | `/market/supply` | Set minted supply |
| POST | `/orders`, `/orders/batch`, `/orders/burst` | Order entry |
| GET | `/orders/history`, `/orders/stream` | Execution reports |
| GET | `/positions/history`, `/positions/stream` | Position updates |
| GET | `/nats/streams`, `/nats/monitor`, `/nats/streams/{s}/messages` | NATS inspection |
| GET | `/centrifugo/info`, `/channels`, `/history/{channel}` | Realtime inspection |
| GET | `/redis/info` | Redis state |

**Infrastructure**

| Thing | Value |
|---|---|
| GCP project | `inplay-497712` |
| Region / zone | `us-east4` / `us-east4-a` |
| Gateway VM | `inplay-fix-gateway`, `10.0.1.2`, service `fix-gateway.service`, env `/opt/fix-gateway/.env` |
| NATS | `10.0.2.2:4222`, monitor `:8222` |
| Centrifugo | `10.0.3.12:8000` (internal LB VIP) |
| Redis | `10.78.64.3:6378` (TLS) |
| Proxy deploy | `cd inplay-admin-panel-trading/proxy && ./deploy.sh` |
| Panel deploy | push to `main` — Vercel builds automatically |
