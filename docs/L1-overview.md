# L1 — Overview

## What this is

A **zero-dependency** (Python 3.11+ stdlib only) static-site generator that produces a
bilingual (中文 / English) HTML learning guide for AgentScope 2.0: an `index.html` table of
contents plus 30 lesson pages under `lessons/`, and single-language print documents for PDF.

## Build flow

```
content modules            shell.py (design system + page shells)
part1..part7, glossary  ─┐        │
   (LESSONS, QUIZZES)    │        │
                         ▼        ▼
registry.py  ──CONTENT──► build.py ──► index.html + lessons/NN-*.html
quizzes.py   ──render()──►   │
                            (same inputs)
                             ▼
                       build_print.py --lang zh|en ──► print.zh.html / print.en.html ──► PDF (CI)
```

1. **Content** is authored with the bilingual DSL in `i18n.py` and grouped into
   `part1.py … part7.py` + `glossary.py`. Each module exposes `LESSONS` (filename → HTML)
   and `QUIZZES` (filename → questions).
2. **`registry.py`** aggregates every module's `LESSONS` into one ordered `CONTENT` map;
   **`quizzes.py`** aggregates every module's `QUIZZES`.
3. **`shell.py`** owns the CSS design system, the page/index HTML shells, the 29-entry
   `PAGES` table (order, titles, part labels), and the bilingual toggle.
4. **`build.py`** renders `index.html` + every lesson; **`build_print.py`** renders a single
   continuous, single-language document for PDF.
5. **`check_links.py`** and **`check_html.py`** guard the output (no dead internal links;
   balanced bilingual structure).

## Bilingual approach (one paragraph)

Every piece of text is emitted **twice** — once tagged `lang="zh"`, once `lang="en"`. A root
attribute `<html data-lang="zh">` plus two CSS rules hide the inactive language; a small
toggle button flips `data-lang` and persists the choice to `localStorage`. The result stays a
single self-contained file per lesson that works over `file://`.

## How to run

```bash
python -m unittest discover -s tests -v          # tests
cd src && python build.py                         # build site
cd src && python check_links.py && python check_html.py
cd src && python build_print.py --lang zh         # print doc for PDF
```
