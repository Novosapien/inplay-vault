# InPlay Core Technical Standards

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

Plain-English companions for the verbose source standards:

- [[standards/PTS-001-plain-english-guide]] — the 10-minute version.
- [[standards/PTS-001-comprehensive-guide]] — full-depth explainer: every rule,
  priority list, formula, and invariant, with Mermaid diagrams, a worked
  example, source-document quirks, and an implementation checklist.
- `PTS-001-comprehensive-guide.html` — self-contained HTML rendering of the
  comprehensive guide (inline CSS + SVG diagrams, no JavaScript). Open in a
  browser; markdown wikilinks don't apply to it.

## Confidentiality

Each document is marked a **Trade Secret of InPlay Global, Inc.** — confidential
and proprietary. Handle per the notice at the top of each file.

## Provenance

Converted from the source PDFs (dated July 1–2, 2026) using `pymupdf4llm`.
The markdown preserves the document structure (headings, sections, tables) but
is a derived copy — the signed PDFs remain the authoritative originals.
