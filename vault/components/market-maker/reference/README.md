# Market Maker — Reference Material from InPlay

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Edwin's own code and data, as supplied, plus what we found on
> reading it. These are **reference implementations, not our build** — nothing
> here runs in `inplay-market-maker`. Where they and the spec disagree, see the
> discrepancies below before assuming either is right.

**Arrived:** 28-07-2026, with Edwin's answers to the six questions
([[standards/MM-edwin-answers-28-07|rendered email]]).

---

## What's here

| Path | What it is |
|---|---|
| `ipo-seeding-runbook.md` | **How the IPO offering is seeded and rested at tZERO** — the two access paths, the four phases, and every trap the 19-08 run found the hard way. Ours, not Edwin's |
| `position-transfer-ledger.md` | Every position transfer ever sent to the venue. The endpoint is one-way, so this is the only complete record |
| `inplay-reference-feed/` | The complete engine as running code — win-total maths, double-count-safe pricing, the college ratings feed, the IPO formula. Stdlib only. **31 tests, all pass.** |
| `inplay-reference-feed/README-edwin.md` | Edwin's own map from each email item to each module |
| `ipo-engine-original.py` | The original IPO pricing computation (`engine.py` in the email). **Authoritative** where it and `inplay_feed/ipo.py` disagree |
| `sample_reference_feed_2026-08-29.json` | A valid sample of the daily feed, in the production schema |
| [[standards/IPO_Pricing_Subscription_Supplement_v1.3\|IPO Pricing & Subscription Supplement v1.3]] | Filed in `standards/` — it is normative, Supplement A to the build spec |

The module we are told we may reuse verbatim: `inplay_feed/feed.py`'s
`validate_records()`, so a bad file is caught on both ends of the pipe.

---

## Verified on arrival

- **31 tests pass** (Edwin's README says 25; the email says 31 — the email is right).
- **The worked example reproduces exactly.** Line 9.5, Over −125, Under +105
  → 9.7200 wins at σ 2.7, 9.6792 at σ 2.2. Both match the email to 4 dp.
- **The sample feed is well formed** — 170 records, 32 NFL + 138 NCAA, matching
  §2.5 exactly; `effective_time` 10:00:00Z = 06:00 ET as specified.

---

## Discrepancies found

Raised under Edwin's own invitation — *"send me anything that doesn't survive
contact with the code"*.

### 1. The tie leg differs between his two IPO implementations

| Source | Computation | Per share |
|---|---|---|
| `ipo-engine-original.py` | `P_TIE × E_TIES_NFL` = 2.50 × 0.08 | **$0.2000** |
| `inplay_feed/ipo.py` | `TIE × NFL_TIE_RATE × games` = 2.50 × 0.004 × 17 | **$0.1700** |

Three cents on every NFL name. The original treats 0.08 as expected ties *per
team per season*; the rebuild treats 0.004 as a *per-game rate* over 17 games,
giving 0.068. The email's "about 0.4% of games" matches the rebuild, the
original does not.

### 2. The rebuild feeds the wrong object into Bradley-Terry

`ipo-engine-original.py` compares **Popularity Index against Popularity Index**:

```python
capture(pop[t.team], pop[o])          # both are 0.6*brand + 0.4*perf
```

`inplay_feed/ipo.py` compares **Popularity Index against a raw Brand tier**:

```python
capture_share(pop_i, brands[opp])     # pop_i is blended, brands[opp] is not
```

Different scales. With two identical teams (brand 70, same form) the original
returns exactly 0.5000; the rebuild returns 0.4975. The in-code comment
describes the approximation as using "league-average Pop", which is not what
the line does.

### 3. The discount scaling is a different function

- **Original:** min-max normalises `contested_off_share` **within each league**,
  then maps to [1%, 3%]. A *relative rank* — the most contested name in a league
  always gets 3%, the least always 1%.
- **Rebuild:** `rate = 1% + 2% × contested_frac`, an absolute map with no
  normalisation.

`ipo.py` flags this itself (`VERIFY-BEFORE-FREEZE`) and predicts exactly this:
*"if it ranked or normalized differently, change this one line to match."* It
did. The supplement (§2.2) confirms the original: *"normalized contested
off-field EV share, per league"*.

### 4. League naming is inconsistent across the artefacts

`ipo-engine-original.py` uses `"NCAAF"`. `inplay_feed/feed.py` validates
`league in ("NFL", "NCAA")` and the sample feed uses `"NCAA"`. A naive join
across the two breaks.

### 5. The IPO acceptance test is not currently runnable

The email says: *"run the engine on the freeze snapshot and match its output;
there is nothing to reverse-engineer."* We cannot. `ipo-engine-original.py`
imports a `teams_config` module — `NFL_BRAND`, `NCAA_BRAND`, `NFL_DIVISIONS`,
`NCAA_CONF`, `OUT_OF_UNIVERSE_OVERRIDES`, `DEFAULT_OUT_OF_UNIVERSE` — and reads
`odds.csv`. **Neither is attached**, nor is `InPlay_IPO_Pricing.xlsx` (the
supplied `.docx` supplement is a different document). It also needs numpy,
pandas and scipy.

### 6. Everything is `float`

§1.6-3 makes decimal arithmetic authoritative and binary floats never
authoritative. So `TeamPricer` cannot be lifted verbatim as the email suggests
— it must be ported to `Decimal`. The formulas port cleanly; only the types
change.

### 7. The supplement is missing a section

`IPO_Pricing_Subscription_Supplement_v1.3.docx` runs 1–6 then 8. §5 refers to
*"see NDSU, Section 7"*, so §7 exists in the author's copy and is absent from
ours.

---

## Where these land against our open questions

| Item | Effect |
|---|---|
| **E19** | Answered. The daily feed supplies expected remaining wins for all 170 teams |
| **S10** | **Closable** — we no longer need Sportradar to carry NCAA win totals |
| **S6** | Answered — price the two-way market as proposed; a tie settles at 0.5 |
| **σ<sub>mkt</sub>** | Now a fixed constant: **2.7 NFL, 2.2 NCAA**. Replaces the unapproved 2.0–2.5 range |
| **Reference Float** | The supplement gives **500,000 shares per team** after Round 10 — the number §4.3 has been missing |
| **RP seeding** | The email decides **EV, not listed price**. The supplement (§8, Open Item 10) had it as OPEN and warns of the consequence |
| **§9.2 MM allocation** | ⚠ **Conflict.** The spec says `floor(0.85 × UnsoldShares)`; the supplement's MM Primary Mandate says the MM buys **all** remaining allotment in Rounds 1–10. Supplement Open Item 9 flags the reconciliation as unresolved |

---

## Dates that now bind us

From the supplement, §3.1 and §3.2:

| | |
|---|---|
| NCAA price freeze | **Wed 19 Aug 2026** |
| NCAA offering | **Sat 22 Aug – Fri 28 Aug 2026** |
| NFL price freeze | **Wed 2 Sep 2026** |
| NFL offering | **Sat 5 Sep 2026** |

The MM has a **Primary Mandate for Rounds 1–10** of every issue: it must buy
every share left after participant demand. Whether that is the quoting engine
or a platform-side account is not stated and needs settling — but if it is
ours, the first hard date is three and a half weeks away.
