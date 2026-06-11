import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import shell  # noqa: E402


class TestDesignSystem(unittest.TestCase):
    def test_accent_is_violet(self):
        self.assertIn("#6d5ae6", shell.CSS)

    def test_bilingual_visibility_rules_present(self):
        self.assertIn('html[data-lang="zh"] [lang="en"]', shell.CSS)
        self.assertIn('html[data-lang="en"] [lang="zh"]', shell.CSS)

    def test_lang_toggle_styled(self):
        self.assertIn(".lang-toggle", shell.CSS)

    def test_favicon_is_data_uri(self):
        self.assertTrue(shell.FAVICON.startswith("data:image/svg+xml;base64,"))

    def test_head_meta_has_title_and_description(self):
        out = shell.head_meta("消息系统", "Messages", "描述", "Desc")
        self.assertIn("Messages", out)
        self.assertIn("描述", out)

    def test_head_meta_escapes_special_chars(self):
        out = shell.head_meta("A & B", "C & D", "d<e>f", "x")
        self.assertNotIn("A & B", out)        # raw & must be escaped
        self.assertIn("A &amp; B", out)
        self.assertIn("d&lt;e&gt;f", out)

    def test_page_escapes_ampersand_in_title(self):
        # PAGES entry "工作区 & 沙箱" / "Workspace & Sandbox" must not leak raw &
        out = shell.page("17-workspace.html", "x",
                         standalone=True, home_href="../index.html")
        self.assertNotIn("Workspace & Sandbox", out)
        self.assertIn("Workspace &amp; Sandbox", out)


class TestPage(unittest.TestCase):
    def _page(self):
        return shell.page("03-lifecycle.html", "<p>BODY</p>",
                          standalone=True, home_href="../index.html")

    def test_doctype_and_default_lang(self):
        out = self._page()
        self.assertTrue(out.lstrip().lower().startswith("<!doctype html>"))
        self.assertIn('data-lang="zh"', out)

    def test_contains_toggle_button(self):
        self.assertIn('id="langtoggle"', self._page())

    def test_localstorage_key_used(self):
        self.assertIn("asvg-lang", self._page())

    def test_body_and_css_embedded(self):
        out = self._page()
        self.assertIn("<p>BODY</p>", out)
        self.assertIn("#6d5ae6", out)

    def test_prev_next_links_resolved(self):
        out = self._page()
        self.assertIn("02-architecture.html", out)
        self.assertIn("04-messages.html", out)

    def test_first_page_has_no_prev(self):
        out = shell.page("01-what-is-agentscope.html", "x",
                         standalone=True, home_href="../index.html")
        self.assertNotIn('rel="prev"', out)


class TestPages(unittest.TestCase):
    def test_29_pages(self):
        self.assertEqual(len(shell.PAGES), 29)

    def test_each_page_is_5_tuple(self):
        for row in shell.PAGES:
            self.assertEqual(len(row), 5)

    def test_filenames_unique_and_numbered(self):
        files = [r[0] for r in shell.PAGES]
        self.assertEqual(len(files), len(set(files)))
        self.assertTrue(files[0].startswith("01-"))
        self.assertTrue(files[-1].startswith("29-"))


class TestIndex(unittest.TestCase):
    def test_index_lists_all_lessons(self):
        out = shell.index_page(standalone=True, lesson_prefix="lessons/")
        for f, *_ in shell.PAGES:
            self.assertIn(f"lessons/{f}", out)

    def test_index_has_bilingual_title_and_toggle(self):
        out = shell.index_page(standalone=True, lesson_prefix="lessons/")
        self.assertIn("AgentScope", out)
        self.assertIn('id="langtoggle"', out)
