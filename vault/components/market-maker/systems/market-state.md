# Market State

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/CTS-002-market-operations-standard|CTS-002]] · guide: [[standards/CTS-002-plain-english-guide]]
> **Status:** Shape known — classifier logic and profile tables ours to design
> **One-liner:** Publishes the Reference Price, decides whether the market can operate normally, and selects the target market shape for the current session. Edwin's term for this whole layer: **"market state."**

---

## Purpose

The layer between valuation and quoting. Three jobs:

1. **Publish the Reference Price** — the ESV, republished unchanged as the
   anchor the quoting engine builds around.
2. **Classify operating condition** — can we operate normally right now?
   (feeds alive, valuation flowing, systems healthy)
3. **Select the operating profile** — given condition + session, how tight,
   deep, and fast should the market look?

## Reference Price Publication

`RP = ESV`, always — an identity **by law**, not a calculation. The layer adds
no math; it adds *publication management*:

- **Gating** — RP only visible in the right lifecycle states (not pre-IPO;
  informational during IPO; live from pre-market).
- **Stamping** — valuation + publication timestamps, states, version →
  every published price reconstructible.
- **Failure handling** — valuation stops → **Protected Reference Price
  State**: last valid RP stands, frozen. No subsystem may invent a substitute.
  This is the mid-game feed-outage answer: the quoting engine keeps quoting
  around the frozen price, wide and defensive, until valuation resumes.
- **The trust boundary** — writing `RP = ESV` down as law forbids anyone
  downstream from "adjusting" the price on the way through.

Edwin confirmed the RP is **the mid** between best bid and best ask. (Source:
standup 2026-07-20)

## Operating Condition (the classifier)

`condition = F(valuation availability, feed health/latency, system health, lifecycle states)`

Classes: **Normal · Degraded · Protective · Recovery · Emergency**. The source
doc famously says "Do NOT define F" — the classifier is deliberately ours.
Expect threshold rules (e.g. probability feed stale > N sec → Degraded).
Mostly "Normal" in practice.

## Operating Profile (the shape)

`profile = G(RP, condition, session, config)` → target spread, displayed
liquidity, depth, refresh, protection level.

> **I/O direction (clarified 21-07):** condition + session are the profile's
> *inputs*; the spread/depth/refresh targets are its *outputs*. Those outputs
> then become the quoting engine's inputs — a pipeline, one layer's outputs
> feeding the next.

The two standards carry mismatched profile menus (CTS-002:
Stable/Active/Balanced/Defensive/Recovery/Emergency; PTS-001:
Stable/Active/Defensive/Recovery/Liquidity-Preservation/Protective). **One
merged profile table** will exist in the build — see
[[market-maker/parameters]]. Starting mapping proposal: Normal→Stable/Active ·
Degraded→Defensive · Recovery→Recovery · Emergency→Protective.

## Sessions (the season rhythm)

Three liquidity sessions with different profiles (Source: standup 2026-07-20):

| Session | Behaviour |
|---|---|
| **In-game** | Tight, fast — calls ~every 200ms ("a second's too long", 23-07) |
| **Around-game** | Intermediate — pre-game build-up, post-game wind-down |
| **Overnight / between games** | Deliberately wide (~$2.5–5 spreads), slow — non-live calls every 30–60s (23-07) |
| **Earnings window** (Tue NFL / Wed NCAA) | Burst: call all ~170 symbols for ~5 minutes around the 7:30 release (23-07) |

Driven by the fixture schedule + Sport Radar official event status, per game
(the Cowboys can be in-game while the Packers are overnight). Underneath sits
the season lifecycle: IPO → open market → weekly loop (pre-game → live →
post-game → weekly report ×18) → final report → settlement.

## Interfaces

- **In:** ESV stream ([[market-maker/systems/valuation-engine]]), feed-health
  signals, fixture schedule, event status.
- **Out:** published RP + condition + active profile + session → the quoting
  engine ([[market-maker/systems/quoting-engine]]); RP also feeds the app's
  price display via the existing market-data path.

## Open Items

Tracked in [[market-maker/open-questions]]: classifier thresholds, merged
profile table values, session boundary definitions (esp. NCAA's 6-day weeks),
Weekly Financial Report ownership.
