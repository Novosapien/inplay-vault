# Print Output: 16:9 Pages and PDF QA

> **When to read:** When finalizing any deck (template or transformed) for print-to-PDF.

Every deck must print to a digital PDF with one slide per page, colors exact, nothing clipped. The two-pager proves the pattern; this adapts it to landscape 16:9.

---

## Required CSS

```css
@page { size: 13.333in 7.5in; margin: 0; }

.slide {
  width: 13.333in;
  height: 7.5in;
  position: relative;
  overflow: hidden;
  background: var(--paper);
  page-break-after: always;
  break-after: page;
}
.slide:last-child { page-break-after: auto; }

/* Screen preview: backdrop and shadow, stripped for print */
body { background: #d7d9de; }
@media screen {
  .slide { margin: 16px auto; box-shadow: 0 8px 30px rgba(6, 18, 43, 0.18); }
}
@media print {
  body { background: none; }
  .slide { margin: 0; box-shadow: none; }
}

/* Colors must print exactly, navy bands especially */
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
```

Rules:

- Fixed slide dimensions in inches, never viewport units (`vh`/`vw` break in print).
- No content within 0.25in of any edge except intentional full-bleed navy bands.
- Interactive/animated elements are out of scope here: these decks are for print. Keep them static.

---

## Producing the PDF

**Option A, Brett prints himself (default):** open `index.html` in Comet (or any Chromium browser), Cmd+P, destination "Save as PDF", Paper size will follow `@page`, margins None, Background graphics ON. Include these instructions when delivering.

**Option B, generate it directly** (useful for QA or when Brett asks for the PDF file). This machine has no Chrome; Brett browses with Comet, and the reliable headless printer is the Playwright Chromium shell already cached locally:

```bash
"$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell" \
  --disable-gpu --virtual-time-budget=10000 \
  --user-data-dir="$(mktemp -d)" \
  --no-pdf-header-footer \
  --print-to-pdf="deck-designs/{deck-name}/{deck-name}.pdf" \
  "file:///absolute/path/to/deck-designs/{deck-name}/index.html"
```

(Comet headless does not print reliably; do not use it for QA.)

---

## QA Checklist

Generate the PDF via Option B and verify:

- [ ] Page count equals slide count exactly (a mismatch means overflow is leaking extra pages)
- [ ] No text or component clipped at any page edge
- [ ] Navy bands and orange accents render at full color (background graphics printing works)
- [ ] Fonts render as Barlow Condensed and Inter, not fallbacks (check a heading's condensed width visually)
- [ ] Logo crisp (SVG, not a rasterized blur)
- [ ] Diagrams intact: no arrows or labels lost to page breaks
- [ ] File opens offline: no missing assets, no network-only resources except the Google Fonts link (acceptable, since printing happens online; if Brett needs fully offline, inline the font CSS)
