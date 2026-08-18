---
description: "N40's engine mechanism found: SR's post-final settled readings re-arm the live regime and the book suspends when the feed stops — fixed as MM PR #45"
---

# 2026-08-15 — the settled-echo guard: why finished books suspend (MM PR #45)

> **Who:** George + Claude (the price-lag session, continued)
> **Type:** live forensics → root cause → build
> **Refs:** MM PR #45 `fix/freshness-settled-guard` @ `1afc9a3` (off
> `main@0b9f601`) · open-questions N40 addendum 15-08 ·
> build-deploy-log row · build/ingestion (two corrections) ·
> repo BUILD-LOG 2026-08-15d

## What we did

1. **Investigated the price-lag complaint first** (earlier in the same
   session): measured on supervised32's live journal — every SR reading
   arrives already **10–13 s old** (n=527, p50 11.9 s, floor 10.4 s);
   our own leg (reading → order live on tZERO) is well under a second.
   The lag is Sportradar's, not ours. Incident report drafted for Cody;
   the `Age`/`Cache-Control` header probe is the next step (S9).
2. **George reported the four live books suspended** (VIKI/GIAN/PANT/
   BILL), then BEAR/BROW followed. Traced live on supervised33: each
   book's last order lands ~20 s after its game's last bus message
   (22:01–22:05Z). All six of the slate's books, same shape as 13/14-08.
3. **Found the engine-side mechanism N40 was missing.** The finals WERE
   consumed: `OFFICIAL_RESULT` accepted at each whistle (20:01–20:04Z),
   `_note_freshness` set `live=False` correctly. Then SR's post-final
   SETTLED readings (p_home = 1/0, ~2 min after each final — verified
   for all three games) hit the `PROBABILITY_UPDATE` branch, which
   re-arms `live` unconditionally and restores `kickoff_time` —
   silently undoing the final. The books survived only on the
   publisher's re-offers — ✎ corrected by the sportradar session: the
   TESTING pool's keep-polling values (2 s for a 7,200 s window, image
   952d8be), not production's 600 s watch — and suspended 20 s after
   that window expired. ⭐ Consequence: **keep-polling was already
   running tonight and the books died anyway** — polling alone cannot
   save a live-regime book; the guard is the fix. The valuation engine
   already refuses these readings (`[settled]`); the freshness tracker
   had no twin.
4. **Built the guard — MM PR #45** in a worktree off `main@0b9f601`:
   `_FreshnessState.settled_game_id` set by `OFFICIAL_RESULT`; a
   reading whose `game_id` matches updates `last_reading_time` only.
   Keyed to the GAME so a stale final can never stop the next fixture
   arming. Checkpoint schema **6 → 7**. 4 new tests (incident sequence
   end-to-end, next-fixture re-arm, replay identity, checkpoint round
   trip); **1,240 tests, ruff + mypy --strict clean.** Not merged, not
   deployed (the 14-08 freeze).
5. Vault: N40 addendum · build-deploy-log row · ingestion.md corrected
   twice (below).

## What we learned

- ⭐ **SR serves a SETTLED probability for minutes after the whistle**
  (p=1/0 readings 2 min post-final on all three games). Legitimate
  data; our freshness tracker mishandled it.
- **N40's "nothing consumes the game-end fact" was wrong** — the engine
  consumes it and then loses it. The failure is an asymmetry: valuation
  had the `[settled]` guard, freshness did not.
- **Publisher #38 is a mitigation, not the cure.** Keep-polling stops
  the suspension but (without #45) holds finished books in the LIVE
  regime at pre-final prices — the COMM/DOLP exposure.
- **Two vault lines were false, now corrected in ingestion.md:** the
  deployed publisher polls LIVE at **~2 s per pool** (`poll_live_s =
  2.0`; the "500 ms" line never reached its config — bus arrivals of
  ~1.2 s are two pools out of phase), and retirement's killer is the
  **immediate 2 s → 600 s drop at the final**, not the 1 h retirement.
- SR docs: probability changes are only captured when they move
  **> 0.1%** — a frozen number on a decided game is expected, not a
  fault. And their `last_updated` is second-resolution with multiple
  distinct readings per stamp (the other session's finding; the
  engine's dedup key drops ~8% of genuine moves — separate defect,
  theirs to fix publisher-side, ours engine-side, unowned row yet).

## What went wrong / got stuck

- First analysis mis-read the finals' timing (took duplicates for first
  arrivals, "final +20 s = suspension"). The real gap is final +2 h;
  the +20 s runs from the last MESSAGE. Corrected before build.
- The earlier "150 ms reading→ack" claim was demoted to "well under a
  second" — the matched ack is not provably causal under the 500 ms
  republish pulse.

## Decisions made

- None of George's; the build was his instruction ("build the guard").
  The E11 post-final policy call stays open and is explicitly NOT
  decided by #45.

## Questions opened / closed

- N40: engine mechanism closed (addendum on the row); the policy half
  (E11) and publisher #38-to-production remain open.
- S9 unchanged: the 10–13 s upstream lag stands measured; header probe
  owed.

## Addendum 22:46–22:49Z — MERGED AND DEPLOYED (George: "deploy this change now")

- **#45 merged as `main@006eb96`; engine cut over to
  supervised34/CFG-0031** (fresh journal; env captured from the running
  process, 3 vars patched; ceremony in the build-deploy-log row). The
  freeze was superseded by George's explicit go; no games live (R11
  clean).
- **ANCHOR_SEED carried 10 anchors** from supervised33 (the lenient
  reader took the schema-6 checkpoint + 531 tail events — exactly the
  review-H1 design point). Replayed 1; **books=180**, was 176.
- **All six suspended books recovered, two-sided at SETTLED prices:**
  BILL 79.92/80.29 · BEAR 71.10/71.31 · VIKI 65.59/65.72 ·
  BROW 44.63/44.86 · PANT 53.11/53.30 · GIAN 55.89/56.11 — winners up,
  losers down. Taker restarted (same SNT-CFG-0024/snt21), filling.
- ⚠ Learned during the ceremony: supervised33 ran **CFG-0028 — a
  config-version REUSE** (supervised30's); CFG-0031 chosen clear of
  0028/29/30. And the boot healer is still inert (`MM_GATEWAY_OPS_URL`
  unset, inherited env) — configure it or keep the fresh-journal
  ceremony.
- ⚠ Honest caveat: the guard's end-to-end proof is TOMORROW's slate
  (final → settled echo → books stay up). Tonight's recovery came from
  the fresh journal + anchors; the guard protected nothing yet because
  no echoes flow post-retirement.

## Addendum 23:0x–23:5xZ — the guard's live proof, and two activity findings

- ⭐ **The guard passed its live proof early.** ~23:03Z a publisher
  restart re-published ENTIRE game timelines onto the bus (1,000+
  historic readings per game, distinct stamps, one `Fetched-At`); the
  fresh journal accepted them all. **No book re-armed, none suspended,
  books=180 throughout.** Without #45 that burst re-suspends every
  settled book ~20 s after it ends.
- **George's report — finished books skip POST_GAME — two causes:**
  (1) the fresh-journal cutover forgets `final_time` until a re-offer
  re-mints the final (22:49 → 23:01 gap; the anchor seed carries
  valuation, not freshness — folds into the auto-recovery design);
  (2) `final_time` was stamped from the minting reading's PROVIDER
  stamp — the last probability move, hours old on a settled game
  (23:14 final carried 22:33; another carried 17:05 → POST_GAME never
  visible). **George's ruling: POST_GAME starts when the game IS
  finished → built as MM PR #46 (`[final-is-receipt]`,
  `final_time = env.receive_time`), 1,241 tests, unmerged.**
- Watch item: 71548114 was live during the 23:03 burst — historic
  prices may have transiently moved its book (`refused=1327`, the
  marketable guard working). P&L glance owed, not an alarm.

## Addendum 16-08 12:40Z — BOTH FIXES VERIFIED LIVE

#46 merged (`main@d2b2fb5`) and deployed 15-08 23:37–23:39Z as
**supervised35/CFG-0032** (fresh journal, ANCHOR_SEED 12 anchors,
books=180). After 13 h / 93,000 ticks:

- ⭐ **ZERO SUSPENSIONS.** All ten books of the five finished games were
  still quoting at 12:38Z — 13 h after their games ended. On 15-08 the
  equivalent books were dead 20 s after their feed quietened, until a
  restart. `books=180` for every tick of the run.
- ⭐ **POST_GAME PROVEN, not inferred.** Activity state is NOT journalled
  (verified: zero occurrences), so it was replayed through the REAL
  deployed functions — `_note_freshness` building the state from the
  journal's accepted events, `_activity_for` reading it. **Seven games,
  fourteen books, all `post_game` at +30 s / +30 min / +59 min and
  `overnight` at +61 min.** Harness: `/tmp/replay_activity.py` on the VM.
- ⭐ **#46 was load-bearing.** The receipt-vs-provider-stamp skews:
  games 71548108/110/112 carried **209–213 min** (their POST_GAME window
  would have expired hours BEFORE the engine learned the game was over —
  George's "straight to overnight" report), 71548114/116 carried 33 and
  20 min, and the two unassisted overnight games 17 and 19 min.
- **The unassisted proof:** 71548118 (RAVE/EAGL, final 01:52:38Z) and
  71548120 (SEHW/COWB, 03:00:26Z) finalled with no human intervention
  and behaved identically to the deploy-re-minted five.

⚠ **Residues (unchanged):** activity transitions are still not
journalled — §6.4 journals market-state changes but not this, which is
why a replay harness was needed at all; and a fresh-journal cutover
still forgets `final_time` until a re-offer re-mints the final. Both
belong to the auto-recovery design.

## Next

1. ~~George's merge/deploy word on MM #46~~ ✅ merged + deployed
   15-08 23:39Z; ~~verify on the next slate~~ ✅ **VERIFIED 16-08**
   (addendum above).
2. **Journal the activity transition** (small; makes this question a
   grep instead of a 3.6 GB replay).
2. **George's ask: design the auto-recovery mechanism** — a suspended
   book must find its own way back (the N40 "every suspension needs a
   defined exit" requirement; inputs: recovered feed, a settled
   transition off `OFFICIAL_RESULT`, manual release via the ops UI).
3. Deploy publisher **#38** to production (mitigation; proven on
   testing).
4. The engine's dedup key drops same-second SR readings (~8% of moves)
   — needs its own row/PR.
5. George rules E11 (deliberate post-final behaviour: settlement
   pricing, re-open, reseed).
6. The S9 header probe (`Age`/`Cache-Control`) against a live game.
7. Set `MM_GATEWAY_OPS_URL` on the VM so the boot healer arms.
