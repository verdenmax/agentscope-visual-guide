"""Fail the build on broken bilingual structure.

Checks per page:
  * content ``lang="zh"`` count == ``lang="en"`` count (excluding the <html> root);
  * the language toggle button is present.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
# match lang="xx" NOT preceded by '-' or a word char (excludes data-lang=)
_ZH = re.compile(r'(?<![-\w])lang="zh"')
_EN = re.compile(r'(?<![-\w])lang="en"')


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
    """Return structural problems (empty == all good)."""
    errors = []
    for fp in _html_files(root):
        rel = os.path.relpath(fp, root)
        with open(fp, encoding="utf-8") as fh:
            html = fh.read()
        zh = len(_ZH.findall(html)) - 1  # exclude the single <html lang="zh"> root
        en = len(_EN.findall(html))
        if zh != en:
            errors.append(f"{rel}: lang count mismatch zh={zh} en={en}")
        if 'id="langtoggle"' not in html:
            errors.append(f"{rel}: missing language toggle button")
    return errors


if __name__ == "__main__":
    errs = check()
    if errs:
        print("HTML structure problems:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    print("HTML check OK")
