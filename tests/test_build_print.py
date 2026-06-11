import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import build_print  # noqa: E402


class TestBuildPrint(unittest.TestCase):
    def test_zh_print_doc(self):
        with tempfile.TemporaryDirectory() as d:
            out = build_print.build_print("zh", root=d)
            html = open(out, encoding="utf-8").read()
            self.assertTrue(out.endswith("print.zh.html"))
            self.assertIn('data-lang="zh"', html)
            # every <details> must be force-opened (no bare <details> remains)
            self.assertIsNone(re.search(r"<details(?! open)", html))
            self.assertNotIn('id="langtoggle"', html)

    def test_details_are_opened_when_present(self):
        # inject a lesson with an accordion to exercise the open transform
        import registry
        from i18n import accordion
        key = next(iter(registry.CONTENT))
        original = registry.CONTENT[key]
        registry.CONTENT[key] = original + accordion("展开", "Expand", "<p>x</p>")
        try:
            with tempfile.TemporaryDirectory() as d:
                html = open(build_print.build_print("zh", root=d),
                            encoding="utf-8").read()
                self.assertIn("<details open", html)
        finally:
            registry.CONTENT[key] = original

    def test_en_print_doc(self):
        with tempfile.TemporaryDirectory() as d:
            out = build_print.build_print("en", root=d)
            html = open(out, encoding="utf-8").read()
            self.assertIn('data-lang="en"', html)

    def test_en_print_doc(self):
        with tempfile.TemporaryDirectory() as d:
            out = build_print.build_print("en", root=d)
            html = open(out, encoding="utf-8").read()
            self.assertIn('data-lang="en"', html)
