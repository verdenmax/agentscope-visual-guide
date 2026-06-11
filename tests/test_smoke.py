import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestHarness(unittest.TestCase):
    def test_runner_works(self):
        self.assertTrue(True)
