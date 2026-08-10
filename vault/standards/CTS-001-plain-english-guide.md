---
description: "Plain-English companion to CTS-001 — the ESV valuation system explained, plus Edwin's actual formula from the 20-07 call and the season-1 build reality"
---

# CTS-001 in Plain English — The Valuation System (what a team is worth)

> **Companion to:** [[standards/CTS-001-financial-valuation-standard]] (the authoritative source)
> **Audience:** Someone with no finance background who needs to understand — and now build — this system.
> **Status:** Derived explainer. Where this guide and the source document disagree, the source wins — **except** where the [20-07 touchdown](#7-what-edwin-actually-told-us-20-07-2026) supersedes the source (Edwin's spoken word beats the generated doc).
> **Scope note (20-07):** George asked Edwin directly whether we build CTS-001/002 or consume them from tZERO. Edwin: **"We will build them."** This is a Novosapien build.
> **See also:** [Quirks & open questions](#8-quirks-and-open-questions) — including the fact that the actual valuation math (Section 3) is missing from the vault copy.

---

## The 30-second version

Every team in the challenge has a stock. Before anyone can trade it, something has to answer one question, continuously, all season:

> **"What is one share of the Chicago Bears worth right now?"**

CTS-001 is the spec for the system that answers it. The answer is called the **Expected Settlement Value (ESV)** — the system's best estimate of what a share will actually pay out when the season ends and the company is wound up. It gets re-estimated every time something relevant happens: a touchdown, an interception, a result elsewhere shifting the season outlook.

The single most important idea in the document:

> **Value and price are different things, produced by different systems, and neither is allowed to influence the other.**

- **ESV (value)** = what the valuation system calculates a share is *worth*, from win probabilities and revenue economics. Calm, mechanical, explainable.
- **Market price** = whatever buyers and sellers actually trade at on the order book. Emotional, herd-driven, discovered by the crowd.

The market maker (PTS-001) takes the ESV — republished as the **Reference Price** — and builds its bid/offer quotes around it. Users then trade wherever they like. If the crowd trades the Bears way above their ESV, that's the market's business; the valuation system never budges because of it.

---

## 1. Valuation basics (skip if you know this)

Think of a **house sale**:

- A surveyor values the house at £300k based on fundamentals — size, location, condition. That's the **ESV**: a model-driven estimate of worth.
- The house actually sells for £340k because two buyers got into a bidding war. That's the **market price**: what someone actually paid.
- The surveyor doesn't revise the valuation to £340k because of the bidding war. Fundamentals didn't change; sentiment did.

CTS-001 builds a surveyor, not an auctioneer. Vocabulary:

| Term | Plain meaning |
|---|---|
| **Team Company** | A real company created for one team (Bears Inc.). It owns the team's revenue rights and issues the stock. |
| **Defined Event** | The competition period the company exists for — here, the NFL / NCAA football regular season. |
| **Contractual Economic Rights** | The revenue streams the Team Company legally owns — performance money, commercial money, minus expenses. The *only* things that create value. |
| **InPlay Security** | One share of a Team Company. Non-voting. Owning it = owning a slice of those revenue rights. |
| **ESV — Expected Settlement Value** | The continuously updated estimate of what one share pays out at season end. The system's entire output. |
| **Initial Valuation** | The first ESV, set at IPO. Everything after is an update to it. |
| **Reference Price** | The ESV, republished as the operational price anchor the market maker quotes around (formally a CTS-002 job — in our build, the same pipe). |
| **Economic Component** | The standardized representation of one revenue right — the objects the math actually runs on. |
| **IVS — InPlay Valuation System** | The engine that computes ESV. The thing this document specifies. What we are building. |
| **Approved Valuation Input** | A data source explicitly allowed to move the ESV (e.g. win probabilities). Anything not on the list may not touch value. |
| **Valuation Lineage** | The complete audit trail: every ESV from IPO to settlement, reconstructible. |
| **Settlement** | Season ends → the company's actual earnings are known → each share pays out its real value → ESV and reality converge. |

---

## 2. Where CTS-001 sits — the three-document stack

| Document | Role | One-liner |
|---|---|---|
| **CTS-001** — this document | What is a team worth? | Produces the **ESV** — the fair-value anchor everything else orbits. |
| **CTS-002** — Market Operations | How do markets run? | Publishes the ESV as the **Reference Price**, tracks market health, defines the rules of engagement. |
| **PTS-001** — the SDMM | How does the market maker behave? | Builds tradable bid/offer ladders *around* the Reference Price. |

CTS-001 is the top of the hierarchy: if any document conflicts with it, CTS-001 wins. It feeds everything and consumes nothing from downstream — by law, no market data may flow back up into valuation.

---

## 3. The golden rules (the "Constitutional Laws," §1B)

Ten laws, distilled to what they mean in practice:

1. **Only contractual value counts.** ESV = the value of the revenue rights the company actually owns. No vibes, no brand premium, no discretionary bumps.
2. **Information-driven, not clock-driven.** ESV updates when something *material* happens, not on a timer. A touchdown → recompute now. Nothing happening → nothing to recompute. (In a live game this effectively means per-play.)
3. **Independent of market price.** The order book, spreads, volume, sentiment, the market maker's inventory — none of it may move the ESV. Ever. This is the load-bearing wall of the whole architecture.
4. **Deterministic.** Same inputs + same methodology + same version = same ESV, on any machine, in any language, at any time. No true randomness, no wall clocks.
5. **Complete lineage.** Every ESV must be reconstructible from the Initial Valuation plus every update since. No orphan numbers.
6. **Everything counted exactly once.** Every revenue right appears in the valuation once — nothing omitted, nothing double-counted.
7. **Fully explainable.** Any ESV can be decomposed into its parts: *this much* from today's game, *this much* from the rest of the season, *this much* off-field. No hidden weights or opaque heuristics.
8. **Valuation and price discovery never redefine each other.** The IVS values; the market prices; separate jobs forever.
9. **Same math everywhere.** Simulation, education, production — operating environments may differ in rules, never in valuation methodology.
10. **Integrity is conformance.** An ESV that isn't correct, consistent, deterministic, reconciled, reproducible, auditable *and* explainable is nonconforming. (See [§7](#7-what-edwin-actually-told-us-20-07-2026) for how hard to hold this bar in season 1.)

---

## 4. The financial hierarchy — where value comes from

The document's core structure, §2.3, is a strict one-way chain:

```
Team Company                (the legal entity — owns everything)
   ↓ owns
Contractual Economic Rights (the revenue streams)
   ↓ backs
InPlay Security             (the share — a proportional slice)
   ↓ valued as
Expected Settlement Value   (what the slice is worth right now)
   ↓ anchors
Secondary Market Price      (what people actually trade it at)
```

Each level derives **only** from the level above. The chain never runs backwards — that's rule 3 again, structurally. A share is worth a slice of the company's revenues; the company's revenues come from the season; the market price is downstream of all of it and feeds back into none of it.

Worth internalizing: **shareholders own the company, not the revenue streams directly.** The share's value routes through the company — which is why every share of the same team has exactly one ESV.

---

## 5. Economic Components — how rights become math

The doc's Section 2 builds a representation layer between legal documents and equations:

- Every revenue right gets exactly **one Economic Component** — a standardized object the math can run on. One right ↔ one component, always.
- Components come in **four classes**: **Performance** (on-field results money), **Commercial** (sponsorship/deal money), **Revenue Allocation** (league/pool distributions), **Expense** (contractual deductions — the only negative class).
- Each component has two halves: a **structural identity** that never changes (what right is this? where did it come from?) and an **economic value** that changes constantly (what's it worth right now?).
- A registry (the **ECR**) tracks every component's identity, origin and lifecycle: *Registered → Active → Continuously Re-estimated → Settled → Archived*.
- **ESV = the aggregation of all component values for that team.** The equations only ever touch components — never legal documents, never the company itself.

Why the ceremony? It's what makes rules 5–7 (lineage, completeness, explainability) mechanically possible: if every value lives in a registered component, then every ESV is auditable by construction.

**The build reality (20-07):** for the challenge, this collapses to roughly **three components per team** — today's-game revenue, rest-of-season revenue, off-field revenue. Keep the structure (it's genuinely useful for explainability); skip the bureaucracy.

---

## 6. What the document does NOT contain — the missing math

The vault copy of CTS-001 ends at §2.33. **Section 3 — "the mathematical valuation of those Economic Components" — is referenced throughout and absent.** The document defines *what* gets valued and *under what laws*, but not *how*: no probability methodology, no aggregation formula, no worked example.

This gap is now mostly filled by Edwin directly (next section), but request the Section 3 PDF anyway — if it exists, it may contain constraints or details the call didn't cover.

---

## 7. What Edwin actually told us (20-07-2026)

The touchdown call reframed this document substantially. Edwin: the standards were *"meant for Claude to read… they're fairly simple."* Translation: the doc is generated context, not carved-in-stone law — the real spec is the model below.

**The actual valuation formula:**

```
share price = on-field + off-field

on-field  = P(win THIS game) × $/win          ← live win probability, this game
          + E[wins, rest of season] × $/win    ← expected remaining wins, all other games

off-field = marketing / advertising revenue component
```

- **$/win** is the revenue value of a win (the vision doc's example: 5 expected wins × $5 = $25/share at IPO).
- **P(win)** comes from **Sport Radar's live win probabilities** — backed by ~20 years of historical data. This is our Approved Valuation Input. (Currently broken: the probabilities API is returning 403s and only 8 of 32 NFL win totals — being chased.)
- **Off-field is deliberately interpretive** — "it's not guaranteed every game… that makes the market really really dynamic for trading." The uncertainty is a feature: it's what gives traders something to disagree about.
- **During a live game, ESV moves per play** — touchdown up, turnover down. That cadence *is* the product.

**Other confirmations that shape this build:**

- **Markets are truly isolated.** The Cowboys' valuation never affects the Bears' intragame. Each game is effectively a *pairs trade* — two correlated symbols whose win probabilities are complementary. Between games, results do flow into next week's expectations.
- **Rankings don't price in.** No goal-difference-style effects; earnings link to wins and off-field revenue only (playoffs are out of scope).
- **Edwin has done this before.** His previous simulations ran on a trigger script that Kevin reckons still exists. Find it — it's the calibration starting point, not a blank page.
- **Event weighting is subjective and learnable.** A touchdown's price impact depends on context (score, quarter, down). Start with a guess per trigger type, then calibrate against how the market actually responds. Expect the first weeks to be volatile while it learns.

**What this means for the golden rules:** the architecture stands (determinism, lineage, explainability are all still right — and cheap if built in from day one), but hold the *ceremony* lightly. Get Edwin's explicit sign-off on the season-1 conformance bar at the Thursday session.

---

## 8. Quirks and open questions

**In the source document:**
- **Section 3 (the math) is missing** from the vault copy — the file ends at §2.33. Request it; Edwin's spoken formula fills most of the gap but may not be all of it.
- **Who publishes the Reference Price** is ambiguous between CTS-001 and CTS-002 (each seems to point at the other). Irrelevant in practice — we build both — but the ESV→RP pipe needs a concrete design (push cadence? bus topic? per-play?).
- The **"Board-approved," trade-secret, formal-approval framing** throughout reads as aspirational corporate scaffolding for a company of six. Treat as context, not process to implement.

**Genuinely open (for Thursday / tZERO calls):**
1. **$/win — the actual number(s)**, and whether it differs NFL vs NCAA.
2. **The off-field revenue model** — what moves it, how often, who supplies the number.
3. **IPO Initial Valuations** — who computes the opening ESV per team, from what (preseason win totals?).
4. **Sport Radar probabilities feed** — fix the 403s/partial data; formalize it as the Approved Valuation Input; define fallback behavior if the feed dies mid-game (CTS-002's Protected Reference Price State says: freeze the last valid price, never invent one).
5. **Settlement mechanics** — how ESV converges to the final payout at season end, and who declares the final numbers (ties into the Weekly Financial Report question in CTS-002).
6. **Edwin's old trigger script** — locate it.

---

## 9. TL;DR mental model

A deterministic surveyor with a live feed:

- **One number per team, always:** ESV = P(win today)×$/win + expected remaining wins×$/win + off-field.
- **Inputs:** Sport Radar win probabilities + the revenue model. Nothing else — *especially* not the market.
- **Cadence:** event-driven; per-play during games.
- **Never:** looks at market prices, invents value, forgets anything (full lineage), or produces two different answers from the same inputs.
- **Output:** flows to the market maker as the Reference Price — the anchor the whole tradable market is built around.
- **Held lightly:** the doc's ceremony compresses to a small, explainable, replayable pricing service. The laws worth keeping are independence, determinism, and explainability.
