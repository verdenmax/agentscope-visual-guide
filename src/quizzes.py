"""Bilingual, JS-free end-of-lesson quizzes.

``QUIZZES`` maps a lesson filename to a list of questions:
    (q_zh, q_en, [(opt_zh, opt_en, is_correct)], exp_zh, exp_en)
``render(fname)`` returns "" when a lesson has no quiz.
"""

from i18n import t

QUIZZES: dict = {}


def render(fname: str) -> str:
    """Render the quiz block for ``fname`` (empty string if none)."""
    qs = QUIZZES.get(fname, [])
    if not qs:
        return ""
    title = t("🧠 小测验", "🧠 Quiz")
    ans_label = t("答案与解析", "Answer & explanation")
    out = []
    for q_zh, q_en, options, exp_zh, exp_en in qs:
        opts = "".join(f"<li>{t(oz, oe)}</li>" for oz, oe, _ in options)
        correct = next(
            (t(oz, oe) for oz, oe, ok in options if ok), t("—", "—")
        )
        out.append(
            f'<div class="quiz-q"><div class="quiz-prompt">{t(q_zh, q_en)}</div>'
            f'<ol class="quiz-opts">{opts}</ol>'
            f'<details class="quiz-ans"><summary>{ans_label}</summary>'
            f'<div class="quiz-correct">{correct}</div>'
            f'<div lang="zh">{exp_zh}</div>'
            f'<div lang="en">{exp_en}</div></details></div>'
        )
    return f'<section class="quiz"><h2>{title}</h2>{"".join(out)}</section>'
