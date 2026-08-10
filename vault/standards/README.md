---
description: "Index for the standards folder — registry of CTS-001, CTS-002 and PTS-001 with their plain-English guides, plus confidentiality and PDF-conversion provenance"
---

# InPlay Core Technical Standards

> ⚠️ **SUPERSEDED FOR MM IMPLEMENTATION (2026-07-24).** The **v1.3
> Consolidated Build Specification** (`MM-build-spec-v1.3.docx` /
> `MM-build-spec-v1.3.html`, this folder) is now the single authoritative
> engineering spec for the Market Maker — adopted as baseline in
> [[market-maker/decisions]]. The CTS/PTS documents below are historical
> context only. Three spec-vs-call conflicts are held open (E17–E19 in
> [[market-maker/open-questions]]).

> **Vision:** [[vision]]
> **Status:** Reference — client-authored authoritative standards
> **Owner:** InPlay Global, Inc. (Edwin Johnson) — mirrored here for engineering reference
> **Source:** Converted from the CTS/PTS master-draft PDFs (see [Provenance](#provenance))

---

## What These Are

The **InPlay Core Technical Standards (CTS)** are the authoritative financial,
mathematical, technical, and operational standards governing the issuance,
valuation, trading, settlement, and lifecycle management of InPlay Securities.
They are canonical governing documents authored by InPlay Global — distinct from
this vault's own [[architecture/index|architecture]] (our implementation
decisions) and [[index|component]] docs (product features). Multiple components
are bound by these standards, so they live at the top level as their own
document class.

**PTS** (Platform/Product Technical Standard) documents define reference
implementations that must conform to the constitutional requirements set by the
CTS documents.

## Registry

| ID | Title | Status | Document |
|----|-------|--------|----------|
| CTS-001 | Financial Valuation Standard (FVS-1) | Master Draft — v1.0 | [[standards/CTS-001-financial-valuation-standard]] |
| CTS-002 | Market Operations Standard (MOS-1) | Master Draft — v1.0 | [[standards/CTS-002-market-operations-standard]] |
| PTS-001 | Simulated Designated Market Maker Standard (SDMM-1) | Master Draft — v1.0 | [[standards/PTS-001-simulated-designated-market-maker-standard]] |

**Dependency:** PTS-001 (SDMM-1) conforms to the constitutional requirements of
CTS-001 and CTS-002.

## Guides

Plain-English companions for the verbose source standards. Where a guide and
its source disagree, the source wins — except where the 20-07-2026 touchdown
superseded the source (noted inline in each guide).

- [[standards/CTS-001-plain-english-guide]] — the valuation system: what a team
  is worth (ESV), value vs price, and Edwin's real formula from the 20-07 call.
  (`CTS-001-plain-english-guide.html` — readable HTML rendering, no JavaScript.)
- [[standards/CTS-002-plain-english-guide]] — market operations: Reference
  Price, market state, sessions, order rules, and the build map of what's ours
  vs tZERO's.
  (`CTS-002-plain-english-guide.html` — readable HTML rendering, no JavaScript.)
- [[standards/PTS-001-plain-english-guide]] — the SDMM bot, the 10-minute version.
- [[standards/PTS-001-comprehensive-guide]] — full-depth SDMM explainer: every rule,
  priority list, formula, and invariant, with Mermaid diagrams, a worked
  example, source-document quirks, and an implementation checklist.
- `PTS-001-comprehensive-guide.html` — self-contained HTML rendering of the
  comprehensive guide (inline CSS + SVG diagrams, no JavaScript). Open in a
  browser; markdown wikilinks don't apply to it.
- `standards/sdmm-machine.html` — interactive clickable map of the whole
  machine: engines, equations with a symbol glossary, reconciled with the
  20-07-2026 touchdown (scope confirmed as Novosapien builds, portfolio
  allocation descoped, new build items).

## Confidentiality

Each document is marked a **Trade Secret of InPlay Global, Inc.** — confidential
and proprietary. Handle per the notice at the top of each file.

## Provenance

Converted from the source PDFs (dated July 1–2, 2026) using `pymupdf4llm`.
The markdown preserves the document structure (headings, sections, tables) but
is a derived copy — the signed PDFs remain the authoritative originals.
