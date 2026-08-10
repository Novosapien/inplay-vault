---
description: "Companion to the quoting engine — every function in one MM decision cycle written as pseudocode, with placeholder constants and the 23-07 v1 supersessions"
---

# Decision Cycle — Every Function Written Out

> **Component:** [[market-maker/market-maker]] · companion to [[market-maker/systems/quoting-engine]]
> **Purpose:** The standards give signatures (`EM = f(RP, MOC, MOP, CFG)`) but
> never the bodies. This doc writes out **every function in one decision
> cycle** as concrete pseudocode, so the machine is fully readable end-to-end.
> **⚠ Every numeric constant is an engineering PLACEHOLDER** (🟡) — **not a
> proposal. Stance change 22-07 (George): parameter values are not our remit —
> we ask Edwin the questions rather than propose answers.** These numbers exist
> only so the pseudocode reads end-to-end; they carry no authority. The
> authoritative question list is [[market-maker/open-questions]].
> Values mirror [[market-maker/parameters]]; symbols in [[market-maker/glossary]].

> **⚠ 23-07 v1 SUPERSESSIONS (MM call — see [[market-maker/decisions]]).**
> Edwin simplified the machine. Where this doc conflicts with the list below,
> the list wins:
> - **No top-ups:** a partially-filled order rests until completely gone.
>   Price move → cancel + post the *remaining* qty at the new price. Full
>   fill at unchanged price → reload at top of book.
> - **Publish is post-first:** no waiting for cancel confirmations; a
>   momentary self-cross during an adjustment is tolerated in v1.
> - **Cadence bifurcated:** live ~200ms · non-live 30–60s · earnings windows
>   all symbols ~5 min. (Replaces the per-session heartbeats below.)
> - **Randomizer = quantities only** — no price jitter (ε is dead).
> - **In-game driver = SR live probability pulled directly** — no event
>   weights.
> - New design surface: **fill-response logic (N14)** — "you got filled, now
>   what?"

The whole engine is one loop per team. Pseudocode is Python-ish; everything is
deterministic — the only randomness is `seeded_rng`, seeded from
`(team, cycle_id)`, so replay reproduces it exactly.

---

## 0 · The loop itself

```python
def run_team_loop(team):
    state = load_committed_state(team)          # event-sourced; empty at first boot
    while market_open(team):
        trigger  = wait_for_trigger(team, state)          # §1
        inputs   = snapshot_inputs(team)                  # RP, condition, session — atomic read
        cycle    = new_cycle_id(team)                     # monotonic counter, not wall clock
        rng      = seeded_rng(team, cycle)                # determinism
        book     = compute_cycle(state, inputs, rng)      # §2–§10 (pure function!)
        publish(team, book, state)                        # §11 cancel-replace into tZERO
        state    = commit(team, cycle, trigger, inputs, book, state)   # §12 immutable record
```

`compute_cycle` is a **pure function**: `(state, inputs, rng) → target book`.
That one design choice gives you determinism, replay, and testability for free.

---

## 1 · Trigger — when does a cycle start?

```python
def wait_for_trigger(team, state):
    # collect everything that arrived since the last cycle committed
    events = drain_event_queue(team)             # coalesce — many triggers, one cycle
    if events:
        return classify(events)                  # NEW_RP | FILL | STATE_CHANGE | SESSION_CHANGE
    if time_since_last_cycle(team) > CALL_INTERVAL:  # ✅ 23-07: ~200 ms live game ·
        return HEARTBEAT                             #    30–60 s non-live ·
    sleep_until_next_event_or_heartbeat()            #    earnings window: all symbols ~5 min
```

Rules: cycles never overlap; triggers arriving mid-cycle batch into the next
one; a game event (touchdown) arrives as `NEW_RP` because the valuation engine
already moved the price.

---

## 2 · Market assessment — "read the room"

The doc's list (order arrival rate, fill velocity, inventory velocity…) is
just rolling-window counters:

```python
def assess(state, window=5.0):                       # 🟡 5-second rolling window
    return Assessment(
        arrival_rate   = count(state.orders_seen, window) / window,
        fill_velocity  = sum(state.fill_qty, window) / window,
        book_burn      = fill_velocity / max(state.displayed_total, 1),   # fraction/sec
        inv_pct        = state.inventory / state.public_float,            # signed
        inv_velocity   = (inv_pct - inv_pct_ago(window)) / window,
        protection     = state.protection_flags)     # e.g. band breach, feed stale
```

---

## 3 · Condition classifier — `MOC = F(AOI)` (the "Do NOT define F" one)

```python
def classify_condition(feeds, valuation, system):
    if system.fault:                          return EMERGENCY
    if valuation.age_s > 10:                  return PROTECTIVE   # 🟡 RP frozen → defensive
    if valuation.age_s > 5:                   return DEGRADED     # 🟡
    if feeds.latency_ms > 2000:               return DEGRADED     # 🟡
    if recovering_from(DEGRADED|PROTECTIVE):  return RECOVERY
    return NORMAL
```

---

## 4 · Profile selection — `MOP = G(condition, session, …)` — a lookup table

```python
PROFILE = {   # (condition, session)      → pricing profile          🟡 whole table
    (NORMAL,    IN_GAME):      ACTIVE,
    (NORMAL,    AROUND_GAME):  STABLE,
    (NORMAL,    OVERNIGHT):    WIDE,        # our name for "quote $2.5–5 wide, slow"
    (DEGRADED,  ANY):          DEFENSIVE,
    (PROTECTIVE,ANY):          PROTECTIVE,
    (RECOVERY,  ANY):          RECOVERY,
    (EMERGENCY, ANY):          PROTECTIVE,  # + supervision may halt
}

MULTIPLIERS = {  # per profile: S spread · D depth · Q size · F refresh · I inv-sens
    STABLE:     (1.00, 1.50, 1.50, 1.00, 0.50),   # ✅ from PTS-001 §6.6.1
    ACTIVE:     (1.50, 1.00, 1.00, 0.50, 1.00),   # ✅
    DEFENSIVE:  (2.50, 0.60, 0.60, 1.50, 1.75),   # ✅
    RECOVERY:   (1.75, 1.00, 0.90, 1.00, 2.50),   # ✅
    LIQ_PRES:   (3.00, 0.50, 0.50, 1.25, 3.50),   # ✅
    PROTECTIVE: (5.00, 0.25, 0.25, None, 5.00),   # ✅ refresh restricted
    WIDE:       (12.0, 0.50, 0.50, 10.0, 1.00),   # 🟡 ours — overnight session
}
```

The inventory-stress escalation (PTS-001's mode switching) is one extra rule:

```python
def adapt(profile, assessment):                       # Behavioral-mode layer, collapsed
    if abs(assessment.inv_pct) > INV_MAX:     return LIQ_PRES     # 🟡 INV_MAX  = 10% of float
    if abs(assessment.inv_pct) > INV_WARN:    return RECOVERY     # 🟡 INV_WARN = 5%
    return profile
```

---

## 5 · Executable market — `EM = f(RP, condition, profile, CFG)` — a constructor

```python
def build_executable_market(rp, profile, cfg):
    S, D, Q, F, I = MULTIPLIERS[profile]
    return EM(
        anchor      = rp,
        base_spread = cfg.tick * cfg.spread_ticks * S,   # 🟡 spread_ticks = 2
        n_levels    = round(cfg.n_base * D),             # 🟡 n_base = 4 → 2–6 levels
        side_budget = cfg.l_base * Q,                    # 🟡 l_base = 5 000 shares/side
        refresh_ms  = cfg.r_base * F,                    # 🟡 r_base = 200 ms
        lam         = cfg.lam_base * I)                  # 🟡 lam_base = 0.5 (see §6)
```

---

## 6 · Offsets — the real equations (PTS-001 Ch 6, operations included)

```python
def offsets(em, a):                                   # a = assessment
    BS = OS = em.base_spread                          # base component, both sides

    IS  = em.lam * a.inv_pct * em.anchor              # inventory skew, in $ terms
    IS_bid   = max(IS, 0)                             #   long  → bid backs away
    IS_offer = max(-IS, 0)                            #   short → offer backs away

    AS = em.base_spread * min(a.book_burn / BURN_REF, 2.0)   # 🟡 BURN_REF = 0.2/s
                                                      # book eaten fast → widen, capped 2×
    PS = em.base_spread * (1.0 if a.protection else 0.0)     # 🟡 flat protection add-on

    BO = BS + IS_bid   + AS + PS                      # ✅ the doc's own equation
    OO = OS + IS_offer + AS + PS                      # ✅
    return BO, OO
```

Worked example (🟡 numbers): RP $25.00, tick 1¢, spread_ticks 2, Active (S=1.5)
→ base = 3¢. Long 4% of float, λ=0.5 → IS = 0.5×0.04×25 = 50¢ on the bid side.
Quiet flow, no protection → `BO = 53¢`, `OO = 3¢` → heavily skewed to sell.

---

## 7 · Reservation prices — real equations

```python
RBP = em.anchor - BO                                  # ✅ reservation bid
ROP = em.anchor + OO                                  # ✅ reservation offer
# spread RS = ROP - RBP is an OUTPUT — never targeted directly
```

---

## 8 · Ladder — market structure

```python
def build_ladder(em, RBP, ROP):
    # ✅ 23-07: price is purely algorithmic — NO price jitter (ε removed);
    # randomization lives in quantities only (§9)
    spacing = cfg.tick * cfg.spacing_ticks            # 🟡 spacing_ticks = 3
    bids, offers = [], []
    for k in range(em.n_levels):
        b = RBP - k * spacing
        o = ROP + k * spacing
        bids.append(  round_down_to_tick(b) )         # rounding widens,
        offers.append(round_up_to_tick(  o) )         # never crosses
    assert bids[0] < offers[0]                        # no locked/crossed — ever
    return bids, offers
```

Tick rule: bids round **down**, offers **up** — rounding always widens.

---

## 9 · Displayed quantities — real equation + weights

```python
def sizes(em, rng):
    W = normalize([FRONT ** k for k in range(em.n_levels)])   # 🟡 FRONT = 0.55
                                                  # front-loaded: ~55/25/12/8%
    out = []
    for k in range(em.n_levels):
        R  = rng.uniform(0.8, 1.2)                # 🟡 size jitter ±20%, seeded
        q  = em.side_budget * W[k] * R            # ✅ Q = L × W × R (the doc's equation)
        out.append(max(round_to_lot(q), MIN_SHOW))  # 🟡 MIN_SHOW = 50 sh, lot = 10
    return out
```

---

## 10 · Quote construction + validation — assembly and assertions, zero math

```python
def construct(bids, offers, bid_sizes, offer_sizes, em):
    book = TargetBook(bids, offers, bid_sizes, offer_sizes)
    checks = [
        book.best_bid < book.best_offer,                    # never crossed
        all(in_band(p, em.anchor, BAND) for p in book.prices()),  # 🟡 BAND = ±30%
        all(q >= 0 for q in book.sizes()),
        book.total_per_side() <= em.side_budget * 1.05,     # small rounding slack
        book.best_bid_size > 0 and book.best_offer_size > 0 # always two-sided
    ]
    if all(checks):  return book
    # reconstruction order: protection → prices → structure → sizes
    return construct(*rebuild_failed_component(...)) or fallback(LIQ_PRES)
```

A book that fails validation is **never published** — rebuilt, or the cycle
falls back to a defensive profile (still two-sided).

---

## 11 · Publish — cancel-replace into tZERO

```python
def publish(team, target, state):
    # ✅ 23-07 v1 model (Edwin + George):
    for level in unchanged_levels(target, state):     # partially-filled orders
        pass                                          # rest until GONE — never touched
    for level in price_moved_levels(target, state):
        cancel(level.old_order)                       # cancel old level...
        send_limit_order(team, level.side,            # ...post REMAINING qty at
                         level.new_price,             #    the new price
                         level.old_order.leaves_qty)
    for level in fully_filled_levels(target, state):
        send_limit_order(team, level.side,            # reload at top of book,
                         level.price,                 #    randomized size
                         randomized_qty(level))
    # post-first: do NOT wait for cancel acks — a momentary self-cross
    # during the adjustment is tolerated in v1 ("first iteration, I don't care")
```

---

## 12 · Commit — the replay record

```python
def commit(team, cycle, trigger, inputs, book, state):
    record = {                       # append-only; this IS deterministic replay
        "cycle": cycle, "trigger": trigger,
        "inputs": inputs,            # RP, condition, session, assessment snapshot
        "book":   book,              # what we published
        "version": CODE_VERSION,     # same code + same record → identical rebuild
    }
    append_event_log(team, record)
    return state.advance(cycle, book)
```

Replay = re-run `compute_cycle` on the recorded inputs and diff the output.
No separate "replay function" exists — purity of §0 makes replay free.

## 13 · Between cycles — quote lifecycle (fills)

```python
def on_execution_report(team, report, state):
    if report.exec_type == FILL:
        state.inventory += signed_qty(report)         # feeds §6's skew next cycle
        # ✅ 23-07: NO replenish — a partial fill leaves the order resting
        # with its remainder. A FULL fill invokes fill-response logic (N14):
        # in-game → reload at top of book next call;
        # off-game → maybe leave it and let the ladder fill down (design w/ Edwin)
        enqueue_trigger(team, FILL)
    if report.exec_type == BUST:                      # ExecType=H from tZERO
        state.inventory -= signed_qty(report.original)
        enqueue_trigger(team, STATE_CHANGE)
```

---

## The complete constant list this file introduces

`CALL_INTERVAL` ✅ bifurcated (live ~200ms · non-live 30–60s · earnings
burst) · assessment `window` · classifier thresholds (5 s / 10 s / 2000 ms) ·
the `PROFILE` table + `WIDE` row · `INV_WARN` 5% · `INV_MAX` 10% ·
`spread_ticks` 2 · `n_base` 4 · `l_base` 5 000 · `lam_base` 0.5 · `BURN_REF`
0.2/s · protection add-on 1× · `spacing_ticks` 3 · ~~ε price jitter~~ ✂ dead
(price purely algorithmic, 23-07) · `FRONT` 0.55 · size jitter ±20% ·
`MIN_SHOW` 50 · lot 10 · `BAND` ±30% · budget slack 5%.

**Everything not marked ✅/✂ is a placeholder** (stance 22-07: we ask, we
don't propose). Each number Edwin confirms gets promoted to ✅ in
[[market-maker/parameters]].
