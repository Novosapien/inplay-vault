# Phase 2: Transform a Deck onto the Approved Template

> **When to read:** When Brett supplies a deck to move into the new CI. Requires an approved template at `deck-designs/ci-template/index.html` (if missing, run Phase 1 first).

The contract: the output deck contains everything the source deck says, word for word, number for number, diagram for diagram, restyled into the new CI. Accuracy beats aesthetics whenever they conflict. Run as a guided walkthrough with the two PAUSE gates below.

---

## Steps

### Step 1: Intake

1. Identify the source format. `.pdf` → `scripts/pdf_extract.py`. `.pptx` → `scripts/pptx_extract.py`. `.key` → ask Brett to export to PPTX or PDF first (File, Export To), then stop and wait.
2. Ask for (or note) any guidance files. These steer emphasis and framing choices only, never wording.
3. Create the workspace: `deck-designs/{deck-name}/source/`.

### Step 2: Extract

Run the matching script into the workspace:

```bash
python3 .claude/skills/inplay-deck-designer/scripts/pdf_extract.py "<deck.pdf>" "deck-designs/{deck-name}/source"
python3 .claude/skills/inplay-deck-designer/scripts/pptx_extract.py "<deck.pptx>" "deck-designs/{deck-name}/source"
```

Both write per-slide markdown, extracted images, page renders (PDF), and `manifest.json`. If the manifest flags scanned/no-text pages, read those page images visually and transcribe them yourself.

### Step 3: Build the content inventory

This is the fidelity mechanism. For every source slide, record in `deck-designs/{deck-name}/inventory.md`:

| # | Slide | Element | Exact content | Carried over? |
|---|-------|---------|---------------|---------------|

- **Element types:** title, subtitle, heading, bullet, paragraph, number/stat, table, diagram, image, footnote, caption.
- **Exact content:** verbatim text (or for diagrams: every node label, every connection, every value, and the relationship structure, described precisely).
- Cross-check the extracted text against the page images visually; extraction can miss text baked into graphics.
- Leave "Carried over?" blank for now.

### Step 4: PAUSE, inventory gate

Show Brett the inventory (slide count, element counts, and anything ambiguous or unreadable in the source). Ask him to confirm it is complete before rebuilding. This is his chance to say "drop slide 7" or "that diagram is obsolete"; only he may remove content.

### Step 5: Rebuild on the template

1. Copy the approved template's head/CSS as the base for `deck-designs/{deck-name}/index.html`.
2. Map each source slide to the closest template slide type. Keep the source's slide order and one-to-one slide mapping unless content physically cannot fit, in which case split into a continuation slide (never condense to make it fit).
3. Text: verbatim. Fix nothing, improve nothing, reword nothing. The only permitted change: normalize em-dashes to commas (house rule).
4. Tables and stats: same values, same units, same precision, restyled.
5. **Diagrams:** recreate natively in HTML/SVG using the CI diagram style: identical structure, all labels verbatim, all values intact, same directional flow. If a diagram is too complex or ambiguous to recreate faithfully, embed the extracted source image, style its frame in the CI, and flag it to Brett at the delivery gate.
6. Old-CI artifacts (legacy colors, old fonts, old logo) are styling, not content: replace them with the new CI. The old logo is replaced by the new logo, never carried over.

### Step 6: Fidelity verification

Walk `inventory.md` top to bottom against the built deck. Mark every row "yes" only if the content appears verbatim (or, for diagrams, structurally identical). Any row that cannot be marked "yes" gets fixed, not explained away. Record the completed table; it is the audit trail.

### Step 7: Print QA, then PAUSE, delivery gate

Load `references/print-output.md`, run its checklist. Then present to Brett:

- The output path and print instructions
- The fidelity result (e.g. "84 of 84 inventory items carried over verbatim")
- Any embedded-not-recreated diagrams, flagged
- Any judgement calls made in slide-type mapping

Stop and wait for his review before treating the deck as final.

---

## Completion Checklist

- [ ] Inventory built and confirmed by Brett before rebuilding
- [ ] Every inventory row marked carried-over, verbatim
- [ ] Diagrams recreated in CI style (or embedded and flagged)
- [ ] No old-CI colors, fonts, or logos anywhere in the output
- [ ] Print QA passed, delivery gate presented
