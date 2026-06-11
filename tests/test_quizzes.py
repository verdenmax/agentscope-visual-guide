import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import quizzes  # noqa: E402


class TestQuizzes(unittest.TestCase):
    def test_unknown_file_renders_empty(self):
        self.assertEqual(quizzes.render("does-not-exist.html"), "")

    def test_render_includes_prompt_options_and_answer(self):
        quizzes.QUIZZES["x.html"] = [
            (
                "AgentScope 的核心循环是什么？",
                "What is AgentScope's core loop?",
                [
                    ("ReAct 推理-行动循环", "ReAct reasoning-acting loop", True),
                    ("纯模板", "Pure templates", False),
                ],
                "Agent 使用推理-行动循环。",
                "The Agent uses a reasoning-acting loop.",
            )
        ]
        try:
            out = quizzes.render("x.html")
            self.assertIn('<section class="quiz">', out)
            self.assertIn("核心循环", out)
            self.assertIn("core loop", out)
            self.assertIn("<details", out)
            self.assertIn("ReAct 推理-行动循环", out)
        finally:
            del quizzes.QUIZZES["x.html"]
