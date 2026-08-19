---
description: "Session note, 05-08 first probe stream: live probes proved UEAR and UPT are entitled on the tZERO OE session, and the account spec PDF landed in the repo"
---

# 2026-08-05c — OMS entitlement probes: UEAR and UPT are live

> **Who:** Hasan + Claude (build/probe session — first of the probe stream)
> **Re-labelled on merge:** filed on its own branch with no suffix. Main had
> already used the bare `2026-08-05` and `-b` slots, so this note takes `-c`.
> **Type:** build / research — live probes against the tZERO OE session
> **Refs:** `tZERO_FIX_AccountPosition_20251015.pdf` (obtained today) ·
> [[tzero-account-position-fix]] · [[tzero-oms-entitlement-probes]] ·
> gateway `internal/{fix,adapter,health}` (uncommitted)

## What we did

- Started from a security question about Cloud Armor coverage, which surfaced the
  trading API's `INPLAY_VENUE_PLACE_SUBS` allowlist and, from there, the MM
  account question.
- Tried to tZERO-onboard a market-maker account four times across two emails.
  All failed. Diagnosed the cause (below).
- **Obtained the Account & Position FIX Spec v3** — previously cited in
  `trading-architecture.md` but held nowhere. Now at
  `vault/architecture/integrations/sources/`, distilled in
  [[tzero-account-position-fix]].
- Extended the gateway: `TagMaxOrdRate` (8935), `TagMMType` (9289),
  `TagTxfrQty`/`TagTxfrCost`/`TagConfirmTyp` (9386/9387/9551), `UPT`/`UPTa`/`UPTx`
  MsgTypes, `SendPositionTransfer`, `handlePositionTransferReply`, and a
  `POST /position-transfer` probe endpoint. Two deploys, both clean.
- Ran three live probes: `UEAR` no-op, `UEAR` with `MaxOrdRate=2500`, `UPT`
  position transfer (both confirm steps).

## What we learned

- **Entitlement is PER-MsgType, not all-or-nothing.** This is the session's
  central finding and it overturns a conclusion recorded in `tags.go` since July.
  `UEAR` ✅ and `UPT` ✅ are live; `UAAR` ❌ and `UEPR` ❌ are silent. Two account
  messages, one works. Two position messages, one works.
- **Per-account risk config is writable over FIX.** `MaxOrdRate` 100 → 2500
  accepted on `5120866205` in 13ms. The order-rate ceiling was assumed to need a
  tZERO-side config request; it doesn't.
- **Inventory seeding is unblocked** via `UPT`, despite `UEPR` being dead.
- **Therefore `MMType` is off the v1 critical path.** It was only ever the
  workaround for a no-inventory world (Reg SHO locate exemption to make offers by
  shorting against the 1,000-share reserve). Which is fortunate: the spec
  enumerates **no values** for `MMType`, unlike every other coded field.
- **`UAAR` and `UEAR` share one field table** (only `9251 AccMPID` is Add-only),
  so anything settable at creation is settable on an existing account.
- **The REST create timeout is a real bug on our side.** `read=30.0` in
  `services/tzero.py` is shorter than tZERO's create latency, so the first create
  on any email times out and the account is orphaned — id never received. Then
  every retry on that email returns a fast `500 ACCOUNT_CREATION_FAILED`.
  Confirmed by `nova@novosapien.ai`, whose only prior interaction was one timeout.
- `UAU` is deprecated ("Fading, being replaced by `UAARa`"), so its absence at
  logon was never good evidence of anything.
- `UBT` needs `BankIDN` from a `UABR` first — an undocumented dependency in our
  planning.

## What went wrong / got stuck

- **We created two orphan tZERO accounts** — `hasan.ahmed+mm@novosapien.ai` and
  `nova@novosapien.ai` — whose ids we never received. Only tZERO can return them.
  Root cause: the 30s read timeout, compounded by `transactionId` being generated
  inside `build_individual_payload` and surfacing only on the success path, so a
  timeout leaves no correlation id.
- **Chased two wrong hypotheses before the right one.** First that a synthetic
  identity ("Market Maker", DOB 2000-01-01) was failing CIP — disproved by three
  existing accounts carrying placeholder DOB `1990-01-01`. Then that plus-address
  normalisation was colliding `+mm@` with the base account — disproved by `nova@`
  behaving identically. The timeout pattern was visible in the timings from the
  start.
- **Probably double-seeded George's position.** `UPT` is a non-idempotent signed
  delta; the `ConfirmTyp=1` and `ConfirmTyp=2` sends carried different ClOrdIDs,
  so they were likely two transfers, not two steps. Most likely 2 shares of
  IPTCCOWB at $2.00, not 1. Unverifiable — no position read-back exists.
- **`MMType(9289)` was being treated as settled since 22-07** on the strength of
  one summary line citing a document nobody held. The tag number turned out
  correct, but the provenance was a single unverifiable citation and it had no
  `parameters.md` row, against the working guide's own rule.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **Entitlement is per-MsgType.** `UEAR` + `UPT` live; `UAAR` + `UEPR` silent.
- ✅ **A regular `INDIVIDUAL` account is sufficient for the MM in v1** —
  configured via `UEAR`, seeded via `UPT`. No `MMType`, no `UAAR`, no
  non-INDIVIDUAL account type on the critical path.
- ✅ **`MaxOrdRate` is self-service.** The MM's 1,700 msg/s requirement is not
  blocked on a venue ask.
- ✅ **Do not write `MMType` on a guess.** No enumerated values, no read-back, and
  it plausibly gates a Reg SHO exemption. Wired in the gateway but unexercised.
- ✅ **`35=F`/`35=G` is now the sole remaining blocker** to a running MM — a build
  we own, not a permission we wait for.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **T1 partially closed** — the mechanism question is answered empirically.
  Remaining: enable `UAAR`/`UEPR`, and return the two orphan account ids.
- **T2 substantially closed** — `MaxOrdRate` is writable by us. The residual
  question is what sustained rate tZERO will *authorise*, vs what they'll accept.
- **Opened: `MMType` value list.** One narrow question for Rob (unavailable
  today). Not blocking.
- **Opened: REST create timeout + lost transactionId.** Two small PRs on the
  broker.
- **Opened: `UPT` idempotency discipline.** A retry after a timeout silently
  double-seeds. The MM build needs a ClOrdID ledger or reconciliation.
- **Opened: does `Stop Wash Trades` (8985) conflict with N12?** N12 accepts a
  momentary self-cross on re-quote; the IPLY default rejects it. Now settable via
  `UEAR`, so it's a decision rather than a constraint.

## Next

- Reverse or keep George's IPTCCOWB position — if reversing, send the **exact
  mirror** (`-1` at ConfirmTyp=1, then `-1` at ConfirmTyp=2), never a single `-2`.
- Then: the George → market-maker conversion runbook (drafted this session).
- Ask Rob for the two orphan account ids, `MMType` values, and `UAAR`/`UEPR`
  entitlement.
- Branch + PR both repos — gateway and vault changes are uncommitted.
- `35=F`/`35=G` is the build that matters. Everything else is now configuration.
