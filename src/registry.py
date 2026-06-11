"""Single source of truth: ordered map of output filename -> lesson HTML.

Both ``build.py`` and ``build_print.py`` import this so the lesson set stays in
sync. Entries are added as content modules land (Tasks 14–21).
"""

import part1

CONTENT = {
    "01-what-is-agentscope.html": part1.LESSON_01,
}
