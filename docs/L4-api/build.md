# L4 — `src/registry.py`, `src/quizzes.py`, `src/build.py`, `src/build_print.py`

## `registry.py`
- `CONTENT: dict[str, str]` — ordered `{lesson_filename: html}`. Built by importing every
  content module (`part1..part7`, `glossary`) and merging each module's `LESSONS`. The single
  source of lesson bodies shared by `build.py` and `build_print.py`.

## `quizzes.py`
- `QUIZZES: dict[str, list]` — `{filename: [question, …]}` where a question is
  `(q_zh, q_en, [(opt_zh, opt_en, is_correct), …], exp_zh, exp_en)`.
- `render(fname) -> str` — the bilingual quiz `<section>` for `fname`, or `""` if none.
  JS-free: the correct answer + explanation are revealed via `<details>`.
- `_aggregate()` — imports each content module in `_PART_MODULES` (defensively skipping
  missing ones) and merges its `QUIZZES`. Called once at import.

## `build.py`
- `DEFAULT_ROOT` — repo root (parent of `src/`).
- `build(root=DEFAULT_ROOT) -> list[str]` — writes `index.html` + `lessons/NN-*.html` (each
  body = `CONTENT.get(fname, "") + quizzes.render(fname)`, wrapped by `shell.page`). Returns
  the list of written relative paths. CLI prints a summary.

## `build_print.py`
- `_PRINT_CSS` — print-only overrides (page breaks per lesson; hide topbar/nav/toggle).
- `build_print(lang, root=DEFAULT_ROOT) -> str` — writes one continuous single-language
  `print.<lang>.html` (all lessons stacked; `<details>` force-opened so accordions/quiz
  answers print expanded) and returns its path. `lang ∈ {"zh","en"}`.
- CLI: `--lang zh|en` (default `zh`).
