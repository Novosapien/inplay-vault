---
description: "The ladder-shape investigation: the sizes are stale by design under N10, the Go port is faithful, and two live attempts to change it both failed"
---

# 2026-08-20 (d) — The ladder shape, and two fixes that failed live

> **Who:** George + AI session.
> **Type:** live operations + build. Four deploys to `mm-2`, two of them reverted.
> **Refs:** [[market-maker/sessions/2026-08-20-c-stranded-book]] · N10 · N62 ·
> Go PRs `2a55d74`, `fa3dfc2` on `feat/phase-3-ingestion`.
> **⚠ Ended with the Go maker STOPPED and unusable. The Python maker is the fallback for tonight.**

## What we did

- Started the Go maker on the deliver-policy fix (`5988827c`, `CFG-0040-GO`,
  `go-run04`, `MM_READINGS_FROM_NEW=on`). The readings leg bound at stream HEAD
  and delivered 395 readings. That part worked.
- George reported the books were wrong: the level sizes did not fall as the
  ladder went outward, and some quantities looked about twice what they should be.
- Measured it. Built a fix. The fix failed live. Built a second fix. George
  stopped the run before it was verified.

## What we learned

### ⭐ The ladder sizes are stale BY DESIGN, and the design is N10

The reconciler keeps a resting order when its price is still wanted, at whatever
size it carries (`reconciler.go:266`). That is Edwin's rest-until-gone (N10,
23-07). The size ladder is re-drawn every quote version (§5.7.3). So a kept
order holds the draw that posted it, and its neighbours hold the current one.

Measured live across 180 books at one instant:

```
SIZE-INVERTED ladders            197 of 360  (54.7%)
age spread within one ladder     median 39 s · max 277 s
largest step-up observed         2.16x   (IPTCSALJ bid 2,926 -> 6,328)
```

⭐ **The arithmetic proves it is version mixing, not variation.** Sizes are
`10,000 × 0.72^i` varied by `VF ∈ [0.75, 1.25]`. Inside ONE version the largest
possible step-up is `0.72 × 1.25/0.75 = 1.20`. Steps of 2.16, 1.46 and 1.35
cannot come from one version.

### ⭐ The Go port is faithful. This is Python's behaviour too

Proven three ways, because reading the comments was not enough:

- **960 quantity ladders byte-identical** to the pin (5 securities × 4 quote
  versions × 6 EPRs × 2 sides × 3 to 6 levels).
- **The venue differential fuzz passes fresh** (`-count=1`, 4 seeds, SHA-256 of
  state at every step against Python's recorded script).
- **The quoting gate passes** — target books field for field over 1,089 readings.
- The KEEP pass is the same logic in `reconciler.go:266` and `reconciler.py:372`.

⚠ We could NOT confirm it on Python's live book. `mm-1` has been stopped since
19-08 and the retail wire log carries only the IPO offering from 11:10 onward.
The comparison is code-level and fixture-level only. **George states he watched
both books and Python's decayed correctly. That observation is unexplained.**

### ⚠ `base_size` is 10,000 in BOTH engines

`quantity.go:29` and `dictionary.py:129` both hold `10,000`. Edwin's agreed
resting size is **500 to 3,000** (✅ 17-08), countered at ~550 on 18-08. That
parameter round has landed in neither engine. Measured top-of-book median 9,656,
and 9.69 M shares resting across 180 books.

## What went wrong

### 1 · ⚠⚠ I called it a cancel failure. It is not

I reported "stale orders survive a re-quote — this is the cancel bug" before
reading the KEEP pass. The cancels work. The behaviour is the ruling. George
had to be told the correct diagnosis after the wrong one.

### 2 · ⚠⚠ The first fix took the books dark, live

`MM_REQUOTE_CLEAR_FIRST` cancelled every order whose drawn size had moved and
posted the new ladder on the NEXT pass. Sizes are re-drawn every version, so
EVERY order mismatched on EVERY version and every book spent a whole pass empty:

```
books quoting per sample (10 samples, 3 s apart)  72 to 97 of 180
books quoting in ALL ten samples                  11 of 164
books quoting in <= 2 of ten samples              42
```

George saw it on the panel before the measurement finished — teams appearing and
disappearing. ⚠ **The unit tests passed. Nothing in them measured how often a
book is absent**, because every test asserted on ONE reconcile call.

### 3 · ⚠ The second fix was never verified

Rebuilt as a resize in place: a level whose price is still wanted is REPLACED to
the current draw (35=G), so one order holds the level throughout. `make gate`
PASS, deployed as `7db40ce4` / `CFG-0042-GO` / `go-run06`. George stopped the run
during the first measurement. **The resize build is UNVERIFIED live.**

### 4 · ⚠ I reported a bad sample as fact

Read `/orders/mm` once, got 10 orders of 900,000 shares, and reported the IPO
offering had returned. The next read showed 1,648 orders at normal sizes. The
first read was wrong and I had not checked it before saying it.

## Decisions made *(mirror into [[market-maker/decisions]])*

- **George: the old quotes must be cleared before the new quotes go out.** This
  reverses N10 and needs Edwin told.
- **Clearing must never empty a wanted level.** A price the ladder still wants
  is resized, not cancelled and re-posted.
- **The Go maker does not trade tonight.** The Python maker is the fallback.

## Questions opened *(mirror into [[market-maker/open-questions]])*

- **N63** — `base_size` 10,000 versus Edwin's agreed 500 to 3,000. In neither engine.
- **N64** — George observed Python's live books decaying correctly and the Go
  books not. Unit parity says they are identical. The observation is unexplained
  and no Python live book exists to re-measure.

## Next

1. **Do not start `mm-2`.** It holds `MM_REQUOTE_CLEAR_FIRST=on` and the
   UNVERIFIED resize build. Set the flag off before any start that is not a test
   of that build.
2. Repoint the Python maker at the MM gateway — ⚠ **bump its
   `MM_CONFIG_VERSION` first.** The Go maker burned `CFG-0038` ids at the venue
   today, the mint is deterministic, and tZERO refuses a duplicate for the day.
3. Capture a Python live book while it runs tonight, and measure its ladders the
   same way. That is the only way to settle N64.
4. Then verify the resize build against that measurement.
