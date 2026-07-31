# Market Maker — Decisions Log

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Dated, source-attributed log of confirmed decisions — including
> where spoken decisions **supersede the written standards**. When a standard
> doc and this log conflict, **this log wins** (the standards are AI-generated
> context; Edwin: "meant for Claude to read… they're fairly simple").

Format: newest first. ✅ decision · ✂ supersession of a standard · ⚠ caveat.

---

## 2026-07-31 — Chapter 5 built · §3.3–§3.5 built · the machine quotes

- ✅ **Chapter 5 is built, in the adoption spec's five pieces.**
  `volatility.py` (σ²) · `width.py` (γσ² + C) · `ladder.py` (§5.3/§5.4/§5.6)
  · `quantity.py` (§5.7) · `quotes/engine.py` (§5.8/§5.10/§7.5). **329
  tests**, ruff and mypy strict clean. Mechanisms only — every constant is
  🟡/🔴 pending E31. Deferred, externally gated: §5.5 (Ch 8) and §5.9 (E17).
  Headline proof: two fresh engines fed the same six events produce
  **byte-identical books, version chains and check reports**.
- ✅ **§3.3–§3.5 are built** — freshness bands, Reference Price Status with
  the §3.4.1 ratchet (demotions instant, promotions one rung per 10 s dwell,
  relapse resets), and Confidence with its status ceiling. §5.10's check 1
  is real whenever a status is supplied. **MEV** (§5.4's ceiling) computed
  in `reference_price.py` — the last test-supplied quote input gone.
- ⭐ **Materiality is judged BEFORE the §5.7.3 variation, on the held
  shape.** Final sizes are drawn with a fresh quote version, so they always
  differ — comparing them would republish every cycle. The comparison
  record stores pre-variation sizes; "a different possible random quantity
  is never a reason to publish" holds by construction.
- ✅ **The Quote Version increments only on publish**, and every seeded draw
  (shape, extra, dwell, sizes) is keyed on it — the whole replay result
  hangs on this. A held cycle consumes nothing.
- ✅ **N26 implemented as filed and closed.** §5.8's thresholds are the only
  publish trigger; an expired dwell only permits the next real publish to
  carry a fresh shape, at zero extra venue messages.
- ⭐ **An Invalid status gates the cycle BEFORE any state is touched —
  including σ² (George's dead-feed question).** A dead feed's frozen price
  reads as CALM to a volatility estimator and would tighten the book into
  the §2.3 danger case. Same-value-new-timestamp readings are accepted and
  reset the age — a feed confirming its number is alive; only silence
  decays trust.
- ⚠ **Cold starts are wide-when-ignorant, and that is book-visible → E31.**
  A new security's first σ² reads at the ceiling (V₀ = ceil ÷ H — the
  ceiling is on σ², not V, George's catch); a new StatusTracker starts
  Invalid and earns Degraded with its first valuation. Safe direction
  built, Edwin signs off the values.
- ✅ **The odd-tick side is a stateless seeded 50/50, not strict
  alternation** (ours under the remit line, tagged `[odd-side]`). Strict
  alternation needs "which side was it last time"; the hash bit achieves
  the same fairness with no state and full replay safety.
- 📅 **E18 refined into three separate numbers (George's challenge):** the
  poll rate (~2 s, matches SR's measured 4 s median), the reaction bound
  (~200 ms, costs nothing — the engine is event-driven), and §3.3's bands
  (break-detectors a healthy feed never trips). ⚠ Republishing every 200 ms
  to refresh the randomisation is explicitly forbidden by §5.8 and would
  cost queue position on every book 5×/second. **New question for Edwin:
  is 200 ms a reaction bound, or does he want the book visibly moving with
  no new information?** His RPV-2 instinct suggests the latter; his spec
  says the former.

## 2026-07-30b — a second market maker arrives · the Edwin call · a process fix

- ⭐ **Edwin will send spec-style documents with the equations, not code
  (agreed on the call, 30-07).** George raised it directly: three documents so
  far, each changing things, roughly a week spent understanding the first
  before the second moved it. Framed as *"we want to move fast, but this is
  not our area of expertise."* Edwin was fine with it and will rewrite the
  handoff package as a narrative document. **This is the most valuable outcome
  of the day** — more valuable to the timeline than any single algorithm change.
- ✅ **ASMM-1 is not a drop-in replacement, and Edwin accepts it.** His opening
  position was *"I think I've done the market maker for you… all you need to do
  is plug the code into T0."* The argument that landed, checkable in one line
  of each file: **`quote(now, rp, inventory)` takes the reference price and the
  share count as arguments**, and `RPV2.step(now, fair_value)` takes the fair
  value. Neither module computes either input. Our build computes both.
  Everything downstream — Chapter 3, the feed reader, the SR path, positions,
  the journal, replay — is untouched by his package.
- ⭐ **Adopt his width equation into Chapter 5.** `width = γσ² + (2/γ)ln(1+γ/k)`
  plus a seeded 0–3 tick extra. It replaces §5.2's lookup table, which is keyed
  on a state classifier **we never built** (N3's thresholds are still 🔴). His
  needs no classifier, no new inputs, works in an empty book, and cannot be
  gamed by posting orders — it reads only our own Reference Price. ⚠ The
  `(2/γ)ln(1+γ/k)` term is a **constant, 1.653 ticks**, because γ and k are
  constants. Compute it once at construction.
- ⭐ **Volatility scales the width, never the lean (George).** The width is a
  risk control, so volatility belongs in it. The lean is a **distribution**
  tool (29-07: §1.5 excludes profit, so the reason to shed inventory is that a
  market with no shares in circulation is not a market). Vol-scaling a
  distribution tool means pushing hardest to distribute during a live game and
  least overnight — backwards — and it reaches the cap sooner, so **it makes
  N20 worse**.
- ✅ **Keep our float denominator for the lean; his is wrong for us.** §4.3
  divides by the Reference Float, which answers *what share of this team do we
  own?* His divides by **4,000 shares**, which has no relationship to the
  security. Every extra share moves his lean ~22× further, so his cap arrives
  ~19× sooner: ours pins at 225,000 shares, his at **12,000**. §4.3–§4.6 stand
  as built; no change to `inventory.py`.
- ✂ **Reject his one-sided guard and his drawdown kill.** Past 6,000 shares in
  a live game ASMM-1 quotes **one side only**; §4.1 says the opposite —
  *inventory never prevents quoting* — and §4.1 is right precisely because we
  are the mandated buyer. Run as shipped there would be **no bid on any book**.
  A $25,000 mark-to-market kill on a book we are mandated to make is a market
  outage, not a risk control; §1.5 excludes profit, so drawdown is not a signal
  we should act on. The kill switch we need already exists (§6.3, operator-
  triggered, through the gateway's `cancel_all`).
- ✂ **Build none of RPV-1 / RPV-2, pending E30.** Three of its four additions
  are **invented movement**: a random OU trend worth up to **$0.80**, a
  continuous random walk, and event jumps. His own header states the purpose —
  *"the reference price sits still and the noise taker just chops around a
  fixed anchor… RPV-1 makes RP MOVE… so the whole market breathes."* That is a
  simulator. ⚠ The event jumps are a substitute for a probability feed **we
  already have**: `x_g` moves on every play, so adding them double-counts. And
  the fourth addition — RP responding to net order flow — is the compliance
  problem, because the house taker does most of the buying on day one.
- ⚠ **His width has no wide end.** The σ² ceiling of 400 caps it at ~10 ticks
  plus the random 3 — about **$0.13 on a $65 team, ever**. §5.2 Defensive is
  $0.40 and the indicated overnight spread is $2.50–$5.00. Worse: **a dead feed
  produces LOW volatility**, so the equation would quote tight into exactly the
  case §2.3 calls dangerous. **Recommendation: per-state width floors** off the
  §3.3/§3.4 freshness ladder, rather than raising the ceiling. → **E31**.
- ✅ **Take his ladder shape, keep our scale and our seeding.** Adopt the random
  level count (3–6), the random 1–4 tick step, and the geometric ×0.72 size
  decay — all of which remove further dependencies on the unbuilt classifier.
  ✂ Reject his 250-share base size (40× too small) and his `random.Random`
  jitter: **§5.7.3's seeded SHA-256 scheme is the fixture we reproduced
  byte-exact and the reason replay works.**
- ⚠ **His dwell timer must not drive a requote on its own (→ N26).** Redrawing
  the whole ladder every 3–12 s in a live game means cancel-and-repost with no
  new information, on 170 securities — a message-budget problem (T2 unanswered)
  and a lifecycle contradiction, since under rest-until-gone it wipes a
  partially-filled level for cosmetic reasons. **Rule: §5.8's material-change
  thresholds remain the gate; the dwell only defines when the shape is allowed
  to change.**
- ✂ **His port obligations, restated because they are the same three every
  time.** All `float` → §1.6-3 makes Decimal authoritative. `time.time()`
  inside the model → §10.3 requires bit-identical replay, so every `Δt` comes
  from event timestamps. `random.Random` → seeded SHA-256 only. Decimal has
  `.exp()` and `.ln()`, so step 2 of the volatility update needs no float.
- ⚠ **SNT-1 as written cannot run on tZERO.** Its entire order model is
  marketable **IOC**, and the venue supports **DAY / GTC / GTD only** —
  verified twice, the platform doc (22-07) and the OE FIX spec (23-07). The
  workaround (a marketable DAY order plus an immediate cancel) breaks SNT-1's
  own stated guarantee that it never posts resting liquidity. → **E32**.
- ⚠ **SNT-1's `max_spread_ticks_to_trade = 8` is narrower than our narrowest
  spread.** §5.2 Stable is $0.10 = 10 ticks. As configured it would never trade
  at all — least of all overnight, the state it was built for. Clean evidence
  the file was never reconciled against the MM spec. → **E32**.
- ⚠ **SNT-1 does not distribute the float, and it would hide that it doesn't.**
  Its flow is 50/50 and price-insensitive, so it defeats the only tool we have:
  a lean works by making our offer attractive, and a counterparty that ignores
  price does not respond. Volume would read healthy while **N20** is untouched.
- ⚠ **SNT-1 decides E17.** At LIVE intensity it crosses **~30,000 shares/hr per
  book** against a 10,000-share L1, and its sweeps cap at 3 ticks while our
  ladder spacing is $0.05 — so **every order lands on L1 only**. Under
  rest-until-gone the top level erodes to nothing over ~40 minutes and reloads
  only when fully consumed. §5.9's replenishment makes it a non-issue.
  **E17 stops being a preference and becomes a correctness question.**
- 🔴 **Two house accounts trading with each other, on a FINRA-regulated ATS.**
  On day one SNT-1's counterparty is overwhelmingly the MM. Common beneficial
  ownership on both sides is the definition of a wash trade, and the 23-07
  rulebook decision prohibits exactly this for users. Concrete: the OMS spec
  has per-account wash-trade blocking, so if T0 treats the two as related the
  prints are simply rejected. **Compliance read, not an engineering answer** —
  same class as S8. → **E33** + **T13**.
- ⚠ **The package disagrees with itself and with its own verification claim.**
  `HANDOFF.md` §3 says the flow impact is 10 ticks per 1,000 shares;
  `RPV2Config` says **6.0**. The package is described as clean-room verified.
- ⚠ **Two findings from his own results, worth reflecting back.** His §7 admits
  teams priced under ~$50 run **negative median MM P&L** — about half the
  universe. And his cohort economics put **retail participants at −$6,100 a
  session** to the house.
- ⚠ **Correction (George, 30-07): our day-one position is NOT a fixed 500,000
  shares a team.** The Mandate is *buy whatever participants do not*, so it
  depends on demand — more or less. 500,000 is the ceiling on the ten-round
  reading of **E24**, not an expectation. ✅ The argument against ASMM-1's
  scale does not rest on it: even a **90 % subscribed** offering leaves ~50,000
  shares a team, still **8×** his one-sided threshold and **4×** his lean cap.
- 📅 **Build status (George, 30-07): roughly halfway, and 80–90 % of the time
  so far has gone on understanding rather than writing.** Three documents, each
  superseding the last. The process fix at the top of this entry is the direct
  response.
- ⭐ **The market cannot move the price, and that is arithmetic (George, 30-07b
  → E34).** A normal market has several **profit-seeking** market makers each
  guessing fair value, and flow moves the price between them. We have **one**,
  explicitly **not** profit-seeking (§1.5), quoting a fixed spread around a
  **model** number. The quote is `RM = RP + IA` and §4.5 bounds `IA` to
  **±$0.25** — so that $0.50 band is the *entire* range in which market
  activity can move the price, **0.5% on a $50 share**. The Mandate pins us at
  the bottom of it on day one: **$0.00 of downward room, $0.25 upward, and only
  if participants buy our whole holding.**
  ⭐ **Corroborated independently: Edwin built RPV-2's invented price drift
  because he noticed his prices did not move.** Two routes, one finding. He
  fabricated movement; the real problem is that nothing real can create it.
  ⚠ **The product consequence is the one to lead with:** users watching prices
  move in the app would be watching our model, not a market — and a participant
  can never be right *early*, only right *at settlement*.
  **This reframes N20: it is not a distribution problem, it is the
  price-discovery problem**, and it is the root cause behind E30 and E35 too.
  Three ways out, of which (2) and (3) are the same fix: accept it as a
  fixed-odds product and stop calling it a market · raise `M` substantially ·
  distribute the float so participants set the price between themselves.
- ⚠ **Inventory is NOT a clean sentiment channel here (George's correction,
  30-07b).** I had argued flow reaches the price through inventory → lean. In a
  normal market maker that works, because accumulating costs money, so the
  markdown is an inference — *"flow is beating me, my price is wrong."* Ours has
  unlimited capital and is **required** to buy, so most of our position carries
  no information about whether our price is right. The mandated position is
  noise sitting on the signal, and it pins the lean before any voluntary flow
  can register.
- 🔴 **The Reference Price definition was reversed and nobody noticed (→ E35).**
  20-07: *"Reference Price = the mid between best bid and best ask."* The v1.3
  spec: the model value, `ROF + ΣGEV + RAV + EAV`. We built the spec's version.
  **The change is recorded nowhere as a decision.** Our recommendation is to
  keep the fair value pure — this security settles at a known number (§11.3), so
  sentiment does not change what a share pays, and chasing flow both destroys a
  correct participant's edge and creates an exploit. ⚠ But that recommendation
  only holds **if E34 is answered by distributing the float**, so the market has
  somewhere real to disagree.
- ✅ **The sentiment-in-RP blend was proposed and WITHDRAWN the same evening
  (30-07, review under Fable).** The idea: `RP = w × model + (1−w) ×
  participant-only price (§5.5)`, `w` falling as volume grows. Killed on three
  findings: (1) the model's forward leg is already **anchored to de-vigged
  sportsbook lines** — a far deeper crowd than our book will ever be, so the
  blend dilutes a strong crowd with a weak one; (2) **resting orders are free**,
  so a §5.5-driven mark is spoofable, and §4.2 marks every portfolio and the
  leaderboard at RP — with prizes attached, someone will; (3) **§2.3 is
  therefore deliberate and correct**, not an oversight. Season 1 collects the
  behavioural tape; any sentiment mechanism is a season-2 question argued from
  evidence. **E34 is asked as product intent only and blocks no build.**
- ⚠ **Two of the E34 claims were overstated and are corrected in the filing.**
  *"A participant can never be right early"* — false: the price moves on every
  result, probability and daily file, so being right pays as evidence lands.
  *"A wrong model is never corrected"* — false: banked results correct it at
  $5 a time, weekly. The true residual claim: **opinion ahead of evidence
  cannot be monetised, and the app shows a model tracking reality, not a crowd
  discovering it.**
- ✅ **The quote assembly is fixed (George, 30-07 evening):**
  `RP → + lean → centre (RM) → ± width/2 → L1 → ± step → ladder`. The lean
  moves the pair and never the gap; the odd tick alternates sides per draw.
  Chapter 5 builds this shape.
- ✅ **Distribution runs on size and depth, not price (George + review).** While
  the mandated position is large: more levels and much larger sizes on the
  offer, fewer and smaller on the bid. Both prices stay fair — no §2.3 issue,
  no §5.4 issue, works under any E34 answer. Needs three InPlay numbers
  (→ E31): the §5.7.3 quantity ceiling (15,000 binds first), the §5.7.2
  modifier range (1.5× is far too small), and §5.2's symmetric level counts
  relaxed.
- 🟡 **The split-position lean is proposed, not built.** `traded = NP −
  OpeningPosition`; sentiment lean on `traded` with a small cap, distribution
  lean on the mandated part with Edwin's cap. **Blocked on E27** — until the
  opening position has a publisher, `traded` cannot be computed. §4.5's
  single-position lean stands in the meantime.
- ▶ **Full rulings, area by area: [[market-maker/asmm1-adoption-spec]]** —
  including the new §0 assembly section.

## 2026-07-30 — the spec filter · Chapter 4 built

- ⭐ **The spec's finance is authoritative; its engineering is AI scaffolding
  (George).** The v1.3 spec was written by a domain expert in finance who does
  not code, using AI. So: formulas, settlement, the skew mechanics, the
  de-vig, $5 a win — his own domain, defer to them. Event types, idempotency
  tables, journal design, replay architecture — generated, so **judge on
  merits rather than obeying**. ⚠ Judge, not ignore: some scaffolding has
  proved load-bearing. §7.3's per-game keying exposed the adapter bug that
  left half the universe unpriced, and §7.2's lifecycle ordering settled
  where rejection belongs. This filter is narrower than the 22-07
  platform-doc one and applies to the build spec itself.
- ✅ **Chapter 4 is built.** `position.py` (§4.1 net position, §4.2 average
  cost and P&L) · `inventory.py` (§4.3 float and ratio, §4.4 pending
  exposure, §4.5 the skew, §4.6 Reservation Midpoint) · `position/engine.py`
  (fills in, positions and skews out). **171 tests**, ruff and mypy strict
  clean.
- ⚠ **The Reservation Midpoint goes negative without §4.6's floor.** §4.6
  says RM "must remain within the price boundaries of §5.4" and that is
  load-bearing, not decoration: §5.4's floor is $0.01 and the skew reaches
  −$0.25, so `RP $0.10 + IA −$0.25 = −$0.15`. A team late in a losing season,
  priced near the floor, with us holding most of its float — not a contrived
  case. `reservation_midpoint()` clamps, and a clamped RM is worth noticing
  because it means the skew is asking for something the price cannot deliver.
- ✅ **The Position Ratio is deliberately NOT clamped to ±1.** v2 lets
  participants short the full float, so what can be sold to us is float plus
  short interest, and §4.1 imposes no inventory limit. A ratio above 1.0 is a
  state the spec permits (**E26**); clamping it would hide exactly the
  situation we would most want to see.
- ✅ **A fill for an untracked security RAISES**, deliberately the opposite of
  the valuation engine's silent skip. An unknown *team* is a legitimate §2.5
  boundary — NCAA sides play FCS schools with no Team Company. An unknown
  *fill* has no such story: we only receive execution reports for orders we
  placed, so it means the universe is wrong or we traded something we cannot
  price. Either way we hold inventory that never skews.
- ✂ **`IPO_ALLOCATION` and `CORPORATE_ACTION` are not built (George).** The
  opening position arrives as a constructor argument instead — same status as
  the RAV/EAV mocks, and replay still reproduces it. §7.3 reserves both event
  types but nothing sends either (**E27**, **E28**). Build them when we know
  what actually arrives rather than guessing. ⚠ I first argued the v2 dates
  force an overlap between the primary and the secondary; re-reading, §1.1 is
  clean and the overlap appears only from §2.1 + §5.2 together — drafting
  sloppiness, not intent. Conceded.
- ✅ **Realized P&L is emitted per fill and never accumulated.** A running
  total is derived state — the thing §2.5 prohibits, and the thing that caused
  the double-banking defect. A consumer sums the records; replay reproduces
  the total exactly.
- ⚠ **Average cost is a division, so it recurs.** `$23,000,000 ÷ 450,000`
  cannot be held exactly, so the unrealized P&L lands 5 x 10⁻²² from a round
  number. Not a defect — it is why §1.6-3 says round only where the algorithm
  says to. **Never compare an average cost against a hand-written literal.**
- ✅ **Comments move to a `# Notes` block at the end of each file (George).**
  Inline density was making the code unreadable. Short marked line inline,
  long form at the bottom keyed by a **named** marker — names survive edits,
  numbers drift. Nothing is deleted when a comment moves; it is relocated.
  Applied to all ten source files; repo `CLAUDE.md` rewritten so it holds.
  Tests are the exception — there the comment IS the statement of behaviour.
- ⭐ **Wins are conserved, and the feed does not conserve them (George).** 32
  NFL teams x 17 games = 272 games, so the 32 expected-win figures must sum to
  **272**. Real BetMGM lines sum to **275.00**; after the de-vig, **273.95**.
  The de-vig removes a third of the excess, but Edwin's rake works per team
  and nothing enforces the league total. Worth **$0.30 a share**,
  one-directional — every NFL name slightly high, never low — and we are the
  mandated buyer of the residual float, so ≈**$8.6 M**. **George's call
  (30-07): minor, park it as a question (N25) rather than act on it.**
  ⚠ NFL only — NCAA teams play FCS opponents outside the 170, so their wins
  legitimately exceed games ÷ 2.
- 🔴 **Two of §4.1's four inputs have no publisher.** Buys and sells arrive as
  fills and that path is built and QA'd. The **opening position** (**E27**)
  and **corporate adjustments** (**E28**) have nothing sending them. E27 is
  now the second-priority open question: v2 makes us the buyer of all
  remaining shares, so it is the entire day-one book.

## 2026-07-29b — the on-field leg built · the window is kickoff → the next T

- ✅ **The on-field leg is built.** `on_field_value()` in
  `mm/valuation/reference_price.py`, with `KickedOffGame`. 70 tests, ruff and
  mypy strict clean. Edwin's three stated unit tests plus four more: the
  in-play cancellation trap, the tie as half a win, two games netted, and the
  two sides of one game cancelling.
- ✂ **It supersedes §3.1.1's on-field terms** (`ROF + Σ GEV(g)`) with
  `$5 × (T − Σ p_ref(g) + Σ x_g)`. Authority: this log outranks the spec, and
  Edwin confirmed the formula on 28-07. **E23** — how his composition maps
  back to §3.1.1 — stays open. `RAV`/`EAV` are untouched.
- ⭐ **The adjustment window is kickoff → the next T, NOT kickoff → the final
  whistle (George's catch).** Verified with numbers: Chiefs T 11.6, p_ref
  0.566. They win, and if the adjustment stops at the whistle the price
  **drops $2.17 for winning**, then jumps back when the 06:00 file lands. A
  sawtooth every Sunday evening. Edwin's unit test (c) exists for exactly
  this: *"after the final whistle, it holds at banked-plus-expected until the
  next T arrives."*
- ✅ **Membership of G is a timestamp comparison, never a judgement.** Compare
  each game's kickoff time against T's `effective_time`:

  | Game | T holds it as | In G? |
  |---|---|---|
  | kicked off **before** T | a banked fact | no |
  | kicked off **after** T | a probability | **yes** |
  | not kicked off yet | a probability | no |

- ✅ **An upcoming game needs no adjustment** — it is already inside T, and
  T's guess is still the best one we have. This is why the adjustment starts
  at kickoff and not before.
- ✅ **A played game needs no probability** — `x` is the result: 1, 0.5 or 0.
  Only a game in play needs a live number. A loss moves the price **down** by
  `$5 × p_ref`, so a favourite losing costs more than an underdog losing.
- ✅ **With a healthy feed, G holds 0 or 1 games.** A team plays once every
  4–7 days and T lands daily. The set form Edwin required is purely the
  missed-file case — kept, because a missed file otherwise loses a real win
  from the price silently.
- 📅 **Kickoff time is now load-bearing.** The G membership test needs it, and
  the adapter currently discards it. **Fix-pass step 4 is a dependency of
  pricing, not a tidy-up.**
- ⚠ **Edwin's definition of `p_ref` disagrees with his own unit test (a), and
  we build the definition (George, 29-07b).** He defines `p_ref` as the
  pregame probability *"frozen at the moment T was ingested"* (06:00 ET), but
  test (a) requires the leg to equal `$5 × T` **at kickoff**, seven hours
  later, which only holds if `p_ref` is the closing number. Worked example:
  Chiefs T 11.6, 06:00 probability 0.566, kickoff 0.540 → the definition
  gives $57.87 and the test expects $58.00, a **13¢** gap. Freezing at
  kickoff instead leaves that 13¢ of pregame news out of the price until the
  next file. **Ruling (George): freeze AT KICKOFF — the closing pregame
  probability.** Edwin's own fallback clause already permits it, it makes his
  test (a) exact rather than approximate, and it needs no probability held
  from 06:00. The 13¢ of pregame drift stays inside T until the next file;
  that is the accepted cost. **Asked anyway → N22.** One line to change on
  his answer.
- ✅ **A tie is a terminal state, not a live probability (George).** Sportradar
  gives a two-way market and no tie probability exists (S6), so `x` is simply
  the live win probability while the game is in play, and becomes 1, 0.5 or 0
  once final. The 0.5 appears only at settlement. Do not blend a tie
  probability into the live number — there is no such number to blend.
- ✅ **Assume at least one T always exists (George).** T is required at
  construction rather than optional, so a "no price yet" state cannot occur.
  Edwin's rule already guarantees it operationally: a missing daily file is an
  alarm and we hold the last value.
- ✅ **A stale T is repairable, even weeks later.** Sportradar's timeline
  endpoint returns a game's whole history, so a pregame probability we failed
  to capture at kickoff can still be recovered.
- ✅ **Do not smooth on a new T** (reconfirmed). Edwin: *"a discontinuous
  repricing reflecting newly available information, not market-maker
  behavior."* Expect the new T to land near, but not exactly on, our adjusted
  number — his is the whole season rebuilt from his ratings, so other results
  moved it too. Widen quotes around the 06:00 window if we want cover.

## 2026-07-29 — IPO Requirements v2 · the gospel ruling · the deadline moves

- ✅ **Authority ruling (George): IPO Draft Business Requirements v2 (28-07)
  and `reference/season-win-totals-170.csv` are gospel.** Where either
  conflicts with an email, a spreadsheet or the IPO Supplement, they win. This
  settles three things immediately: **NFL float is 900,000** (not the 875,000
  in Edwin's email of the same day) · **§5.2.3 means NCAA**, 1,000,000 shares
  available for shorting · the **Washington Commanders DraftKings line
  stands**, so its IPO price is the price.
- 📅 **The deadline is secondary trading, not the season.** NCAA secondary
  opens **26 or 27 August** (v2 disagrees with itself — E25), NFL on
  **7 September**. The market maker must be quoting from the earlier date,
  about four weeks out. Every earlier plan assumed the season start.
- ✅ **The market maker buys ALL remaining shares, not 85%** (v2 §4). This
  **supersedes spec §9.2**'s `floor(0.85 × UnsoldShares)`. Closes E20.
- ✅ **InPlay Markets is the exclusive seller in the primary** (v2 §2). The
  market maker is a **buyer only** during the offering. Participants may buy
  only — no selling and no shorting until secondary opens.
- ⚠ **Shorting is new and unbounded** (v2 §1.2, §5.2). The full float may be
  sold short in the secondary market. So what can be sold to us is float
  **plus** short interest — 2,000,000 rather than 1,000,000 for an NCAA team.
  §4.3's Position Ratio can exceed 1.0, and §4.1 imposes no limit. → E26.
- ⭐ **The reason to distribute is liquidity, not profit or risk (George).**
  §1.5 excludes profit as a motive and the market maker has unlimited money,
  so the usual reason to shed inventory does not apply. The real reason is
  that **a market with no shares in circulation is not a market** —
  participants have nothing to trade with each other, and §3.6.3 excludes
  market-maker volume from the off-field value, so our own trading cannot
  feed the Popularity Index either. **That reframes the inventory skew as our
  distribution tool rather than our risk tool.**
- ⚠ **And the skew has no room left.** §4.5 caps it at $0.25, which binds once
  we hold 25% of the float. After the offering we hold 50–100%. Verified:
  holding the entire NFL float reads **identically** to holding a quarter of
  it. The only tool the spec gives us for the thing that actually matters is
  saturated from the first minute. → N20.
- ✅ **The fix pass is complete.** All four defects from the 27-07 review are
  fixed and merged (PRs #1, #2, #3). 63 tests. One new defect (#5, the
  `GameStatus` coverage flag) is recorded and open.
- ✅ **Nothing blocks the build.** The spec covers Chapters 3–8 in full. Only
  §5.9 replenishment is genuinely blocked, because **E17** is a mechanism
  question and not a value. Two data gaps — the schedule (§3.6, §2.5) and the
  live feed — do not stop us writing code today.

## 2026-07-28 — Edwin's answers to all six questions ([[standards/MM-edwin-answers-28-07|email]] + code + IPO Supplement)

- ✅ **Expected wins, not per-game probabilities — but never the raw posted
  line.** De-vig both sides, then `mean = line + σ_mkt × InvNorm(fair over)`.
  σ_mkt is a league constant: **2.7 NFL, 2.2 NCAA**. Worked example verified
  against his code to 4 dp.
- ✅ **`T` is whole-season** — banked wins included — which is exactly why the
  formula subtracts. The published feed field is the opposite: **remaining
  games only**. Both, deliberately; his definitions block governs.
- ✅ **Our double-count fix confirmed, and generalised.**
  `$5 × (T + Σ(x_g − p_ref(g)))` over **G, a set** of games kicked off since
  T's timestamp. A game **enters at kickoff and stays until a new T absorbs
  it** — so the adjustment survives the final whistle. Building it for a
  single live game (as I first did) loses the win until the next publication.
- ✂ **Do not smooth the mid** when a new T lands. *"The price change… is a
  discontinuous repricing reflecting newly available information, not
  market-maker behavior. Smoothing it would mean quoting a price you know is
  wrong."* Widen quotes around publication windows instead.
- ✅ **College is his, not Sportradar's** — MOV-capped Elo, calibrated weekly
  against SR's posted pregame probabilities; NFL raked so remaining-game
  probabilities sum exactly to the de-vigged sportsbook total. Published as a
  **daily 06:00 ET JSON file, all 170 teams every file**, heartbeat even when
  unchanged, **a missing file is an alarm**. `team_id` is Sportradar's
  competitor ID — no mapping table. **Closes S10.**
- ✅ **Ties: price the two-way market as proposed; settle at 0.5 → $2.50.**
  Closes S6. The ~0.4 % drag is a reserve, not a model.
- ✅ **IPO: `price = EV − discount`, and RP seeds at EV, not the listed
  price.** Frozen T-3, full precision, never revised. ⚠ The Supplement (§8,
  Open Item 10) had this **[OPEN]** and warned it gaps every discounted name
  1–3 % at the open with the MM as counterparty — the email decides it
  anyway, so that is now an *accepted* day-one exposure.
- ⚠ **Conflicts opened, not resolved:** **E20** §9.2's `floor(0.85 × Unsold)`
  vs the Supplement's MM Primary Mandate (buy *all* remaining, Rounds 1–10,
  up to 85 M shares) · **E21** his own two IPO implementations disagree on the
  tie leg, the Bradley-Terry inputs and the discount scaling, and the
  acceptance test is unrunnable without `teams_config.py` + `odds.csv` ·
  **E22** issued share count still missing, which blocks all of Chapter 4 ·
  **E23** his "retained earnings + on-field + ad accrual" composition vs
  §3.1.1's `ROF + ΣGEV + RAV + EAV`.
- ⚠ **His code is all `float`.** §1.6-3 makes Decimal authoritative, so
  `TeamPricer` and `validate_records()` must be **ported, not lifted**,
  despite the email's "lift it verbatim". Formulas port cleanly; only types
  change.
- 📅 **Dates now bind us:** NCAA freeze **19 Aug**, NCAA offering **22–28
  Aug**, NFL freeze **2 Sep**, NFL offering **5 Sep**.

## 2026-07-27/28 — Build review + the expected-wins insight (George + Claude)

- ✅ **A probability reading is a fact about a GAME, not a team — one event,
  both securities.** §7.3 keys a probability update on Source + Game +
  Provider Sequence with **no team component**, so per-team events collide:
  same key, different payload, and the acceptor correctly refuses the second
  as a conflicting duplicate. Proven on the real Chiefs–Ravens timeline —
  1,089 accepted, **1,089 conflicts, and the Ravens never priced at all**.
  The adapter now emits one side-neutral envelope per reading and the
  valuation engine fans it out. ⚠ **Spec tension to raise:** §3.2 describes
  a probability input record as carrying a single *Team Company ID*, while
  §7.3 keys the event per game. We implement the §7.3 shape because it is
  the normative table and the only one that works.
- ✅ **The pairs identity is a hard invariant, not a comment.**
  `GEV(home) + GEV(away) = $5.00 × (P_home + P_away + P_tie) = $5.00`,
  always. Enforced in the engine and checked **before** any state is
  written. Verified exact across 5,948 normalized triples, so a mismatch is
  never a rounding artefact — it means swapped sides or a broken §3.2.1
  repair. §2.3: wrong quotes are worse than no quotes, so it raises.
  (George's call: he asked for a belt-and-braces check; double-validating
  the *input* was measured to be a no-op — 0 disagreements over 1,001
  splits — so the check moved to the *output*, where it catches things
  double-validation never could.)
- ✅ **The universe map must be complete or we refuse to start.** A missing
  team entry was previously indistinguishable from a legitimate non-universe
  opponent (NCAA sides play FCS schools with no Team Company) — both simply
  produced no price, silently, forever. Construction now rejects any
  security the map cannot reach. (George spotted this.)
- ⭐ **RP needs expected WINS, not per-game probabilities.** Every win pays a
  flat $5, so `Σ GEV(g) = $5.00 × Σ P_win(g) = $5.00 × expected wins` — the
  per-fixture breakdown cancels out entirely. Collapses E19's requirement
  from ~2,400 game probabilities to **170 numbers**. (George's insight.)
  Sent to Edwin 28-07 as a proposal, not adopted unilaterally: it is
  arithmetically identical to §3.1.1 but not what §3.1.1 writes.
- ⚠ **Keep the three-term structure even though it collapses.**
  `W×$5 + p_live×$5 + tail×$5` is algebraically `$5 × T`, but the first two
  terms are *facts* and only the third is an estimate. Collapsing it makes
  the price track the bookmaker's opinion about games we already know the
  result of, and stops it hardening as the season resolves.
- ⚠ **The in-play cancellation trap (verified).** Season win totals are
  futures markets and are never repriced during a game. Subtracting the
  *current* live probability from a frozen whole-season total cancels the
  in-game movement exactly — the price sits at $60.00 whether the team is at
  60% or 90%. **Fix:** at kickoff the game leaves the tail carrying its
  *pre-game* probability, and the tail freezes for the game's duration.
- ✅ **HOW-IT-WORKS.md is the explainer, BUILD-LOG.md is the status.**
  Concepts in one, state in the other, and the boundary is stated in the
  file so they don't drift into each other and become untrustworthy.
- ✅ **`inplay-market-maker` now has a remote** —
  `Novosapien/inplay-market-maker`, private. Two days of work had existed on
  one disk.

## 2026-07-24 — Friday touchdown (Edwin + Cody + Troy + Kevin + Novo) — [[24-07-2026-touchdown]]

- ✅ **Probabilities ride SR's betting-side feed (Cody).** SR's licensed
  *media* data feeds power the gamecast; SR's own hosted match-tracker widget
  runs on *betting* data — faster, but the raw betting feeds are licensed to
  sportsbooks only and unavailable to InPlay. The **probabilities API is off
  the betting feed** and updates faster than media events — so the MM (which
  consumes the probability, not the event) is not disadvantaged: in-app users
  see events at the same moment the MM does. Edwin's ruling: use the fastest
  feed available for everything; must never lag the sportsbooks (S4
  mitigated). Cody lobbying SR for the betting feeds in parallel.
- ✅ **MM monitoring dashboard — phased, read-only first (Edwin ask).** An
  InPlay person monitors the market as we near production. Phase 1: see the
  backend working — positions/holdings ("how many shares it owns of PMX Y"),
  variables visible but static. Later: changeable variables for an active
  trade. Explicitly NOT about changing MM logic. George: the MM is just
  another user — the **same inventory/portfolio APIs that serve users serve
  the dashboard**. Feeds [[market-maker/systems/mm-ops-ui]].
- ✅ **SR entitlement channel agreed:** George emails the blocked
  products/versions to SR support + Scott + Cody (→ S7); Cody drives with
  Scott + David. Master-key model; call limits + versioning claimed moot at
  the real-time tier.
- ✅ **E19 reinforced:** Edwin re-affirmed he builds the remaining-season
  probability model internally ("I'll come up with a piece that you can
  pull"); weekly manual input via the MM platform floated. "We'll work that
  out over the next few days."
- ✅ **NCAA IPO prices in motion (E3):** Cody delivered the NCAA totals;
  Edwin pushing updated IPO prices into the app same day.
- ✅ **Trading launch anchor:** trading functionality live for **~Aug 22**
  (Troy: "we need to get this live for the 22nd"); the KYC-less academic
  variant is deliberately deprioritised behind it (needed ~first week of
  September).

## 2026-07-24 — Gateway: everything the MM needs is BUILT (Hasan, second report)

> Supersedes the earlier same-day entry. All five asks **plus both
> nice-to-haves** are built and deployed; what remains is a cert pass, not a
> build. Deployed code runs **ahead of the pushed `origin/main`** we fetched —
> build to the contract below and reconcile when the code lands.

- ✅ **Cancel (35=F) + cancel/replace (35=G) LIVE** (`33bf32a`), verified
  against **real tZERO QA**: cancel acked `150=4` solicited ~12 ms, replace
  acked `150=5` ~11 ms. Intake `gateway.orders.cancel`. The **caller mints
  the ClOrdID**; the gateway fills 55/54/38 from tracked state (35=F must
  carry the original OrderQty). Replace publishes `ORDER_REPLACED` on **both**
  the old and new subjects, so consumers keyed on either id stay consistent.
  GTD expiry inherited on replace unless overridden. `HandlInst(21)="1"` set
  on G — the venue requires it there while rejecting it on D (**verified in
  the OE spec, see below**).
- ✅ **Dead-man switch built + deployed, OFF** (`MM_ENABLED=false` **until our
  bot exists — we are now the gating item**). Needed an unlisted
  prerequisite: a **Redis open-order index**, because after a gateway restart
  the in-memory tracker is empty and 35=F can't be built without the original
  OrderQty. Shape: heartbeat silence **4 s** → rate-paced 35=F sweep,
  `Text(58)="deadman"`, **latched** (a bot down an hour produces one sweep,
  not one every 4 s), armed at boot so a restart rehydrating orphaned MM
  quotes is covered. Exercised end-to-end against the mock venue; **not yet
  against real tZERO** — cert item.
- ✅ **Tag 60 passthrough LIVE** (`e845721`): `source_timestamp` now carries
  tZERO's `TransactTime`, parsed across second/milli/micro variants, with the
  gateway clock as **fallback rather than the answer**. Unit-covered; not yet
  eyeballed on live venue traffic (cert item). → our envelope's
  `provider_event_time` is real for venue events.
- ✅ **Rejection NAK LIVE:** every validation failure on
  `gateway.orders.new` publishes `ORDER_REJECTED` with `local:true` + reason
  (`INVALID_CLORDID`, `UNKNOWN_SYMBOL`, `INVALID_SIDE`, `INVALID_QUANTITY`,
  `INVALID_PRICE`, the GTD/TIF family, `SESSION_DOWN`, `SEND_FAILED`).
  **No guess-by-timeout.** ⚠ Requests missing `userId`/`clOrdId` remain
  log-only — no subject exists to reply on.
- ✅ **MM namespace deployed (off):**
  `gateway.orders.mm.{new,cancel,replace,heartbeat,cancel_all}` on its own
  queue group, so MM churn can't starve retail intake. Token-bucket governor
  + **ClOrdID prefix partitioning enforced both ways** — MM traffic must
  carry the prefix, retail must not, else the dead-man's notion of "an MM
  order" isn't trustworthy. Gateway's NATS user already has
  `subscribe: ["gateway.>"]`; **only our bot's user needs an ACL change**.
- ✅ **At-least-once ON** for `order.*` / `position.*`: publish-with-ack,
  `Nats-Msg-Id` dedup, bounded retry, then a **Redis dead-letter rather than
  a drop**. Verified in production (0 retries, 0 dead-letters, core
  subscribers unaffected). **Market data deliberately stays on core NATS** —
  "a stale quote is worthless, a lost fill is a support ticket."
- ⚠ **Correction to our earlier note:** "the publisher drops on queue
  overflow" was accurate but incomplete — it also used fire-and-forget
  `nc.Publish`, so a message could be lost *without* the queue overflowing.
  The dropped counter never left zero; the real exposure was the un-acked
  publish.
- 🟡 **Remaining = cert pass, not build:** does tZERO accept `Text(58)` on
  35=F · pin the placeholder **50 msg/s governor** and **4 s dead-man
  window** against tZERO's session-throughput guidance · exercise the sweep
  against the live venue with a hand-rolled heartbeat publisher.

**Consequences for the MM build (new obligations on us):**

- ✅ **We must publish a heartbeat** on `gateway.orders.mm.heartbeat` faster
  than the dead-man window, or our own book gets swept. New requirement for
  the venue-sync engine (spec Ch 8).
- ✅ **Our ClOrdIDs must carry the MM prefix** (gateway convention) *and* obey
  the venue's ≤20 chars / no-leading-zeroes. **George 24-07: the ID scheme is
  fine** — 18 chars after the prefix is ample. Real constraint is that IDs be
  generated **deterministically**, so replay reproduces the same chain.
- ✅ **`cancel_all` is our kill-switch mechanism** — spec §6.3 (global kill
  switch → Suspended → "initiates cancellation of cancellable orders") now
  has a real implementation to call.
- ✅ **Duplicate fills are now possible by design** (at-least-once). Our
  §7.3 execution idempotency (venue + ExecID) moves from speculative to
  load-bearing.
- ✅ **Peak messaging is not a concern (George, 24-07)** — the 50 msg/s
  governor is Hasan's placeholder, not a venue limit; diff-based publishing
  is an optimisation, not a requirement.
- ✅ **Heartbeat cadence + dead-man window are OURS to set (George, 24-07)** —
  "we can update the code ourselves if we need." Decide from the real cycle
  timing once venue sync exists; don't inherit the 4 s placeholder by default.
- 🔴 **New ask:** NATS ACL for the MM bot's user (publish on
  `gateway.orders.mm.>`).

## 2026-07-24 — tZERO OE FIX spec re-verified (against the PDF, not memory)

- ✅ **ClOrdID = max 20 chars, NO LEADING ZEROES** — stated identically on
  35=D, 35=G and 35=F. ⚠ **Replace and cancel each carry TWO ids** —
  `ClOrdID` (new) + `OrigClOrdID` (superseded) — **each** capped at 20. Every
  replace mints a fresh id, so the chain is a sequence of ids, not one id.
- ✅ **`HandlInst(21)`: "Currently not supported" on 35=D · "Y — value is
  always 1" on 35=G.** Hasan's handling verified exactly.
- ⚠ **The OE spec contains NO rate-limit language whatsoever** (no msg/s,
  throughput, throttle or `MaxOrdRate`). **T2 is therefore unanswerable from
  documents** — `MaxOrdRate` is a per-account OMS configuration tZERO applies
  at account creation, so it must be asked **with T1**, in the same
  conversation.
- ✅ **MM data consumption (George):** the MM subscribes to the gateway's
  NATS streams (fills, positions, top-of-book, status) — no second tZERO
  session in v1; the dedicated MM FIX session stays a filed T0 ask. The MM
  subtracts its own resting orders from the feed to get the §5.5
  participant-only book.
- ✂ **Watchdog/supervision descoped from the MM (George, 24-07):** trade
  busting — and its detection — is tZERO's remit; consistent with the v1.3
  spec, whose six-engine pipeline has no supervision engine. Residual: T4
  keeps the ask to confirm T0 *detects* out-of-band trades, not just executes
  busts. The public trade stream remains consumed later only for §3.6
  off-field volume counting.

## 2026-07-24 — SR ingestion research (code + live API + SR docs via MCP)

> Question asked: could the MM ride SR's **push stream** (→ worker →
> Centrifugo) instead of polling, for lowest latency?

- ✂ **There is NO probabilities push feed — for any sport.** Verified four
  ways: the push message schema carries no probability field; 414 captured
  push messages across six fixtures contain zero matches for "prob"; the
  published live contract has none; and SR's own docs list the *only* push
  products as **Events, Statistics, Draft Picks, Draft Trades, Pulse** (NFL)
  and **Events, Statistics** (NCAA). Searching **every** SR spec for
  `subscribe` returns nothing outside the events streams.
  **Probabilities are REST-pull only. Full stop.**
- ⚠ **CORRECTION — probability update cadence.** Previously recorded (S5 +
  the 24-07 entry below) as *"per play, ~30–40 s"*. **That is wrong by an
  order of magnitude.** Measured from our own captured Chiefs–Ravens
  timeline: **median gap 4 s**, mean 11.5 s, p90 28 s; **64 % of updates
  within 5 s**; **1,089 updates across ~160 plays** (≈6–7 per play) because
  live win probability decays with the game clock, not only on plays; 1,070
  of 1,088 were genuine value changes, not restamps. **Consequence: a ~2 s
  poll is justified as *matching the median update interval*, not as
  oversampling. A 30 s poll would miss ~92 % of the movement.** (Caveat:
  `last_updated` is SR's own stamp and excludes network lag; the retro
  timeline is an upper bound on what a live poller can observe.)
- ✂ **Centrifugo is the wrong plane for pricing** (and carries no
  probabilities anyway): the `game` namespace runs **history OFF** →
  at-most-once with **no server-side recovery**; the documented recovery path
  is "re-fetch the snapshot and compare `seq`" — i.e. a fetch, which the MM
  hot path forbids. Plus per-user HS256 auth and a user-facing blast radius.
  **Centrifugo shows users the probability; the bus feeds the pricing.**
- ✂ **The SR service's Redis probability keys are unusable** — TTL
  cache-aside artefacts populated only when a user hits the API (3 min single
  / 30 min bulk), refreshed by nothing. Also: the SR service has **no
  internal bus at all** (no NATS, no Redis pub/sub) — Centrifugo HTTP publish
  + Redis writes are its only fan-out.
- ✅ **Poller architecture confirmed** (corroborates the 24-07 decision
  below): poller at the Approved-Data-Sources edge, ~2 s per live game,
  writes MM memory + publishes to the bus; hot path never fetches. Reuse the
  SR client + the **already-entitled, already-working** ID bridge as a
  library. Switch to the **v2 bulk live endpoint** the moment S7 lands (all
  live games in one call — ~0.5 QPS vs ~20 QPS peak per-game on an NCAA
  Saturday). ⚠ v1 has **no** bulk-live endpoint.
- 🔴 **Official results have no source today.** Nothing publishes "game X is
  final" onto any bus, and the §3.1.3 expected→realized swap depends on it.
  Scope it with the same poller — one worker, two publications. → N15.
- 🔴 **Two new risks raised (→ S8, S9):** SR's AF Probabilities docs state
  *"For media use only… prohibited for betting clients"*; and the SR
  service's own latency research puts Probabilities on the **media** tier
  (~5–15 s) which **contradicts Cody's 24-07 report** that it rides the
  betting feed. Both cannot be true, and which holds decides whether users
  can pick the MM off (S4).

## 2026-07-24 — MM build started (`inplay-market-maker`, Python)

> Working mode: step by step with George — each step states what we're
> writing, why, and which spec sections to read. Commits on `main`.

- ✅ **Foundations built + tested (48 tests, ruff + mypy --strict clean):**
  decimal policy rejecting floats at the door (§1.6-3) · the §5.7.3 quantity
  golden fixture reproduced byte-exact · event envelope (§7.1) with immutable
  records, canonical UTC-Z, payload hashing · idempotency keys (§7.3) ·
  append-only fsync'd journal + acceptor (§7.2/§7.4) with dedupe,
  conflict detection and restart recovery · Reference Price formula (§3.1) ·
  probability validation bands (§3.2) · valuation engine wiring.
- ✅ **Replay equality demonstrated on real data** (§10.3): the actual
  Chiefs–Ravens 2024 opener (1,089 SR probability points) priced end-to-end —
  kickoff $2.83 → final whistle $5.00, never outside $0–$5 — then rebuilt
  from the journal alone to an **identical** price stream.
- ✅ **SR adapter is a pure translator** — it never calls SR. Polling belongs
  to a separate (unbuilt) poller; the adapter takes parsed data, so file
  replay and live polling share one proven translation path.
- ⚠ **Two interim mappings, flagged in code:** `last_updated` stands in for
  the provider sequence SR doesn't supply (→ D-2; verified 1,089/1,089
  unique on real data, zero collisions) and `p_tie = 0` treats games as
  tie-impossible (→ S6). One line each to change on ruling.
- ⚠ **Float discipline extends to the border:** SR JSON is parsed with
  `parse_float=str`, so a binary float never exists anywhere in the pipeline.
  The live poller must use the same parse (not `response.json()`).

## 2026-07-24 — v1.3 Build Spec intake · tZERO confirmed · SR probability probe

> Sources: `InPlay_Market_Maker_Build_Specification_v1.3_FINAL.docx` (InPlay,
> "release-final for Novosapien"), mirrored at `standards/MM-build-spec-v1.3.docx`
> + `.html` rendering · live SR API probes (24-07, trial Probabilities key) ·
> codebase research on `inplay-sportradar-service` + `sportradar-futures`.

- ✂ **The v1.3 Consolidated Build Specification is the working baseline.**
  It declares itself the single authoritative engineering spec for MM v1 and
  supersedes the CTS/PTS standards for implementation. Adopted (George, 24-07)
  with one carve-out: the three spec-vs-call conflicts below are NOT silently
  adopted — they go to Edwin/InPlay as written blocking questions (E17–E19).
- ✅ **E11 answered — settlement:** `FSV = realized on-field + realized
  off-field` (§11.3). $5/win, $2.50/tie, $0/loss over the regular season only;
  postseason worthless. Longs receive FSV, shorts pay it, positions zero out.
- ✅ **E12 answered — NCAA in:** 170 securities (32 NFL + 138 NCAA D-I),
  evaluated 24 h/day (§2.5).
- ✅ **E1 answered:** $5.00/win both leagues + **new $2.50 tie value**
  (§3.1.2). InPlay-authored release-final doc = the sign-off.
- ✂ **Off-field redefined** (supersedes the 23-07 "popularity index ~$14–30"
  description): **$2.50 per-game pool split by counted trading volume** (§3.6);
  expected side from the BDI/VMI popularity blend; ceiling = games × $2.50.
  Confirms the sheet decode: NFL cap $85 + $42.50 = **$127.50**.
- ✅ **All pricing numbers landed (E5):** spreads $0.10/$0.20/$0.40 by state,
  levels 3/2/1, sizes 10k/7.5k/5k, skew S=$1.00 · cap M=$0.25 — most marked ▸
  proposed: mechanism mandatory, value pending InPlay approval (§12.2, Ch 14-A).
- ✅ **Skew denominator (E14):** Reference Float = issued − treasury (§4.3).
- ✅ **Venue = tZERO — confirmed by George (24-07)** (spec open item C-1
  answered on our side). The "Matching Engine ICD" is effectively the tZERO
  FIX specs mined 23-07 — C-2/C-3/C-4/C-9 already answered there; message-rate
  limits (C-7 = T2) stay open.
- ✅ **The reconciler is back:** §8.1 mandates venue sync by diffing the target
  book against the confirmed book and issuing minimal instructions — the
  shelved 22-07 reconciler design is now the required shape.
- ✅ **Replay harness first** (§1.6-4). The §5.7.3 SHA-256 golden fixture was
  reproduced locally, byte-exact (VF = 1.2433331614).
- ⚠ **Three conflicts held open — NOT adopted either way (→ E17–E19):**
  1. §5.9 fill replenishment (top up below 50 % after 15 s) vs Edwin's 23-07
     "rest until gone, no top-ups ever".
  2. §3.1.4 2.0 s sweep + 5 s-fresh-is-Current vs Edwin's "~200 ms — a
     second's too long".
  3. §1.5 excludes internally-generated probabilities vs Edwin's 23-07
     "InPlay produces remaining wins internally, weekly" — now with proof the
     spec's D-1 is unsatisfiable as written (see SR probe below).
- ✅ **SR probe results (trial key, 24-07):**
  - The standalone Probabilities product **works on the trial key** (200s) —
    the 403 story was key placement, not entitlement death. S1 downgraded;
    production key/quota still needed.
  - **2-way market only — no tie probability exists** in the product. The spec
    requires P_tie and forbids inferring it (§3.2.2). → S6.
  - **Rolling pricing:** NCAA 70 of ~1,700 games priced today; NFL priced via
    the **date-schedule endpoint** (12 games on 13-09) even though its seasons
    listing is empty. **Full-season Σ GEV(g) is NOT computable from SR
    alone.** Resolution options (→ E19): SR season win totals for the unpriced
    tail (NFL verified; NCAA absent per the 16-07 OC-Futures email), or
    InPlay-internal weekly (Edwin's original model, needs a §1.5 Change
    Order), or both.
  - **Live-bulk endpoint** (all live games, one call) exists in **global AF
    probabilities v2** — 403 on our key; separate product. Product ask → S7:
    v2 entitlement (~200k calls/mo, 0.5 QPS) or v1 quota bump (~2.5M/mo,
    ~20 QPS peak on an NCAA Saturday).
- ✅ **Probability ingestion architecture:** a dedicated MM poller at the
  spec's Approved-Data-Sources edge — reuses the SR client + ID bridge from
  `inplay-sportradar-service` **as a library**, write-through push (Redis +
  bus), never TTL cache-aside; the valuation/quoting hot path never calls SR.
  **Polling rate comes from the freshness bands (~2 s per live game), not the
  decision-cycle rate.** ⚠ The reason originally given here — "SR's number
  only moves per play (~30–40 s)" — is **WRONG and superseded by the 24-07 SR
  ingestion research above**: the measured median update gap is **4 s**. The
  ~2 s conclusion stands; the justification is "matches the median", not
  "oversamples".
- ✅ **Sportradar service facts (code-verified):** full-season schedules +
  results for all 170 teams work today on the core key; game replay works two
  ways (SR playback host streams real recorded games — no auth, real-time —
  and local JSONL fast-replay through the same pipeline). **S5 resolved.**
  Real SR Push (events stream) is itself an unconfirmed add-on entitlement.
- ✅ **Build start (George, 24-07):** begin now against mock + replay
  probability inputs — replay harness → valuation engine → position/quote/
  state engines. Venue sync and live data integrate later.

## 2026-07-23 — MM follow-up call (Edwin + Troy + team) — [[23-07-2026-market-maker-follow-up]]

> Not the planned deep-dive: **E11 (settlement) and E12 (NCAA) were never
> asked** — another MM call expected. George emailing the anchor doc to Edwin.
> Theme: **"really simple to start"** — augment over the next couple of months.

- ✂ **Quote lifecycle overturned — no top-ups, ever.** A partially-filled
  resting order is never refreshed; it rests until completely gone. On a
  price move: cancel the old level, post the **remaining** quantity at the
  new price. After a full fill at an unchanged price: reload at top of book.
  Supersedes the 22-07 amend-in-place recommendation (N12) and the
  top-up-replace mechanics (N10 → resolved).
- ✅ **Replace = cancel + new order at the back of the queue** — confirmed on
  the T0 call and by Troy ("common practice on just about every matching
  engine"). Edwin: **"we don't care about that."** (T8.1 resolved; 35=G's
  only remaining value is message count.)
- ✅ **v1 crossing tolerance (confirmed by George 23-07):** post the new
  quotes without waiting for cancel confirmations; a **momentary self-cross
  during a price adjustment is acceptable** in v1. Edwin: "new orders are
  faster than cancels… on the first iteration, if we have to cross in order
  to make the adjustment in price, I don't care." No cancel-first-wait gap.
- ✅ **Cadence bifurcated by game state:** live games **~200ms per call**
  ("a second's too long") · non-live **every 30–60s** · **earnings windows**
  (Tue NFL / Wed NCAA): call all ~170 symbols for **~5 minutes**. Supersedes
  the flat all-teams-every-cycle framing.
- ✅ **Randomizer = quantities only** (especially top-of-book size, so the
  book doesn't read programmatic). **Price is purely algorithmic** — no
  price randomization. Narrows the 20-07 randomizer decision.
- ✅ **In-game price driver = Sport Radar live win probability, pulled
  directly.** No own event-weight algorithm in v1 ("you don't have to create
  it — you just pull Sport Radar's probability in"). E15 resolved;
  `event trigger weights` not needed v1.
- ✅ **Remaining-season wins produced internally by InPlay, weekly.** SR
  doesn't compute season win probability (futures aren't updated/tradeable);
  Edwin helping automate. E13 resolved.
- ✅ **Off-field = Edwin's popularity index** — ranked attendance/merch/
  popularity, valued **~$14–30 per team** (Dallas ~$30; Carolina/Arizona
  ~$14); **static at the start** and already inside the NFL IPO prices;
  changes with winning + star-player effects. E2 substantially resolved.
- ✅ **The Wednesday data drop:** every Wednesday InPlay delivers the updated
  off-field metric + remaining-game win probabilities; we plug them into the
  algo. New operational cadence.
- ✅ **Betting-feed parity requirement:** our probabilities must not lag
  DraftKings/FanDuel "or we're going to get picked off." Cody owns getting
  the feeds. (New Phase-0 item.)
- ✅ **User wash-trading policy = rulebook + surveillance, not tech (v1):**
  prohibited in the rulebook; order-query on high-volume accounts; removal
  from the event. Troy checking what self-match prevention T0 employs (new
  T-item).
- ✅ **MM is a buyer at every IPO** — when buyers are short / to balance
  shares pushed into the market. Edwin: **"we're going to start with the
  IPO"** — sequencing signal; fuller session promised.
- ✅ **Testing via SR simulation games:** replay a past game in a ~4-hour
  window instead of waiting for preseason.
- ✅ **Edwin sending the original MM simulation Python files** ("functional,
  not a heavy lift") — E4 in motion.

## 2026-07-23 — tZERO Order Entry FIX spec v2.2 read (George + Claude, validated)

**Adopted — venue facts from the OE spec itself:**

- ✅ **FIX 4.2 only** (`BeginString` always FIX.4.2). Limit orders only
  (OrdType=2 is the sole value) — reconfirms 22-07. TIF = Day / GTC / GTD;
  GTC/GTD require `RoutingInst(9303)=DNRI`. Price field to 4 decimals (field
  precision — tick policy stays $0.01).
- ✅ **Order Replace Request (35=G) exists.** Symbol AND **Side must match the
  original order** — side is immutable; a bid can never become an offer.
- ✅ **Fills survive the replace chain:** Order Replaced carries `CumQty` +
  `AvgPx` forward. `OrderQty` on a replace = the new **total** for the chain;
  `LeavesQty = OrderQty − CumQty`. (Top-up to X resting = replace with
  `OrderQty = CumQty + X`.)
- ✅ **The fill-vs-cancel race has a defined reject:** Cancel/Replace Request
  Reject with `CxlRejReason 0 = "Too Late To Cancel"` (1 = unknown order).
- ✅ **Every execution report can carry `PosSIZ` / `PosCOST` / `PosRpnl` /
  `PosUpnl`** — venue-authoritative position + P&L per fill. Fields optional,
  so: our own event-sourced inventory stays primary; venue values used as a
  free cross-check (disagreement = bug alarm) + ops-UI P&L source.
- ✅ **No iceberg orders** — `MinQty`/`MaxFloor` "not supported on tZERO
  Matching Engine": displayed size = real size, always.
- ✅ **No `ExecInst`** — no post-only, no self-trade prevention at order
  entry. Our publish sequencing is the ONLY protection against executing
  against our own stale quotes.
- ✅ **Unsolicited cancels exist** (Order Cancelled has an unsolicited
  variant) — the reconciler must absorb venue-initiated cancels.
- ✅ **Execution Busted (ExecType=H)** confirmed at OE level; **Execution
  Corrected (ExecType=G)** also exists — a past fill's price/qty can be
  re-stated (either direction). Both reprocess through the same
  fill-reconciliation path. **Done for Day** message exists.
- ✅ `ClOrdID` ≤ 20 chars, **no leading zeroes**. Cancel/Replace *Pending*
  acks suppressed by default (request → silence → Replaced/Rejected).

**Adopted — our design consequences (validated 23-07):**

- ✅ Reconciler **never sends a replace with `OrderQty ≤ CumQty`** — where a
  shrink would go below what's filled, cancel + create fresh instead.
- ✅ Hot path is **push-only, memory-only**: FIX execution reports + bus RP
  push + in-memory state; per-cycle snapshot-at-start (atomic copy, live
  state keeps mutating, mid-cycle arrivals coalesce to next cycle); the
  append-only event log is disk-based, background-flushed, never blocks a
  cycle.
- ✅ **MM event log fully isolated from the production app database**
  (George, 23-07). It is not a transactional DB at all: one local append per
  cycle (few KB, sequential) → shipped asynchronously (log stream / object
  storage) → analysis store built from it later only if needed. The app never
  reads MM cycle records; the MM reads the log only at boot (state snapshot +
  tail replay for fast recovery). MM disk/log-shipping failure must never be
  able to touch the app (failure-domain isolation).

## 2026-07-22 — Share capacity + working process

- ✅ **Per team: 5,000,000 shares available for LONGS and 5,000,000 available
  for SHORTS** (learned 21-07, recorded by George 22-07). Supersedes the
  sheet's 875k float basis for capacity purposes; consistent with the IPO
  module's 5M float. ⚠ Consequences: the QA 1,000-share short reserve is a
  test config, not the product number; and **inventory-as-%-of-float maths
  (the skew gain λ) must be re-based** — 5M base vs 875k changes the
  effective gain ~5.7×. See [[market-maker/parameters]].
- ✅ **Working process established:** [[market-maker/working-guide]] +
  `sessions/` log + CLAUDE.md rule — any MM work starts by reading the guide,
  every session ends with a session note + working-doc updates.

## 2026-07-22 — Platform reality map (`trading-architecture.md` v1.0, live-verified)

> **Filter applied (George, 22-07): platform + venue facts from this doc are
> adopted as fact. Anything about the MM's own design (the `sdmm.py`
> prototype, its parameters, the "decided" 200 ms full-replace cadence,
> MM-as-user-account identity, the `gateway.orders.mm.*` seam) is treated as
> SUGGESTION ONLY — we design the MM from scratch. Those items live in
> open-questions as inputs, not here as decisions.**

**Adopted — venue facts (all test-verified, dates in source doc):**
- ✅ **Universe is 170 symbols: 32 NFL + 138 NCAA** (tickers `IPTC****`) —
  supersedes the standards' 163/131 count everywhere in this component.
- ✅ **tZERO has NO quote/mass-quote interface** — FIX schema is order-based
  only (D/F/G/8/9). Any MM is an order-based MM shaping the book with resting
  limit orders. (Closes T7.)
- ✅ **Limit orders only** (gateway hardcodes 40=2); **TIF = DAY / GTC / GTD
  only** — IOC and FOK do not exist in the venue spec.
- ✅ **No venue price band by default** — $0.01 and $1,000,000 limits both
  accepted verbatim. BUT the OMS Account/Position spec exposes a per-account
  collar (`LmtCents` + enforcement toggles) and wash-trade blocking — asks
  filed to enable on user accounts. Self-collar remains mandatory.
- ✅ **Shorts verified** (side=5): 1,000-share/security reserve ceiling,
  pre-trade enforced; stock-loan fee charged per short execution (absolute $,
  delivery not yet live on tZERO's side).
- ✅ **Session behaviour**: daily sequence reset 23:59 ET; resting DAY orders
  SURVIVE disconnects (cancel-on-disconnect empirically OFF) — a dead MM's
  stale quotes rest until end of day unless actively cancelled.
- ✅ **MM account mechanics exist in the OMS spec**: `UAAR` (create, with
  `MMType` + initial buying power), `UEPR` (seed per-symbol inventory),
  `UBT` (cash transfers). Entitlement ask filed. (T1 mechanism in hand.)
- ✅ **Our-side throughput is a non-issue**: Go gateway hot path measured
  ~460k orders/s/core. Binding constraint = tZERO's per-account
  `MaxOrdRate` + sustained-load authorization (ask filed). (Reframes T2.)

**Adopted — platform facts:**
- ✅ FIX gateway (Go) is live + battle-tested; two sessions (OE+MD); 170
  symbols subscribed; only 6 quoted two-sided in QA today.
- ✅ **Gateway gap #1: no outbound cancel (35=F) or cancel/replace (35=G)
  exists.** Cancel-system build committed 22-07 (owner Hasan) — includes an
  MM intake namespace, dead-man switch, Redis open-order index. Everything
  MM-shaped queues behind this build.
- ✅ Two trading planes: primary/IPO (internal, no venue) vs secondary (tZERO
  ATS). **The MM lives on the secondary plane only** — IPO fills never touch
  it.

**Adopted — economics (pending Edwin sign-off):**
- ✅ The client's real NFL IPO sheet exists and its economics decode to
  **`ESV = OffField + $5.00 × ExpectedWins`** — additive, arithmetic verified
  across all 32 rows. So **$/win = $5.00** (provisional). Float =
  **875,000/team**; price cap **$127.50**, floor 1 tick.
- ⚠ **Settlement definition** (what actually pays at season end) elevated to
  the single most important Edwin question.
- ⚠ **NCAA secondary-market scope for season 1 is OPEN** — the sheet covers
  32 of 170; NFL-only secondary is a live possibility.

**Noted as suggestions only (NOT adopted — MM is built from scratch):**
- The `sdmm.py` Phase-1 prototype and its Avellaneda-Stoikov formulation.
- Its proposed parameters (2-tick half-spread, λ 1500¢/100% float, 3
  levels/side, 6,000 sh/side, 2^k weights).
- The 200 ms full-per-team-cancel-replace cadence framing.
- MM identity as an individual user account.
- The `gateway.orders.mm.*` intake namespace (the platform's *offered* seam —
  our design may use it, but it doesn't bind the MM's architecture).

## 2026-07-20 — Market-maker Q&A (Edwin + Troy) — [[20-07-2026-touchdown]]

- ✅ **Scope: Novosapien builds CTS-001 and CTS-002** as well as PTS-001.
  George asked build-or-consume directly; Edwin: "We will build them." The
  matching engine / order book remain T0's.
- ✅ **Valuation formula given** (fills CTS-001's missing Section 3):
  `price = P(win this game)×$/win + E[remaining wins]×$/win + off-field`.
  Sport Radar live win probabilities are the input.
- ✂ **Unlimited capital — PTS-001 Ch 5 (Portfolio Allocation Engine)
  descoped.** Edwin: "The market maker will never have a limit on what it can
  do on capital"; buying power set to ~$100M–$100B. No finite pool, no
  zero-sum allocation. Per-team displayed-size config survives.
- ✅ **MM entity = ordinary participant + unlimited buying power + short-locate
  exemption.** T0 to stand up the synthetic MM entity in QA (asked via the new
  Tue/Thu T0 tech calls).
- ✅ **Limit orders only, including for the MM** — aggression via pricing
  through levels (bid 11 on a 7-at-8 market to sweep to 10).
- ✅ **Reference Price = the mid** between best bid and best ask.
- ✅ **Quoting = base spread ± per-side offsets around RP, with inventory
  skew** (long → offer drops toward RP to offload) — matches PTS-001 Ch 6.
- ✅ **Randomizer on quoted sizes** + occasional randomized **aggressive
  orders** that deliberately move price to exit inventory. ⚠ The aggressive
  behaviour goes beyond PTS-001's passive quoting — needs explicit bounds.
- ✅ **Cadence: cancel-replace ~5–10×/sec** intragame ("wipe the book and
  replace it"), plus event-triggered recompute. George's 200ms-baseline +
  event-trigger model approved by Troy for intragame.
- ✅ **Three liquidity sessions** — in-game / around-game / overnight
  (overnight deliberately wide, ~$2.5–5 spreads).
- ✅ **Markets truly isolated intragame**; each game a pairs trade; no
  rankings/tiebreaker effects; cross-game effects only between games.
- ✅ **Price band (~30%) + trade busting with T0** required for orderly
  markets — policy sessions "over the next couple of days."
- ✅ **NEW BUILD: synthetic market order** (app-side price-through) — before
  the first NFL game. Troy to help with logic. "A market order means whatever
  you get, you get" — no user-facing bounds.
- ✅ **NEW BUILD: MM ops desktop UI** — params, order lookup, positions, P&L;
  Kevin likely operates; sequenced last; first desktop surface of the app.
- ✅ **Priorities: challenge = stability first, profit last. Production =
  profit first** (if InPlay becomes its own MM — Edwin would open another
  company for it).
- ✅ **Terminology: "market state"** is Edwin's word for the condition/profile
  layer (not "market conditions").
- ⚠ **The standards are context, not constitution** — Edwin: "I meant it for
  Claude to read." Season-1 conformance bar to be signed off explicitly
  (Thursday 23-07).
- ✅ **T0 cadence: two tech calls/week (Tue + Thu)** from this week.
- ✅ **Deep-dive booked: Thursday 23-07, 3–4pm London.**

## 2026-07-15 / 17-07 — Standups — [[15-07-2026-touchdown]] · [[17-07-2026-touchdown]]

- ✅ **IPO fill guarantee / float warehousing:** the MM warehouses unsold IPO
  float in max clips (~50k), guaranteeing ~35% (possibly up to 50%) of every
  float — the straw-buyer mechanism. (15-07)
- ✅ **Reference-price blend** (on-field probability + off-field) named as the
  price driver; **load-balancing algo vs market-making algo** distinction
  raised — boundary still unclear. (17-07)
- ✅ Randomized, non-uniform quote sizes flagged (book must not read as a
  machine). (17-07)

## 2026-07-17 (commit) — Standards received

- ✅ CTS-001 / CTS-002 / PTS-001 master drafts (PDFs dated 01–02 Jul) mirrored
  into [[standards/README|standards/]] via `feat/technical-standards`.
- ⚠ CTS-001's Section 3 (valuation mathematics) absent from the converted
  copy — referenced throughout, file ends at §2.33.

## 2026-07-21 — Structure decisions (this vault)

- ✅ Component named **market-maker**, umbrella over all three standards +
  new build items, with custom `systems/` + working-docs structure (this
  folder) instead of the standard component/sub-component pattern.
- ✅ Clarified I/O direction of the profile layer (condition/session in →
  spread/depth/refresh targets out) and the three-role bust model
  (participant / venue / operator) — see
  [[market-maker/systems/market-supervision]].
