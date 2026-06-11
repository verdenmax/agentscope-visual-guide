import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import registry  # noqa: E402


class TestRegistry(unittest.TestCase):
    def test_content_is_dict(self):
        self.assertIsInstance(registry.CONTENT, dict)

    def test_lesson_one_present_and_nonempty(self):
        self.assertIn("01-what-is-agentscope.html", registry.CONTENT)
        self.assertTrue(registry.CONTENT["01-what-is-agentscope.html"])

    def test_all_keys_are_known_pages(self):
        import shell
        valid = {row[0] for row in shell.PAGES}
        for key in registry.CONTENT:
            self.assertIn(key, valid)
