# Brand / Corporate Identity

Drop InPlay's corporate identity (CI) deliverables here. The admin panel's
**CI** page (`/admin/ci`) publishes everything in this folder automatically on
the next vault sync — no code changes needed.

## Supported files

`.svg` · `.png` · `.jpg` / `.jpeg` · `.webp` · `.gif` · `.html`

(HTML renders in a sandboxed preview — scripts are blocked; use "Open in new
tab" in the panel for full interactivity.)

## Categories

The **first subfolder** is the category shown in the panel. Loose files at the
root of `brand/` fall under **General**.

```
brand/
  logo.svg              → General
  logos/
    primary.svg         → Logos
    monochrome.png      → Logos
  colours/
    palette.png         → Colours
  guidelines/
    brand-guide.html    → Guidelines
```

## Optional titles / overrides

Add a `brand/manifest.json` to override an asset's display title or category,
keyed by its path relative to `brand/`:

```json
{
  "logos/primary.svg": { "title": "Primary Logo" },
  "misc/hero.png": { "title": "Hero Image", "category": "Imagery" }
}
```

Files fall back to a humanized filename when no override is given.
