"""Build the AgentScope visual guide as a standalone static site.

Produces ``index.html`` + ``lessons/NN-*.html`` (relative links; works via
``file://`` or any static server).

Usage:
    cd src && python build.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import shell  # noqa: E402
import quizzes  # noqa: E402
from registry import CONTENT  # noqa: E402


def build(root: str = DEFAULT_ROOT) -> list:
    """Write the full site under ``root``; return the list of written paths."""
    lessons_dir = os.path.join(root, "lessons")
    os.makedirs(lessons_dir, exist_ok=True)
    written = []
    for fname, *_ in shell.PAGES:
        body = CONTENT.get(fname, "") + quizzes.render(fname)
        html = shell.page(fname, body, standalone=True, home_href="../index.html")
        with open(os.path.join(lessons_dir, fname), "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(os.path.join("lessons", fname))
    with open(os.path.join(root, shell.INDEX_FILE), "w", encoding="utf-8") as fh:
        fh.write(shell.index_page(standalone=True, lesson_prefix="lessons/"))
    written.append(shell.INDEX_FILE)
    return written


if __name__ == "__main__":
    done = build()
    print("Wrote", len(done), "files under", DEFAULT_ROOT)
    for f in done:
        print("  -", f)
