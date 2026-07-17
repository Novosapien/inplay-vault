# PTS-001 in Plain English — The Simulated Market Maker (SDMM)

> **Companion to:** [[standards/PTS-001-simulated-designated-market-maker-standard]] (the authoritative source)
> **Audience:** Someone with no market-making background who needs to understand — and eventually build — this system.
> **Status:** Derived explainer. Where this guide and the source document disagree, the source wins.
> **See also:** [Quirks & open questions](#9-quirks-and-open-questions-in-the-source-document) — issues in the source doc worth raising with InPlay before implementation.

---

## The 30-second version

InPlay's simulation lets users trade "team stocks" (e.g. one stock per NFL team) with fake money. For that to work, there must always be someone on the other side of every trade — someone willing to sell when a user wants to buy, and buy when a user wants to sell.

**The SDMM (Simulated Designated Market Maker) is that someone.** It's a bot that, for every team stock, continuously publishes:

- a price it will **buy** at (the *bid*), and
- a price it will **sell** at (the *offer*),

plus several backup prices at worse levels (the *ladder*), each with a quantity attached.

PTS-001 is the engineering spec for that bot. Its two big obsessions are:

1. **Always be quoting.** The market must never go blank while trading is open.
2. **Be perfectly reproducible.** Given the same inputs, the bot must always do exactly the same thing, so any moment in market history can be replayed and audited.

Crucially, the SDMM **does not decide what a team is worth**. It receives a fair price from upstream (the *Reference Price*) and builds a tradable market *around* it.

---

## 1. Market-making basics (skip if you know this)

Think of a **currency exchange booth at an airport**:

- It shows two prices: "we buy dollars at 0.90, we sell dollars at 0.95."
- The gap between the two — the **spread** — is how the booth makes money.
- The booth doesn't predict where the dollar is going. It just keeps two prices up and earns the spread on traffic passing through.
- If too many people sell dollars to the booth, its till fills up with dollars (**inventory** builds). It reacts by lowering its buy rate (discouraging more sellers) and lowering its sell rate (encouraging buyers to take dollars off its hands).

That's a market maker. Now the vocabulary the spec uses:

| Term | Plain meaning |
|---|---|
| **Bid** | Price the SDMM will buy at. Users *sell* into the bid. |
| **Offer** (or ask) | Price the SDMM will sell at. Users *buy* from the offer. |
| **Spread** | Gap between best bid and best offer. |
| **Two-sided quote** | Having a live bid *and* offer at the same time. |
| **Order book** | The full list of live buy and sell prices with quantities. |
| **Depth / ladder** | Prices beyond the best one. Level 0 is the best bid/offer; level 1 is a bit worse; and so on. Lets big orders fill across several levels. |
| **Displayed quantity** | How many shares are shown at each price level. |
| **Tick** | The minimum price increment (e.g. $0.01). All prices must land on a tick. |
| **Inventory** | The net position the SDMM holds in a stock. Bought more than it sold → *long*. Sold more than it bought → *short*. Measured as a % of the publicly tradable float. |
| **Locked/crossed market** | Bid equals offer (locked) or bid is above offer (crossed). Nonsense states — banned. |
| **Issuer / Team Company** | One team's stock (the Chiefs, the Jets, …). |
| **Portfolio** | A league's worth of Team Companies with a shared pot of capital (e.g. NFL = 32, NCAA D1 football = 131). |

---

## 2. Where PTS-001 sits — the three-document stack

The standards form a hierarchy. The two CTS documents are "constitutional" — PTS-001 must obey them and can never override them.

| Document | Role | One-liner |
|---|---|---|
| **CTS-001** — Financial Valuation Standard | What is a team worth? | Produces the **Expected Settlement Value** and the **Reference Price** — the fair price everything anchors to. |
| **CTS-002** — Market Operations Standard | How do markets run? | Produces the **Market Operating Condition** (is the market open/halted/etc.) and the **Market Operations Profile** (the rules of engagement), and owns order matching. |
| **PTS-001** — this document | How does the market maker behave? | Consumes all of the above and builds the actual tradable order book. |

The spec calls the upstream outputs **constitutional market objects**. The single most repeated rule in the whole document:

> **The SDMM consumes constitutional objects. It never creates or modifies them.**

So the SDMM never invents a price, never decides the market should halt, never changes the trading rules. It takes those as given and does exactly one job: turn *"fair price is $25.00, market is open, normal conditions"* into a full, realistic, tradable order book.

---

## 3. The seven golden rules

Chapter 1 lays down principles that every later chapter enforces. Distilled:

1. **Continuous liquidity** — a live bid and offer must exist at all times while trading is authorized. No blank markets.
2. **Determinism** — same inputs → identical behavior, every time, on every conforming implementation. No wall clocks, no true randomness, no external data sneaking in.
3. **Inventory awareness** — the bot always knows its position and factors it into pricing.
4. **Inventory never silences the market** — even when it's uncomfortably long or short, it keeps quoting both sides. It manages inventory by *skewing prices*, never by going dark.
5. **Realism** — quotes should look and move like a real market (that's what the bounded randomization later is for).
6. **Replayability** — every quote, trade, and decision can be reconstructed after the fact, exactly.
7. **Isolation** — the bot uses *only* constitutional inputs plus approved configuration. No live sports feeds, no external prices.

Rule of thumb when rules conflict: **safety first, market presence second, profit last.** (Formally: Protection → Continuous Availability → Market Integrity → Inventory Stability → Market Quality → Performance.)

A note on "profit": the SDMM plays with simulation capital — fake money that can't be cashed out (Chapter 2). It still *tries* to be a profitable market maker (capture spread, manage inventory well) because that's what makes its behavior realistic and educational. Profit is a realism target, not actual revenue.

---

## 4. The big loop — the Decision Cycle

The SDMM is a loop, not a stream of ad-hoc reactions. Each iteration is a **Decision Cycle**:

**Something happens** → run every engine in a fixed order → validate → **publish a new order book** → commit the records → wait for the next trigger.

Triggers for a new cycle include (Ch 10.2.1):

- a new Reference Price arrives;
- a user order executes (fully or partially);
- the market state, inventory profile, pricing profile, portfolio allocation, or protection state changes;
- CTS-002 changes the operating condition or operations profile;
- a maximum cycle duration expires (heartbeat).

Rules of the loop:

- Cycles never overlap — one must fully complete (or be terminated) before the next starts.
- Multiple triggers arriving mid-cycle get batched into the next cycle.
- Once a cycle **commits**, nothing it produced can ever be modified. History is append-only — that's what makes replay possible.
- Everything downstream is stamped with the cycle it belongs to: one order book, one decision trail, one cycle.

---

## 5. The pipeline — what actually happens inside one cycle

The document is organised as a chain of "engines," each consuming the previous one's outputs (read-only — no engine may reach back and tweak an earlier stage). In build terms these are pipeline stages, not necessarily separate services.

```
constitutional inputs (Reference Price, market condition, profile)
        │
        ▼
[1] Market Objective Engine ......... what are we trying to do right now?
        ▼
[2] Portfolio Allocation Engine ..... split the league budget across teams
        ▼
[3] Issuer Market Making Engine ..... per team: compute prices, ladder, sizes
        ▼
[4] Market Adaptation Engine ........ pick the behavioral mode / react to change
        ▼
[5] Quote Construction Engine ....... assemble + final safety checks
        ▼
    PUBLISH the Executable Order Book
        ▼
[6] Quote Lifecycle Engine .......... babysit live quotes (age, refill, cancel)
        ▼
[7] Verification & Replay ........... record everything for reconstruction
```

*(The source document's own architecture diagram in §1.7 uses different engine names than its chapters — see [Quirks](#9-quirks-and-open-questions-in-the-source-document). The list above follows the chapters, which are the substantive definitions.)*

### 5.1 Market Objective Engine (Ch 4) — "read the room"

Before touching prices, the bot assesses the environment: how fast are orders arriving, how quickly are quotes getting eaten, what's our inventory, are any protections tripped, what phase is the external market in.

From that it produces four decisions that steer everything downstream:

- **Effective Market State** — its classification of current conditions;
- **Inventory Risk Profile** — how much position risk is tolerable right now;
- **Liquidity Budget** — how much liquidity we're willing to put on the table;
- **Pricing Profile** — which pricing "personality" to use (see §6 below).

### 5.2 Portfolio Allocation Engine (Ch 5) — "divide the pot"

One league = one Portfolio = one capital pool. Each cycle, this engine splits the **Portfolio Liquidity Budget** across all active teams:

- Every team gets exactly one **Issuer Liquidity Budget**: `ILB_i = PLB × A_i`, where the allocation weights `A_i` sum to exactly 1 — the pot is fully allocated, never over- or under-spent.
- Each team's budget is further split into a **bid-side** and **offer-side** budget (they need not be equal — a team the bot is long in might get more offer-side budget to help it sell down).
- Hot, active markets can be weighted more; quiet ones less.
- Hard constraints: total allocations ≤ portfolio budget ≤ portfolio capital; no team over its individual cap; nothing crosses portfolios (NFL money never funds NCAA quoting).
- Team-level engines must live inside their allocation — they can't borrow, resize, or trade budgets.

### 5.3 Issuer Market Making Engine (Ch 6) — "build one team's market"

The heart of the spec. Runs independently per team, in a strict 11-step sequence. The essential flow:

**Step 1 — anchor on the Reference Price and compute Reservation Prices.**

The *reservation prices* are the bot's true best bid and offer, built by pushing away from the Reference Price on each side:

```
Reservation Bid   = Reference Price − Bid Offset
Reservation Offer = Reference Price + Offer Offset
```

Each offset is a sum of four components:

| Component | What it does |
|---|---|
| **Base spread** | The default margin — the booth's cut. Set by the Pricing Profile. |
| **Inventory skew** | Pushes prices to steer inventory back toward flat (see §7). |
| **Activity adjustment** | Widens when order flow gets fast/aggressive — the market is riskier to quote into. |
| **Protection adjustment** | Extra width when protection mechanisms are on alert. |

The two sides are independent — the market can be lopsided on purpose.

**Step 2 — build the ladder.** Around each reservation price, lay out N price levels with configured spacing (uniform, front-loaded, etc. — geometry comes from the Pricing Profile and product config).

**Step 3 — spread the budget across the ladder.** The side's liquidity budget is split across levels by normalized weights (weights sum to 1, so the whole budget lands on the book) — e.g. most size near the top, thinner further out.

**Step 4 — controlled randomization.** Small, *seeded, bounded, deterministic* wobble is applied to level prices and sizes so the book doesn't look robotically identical every refresh. Because the randomness is seeded, replays still reproduce it exactly. It may never make a quote more aggressive than the reservation price (no accidentally giving users a better deal than intended), and never produces misleading behavior.

**Step 5 — tick rounding.** Bids round *down* to a valid tick, offers round *up* — rounding always widens, never tightens, so it can never cause a locked/crossed market.

**Step 6 — validate, then publish.** Before anything goes live: bid < offer everywhere, prices within permitted bands, quantities non-negative and within budget, inventory limits respected, protection satisfied, everything replayable. **A market that fails validation is never published** — the engine reconstructs the failed component (worst failures first) up to a configured retry cap, and if it still can't produce a valid market it falls back to a defensive profile (Liquidity Preservation or Protective) rather than going dark.

### 5.4 Market Adaptation Engine (Ch 9) — "pick the mode"

Watches inventory, market condition, and protection state, and sets one **Behavioral Mode** per cycle: *Normal, Active, Recovery, Liquidity Preservation,* or *Protective*. The mode is the bot's overall stance; the pricing profile (§6) is how that stance is expressed in numbers. Even in the most defensive mode, two-sided quoting continues — only a CTS-002 halt stops the market.

### 5.5 Quote Construction Engine (Ch 10) — "final assembly"

Takes everything upstream and assembles the published **Executable Order Book**. Explicitly makes *no* decisions of its own — it's the printer, not the author. It runs **protection enforcement** as the last gate before publication: it may suppress individual quotes, shrink displayed sizes, or restrict publication, but may never touch reservation prices or constitutional objects.

### 5.6 Quote Lifecycle Engine (Ch 7) — "babysit live quotes"

Once published, each quote is a tracked object with exactly one state at a time: *Created → Published → (Partially) Executed / Refreshed / Replaced / Replenished / Cancelled / Expired / Suppressed*.

- Quotes **age** and have min/max lifetimes.
- **Refresh** = update a quote's attributes in place. **Replace** = swap it for a new one. **Replenish** = top its quantity back up after users eat some of it.
- All of it bounded by the same budgets/limits, all deterministic, all recorded.
- Prefer incremental updates over rebuilding the whole book — full reconstruction is reserved for big events (profile transition, protection, reference price change, validation failure).

### 5.7 Verification & Deterministic Replay (Ch 12) — "the black box recorder"

Every cycle must persist enough state to independently rebuild every decision it made: same constitutional inputs + same engineering state + same user interactions + same version = byte-identical results. Verification is strictly observational — it can never alter the history it checks. This is the spec's ultimate audit and debugging mechanism, and it's *mandatory*, not nice-to-have.

---

## 6. The six Pricing Profiles — the bot's personalities

One profile governs each cycle. Each scales five base parameters: spread width (S), book depth (D), displayed size (Q), refresh speed (F), and inventory sensitivity (I). From §6.6.1 (defaults; a product standard may override):

| Profile | Spread | Depth | Size | Refresh | Inv. sens. | Intuition |
|---|---|---|---|---|---|---|
| **Stable** | 1.00× | 1.50× | 1.50× | 1.00× | 0.50× | Calm seas. Tight spread, deep generous book, relaxed about inventory. |
| **Active** | 1.50× | 1.00× | 1.00× | 0.50× | 1.00× | Busy market. A bit wider, refreshing twice as fast to keep up. |
| **Defensive** | 2.50× | 0.60× | 0.60× | 1.50× | 1.75× | Getting picked off. Widen out, shrink the book, slow down. |
| **Recovery** | 1.75× | 1.00× | 0.90× | 1.00× | 2.50× | Digesting a bad position. Moderately wide, very inventory-sensitive to work back to flat. |
| **Liquidity Preservation** | 3.00× | 0.50× | 0.50× | 1.25× | 3.50× | Conserving ammunition. Wide and thin, but still present. |
| **Protective** | 5.00× | 0.25× | 0.25× | restricted | 5.00× | Alarm bells. Extremely wide, minimal size, updates only as protection rules permit. Still two-sided. |

When a profile transition happens mid-flight, everything derived from the old profile (reservation prices, ladder, sizes, quotes) is invalidated and rebuilt. No stale leftovers.

---

## 7. Inventory skew — the one mechanism worth internalizing

This is how the bot stays roughly flat without ever leaving the market. Inventory influence is `IS = λ × inventory%`, where λ (sensitivity) comes from the current state/profile, and it lands asymmetrically:

**Bot is long (bought too much):**
- Bid offset **increases** → its buy price drops further below fair value → selling to the bot becomes less attractive → it accumulates less.
- Offer offset may **decrease** → its sell price edges closer to fair value → buying from the bot becomes more attractive → it sheds inventory.
- Shown sizes can shift the same way: show less on the bid, more on the offer.

**Bot is short (sold too much):** mirror image — offer backs away, bid gets more attractive.

The exchange-booth till, exactly. Two hard limits: skew is bounded by the Inventory Risk Profile, and it may *never* result in a one-sided market.

---

## 8. A worked example (illustrative numbers, not from the spec)

Chiefs stock. Reference Price ticks up to **$25.00**. Market calm → *Stable* profile. Bot is slightly long. Tick = $0.01.

1. New Reference Price → new Decision Cycle.
2. Objectives: state = stable, inventory risk = normal, Chiefs' slice of the NFL budget → bid-side $10k / offer-side $12k (offer-heavier because we're long).
3. Offsets: base spread 1¢ per side + inventory skew (long → +1¢ on the bid side, −0.5¢ on the offer side) + no activity or protection add-ons.
   - Reservation Bid = 25.00 − 0.02 = **$24.98**
   - Reservation Offer = 25.00 + 0.005 → tick-rounds **up** to **$25.01**
4. Ladder (3 levels/side, 3¢ spacing, front-loaded sizes, seeded wobble applied):

   | Bids | | Offers | |
   |---|---|---|---|
   | $24.98 | 480 | $25.01 | 610 |
   | $24.95 | 320 | $25.04 | 400 |
   | $24.92 | 190 | $25.07 | 240 |

5. Validation passes (bid < offer, budgets respected) → book published, cycle committed.
6. A user buys 610 @ $25.01 → trigger → next cycle: inventory drops toward flat, so the next book skews a touch less.

---

## 9. Quirks and open questions in the source document

The source doc is a master draft with real inconsistencies. Worth raising with InPlay before implementation — flagged here so nobody codes against the wrong text.

**Naming and numbering drift**
- The §1.7 architecture diagram and the Ch 11.4 execution sequence both list engines ("Market Posture Engine", "Price Formation Engine", "Market Structure Engine") that don't match the actual chapter names (Market **Objective** Engine, **Portfolio Allocation** Engine, **Issuer Market Making** Engine) — and Ch 11.4's sequence omits Portfolio Allocation and Quote Lifecycle entirely. §3.8 and §4.10 also hand off to chapters by the wrong names. The chapters look like the newer, substantive text; the diagram/sequence look stale.
- Stray section numbers: §5.4.1 appears inside Chapter 6; §6.13.1 cites "Section 5.3.1" where it appears to mean 6.3.1; Ch 11 has a "111.3"; §12.8 says "SDDM".
- Chapters 8 (Displayed Quantity) and 9 (Market Adaptation) key off "Market Posture," which is never defined as a chapter output — presumably the Effective Market State / Pricing Profile from Chapter 4 under an older name.

**Who publishes the Reference Price?** §1.4 says the Reference Price is "published by CTS-001," while the §1.7 diagram places it under CTS-002. Doesn't change the SDMM's job (it consumes it either way) but should be pinned down.

**Most of the actual math is deliberately missing.** The spec fixes the *architecture* and repeatedly defers formulas to "the applicable Product Technical Standard": allocation weights, liquidity budget functions, assessment classifications, ladder geometry, component formulas for the offsets, quote lifetimes, retry caps. **PTS-001 tells you the shape of the machine, not the numbers inside it.** Implementing it requires either a further product-standard document from InPlay or InPlay's sign-off on our own parameter choices.

**Conversion artifacts.** The markdown was extracted from a PDF; several equation images (notably in §§5.6, 5.9, 6.6, 6.9, 6.10, 9.4, 10.4) came through blank or garbled. Check the original PDF (`~/Downloads/inplay core technical standards PTS_001.pdf`) before trusting any formula rendering in the converted file.

---

## 10. TL;DR mental model

A deterministic vending machine for liquidity:

- **Inputs** (from upstream, never questioned): fair price, market open/closed, rules of engagement.
- **Loop:** event → assess → budget the league → price each team (fair price ± spread ± inventory skew ± safety margin) → build the ladder → sprinkle seeded randomness → round to ticks → validate → publish → record.
- **Never:** invents a price, goes one-sided, publishes a crossed market, uses real randomness or wall-clock behavior, or forgets anything (full replay, forever).
- **Personality dial:** six profiles from tight-and-generous (Stable) to wide-and-tiny (Protective), driven by conditions and inventory.
