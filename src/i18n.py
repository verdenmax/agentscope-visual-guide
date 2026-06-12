"""Bilingual block DSL for the AgentScope visual guide.

Every helper emits BOTH language variants tagged ``lang="zh"`` / ``lang="en"``.
Pure CSS (see ``shell.py``) shows only the active language. Block helpers take
full ``zh``/``en`` strings; inside those strings use language-neutral inline HTML
only. Inline ``t()`` is for bilingual fragments inside shared containers
(``th``/``td``/``li``/``summary``) — never nested inside a block helper.
"""

import html
import io
import keyword
import tokenize

__all__ = [
    "esc", "t", "lead", "p", "h2", "h3", "card", "table", "code",
    "accordion", "keypoints", "source_map", "analogy", "note", "tip",
    "important", "highlight", "blocks", "steps",
]


def esc(s: str) -> str:
    """HTML-escape text including quotes."""
    return html.escape(s, quote=True)


def t(zh: str, en: str) -> str:
    """Inline bilingual span pair (for use inside shared containers)."""
    return f'<span lang="zh">{zh}</span><span lang="en">{en}</span>'


def lead(zh: str, en: str) -> str:
    """Lead paragraph pair."""
    return f'<p class="lead" lang="zh">{zh}</p><p class="lead" lang="en">{en}</p>'


def p(zh: str, en: str) -> str:
    """Paragraph pair."""
    return f'<p lang="zh">{zh}</p><p lang="en">{en}</p>'


def h2(zh: str, en: str) -> str:
    """``<h2>`` pair."""
    return f'<h2 lang="zh">{zh}</h2><h2 lang="en">{en}</h2>'


def h3(zh: str, en: str) -> str:
    """``<h3>`` pair."""
    return f'<h3 lang="zh">{zh}</h3><h3 lang="en">{en}</h3>'


_CARD_TAGS = {
    "analogy": ("🧩 生活类比", "🧩 Analogy"),
    "note": ("📌 注意", "📌 Note"),
    "tip": ("💡 提示", "💡 Tip"),
    "important": ("⚠️ 重要", "⚠️ Important"),
}


def card(
    zh: str,
    en: str,
    kind: str = "note",
    tag_zh: str | None = None,
    tag_en: str | None = None,
) -> str:
    """A callout card. ``kind`` ∈ {note, tip, important, analogy}."""
    default_zh, default_en = _CARD_TAGS.get(kind, _CARD_TAGS["note"])
    tag = f'<div class="tag">{t(tag_zh or default_zh, tag_en or default_en)}</div>'
    return (
        f'<div class="card {kind}">{tag}'
        f'<div lang="zh">{zh}</div><div lang="en">{en}</div></div>'
    )


def table(headers: list, rows: list) -> str:
    """Bilingual table. ``headers``: list[(zh, en)]; ``rows``: list[list[(zh, en)]]."""
    head = "".join(f"<th>{t(z, e)}</th>" for z, e in headers)
    body = ""
    for row in rows:
        cells = "".join(f"<td>{t(z, e)}</td>" for z, e in row)
        body += f"<tr>{cells}</tr>"
    return f'<table class="t"><tr>{head}</tr>{body}</table>'


def _line_starts(src: str) -> list:
    # Offsets must follow tokenize's line model, which breaks on "\n" only.
    # (str.splitlines also splits on \f, \v, \u2028, \x85, ... — using it here
    # would desync token positions and corrupt the reconstructed text.)
    starts = [0]
    for part in src.split("\n"):
        starts.append(starts[-1] + len(part) + 1)
    return starts


def _highlight_python(src: str) -> str:
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return esc(src)
    starts = _line_starts(src)

    def off(pos: tuple) -> int:
        row, col = pos
        if row - 1 >= len(starts):
            return len(src)
        return min(starts[row - 1] + col, len(src))

    out, prev = [], 0
    for tok in toks:
        s, e = off(tok.start), off(tok.end)
        if s > prev:
            out.append(esc(src[prev:s]))
        text = src[s:e]
        cls = None
        if tok.type == tokenize.COMMENT:
            cls = "cm"
        elif tok.type == tokenize.STRING:
            cls = "st"
        elif tok.type == tokenize.NUMBER:
            cls = "nu"
        elif tok.type == tokenize.NAME and (
            keyword.iskeyword(text) or keyword.issoftkeyword(text)
        ):
            cls = "kw"
        out.append(f'<span class="{cls}">{esc(text)}</span>' if cls else esc(text))
        prev = e
    if prev < len(src):
        out.append(esc(src[prev:]))
    return "".join(out)


def _highlight(src: str, lang: str) -> str:
    return _highlight_python(src) if lang == "python" else esc(src)


def code(
    src: str,
    lang: str = "python",
    cap_zh: str | None = None,
    cap_en: str | None = None,
) -> str:
    """Code block (shared across languages). Optional bilingual caption."""
    body = _highlight(src.strip("\n"), lang)
    pre = f'<pre class="code" data-lang="{esc(lang)}">{body}</pre>'
    if cap_zh is None and cap_en is None:
        return pre
    cap = (
        f'<div class="code-cap" lang="zh">{cap_zh or ""}</div>'
        f'<div class="code-cap" lang="en">{cap_en or ""}</div>'
    )
    return f'<figure class="code-fig">{pre}{cap}</figure>'


def accordion(sum_zh: str, sum_en: str, body: str, num: int | None = None) -> str:
    """Collapsible deep-dive card. ``body`` is pre-rendered HTML."""
    badge = f'<span class="badge-num">{num}</span>' if num is not None else ""
    hint = f'<span class="hint">{t("点击展开", "expand")}</span>'
    summary = f"<summary>{badge}{t(sum_zh, sum_en)} {hint}</summary>"
    return (
        f'<details class="accordion">{summary}'
        f'<div class="acc-body">{body}</div></details>'
    )


def keypoints(
    items: list,
    title_zh: str = "✅ 关键要点",
    title_en: str = "✅ Key takeaways",
) -> str:
    """A titled list of bilingual takeaways. ``items``: list[(zh, en)]."""
    lis = "".join(f"<li>{t(z, e)}</li>" for z, e in items)
    return (
        f'<div class="keypoints"><div class="kp-title">'
        f"{t(title_zh, title_en)}</div><ul>{lis}</ul></div>"
    )


def steps(items: list) -> str:
    """Always-visible numbered steps for a process/flow.

    ``items``: list[(zh_title, en_title, zh_body, en_body)]. Use this for core
    sequences (e.g. a lifecycle or loop) instead of collapsed accordions.
    """
    out = []
    for i, (zt, et, zb, eb) in enumerate(items, 1):
        out.append(
            f'<div class="step"><div class="step-n">{i}</div>'
            f'<div class="step-c"><div class="step-t">{t(zt, et)}</div>'
            f'<div class="step-b">{t(zb, eb)}</div></div></div>'
        )
    return f'<div class="steps">{"".join(out)}</div>'


def source_map(
    items: list,
    title_zh: str = "🔬 源码对应",
    title_en: str = "🔬 Source mapping",
) -> str:
    """Map real source files to bilingual descriptions.

    ``items``: list[(file, zh_desc, en_desc)]. Cite file + symbol, never line numbers.
    """
    rows = "".join(
        f"<tr><td><code>{esc(f)}</code></td><td>{t(z, e)}</td></tr>"
        for f, z, e in items
    )
    return (
        f'<div class="srcmap"><div class="kp-title">{t(title_zh, title_en)}</div>'
        f'<table class="t">{rows}</table></div>'
    )


def analogy(zh: str, en: str) -> str:
    """Everyday-metaphor card."""
    return card(zh, en, kind="analogy")


def note(zh: str, en: str) -> str:
    """Note card."""
    return card(zh, en, kind="note")


def tip(zh: str, en: str) -> str:
    """Tip card."""
    return card(zh, en, kind="tip")


def important(zh: str, en: str) -> str:
    """Important-callout card."""
    return card(zh, en, kind="important")


def highlight(zh: str, en: str) -> str:
    """Design-highlight card (💡)."""
    return card(
        zh, en, kind="tip", tag_zh="💡 设计亮点", tag_en="💡 Design highlight"
    )


def blocks(*parts: str) -> str:
    """Concatenate rendered block strings."""
    return "".join(parts)
