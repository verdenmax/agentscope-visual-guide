import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import check_links  # noqa: E402


def _write(root, rel, html):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)


class TestCheckLinks(unittest.TestCase):
    def test_passes_when_targets_exist(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "index.html", '<a href="lessons/01.html">go</a>')
            _write(d, "lessons/01.html", '<a href="../index.html">home</a>')
            self.assertEqual(check_links.check(root=d), [])

    def test_flags_dead_link(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "index.html", '<a href="lessons/missing.html">x</a>')
            _write(d, "lessons/01.html", "<p>ok</p>")
            errs = check_links.check(root=d)
            self.assertTrue(any("missing.html" in e for e in errs))

    def test_ignores_external_and_anchor(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "index.html",
                   '<a href="https://x.com">e</a><a href="#top">a</a>')
            self.assertEqual(check_links.check(root=d), [])
