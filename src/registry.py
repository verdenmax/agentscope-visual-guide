"""Single source of truth: ordered map of output filename -> lesson HTML.

Each content module exposes a ``LESSONS`` dict ({filename: html}); this registry
merges them in lesson order into ``CONTENT``. Both ``build.py`` and
``build_print.py`` import it so the lesson set stays in sync.
"""

import part1
import part2
import part3
import part4
import part5
import part6
import part7
import glossary

CONTENT: dict = {}
for _module in (part1, part2, part3, part4, part5, part6, part7, glossary):
    CONTENT.update(_module.LESSONS)
