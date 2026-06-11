# L3 — Details

## Bilingual mechanism

The guide ships **both** languages in every page and shows one at a time, with no framework
and no second page tree.

1. **Authoring:** every DSL helper emits both variants, e.g. `p("你好","Hi")` →
   `<p lang="zh">你好</p><p lang="en">Hi</p>`. Inline fragments use `t(zh, en)` →
   `<span lang="zh">…</span><span lang="en">…</span>`.
2. **Visibility:** two CSS rules in `shell.CSS` do all the work:
   ```css
   html[data-lang="zh"] [lang="en"] { display: none; }
   html[data-lang="en"] [lang="zh"] { display: none; }
   ```
3. **Default + no-flash:** a tiny `<head>` script sets `data-lang` from `localStorage`
   (key `asvg-lang`, default `zh`) before paint.
4. **Toggle:** a body-end script wires `#langtoggle` to flip `data-lang`, update `<html lang>`,
   persist to `localStorage`, and relabel the button (中文 ⇄ EN).

**The DSL rule:** block helpers (`p`, `h2`, `card`, …) take full `zh`/`en` strings; inline
`t()` is only for shared containers (`th`/`td`/`li`/`summary`). Never nest `t()` inside a
block helper, and never nest opposite-language elements — otherwise the visibility CSS hides
the wrong thing. `check_html.py` enforces the per-page balance as a backstop.

## DSL block semantics

- **`code(src, lang, cap_zh, cap_en)`** — the code is shared (language-neutral); only the
  optional caption is bilingual. Output is `<pre class="code">…</pre>`, or wrapped in
  `<figure class="code-fig">` when a caption is given.
- **`table(headers, rows)`** — `headers=[(zh,en)]`, `rows=[[(zh,en),…]]`; every cell is a
  `t()` pair.
- **`accordion(sum_zh, sum_en, body, num)`** — `<details>`; `body` is pre-rendered HTML
  (compose with `blocks(...)`).
- **`source_map(items)`** — `items=[(file, zh_desc, en_desc)]`; renders a file→description
  table. Cite **file + symbol**, never line numbers (they drift on upstream updates).

## Python syntax highlighter

`code(..., lang="python")` highlights via the stdlib `tokenize` module — robust and
dependency-free:

- Tokens are classified into `kw` (keywords + soft keywords), `st` (strings), `cm` (comments),
  `nu` (numbers); everything else is escaped plain text.
- Because real tokenization is used, **keywords inside strings/comments are not highlighted**.
- Unparseable snippets fall back to fully-escaped text (no crash); non-Python `lang` is
  escaped only.
- **Line model:** `_line_starts` splits on `"\n"` **only**, to match how `tokenize` (reading
  via `io.StringIO(src).readline`) counts lines. Using `str.splitlines()` here would also
  split on `\f`, `\v`, `\u2028`, `\x85`, … desyncing token offsets and corrupting output.

## CSS design system

`shell.CSS` defines violet design tokens (`--accent:#6d5ae6`) with a full
`prefers-color-scheme: dark` override, then styles every component: topbar + progress,
hero, cards (`note`/`tip`/`important`/`analogy`), `pre.code` + token colors, accordion,
keypoints, `srcmap`, tables, quiz, lesson nav, footer, and the index TOC. All values flow
from CSS variables, so the skin is changed in one place.

## Escaping

Framework-controlled strings that originate from `PAGES` (titles, part labels) and `head_meta`
descriptions are passed through `i18n.esc()` at every render site (`<title>`, `<h1>`, the
pill, nav titles, the TOC, and all meta tags). This keeps output valid even for titles
containing `&`/`<`/`>` (e.g. "Workspace & Sandbox"). Content authored via the DSL is the
author's responsibility to keep well-formed (use `&amp;` etc. inside block strings).

## CI pipeline

- **`ci.yml`** (push/PR): run unit tests; rebuild and `git diff --exit-code` on
  `index.html`+`lessons/` (drift guard); run `check_links.py` and `check_html.py`.
- **`deploy.yml`** (push to `main` / `v*` tags): rebuild site + both print docs, install
  Chromium + Noto CJK/emoji fonts, render the two PDFs, deploy `index.html` + `lessons/` +
  PDFs to GitHub Pages, and attach the PDFs to a Release on tags.
- **One-time:** the repo owner must set Settings → Pages → Source: GitHub Actions (the
  Actions token can deploy to, but not create, the Pages site).
