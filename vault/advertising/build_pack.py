#!/usr/bin/env python3
"""Build the InPlay advertising onboarding pack as a single CI-styled HTML page.

Reads the three markdown artefacts and renders them into one readable document
in InPlay's corporate identity. The markdown stays the source of truth.

Usage:  python3 build_pack.py 2026-08-12-0930
"""
import html
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
STAMP = sys.argv[1] if len(sys.argv) > 1 else "2026-08-12-0930"

DOCS = [
    ("offer", "The Offer", "What may be said", "inplay-advertising-offer.md"),
    ("icps", "The ICPs", "Which companies to say it to", "inplay-advertising-icps.md"),
    ("personas", "The Buyer Personas", "Which humans it must land with", "inplay-advertising-buyer-personas.md"),
]


def inline(text):
    """Inline markdown to HTML.

    Code spans are lifted to placeholders first so their contents are never
    re-parsed, but bold and italic still pair across them: the ICP pain tables
    wrap bold around a code span and both markers must survive.
    """
    spans = []

    def stash(m):
        spans.append(html.escape(m.group(1)))
        return "\x00{}\x00".format(len(spans) - 1)

    t = re.sub(r"`([^`]+)`", stash, text)
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: "<code>" + spans[int(m.group(1))] + "</code>", t)


def render_table(rows):
    head, body = rows[0], rows[2:]
    h = "".join("<th>" + inline(c) + "</th>" for c in head)
    b = ""
    for r in body:
        b += "<tr>" + "".join("<td>" + inline(c) + "</td>" for c in r) + "</tr>"
    return "<div class='tw'><table><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>".format(h, b)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def convert(md, slug):
    lines = md.split("\n")
    out = []
    list_stack = []
    table_rows = []
    quote_buf = []

    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][1] > to_indent:
            kind, _, nested = list_stack.pop()
            out.append("</" + kind + ">")
            if nested:
                out.append("</li>")

    def flush_quote():
        if quote_buf:
            body = "".join("<p>" + inline(q) + "</p>" for q in quote_buf if q.strip())
            out.append("<blockquote>" + body + "</blockquote>")
            del quote_buf[:]

    def flush_table():
        if table_rows:
            out.append(render_table(list(table_rows)))
            del table_rows[:]

    def open_list(kind, indent, content):
        close_lists(indent)
        if not list_stack or list_stack[-1][1] < indent:
            # A deeper list belongs inside the item above it, not beside it.
            nested = bool(out) and out[-1].endswith("</li>")
            if nested:
                out[-1] = out[-1][:-len("</li>")]
            list_stack.append((kind, indent, nested))
            out.append("<" + kind + ">")
        out.append("<li>" + inline(content) + "</li>")

    for raw in lines:
        line = raw.strip()

        if line.startswith("|"):
            close_lists()
            flush_quote()
            table_rows.append(split_row(line))
            continue
        flush_table()

        if line.startswith(">"):
            close_lists()
            quote_buf.append(line.lstrip("> ").rstrip())
            continue
        flush_quote()

        if not line:
            close_lists()
            continue

        if line.startswith("---") and set(line) <= set("- "):
            close_lists()
            out.append("<hr>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_lists()
            lvl = len(m.group(1))
            txt = m.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")[:60]
            out.append('<h{0} id="{1}-{2}">{3}</h{0}>'.format(lvl, slug, anchor, inline(txt)))
            continue

        m = re.match(r"^(\s*)[-*]\s+(.*)$", raw)
        if m:
            open_list("ul", len(m.group(1)), m.group(2))
            continue

        m = re.match(r"^(\s*)\d+\.\s+(.*)$", raw)
        if m:
            open_list("ol", len(m.group(1)), m.group(2))
            continue

        close_lists()
        out.append("<p>" + inline(line) + "</p>")

    close_lists()
    flush_quote()
    flush_table()
    return "\n".join(out)


CSS = """
:root{--navy:#06122B;--navy-2:#0A1A36;--orange:#FF6A1F;--green:#119855;
--paper:#f5f5f7;--line:#e0e0e5;--gray:#5b6678;--rule:#cdd6e4;
--header-font:"Barlow Condensed","Arial Narrow",sans-serif;
--body-font:"Inter",-apple-system,"Segoe UI",Roboto,sans-serif;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--body-font);color:var(--navy);background:var(--paper);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--orange)}
.wrap{max-width:1100px;margin:0 auto;padding:0 32px 96px}
header.hero{background:var(--navy);color:#fff;padding:56px 32px 44px}
header.hero .inner{max-width:1100px;margin:0 auto}
header.hero .mark{font-family:var(--header-font);letter-spacing:.14em;text-transform:uppercase;font-size:13px;color:var(--orange);font-weight:600}
header.hero h1{font-family:var(--header-font);font-size:54px;line-height:1.02;text-transform:uppercase;margin:14px 0 10px;font-weight:700}
header.hero p{color:#9fb0c9;max-width:70ch;font-size:15px}
header.hero .meta{margin-top:22px;font-size:12.5px;color:#9fb0c9;border-top:1px solid rgba(255,255,255,.14);padding-top:14px}
nav.sticky{position:sticky;top:0;z-index:20;background:var(--navy-2);border-bottom:2px solid var(--orange)}
nav.sticky .inner{max-width:1100px;margin:0 auto;padding:0 32px;display:flex;gap:26px;flex-wrap:wrap}
nav.sticky a{display:inline-block;padding:13px 0;color:#cdd6e4;text-decoration:none;font-family:var(--header-font);
text-transform:uppercase;letter-spacing:.09em;font-size:14px;font-weight:600}
nav.sticky a:hover{color:var(--orange)}
.callout{background:#fff;border-left:4px solid var(--orange);padding:20px 24px;margin:28px 0;box-shadow:0 1px 3px rgba(6,18,43,.07)}
.callout h2{font-family:var(--header-font);text-transform:uppercase;font-size:19px;letter-spacing:.05em;margin-bottom:8px}
section.doc{background:#fff;border:1px solid var(--line);padding:44px 48px;margin-top:36px;box-shadow:0 1px 3px rgba(6,18,43,.06)}
.doc-head{border-bottom:3px solid var(--navy);padding-bottom:16px;margin-bottom:28px}
.eyebrow{font-family:var(--header-font);text-transform:uppercase;letter-spacing:.16em;font-size:12px;color:var(--orange);font-weight:600}
.doc-head h1{font-family:var(--header-font);font-size:42px;text-transform:uppercase;line-height:1.05;margin-top:6px;font-weight:700}
section.doc h1{font-family:var(--header-font);font-size:32px;text-transform:uppercase;margin:44px 0 14px;font-weight:700;
border-bottom:2px solid var(--rule);padding-bottom:8px}
section.doc h2{font-family:var(--header-font);font-size:26px;text-transform:uppercase;margin:38px 0 12px;font-weight:700}
section.doc h3{font-family:var(--header-font);font-size:20px;text-transform:uppercase;letter-spacing:.03em;
margin:30px 0 10px;font-weight:600;color:var(--navy-2)}
section.doc h4{font-size:15px;margin:22px 0 8px;font-weight:700;color:var(--navy-2)}
section.doc p{margin:11px 0;font-size:14.6px}
section.doc ul,section.doc ol{margin:11px 0 11px 22px;font-size:14.6px}
section.doc li{margin:6px 0}
section.doc li>ul,section.doc li>ol{margin-top:6px}
strong{color:var(--navy);font-weight:650}
code{background:#eef1f6;border:1px solid var(--line);border-radius:3px;padding:1px 6px;font-size:12.8px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--green)}
blockquote{background:#f7f9fc;border-left:3px solid var(--rule);padding:14px 20px;margin:18px 0;color:var(--gray);font-size:14px}
blockquote strong{color:var(--navy)}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}
.tw{overflow-x:auto;margin:20px 0}
table{border-collapse:collapse;width:100%;font-size:13.4px}
th{background:var(--navy);color:#fff;text-align:left;padding:10px 12px;font-family:var(--header-font);
text-transform:uppercase;letter-spacing:.06em;font-size:13px;font-weight:600;vertical-align:bottom}
td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even){background:#fafbfd}
footer{max-width:1100px;margin:0 auto;padding:32px;color:var(--gray);font-size:12.5px;border-top:1px solid var(--line)}
@media print{
 body{background:#fff}
 nav.sticky{display:none}
 section.doc{border:0;box-shadow:none;padding:0;margin-top:24px;page-break-before:always}
 section.doc:first-of-type{page-break-before:avoid}
 header.hero{background:#fff;color:var(--navy);padding:0 0 24px}
 header.hero h1{color:var(--navy)}
 header.hero p,header.hero .meta{color:var(--gray)}
 .wrap{padding:0}
 th{background:#e8ecf3;color:var(--navy)}
 a{color:var(--navy);text-decoration:none}
}
"""

HEAD_BLURB = (
    "The three artefacts the Cold Outreach Workforce grounds on. The Offer says what may be claimed. "
    "The ICPs say which companies to claim it to. The Buyer Personas say which humans inside them it "
    "must land with. None of them is a brochure and no advertiser ever reads one."
)

CALLOUT = """
  <div class="callout">
    <h2>Read this first</h2>
    <p><strong>Not yet loadable into the workforce.</strong> Every unresolved fact is written <code>unknown</code>
    and collected into a gaps list at the foot of each document. Nothing here is padded and nothing is inferred.
    The blocking items are the launch inventory map (Cody), the makegood wording and the definition of an exposure
    (counsel), and the rest of the advertiser category list (Edwin).</p>
    <p><strong>Every persona quote is invented.</strong> InPlay has closed no advertising deals, so the first-person
    phrasing in the personas was written by Novosapien rather than remembered from a call. That was a deliberate
    decision to keep moving. Replace it with real phrasing as real conversations happen.</p>
  </div>
"""


def build():
    sections, nav = [], []
    for slug, title, sub, fname in DOCS:
        md = (BASE / fname).read_text(encoding="utf-8")
        md = re.sub(r"^#\s+.*$", "", md, count=1, flags=re.M)
        body = convert(md, slug)
        nav.append('<a href="#{}">{}</a>'.format(slug, html.escape(title)))
        sections.append(
            '<section id="{}" class="doc"><div class="doc-head">'
            '<span class="eyebrow">{}</span><h1>{}</h1></div>{}</section>'.format(
                slug, html.escape(sub), html.escape(title), body
            )
        )

    return """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>InPlay Advertising &middot; Outbound Onboarding Pack</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="hero">
  <div class="inner">
    <div class="mark">InPlay Global &middot; Advertising</div>
    <h1>Outbound Onboarding Pack</h1>
    <p>{blurb}</p>
    <div class="meta">Draft v1 &middot; authored 12 August 2026 in working session with Edwin Johnson and Cody Haugen &middot; generated {stamp}</div>
  </div>
</header>
<nav class="sticky"><div class="inner">{nav}</div></nav>
<div class="wrap">{callout}{sections}</div>
<footer>Novosapien for InPlay Global &middot; Cold Outreach Workforce onboarding &middot; Offer Structure v2, the ICP authoring structure and the 12-section Buyer Persona structure, followed verbatim. Regenerate this page with <code>build_pack.py</code>.</footer>
</body>
</html>
""".format(css=CSS, blurb=HEAD_BLURB, stamp=STAMP, nav="".join(nav), callout=CALLOUT, sections="".join(sections))


if __name__ == "__main__":
    out = BASE / "inplay-advertising-onboarding-pack-{}.html".format(STAMP)
    out.write_text(build(), encoding="utf-8")
    print("wrote {} ({:,} bytes)".format(out, out.stat().st_size))
