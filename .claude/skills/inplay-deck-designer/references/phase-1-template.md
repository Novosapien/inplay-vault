# Phase 1: Build the CI Presentation Template

> **When to read:** When building or revising the presentation CI template (first run, Brett says "template", or Brett requests look-and-feel changes).

The goal: a sample deck in the new CI showing every slide type, so Brett can sign off on the look and feel before any real deck is transformed. Run this as a guided walkthrough: announce each step, show the result, and stop at the gate.

---

## Steps

### Step 1: Verify sources

Announce, then confirm each exists:

1. `inplay-advertising-2pager.html` (canonical CI source)
2. The logo SVG set (see SKILL.md source-of-truth table)
3. The vault at `inplay-vault/vault/` (skim `index.md` and `vision.md` for realistic sample content and correct product language)

If Brett supplied guidance files, read them now and reflect back in one short list what direction they set.

### Step 2: Re-extract the design tokens fresh

Do not trust this skill's own CI file blindly. Extract from the two-pager directly:

```bash
python3 -c "
import re
html = open('inplay-advertising-2pager.html').read()
css = re.search(r'<style[^>]*>(.*?)</style>', html, re.S).group(1)
print(re.search(r':root\s*{([^}]*)}', css).group(1))
"
```

Compare against `references/inplay-ci.md`. If anything differs (the two-pager may have been updated), the two-pager wins: update `inplay-ci.md` and tell Brett what changed.

### Step 3: Build the template deck

Start from `templates/deck-shell.html`. Fill every slide type with realistic InPlay sample content (from the vault, not lorem ipsum):

1. **Title slide**: photographic full-bleed (`cover.jpg`) with navy scrim, orange logo, deck title, subtitle, date
2. **Agenda slide**: poster treatment, giant orange numerals + big section titles (see inplay-ci.md)
3. **Section divider**: photographic full-bleed (`shift.jpg`, football player leads via scale transform) with navy scrim, text left
4. **Content slide**: heading + body + orange tick list, vertically centered
5. **Stat slide**: 3 or 4 big numbers (~72px, stat color rule), ghosted candlestick watermark, vertically centered
6. **USP / cards slide**: 3-up orange-left-border cards with elev-1, vertically centered
7. **Diagram slide**: sample flow in native HTML/SVG with orange price-path connectors, proving the diagram style
8. **App showcase slide**: three-up app screen grabs in iPhone 17 frames, captions
9. **Image-split slide**: text left (3fr), single framed iPhone right (2fr)
10. **Quote slide**: paper background, giant orange quote glyph, 48px Barlow quote with orange `.pop` phrase
11. **Closing slide**: photographic hard close (`closing-hero.jpg`, top-weighted scrim), call to action, logo

Imagery sources and treatments: see the Imagery section of `inplay-ci.md`. Embed the logo and all images as base64 (per `inplay-ci.md`). Keep a tokenized `source.html` next to the built file and rebuild `index.html` from it via a base64-embed step, so future edits never touch embedded data. Save to `deck-designs/ci-template/index.html`.

### Step 4: Print QA

Load `references/print-output.md` and run its checklist against the template. Fix anything that fails before showing Brett.

### Step 5: PAUSE, sign-off gate

Present to Brett:

- The file path, plus how to open and print it
- A one-paragraph summary of the design decisions (what was carried from the two-pager, how it was adapted to 16:9)
- Any deviations or judgement calls, flagged explicitly

Then **stop**. Do not proceed to any transformation until Brett approves. If he requests changes, apply them, re-run Step 4, and present again. On approval, the template at `deck-designs/ci-template/index.html` becomes the base for all Phase 2 work.

---

## Completion Checklist

- [ ] Tokens re-extracted from the two-pager, discrepancies resolved in its favour
- [ ] All eleven slide types present with realistic InPlay content
- [ ] Logo embedded base64, file opens offline
- [ ] Print QA passed (16:9 pages, no overflow, colors print exactly)
- [ ] Brett has explicitly signed off
