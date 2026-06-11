"""Fail the build if any internal link points to a missing file."""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
_HREF = re.compile(r'href="([^"]+)"')
_EXTERNAL = ("http://", "https://", "#", "mailto:", "data:")


def _html_files(root: str) -> list:
    files = []
    index = os.path.join(root, "index.html")
    if os.path.exists(index):
        files.append(index)
    lessons = os.path.join(root, "lessons")
    if os.path.isdir(lessons):
        files += [
            os.path.join(lessons, f)
            for f in sorted(os.listdir(lessons))
            if f.endswith(".html")
        ]
    return files


def check(root: str = DEFAULT_ROOT) -> list:
    """Return a list of dead-link descriptions (empty == all good)."""
    errors = []
    for fp in _html_files(root):
        base = os.path.dirname(fp)
        with open(fp, encoding="utf-8") as fh:
            html = fh.read()
        for href in _HREF.findall(html):
            if href.startswith(_EXTERNAL):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            path = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(path):
                errors.append(f"{os.path.relpath(fp, root)} -> {href}")
    return errors


if __name__ == "__main__":
    errs = check()
    if errs:
        print("Dead internal links:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    print("Link check OK")
