#!/usr/bin/env python3
"""
pdf_extract.py, InPlay deck designer ingestion (Phase 2, Step 2).

Extracts a source deck PDF into everything the transformation needs:
  - per-page text as Markdown (headings inferred from font size)
  - a full-page PNG render of every page (for reading diagrams and layout)
  - every embedded image, saved per page
  - manifest.json summarising what was found

Usage:
    python3 pdf_extract.py <deck.pdf> <output_dir>

Output layout:
    <output_dir>/content.md              page-by-page text
    <output_dir>/pages/page-NN.png       full render of each page (2x scale)
    <output_dir>/images/page-NN-*.png    embedded images per page
    <output_dir>/manifest.json           pages, word counts, image counts, flags

House style: long-dash characters (U+2014, U+2013) in extracted text are
normalised to commas. Pages with no extractable text are flagged
"needs_visual_read" in the manifest; read their page render visually and
transcribe.
"""
import json
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF (fitz) is required. Install with: pip3 install pymupdf")

# U+2014 (em dash) and U+2013 (en dash) are banned by house style
DASH_RE = re.compile("\\s*[\\u2014\\u2013]\\s*")


def clean(text: str) -> str:
    text = DASH_RE.sub(", ", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def page_markdown(page) -> str:
    """Extract text blocks, inferring headings from relative font size."""
    blocks = page.get_text("dict")["blocks"]
    sizes = [
        span["size"]
        for b in blocks if b.get("type") == 0
        for line in b["lines"] for span in line["spans"]
        if span["text"].strip()
    ]
    if not sizes:
        return ""
    max_size = max(sizes)
    out = []
    for b in blocks:
        if b.get("type") != 0:
            continue
        for line in b["lines"]:
            text = clean("".join(s["text"] for s in line["spans"]))
            if not text:
                continue
            size = max(s["size"] for s in line["spans"])
            if size >= max_size * 0.9 and len(text) < 90:
                out.append(f"## {text}")
            elif size >= max_size * 0.72 and len(text) < 90:
                out.append(f"### {text}")
            else:
                out.append(text)
    return "\n\n".join(out)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pdf_path, out_dir = sys.argv[1], sys.argv[2]
    pages_dir = os.path.join(out_dir, "pages")
    images_dir = os.path.join(out_dir, "images")
    for d in (out_dir, pages_dir, images_dir):
        os.makedirs(d, exist_ok=True)

    doc = fitz.open(pdf_path)
    md_parts = [f"# Source deck: {os.path.basename(pdf_path)}\n"]
    manifest = {"source": os.path.abspath(pdf_path), "pages": []}

    for i, page in enumerate(doc, start=1):
        # Full-page render at 2x for visual reading of diagrams/layout
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        render = os.path.join(pages_dir, f"page-{i:02d}.png")
        pix.save(render)

        # Embedded images
        img_count = 0
        for j, img in enumerate(page.get_images(full=True), start=1):
            try:
                base = doc.extract_image(img[0])
                ext = base.get("ext", "png")
                path = os.path.join(images_dir, f"page-{i:02d}-{j}.{ext}")
                with open(path, "wb") as f:
                    f.write(base["image"])
                img_count += 1
            except Exception:
                continue

        text = page_markdown(page)
        md_parts.append(f"\n---\n\n# Page {i}\n\n{text or '(no extractable text, read the page render)'}")
        manifest["pages"].append({
            "page": i,
            "words": len(text.split()),
            "embedded_images": img_count,
            "render": os.path.relpath(render, out_dir),
            "needs_visual_read": not text.strip(),
        })

    with open(os.path.join(out_dir, "content.md"), "w") as f:
        f.write("\n".join(md_parts) + "\n")
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    flagged = sum(1 for p in manifest["pages"] if p["needs_visual_read"])
    print(f"Extracted {len(manifest['pages'])} pages to {out_dir}"
          f" ({flagged} page(s) flagged for visual read)")


if __name__ == "__main__":
    main()
