# AgentScope 图解教程 · Visual Guide

![Lessons](https://img.shields.io/badge/lessons-29-6d5ae6.svg)
![Parts](https://img.shields.io/badge/parts-8-9cf.svg)
![Built with](https://img.shields.io/badge/built%20with-Python%203-3776AB.svg?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)
![Docs](https://img.shields.io/badge/docs-中文%7CEnglish-orange.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

> 🌐 **在线阅读 / Read online**：<https://verdenmax.github.io/agentscope-visual-guide/>
> 　·　📄 **PDF**：[中文](https://github.com/verdenmax/agentscope-visual-guide/releases/latest/download/agentscope-visual-guide-zh.pdf)
> ｜ [English](https://github.com/verdenmax/agentscope-visual-guide/releases/latest/download/agentscope-visual-guide-en.pdf)

一套面向**完全新手**的可视化（HTML 图解）**中英双语**教程，带你从零理解
[AgentScope 2.0](https://github.com/agentscope-ai/agentscope) ——
既有**宏观全景**，也有**内部源码**，每一课都对照真实源码（文件 + 符号）核实。

A bilingual (中文 / English) visual guide that takes a complete beginner from zero to
understanding the [AgentScope 2.0](https://github.com/agentscope-ai/agentscope)
framework — macro overview **and** internals, every lesson cross-checked against the
real source (file + symbol).

> 📌 **版本锚点 / Version anchor**：对照 AgentScope 2.0 源码，核验于 **2026-06**。源码引用以
>「文件 + 符号名」为主（行号会随上游更新失效，故不写死）。

---

## 👤 适用人群 / Audience

- 完全没接触过 AgentScope、想从零入门的新手 / Newcomers starting from zero.
- 想先建立宏观认知、再深入内部源码的学习者 / Learners who want the big picture, then internals.
- 准备阅读 / 调试 / 贡献 AgentScope 源码的开发者 / Developers heading into the source.

## 🌏 双语 / Bilingual

每一课都是**单个 HTML 文件**，内置 **中 / EN 切换按钮**：点一下即时切换语言，选择会被记住
（保存在 `localStorage`）。无需联网、无需服务器，`file://` 直接打开即可。

Every lesson is a **single HTML file** with an in-page **中 / EN toggle**: one click flips
the language instantly and the choice is remembered (`localStorage`). No network, no server —
open via `file://` directly.

## 🚀 如何阅读 / How to read

直接用浏览器打开 **`index.html`** 即可。也可用任意静态服务器预览：

Just open **`index.html`** in a browser, or preview with any static server:

```bash
python -m http.server 8000   # then visit http://localhost:8000/
```

## 📚 教程结构 / Structure（8 部分 · 29 课 / 8 parts · 29 lessons）

| # | 部分 / Part | 课程 / Lessons |
|---|-------------|----------------|
| 1 | 宏观全景 / Macro | 01 是什么 · 02 架构全景 · 03 一次 reply 的生命周期 |
| 2 | 用户视角 / User's view | 04 消息 · 05 聊天模型 · 06 凭证 · 07 工具 · 08 Agent 入门 |
| 3 | 事件与流式 / Events & streaming | 09 事件系统 · 10 流式消费 · 11 Formatter |
| 4 | 内部源码 / Internals | 12 Agent 内部 · 13 Toolkit 内部 · 14 模型调用内部 · 15 中间件 |
| 5 | 进阶能力 / Advanced | 16 权限 · 17 工作区 · 18 MCP · 19 状态与任务 · 20 技能 · 21 嵌入 · 22 TTS |
| 6 | 服务化 / Productionization | 23 Agent Service · 24 消息总线 · 25 Agent Team |
| 7 | 自己动手 / Build your own | 26 自定义工具 · 27 自定义中间件 · 28 端到端实战 |
| 8 | 速查 / Reference | 29 术语表 |

## 🎨 每页包含 / Each page contains

🌍 大局观 · 🔬 源码对应（文件 + 符号）· 🧩 生活类比 · 🧪 真实代码示例 · ✅ 关键要点 ·
💡 设计亮点 · 🧠 小测验 · 顶部进度条 + 上一课/下一课 + 中/EN 切换。

🌍 Big picture · 🔬 source mapping (file + symbol) · 🧩 analogy · 🧪 real code · ✅ key takeaways ·
💡 design highlight · 🧠 quiz · progress bar + prev/next + 中/EN toggle.

## 🛠️ 重新生成 / Regenerate

无第三方依赖，仅需 Python 3.11+ / Zero third-party dependencies, Python 3.11+ only:

```bash
cd src
python build.py                  # → index.html + lessons/
python build_print.py --lang zh  # → print.zh.html (for the zh PDF)
python build_print.py --lang en  # → print.en.html (for the en PDF)
```

测试与校验 / Tests & checks:

```bash
python -m unittest discover -s tests -v   # unit tests
cd src && python check_links.py            # no dead internal links
cd src && python check_html.py             # balanced bilingual structure
```

### 本地导出 PDF / Export PDF locally

```bash
chromium --headless=new --no-pdf-header-footer \
  --print-to-pdf=agentscope-visual-guide-zh.pdf \
  --virtual-time-budget=20000 "file://$PWD/print.zh.html"
```

## 🚀 自动化 / CI（GitHub Pages + PDF）

`.github/workflows/deploy.yml` 在推送到 `main` 时**自动**重建站点、用无头 Chrome 渲染中/英两份
PDF，并部署到 GitHub Pages；打 `v*` 标签时发布带 PDF 的 Release。`.github/workflows/ci.yml`
在每次 push / PR 时做**防回归**：重建并校验提交的 HTML 无漂移、内部链接无死链、双语结构平衡。

> ⚠️ **首次启用（一次性）/ One-time setup**：仓库 owner 需在 **Settings → Pages → Source**
> 选择 **GitHub Actions**。Actions 的 token 无法创建 Pages 站点，只能向已启用的站点部署。

## 📄 许可 / License

本教程以 [MIT License](./LICENSE) 开源。AgentScope 是
[agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) 的项目（上游 Apache-2.0），
相关名称与商标归其作者所有。本教程为**独立的第三方学习材料**，与官方无隶属关系。

This guide is released under the [MIT License](./LICENSE). AgentScope is a project of
[agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) (Apache-2.0 upstream);
names and trademarks belong to their authors. This is **independent third-party learning
material**, not affiliated with the official project.
