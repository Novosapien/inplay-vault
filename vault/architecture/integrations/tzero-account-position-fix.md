---
description: "Distillation of the tZERO Account & Position FIX spec v3 — the message families, tags and risk toggles behind MM account, inventory and cash mechanics"
---

# tZERO Account & Position FIX Spec (v3)

> **Integration:** [[t0]] · [[integrations]]
> **Source:** `tZERO_FIX_AccountPosition_20251015.pdf`, Version 3, prepared March 2026.
> Held at `sources/tZERO_FIX_AccountPosition_20251015.pdf` (beside this doc).
> **Status:** Primary source. This doc is a distillation — the PDF is authoritative.
> **Confidentiality:** tZERO proprietary. Do not redistribute outside the team.

---

## Why this doc exists

Until 2026-08-05 this spec was cited in `trading-architecture.md` §2 but **not held
anywhere in the repo**. Every downstream claim about MM account mechanics —
`MMType`, `UAAR`/`UEAR`, `UEPR` inventory seeding, `UBT` cash, the risk suite —
traced back to a single summary line citing a document nobody could open. The PDF
is now in `sources/`. Read it before building anything against these messages.

## Message families

| Family | Input | Accepted | Rejected |
|---|---|---|---|
| Add Account | `UAAR` | `UAARa` | `UAARx` |
| Edit Account | `UEAR` | `UEARa` | `UEARx` |
| Delete Account | `UDAR` | `UDARa` | `UDARx` |
| Edit Account PII | `UEAP` | `UEAPa` | `UEAPx` |
| Edit TIN | `UETR` | `UETRa` | `UETRx` |
| Add Bank | `UABR` | `UABRa` | `UABRx` |
| Edit Bank | `UEBR` | `UEBRa` | `UEBRx` |
| Edit Position | `UEPR` | `UEPRa` | `UEPRx` |
| Balance Transfer | `UBT` | `UBTa` | `UBTx` |
| Position Transfer | `UPT` | `UPTa` | `UPTx` |
| Account Update (output) | `UAU` | — | — |

Tag `58 Text` carries the rejection reason on every `…x` variant.

## The critical structural fact

**`UAAR` and `UEAR` share ONE field table.** The spec heads it "Add Account
Request (UAAR, UAARa, UAARx) **and** Edit Account Request (UEAR, UEARa, UEARx)".

Per-field requirements distinguish them, and only one field is Add-only:

| Tag | Field | Required on |
|---|---|---|
| `11` | ClOrdID | **UAAR or UEAR** |
| `1` | Account | **UAAR or UEAR** |
| `9251` | AccMPID | **UAAR** only |

Every other field in the table — including `MMType` and the entire risk suite —
carries no message qualifier, so it applies to **both**. Anything settable at
creation is therefore also settable on an existing account via `UEAR`.

This matters because, as of 2026-08-05, `UEAR` is the one account-management
message proven live on our session (see [[tzero-oms-entitlement-probes]]).

## Account fields (UAAR / UEAR)

| Tag | Field | Notes |
|---|---|---|
| `15` | Currency | USD |
| `9251` | AccMPID | Required on UAAR |
| `9252` | AccOBO | Account On-Behalf-Of |
| `9255` | CASHo | Initial cash balance |
| `9253` | DTBPo | Initial day-trading buying power |
| `9270` | DTMult | Day-trading margin multiple |
| `9271` | RlsCoveredDTBP | 0=false, 1=true |
| `9272` | ReqText | Free text on a request |
| `9273` | AccNAME | Account name |
| `9274` | AccCFRM | Clearing firm |
| `9275` | AccBRNCH | Branch |
| `9276` | AccRep | Rep code |
| `9277` | RmtAccno` | Remote account number |
| `9278` / `9279` | SrcaccOvrd / DstaccOvrd | Source / destination account override |

### Risk-management fields

| Tag | Field | Notes |
|---|---|---|
| `9282` | AccStreetCapcty | Street capacity code — **values not enumerated in spec** |
| `9283` | AccType | Account type code — **values not enumerated** |
| `9284` | DTCNumb | DTC number |
| `9285` | AccIMID | Account IMID |
| `9286` | ClientID | |
| `9287` | CRDNumb | |
| `9288` | MemberType | Member type code — **values not enumerated** |
| **`9289`** | **MMType** | **MM Type — values NOT enumerated in the spec** |
| `9267` | RegStat | RDA / RSA / RDN / RSN / RAA / RAN |
| `9290` | MaxOpenOrds | Maximum open orders |
| `9291` | MaxOpenPos | Maximum open positions |
| `9292` | MaxPosSize | Maximum position size |
| `9293`–`9298` | MaxQtyAbs, MaxCostAbs, MaxQtyExt, MaxCostExt, MaxLossAcc, MaxLossPos | |
| `8900`–`8904` | PrctDTBP, PrctLossAcc, PrctLossPos, TotEquity, PrctEquity | |
| `8908`–`8912` | Spoofing + layering controls | |
| `8913`–`8917` | ADV limits | |
| `8926`–`8933` | Limit percentage, core + pre/post session tiers [0..3] |
| `8934` | LmtCents | Max limit price range in cents |
| **`8935`** | **MaxOrdRate** | **Maximum order rate — the IPLY default is 100/sec** |
| `8936` | MaxDupOrdRate | Max duplicate order rate — IPLY default 20/sec |

### Risk-management option toggles (`0=false, 1=true`)

`8940`–`8998`. The ones that matter here:

| Tag | Field |
|---|---|
| `8942` | Rmo_IsMarginAcc |
| `8943` | Rmo_EnforceDTBP |
| `8961` | Rmo_ShortListLookup |
| `8969` / `8970` / `8971` | Rmo_MaxOpenOrds / MaxOpenPos / MaxPosSize |
| `8982` | Rmo_PreventSpoofing |
| **`8985`** | **Rmo_StopWashTrades** |
| `8995` / `8996` | Rmo_LmtPerc / Rmo_LmtCents |
| **`8997`** | **Rmo_EnforceMaxOrdRate** |
| `8998` | Rmo_EnforceMaxDupOrdRate |

A limit value (e.g. `8935`) is only enforced when its `Rmo_` toggle is on. Per
[[tzero-oms-risk-settings]], `Max Order Rate` is already ON for IPLY at 100/sec,
so writing `8935` should take effect without also flipping `8997`.

## Position messages

### `UEPR` — Edit Position Request

Sets a position's **opening** state. Absolute values, so a retry is safe.

| Tag | Field | Notes |
|---|---|---|
| `1` | Account | Required |
| `15` | Currency | USD |
| `55` | Symbol | Identifies the position object |
| `9381` | Qto | Initial quantity |
| `9382` | Eto | Initial cost basis |
| `9388` | SecTyp | `EQT` equity · `OPT` option · `DAS` digital asset · `DES` digitally enhanced |

Returned on `UEPRa`: `9383 Qt`, `9384 Et`, `9385 Rpnl`, `9389 Upnl`.

### `UPT` — Position Transfer

**A second, distinct inventory mechanism.** Takes signed deltas rather than
`UEPR`'s absolute opening values.

| Tag | Field | Notes |
|---|---|---|
| `9386` | TxfrQty | Signed. Positive = deposit, negative = withdrawal. Non-zero, required |
| `9387` | TxfrCost | Must share TxfrQty's sign. `(TxfrCost / TxfrQty) = averagePrx > 0.00` |
| `9551` | ConfirmTyp | 1=Administrator confirm (first step) · 2=Agent confirm (final step) |

Because `UPT` is a separate MsgType from `UEPR`, it may carry separate
entitlement — worth probing independently if `UEPR` stays silent.

## `UBT` — Balance Transfer (cash)

| Tag | Field | Notes |
|---|---|---|
| `9262` | TxfrAmnt | Signed. Positive = deposit, negative = withdrawal. **Non-zero, required** |
| `9263` | TnxFee | Negative fees are rebates/credits |
| `9550` | BalTxfrTyp | 1=ACH · 2=Wire Domestic · 3=Wire International |
| `9551` | ConfirmTyp | 0=Unconfirmed · 1=Margin confirmed · 2=Transfer confirmed · 3=Bank confirm pending · 4=Bank confirmed |
| `9501` | BankIDN | **Required. Only returned by a `UABRa`** |

**Dependency worth flagging:** `UBT` requires `BankIDN`, which comes from an
`Add Bank account Request` (`UABR`). So funding an account over FIX needs a bank
profile registered first — a prerequisite not previously logged anywhere.

Withdrawals debit immediately and are rejected (`UBTx`) if funds are unavailable.
Deposits are **not** credited until bank-confirmed (`9551=3`).

## `UAU` — Account Update

The spec marks this **"Fading (being replaced by `UAARa`)"**.

Carries `9267 RegStat`, `9251 AccMPID`, `9255 CASHo`, `9253 DTBPo`, `9258 CASH`,
`9256 DTBP`, `9259 RPNL`, `9260 TotalDebit`, `9261 LivOrdDebit`, `12 Commission`,
`9265 DateCreated`, and `9266 UpdateTyp` (`RFR` initial session refresh, once ·
`NEW` · `EDT` · `TRD`), which the spec says is "for diagnostic purposes only".

**Consequence:** the absence of `UAU` at logon was previously read as evidence
that the account-management plane is disabled on our session. That inference is
weak — `UAU` is being retired regardless.

## PII / TIN / bank, in brief

- `UEAP` — `9302 PiiAccTyp`: 1=Individual · 2=Joint · 3=LLC · 4=Corporation ·
  5=Partnership · 6=Trust. Also `9304 BrkAccStat` (1=Active, 2=Disabled),
  `9309 AccLegalNam`, `9310 Accreditation`, `9312 NumInvestors`.
- `UETR` — `9315 TinRole`: 1=Primary (one per account) · 2=Joint · 3=Beneficiary ·
  4=BeneficialOwner · 5=Entity. `9327 TinTyp`: 1=SSN · 2=EIN. `9326 TIN` is a
  9-digit integer. `9369 KycStatus`: 1=Pending · 2=Approved · 3=Declined.
  `9394 HasPlaceholdr` flags a placeholder TIN.
  Entity-only fields `9371`–`9379` (CompanyNam, CntryCodForm, StateForm,
  DateForm, InstitType, …) apply when `TinRole == ROLE_Entity`.
- `UABR`/`UEBR` — `9501` BankIDN through `9528` ReferenceId.

**`PiiAccTyp` (9302) and `TinRole=5 (Entity)` are the entity-account route.** They
are the concrete alternative to an INDIVIDUAL account for a house/firm market
maker — separate from, and possibly complementary to, `MMType`.

## Open against this spec

1. **`MMType` values are undefined here.** The spec enumerates values wherever it
   knows them (`RegStat`, `PiiAccTyp`, `TinRole`, `TinTyp`, `KycStatus`,
   `SecTyp`, `BalTxfrTyp`). `MMType`, `AccType`, `AccStreetCapcty` and
   `MemberType` have bare descriptions. Ask tZERO. → T-item.
2. **Entitlement is per-MsgType on our session,** not all-or-nothing. See
   [[tzero-oms-entitlement-probes]].
3. **How REST-onboarded account ids map to OMS `AccNUMB`** is still open (T1).
   Empirically the 10-digit REST id works as Tag 1 on orders.
