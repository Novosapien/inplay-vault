# InPlay Global — Engineering Handoff for George Westbrook / novosapien

Prepared by Edwin Johnson · InPlay Trading Challenge mock (build of Aug 8, 2026).

This bundle is the current front-end mock plus the **fair-value (EV) pricing model** that drives share prices. Start with `03-PRICING/` — that's the part you specifically need.

---

## What's in here

### 01-DEMO/
- **InPlay-Demo.html** — the whole app, self-contained. Double-click to open in any modern browser (Chrome/Safari). No install, no build step. This is the fastest way to see current state. It's a phone-shaped mock; use the browser device toolbar for the intended look.

### 02-SOURCE/
- **InPlayApp-ASSEMBLED.jsx** — the entire app as one React file with all image assets inlined. This is what the demo is built from. Use it to read/port code.
- **InPlayHomeV1423-SOURCE.jsx** — the same app but with 7 image assets swapped for text placeholders, so the file is diff-friendly and small. **Edit this one**, then rebuild (see BUILD below).
- **assets/** — the 7 base64 image files that fill the placeholders.

### 03-PRICING/ ← read this first
- **InPlay-Handoff-George-FairValue-EV.md** — **how we compute a share's current fair value (the "final EV").** Two layers: resting EV (`seasonFair`) and live in-game EV (`lgValuePrice`), every formula, constant, and a worked example. This is the core deliverable.
- **InPlay-Gamecast-Pricing-Spec.md** — the full v3 spec with the design rationale and all the decisions behind the model. Reference/background.

---

## Rebuilding from source (02-SOURCE)

The assembled file = the source with 7 placeholders replaced by the base64 asset strings. Placeholder → asset map:

| placeholder        | asset file            |
|--------------------|-----------------------|
| `__IPG_URI__`      | `ipg_b64.txt`         |
| `__IPG_WORDMARK__` | `ipg_welcome_b64.txt` |
| `__IPG_HOUSE__`    | `ipg_house_b64.txt`   (used 6×) |
| `__TZERO_LOGO__`   | `tzero_b64.txt`       |
| `__SPORTRADAR__`   | `sportradar_b64.txt`  |
| `__PERSONA__`      | `persona_b64.txt`     |
| `__EJ_AVATAR__`    | `ej_avatar_b64.txt`   |

To produce a runnable bundle: replace each placeholder with the contents of its asset file to get the assembled `.jsx`, then bundle it with React 18 + react-dom 18 + lucide-react 0.383.0 (esbuild works; `process.env.NODE_ENV='production'`). The demo HTML in 01-DEMO is exactly this bundle inlined into a minimal HTML shell. No browser storage APIs are used.

---

## Current build state (what's real vs. mock)

- **Front-end only.** All game action, order books, and prices are simulated in-browser. There is **no** live Sportradar feed, no real matching engine, no backend yet — that integration is the ceiling and it's your side.
- **32 NFL teams** are fully live, tradable, and backtestable; each has its own L2 order book and a play-by-play game engine (clock, timeouts, 4th-down logic, OT, penalties, injuries).
- **Pricing is value-based** (the reason for the pricing docs): share price tracks enterprise value, not win probability. WP is only an input.
- Two engines run identical math: `makeLiveGame` (live store) and `lgSimulate` (pure replay). Port pricing from either.

## Known open items (your side / next)
- **Sportradar WP backfill** for historical game-week replay.
- Live data feeds to drive `lgValuePrice` in production: live win probability, score/clock, injuries, plus each team's IPO price and results-to-date (see the EV doc, §4).
- The simulated "market noise" that sits on top of fair value is sim-only and gets replaced by real order flow — do not port it as pricing (EV doc, §3).

Questions → Edwin.
