"""Single source of truth: ordered map of output filename -> lesson HTML.

Each content module exposes a ``LESSONS`` dict ({filename: html}); this registry
merges them into ``CONTENT``. Both ``build.py`` and ``build_print.py`` import it
so the lesson set stays in sync. Modules are added as content lands (Tasks 14-21).
"""

import part1
import glossary

CONTENT: dict = {}
CONTENT.update(part1.LESSONS)
CONTENT.update(glossary.LESSONS)
