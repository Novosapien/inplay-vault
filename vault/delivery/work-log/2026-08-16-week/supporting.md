---
description: "Weekly engineering record for the supporting repositories, 09-16 August 2026 — the vault, the specs repo and the global website, including the normative market-maker requirements"
service: inplay-vault · specs · inplay-global-website
window: 2026-08-09 .. 2026-08-16
commits: 45 in scope (67 total across the three repositories; 22 out of scope)
authors: { westy412: 43, Hxsan: 0, Claude Code: 2 }
branches: { touched: 4, merged: 3, open: 1 }
---

# Supporting repositories — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

Covers `inplay-vault`, `specs` and `inplay-global-website`. The three service
repositories are covered in their own files.

## Headline

The written record caught up with the trading build this week. It started on
9 August with a live probe that decoded an undocumented venue rule. The same day
produced two normative lists of what must be true before the market maker and
the taker go live. George then added 43 session notes to the vault and created a
build/deploy log that tracks every change from build to live. He also wrote a
plain-English guide that decodes Edwin Johnson's fair-value pricing model. The
guide checks Edwin's arithmetic and finds one error in his worked example. It
also proves that Edwin's model and ours are one model, written two different
ways. In parallel the `specs` folder became a git repository for the first time.
The twelve written plans behind the service work now have a history, not only a
filesystem.

The single commercial change was a full stop. The global website merged a copy
edit that turns "Trade Sports. As Stocks." into "Trade Sports As Stocks."

---

## 1 · `inplay-vault`

### Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 61 total — westy412 37, `Claude Code` 2 (agent commits),
  Brett StClair 22 (out of scope)
- **In-scope commits:** 39
- **Branches touched:** 3 — `docs/t0-plain-english-guide` (open, 3 commits ahead),
  `origin/main` (mainline), `docs/advertising-outbound-onboarding` (Brett, out of scope)
- **Busiest day:** 2026-08-13 (11 in-scope commits)
- **In-scope commits per day:** 09-08: 6 · 10-08: 4 · 13-08: 11 · 14-08: 4 ·
  15-08: 10 · 16-08: 4

**Brett StClair, out of scope, one line:** 22 commits between 10 and 14 August.
They cover the dated delivery flight plans, the meeting digests for 27-07 to
12-08, and a new advertising outbound onboarding pack (offer, ICP, persona).
They are not detailed here and are not in the commit appendix.

**A note on the commit count.** The repository was live while this file was
written. Two westy412 commits landed on 16 August during the work: `dd0e6a4` at
18:55 and `63115a0` at 19:20. The count above includes both.

Every count in this section uses explicit clock times on both bounds:
`--since="2026-08-09 00:00:00" --until="2026-08-17 00:00:00"`. Git reads a bare
date at the current time of day, not at midnight. The bare-date form drops the
earlier commits of 09 August.

### Themes

#### 09 August — the normative requirements lists, and the venue rule that forced them

Six commits landed on 9 August, all inside one hour. They are the written brief
that the market-maker and trading-service work executed for the rest of the
week. Four of them are one connected piece of work.

**The trigger was a live probe.** No tZERO document says what happens when the
engine tries to sell more shares than it holds. An agent sweep of the vault,
both gateway repositories, the trading service and the vendor PDFs found nothing.
Worse, the app held three contradictory beliefs about it in three files, and
none cited a source. So George probed the venue directly, on his own account, at
his own direction. The venue answered in one reject line and printed its own
arithmetic:

```
FAILSRISK[5120866205]: You can SELL at most 50 shares of IPTCGIAN. Pos=100 livS=50
```

`2da621e` records the rule. **A sell may not exceed `Pos − livS`** — the
position minus the quantity already committed to live resting sells. Over that
limit the venue rejects the **whole order**. It never part-fills to the limit,
and it never opens a short. That makes the ask side of every ladder
inventory-bounded, and it makes the taker's sell gate a correctness requirement
rather than a nicety.

The same probe produced three further findings, all of which the week then
worked on:

1. **`DONE_FOR_DAY` has never happened.** No `39=3` appears anywhere in the
   gateway FIX log. Orders placed at 00:31 on 8 August survived two 23:59 ET
   boundaries and still rest. An adopted "venue fact" was contradicted, live
   test B1 lost its premise, and open question T14 was raised.
2. **The engine crosses the stale book on every repost.** One measured case: a
   COWB bid at 76.04 was marketable against stale asks at 54.35–55.05 and swept
   eight levels — 920 shares, **$50,366**. The market maker was taking liquidity
   while it intended to rest.
3. **The engine adopts any MM-prefixed order on its own user id.** The
   reconciler cancel-replaced a hand-sent probe order 0.7 seconds later. No
   manual order on the MM user id is safe while the engine runs.

The session note is honest about cost and about its own errors. The first probe
woke an engine that had been quiet for 38 hours, and that is what triggered the
$50,366 sweep. A separate demonstration order filled unintentionally for
$14,600. The instruction "well below the market" was too vague on a book that
carried stale quotes at double fair value. Two claims made mid-session were
retracted in the same note.

**Two normative documents followed within twenty-five minutes.**

`abba4eb` created `vault/components/market-maker/requirements.md` — the market
maker's go-live list. It has 44 requirements in six groups, plus a table of
external gates that are not ours to satisfy:

- **V · The venue contract** (11) — what tZERO requires of us. Unique ClOrdIDs,
  one in-flight request per order, no IOC, per-symbol price bands, and the new
  R-V07 sell rule.
- **L · Lifecycle** (8) — rest-until-gone, one cancel-replace per price move,
  post-first instruction order.
- **Q · Quoting** (9) — a book is never left without a resting side; the ladder
  is non-increasing outward; and the two new red rows, R-Q08 (the ask ladder
  respects `Pos − livS`) and R-Q09 (a published order must not be marketable
  against the live book).
- **D · Determinism and recovery** (6) — seeded randomness only, event sourcing,
  and checkpoint resume equal to a full replay.
- **R · Risk and safety** (6) — one book's fault suspends only that book.
- **S · SNT-1** (9) — the taker's requirements as they touch the maker.
- **X · External gates** (6) — owned by Hasan, Edwin, Rob or legal.

Every row carries a source (`VENUE`, `EDWIN`, `GEORGE`, `OURS`, `SPEC`), a
status, and how it was verified. The document states its own change rule at the
top. Do not silently edit a requirement. Add a dated addendum entry first, then
edit the row and mark it. The addendum is the audit trail.

`cce3d41` created `market-taker-requirements.md` on the same pattern — 44
requirements for SNT-1 in seven groups: identity and account, flow character,
order mechanics, money control, state and recovery, safety, and compliance. Its
purpose is stated plainly: Edwin's reference is the design source, and this
document is what we are accountable for building. Three rows carry weight beyond
the rest:

- **T-F06** — the disposition tilt is the only departure from pure noise, and it
  is flagged to compliance because it makes the taker's flow weakly correlated
  with price.
- **T-O03** — "taker only, never rests" cannot be literally true on a venue with
  no IOC. The substitute order rests for up to the cancel window. Edwin owes a
  re-wording.
- **T-C01** — two house accounts trading with each other must be cleared by
  compliance. Nothing ships before that.

The document closes with an honest state line. The brain, the IOC substitute,
the journal and the reject guard were built and tested. Everything not built was
inventory-shaped: the sell bound, the seeded float, position reconciliation, the
notional cap, the kill switch and activity-state mapping.

`e7e2a79` filed the 09-08b handover, 166 lines, written to be the single entry
point for the next session. It records six things:

- where every repository sat, and what ran live;
- the sell rule;
- the three unfixed live problems;
- five corrections to facts previously recorded as true;
- the new documents and the open decision on them;
- the ordered build queue.

`51f6005` then wired both new requirements documents, the test plan and SNT-1
into the hub and the build index. They now sit inside the mandatory reading
order rather than beside it.

All six commits reached `origin/main` in pull request #23, 10 August.

#### The home page rework plan — a vault document that briefs the app

`ab0165b` is the odd one out of the 09 August six. It touches no market-maker
file. It adds
`vault/components/information-layer/sub-components/discovery-home/home-rework-plan.md`,
101 lines, and it is the brief behind the `inplay-app` home rework.

The problem it states is a conflict of product opinion. Edwin's 8 August mock
has a **trader-first** home page: your money, your teams, the movers. The home
page already scoped in the vault is **games-first**: the day's slate. The plan
merges the two. The dashboard sits on top and the slate sits below it.

It specifies 13 blocks, top to bottom, and marks each one new or kept:

| # | Block | New or kept |
|---|---|---|
| 1 | App bar — news, search, notifications badge | from the mock, Pro lock omitted |
| 2 | Live ticker tape | **reuse** — it already exists on other pages |
| 3 | Greeting card — avatar, daily streak, favourite teams | new |
| 4 | Competitions block — free (13+) against KYC-verified cash (18+) | new |
| 5 | Trading capital card — equity, invested against available, day P&L | new |
| 6 | Sponsored slot — full-bleed rotating house-ad unit | new |
| 7 | Today's movers — biggest swings, tap to trade | new |
| 8 | Watchlist — editable glance list | new |
| 9 | IPO calendar strip | new |
| 10 | Day's-slate game cards, 3 data points maximum | kept |
| 11 | Featured / marquee games | kept |
| 12 | Last-game-of-the-day flag | kept |
| 13 | Leaderboard proximity | kept |

Three further sections make the plan buildable. A mock-to-build table names the
React component in `02-SOURCE/InPlayHomeV1423-SOURCE.jsx` for every block, so
the app ports the anatomy and restyles it. A walkthrough section instructs the
builder to add `data-coach` attributes to each block as it is built. The coach
tour itself lands later as its own feature. A five-step work order then runs
from the layout skeleton, through the blocks that already have data, to the
blocks that need account data. The tour is the last step.

The plan records three decisions taken in the same session. The home page is the
first work item. The Pro paid tier is parked, with no App Store subscription
work before launch. The ticker is reused, not rebuilt.

Its open questions are the useful part for the roll-up. Does the backend already
hold the daily streak and favourite teams? Movers needs a change-ranking source
and the IPO calendar needs the IPO schedule feed. Who implements which blocks —
our side or Hasan's? And Edwin still owes a sign-off on the block order. The
plan also names what comes next after home: the Gamecast updates, blocked on the
pricing engine publishing a per-play decomposition.

Landed on `origin/main` in pull request #23, 10 August.

#### The vault became the operating record of the market-maker build

The market maker ran live games for the first time this week. Every session that
touched it wrote its state back into the vault, because the working guide
(`vault/components/market-maker/working-guide.md`) requires it. westy412 added
60 new documents in the window. 43 of them are session notes under
`vault/components/market-maker/sessions/`. The rest are references, drafts and
system designs. On top of that sit updates to the eight working documents those
sessions touched: `decisions.md`, `open-questions.md`, `parameters.md`,
`requirements.md`, `learnings.md`, `test-plan.md`, `market-taker-requirements.md`
and the `build/` pages.

The largest single addition was a new file. `build-deploy-log.md` was born on
13 August. It holds one row per in-flight change. Each row states the code state
and the deploy state separately, because a merged change is not a running
change. Each deployed row also carries the running coordinates: the engine
generation, the config version and the commit. The next session can therefore
verify the state rather than trust it. The file states its own rule at the top.
Check it before you deploy anything, because a parallel session may hold a
change on the same component.

The `decisions.md` log gained 42 dated entries across the window's commits. A
few of those entries carry dates before 9 August, because they arrived through
merges from `origin/main` rather than being written this week. The entries written this week
include these five:

- The engine must always be quoting (13-08).
- The dual-engine incident, and the single-engine lock that followed it (13-08 evening).
- The de-phasing gate is withdrawn (14-08).
- The 500-share quantity grid is dropped in favour of raw share counts (15-08).
- The taker's live rate becomes one print per second (15-08).

`learnings.md` gained 6 entries, five of them dated inside the window. One is
titled "writing a lesson down does not make it transfer".

Landed on `origin/main` through pull requests #23, #26 and #27, all from
`docs/t0-plain-english-guide`.

#### Edwin's fair-value model, decoded for a reader who is not an engineer

Edwin Johnson sent a handoff bundle on 9 August. It contains the pricing model
behind the front-end mock. George filed the bundle verbatim under
`vault/components/market-maker/reference/edwin-handoff-2026-08-09/` and then
wrote `vault/standards/gamecast-ev-plain-english-guide.html` — 712 lines, a
self-contained HTML page in nine sections with a thirty-second summary at the
top.

The guide is written for a reader who must understand the pricing model without
reading the source code. It explains the one idea the model rests on: a share
price tracks the value of a team's season revenue, not its win probability. It
then works through both layers. Layer 1 is the resting price between games.
Layer 2 is the live price, re-computed play by play. Each layer carries its
formulas in plain code blocks. A worked example for Kansas City reconciles to
Edwin's own output.

Three findings in the guide matter beyond the explanation:

1. **The guide found an error in Edwin's document.** His §1.4 says the Kansas
   City share "rests at 68.93 (up from a lower IPO)". Back-solving his own
   formulas gives an IPO price of about $73.94 against a fair value of $68.93.
   The share is down $5.01, not up. The model behaves correctly. The sentence is
   wrong, and it teaches the wrong direction to anyone who reads the example.

2. **The two pricing models are one model.** Expand Edwin's resting layer and it
   collapses into the model the engine already implements from his own 28 July
   email. The live layer is our own formula multiplied by a time-decay dial that
   reaches 1.0 at the final whistle. Both models therefore bank exactly $5.00 on
   every win. Only the price path differs, and our engine is about 2.9 times
   more sensitive to a first-quarter probability move.

3. **One part of the bundle is worth taking, and one input is a hard stop.** The
   off-field method is new, cheap to build, and fills the one leg of our
   valuation engine that is still mocked. The time-decay dial cannot be built at
   all: it needs a game clock, and the Sportradar probabilities feed carries no
   clock at any point. The guide closes with seven items to put to Edwin.

The guide also caught an arithmetic defect in the off-field formula. Edwin
describes off-field money as a $2.50 per-game pool split between two teams, but
his formula never references the opponent. Two elite teams claim $3.00 from a
$2.50 pool. That matters because settlement pays out of real revenue.

Landed on `origin/main` in pull request #23, 10 August.

#### The daily reference feed — analysed, designed, and deliberately not built

The market maker quotes around a reference value per team. That value is static
today, seeded on 11 August from a CSV. The designed end state is a daily file at
06:00 ET carrying `expected_remaining_wins` and `sigma` for all 170 teams.

George filed a brief on 13 August (`vault/drafts/daily-reference-feed-analysis-brief.md`)
that set the mode explicitly: analyse and design, deploy nothing. The output is
`vault/components/market-maker/systems/daily-reference-feed.md`, marked
"DESIGN — nothing built, nothing deployed".

Its verdict answers three questions. First, the 28 July engine is normative for
the daily file, and the 9 August bundle is the mock's own pricing. Second, Edwin
remains the producer, because §1.5 bans internally generated probabilities; our
side should run the NFL de-vig as a cheap verifier only. Third, the ingestion
design follows the already-decided bucket-plus-database store.

The document then raises the conflict it cannot settle. Edwin's handoff calls
his live price "the number your system needs to reproduce", which is a normative
claim. That became open question **E47**, and the document's instruction is
unambiguous: build nothing from the 9 August bundle until Edwin answers.

Landed on `origin/main` in pull request #26, 15 August.

#### The taker got its own requirements list and its own test protocol

The taker (SNT-1) was treated as part of the maker until this week. Two
documents separated it. `market-taker-requirements.md` is the normative go-live
list, created on 9 August and covered in the first theme above.
`market-taker-test-plan.md` is the second, and it was born on 11 August. It runs
in three strict phases: the taker in isolation, then the maker's own plan, then
the two together. George's stated reason is in the document. A joint failure
must never be the first time either bot meets a case.

The plan names its cases and their statuses. TT2 passed on 10 August with 67
sends, 67 fills and 0 rejects. TT4 drilled the kill switch on 11 August. TT6, an
SR game simulation that drives the taker, still needs a build.

A related proposal sits unapplied on purpose. `drafts/2026-08-12-taker-requirements-addendum-PROPOSAL.md`
adds manual-order and observability requirements to the go-live list, and its
header states it is not applied and awaits George's approval. A builder does not
amend a normative list mid-task.

Landed on `origin/main` in pull request #26, 15 August.

#### The live worker play-by-play investigation — a vault brief that reached another service

This is the one cross-service item in the vault. The 6 August preseason game
happened, and no InPlay system streamed its play-by-play. The 11 August night
session filed `vault/drafts/live-worker-pbp-investigation-brief.md` for a fresh
session to work in `inplay-sportradar-service`.

The findings landed the next day in
`vault/drafts/live-worker-pbp-investigation-findings-2026-08-12.md`. Two of the
brief's assumptions were already out of date, and three code defects were new.
The Sportradar Push entitlement is proven — the real feed accepted the
production key and streamed, which closes gate 1 of the go-live runbook. The
production worker is already in real-Sportradar mode, contrary to the brief and
to the service's own `CLAUDE.md`. The one remaining gate is the `LIVE_GAME_IDS`
environment variable, which is empty. While it is empty, no play-by-play reaches
the app whatever Sportradar sends.

The brief also records one edge worth fixing. Game discovery runs once per UTC
date. A game that starts at or after 00:00Z is therefore adopted only at
kickoff, and it loses its pre-kickoff ramp.

Landed on `origin/main` in pull request #26, 15 August.

#### Live verification and a recovery design, still on the branch

The last three commits of the window record the live proof of the market maker's
fix set, plus one new design. `460fad2` (16-08, 13:38) reports 92,111 due-sweep
ticks with zero missed sweeps across a 13-hour run. It also reports an anchor
chain that held across three consecutive engine cutovers. One of those cutovers
had no usable checkpoint, which is the exact scenario a reviewer had constructed
as a blocker.

`dd0e6a4` (16-08, 18:55) reports both game-end fixes verified live. Ten books
across five finished games were still quoting 13 hours later. The POST_GAME
state was proven by replay over the journal, through the real deployed
functions.

`63115a0` (16-08, 19:20) adds
`vault/components/market-maker/systems/suspension-recovery.md`, 161 lines. Its
finding reverses the premise of the work: automatic recovery already exists,
because the restriction function is pure and leaving the Suspended state has no
dwell. A book therefore re-opens by itself the moment its inputs recover. The
15 August dead end was an input that could never recover — a finished game's
feed — and not a latch. The document then specifies four real gaps, including a
terminal-suspension alarm and derived state that a fresh journal forgets.

All three commits sit on `docs/t0-plain-english-guide` and have **not** reached
`origin/main`.

### Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `docs/t0-plain-english-guide` | westy412 | 34 | `origin/main` for 31 of 34, through PRs #23, #26, #27 — **3 commits still ahead** | The market-maker working branch. Older than the window. Despite its name it now carries all MM documentation work, not only the plain-English guide. It also carried the 09-08 requirements documents and the app home rework plan. |
| `origin/main` | westy412 | 3 | mainline | The three pull-request merge commits: #23 (10-08), #26 (15-08), #27 (15-08). |
| `docs/advertising-outbound-onboarding` | Brett StClair | 1 unique | **open** | Out of scope. Its one unique commit duplicates a commit already on `origin/main`. |

Two further commits belong to no branch at all. `a8d60e4` and `6bcbb22` are
`Claude Code` WIP rate-limit checkpoints. `git branch -a --contains` returns
nothing for either, so both are unreachable from every branch and every remote.
They are agent commits on George's branch, superseded by the real commits that
followed. They are recorded here for completeness and cost nothing.

### Still open

- **`docs/t0-plain-english-guide`, 3 commits ahead of `origin/main`.** Commits
  `460fad2`, `dd0e6a4` and `63115a0`, all dated 16 August, the last at 19:20 on
  the final day of the window. **In flight, not abandoned** — a fourth pull
  request is owed. Two of the three record live verification of changes that are
  already deployed, so the code is ahead of the document, not behind it. The
  third is a new design document that nothing has built yet.
- **`docs/advertising-outbound-onboarding`.** Brett's branch, out of scope. Its
  one unique commit `7bf9c49` duplicates `93e7279`, which is already on
  `origin/main`. Nothing appears to be lost if the branch is deleted, but that
  is Brett's call, not a finding of this file.
- **Two unreachable agent commits.** `a8d60e4` and `6bcbb22`. No action is
  needed. They will be removed by garbage collection.

---

## 2 · `specs`

### Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 5 — all westy412, all on `main`
- **Branches touched:** 1 — `main`, the mainline, no remote configured
- **Busiest day:** 2026-08-15 (4 commits)

### Themes

#### The specs folder became a repository

`e1dff70` on 14 August is the first commit in the repository's history. It added
90 files and 21,415 lines in one commit. That import brought twelve spec folders
under version control, the oldest dated 8 May 2026.

Until this commit the written plans behind every InPlay service lived in an
unversioned folder. There is still no remote, so the history exists on one
machine only.

#### Every spec, and the service it belongs to

This is the map the roll-up needs. Status is taken from each spec's own `Meta`
block, not inferred.

| Spec folder | Service / repository | Status in the spec |
|---|---|---|
| `2026-05-08-admin-panel-module-approval` | `inplay-admin-api` + `inplay-admin-panel` | complete |
| `2026-05-18-client-portal-docs-viewer` | `inplay-admin-panel` + `inplay-admin-api` | complete |
| `2026-05-30-feedback-mechanism-global-website` | `inplay-global-website` | complete |
| `2026-06-03-sportradar-service` | `inplay-sportradar-service` | complete (Phases 1–4) |
| `2026-06-04-app-sportradar-integration` | `inplay-app` (primary) + `inplay-sportradar-service` | in-progress |
| `2026-06-08-phase2-live-ingestion` | `inplay-sportradar-service` (worker) + `inplay-app` (realtime) | in-progress |
| `2026-07-03-sr-ipo-data-domains` | `inplay-sportradar-service` + `inplay-app` | complete |
| `2026-08-02-insights-founder-memos` | `inplay-global-website` | draft, review 001 applied |
| `2026-08-11-preseason-schedule` | `inplay-sportradar-service` (primary) + `inplay-app` | draft |
| `2026-08-12-admin-trading-observability` | `inplay-market-maker` + `inplay-admin-panel-trading` + `inplay-vault` | in-progress |
| `2026-08-14-mm-python-fix-set` | `inplay-market-maker` (primary) + `inplay-fix-gateway-go` (one ops route) | in-progress |
| `2026-08-15-live-pbp-expansion` | `inplay-sportradar-service` + `inplay-app` | scoping — **untracked, never committed** |

#### The MM Python fix set carried four of the five commits

Four commits after the import all serve one spec folder,
`2026-08-14-mm-python-fix-set`. It is the written plan behind the market maker's
week. Its deadline section names the reason. The NFL secondary market opens on
7 September, and the spec's Phase 4 gate must clear well before that date.

The four commits track the spec through its phases:

- `5da8a74` — through the Phase 3 reviews. Added `scan-sweep.md`,
  `profile-cb4.md` and the CB4 profile evidence.
- `c323d8f` — the CB4 rig verdict. The prune fix moved the missed-sweep ratio
  from 28.76% to 0.00% on the production VM shape. Also added
  `reviews/review-002-f5-merge-train.md`, the seven-reviewer adversarial review
  of the merge train.
- `0db2918` — the GATE v2 results, 494 lines, plus the deploy ceremony. Clause 1
  of acceptance criterion AC4 passes at both 1× and 10× load. Clause 2 fails as
  written and the commit says so plainly: the failure is mis-specification, not
  a defect, because every DRAIN_CAPPED event is the boot re-stand.
- `e9ae87f` — corrections to the gate results. Three of them matter. The rig
  drifts about 31% within a single day, so only adjacent test arms may be
  compared. The whole 16.4× increase sits inside one stage, the venue drain.
  The Go datum was re-derived, and NCAA Saturday's load now sits about 6.3×
  beyond it, not "between" as the earlier figures implied.

#### The evidence is committed alongside the specs

`0db2918` added 13,408 lines, and most of them are machine output: three
`ticks.csv` files totalling about 10,900 rows, profile JSON, manifests and run
logs under `profiles/gate-v2/`. This is a deliberate choice to make a
performance claim checkable rather than quotable. The same pattern appears in
`5da8a74` and `c323d8f` for the CB4 arms.

### Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `main` | westy412 | 5 | `main` (mainline; no remote configured) | The repository's entire history. The import, then the MM Python fix set through its phases. |

### Still open

- **`2026-08-15-live-pbp-expansion/` is untracked.** `git status` reports it as
  an untracked directory. Its `scoping.md` is 134 lines and describes three
  additions to the Phase-2 live contract for `inplay-sportradar-service` and
  `inplay-app`: timeouts remaining, current-drive summary, and a full play list.
  Addition A is marked DONE on 2026-08-16. **In flight, not abandoned** — but
  the work is done and the plan is not committed.
- **`2026-06-08-phase2-live-ingestion/contract.md` has uncommitted changes.**
  Three added lines add `homeTimeoutsRemaining` and `awayTimeoutsRemaining` to
  the live snapshot contract, with a mapping row. The comment in the diff dates
  the addition to 2026-08-16 and states no version bump, per the contract's own
  §7 rule for additive optional fields. This is a **live contract change between
  two services that is not in git.**
- **The repository has no remote.** All five commits, and the twelve spec
  folders they carry, exist on one machine only.

---

## 3 · `inplay-global-website`

### Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 1 — westy412
- **Branches touched:** 2 — `origin/main` and `origin/dev`, both at the same commit
- **Busiest day:** 2026-08-12 (1 commit)

### Themes

#### One merge, one copy edit, and the Insights section promoted

`c57ccc0` on 12 August merges `main` into `dev`. Both parents are dated
5 August, so the week's only change is the merge itself.

The merge does two things. It picks up Max Kingaby's copy edit, which removes
the full stop after "Sports" in the positioning line. `"Trade Sports. As
Stocks."` becomes `"Trade Sports As Stocks."` in three places:

- the home hero headline (`src/components/section/home-hero.tsx`);
- `siteConfig.positioningLine` and the SEO default title (`src/config/site.config.ts`);
- the favicon web manifest description (`public/favicons/site.webmanifest`).

It also carries the Insights founder-memos work — 17 files, about 1,062 added
lines — from `dev` onto the same commit as `main`. That is the section at
`/insights` for Edwin Johnson's weekly memos, written to the
`2026-08-02-insights-founder-memos` spec in the `specs` repository. Both
`origin/main` and `origin/dev` now point at `c57ccc0`, so `dev` and `main` are
level.

### Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `main` / `dev` | westy412 | 1 | `origin/main` and `origin/dev` (both at `c57ccc0`) | Merge `main` into `dev` to pick up the positioning-line edit before promotion. |

### Still open

Nothing from this window. Four other branches exist on the remote
(`feature/insights-founder-memos`, `feat/newsroom`, `feature/app-store-badge`,
`Max's-edits` and its merge branch), but none has a commit inside the window, so
this file does not judge their state.

---

## Commit appendix

Grouped by repository, then by branch. Brett StClair's 22 vault commits are
excluded, as instructed.

### `inplay-vault` — branch `docs/t0-plain-english-guide` (34 commits)

`63115a0` · `2026-08-16` · westy412 · mm: suspension recovery design — auto-recovery already exists; four real gaps specified
`dd0e6a4` · `2026-08-16` · westy412 · mm: both game-end fixes verified live — zero suspensions in 13 h, POST_GAME proven by replay
`460fad2` · `2026-08-16` · westy412 · mm: the fix set is proven live — 92,111 due-sweep ticks, zero missed; the anchor chain held across three cutovers including a no-checkpoint hop
`e5999b0` · `2026-08-15` · westy412 · Merge remote-tracking branch 'origin/main' into docs/t0-plain-english-guide
`01af913` · `2026-08-15` · westy412 · mm: the taker timing audit + the stale-price bug — found, fixed, deployed
`6624238` · `2026-08-15` · westy412 · mm: the fix-set cutover — supervised33/CFG-0028, ANCHOR_SEED carried 6 anchors, PANT un-wedged
`47fb2ad` · `2026-08-15` · westy412 · mm: the Python fix set — build, review, merge and the rig verdict (15-08)
`ec7b827` · `2026-08-15` · westy412 · mm: session closed — machine independent (supervised26/CFG-0024), open items owned elsewhere
`d760338` · `2026-08-15` · westy412 · Merge origin/main: fold the digest's duplicate T15 (STX daily reseeder ask) into T19
`8772b2c` · `2026-08-15` · westy412 · mm/taker: the 10-08 → 14-08 working-doc sweep — six sessions of state
`63e0765` · `2026-08-14` · westy412 · mm(cb1): the validation arm settles R1 — and the bar was never measured
`6d68877` · `2026-08-14` · westy412 · mm(cb1): the tick profile — the venue ack drain is 98% of the tick
`a386d33` · `2026-08-14` · westy412 · log(mm): flag IPTCBENG/IPTCLION dead live win-probs for triage (app side ruled out)
`92b103e` · `2026-08-14` · westy412 · mm: addendum 6 — first live games ran the full path; dead-man spiral at live load throttled mid-game (supervised26/CFG-0024)
`3c47384` · `2026-08-13` · westy412 · mm: the 08-13 evening — converger deployed, dual-engine incident, the 1.0s sweep tolerance ruling, the single-engine lock (supervised25/CFG-0023)
`fa99c64` · `2026-08-13` · westy412 · mm: addendum 4 — the ACTIVE/DEFENSIVE flapping traced to the portfolio-wide missed-sweep counter (George's catch)
`2436c04` · `2026-08-13` · westy412 · mm: step-4 design pass — target-book staging + bounded round-robin converger (proposal for George)
`050af80` · `2026-08-13` · westy412 · mm: brief filed for the daily-reference-feed analysis session (analyse Edwin's material, design, no deploy)
`1830523` · `2026-08-13` · westy412 · mm: live-game watch prep — receipts on maker/taker/publisher, NE-IND 23:30Z correction, VM-side watch armed
`c872d72` · `2026-08-13` · westy412 · mm: boundary verdict PASS — close/open fired clean on supervised21, no storm; MISSED_SWEEPS finding filed (engine time on ack bursts)
`a053af9` · `2026-08-13` · westy412 · mm: always-quoting steps 1-3 DEPLOYED as supervised21/CFG-0020 — session note + decision record
`c1331ef` · `2026-08-13` · westy412 · mm: progress-aware heartbeat built (always-quoting step 3) — threshold row added, decision extended, runtime page updated
`2641cba` · `2026-08-13` · westy412 · mm: N31 group commit built (always-quoting step 2) — question closed, §7.4 supersession recorded, build pages updated
`14b780e` · `2026-08-13` · westy412 · mm: bounded drain per tick built (always-quoting step 1) — ruling logged, cap rows added, runtime page updated
`2c005ab` · `2026-08-13` · westy412 · mm: the full-market marathon (08-11→08-13) — five session notes + working docs
`d65ffeb` · `2026-08-10` · westy412 · mm: session note — the 10-08-b main merge, conflict rules applied, digest renumbering recorded
`d69becf` · `2026-08-10` · westy412 · Merge origin/main: reconcile the tZERO sweep + meeting digests with the MM branch docs
`6738288` · `2026-08-10` · westy412 · mm: SNT-1 float + sell gate session docs, Edwin handoff filed, 08-10 run forensics session note, gamecast EV plain-English guide
`51f6005` · `2026-08-09` · westy412 · mm: hub + build index link the requirements docs, the test plan, and SNT-1 — the new docs now sit in the mandatory reading path
`e7e2a79` · `2026-08-09` · westy412 · mm: handover 2026-08-09b — repo/live state, the sell rule, three unfixed live problems, corrections to recorded facts, and the ordered build queue
`cce3d41` · `2026-08-09` · westy412 · mm: market-taker-requirements.md — the normative list for SNT-1 (identity, flow character, order mechanics, money, state, safety, compliance, external gates) with a dated addendum; linked from the systems page and working guide
`abba4eb` · `2026-08-09` · westy412 · mm: requirements.md — the normative go-live list (venue contract, lifecycle, quoting, determinism, risk, SNT-1, external gates) with a dated addendum; linked from the working guide
`2da621e` · `2026-08-09` · westy412 · mm: the sell rule decoded (sellable = Pos - livS, whole-order reject) — decisions 08-09, venue bands + risk params, venue build page, B1 premise falsified, T14/T15, session note
`ab0165b` · `2026-08-09` · westy412 · docs: home page rework plan from Edwin's Aug 8 handoff — block list, mock mapping, work order

### `inplay-vault` — branch `origin/main` (3 commits)

`cda17c2` · `2026-08-15` · westy412 · Merge pull request #27 from Novosapien/docs/t0-plain-english-guide
`9684938` · `2026-08-15` · westy412 · Merge pull request #26 from Novosapien/docs/t0-plain-english-guide
`d6ba357` · `2026-08-10` · westy412 · Merge pull request #23 from Novosapien/docs/t0-plain-english-guide

### `inplay-vault` — no branch (2 commits, unreachable)

`a8d60e4` · `2026-08-16` · westy412 (agent commit) · WIP: Claude Code rate-limit checkpoint (9439d47d)
`6bcbb22` · `2026-08-15` · westy412 (agent commit) · WIP: Claude Code rate-limit checkpoint (f2616bbd)

### `specs` — branch `main` (5 commits)

`e9ae87f` · `2026-08-15` · westy412 · specs: gate-v2 corrections — within-day drift, the stage breakdown, and the Go datum re-derived
`0db2918` · `2026-08-15` · westy412 · specs: the GATE v2 results — AC4 miss clause passes on merged main; the drain is superlinear in ack count
`c323d8f` · `2026-08-15` · westy412 · specs: the CB4 rig verdict — AC4's miss ratio 28.76% -> 0.00% on the production VM shape
`5da8a74` · `2026-08-15` · westy412 · specs: mm-python-fix-set through Phase 3 reviews — scan-sweep, profile docs, progress, drift log
`e1dff70` · `2026-08-14` · westy412 · specs: snapshot — mm-python-fix-set through Phase 1 (spec, reviews, progress, CB1 profile + evidence)

### `inplay-global-website` — branch `main` / `dev` (1 commit)

`c57ccc0` · `2026-08-12` · westy412 · Merge main into dev: pick up the positioning-line edit before promotion
