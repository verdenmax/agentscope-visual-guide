"""Build a single-language print document (one page) for PDF rendering.

Usage:
    cd src && python build_print.py --lang zh
    cd src && python build_print.py --lang en
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import shell  # noqa: E402
import quizzes  # noqa: E402
from registry import CONTENT  # noqa: E402

_PRINT_CSS = """
.print-lesson { page-break-before: always; padding-top: 1rem; }
.print-lesson:first-child { page-break-before: avoid; }
.print-lesson .part { font-size: .76rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--accent); font-weight: 700; }
.print-lesson h1 { font-size: 1.7rem; margin: .2rem 0 1rem; }
.topbar, .lesson-nav, .lang-toggle { display: none !important; }
"""


def build_print(lang: str, root: str = DEFAULT_ROOT) -> str:
    """Write ``print.<lang>.html`` under ``root``; return its path."""
    parts = []
    for fname, zt, et, zp, ep in shell.PAGES:
        title = zt if lang == "zh" else et
        part = zp if lang == "zh" else ep
        body = CONTENT.get(fname, "") + quizzes.render(fname)
        parts.append(
            f'<section class="print-lesson"><div class="part">{part}</div>'
            f"<h1>{title}</h1>{body}</section>"
        )
    combined = "".join(parts).replace("<details", "<details open")
    html = (
        f'<!doctype html>\n<html lang="{lang}" data-lang="{lang}">\n<head>\n'
        '<meta charset="utf-8">\n'
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
