---
description: "T-F07 built and merged (PR #14), all four MM PRs merged, the NATS grants done in-house, and the taker deployed unattended on the MM VM"
---

# 2026-08-11 — T-F07: the schedule-derived activity state

> **Type:** design call + build session. George + Claude.
> **Repo state at close:** ALL FOUR MM PRs MERGED on George's go —
> #11 → #13 (one trivial `__init__` conflict with #11, resolved:
> both fields kept) → #12 → #14 (re-targeted to main). Main is
> **`5681767`**: **670 tests, ruff + mypy-strict green** on the merged
> tree. Built in a git worktree (`../inplay-market-maker-tf07`).
> **Vault:** this branch still carries earlier sessions' uncommitted doc
> work; this session's edits sit beside it, uncommitted — George's
> standing call.

## What we did

1. **The T-F07 design call, as George asked — options before build.**
   Four schedule sources presented; George chose **A: consume the bus**.
   The sportradar service discovers games from SR's probabilities
   sport-schedule endpoint, polls each game at tier cadence, and every
   publish on `sr.probabilities.reading.>` carries `kickoff_time`,
   `status`, scores and both competitor ids — so the bus alone drives
   the derivation. Rejected: a service-published state subject (one
   consumer; taker policy would leak into the feed service) and direct
   SR polling (the 05-08c ingestion ruling). The file source survives
   behind the same store as fixture/fallback.
2. **Built it** (`snt/schedule.py` + runtime/config/journal wiring):
   per-BOOK states via `TEAM_BINDINGS`, `SNT_STATE=AUTO` vs operator
   pin, `AUTO` un-pin command, audit-only derived journal records,
   `SNT_IPO_WINDOWS` PRE_KICKOFF floor, `SNT_SCHEDULE_FILE` fallback.
   JetStream ordered consumer, last-per-subject — boot rehydrates the
   newest reading per game in one burst. 17 new tests.
3. **Deploy artifacts updated** (`snt-1.env.example`, `SNT-RUNBOOK.md`):
   the AUTO section, the grant dependency, the fallback file.
4. **Docs:** decisions entry (the source ruling) · parameters (4 rows
   🟡 OURS) · taker requirements (T-F07 🔴→🟡, T-F04 note, addendum,
   frontmatter description added, stale tail rewritten) · E41 carries
   the per-book confirm for Edwin.

## What we learned

- The taker's four states already mirror the service's poll tiers —
  the `PollScheduler` docstring cites the MM vault's tier table. One
  derivation, two consumers, no new contract needed.
- The service errs BUSY (unknown kickoff → live-rate polling); the
  taker must err QUIET (unknown anything → OVERNIGHT). Same facts,
  opposite failure costs — recorded in the code notes.
- A reading payload exists only once a probability posts. In practice
  that is days before kickoff; a game with no probability ever stays
  OVERNIGHT — the quiet direction.

## What went wrong / got stuck

- Nothing blocking. Ruff's rule set here is wider than the MM
  pyproject suggests (FURB/BLE/I fired) — three findings, all fixed.

## Decisions made

- Mirrored to [[market-maker/decisions]] (2026-08-11): bus source ·
  per-book states · pin/AUTO precedence · err-quiet · IPO windows as
  config · the four 🟡 numbers.

## Questions opened/closed

- E41 grows the per-book-shape confirm (Edwin).
- New grant owed by **Hasan**: JetStream consume on
  `sr.probabilities.>` for the taker's NATS user — bundle with the
  still-owed `snt.control.{bot_id}` grant.

## Late addition — the session continued: grants done OURSELVES, the taker DEPLOYED

George: "Why are you not able to do the Hasan asks yourself? … If we
haven't got the access, we need to request the access." We had the
access. After a Slack not-mid-work check on Hasan, all NATS-box work
was done by us, per the box's own conventions (dated `.bak`,
`nats-server -t`, SIGHUP hot reload, zero dropped connections):

- The `snt-taker` NATS user (kill switch + scoped JetStream consume) ·
  the `SR_PROBABILITIES` stream created to the publisher's exact
  contract · the `sportradar` user's publish extended for the future
  mm-publisher deploy · everything verified end to end.
- Credentials to Secret Manager: `snt-taker-nats-password` (rotated
  once — the first value printed in a CLI error, burned on the spot)
  and `snt-taker-venue-login`.
- **Deployed:** `snt-1.service` unattended on the MM VM —
  `main@5681767`, `SNT-CFG-0003`, journal `/var/lib/mm/snt3`,
  `SNT_STATE=AUTO`, EAGL float pinned 4,988. Boot clean; **the kill
  switch drilled live** (halt → resume, journaled). T-R01 → ✅.
- Lessons: consumer-create grants need the `$JS.API.CONSUMER.CREATE.
  <stream>.>` wildcard form on modern servers; nats CLI errors print
  the credentialed URL — use `--user/--password`, never URL creds.

Full record: [[market-maker/decisions]] 2026-08-11b.

## Late addition 2 — the mm-publisher DEPLOYED (the ingestion go-live for the taker's feed)

George: "just get it deployed." Coordinated across sessions — a sibling
session had prepared the deploy (PR #8 merged, the terraform + deploy.yml
third step, the `inplay-mmpub-nats-url` secret, PR #10 open); this
session messaged both sibling sessions to stand down, took ownership,
and finished it:

- **PR #10 (dev → main) conflict resolved and MERGED** (CI green); the
  production dispatch ran. API + live worker deployed; the NEW publisher
  pool step failed (image-only deploy cannot CREATE a pool — it fell to
  the default compute SA, 403 actAs).
- **Bootstrapped `inplay-mm-publisher` by hand** on the same SHA image,
  full config (cloudrun-sa, direct VPC egress, manual 1 instance —
  the AlwaysOwns fence). Two boot gaps found and fixed en route:
  the pool needs **PROBABILITIES_API_KEY** (the probability endpoints
  never read the SR key — blank = silent 403s) and **REDIS_URL**
  (production_mode's fail-fast validator demands non-loopback even
  though the worker never touches Redis). tfvars corrected on dev.
- **The stream is now the PUBLISHER'S:** its idempotent `add_stream`
  refused my morning hand-made stream ("different configuration" — the
  CLI's `--defaults` set fields nats-py omits). The empty stream was
  deleted; the publisher recreated it as owner. **Rule: the publisher
  owns the stream config; never pre-create it by hand.**
- **Verified live:** publisher boots, NATS connected, discovery fetched
  today's SR probabilities schedule (200). Zero readings today = no
  universe games on 11-08 — the correct quiet state. The taker was
  restarted so its consumer binds the recreated stream; boot clean.
- ⚠ **A mistake of mine, caught by a sibling session:** my regex union
  of the terraform merge conflict produced a broken `main.tf` (unclosed
  resource block). Their `fix/terraform-stitch` (PR #12) repaired dev.
  The deployed pool was unaffected (created via gcloud). Lesson: never
  merge-resolve HCL by regex without a syntax check.

## Late addition 3 — the test protocol filed + the taker's SHORTS built

- **[[market-taker-test-plan]] created** (George's protocol: taker
  isolated → the maker's own plan → joint TJ1–TJ4, with SR game
  simulation as TT6's two rungs — rig replay via the A2 harness, then
  true SR simulation through the production publisher on `.TEST`).
- **Shorts unblocked** (George: Edwin confirmed 10-08; flatten first,
  then short, both bots) and the TAKER half built — **MM PR #15**,
  T-O10 verbatim, `SNT_SHORTS`-gated off, dormant under the standard
  float. 682 tests. The MAKER half (N34) handed to the MM session with
  the minting-not-amending design note. Details: decisions 2026-08-11d.

## Next

1. ~~Merge PRs #11–#14~~ ~~taker deployment~~ ~~the Hasan grants~~
   ~~Hasan notified~~ ~~mm-publisher deploy~~ — **ALL DONE this
   session.** The full taker chain now runs unattended: SR → publisher
   → JetStream → taker AUTO states → (books, once the engine runs).
2. **Thursday 13-08 (the dry run) is the first live proof** of the
   publisher → taker chain on a real game: expect the game's two books
   to go PRE_KICKOFF → LIVE → POST unaided. Watch `snt-1`'s journal
   for the derived marks.
3. The MM engine's next run (`supervised10`/CFG-0009) picks up #11+#13;
   its VM checkout still needs `main@5681767` (the bundle is already in
   `~/kit/snt3.bundle`).
4. The shorts build (T-O10 + side-5) stays queued behind E26 + T16.
5. Vault docs on this branch remain uncommitted (three sessions' worth)
   — George's standing call.
