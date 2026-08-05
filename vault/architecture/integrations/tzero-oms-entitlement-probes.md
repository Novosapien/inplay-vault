# tZERO OMS message entitlement — probe log

> **Integration:** [[t0]] · [[integrations]] · spec: [[tzero-account-position-fix]]
> **Status:** Live empirical record. Append a row per probe; never delete one.
> **Session:** OE `FHINPLAY01->TZFIXORDQA` (staging/QA — tZERO run one environment, see T10)

---

## Why this exists

Entitlement for the OMS account-management messages is **per-MsgType, not
all-or-nothing**. That was not obvious: two silent probes in July led to the
recorded conclusion that "the account-management side of the protocol is not
enabled on this session" (`inplay-fix-gateway-go/internal/fix/tags.go`), and on
2026-08-05 a third probe disproved it. This table is the authority; correct the
code comment against it, not the reverse.

## What silence means

A probe that draws **no reply, no session Reject (35=3, reason 11) and no
Business Message Reject (35=j)** is being dropped before anything evaluates it.
An engine that parsed the MsgType and refused it would say so. So silence points
at session-level entitlement, not at our payload — no amount of tag-fixing helps.

## Probe log

| Date | MsgType | Account | Payload | Result | Verdict |
|---|---|---|---|---|---|
| 2026-07-27 | `UAAR` | both accounts, both plausible MPIDs (4 sends) | account create | **Silence** — no reply, no 35=3, no 35=j | ❌ Not enabled |
| 2026-07-28 13:32 | `UEPR` | `3505873306` | `IPTCCOWB`, Qto=0, Eto=0, SecTyp=EQT (well-formed no-op) | **Silence** — no `UEPRa`, no `UEPRx`, no 35=3, no 35=j. Session stayed logged on | ❌ Not enabled |
| 2026-08-05 11:57:02 | `UEAR` | `9890898322` | `1=9890898322 11=Bhl25dvljyv 15=USD 9251=IPLY 9270=1` (DTMult=1, a no-op vs the IPLY default) | **`UEARa` in 16ms** — `35=UEARa 11=Bhl25dvljyv 1=9890898322` | ✅ **ENABLED** |
| 2026-08-05 13:33:55 | `UEAR` | `5120866205` (George, with consent) | `1=5120866205 11=Bhl2820mc72 15=USD 8935=2500 9251=IPLY` — **MaxOrdRate 100 → 2500** | **`UEARa` in 13ms** — `35=UEARa 11=Bhl2820mc72 1=5120866205` | ✅ **Risk fields writable** |

| 2026-08-05 14:32:47 | `UPT` | `5120866205` (George, with consent) | `1=5120866205 11=Thl29oexpa6 15=USD 55=IPTCCOWB 9386=1 9387=1 9551=1` — transfer 1 share @ $1.00, ConfirmTyp=1 (admin confirm, first step) | **`UPTa` in 12ms** — echoes `9386=1 9387=1.000000`, but **not** the Qto/Eto/Qt/Et/Rpnl/Upnl the spec says come back | ✅ **ENABLED — inventory seeding unblocked** |

### What the 14:32 probe establishes — the important one

**`UPT` is entitled even though `UEPR` is not.** Both are position messages; only
one is enabled. That is the third independent confirmation that entitlement is
per-MsgType, and it removes the market maker's inventory blocker: offers require
seeded sellable inventory per symbol, `UEPR` was the only known route, and it is
dead. `UPT` is a live route.

Consequence for the MM account question (open since 22-07 as T1): a **regular
`INDIVIDUAL` account** configured via `UEAR` (`MaxOrdRate`, `DTBPo`, `CASHo`,
`MaxDupOrdRate`, the `Rmo_` toggles) and seeded via `UPT` appears sufficient for
v1. `MMType` was only strictly needed as a workaround — the Reg SHO bona-fide
market-maker locate exemption — for the case where inventory *could not* be
seeded and offers had to come from shorting against the 1,000-share/security
reserve. That case no longer applies. **`MMType`, `UAAR` and a non-INDIVIDUAL
account type are all off the v1 critical path.**

The remaining blocker is `35=F`/`35=G` cancel-replace, which is a build we own,
not a venue permission.

### Follow-up: `ConfirmTyp=2` (2026-08-05 15:06:53)

Sent the same transfer with `9551=2` (agent confirm, final step). **Also `UPTa`,
in 15ms** — and again **no position figures**: no `Qto`/`Eto`/`Qt`/`Et`/`Rpnl`/
`Upnl`, just `9386=1 9387=1.000000` echoed back.

So the two-step theory does not explain the missing figures. This OMS build
simply does not populate them on `UPTa`, at either confirm step.

### ⚠ Idempotency ambiguity — unresolved

`UPT` applies a **signed delta and is not idempotent**. The two sends carried
**different ClOrdIDs** (`Thl29oexpa6`, `Thl2am9ixq2`), which is how two
*independent requests* look, not two steps of one. So `5120866205` most likely
now holds **2 shares of IPTCCOWB at $2.00 cost basis**, not 1.

It cannot be confirmed from here: there is no position read-back. The REST
account view carries no positions, `UEPRa`/`UAU` never fire, and the only other
path — reading `9383 Qt` off an ExecutionReport — needs a live order, which
without `35=F` would rest until 23:59 ET.

**Exact-mirror reversal is available and is sign-safe.** Because transfers
compose as deltas, sending the precise inverse of what went out —
`txfrQty=-1, txfrCost=-1.00` at `ConfirmTyp=1`, then the same at `ConfirmTyp=2` —
restores the prior state under *either* interpretation (net −1 against +1, or
net −2 against +2). Do not send a single −2: that over-corrects to a short if the
two sends were in fact one transfer.

**Lesson for the MM build:** every `UPT` needs an idempotency discipline of its
own (a ClOrdID ledger, or reconciliation against a position read that does not
yet exist). A retry after a timeout silently double-seeds. This is the same class
of bug as the REST create timeout — see [[tzero-rest-onboarding-timeout]].

### What the 13:33 probe establishes

A **risk-management field** — not just the cash/DTBP fields already in the
builder — was accepted on an existing account via `UEAR`. So per-account risk
configuration is **self-service over FIX**, not a tZERO-side config request.

That directly unblocks the MM's order-rate ceiling: the IPLY default of 100/sec
is ~17× below the modelled 1,700 msg/s peak (5 levels/side × 34 live teams × 5
cycles/s), and we can raise it ourselves.

**Still acceptance, not application.** No read-back exists. The supporting
evidence that it took effect: the field is spec-documented with known semantics,
and its enforcement toggle (`8997 Rmo_EnforceMaxOrdRate`) is already ON per the
IPLY matrix, so the value should bite without further changes. Behavioural
confirmation — submitting above 100/sec and observing no rejection — is the only
real proof and has not been done.

**Gateway support added 2026-08-05** (`TagMaxOrdRate = 8935`, `TagMMType = 9289`,
`SendEditAccount` extended, `POST /buying-power` accepts `maxOrdRate`/`mmType`).
`mmType` is wired but deliberately unexercised — the spec enumerates no values
for it.

Payload verified against the spec after the fact: the `UEPR` probe was correctly
formed (Account, Symbol, Qto, Eto, SecTyp all present and valid per
[[tzero-account-position-fix]]). Its silence is genuinely entitlement.

## Current picture

| Message | Status |
|---|---|
| `UEAR` — Edit Account | ✅ Enabled, replies in ~16ms |
| `UAAR` — Add Account | ❌ Silent |
| `UEPR` — Edit Position | ❌ Silent |
| `UPT` — Position Transfer | ⬜ Never probed — separate MsgType, may carry separate entitlement |
| `UBT` — Balance Transfer | ⬜ Never probed — needs `BankIDN` from a `UABR` first |
| `UABR` — Add Bank | ⬜ Never probed |
| `UDAR` — Delete Account | ⬜ Never probed |
| `UAU` — Account Update (inbound) | Never observed at logon — but the spec marks it "Fading (being replaced by `UAARa`)", so absence is weak evidence |

## Why `UEAR` being live matters

`UAAR` and `UEAR` share one field table in the spec, and only `9251 AccMPID` is
Add-only. So **everything settable at account creation is also settable on an
existing account via `UEAR`** — including:

- `9289 MMType` — the MM classification
- `8935 MaxOrdRate` — the order-rate cap (IPLY default 100/sec)
- `8936 MaxDupOrdRate`, `9290 MaxOpenOrds`, `9291 MaxOpenPos`
- `8985 Rmo_StopWashTrades` and the rest of the `Rmo_` toggles
- `9255 CASHo`, `9253 DTBPo`, `9270 DTMult`

If that holds in practice, **per-account risk configuration is self-service over
FIX** rather than a tZERO-side config request. That is the single highest-value
thing to establish next, because the MM needs `MaxOrdRate` raised from 100/sec to
~2,500/sec and that was assumed to be blocked on a venue ask.

## The verification gap

`UEARa` confirms **acceptance, not application**. It echoes only `11 ClOrdID` and
`1 Account` — no field values. And the REST account view
(`GET /pi/v1/accounts/{id}`) exposes `id`, `type`, `status`, investor PII and
`investmentProfile` — **no risk fields, no MMType**. So there is currently **no
read-back path for anything written via `UEAR`.**

Consequences:
- Prefer probing fields with *known* semantics and *observable* effects
  (`MaxOrdRate`) over opaque ones (`MMType`, whose valid values the spec does not
  enumerate).
- Treat any `UEAR` write as one-way until a read path exists. `SendEditAccount`
  skips zero values, so a field may be settable but not clearable.

## Recovering an orphaned account id — the unsolicited `UAARa`

**tZERO pushes an unsolicited `35=UAARa` on the OE session whenever an account is
created via REST.** (Recorded in `inplay-onboarding-referral/deploy.sh`, and
confirmed 2026-08-05.) The gateway parses these into `handleAddAccountReply`, so
they land in `journalctl -u fix-gateway` even when the REST caller never receives
a response.

This is the read path that recovers a create that timed out:

```bash
sudo journalctl -u fix-gateway --since '<t0>' --until '<t1>' --no-pager | grep UAARa
```

Both accounts orphaned on 2026-08-05 were recovered this way:

| REST create | Token sent | Our 30s timeout | Unsolicited `UAARa` | Account | Real latency |
|---|---|---|---|---|---|
| `hasan.ahmed+mm@novosapien.ai` | 11:50:49 | 11:51:19 | **11:51:43** | **`1797733477`** | ~54s |
| `nova@novosapien.ai` | 12:07:08 | 12:07:38 | **12:08:32** | **`8427773360`** | ~84s |

**Creates are taking 54–84s.** That is the hard number behind the timeout bug: the
httpx `read` timeout was 30s *and* the Cloud Run request timeout is 60s, so even
a raised client timeout cannot help until the service timeout is raised too.

## ⚠ The recovered accounts exist in the OMS but NOT in REST

| Check | `1797733477` | `9890898322` (control) |
|---|---|---|
| `GET /pi/v1/accounts/{id}` | **404 `ACCOUNT_NOT_FOUND`** | 200, full record |
| `UEAR` over FIX | **`UEARa` in 10ms** | `UEARa` |

So the create reached far enough to mint an OMS account and announce it, then
failed before the REST-side record was finalised. That also explains the
deterministic fast `500 ACCOUNT_CREATION_FAILED` on every retry: the email is
taken, but the record is incomplete.

This is a **half-created state**, and it is the concrete form of the open T1
question about how REST ids map to OMS `AccNUMB`s. Normally they are the same
id-space — `9890898322` resolves in both. These two resolve in only one.

**For the market maker this may not matter.** The MM path is entirely OMS-side:
Tag 1 on orders, `UEAR` for risk config, `UPT` for inventory. None of it touches
REST. `1797733477` is addressable for all three. What is untested is whether it
can actually trade, and what PII/TIN state it is in — neither of which is
readable from our side.

## Related

- Order-entry side is unaffected and fully live — `35=D` proven, Tag 1 echoed on
  execution reports since 17-07.
- REST account creation (`POST /pi/v1/accounts/INDIVIDUAL`) is a **separate**
  surface from FIX entitlement and has its own failure mode — see
  [[tzero-rest-onboarding-timeout]].
