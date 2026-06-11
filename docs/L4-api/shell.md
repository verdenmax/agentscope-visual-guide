# L4 — `src/shell.py`

Design system, page shells, and the lesson registry of record.

## Constants
- `ACCENT = "#6d5ae6"` — the violet accent (also the favicon fill).
- `FAVICON` — inline base64 SVG data URI ("AS" on a violet rounded square).
- `INDEX_FILE = "index.html"`.
- `CSS` — the full design system: violet tokens + dark override, the two bilingual visibility
  rules, `.lang-toggle`, and every component style.
- `PAGES` — ordered `list[(file, zh_title, en_title, zh_part, en_part)]`, 29 entries. Single
  source for lesson order, titles, part grouping, progress %, and prev/next.
- `_HEAD_LANG_SCRIPT`, `_TOGGLE_SCRIPT` — the no-flash language init and the toggle wiring.

## Functions
- `head_meta(zh_title, en_title, zh_desc, en_desc) -> str` — SEO/social meta + favicon link.
  Escapes the combined title and the (zh) description via `esc`.
- `page(fname, content, standalone, home_href) -> str` — full lesson page: doctype, head
  (meta + `CSS`), sticky topbar (home link, part pill, `#langtoggle`, progress bar), hero
  (part label + bilingual `<h1>`), the `content`, prev/next nav, footer (version anchor), and
  the toggle script. PAGES-derived titles/labels are escaped before display.
- `index_page(standalone, lesson_prefix) -> str` — the TOC page: groups `PAGES` by part
  (preserving order) and links each lesson as `{lesson_prefix}{file}`.
- `_page_index(fname) -> int` — index of `fname` in `PAGES` (raises `KeyError` if absent).

## Notes
- Imports `t`, `esc` from `i18n`.
- Targets Python 3.11+: HTML is assembled by concatenating f-strings that interpolate only
  precomputed local variables (no nested function calls with string literals inside
  `f"""…"""`, which would require 3.12+).
