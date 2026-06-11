import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import build  # noqa: E402
import shell  # noqa: E402


class TestBuild(unittest.TestCase):
    def test_build_writes_index_and_all_lessons(self):
        with tempfile.TemporaryDirectory() as d:
            written = build.build(root=d)
            self.assertIn("index.html", written)
            self.assertTrue(os.path.exists(os.path.join(d, "index.html")))
            for fname, *_ in shell.PAGES:
                self.assertTrue(
                    os.path.exists(os.path.join(d, "lessons", fname)),
                    fname,
                )

    def test_lesson_page_has_bilingual_markers(self):
        with tempfile.TemporaryDirectory() as d:
            build.build(root=d)
            html = open(
                os.path.join(d, "lessons", "01-what-is-agentscope.html"),
                encoding="utf-8",
            ).read()
            self.assertIn('lang="zh"', html)
            self.assertIn('lang="en"', html)
            self.assertIn('id="langtoggle"', html)
