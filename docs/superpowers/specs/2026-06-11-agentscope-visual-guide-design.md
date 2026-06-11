# AgentScope 图解教程 · 设计文档 / Design Spec

- **Date / 日期**: 2026-06-11
- **Status / 状态**: Approved (design phase complete)
- **Topic / 主题**: A bilingual, visual (HTML) learning guide for the AgentScope 2.0 framework
- **Version anchor / 版本锚点**: AgentScope 2.0 source (`agentscope-ai/agentscope`), verified 2026-06
- **Reference / 参照**: `../langchain-visual-guide` (spirit & polish; generator built fresh)

---

## 1. Overview / 概述

A self-contained, zero-dependency static site that teaches the **AgentScope 2.0**
multi-agent framework to complete beginners and source-divers alike, following a
"**完全新手 → 会用 → 懂原理 / 读源码**" arc.

The site is **bilingual (中 / English)** with an in-page toggle, comprehensive
(29 lessons across 8 parts), and grounded in the **real** AgentScope public API
and source layout.

### Audience / 适用人群
- Newcomers who have never used AgentScope and want to start from zero.
- Learners who want the macro picture first, then internals.
- Developers preparing to read / debug / contribute to AgentScope source.

### Goals
- Explain every major module: `agent`, `model`, `tool`, `event`, `message`,
  `formatter`, `middleware`, `permission`, `workspace`, `mcp`, `state`, `skill`,
  `embedding`, `tts`, and the `app` (FastAPI agent service).
- Provide macro intuition + real source mapping (file + symbol) + everyday
  analogies + runnable code examples per lesson.
- Ship as a polished, portable static site (works via `file://` or any static
  server) plus downloadable PDFs.

### Non-goals (YAGNI)
- Not a replacement for official AgentScope docs.
- No runtime/JS framework, no build toolchain beyond Python 3 stdlib.
- No hard-coded source line numbers (they drift); cite **file + symbol** only.
- No server-side search; the glossary + index provide navigation.

---

## 2. Approved decisions / 已确认决策

| # | Decision | Choice |
|---|----------|--------|
| 1 | Location | New sibling repo `../agentscope-visual-guide/` (standalone) |
| 2 | Language | **Bilingual 中 / English** |
| 3 | Bilingual UX | **In-page 中/EN toggle**, single file per lesson, `file://`-portable |
| 4 | Scope | **Comprehensive — 29 lessons / 8 parts** |
| 5 | Build approach | **Fresh generator from scratch** (pure Python, zero deps) |
| 6 | Quizzes & glossary | **Keep both** (bilingual), full parity with reference |
| 7 | Accent color | **Violet/indigo `#6d5ae6`** |
| 8 | Page structure | **Flexible template** — adapt each page's sections to its content |
| 9 | PDF | **Two PDFs** (`-zh`, `-en`) via `build_print.py --lang` |
| 10 | Dev docs | **Layered L1–L4** docs for the generator under `docs/` |

---

## 3. Architecture / 架构

Pure **Python 3, stdlib only** (no third-party dependencies). Generator produces a
self-contained static site.

```
agentscope-visual-guide/
├── index.html              ← table of contents (generated)
├── lessons/NN-*.html       ← lesson pages (generated)
├── src/
│   ├── shell.py            design system (CSS), page/index shells, top nav,
│   │                       中/EN toggle, PAGES list, favicon
│   ├── i18n.py             ★ bilingual block DSL (the new core)
│   ├── part1.py … part8.py lesson content modules
│   ├── glossary.py         bilingual term index (lesson 29)
│   ├── quizzes.py          bilingual end-of-lesson quizzes
│   ├── registry.py         filename → lesson content map
│   ├── build.py            site build  → index.html + lessons/
│   ├── build_print.py      PDF source  → print.html (--lang zh|en)
│   ├── check_html.py       structural lint (balanced lang pairs, etc.)
│   └── check_links.py      internal-link check
├── docs/                   layered L1–L4 developer docs (see §9)
│   └── superpowers/specs/  this design doc
├── .github/workflows/{deploy.yml, ci.yml}
├── README.md  ·  LICENSE (MIT)  ·  .gitignore
```

`registry.py` is the single source of truth mapping output filename → content, so
`build.py` and `build_print.py` stay in sync. `shell.PAGES` defines lesson order,
short titles, and part labels.

---

## 4. Bilingual model / 双语机制

The core novelty. Every lesson is authored **once** through a small **block DSL**
(`i18n.py`) where each block accepts both languages.

- Helpers: `p(zh, en)`, `h2(zh, en)`, `h3(zh, en)`, inline `t(zh, en)`,
  `card(kind, zh, en)`, `code(lang, src, cap_zh=None, cap_en=None)`,
  `table(headers, rows)`, `accordion(summary, body)`, `keypoints([...])`,
  `note/tip/important/analogy` variants.
- Each block emits **both** language variants into the DOM, tagged
  `lang="zh"` / `lang="en"` on the appropriate block/inline element.
- A root attribute `<html data-lang="zh">` plus **pure CSS** controls visibility:
  ```css
  html[data-lang="zh"] [lang="en"] { display: none; }
  html[data-lang="en"] [lang="zh"] { display: none; }
  ```
- A **中/EN button** in the top bar flips `data-lang`, persists the choice to
  `localStorage`, and updates `<html lang>` for a11y/SEO. Default language: **zh**,
  remembered across pages. Tiny inline script, no per-element JS.
- **Code blocks** are shared (language-neutral Python); only optional captions are
  bilingual. Code comments are kept short/neutral or duplicated only when essential.

**Why this approach**: keeps single-file `file://` portability (no separate page
trees), no JS framework, and authoring stays DRY because each block carries its own
translation pair.

---

## 5. Lesson outline / 课程大纲 (29 lessons · 8 parts)

**Part 1 · 宏观全景 / Macro**
1. AgentScope 是什么 / What is AgentScope — problem it solves · 2.0 mental model (agentic LLM + event-driven)
2. 整体架构全景 / Architecture panorama — agent · model · tool · event · app layering
3. 一次 reply 的生命周期 / Lifecycle of a reply — `UserMsg` → event stream data flow

**Part 2 · 用户视角 / User's view**
4. 消息系统 / Messages — `Msg` family + ContentBlocks (Text/Thinking/ToolCall/ToolResult/Data)
5. 聊天模型 / Chat Models — `ChatModelBase` + multi-vendor + `ChatResponse`
6. 凭证管理 / Credentials — `CredentialBase` · `CredentialFactory`
7. 工具 Tools — `Toolkit` · built-in `Bash/Read/Write/Edit/Grep/Glob` · `FunctionTool`
8. Agent 入门 / Agent intro — `Agent(...)` · `reply` / `reply_stream` · ReAct loop

**Part 3 · 事件与流式 / Events & streaming**
9. 事件系统 / Event system — `EventType` full spectrum
10. 流式消费 / Streaming — `reply_stream` consumer state machine
11. Formatter / 多厂商适配 — Chat vs MultiAgent formatter

**Part 4 · 内部源码 / Internals**
12. Agent 内部 / Agent internals — reasoning-acting loop + middleware chain
13. Toolkit 内部 / Toolkit internals — `get_tool_schemas` (async) · `ToolGroup`
14. 模型调用内部 / Model-call internals — `ChatResponse` / `StructuredResponse`
15. 中间件系统 / Middleware — `MiddlewareBase` · Tracing · TTS

**Part 5 · 进阶能力 / Advanced**
16. 权限系统 / Permission — `PermissionEngine` · `Rule` · `Mode` · `Decision`
17. 工作区 & 沙箱 / Workspace — Local/Docker/E2B · `Offloader`
18. MCP 集成 / MCP — `MCPClient` · Stdio/Http config · `MCPTool`
19. 状态与任务 / State & Tasks — `AgentState` · `Task` · `TaskContext`
20. 技能系统 / Skills — `Skill` · `SkillLoader` · `LocalSkillLoader`
21. 嵌入与检索 / Embeddings — `EmbeddingModelBase` · cache (RAG基础)
22. TTS 语音 / TTS — `TTSModelBase` · Realtime TTS

**Part 6 · 服务化 / Productionization**
23. Agent Service — `create_app` (FastAPI) · multi-tenancy / multi-session
24. 消息总线 / Message Bus — registry primitives · bg_task · distributed cancel
25. Agent Team — leader-worker collaboration · team tools

**Part 7 · 自己动手 / Build your own**
26. 写自己的工具 / Custom tools — subclassing `ToolBase`
27. 写自己的中间件 / Custom middleware — `MiddlewareBase` hooks
28. 端到端实战 / Capstone — tools + permission + workspace → one agent

**Part 8 · 速查 / Reference**
29. 术语表 / Glossary — bilingual term index with deep links

---

## 6. Page design & per-lesson features / 页面设计

**Design system (`shell.py`)**: card-based layout, light/dark via
`prefers-color-scheme`, sticky top bar with progress, prev/next nav, responsive,
system-font stack with CJK fallbacks. Accent `--accent: #6d5ae6` (violet/indigo) +
inline SVG favicon.

**Top bar**: home link · part-label pill · **中/EN toggle** · progress bar.

**Per-lesson template (flexible — adapt to content, not a rigid checklist):**
- 🌍 大局观 / Big picture — why it's designed this way
- 🔬 源码对应 / Source mapping — real files by **file + symbol** (e.g. `agent/_agent.py`, `tool/_toolkit.py`)
- 🧩 生活类比 / Analogy
- 🧪 代码示例 / Code examples — real AgentScope API, shared code block
- ✅ 关键要点 / Key takeaways
- 💡 设计亮点 / Design highlight
- Collapsible **accordion** deep-dives where useful
- End-of-lesson **quiz** (bilingual)

**Footer**: version anchor — "对照 AgentScope 2.0，核验于 2026-06".

---

## 7. Build, PDF & deployment / 构建与部署

**Local build** (Python 3 only):
```bash
cd src
python build.py                 # → index.html + lessons/
python build_print.py --lang zh # → print.zh.html
python build_print.py --lang en # → print.en.html
```

**Bilingual PDF**: `build_print.py --lang zh|en` forces one language (strips the
other; a static PDF has no toggle), producing two PDFs:
`agentscope-visual-guide-zh.pdf` and `agentscope-visual-guide-en.pdf`, rendered with
headless Chromium.

**`.github/workflows/deploy.yml`** (push to `main`):
1. Rebuild site + both `print.*.html`.
2. Headless Chrome → two PDFs (CI installs CJK + emoji fonts).
3. Deploy `index.html`, `lessons/`, both PDFs to **GitHub Pages**.
4. On `v*` tag → publish a Release with both PDFs attached.

> ⚠️ **One-time manual step**: repo owner must set **Settings → Pages → Source:
> GitHub Actions** once. The Actions token cannot create the Pages site itself,
> only deploy to an already-enabled site. Documented in README.

**`.github/workflows/ci.yml`** (every push/PR):
- **Drift check** — re-run `build.py`, fail if committed HTML differs from `src/`.
- **Link check** — `check_links.py` (no internal dead links).
- **HTML structure check** — `check_html.py` (balanced `lang` pairs, valid bilingual structure).

---

## 8. Content accuracy / 内容准确性

- Every "源码对应 / Source mapping" references **real AgentScope symbols** verified
  against the repo (`src/agentscope/...`).
- Cite by **file + symbol name**, never hard-coded line numbers.
- Code examples use the real public API (`Agent`, `Toolkit`, `DashScopeChatModel`,
  `EventType`, `reply_stream`, etc.).
- Footer version anchor on every page.

---

## 9. Repo meta & layered docs / 仓库元信息与分层文档

- `README.md` — bilingual intro, badges, project structure, build/regenerate
  instructions, one-time Pages enablement note, attribution (independent
  third-party learning material; AgentScope is Apache-2.0 upstream).
- `LICENSE` — MIT (the guide itself).
- `.gitignore` — Python artifacts; locally-generated PDFs.

**Layered developer docs (L1–L4) for the generator**, under `docs/`, filled in
alongside code and committed with it:
- **L1 — overview**: what the generator is, end-to-end build flow.
- **L2 — components**: responsibilities & interfaces of `shell.py`, `i18n.py`,
  `registry.py`, `build*.py`, `check_*.py`, content modules.
- **L3 — details**: bilingual mechanism, DSL block semantics, CSS design system,
  CI pipeline details.
- **L4 — per-file API**: function/class reference per source file.

---

## 10. Open questions / 待定

None — all design decisions resolved during brainstorming.
