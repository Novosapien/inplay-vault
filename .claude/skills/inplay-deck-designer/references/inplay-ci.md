# InPlay Presentation CI (the signed-off design system)

> **When to read:** Before writing any HTML in either phase. This is the design system extracted from the client-signed two-pager. Match it exactly.

**Canonical source:** `/Users/brettstclair/programming/inplay/inplay-advertising-2pager.html`. The client has signed off on this look and feel. When in doubt, open it and mirror its treatment. If any value below ever disagrees with the two-pager, the two-pager wins: re-extract and correct this file.

---

## Palette

Light, editorial, premium. Paper surfaces with deep navy ink, one hot-orange accent, green reserved for positive proof points. This is NOT the dark immersive theme used by the interactive stock-expert explainers; presentations follow the two-pager.

| Token | Hex | Use |
|-------|-----|-----|
| `--navy` | `#06122B` | primary ink, headings, masthead/callout bands, title slides |
| `--navy-2` | `#0A1A36` | secondary navy, gradients and depth on navy surfaces |
| `--orange` | `#FF6A1F` | InPlay orange: accents, h2 underline, card left-borders, bullets, money numbers |
| `--green` | `#119855` | **gains only**: up-ticks, sparklines, positive percentages. Never bullets, never decoration (Brett-signed after review round) |
| `--green-light` | `#6FE6A1` | positive accents on navy surfaces |
| `--paper` | `#f5f5f7` | slide/page surface (dominant) |
| `--line` | `#e0e0e5` | hairline borders, dividers, stat-band grid lines |
| `--gray` | `#5b6678` | secondary/muted body text |
| backdrop | `#d7d9de` | screen-only backdrop behind pages (never prints) |

Banned: the retired green/black CI (`#c3f753` family) and any of its styling.

---

## Typography

Two typefaces, loaded from Google Fonts:

```
https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap
```

| Role | Stack | Treatment |
|------|-------|-----------|
| Headers | `"Barlow Condensed", "Arial Narrow", sans-serif` | h1: 700, tight line-height (~0.98), slight letter-spacing. h2: 600, UPPERCASE, letter-spacing ~1.4px, small size, orange underline accent |
| Body | `"Inter", -apple-system, "Segoe UI", Roboto, sans-serif` | 400 to 500, line-height ~1.4 to 1.6 |
| Big numbers | Barlow Condensed 700 | stat color rule: navy by default, orange for money/revenue figures, green ONLY for gains (up-moves, positive %). Stat slides: ~72px numerals, vertically centered |

The h2 signature: uppercase Barlow Condensed with a 2px hairline bottom border and a short (46px) 2px orange bar overlapping it (via `::after`). Reuse this exact treatment.

---

## Component Library (from the two-pager)

| Component | Treatment |
|-----------|-----------|
| Masthead / navy band | `background: var(--navy)`, white text, logo left, flex space-between. On slides: title and closing slides go full navy |
| Stat band | CSS grid of stat cells, 1px `--line` gaps, 8px radius, numbers in Barlow Condensed 700, labels small in Inter |
| USP card | white background, 1px `--line` border, 4px solid orange left border, 6px radius |
| Callout band | navy background, white text, 8px radius, generous padding |
| Insight band | `rgba(255,106,31,0.08)` tint, 4px solid orange left border, 8px radius |
| Next-steps box | orange 8% tint, 1px dashed orange border, 8px radius |
| Tick list | **orange** dot bullets (12px circle, white inset ring) on list items. The two-pager used green here, but green is now reserved for gains; orange bullets are the locked rule |
| Agenda slide | poster treatment, not a list: 4-row grid (`.agenda`), giant orange Barlow Condensed 700 numerals (~64px, `01`-`04`), section titles ~36px navy, hairline row separators. Fills the slide |
| Diagram flow | card nodes (~300px) with elev-1; connectors are orange price-path polylines (jagged up-trending line + arrowhead, stroke `--orange`), not straight arrows; the emphasized node gets an orange border and may carry a small green gain-sparkline inside |

---

## Imagery

Two approved image sources. Embed as base64 (JPEG for photos, PNG for app UI), resize app screenshots to ~720px wide with `sips -Z 720` before embedding.

**1. Website imagery** (used on inplayglobal.com and the challenge page):
`/Users/brettstclair/programming/inplay/Inplay Outreach/assets/optimized/`

| File | Content | Best use |
|------|---------|----------|
| `cover.jpg` | Stadium at night, orange price line rising over the pitch | Title-slide background |
| `shift.jpg` | American football player leading, other athletes behind | Section-divider background; zoom with `transform: scale(1.32); transform-origin: left center;` so the football player leads and secondary figures crop at the edge |
| `baseball.jpg` | Batter mid-swing, dark navy left half is empty | Secondary divider option only (Brett prefers football) |
| `challenge.jpg` | Phone: group chat sharing an InPlay challenge link | Image-split slide, virality/distribution stories |
| `hero.jpg` | Website hero: football + basketball + market UI (has site nav baked in, crop or avoid) | Sparingly |
| `marketline.jpg` | "InPlay is the real market for sports" poster with annotated price line | Full-bleed statement slide (has type baked in) |
| `leaderboard.jpg`, `settlement.jpg`, `gatorade.jpg`, `home.jpg` | App/brand shots | Supporting visuals. `gatorade.jpg` carries an "Expo Go" status bar at the top: crop the top ~40px before using |

**Closing hero (Brett-signed):** the touchdown image from the bottom of inplayglobal.com (`https://www.inplayglobal.com/home/future-hero.png`, saved as `assets/closing-hero.jpg`). Full-bleed with a TOP-weighted scrim (`linear-gradient(180deg, rgba(6,18,43,0.92) 0%, ... transparent 100%)`), text block top-left. The image bakes in a phone on its left: shift the composition with `transform: scale(1.24); transform-origin: 88% 60%;` so the phone bleeds off the left edge and the player dominates. Do not reuse the divider image on the closing slide.

**2. App screen grabs:** `/Users/brettstclair/programming/inplay/app screen shot/`
Three portrait screenshots: home with sponsored (Coca-Cola) challenge, portfolio with buy/sell, limit-order ticket. Approved treatment (Brett-signed): **iPhone 17 frame**, never a raw cropped rectangle:

```css
.iphone .device { background: #0b0e16; border-radius: 30px; padding: 7px; box-shadow: var(--elev-2); }
.iphone .screen { border-radius: 24px; overflow: hidden; aspect-ratio: 9 / 19.5; }
.iphone .screen img { width: 100%; height: 100%; object-fit: cover; object-position: center top; }
```

Three-up flex row, ~2.06in wide each, centered, caption below (Barlow Condensed strong line + gray Inter line).

**Elevation system** (Material-inspired, use these and nothing else):

```css
--elev-1: 0 1px 3px rgba(6,18,43,0.12), 0 1px 2px rgba(6,18,43,0.08);   /* subtle */
--elev-2: 0 4px 12px rgba(6,18,43,0.16), 0 1px 3px rgba(6,18,43,0.10);  /* phones, cards */
--elev-3: 0 12px 32px rgba(6,18,43,0.22), 0 2px 6px rgba(6,18,43,0.12); /* hero visuals */
```

**Image-split slide:** never full-bleed half-slide images, and never images with their own baked-in backgrounds (Brett rejected that). Use a single framed iPhone (~2.15in wide, same `.iphone` treatment) centered in the right column (3fr text / 2fr visual grid), footer stays. Simplicity and whitespace over bleed.

**Quote slide (Brett-signed):** no navy band. Paper background, giant orange `&ldquo;` glyph (Barlow Condensed 700, ~150px), quote in Barlow Condensed 700 at ~48px navy with the key phrase in orange (`.pop`), attribution below as a 46px orange bar + small gray Inter text.

**Photographic slide treatment:** full-bleed `<img class="bg">` with `object-fit: cover`, plus a navy scrim `linear-gradient(90deg, rgba(6,18,43,0.85-0.96) 0%, ... transparent 100%)` (or 180deg top-weighted for the closing hero) so white Barlow Condensed type sits on the darkened side. Never place text on an un-scrimmed photo. Brett's preference: lead with American football imagery (`shift.jpg` divider, `cover.jpg` title, closing hero); baseball only as a secondary option. When a photo's key subject is off-center, recompose with `transform: scale(...)` + `transform-origin` on the `.bg` img rather than swapping the asset.

---

## Logo

Official SVG set: `/Users/brettstclair/programming/inplay/Inplay Outreach/InPlay Global Logo/InPlay Global Logos (SVG)/`

**Warning: do NOT embed these SVGs directly.** They wrap full-canvas raster PNGs, so on any non-matching background they show a visible box edge (both review personas flagged this). Use the pre-rendered, tight-cropped PNGs in `deck-designs/ci-template/assets/` instead:

- `logo-orange.png`: orange wordmark, transparent. Use on ALL dark/navy/photographic slides (matches the live inplayglobal.com convention).
- `logo-navy.png`: navy wordmark, transparent. Use in footers and anywhere on paper surfaces.

If a new variant is ever needed, render the SVG with the headless shell at its declared canvas size (`--window-size=2000,800 --default-background-color=00000000`), then tight-crop to the alpha bounding box with PIL.

**Embedding rule:** decks ship as one self-contained HTML file with all images base64-embedded. Use the tokenized build pattern (below), never hand-paste data URIs.

---

## Build Pattern (durable, per deck)

Each deck directory keeps three things: `source.html` (tokenized markup with `LOGO_*_URI` / `IMG_*` placeholders, the ONLY file you edit), `assets/` (all referenced images), and `build.py` (maps tokens to asset files, base64-embeds them, writes `index.html`). Rebuild with `python3 build.py` from the deck directory. Never edit `index.html` directly. `deck-designs/ci-template/build.py` is the reference implementation.

---

## Layout Feel for Slides

- Landscape 16:9 pages (13.333in x 7.5in), paper surface, generous margins (~44px+ sides on the two-pager scale, scale up proportionally for slides).
- One idea per slide. White space is part of the design; do not crowd.
- Title slide and closing slide: full-bleed navy with white Barlow Condensed and the white/orange logo.
- Section dividers: navy band or full navy slide with the section title.
- Content slides: paper surface, h2 signature header, components from the library above.
- Footer on content slides: small logo plus page number, hairline separated.
- Diagrams: built from the palette above; boxes use card treatments, flows/arrows in navy or gray, emphasis in orange only.

---

## Voice and Text Rules

- This skill does not write copy during transformation: source wording is carried over verbatim (see Key Principles).
- For template sample content and any connective labels: confident, plain, warm. Short sentences.
- **No em-dashes anywhere** (house rule). A comma, colon, full stop, or parentheses instead. Normalize any em-dash found in extracted source text to a comma, but change nothing else about the wording.
