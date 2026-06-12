"""Build a single-language print document (one page) for PDF rendering.

Usage:
    cd src && python build_print.py --lang zh
    cd src && python build_print.py --lang en
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import shell  # noqa: E402
import quizzes  # noqa: E402
from i18n import esc  # noqa: E402
from registry import CONTENT  # noqa: E402

# Print/PDF overrides. A full light palette is re-declared *after* shell.CSS so it
# wins over the dark `prefers-color-scheme` block when the reader's OS is in dark
# mode; print-color-adjust keeps card/code backgrounds in the exported PDF; and
# code lines wrap instead of clipping at the page margin.
_PRINT_CSS = """
:root {
  --bg:#fff; --panel:#fff; --panel-2:#f3f3f8; --ink:#1d2129;
  --muted:#4b5563; --faint:#6b7280; --line:#e4e4ee;
  --accent:#6d5ae6; --accent-soft:#ece8fc; --accent-ink:#4b3bc0; --on-accent:#fff;
  --blue:#1f56d3; --blue-soft:#e7efff; --amber:#965104; --amber-soft:#fdf1dd;
  --purple:#7c3aed; --purple-soft:#f0e9ff; --red:#c12f2f; --red-soft:#fbe6e6;
  --code-bg:#0f172a; --code-ink:#e2e8f0; --code-line:#1e293b;
}
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
pre.code { white-space: pre-wrap; overflow-wrap: anywhere; }
.print-lesson { page-break-before: always; padding-top: 1rem; }
.print-lesson:first-child { page-break-before: avoid; }
.print-lesson .part { font-size: .76rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--accent); font-weight: 700; }
.print-lesson h1 { font-size: 1.7rem; margin: .2rem 0 1rem; }
.topbar, .lesson-nav, .lang-toggle { display: none !important; }
"""

# Intra-guide cross-references (e.g. href="16-permission.html") point at files
# that don't exist alongside the combined print document; rewrite them to in-page
# anchors that jump to the matching <section> id instead.
_XREF = re.compile(r'href="(\d{2}-[^"#]+\.html)"')


def build_print(lang: str, root: str = DEFAULT_ROOT) -> str:
    """Write ``print.<lang>.html`` under ``root``; return its path."""
    parts = []
    for fname, zt, et, zp, ep in shell.PAGES:
        title = zt if lang == "zh" else et
        part = zp if lang == "zh" else ep
        body = CONTENT.get(fname, "") + quizzes.render(fname)
        body = _XREF.sub(r'href="#\1"', body)
        parts.append(
            f'<section class="print-lesson" id="{esc(fname)}">'
            f'<div class="part">{esc(part)}</div>'
            f"<h1>{esc(title)}</h1>{body}</section>"
        )
    combined = "".join(parts).replace("<details", "<details open")
    doc_title = (
        "AgentScope 可视化指南 · 打印版"
        if lang == "zh"
        else "AgentScope Visual Guide · Print"
    )
    html = (
        f'<!doctype html>\n<html lang="{lang}" data-lang="{lang}">\n<head>\n'
        '<meta charset="utf-8">\n'
        f"<title>{esc(doc_title)}</title>\n"
        f"<style>{shell.CSS}{_PRINT_CSS}</style>\n</head>\n<body>\n"
        f'<div class="wrap">{combined}</div>\n</body>\n</html>'
    )
    out = os.path.join(root, f"print.{lang}.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = ap.parse_args()
    print("Wrote", build_print(args.lang))
