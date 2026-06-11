# L2 — Components

Each `src/` module, its single responsibility, and its public interface.

## `i18n.py` — bilingual block DSL
The vocabulary every lesson is written in. Pure functions that each take a `(zh, en)` pair
and return HTML containing **both** language variants.
- **Inline:** `esc(s)`, `t(zh, en)`.
- **Text blocks:** `lead`, `p`, `h2`, `h3`.
- **Cards:** `card(zh, en, kind=...)` + shortcuts `analogy`, `note`, `tip`, `important`,
  `highlight`.
- **Rich blocks:** `code(src, lang="python", cap_zh=, cap_en=)`, `table(headers, rows)`,
  `accordion(sum_zh, sum_en, body, num=)`, `keypoints(items)`, `source_map(items)`.
- **Glue:** `blocks(*parts)`.
- Depends on: stdlib only (`html`, `io`, `keyword`, `tokenize`).

## `shell.py` — design system + page shells
Owns everything visual and structural that surrounds lesson content.
- `CSS` (violet design tokens, light/dark, the two bilingual visibility rules, every
  component style), `FAVICON`, `ACCENT`, `INDEX_FILE`.
- `head_meta(zh_title, en_title, zh_desc, en_desc)` — escaped meta tags.
- `PAGES` — the ordered list of 29 `(file, zh_title, en_title, zh_part, en_part)` tuples
  (single source of lesson order, titles, part grouping, progress, prev/next).
- `page(fname, content, standalone, home_href)` — full lesson HTML.
- `index_page(standalone, lesson_prefix)` — the table-of-contents page.
- Depends on: `i18n` (`t`, `esc`).

## `registry.py` — content map
`CONTENT`: ordered `{filename: html}` built by aggregating each content module's `LESSONS`.
Single source shared by `build.py` and `build_print.py`. Depends on: `part1..part7`, `glossary`.

## `part1.py … part7.py`, `glossary.py` — content
The lessons themselves, authored with the DSL. Each exposes `LESSONS` (`{filename: html}`) and
`QUIZZES` (`{filename: [questions]}`). Depend on: `i18n`. (Verified against the AgentScope
source — see each module's source-mapping blocks.)

## `quizzes.py` — quiz renderer
`render(fname)` → the bilingual quiz `<section>` for a lesson (or `""`). `QUIZZES` is
aggregated from every content module at import. Depends on: `i18n` (`t`) + content modules.

## `build.py` — site build
`build(root=...)` writes `index.html` + `lessons/NN-*.html` (each = `CONTENT.get(fname,"")` +
`quizzes.render(fname)`, wrapped by `shell.page`). Depends on: `shell`, `registry`, `quizzes`.

## `build_print.py` — print build
`build_print(lang, root=...)` writes one continuous single-language `print.<lang>.html`
(accordions/quiz answers force-opened; topbar/nav hidden) for headless-Chrome PDF rendering.
Depends on: `shell`, `registry`, `quizzes`.

## `check_links.py` — link checker
`check(root=...)` → list of internal links whose target file is missing (external/anchor
links ignored). CLI exits non-zero on failure.

## `check_html.py` — structure checker
`check(root=...)` → list of pages where content `lang="zh"` count ≠ `lang="en"` count (the
`<html>` root excluded) or the toggle button is missing. CLI exits non-zero on failure.
