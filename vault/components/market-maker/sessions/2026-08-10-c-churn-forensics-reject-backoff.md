---
description: "Testing audit, the replace-churn forensics (not a bug: 2x ack pairs + fill-driven rotation), and the C4 reject-backoff built as MM PR #13"
---

# 2026-08-10c — the testing audit, the churn dissolved, the backoff built

> **Type:** analysis + build session. George + Claude.
> **Repo state at close:** MM PR #13 (`fix/reject-backoff`) OPEN off main,
> 618 tests, ruff + mypy-strict green — built in a git WORKTREE
> (`../inplay-market-maker-backoff`) because the main checkout carries
> another session's uncommitted SNT work on
> `feat/snt-1-float-and-sell-gate`, untouched.
> **Vault:** this branch already carried another session's uncommitted
> changes; this session's doc edits sit beside them, all uncommitted.

## What we did

1. **Testing audit** (George: "the current way we test is not very
   production-like"). Mapped the five current avenues (unit suite ·
   one-game replay · docker rig · static supervised runs with the
   poker · one-off probes) against the production shape, and ranked
   six additions — A2-on-the-rig first, maker+taker joint rig run,
   170-book scale run, the `.TEST` dress rehearsal, a failure-drill
   program with soak/divergence detection, a CI/CD gate.
2. **Reviewed the open error list**; George picked the unexplained
   replace churn. Copied `supervised5` + `supervised9` journals OFF the
   MM VM (read-only; scratchpad) and ran four forensic passes.
3. **The churn dissolved — NOT a bug.** Recorded in build/next.md:
   - Every ORDER_REPLACED ack is journalled **exactly twice** (same
     execution id, <50 ms apart, different gateway message uuid) — the
     adapter's own documented `[ack-key]`/`[replace-pair]` choice. All
     counters were 2× inflated: 35,982 acks = 18,070 real replaces.
     Fills/accepts/cancels are NOT duplicated — position safe.
   - The real replaces track the poker minute-by-minute (~150 fills/min
     ↔ ~250 replaces/min, 72 active minutes, then 8+ h of silence once
     the poker stopped). Fill → skew → one-tick rotation → replace.
     The "40/min for 15 h with the poker stopped" reading divided
     cumulative counters by uptime.
   - The genuine pathology: **8 cancel ids × 18–124 UNKNOWN ORDER
     rejects in 8 min** on the diverged supervised5 boot (09:45–09:53)
     — exactly C4 + R-D05.
4. **Built the C4 reject-backoff** (MM PR #13): `mm/venue/backoff.py` —
   submit rejects back off per (security, side, price), cancel/replace
   rejects per resting order; min(2 s × 2^(n-1), 60 s), success-only
   reset; the reconciler's diff skips suppressed prices/targets;
   expiry priced with the triggering event's own time (replay-safe);
   state rides the checkpoint (**schema 3 → 4**). 9 new tests.
5. **Docs:** test-plan C4 → 🔄 built/live-run-owed (+ frontmatter
   description added) · requirements R-R03 🔴 → 🟡 · three parameter
   rows (🟡 ours) · build/venue.md backoff section · build/next.md
   churn item closed + backoff marked DONE.

## What we learned

- **Halve any ack-based statistic** before believing it — the
  replace-pair delivery doubles replace confirms and most
  cancel-rejects. The 08-09 churn scare was born from unhalved
  cumulative counters divided by uptime.
- The book visibly rotates a tick on every noise clip (fill → skew →
  rotation). Designed behaviour; whether Edwin wants it calmer is an
  E31-adjacent, book-visible dial — his remit.
- **The engine is RUNNING again** — another session started
  `supervised9` at 18:54. ✂ **Corrected 08-11:** the launcher
  (`run_supervised9.sh`) exports **CFG-0008** — the rule WAS followed.
  The journal envelopes stamp `CFG-0001` because the ack-adapter path
  stamps a default rather than the settings' version — a cosmetic
  stamping inconsistency worth a small fix, not a rule breach.
- **Seven real fills hit the MM's asks tonight** (EAGL×5, PATR, COWB)
  with no poker running — an outside counterparty trades the QA books.
  All seven arrived with empty payloads (qty/price None, the known
  gateway quirk); whether the position engine applies such fills
  correctly is worth a check.

## What went wrong / got stuck

- Nothing blocking. The one design wrinkle: suppressing a price can
  thin a side, but the suppressed level was rejecting anyway — nothing
  rested either way (noted in the reconciler's `[backoff-diff]`).

## Decisions made (ours, recorded)

- The replace churn is closed as NOT-A-BUG (three explained parts) —
  build/next.md 08-10c entry is the record.
- Backoff values 2 s / ×2 / 60 s filed 🟡 OURS in parameters.

## Questions opened

- ~~Does the position engine apply an empty-payload fill correctly?~~
  **RESOLVED same session — a false alarm of ours.** The seven fills
  carry full payloads (qty/price/leaves/cum); the "None" reading came
  from this session's own analysis script using wrong field names.
  Checked while there: a genuinely field-less fill is POISON in the
  drain (counted, skipped loudly, engine survives); only deliberate
  alarms (busts, unmapped fills) stay fatal. Nothing to fix.
- Who/what runs supervised9 on CFG-0001, and should it be restarted
  under the config-version rule? (Coordinate — cross-session.)
- The seven fills are real outside SELL-side takes: ~31,000 EAGL +
  10,000 PATR + 100 COWB bought FROM the MM's asks (~$3.2M notional).
  Who is the counterparty on the QA books tonight?

## Late addition 5 (08-11, evening) — ⭐ MAKER + TAKER LIVE TOGETHER: the incident chain, the LIVE burst, and the share-perfect validation

The first true joint session on the real venue, on separate accounts.
The taker's "not working" unwound into a chain of designed protections
plus one env relic, each now a recorded rule (MM repo CLAUDE.md, PR #20):

- **Boots HALTED after any journalled halt** — resume is explicit.
- **T-S05 fired on ALL FIVE books** — real venue-vs-journal gaps from
  one bad first stop (plain kill, not halt-before-stop: in-flight
  orders filled with nobody to journal them). Recovery lever:
  `SNT_FLOAT_OVERRIDES` per book (float = venue − journalled drift,
  both on the HALT line). Final floats: COWB 4959 · STEE 5256 ·
  EAGL 5132 · GIAN 4737 · PATR 4836.
- **Same config version ⇒ same RNG draws** — every resume re-sold the
  same COWB clip until the version bumped. Bump EVERY restart.
- **`SNT_MINUTES=15`** lurked in the inherited env — every "mystery
  exit" was the QA run window. Now 0 (continuous).
- Ops footguns recorded: remote kill patterns self-match (match ps
  FIELDS); control commands need the repo cwd (`.venv` is relative).

**The LIVE-intensity test (George's ask, reverted after):** state
pinned LIVE by control command → **20 fills/90 s across all five
books**, zero halts, zero rejects — the game-day profile demonstrated
on the real venue. Reverted to PRE_KICKOFF by the same lever.

**Journal validation — every expectation MET:** 198 sends → 198 fills
(100%, zero rejects) · direction 49.5% buys (the 50/50 design) · clip
mean 48 vs Edwin's smoke-tested ~44 · crossing cost mean 2.3¢, max 4¢
(inside the 3-tick cap) · drift within the 1,500 cap everywhere ·
⭐ **the maker's and taker's journals mirror SHARE-FOR-SHARE on all
ten (book, side) totals** — two event-sourced journals, two processes,
two accounts, in exact agreement. Also proves 100% of taker flow met
the maker (the E33 house-to-house fact, measured).

**State at close:** maker `supervised12` (CFG-0011, ~7 h up, six books,
bus-wired) · taker `snt-0811.env` CFG-0006, continuous, own account +
`snt-taker` NATS user, PRE_KICKOFF pin. JETS still reference-blocked
(Rob). ⚠ The taker env's float overrides are load-bearing state — do
not regenerate the env without carrying them.

**George's next-session plan (ruled, in order):**
1. **Full-book test** — seed ALL current tickers incl. the ten `.TEST`
   (they exist in the gateway's 180-symbol config) to the MM via
   position-transfer (ledger discipline: not idempotent, T-prefix ids),
   then run the MM on the full book: the B3 load test, the LmtPerc
   empty-book experiment, and the N31 fsync measurement in one.
2. **The synthetic game day** — a scripted probability stream for two
   quoted books over the production bus (kickoff → swings → halftime →
   final): A2 stage 2 mechanics + A3/A4/A5 transitions + taker at ×75,
   the 13 Aug shape with controlled data.
3. **C2** — checkpoint-resume on supervised12's real journal.
4. Externals to chase in parallel: T17 tickers · Rob (STX reseeder,
   JETS reference, T14/T15/T16) · Hasan (B2) · the Edwin round.

## Late addition 4 (08-11, afternoon) — ⭐ the stale quotes are a VENUE-SIDE RESEEDER; books cleared

George kept seeing small orders after the engine + taker stopped and
the dead-man swept. Three layers found:

1. **The depth feed lied** — `market.book` frames showed every book
   empty while the venue held ladders (the 08-10 MD-rebuild flaw
   again). The gateway's `POST /md/probe` full-book snapshot was the
   truth instrument; `POST /md/book-resubscribe` is the heal.
2. **The truth: 49 stale levels across the six books** — descending
   10-cent ladders, 60–150 shares/level, at the OLD test-quote price
   zones (COWB 53.x bids · STEE 38.5 bids · JETS 18.0/18.3 both sides
   · EAGL 146+ asks · PATR 112.7+ asks · GIAN 68.6+ asks). ⭐ **Entry
   stamps: placed TODAY 10:16Z, originator 275=STX** — the quotes
   eaten on 08-07e CAME BACK. A QA-venue test-quote seeder reseeds
   them; eating is whack-a-mole until tZERO disables it → **Rob ask**.
3. **All 49 eaten at their own prices** from the MM account (engine
   stopped — no adoption risk; zero rejects; the residual per-book
   probe entry is the last-trade print, not an order). **Verified: 0
   resting levels on all populated books + BILL · 0 live bid/offer in
   the gateway's Redis quote cache** — which DOES self-clear now
   (174/180 entries were bare shells; the 08-07 "never clears" note is
   stale for quotes). MM positions moved slightly by the eats (QA
   account, seeded 100k/ticker).

New Rob asks: (a) disable/clear the STX test-quote reseeder on the
IPTC* books; (b) what is originator STX, and on what schedule does it
reseed (today's batch: 10:16Z)?

## Late addition 3 — A2 stage 1 BUILT and PASSED (smoke)

The session continued into the top-ranked testing avenue. The rig was
revived (mm-nats + mm-gateway were in fact both up; the earlier "gone"
reading was a truncated listing) and `scripts/a2_replay_drill.py` was
built (committed to MM PR #13): the full 1,089-reading Chiefs–Ravens
capture over the rig JetStream at recorded-pace ÷ speed, re-offers
every 2 s per the live publisher's contract, twelve checks at close.
**120× smoke: 12/12 PASS** after three harness iterations. The 10×
recorded run was in flight at session close — see test-plan A2.

Findings worth keeping (all recorded in test-plan A2):

- **The E17 remnant is fill-free** — monotonicity 50–100% from
  rest-until-gone generation mixing alone, on a venue with zero fills.
  Strong evidence for the Edwin round: the lifecycle, not fill noise.
- **Through-venue BYTE replay equality is not an invariant today**:
  `stand_the_book` is a deliberate un-journalled operator action, and
  an order admitted from an ack carries the gateway's price string
  ("77.6" vs "77.60"). The deterministic core (acceptor + valuation +
  position) IS byte-identical on full replay, and the settled venue
  book replays identically by VALUE. Both residues named in the drill;
  closable (journal the standing cycle; normalize admitted prices) if
  byte equality through the venue leg is ever wanted.
- **The rig gateway remembers ClOrdIDs for its whole process life** —
  the duplicate-id lesson (07-08f), rig edition; the drill mints a
  fresh `MM_CONFIG_VERSION` per run.
- Harness lessons: freeze state only AFTER the runtime stops (sweeps
  keep journalling); belief `status` is sweep-aged and path-dependent;
  `wire_messages()` consumes its raw dict.

## Next

1. **Merge PR #11** (`fix/cancel-reject-drain`) and **PR #13**
   (`fix/reject-backoff` — now also carries the A2 drill) — they
   compose: #11 stops foreign cancel-rejects killing the engine, #13
   stops our own reject loops.
2. ~~Read the A2 10× result~~ **DONE (00:4x, 08-11): 12/12 PASS at
   10× too** — filed in test-plan A2. A3/A4/A5/C3 ride the same
   harness next (needs per-reading status reconstruction for the
   kickoff/final transitions).
3. **Run C4's live half** after deploy: recreate a rejecting book,
   confirm the rate follows the schedule (halve the ack counts).
4. **The maker + taker joint rig run** — the next untested avenue;
   SNT-1 vs the MM on the same loopback book.
5. Commit the vault docs once the other session's uncommitted work is
   reconciled.
6. ➕ **08-11: the publisher branch is PUSHED and PR'd** — sportradar
   service **PR #8** (`feat/mm-probability-publisher` → `dev`, 577
   tests green, based exactly on dev's tip). George's check found no
   PR existed; the build was done 06-08 but never left the laptop.
   Three MM-adjacent PRs await review: MM #11, MM #13, service #8.
7. ➕ **08-11, later: the publisher is DEPLOYED to production AND
   testing** — ⭐ George overrode the Hasan freeze ("treat Hasan as
   not doing anything, incorporate his changes"). The full sequence:
   PR #8 → dev · dev→main release PR #10 (carrying Hasan's six dev
   fixes) · terraform worker pools (PR #9, repair #12, align #13) ·
   testing auto-deploy + production. Findings on the way, recorded in
   [[market-maker/build/infrastructure]]: Hasan had PRE-PROVISIONED
   the whole path (firewall 2024, the `sportradar` NATS user with
   `sr.probabilities.>` + JS grants, `snt-taker-nats-password` for the
   taker too); the probabilities entitlement is PRODUCTION now (probed
   200 — the code default still said trial, whose quota was half-burned;
   `PROBABILITIES_ACCESS_LEVEL=production` set); the publisher's lease
   fence is still `AlwaysOwns` (C15 unbuilt) so both pools run ONE
   instance. ⚠ **A parallel session worked the same repo throughout**
   — it double-merged main→dev (breaking the terraform, repaired in
   #12), hand-created the prod pool after its 12:07 dispatch failed
   (imported into terraform state), and raced the env fix (merged).
   Cross-session coordination cost real time again — the 08-10
   lesson's repo-side twin. **A2 stage 2's publisher gate is CLOSED**;
   what remains for stage 2 is the MM-side go-live ingestion switch.
   The testing pool is left at 1 instance (harmless duplicate
   readings, dedup-covered) — scale to 0 or keep for the 13 Aug
   rehearsal, George's call.
8. ➕ **08-11, later still: ⭐ LIVE poll ruled 500 ms (George)** —
   "an unchanged successful fetch is not no-data, it is confirmation;
   2 s is not good enough for updating the quotes." Matches Edwin's
   03-08 number; supersedes the 2 s evidenced interim. Applied to BOTH
   deployed publisher pools (`MMPUB_POLL_LIVE_S=0.5`, service PR #15;
   ⚠ PR #14 was a mislabelled fmt-only merge after a failed scripted
   edit — noted in #15's description). **E18 narrows**: the poll-rate
   half is now ruled; what remains is the reaction-bound half — the
   engine's 1 s tick is the next limiter in the chain (poll 0.5 s →
   publish → tick ≤ 1 s → cycle ≈ worst ~1.5 s reading-to-quote), and
   the 04-08 "build capable, choose the rate later" moment is due at
   the ingestion-switch QA run. ⚠ The IN-ENGINE poller still carries
   2 s — retire it (the switch) before any live game, or bump it.
10. ➕ **08-11, close: ⭐ THE INGESTION SWITCH IS DEPLOYED AND PROVEN.**
    MM PR #17 (`MM_READINGS=bus`) merged after the drill gate passed
    **11/11 at the 500 ms cadence** — the gate run surfaced and
    resolved three things: the rig gateway ran the stale 50 msg/s
    governor (now production-true 5000/2000, in parameters); the
    end-of-replay book emptying is the **E38 silence-suspension
    working correctly** (harness now freezes before the 20 s mark);
    and a benign ~1.2/s cancel-vs-ack race at 500 ms (self-corrects,
    journalled; the harness gates only non-race rejects, and doubles
    must persist 2 samples). **supervised10 (CFG-0009) runs on the VM**
    — six QA books, bus-wired, carrying the backoff + drain + 500 ms
    cadence; deployed by git bundle (the VM repo has no GitHub
    remote). The NATS `market-maker` user gained SR_PROBABILITIES
    consumer grants (conf backed up). **Pipe proven**: one captured
    reading published on the production JetStream reached the engine
    (`readings=1`, journalled; no orders — CHIE/RAVE not quoted).
    Stream otherwise empty — no games today. ✂ Also corrected: the
    supervised9 CFG note (the launcher DID export CFG-0008; the
    journal stamped the adapter default — stamp fix in PR #17).
    ⚠ Residue: `supervised10.log` line 1 prints the NATS URL with the
    credential (pre-existing in the launcher pattern) — scrub when
    the systemd unit lands. A2 stage 2 now needs only a real game.
9. ➕ **08-11, final: ⭐ the quote cadence ruled and BUILT — new orders
   every 500 ms in-game, changed or not (MM PR #16).** George chose the
   timer reading explicitly over the reaction-bound reading when both
   were put to him. Tick 0.5 s · sweep 0.5 s (✂ §3.1.4) · LIVE dwell
   0–0 (✂ Edwin's 3–12 s) · `_timer_due` publishes an immaterial LIVE
   book after 500 ms; non-live keeps the §5.8 gate (proven at the same
   offset). R-Q03 ✎ (requirements addendum); rest-until-gone untouched.
   672 tests. **E18 is closed on our side** — Edwin gets the dwell
   collapse as a flag, not a question. ⚠ N31 group commit becomes
   REQUIRED at NCAA-Saturday scale. Full record: decisions 2026-08-11.
