# L4 — `src/check_links.py`, `src/check_html.py`

Both are runnable as scripts (exit non-zero on failure) and importable for tests
(`check(root=...)` returns a list of problem strings; empty == OK). Both scan `index.html`
plus every `lessons/*.html`.

## `check_links.py`
- `check(root=DEFAULT_ROOT) -> list[str]` — for every `href="…"`, resolve relative targets
  against the file's directory and report any whose file is missing. External schemes and
  anchors (`http://`, `https://`, `#`, `mailto:`, `data:`) and pure `#frag` links are ignored;
  a `path#frag` link is checked against `path`.
- `_html_files(root)` — ordered list of HTML files to scan.
- `_HREF` — `re.compile(r'href="([^"]+)"')`.

## `check_html.py`
- `check(root=DEFAULT_ROOT) -> list[str]` — per page, report:
  - `lang count mismatch` when content `lang="zh"` count ≠ `lang="en"` count, and
  - `missing language toggle button` when `id="langtoggle"` is absent.
- The counts use `_ZH`/`_EN` = `re.compile(r'(?<![-\w])lang="xx"')`: the negative lookbehind
  excludes `data-lang="…"`, and the single `<html lang="zh">` root is subtracted from the zh
  count so a balanced page nets equal counts.
- `_html_files(root)` — ordered list of HTML files to scan.
