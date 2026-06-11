import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import check_html  # noqa: E402


def _write(root, rel, html):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)


_GOOD = (
    '<html lang="zh" data-lang="zh"><body>'
    '<button id="langtoggle">EN</button>'
    '<p lang="zh">你好</p><p lang="en">Hi</p>'
    "</body></html>"
)
_BAD = (
    '<html lang="zh" data-lang="zh"><body>'
    '<button id="langtoggle">EN</button>'
    '<p lang="zh">你好</p><p lang="zh">缺英文</p><p lang="en">Hi</p>'
    "</body></html>"
)


class TestCheckHtml(unittest.TestCase):
    def test_balanced_page_passes(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "lessons/01.html", _GOOD)
            self.assertEqual(check_html.check(root=d), [])

    def test_unbalanced_page_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "lessons/01.html", _BAD)
            errs = check_html.check(root=d)
            self.assertTrue(any("mismatch" in e for e in errs))

    def test_missing_toggle_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "lessons/01.html",
                   '<html lang="zh" data-lang="zh"><body>'
                   '<p lang="zh">a</p><p lang="en">b</p></body></html>')
            errs = check_html.check(root=d)
            self.assertTrue(any("toggle" in e for e in errs))
