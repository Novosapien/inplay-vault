---
description: "Running log of distilled MM understanding — why SNT-1 exists, the rest-until-gone v1 lifecycle, hot-path and event-log design, and the Edwin remit line"
---

# Market Maker — Learnings

> **Component:** [[market-maker/market-maker]]
> **Purpose:** A running log of things we actually *understood* while working —
> concepts that clicked, traps caught, intuitions corrected. This is neither
> decisions ([[market-maker/decisions]]) nor questions
> ([[market-maker/open-questions]]) — it's understanding, kept so it doesn't
> have to be re-derived. Newest first. Add to it every session.

---

## 2026-08-19 — a library is an assumption, and a corpus can carry a fault

Gate 0-b ran for the first time and found four defects. Three lessons transfer.

**A library is an assumption until you test its edges.** We chose `apd` because
it is Go's decimal library. We then found two defects in it. The first: `Exp`
returns **zero** when `|x|` is above 22,977, where Python returns the true
value. The second: `apd` cannot hold any exponent past ±100000, where Python
reaches ±999999. Neither defect appears in normal use. Both appear on the real
corpus. ⭐ The rule: test a library at the edge of the domain the work actually
reaches, not at the middle.

**A corpus can carry a fault that looks like an engine fault.** The a2 journal
spans nearly two years, because its readings carry the 2024 game's timestamps
and its venue events carry the 2026 replay's. That gap forced a number no live
engine can produce. The port looked wrong. The corpus was wrong. ⭐ Ask of a
failing comparison: can the live machine even reach this input?

**A zero value is a decision you did not make.** `ConditionInputs` carries two
fields for unbuilt chapters. Their healthy values are `true` and `Normal`. Go's
zero values are `false` and empty. A struct literal chose the unhealthy values
silently, and every book suspended. The constructor existed to prevent this.
⭐ The rule: where a type has a constructor, the constructor is the contract.

**A near-correct result is worse than a wrong one.** The fold hardcoded the
config version, which seeds every §5.7.3 draw. Every price that needs no draw
stayed right. Every drawn price went wrong. A result that is mostly right reads
as a small bug and hides a systematic one.

## 2026-08-17b — what is running, and what is watching it, are both things you must check rather than assume

- **⭐ `systemctl list-units` is not an inventory of what is running.** The
  maker engine was invisible to it all weekend because it is not a unit —
  a bare `python -m mm.runtime`, PPID 1, orphaned from a `screen` login
  session. This session told George "snt-1 is the only trading unit on the
  VM" while judging whether a restart was safe. True as stated, wrong as
  understood, and only caught because George said "I swear the maker and
  the taker are on the same VM". Use `ps -eo pid,ppid,etime,cmd` before
  believing any VM inventory, and treat "no unit" as a finding rather than
  an absence.
- **⭐ An alert policy named after a machine is not watching that machine.**
  `VM root disk > 80% used (fix-gateway, market-maker, nats)` had claimed
  the market-maker VM since it was written. It filters
  `agent.googleapis.com/*`, that VM had no ops agent, and so it watched
  nothing there — through the 15-08 incident where a full disk took down
  both FIX sessions. **Verify the series exists, not that the policy
  exists.** One `timeSeries` query per policy would have caught it.
- **Make silence page.** The whole 50-hour outage was an absence: the
  signal was published once a second and rendered in the panel, and
  nothing turned it into a noise. Any checker built to fix that must
  itself fire when IT goes quiet — `EVALUATION_MISSING_DATA_ACTIVE`, not
  just a threshold — or it recreates the trap one level up.
- **An untested alert is not an alert.** Prove it with a synthetic metric
  value rather than by breaking the real thing: 11 minutes of injected
  `halted=1` against a 5-minute threshold proved the policy without
  stopping a trading bot. Drop the other humans off the policy first so a
  drill does not page them.
- **A monitor should not hold a trading identity.** The first cut reused
  the taker's own NATS credential and its env files. That couples the
  monitor to the thing it monitors — the taker's env is rewritten during
  every recovery ceremony — and hands read-write trading rights to a
  process that only needs to read two subjects.
- **Private Google Access is not internet access.** The MM VM reaches
  `*.googleapis.com` (so writing metrics works) but has no external IP and
  is in none of the three Cloud NATs, so `dl.google.com` simply hangs for
  300 s. Side-load the `.deb` over `scp`; do not "fix" it by giving a
  trading VM general egress.

---

## 2026-08-17 — a rate is not a lag, and a latency needs its denominator

- **⭐ A latency figure without its message count is not a measurement.**
  The 33-hour halt was blamed on "the gateway running 17–27 s behind"
  after the rate change. That number came from 18 samples inside
  08:15:3x — a minute carrying **36 messages**, because the FIX session
  was down. It measures the age of a post-outage flush. The same metric
  in a normal 6,200-message minute reads **0.02 s**. Bucket lag and
  volume together, per minute, or the number will describe an outage and
  be read as a load level.
- **⭐ "Traffic collapsed" and "traffic congested" look the same in a lag
  chart and opposite in a rate chart.** The tell that 08:13 was a session
  break rather than overload: **our own outbound orders fell from ~740 to
  2 per minute**. Load does not stop us sending. Always check both
  directions before blaming your own throughput.
- **The cheapest possible check on a data-loss claim: count both sides.**
  Taker fills logged per hour against fills on the FIX wire per hour —
  two `awk` passes — settled a 33-hour argument at **230,841 of 230,847,
  0.0026%**. It should have been the FIRST measurement taken, not the
  last, because it bounds the whole problem before any theory is built.
- **⚠ `BOOT REBASE` lines are not a damage count.** On a fresh journal
  every one prints `journal=` equal to that book's `SNT_FLOAT_OVERRIDES`
  seed, so a book that simply traded overnight produces a large,
  alarming-looking difference. All 177 matched the override exactly on
  17-08. This session read 162 of them as evidence of widespread lost
  fills, said so, then had to withdraw it — the same class of error as
  the diagnosis it was correcting.
- **The venue's daily session roll (03:59–04:01Z) is graceful; an
  unplanned break is not.** The roll cost zero fills on 16-08. The
  unplanned break cost four and a 50-hour outage. The difference is the
  `ResendRequest` flush, where fills arrive under cancels that were
  registered minutes earlier.
- **Retention decides whether the next incident is observed or
  reconstructed.** The gateway's app log for 16-08 aged out of journald
  before anyone read it, and the FIX event log kept only the tail of the
  resend. Everything about the discard path is therefore inference. Fix
  retention BEFORE the fix that needs it.

---

## 2026-08-15d — the measurement is an artefact too, and it can lie quietly

- **⭐ Assert on the FINGERPRINT, not on the timings.** CB4 spent a night
  on rig arms that all loaded the same unfixed engine. Every arm
  completed, printed a summary, and produced numbers of a believable
  magnitude — for a tree nobody was testing. The tell would have been
  free: the change under test should leave a visible artefact, so assert
  on THAT. CB2 could prove its own A/B was real because its ON arm made
  24,144 converger passes against 7,642 — a number the OFF build cannot
  produce. CB4 had no such control, which is exactly why the wrong result
  looked normal for hours. **Where a change should leave a fingerprint,
  check the fingerprint; timings alone cannot tell you what ran.**
- **The failure mode to fear is not the crash, it is the plausible
  number.** A measurement that errors costs minutes. A measurement that
  silently measures the wrong thing costs a night, and it also spends
  your credibility, because you report it before you doubt it. Ask of any
  gating number: *what would I see if this were measuring the wrong
  thing?* If the answer is "the same thing", the instrument is not
  finished.
- **The mechanism:** `import x` under a `src/` layout does not resolve
  from the repo root, so it falls through to whatever the venv installed.
  A venv copied between trees (`cp -a`) brings its editable-install
  `.pth` with it, still pointing at the ORIGINAL tree. Replacing the
  copy's source then changes the files on disk and changes nothing about
  what runs. N trees, one engine, N sets of credible numbers.
- **A run's provenance belongs in the run's own output.** Not in the
  operator's memory of which directory they were in, and not in the
  transcript of the session that launched it — both die with the worker.
  The profile now records which package it loaded and prints it beside
  the numbers it produced, so the pair cannot be separated later.
- **⭐ The machine is a variable, and on the rig it is a bigger one than
  most changes.** The same code measured 9.893 ms/ack one day and 6.149
  the next; adjacent runs agree to ~4%. So a "40% improvement" against a
  figure recorded yesterday is indistinguishable from the box having a
  better afternoon. **Pair the arms adjacently or do not claim.** This
  retroactively softens every cross-day comparison, not just the one that
  found it.
- **A saturating metric moves in cliffs.** The missed-sweep ratio reports
  whether the loop held cadence, so it sits at 0% until the loop cannot
  cope and then climbs fast — a 1.7× cost change took one arm from 8.97%
  to 0.00%. It is the right thing to GATE on and the wrong thing to SIZE
  with. Quote it beside a continuous measure.
- **An estimate built from counting operations can be an order of
  magnitude out.** A follow-up was sized at "~15% of the ack path" by
  counting wasted iterations; measured, it is **under 0.5%** (4.2 µs and
  2.1 µs per call). The session's headline lesson in miniature — and the
  reason it was killed rather than scheduled.
- **Where retained state costs per-event work, cost scales with the
  SQUARE of the rate.** The venue holds dead orders for
  `venue_terminal_retention_s`, so records held ≈ instruction rate ×
  retention window. When a per-event scan walks that set, twice the
  instruction rate means twice the records AND twice the cost per event.
  That compounding is why a busy slate hurts more than a linear
  projection says, and why the lever is the retained SET, not the scan.

## 2026-08-15c — a rate is only as true as the clock that serves it

- **"Every 5.3 seconds" was the design, not a defect.** Edwin's feedback
  that the taker was too slow in live games matched his own reference
  numbers to the decimal (9/h × 75 = 5.33 s). Before treating a
  complaint as a bug, check whether the observed value IS the configured
  value — here the fix was a ruling, not a repair.
- **A served-at-tick loop biases every rate long, and the bias grows with
  the rate.** The taker's arrival rescheduled from the tick that served
  it, not from the arrival's own instant, so every gap carried ~half a
  tick. Invisible at 5.3 s (+4.5%), a quarter of the target at 1 s
  (+27%), and the shape drifts toward "one every tick" as λ·Δt → 1 —
  which would have quietly broken the "no learnable schedule" property
  the taker exists for. Whenever a rate is realised by a polling loop,
  measure the realised rate against the target before trusting the
  parameter; the loop's grain is part of the number.
- **Cap by thinning, not by queueing.** A rate cap that DEFERS arrivals
  turns a Poisson stream into a metronome at the cap; a cap that DROPS
  and reschedules leaves it Poisson. Same ceiling, opposite signature.
- **A per-book knob is a portfolio load.** Ruling "one print a second
  per book" is really "N prints a second", N = books live at once — six
  on a Thursday, twenty on a Sunday, sixty on an NCAA Saturday — and each
  print is an ack the maker must drain. State the portfolio number next
  to every per-book ruling.

## 2026-08-15b — two lessons from the converger, both about transfer

Full inventory: `specs/2026-08-14-mm-python-fix-set/scan-sweep.md` — every
per-event whole-collection scan in `src/mm` and `src/snt`, with growth
drivers and dispositions. Both lessons below came out of building it and
out of the CA2 chunk that prompted it.

### The pruner template, and the two shapes it does NOT fix

- **Scan-everything-to-find-the-expiring-few is the recurring defect.**
  `VenueEngine._stamp_and_prune` walked every order on every venue event
  to expire a handful. The acceptor's seen-key pruner had already learned
  this on 08-12 and fixed it — in a sibling module that never got told.
  The same shape then turned up four more times in the taker.
- **The fix template is head-prune an arrival-ordered structure:** append
  in arrival order, then `while queue and queue[0] < cutoff: popleft()`.
  Cost becomes proportional to what actually expires. It applies wherever
  the retention key is monotonic with insertion order — which is true of
  every expiry case in either engine.
- ⚠ **But two other shapes look identical and need different fixes.** A
  *filter-a-global-table-by-key* scan (`backoff.py`'s `suppression()`,
  walking the whole portfolio's reject table to answer about one
  security) is not a pruning problem at all — it needs an INDEX, and a
  deque does nothing for it. And a *whole-set rebuild* on a tick path is
  often fine by design and should just be recorded. Reaching for the
  queue everywhere would fix one of three.
- **A cap upstream does not bound any of them.** CA2b's examined-books
  cap bounds how many books a converge pass diffs and does nothing about
  the per-call cost of what each diff then calls. **Bounding the number
  of calls is not the same as bounding the call.**

### Writing a lesson down does not make it transfer

- The converger's round-robin advanced only on SERVED books. That was
  harmless for years because a served book leaves the dirty set, so the
  list drained itself and fairness was free.
- Adding the examined-books cap broke that, and the starvation appeared
  in **three classes in one chunk**: `rest` had a rotation, `live` had
  none (found while testing), and `suspends` cannot have one at all
  (found by the Phase-3 review, after it shipped).
- The general rule, worth keeping: **a work list that drains itself needs
  no fairness mechanism; the moment an item can stay on the list without
  being completed, it does.** A suspend re-stages every cycle, so it
  *behaves* like it stays even though each target is deleted.
- ⚠ **The uncomfortable part: that rule was already written in
  [[market-maker/decisions]] when the third instance was introduced, by
  the same hand, and it still did not get applied.** A written lesson is
  not a check. What would have caught it is enumerating the classes the
  change touches and asking the question of each one — the rule tells you
  what to ask, not where to ask it.

---

## 2026-08-15 — a coarse grid eats the randomization it carries

- **§5.7.3's variation and its increment fight each other.** The ±25%
  seeded variation at a 10,000-share touch spans ±2,500 shares — but a
  500-share grid quantizes that span to 11 landing spots, every one
  ending in 000 or 500. The book read as machine blocks not because the
  variation was too narrow but because the GRID swallowed it.
- **The tell is roundness, not just granularity.** The first fix
  (grid 100) made sizes finer but still round — and George rejected it:
  a book whose every size is a round lot reads as UNTOUCHED, i.e.
  inactive. Odd integers (12,433 · 8,617) read as partial fills having
  happened — an active book. So the grid went to 1, not to a smaller
  grid. "Make it look randomized" meant "make it look traded".
- **Grid and materiality are different rows that happen to share a
  number.** `qty_increment` (display granularity) and
  `material_qty_change` (publish trigger, §5.8) were both 500, which
  hid a coupling: on a 500 grid every basis move is automatically
  material. Dropping the grid decoupled them — and the only cadence
  effect is DOWNWARD (sub-500 drifts stop force-publishing).

## 2026-08-14 — the build-state sync: where "as built" actually lives

- **The VM outruns the vault by hours, reliably.** The deploy-log row
  read "waiting on George's go" while the ceremony was executing. A
  doc that records DEPLOY STATE is stale the moment an operating
  session moves; the durable fix is pointers, not copies — the build
  pages now say "read the log + the VM", and running coordinates live
  in ONE place ([[market-maker/build-deploy-log]]).
- **A process's code root is what it IMPORTS, not where its
  interpreter lives.** The taker's ExecStart names
  `~/inplay-market-maker/.venv/bin/python`, but PYTHONPATH points at
  `~/snt-checkout/src` — an ancestry check against the venv-side repo
  produced a confident, wrong regression alarm. Verify with
  `/proc/PID/environ`; the unit file is a decoy.
- **"Open PR" does not mean "not deployed", and "merged" does not mean
  "running".** Production runs a deploy lineage whose PRs (#24–#27,
  #30) are still under review, while merged work (#29) reaches the
  taker by a different checkout. The only reliable questions are
  ancestry questions against the RUNNING tree.
- **A PR's title is not its diff.** "PR #37: universe-filter fix" is
  actually the entire testing branch (65 commits) promoted to main —
  merge decisions need the diff stat, not the label.
- **Explorer claims are hypotheses until re-verified at the target.**
  The subagents' "no branch carries both features" was TRUE of the
  repo and still produced a false operational conclusion, because the
  deployment indirection (snt-checkout) was invisible from the repo.

- **Dedup on the publish side strips the liveness signal.** The
  publisher's "send only new readings" watermark looked like a polite
  optimisation. But on the push path, the ONLY way the consumer can know
  "the source answered just now" is a message arriving — so a watermark
  turns every quiet stretch into apparent silence, and the halftime trap
  (E38: 2,862 s with no new reading) comes back one layer down, after
  being carefully engineered out of the freshness rules. The general
  form: **whenever a signal is derived from message ARRIVAL, any
  filtering upstream of the consumer changes the signal's meaning.**
  Dedup belongs at the consumer (§7.3), where the identity lives.
- **A dedup id must name what it protects against.** JetStream's msg-id
  first named the READING — which made the server swallow deliberate
  re-offers along with accidental retries. Naming the publish ATTEMPT
  (reading + fetch stamp) dedups exactly the accidents and nothing else.
  Ask of any dedup key: "which repeats are accidents, which are on
  purpose?" — the key must separate them.
- **The ack is the durability boundary, so its position is a design
  decision, not plumbing.** Ack after journal makes every crash window
  safe (before → redelivery; after → §7.3 discards). Ack before journal
  would quietly re-open the exact loss JetStream was adopted to close.
  The same shape as write-the-object-then-the-row (03-08): order the
  irreversible step last.
- **Structural parity beats tested parity.** Two code paths that must
  emit identical envelopes (file replay vs the wire) drift eventually if
  parity is only asserted in tests; giving both paths ONE constructor
  makes drift impossible and turns the tests into proof of the callers'
  argument derivation only. The 1,089-reading equality test then guards
  the contract, not the construction.

## 2026-08-05c — the drift George caught

- **A drift can be fully documented and still be a drift.** The 24-07
  ingestion decision says the hot path never calls SR — a poller at the
  edge, pushing onto the bus. Across four sessions the build absorbed
  polling into the engine, each step logged in the vault, and no step
  checked itself against the ARCHITECTURE decision — only against the
  previous session's state. The stop-condition ("contradicts a recorded
  decision") never fired because each increment was small and locally
  consistent. **Reconcile the built shape against the decisions log,
  not just against the last session note.** George caught it in review;
  the seam meant the correction was cheap — which is the second lesson:
  a well-placed seam is what makes an architecture mistake survivable.

- **A handover is context, not consent.** This session started
  autonomously because the handover said "fully unblocked", carrying
  yesterday's ruling forward as authorization. George had not approved
  the run. Spend that cannot be un-spent (API quota, external calls)
  deserves a fresh confirmation at session start, even when a recorded
  ruling appears to cover it.

## 2026-08-03→05 — the deployment thread, the runtime, and the liveness lesson

- **Two different facts were fused into one number, and it took George
  pushing back twice to see it.** "How old is the probability" and "when
  did the source last answer us" are different questions. Sportradar sends
  no heartbeat — 98 % of timeline entries change the number, so its
  timestamp advances only when the game moves. Measured on the real game:
  halftime is a 2,862 s gap. §3.3.1 as written suspends every book for all
  of it. The fix is not new bands — it is applying the same bands to the
  right fact (the fetch, not the reading). **When a rule misbehaves, ask
  which FACT it measures before touching its values.** And the second
  correction mattered as much as the first: a confirmed number is not
  a *degraded* form of fresh — it is fresh. Nothing to discount.

- **Clock-driven work in an event-sourced core has exactly one honest
  shape: a producer.** The sweep needed to run every 2 s; the orchestrator
  reads no wall clock; therefore the scheduler lives OUTSIDE, mints a
  journalled event, and replay consumes what it minted. Same relationship
  the poller already had. Corollary learned the same day: keep every
  clock-reader in ONE module (`runtime/loop.py`), because a second one can
  creep in silently and nothing will flag that replay broke.

- **The dedup system fights liveness signals, correctly.** A source that
  republishes the same probability every 2 s produces duplicates from the
  second copy on — recorded, then ignored. So "proof of life" can never
  ride an existing fact's identity; it needs its own (the sweep's
  observations map, or a fetch-stamp in a push message's key). We nearly
  built it twice the wrong way: a fetch-time in the key would re-mint the
  whole re-fetched timeline as new facts; in the payload alone it would
  CONFLICT-alarm every 2 s. **The identity design IS the feature.**

- **Estimates were wrong by 22× in the safe direction, and one benchmark
  ended the argument.** ~140 ms per pass was the carried belief; 6.3 ms is
  the measurement. The compute case for a Go port evaporated in a minute
  of running code. Meanwhile the Mac's fsync figure was 35k/s — invalid,
  because macOS `fsync` does not flush the drive cache. **Benchmarks only
  count on the hardware that will run the thing** (N31 waits for the VM).

- **The restart drill demonstrated a gap no test had reached:** events
  that publish into our absence are simply gone (core NATS, no JetStream
  on that subject) — the replayed record believed three swept levels still
  rested. Replay is honest about what the journal SAW, not about what
  happened. Venue truth needs either a snapshot at boot or a healer that
  re-derives it — both known, both parked with eyes open.

- **Docs-vs-reality is a live failure mode, twice in one session.** The
  vault's VPC draft had every address wrong (the deployed proxy's env was
  the truth), and the "reading time vs last_updated" confusion came from
  me trusting my own earlier summary over the adapter's code. The working
  mode's third stop condition (reality ≠ docs) earns its place.

- **The tail-pipe gotcha bit AGAIN.** Piping gates through `tail` in an
  `&&` chain masked a broken import and let a commit through; caught on
  the unpiped rerun. Two sessions, same trap. Never pipe a gate.

- **The tests were shaped like the bug.** Every test ran one side of a game
  at a time, so the head-on collision between two per-team events sharing a
  game-level idempotency key never occurred in the suite. There *was* an
  away-side test — it built the envelopes and checked the probabilities were
  flipped, but never put them through an acceptor. A passing suite proved
  the translation right and the architecture wrong. **Ask what shape the
  tests are, not just whether they pass.**

- **Storing answers instead of ingredients is the root of a whole bug
  class.** The engine kept each game's computed expected value and a running
  banked total, not the probabilities and results that produced them. From
  that single choice came: a corrected official result double-banking (a
  win corrected to a loss still reads $5.00), a finished game resurrecting
  when a late probability arrives ($10.00 → $14.50 on a game already over),
  and configured values that could change without any stored price
  noticing. §2.5 says it in one line — *"incremental valuation state is
  prohibited"* — and it turns out to be a bug-prevention rule, not an
  aesthetic one.

- **A silent skip and a silent failure can be the same code path.** The
  engine dropped unknown teams deliberately, because NCAA sides play FCS
  schools with no Team Company. That correct behaviour made a *missing map
  entry* invisible: an unmapped Chiefs would have looked exactly like a
  legitimate FCS opponent, priced never, alarmed never. Whenever "ignore
  this" is correct for one reason, check what else it now hides.

- **Belt-and-braces belongs on the output, not the input.** George asked for
  a second validation pass as a safety net. Measured, the same triple
  validated from either side can't disagree — 0 differences over 1,001
  splits, because addition commutes. The check that *does* earn its place
  is on the result: the two teams' expected values must sum to exactly
  $5.00. That catches swapped sides, broken repairs and a wrong payout
  constant, none of which double-validation would see. **The instinct was
  right and the mechanism was wrong — worth separating those.**

- **⭐ The per-game breakdown cancels out of the price.** Because every win
  pays a flat $5, the sum of per-game win probabilities and the total
  expected wins are the same number times five. Nine months of "we need a
  probability for all ~2,400 games" turns into "we need 170 numbers." The
  hard problem was an artefact of how the formula is written, not of what
  the formula needs. (George.)

- **A betting line is not a forecast.** The over/under is set where the money
  balances, which makes it the *median* outcome, not the mean — a different
  number, and worth up to a few dollars a share on a ~$57 share when our
  whole spread is $0.10. And these particular lines are known to be biased:
  too high for very strong teams, too low for very weak ones, missing final
  records by ~2 wins on average (Woodland & Woodland 2013). Using market
  data is fine; **using it without knowing what object it is** is not.

- **A frozen input can cancel a live one exactly.** Season win totals don't
  move during a game. Subtract the current live probability from one and the
  in-game price movement vanishes completely — $60.00 at 60%, $60.00 at 90%.
  It would have looked like a working system with a dead price. Whenever
  two terms are derived from overlapping information and one is stale, check
  whether the update is being subtracted from itself.

- **"Not in the feed" and "doesn't exist" are different findings.** Our
  16-07 pull proved SR's NCAAFB futures feed has no win totals. A research
  agent then reported the market is near-universal across all five books SR
  already sources, and concluded our evidence must be wrong. Both were
  right — the market exists, SR just isn't carrying it. That distinction
  turns an impossible ask into a coverage complaint, and it's the difference
  between building a model for 138 teams and sending an email.

## 2026-07-30

- **A dead book is the real launch risk, and the fix is a house taker, not more makers.** SNT-1 exists because a real exchange with few users looks empty. The MM alone does not solve this: it posts liquidity, but liquidity nobody hits still reads as "no trading." SNT-1 manufactures the *taking* side so prints actually happen. Two house agents, opposite roles: maker (MM) and taker (SNT-1).
- **Noise is bought, not free.** SNT-1 is a deliberate controlled loser; its cost is literally the spread it crosses, metered against a $100k/team/session budget. That spread cost is the **subsidy that seeds the market** and is largely captured by the MM on the other side. The budget is a spend cap on that subsidy, not a P&L target.
- **Uninformed-by-construction is the safety property.** The realism (disposition-effect profit-taking) conditions only on SNT-1's own cost basis vs mid, never on book state or participant data. That is what keeps its flow noise rather than a signal participants could reverse-engineer or that could push price toward a target.
- **The off-field rule already handled this.** Because SNT-1 carries no participant side, its MM-facing prints fall outside the >= 1-participant-side off-field-volume rule automatically. A well-drawn rule needed no amendment for a new agent, worth remembering when the next house agent appears.

## 2026-07-24 (b) — build day + ingestion research

- **Measure the feed; don't reason about it.** We recorded twice that SR
  probabilities move "per play, ~30–40 s" — plausible, repeated, and wrong by
  an order of magnitude. Counting gaps in our own captured game gave a
  **4 s median**, because win probability decays with the game *clock*, not
  only on plays (~6–7 updates per play). The 2 s conclusion survived, but the
  *reason* inverted — 2 s matches the median rather than oversampling. Any
  claim about a feed's behaviour should come with the measurement.

- **"Is there a push feed?" is answerable definitively, and worth answering.**
  Four independent checks (schema, 414 captured messages, published contract,
  vendor docs) beat one plausible assumption. Answer: SR has no probabilities
  push product for **any** sport — pull only. Knowing that is worth more than
  a faster guess, because it closes an architecture debate permanently.

- **Fan-out planes have contracts; pick the one whose contract you need.**
  Centrifugo is at-most-once, history off, recovery-by-refetch — perfect for
  showing a phone the score, disqualifying for a price input whose recovery
  path must never be "go fetch something". Backend-to-backend belongs on the
  durable bus. Same layer, same data, wrong contract.

- **A cache is not a feed.** The SR service's Redis probability keys look
  like a free push source and are actually TTL cache-aside artefacts, written
  only when a *user* happens to hit the API and refreshed by nothing. "The
  data is in Redis" says nothing about whether it's current.

- **Placeholders travel as facts unless you label them.** A "50 msg/s"
  governor from a colleague's message became, in my head, "our budget" — and
  briefly promoted diff-publishing from optimisation to requirement. It was a
  placeholder; the venue spec contains **no rate language at all**. Check
  where a number came from before designing against it.

- **Verify a vendor claim against the vendor's own document.** Two minutes
  with the tZERO PDF confirmed ClOrdID ≤20/no-leading-zeroes, revealed that
  replace and cancel each carry **two** such ids, and confirmed the odd
  `HandlInst` asymmetry (banned on new orders, mandatory on replaces). It
  also proved a negative — no rate limits documented — which redirected T2
  from "read the spec" to "ask tZERO with T1".

- **Golden fixtures are cheap certainty.** The spec shipped one worked
  example for the quantity seed; reproducing it byte-exact before writing
  anything else validated both the document's precision and our reading of
  it. Do this first with any spec that ships fixtures.

- **Keep the translator pure and the fetcher separate.** The SR adapter takes
  parsed data and returns envelopes — no network, no clock. So a captured
  game is a deterministic test input *and* the live poller inherits an
  already-proven translation path. The messy part (retries, quota, timing)
  stays quarantined in the part that can't be unit-tested anyway.

- **Enforce invariants at the border, not in the middle.** Floats are refused
  by the money/probability constructors, by the payload hasher, *and* by
  parsing SR's JSON with `parse_float=str`. Three chokepoints mean no code
  path downstream has to remember the rule.

## 2026-07-24

- **A written spec can overturn call decisions — the protocol held.** The
  v1.3 Build Spec contradicted three things Edwin said five days earlier
  (lifecycle, cadence, probability source). Because the rule is "surface
  every conflict, never silently adopt", they became E17–E19 instead of
  silent rewrites. The doc is the baseline; the conflicts stay visible.

- **"Priced" = probabilities published, and SR prices rolling.** A game can
  be scheduled without being priced; SR attaches probabilities as games
  approach (NCAA: 70 of ~1,700 today). Consequence: full-season Σ GEV(g) is
  impossible from SR alone — and since Σ P_win(g) ≡ expected remaining wins,
  the fix is a source swap for the unpriced tail (SR win-total futures, or
  InPlay-internal weekly — Edwin's original model), not a formula change.

- **Polling rate ≠ cycle rate.** The probability only moves per play
  (~30–40 s). The decision cycle reads memory at any speed; the poller polls
  at the freshness band (~2 s per live game). Edwin's 200 ms and the spec's
  2 s stop being a fight about polling — the remaining question is purely
  how fast the *cycle* must react (E18).

- **Derive the quota ask, don't guess it.** Freshness band × concurrent live
  games × season = the number: per-game polling on the current product ≈
  2.5M calls/mo at ~20 QPS peak; the v2 product's live-bulk endpoint (all
  live games, one call) ≈ 200k/mo at 0.5 QPS. The product choice IS the
  quota ask (S7).

- **Probe the real API before trusting any requirement on it.** Thirty
  minutes with the trial key found: no tie probability exists (spec requires
  it, forbids inferring it → S6), NFL's seasons listing is empty but the
  date-schedule endpoint prices it fine, and 403 means per-product
  entitlement, not a broken API.

- **Verify golden fixtures on arrival.** The spec's SHA-256 quantity-seed
  fixture was reproduced locally before adopting anything else in the doc —
  cheap, and it certifies both the doc's precision and our reading of it.

## 2026-07-23

- **The v1 lifecycle is simpler than everything we designed (23-07 call).**
  Rest-until-gone kills the top-up arithmetic, quote aging, replenishment,
  AND the amend-vs-cancel trilemma in one stroke: partially-filled orders
  just sit; price moves cancel-and-repost the remainder; full fills reload
  at top of book. The design surface that replaces all of it is
  **fill-response logic** — "if you get a fill, what do you do next" (N14).
  The 22-07 reconciler analysis is shelved, not wasted — it's the
  augment-later iteration.

- **Replace = back of the queue, everywhere.** Troy (ex-Citadel): standard
  on effectively every matching engine — an updated order is a new arrival.
  It's why real MMs invented queue tricks (partial packets etc.). Here it
  simply doesn't matter — Edwin: "we don't care about that" — because the
  MM isn't competing with other MMs for queue position.

- **v1 tolerates a momentary self-cross (Edwin + George).** "New orders are
  faster than cancels, believe it or not" — waiting for cancel confirmations
  before posting creates a gap Edwin explicitly doesn't want; a fleeting
  cross during a price adjustment is accepted on the first iteration. Wash
  blockers "can be used very predatorily" — policy for users is rulebook +
  order queries + removal, not venue tech (Troy checking tZERO's self-match
  prevention anyway, T11).

- **Edwin's ingestion model is pull, not push.** He talks in "calls" — we
  call Sport Radar on a schedule that bifurcates by game state (live ~200ms,
  non-live 30–60s, earnings burst). The hot-path principle survives
  unchanged: a poller writes memory, the quoting loop reads memory. Whether
  SR can actually serve that call shape is S5.

- **A trade print is a public receipt.** Every match is broadcast on the
  market-data feed — price, size, time, a unique trade ID. Busts appear on
  the same feed as public trade *deletes* (reason "Cancel/Bust").
  Consequence: the supervision watchdog runs entirely off the public feed —
  it sees every trade in every market, including user-vs-user trades the MM
  wasn't part of. No special access needed.

- **Aggregated book = queue position is invisible.** tZERO's feed shows only
  the total per price level (plus an order count) — never individual orders.
  We can never observe where our own order sits in the queue, so T8.1 (does
  an update keep queue position?) can only be answered by tZERO directly or by
  a two-account experiment in QA.

- **Opening auctions exist in the venue.** Some markets open by collecting
  orders without matching, computing one fair opening price from all of
  them, trading everyone at that price, then going continuous. tZERO's feed
  has the machinery (auction state, theoretical opening price). Whether OUR
  market uses one daily = T9 — it changes what the MM does at the open.

- **Match the store to the access pattern (why object storage).** The event
  log is written once, sequentially, and almost never read (boot tail +
  offline analysis). Object storage fits exactly: immutable, pennies/GB,
  zero servers, built for batch reads. Postgres would charge us for indexes,
  transactions, and vacuum we never use — and degrade as it grows. A log
  system (JetStream) is the *pipe*, not the archive. Write segments as
  columnar files and they're queryable later with no database at all.

- **The MM is event-rate bound — not CPU, not RAM.** Working state is
  per-TEAM (latest RP, ~a dozen own orders, inventory, capped counters) —
  a few MB total regardless of user count. Users add message RATE (fills,
  book updates flowing through), not resident state. The math is
  microseconds. The scarce resources are the venue's message allowance (T2)
  and round-trip latency — which is why every design argument lands on
  message budgets, not hardware. Guard: rolling windows as capped
  counters/ring buffers, never unbounded event lists.

- **The two FIX sessions fail differently.** Market-data subscriptions are
  wiped on disconnect (reconnect = re-logon with sequence reset,
  re-subscribe, fresh snapshot). Order-entry resting orders SURVIVE
  disconnect. Recovery flows must be designed separately — and the OE side
  is why the dead-man switch exists.

- **Snapshot-at-cycle-start kills the race (George's catch → confirmed
  design).** Live market state mutates continuously under pushed messages;
  each cycle takes an atomic copy and computes on the frozen snapshot;
  anything arriving mid-cycle lands in live state and coalesces into the next
  cycle. No locks in the hot path — and recording the snapshot is exactly
  what makes deterministic replay work.
- **RAM is bounded; only the disk grows.** Two stores, don't conflate:
  working state in memory (latest RP, ~a dozen live orders/team, inventory,
  seconds of rolling counters) is overwritten forever — bounded. The
  append-only event log grows on disk, background-flushed, never blocking a
  cycle. A season of record-everything is tens of GB of disk — trivial.
- **Order anatomy + the top-up.** OrderQty = chain total · CumQty = filled ·
  LeavesQty = still resting. Fills survive a replace (CumQty carries), so
  top-up to X resting = replace with OrderQty = CumQty + X — or add a sibling
  order of (X − leaves) at the same price. One order/one queue spot vs two of
  each; which is better hangs on T8.1 (queue position) + message budget.
- **The event log is write-only in operation.** One local sequential append
  per cycle (a few KB) — never a remote write inside the loop; durability
  ships asynchronously behind it. It's read in exactly two places: at boot
  (snapshot + tail replay to rebuild state) and offline (replay, audits,
  calibration, the challenge dataset). Nothing in the app reads it → it
  doesn't belong in the production database, or in any transactional DB
  at all.

- **The hot path never asks for anything.** All inputs arrive as pushes (FIX
  execution reports, bus RP, MD subscription); the cycle reads only local
  memory; the database is write-behind. A 50ms fetch anywhere in the loop
  would eat the 200ms budget — so there are no fetches.
- **The venue tells us our position on every fill** (PosSIZ/PosCOST/Rpnl/
  Upnl, optional fields) — our event-sourced inventory stays primary (needed
  between messages, deterministically); venue values = free drift alarm +
  ops-UI P&L source.
- **Users can cross; we can't.** An arriving order priced through the other
  side executes immediately (normal — synthetic MO relies on it). The
  never-crossed law binds only what RESTS — specifically the ladder we
  publish against ourselves.

## 2026-07-22

- **Reconciler reality-check (George pushing on complexity).** Three facts
  deflate it. (1) **Scale:** the ladder is N≈3–6 levels/side → ~6–12 orders
  per team per cycle — the diff is over a dozen orders, not a thousand; the
  1000→1200→1000 shape never happens per team (level count moves ±1–2 on
  profile flips). (2) **Side never flips:** 35=G cannot change Side — bids
  pair only with bids, offers with offers; two independent small lists.
  (3) **No persistent slot state:** pairing is recomputed fresh each cycle —
  sort live orders by price, sort target levels by price, zip, amend each
  pair, create/cancel the tail. Stateless per cycle. And the honest
  fallback: **full wipe-and-replace is a legitimate v1** — the reconciler is
  a message-budget optimization, and T2's MaxOrdRate answer (not taste)
  decides whether it's ever needed.

- **Publish is a reconciler, not a send (George's push, refining the
  trilemma).** Levels and quantities differ cycle-to-cycle, so no single
  strategy (cancel-first / post-first / amend-all) covers a real cycle. The
  correct shape: diff the target book against the believed-live book → a
  per-slot plan — AMEND if the slot persists, CANCEL if gone, CREATE if new,
  no-op if identical (zero messages) — executed under ordering rules:
  retreating side first (retreat can never cross), cancels before creates at
  overlapping prices, advancing side deepest-first with top-of-book last,
  micro-barrier only on the specific orders an advance would cross. Same
  shape as React's DOM diff or terraform plan/apply. The dominant in-game
  case (RP tick, N constant) is pure amends. Corollary: if the seeded jitter
  re-rolls every heartbeat, cosmetic cycles amend the whole book — jitter
  cadence is a message-budget choice, and it's book-visible → Edwin-adjacent
  (randomization bounds, E5).

- **The cancel-replace sequencing trilemma (George's framing).** Per cycle,
  old quotes must become new quotes. (A) cancel→confirm→post = a naked window
  with no MM quotes for ~a round-trip. (B) post-then-cancel = brief 2×
  displayed size AND the new bid can cross the stale offer → self-trade /
  wash-trade block. (C) amend in place via 35=G = atomic per order, no gap,
  no overlap — the venue spec has it; the gateway build (Hasan) adds it;
  only structure changes (adding/removing levels) still face A-vs-B. If
  forced to choose A or B, A (the gap) is safer: users' resting orders still
  populate the book during the window and the band caps sweep damage,
  whereas B risks integrity (self-cross) and double inventory. In ALL three,
  the fill-vs-cancel race (cancel returns "already filled") must be handled
  by the state machine. Feeds N10 + the T2 message budget (G halves
  message count vs cancel+new).

- **"Recalculate on every fill" sounds heavy — it isn't.** Every fill (any
  partial, any level, either side) queues a trigger because inventory moved
  and the skew is now wrong. But cycles never overlap and mid-cycle triggers
  coalesce into ONE next cycle — so a burst of 20 fills costs the running
  cycle plus one more, and the effective ceiling is the cycle rate
  (~5–10/sec in-game) regardless of fill rate. The math itself is
  microseconds; the real cost is the cancel-replace messaging (T2 budget).

- **EMERGENCY is not a quoting profile (George's catch).** The condition
  classifier conflates two different failure classes. **Input failures**
  (Sport Radar dead, valuation stale) — the order path still works, so the
  right response is quoting wide / around a frozen RP. **Actuation failures**
  (gateway or FIX session down) — we cannot post *anything*, so "widen the
  spread" is physically impossible; the only valid responses are out-of-band:
  the **dead-man switch** cancelling our resting quotes (part of Hasan's
  cancel build) and a **halt via supervision**. Made worse by the venue fact
  that resting DAY orders **survive disconnects** — without the switch, a dead
  MM leaves stale quotes resting in the book until 23:59 ET. The decision
  table must split `compute_ok` (can we think?) from `path_ok` (can we act?).

- **The classifier is boring by design.** MOC sits at Normal almost all the
  time. It's five if-statements checked in severity order, not a formula —
  its entire job is noticing the rare moments the inputs can't be trusted.

- **`feed_lag` is not free — it has to be constructed.** You only know how far
  behind you are if messages carry event timestamps (lag = our clock − event
  stamp, which needs clock sync) or by cadence expectation (in a live game,
  plays arrive every ~30–40s; silence beyond that is itself the signal).
  Which of these is available depends on how Sport Radar delivers (S3).

- **The standards' F(…)/G(…) notation is a trap.** They read as mathematical
  functions but are type signatures: the bracket list is an exhaustive
  *allowlist of what may be consulted* plus a purity contract; the bodies are
  lookups, decision tables, and threshold rules. The only real mathematics in
  the whole stack is the offset arithmetic (reservation prices) and the
  displayed-quantity formula. Present them as lookups/rules, never inline
  with prose as if they were equations.

- **The off-field term hides a contradiction (→ E2).** The earnings-report
  component says price impact of EST/ACT is *"market-determined, not a fixed
  function of the number"* — but the MM's ESV needs a mechanical OffField
  value at every moment, and the MM re-anchors the market at ESV. If the MM
  moves mechanically at the 7:30 release, the market never gets to
  "interpret" the surprise. Edwin has to resolve which number ESV holds
  between reports and whether it steps at release.

- **Most of the "deferred math" isn't math.** Across all engines the deferred
  items are: numbers for lookup tables, thresholds for decision rules, and a
  handful of arithmetic constants. The architecture is fully specified; the
  values aren't. That's why "we ask, we don't propose" is workable — the
  questions are enumerable.

- **The remit line.** *"If Edwin watched the book, could he tell the
  difference?"* Yes → his algorithm, his question (all numbers, thresholds,
  visible behaviour). No → engineering mechanics, ours (topology, transport,
  FIX plumbing, replay). Hybrids (like full-replace vs diff-publish) get both
  options put to Edwin with the observable consequences stated.
