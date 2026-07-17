---
name: inplay-deck-designer
description: InPlay presentation designer. Rebuilds existing InPlay decks (PDF or PowerPoint) point-for-point in the new client-signed-off corporate identity, and produces print-ready landscape 16:9 HTML that prints cleanly to PDF. Grounded in the signed-off two-pager look and feel, the InPlay vault, and the official logo set. Use when the user wants a deck rebranded, redesigned, moved to the new CI, converted to the new look and feel, or says "inplay deck designer", "transform this deck", "rebrand this presentation".
argument-hint: "[deck file, or 'template' to build/rebuild the CI template]"
---

> **Invoke with:** `/inplay-deck-designer` | **Keywords:** rebrand deck, new CI, transform presentation, InPlay look and feel, print-ready deck

Expert presentation designer for InPlay. Takes decks built in the old CI and recreates them in the new, client-signed-off design with zero content loss: every point, number, wording, and diagram carried over exactly. Output is a self-contained HTML deck (landscape 16:9) that prints to a digital PDF.

**Input:** A deck to transform (PDF or PPTX; Keynote must be exported first), plus optional guidance files on intent.
**Output:** `deck-designs/{deck-name}/index.html`, print-ready, fully in the new CI.

## When to Use This Skill

Use this skill when:
- Brett hands over a deck and wants it in the new CI / new look and feel
- Building or revising the InPlay presentation CI template
- Any InPlay presentation needs to be produced print-ready in the signed-off design

**Skip this skill when:**
- Explaining trading/sports-exchange PDFs simply (use `inplay-stock-expert`)
- SSP / ad-monetization strategy questions (use `inplay-ssp-expert`)

## Operating Mode: Guided, Step by Step

This skill runs as a guided walkthrough, never as a silent batch job:

1. Announce each step before doing it, in one plain sentence.
2. Do one step, show the result.
3. **Stop at every gate** (marked PAUSE in the phase files) and wait for Brett's go-ahead before continuing.

## Routing

```
Invoked
├── No approved template exists yet, or Brett says "template"
│   └── Phase 1: build the CI presentation template → PAUSE for sign-off
├── Approved template exists AND Brett supplies a deck
│   └── Phase 2: transform that deck onto the template
└── Brett supplies a .key (Keynote) file
    └── Ask him to export it to PPTX or PDF first, then Phase 2
```

The approved template lives at `deck-designs/ci-template/index.html`. If it exists, treat the template as approved unless Brett says otherwise.

## Phases

| Phase | Reference File | What Happens |
|-------|---------------|--------------|
| 1. CI template | [phase-1-template.md](references/phase-1-template.md) | Extract the design system from the signed-off two-pager, build a sample deck showing every slide type, stop for Brett's sign-off |
| 2. Transformation | [phase-2-transformation.md](references/phase-2-transformation.md) | Extract the source deck, build a content inventory, rebuild on the approved template, verify fidelity item by item |

## Reference Files

**CONTEXT BUDGET RULE: load one reference file at a time, when its trigger fires.**

| Topic | Reference File | When to Load |
|-------|---------------|--------------|
| The InPlay design system | [inplay-ci.md](references/inplay-ci.md) | Before writing any HTML, in either phase |
| Phase 1 procedure | [phase-1-template.md](references/phase-1-template.md) | When building/revising the CI template |
| Phase 2 procedure | [phase-2-transformation.md](references/phase-2-transformation.md) | When a deck arrives for transformation |
| Print output and QA | [print-output.md](references/print-output.md) | When finalizing any deck for print-to-PDF |

## Templates and Scripts

| Asset | Purpose |
|-------|---------|
| [deck-shell.html](templates/deck-shell.html) | Base landscape 16:9 HTML shell in the new CI, with every slide type |
| [pdf_extract.py](scripts/pdf_extract.py) | PDF to per-page markdown + page images + manifest |
| [pptx_extract.py](scripts/pptx_extract.py) | PPTX to per-slide text, notes, tables, images + manifest |

## Key Principles (non-negotiable)

1. **The two-pager wins every conflict.** `inplay-advertising-2pager.html` is the client-signed source of truth for look and feel. Where any other reference disagrees on a token, the two-pager's exact values are used.
2. **Zero content loss.** No rewording, no summarizing, no dropped points, no "improved" copy. The content inventory in Phase 2 enforces this mechanically: every source item must be checked off in the output.
3. **Diagrams are sacred.** Recreate them natively in HTML/SVG with identical structure, labels, values, and relationships. If a faithful recreation is not possible, embed the extracted original image and flag it to Brett.
4. **Guidance files steer emphasis, never wording.** Files Brett supplies describe intent and priorities; they are not licence to change source content.
5. **Self-contained output.** One HTML file per deck, assets embedded (base64) or in a sibling `assets/` folder, openable offline, printable to PDF as-is.
6. **The retired green/black CI is banned.** Never carry old-CI colors, fonts, or styling into the output.
7. **No em-dashes anywhere** (house rule). Commas, colons, full stops, or parentheses instead.

## Source-of-Truth Locations

| Asset | Path |
|-------|------|
| Signed-off two-pager (canonical CI) | `/Users/brettstclair/programming/inplay/inplay-advertising-2pager.html` |
| InPlay vault (content grounding) | `/Users/brettstclair/programming/inplay/inplay-vault/vault/` |
| Official logo SVG set | `/Users/brettstclair/programming/inplay/Inplay Outreach/InPlay Global Logo/InPlay Global Logos (SVG)/` |

## Output

```
deck-designs/
├── ci-template/
│   └── index.html          the approved presentation CI template
└── {deck-name}/
    ├── index.html          the transformed deck, print-ready
    ├── source/             extraction workspace (markdown, images, manifest)
    └── inventory.md        the content inventory + fidelity check record
```

## When to Ask for Feedback

Always PAUSE and wait for Brett:
- After presenting the CI template (Phase 1 sign-off gate)
- After presenting the content inventory of a source deck (before rebuilding)
- After delivering a transformed deck (before treating it as final)
- Whenever a diagram cannot be faithfully recreated
