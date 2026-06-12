# L4 — content modules (`part1.py … part7.py`, `glossary.py`)

The lessons themselves, authored with the `i18n` DSL and verified against the AgentScope 2.0
source tree.

## Conventions (every content module)
- Imports the DSL:
  `from i18n import (lead, h2, h3, p, card, code, table, accordion, keypoints, source_map, analogy, note, tip, important, highlight, blocks, t)`
- Exposes two module-level dicts:
  - `LESSONS: dict[str, str]` — `{lesson_filename: rendered_html}`.
  - `QUIZZES: dict[str, list]` — `{lesson_filename: [question, …]}` (see `quizzes.md` for the
    question tuple shape).
- `registry.py` merges every module's `LESSONS` into `CONTENT`; `quizzes.py` merges every
  module's `QUIZZES`.

## Module → lessons

| Module | Lessons (filenames) |
|--------|---------------------|
| `part1.py` | `00-setup`, `01-what-is-agentscope`, `02-architecture`, `03-lifecycle` |
| `part2.py` | `04-messages`, `05-chat-models`, `06-credentials`, `07-tools`, `08-agents-intro` |
| `part3.py` | `09-event-system`, `10-streaming`, `11-formatter` |
| `part4.py` | `12-agent-internals`, `13-toolkit-internals`, `14-model-internals`, `15-middleware` |
| `part5.py` | `16-permission`, `17-workspace`, `18-mcp`, `19-state-tasks`, `20-skills`, `21-embeddings`, `22-tts` |
| `part6.py` | `23-agent-service`, `24-message-bus`, `25-agent-team` |
| `part7.py` | `26-custom-tools`, `27-custom-middleware`, `28-capstone` |
| `glossary.py` | `29-glossary` |

> Note: `part1.py` also defines individual `LESSON_00/01/02/03` names (it was the exemplar);
> all modules additionally expose the uniform `LESSONS` dict used for integration.

## Accuracy policy
Every code example uses the real public API; every `source_map` entry cites a real **file +
symbol** (never line numbers). Content is verified against `agentscope/src/agentscope` and
anchored to AgentScope 2.0 (2026-06).
