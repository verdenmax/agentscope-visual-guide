"""Shared HTML shell: CSS design system, navigation, and bilingual scaffolding."""

import base64

from i18n import t, esc

ACCENT = "#6d5ae6"

_FAVICON_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
    "<rect width='32' height='32' rx='7' fill='#6d5ae6'/>"
    "<text x='16' y='22' font-family='system-ui,sans-serif' font-size='15'"
    " font-weight='700' fill='#fff' text-anchor='middle'>AS</text></svg>"
)
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(
    _FAVICON_SVG.encode()
).decode()

INDEX_FILE = "index.html"


def head_meta(zh_title: str, en_title: str, zh_desc: str, en_desc: str) -> str:
    """SEO/social meta tags + favicon (zh primary, en in og:title alt)."""
    title = esc(f"{zh_title} · {en_title}")
    desc = esc(zh_desc)
    return (
        f'<meta name="description" content="{desc}">\n'
        f'<meta name="theme-color" content="{ACCENT}">\n'
        f'<link rel="icon" type="image/svg+xml" href="{FAVICON}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="AgentScope 图解教程">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta name="twitter:card" content="summary">'
    )


CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:#f7f7fb; --panel:#fff; --panel-2:#f1f1f8; --ink:#1d2129;
  --muted:#5b6470; --faint:#8a939f; --line:#e4e4ee;
  --accent:#6d5ae6; --accent-soft:#ece8fc; --accent-ink:#4b3bc0;
  --blue:#2563eb; --blue-soft:#e7efff; --amber:#b4690e; --amber-soft:#fdf1dd;
  --purple:#7c3aed; --purple-soft:#f0e9ff; --red:#d23f3f; --red-soft:#fbe6e6;
  --code-bg:#0f172a; --code-ink:#e2e8f0; --code-line:#1e293b;
  --shadow:0 1px 2px rgba(16,24,40,.06),0 8px 24px rgba(16,24,40,.06);
  --radius:14px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#0e1016; --panel:#161a22; --panel-2:#1d212c; --ink:#e6edf3;
    --muted:#9aa6b2; --faint:#6e7a86; --line:#2a2f3c;
    --accent:#9b8cf0; --accent-soft:#241d44; --accent-ink:#c9bdfb;
    --blue:#6ea8fe; --blue-soft:#16243f; --amber:#e0a44a; --amber-soft:#33270f;
    --purple:#b794f6; --purple-soft:#271a40; --red:#f08080; --red-soft:#3a1a1a;
    --code-bg:#0a0f1a; --code-ink:#d8e2f0; --code-line:#14202f;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px rgba(0,0,0,.35);
  }
}
html { scroll-behavior: smooth; overflow-x: hidden; }
body {
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",
    "PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  background:var(--bg); color:var(--ink); line-height:1.7;
  -webkit-font-smoothing:antialiased;
}
a { color:var(--accent); text-decoration:none; }
code,.mono { font-family:"SF Mono","JetBrains Mono","Fira Code",ui-monospace,
  Menlo,Consolas,monospace; overflow-wrap:break-word; }
p > code, li code, td code, .acc-body code {
  background:var(--panel-2); border:1px solid var(--line); border-radius:6px;
  padding:.06em .38em; font-size:.88em; color:var(--accent-ink); }

/* ---- bilingual visibility (the core mechanism) ---- */
html[data-lang="zh"] [lang="en"] { display: none; }
html[data-lang="en"] [lang="zh"] { display: none; }

/* ---- top bar + progress ---- */
.topbar { position: sticky; top: 0; z-index: 50; background: var(--panel);
  border-bottom: 1px solid var(--line); backdrop-filter: blur(8px); }
.topbar-inner { max-width: 960px; margin: 0 auto; padding: .7rem 1.25rem;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.topbar .home { font-size: .82rem; color: var(--muted); font-weight: 600;
  display: inline-flex; gap: .5rem; align-items: center; }
.topbar .home b { color: var(--accent); }
.topbar .pill { font-size: .72rem; color: var(--muted); background: var(--panel-2);
  padding: .2rem .6rem; border-radius: 999px; border: 1px solid var(--line);
  white-space: nowrap; }
.progress { height: 3px; background: var(--panel-2); }
.progress > span { display: block; height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--blue)); }

/* ---- language toggle button ---- */
.lang-toggle { font:600 .74rem/1 inherit; cursor:pointer; color:var(--accent-ink);
  background:var(--accent-soft); border:1px solid var(--line);
  padding:.32rem .7rem; border-radius:999px; min-width:3.2rem; }
.lang-toggle:hover { filter:brightness(.97); }

.wrap { max-width: 820px; margin: 0 auto; padding: 2.4rem 1.25rem 5rem; }

/* ---- hero ---- */
.hero { margin-bottom: 2rem; }
.hero .part { font-size: .76rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent); font-weight: 700; margin-bottom: .55rem; }
.hero h1 { font-size: 2.05rem; line-height: 1.2; letter-spacing: -.01em; font-weight: 750; }
.hero .lead { margin-top: .9rem; font-size: 1.06rem; color: var(--muted); }
.index-hero h1 { font-size: 2.3rem; }

h2 { font-size: 1.32rem; margin: 2.4rem 0 .9rem; letter-spacing: -.01em;
  display: flex; align-items: center; gap: .55rem; }
h2::before { content: ""; width: 4px; height: 1.05em; background: var(--accent);
  border-radius: 3px; display: inline-block; }
h3 { font-size: 1.05rem; margin: 1.4rem 0 .5rem; }
p { margin: .7rem 0; }
ul, ol { margin: .6rem 0 .6rem 1.3rem; }
li { margin: .3rem 0; }
strong { color: var(--ink); font-weight: 680; }

/* ---- callout cards ---- */
.card { border-radius: var(--radius); padding: 1.05rem 1.2rem; margin: 1.2rem 0;
  border: 1px solid var(--line); background: var(--panel); box-shadow: var(--shadow); }
.card .tag { font-size: .72rem; font-weight: 700; letter-spacing: .04em;
  display: inline-flex; align-items: center; gap: .4rem; margin-bottom: .5rem; }
.card.note { border-left: 4px solid var(--accent); background: var(--accent-soft); }
.card.note .tag { color: var(--accent-ink); }
.card.tip { border-left: 4px solid var(--blue); background: var(--blue-soft); }
.card.tip .tag { color: var(--blue); }
.card.important { border-left: 4px solid var(--red); background: var(--red-soft); }
.card.important .tag { color: var(--red); }
.card.analogy { border-left: 4px solid var(--amber); background: var(--amber-soft); }
.card.analogy .tag { color: var(--amber); }

/* ---- code ---- */
pre.code { background: var(--code-bg); color: var(--code-ink); padding: .9rem 1rem;
  border-radius: 12px; overflow-x: auto; font-size: .83rem; line-height: 1.6;
  margin: 1.1rem 0; box-shadow: var(--shadow); }
pre.code .cm { color: #7d8aa3; }
pre.code .kw { color: #c792ea; }
pre.code .st { color: #c3e88d; }
pre.code .nu { color: #f78c6c; }
.code-fig { margin: 1.1rem 0; }
.code-fig pre.code { margin: 0; }
.code-cap { font-size: .85rem; color: var(--muted); margin-top: .4rem; }

/* ---- accordion ---- */
.accordion { border: 1px solid var(--line); border-radius: 12px; background: var(--panel);
  margin: .7rem 0; box-shadow: var(--shadow); overflow: hidden; }
.accordion > summary { cursor: pointer; padding: .85rem 1.1rem; font-weight: 650;
  font-size: .96rem; list-style: none; display: flex; align-items: center;
  gap: .6rem; user-select: none; }
.accordion > summary::-webkit-details-marker { display: none; }
.accordion > summary::after { content: "▶"; font-size: .68rem; color: var(--accent);
  margin-left: auto; transition: transform .15s ease; }
.accordion[open] > summary::after { transform: rotate(90deg); }
.accordion > summary:hover { background: var(--panel-2); }
.accordion[open] > summary { border-bottom: 1px solid var(--line); }
.accordion .badge-num { background: var(--accent-soft); color: var(--accent-ink);
  width: 1.6rem; height: 1.6rem; border-radius: 7px; display: inline-flex;
  align-items: center; justify-content: center; font-size: .82rem; font-weight: 700;
  flex-shrink: 0; }
.accordion .hint { font-size: .72rem; color: var(--faint); font-weight: 400; }
.acc-body { padding: .9rem 1.1rem 1.1rem; }
.acc-body pre.code { font-size: .78rem; }

/* ---- keypoints + source map ---- */
.keypoints { background: var(--accent-soft); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 12px; padding: .9rem 1.1rem;
  margin: 1.3rem 0; }
.keypoints .kp-title { font-weight: 700; color: var(--accent-ink); margin-bottom: .3rem; }
.keypoints ul { margin: .3rem 0 0 1.2rem; }
.srcmap { margin: 1.2rem 0; }
.srcmap .kp-title { font-weight: 700; margin-bottom: .5rem; color: var(--accent-ink); }
.srcmap code { background: var(--panel-2); padding: .1rem .4rem; border-radius: 6px; }

/* ---- tables ---- */
table.t { width: 100%; border-collapse: collapse; margin: 1.1rem 0; font-size: .9rem;
  background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--shadow); }
table.t th, table.t td { padding: .6rem .8rem; text-align: left;
  border-bottom: 1px solid var(--line); vertical-align: top; }
table.t th { background: var(--panel-2); font-size: .8rem; letter-spacing: .02em; }
table.t tr:last-child td { border-bottom: none; }
@media (max-width: 640px) {
  table.t { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  table.t th, table.t td { padding: .5rem .6rem; }
}

/* ---- quiz ---- */
.quiz { margin-top: 2.4rem; border-top: 2px dashed var(--line); padding-top: 1.2rem; }
.quiz-q { background: var(--panel); border: 1px solid var(--line);
  border-left: 4px solid var(--blue); border-radius: 12px; padding: .9rem 1.1rem;
  margin: 1rem 0; box-shadow: var(--shadow); }
.quiz-prompt { font-weight: 650; }
.quiz-opts { list-style: upper-alpha; margin: .55rem 0 .6rem 1.5rem; }
.quiz-ans { margin-top: .5rem; }
.quiz-ans summary { cursor: pointer; color: var(--accent-ink); font-weight: 650;
  font-size: .88rem; }
.quiz-correct { font-weight: 700; color: var(--accent-ink); margin: .5rem 0 .3rem; }

/* ---- lesson nav ---- */
.lesson-nav { display: flex; justify-content: space-between; gap: 1rem;
  margin-top: 3rem; padding-top: 1.4rem; border-top: 1px solid var(--line); }
.nav-link { flex: 1; padding: .85rem 1.1rem; border-radius: 12px; border: 1px solid var(--line);
  background: var(--panel); box-shadow: var(--shadow); transition: .15s;
  display: block; }
.nav-link:hover { border-color: var(--accent); transform: translateY(-1px); }
.nav-link.next { text-align: right; }
.nav-dir { font-size: .72rem; color: var(--faint); text-transform: uppercase;
  letter-spacing: .05em; display: block; }
.nav-title { font-weight: 700; color: var(--ink); margin-top: .15rem; display: block; }

.foot { margin-top: 2.6rem; padding-top: 1.2rem; border-top: 1px solid var(--line);
  font-size: .8rem; color: var(--faint); }

/* ---- index page ---- */
.ix-part { margin-top: 1.6rem; }
.ix-part h2 { font-size: 1.1rem; }
.ix-list { list-style: none; margin: .7rem 0 0; display: grid; gap: .55rem; }
.ix-list a { display: flex; align-items: center; gap: .9rem; padding: .8rem 1.05rem;
  border-radius: 12px; background: var(--panel); border: 1px solid var(--line);
  box-shadow: var(--shadow); transition: .15s; }
.ix-list a:hover { border-color: var(--accent); transform: translateX(3px); }
.ix-num { width: 30px; height: 30px; border-radius: 8px; background: var(--accent-soft);
  color: var(--accent-ink); display: inline-flex; align-items: center;
  justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; }
.ix-title { font-weight: 650; color: var(--ink); }
"""

_HEAD_LANG_SCRIPT = (
    "<script>try{var l=localStorage.getItem('asvg-lang');"
    "if(l!=='en')l='zh';document.documentElement.setAttribute('data-lang',l);"
    "document.documentElement.setAttribute('lang',l);}catch(e){}</script>"
)

_TOGGLE_SCRIPT = (
    "<script>(function(){var K='asvg-lang',r=document.documentElement,"
    "b=document.getElementById('langtoggle');"
    "function lab(){if(b)b.textContent=r.getAttribute('data-lang')==='en'?'中文':'EN';}"
    "function set(l){r.setAttribute('data-lang',l);r.setAttribute('lang',l);"
    "try{localStorage.setItem(K,l)}catch(e){}lab();}lab();"
    "if(b)b.addEventListener('click',function(){"
    "set(r.getAttribute('data-lang')==='en'?'zh':'en');});})();</script>"
)


# (file, zh_title, en_title, zh_part, en_part) — order defines progress + nav
PAGES = [
    ("01-what-is-agentscope.html", "AgentScope 是什么", "What is AgentScope",
     "第一部分 · 宏观全景", "Part 1 · Macro"),
    ("02-architecture.html", "整体架构全景", "Architecture panorama",
     "第一部分 · 宏观全景", "Part 1 · Macro"),
    ("03-lifecycle.html", "一次 reply 的生命周期", "Lifecycle of a reply",
     "第一部分 · 宏观全景", "Part 1 · Macro"),
    ("04-messages.html", "消息系统", "Messages",
     "第二部分 · 用户视角", "Part 2 · User's View"),
    ("05-chat-models.html", "聊天模型", "Chat Models",
     "第二部分 · 用户视角", "Part 2 · User's View"),
    ("06-credentials.html", "凭证管理", "Credentials",
     "第二部分 · 用户视角", "Part 2 · User's View"),
    ("07-tools.html", "工具 Tools", "Tools",
     "第二部分 · 用户视角", "Part 2 · User's View"),
    ("08-agents-intro.html", "Agent 入门", "Agent Intro",
     "第二部分 · 用户视角", "Part 2 · User's View"),
    ("09-event-system.html", "事件系统", "Event System",
     "第三部分 · 事件与流式", "Part 3 · Events & Streaming"),
    ("10-streaming.html", "流式消费", "Streaming",
     "第三部分 · 事件与流式", "Part 3 · Events & Streaming"),
    ("11-formatter.html", "Formatter 多厂商适配", "Formatter",
     "第三部分 · 事件与流式", "Part 3 · Events & Streaming"),
    ("12-agent-internals.html", "Agent 内部", "Agent Internals",
     "第四部分 · 内部源码", "Part 4 · Internals"),
    ("13-toolkit-internals.html", "Toolkit 内部", "Toolkit Internals",
     "第四部分 · 内部源码", "Part 4 · Internals"),
    ("14-model-internals.html", "模型调用内部", "Model-call Internals",
     "第四部分 · 内部源码", "Part 4 · Internals"),
    ("15-middleware.html", "中间件系统", "Middleware",
     "第四部分 · 内部源码", "Part 4 · Internals"),
    ("16-permission.html", "权限系统", "Permission System",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("17-workspace.html", "工作区 & 沙箱", "Workspace & Sandbox",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("18-mcp.html", "MCP 集成", "MCP Integration",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("19-state-tasks.html", "状态与任务", "State & Tasks",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("20-skills.html", "技能系统", "Skills",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("21-embeddings.html", "嵌入与检索", "Embeddings",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("22-tts.html", "TTS 语音", "TTS",
     "第五部分 · 进阶能力", "Part 5 · Advanced"),
    ("23-agent-service.html", "Agent Service", "Agent Service",
     "第六部分 · 服务化", "Part 6 · Productionization"),
    ("24-message-bus.html", "消息总线", "Message Bus",
     "第六部分 · 服务化", "Part 6 · Productionization"),
    ("25-agent-team.html", "Agent Team", "Agent Team",
     "第六部分 · 服务化", "Part 6 · Productionization"),
    ("26-custom-tools.html", "写自己的工具", "Custom Tools",
     "第七部分 · 自己动手", "Part 7 · Build Your Own"),
    ("27-custom-middleware.html", "写自己的中间件", "Custom Middleware",
     "第七部分 · 自己动手", "Part 7 · Build Your Own"),
    ("28-capstone.html", "端到端实战", "Capstone",
     "第七部分 · 自己动手", "Part 7 · Build Your Own"),
    ("29-glossary.html", "术语表 · 概念索引", "Glossary",
     "第八部分 · 速查", "Part 8 · Reference"),
]


def _page_index(fname: str) -> int:
    for i, row in enumerate(PAGES):
        if row[0] == fname:
            return i
    raise KeyError(fname)


def page(fname: str, content: str, standalone: bool, home_href: str) -> str:
    """Render a full lesson page. ``standalone`` controls relative linking.

    Target Python 3.11+: every ``t(...)`` / ``head_meta(...)`` call is precomputed
    into a local variable; the f-strings interpolate only simple names.
    """
    i = _page_index(fname)
    _, zt, et, zp, ep = PAGES[i]
    progress = round((i + 1) / len(PAGES) * 100)

    prev_html = ""
    if i > 0:
        pf, pz, pe, _, _ = PAGES[i - 1]
        prev_dir, prev_title = t("← 上一课", "← Prev"), t(esc(pz), esc(pe))
        prev_html = (
            f'<a class="nav-link prev" rel="prev" href="{pf}">'
            f'<span class="nav-dir">{prev_dir}</span>'
            f'<span class="nav-title">{prev_title}</span></a>'
        )
    next_html = ""
    if i < len(PAGES) - 1:
        nf, nz, ne, _, _ = PAGES[i + 1]
        next_dir, next_title = t("下一课 →", "Next →"), t(esc(nz), esc(ne))
        next_html = (
            f'<a class="nav-link next" rel="next" href="{nf}">'
            f'<span class="nav-dir">{next_dir}</span>'
            f'<span class="nav-title">{next_title}</span></a>'
        )

    # head_meta escapes internally; escape the display copies for <title>/<h1>/pill.
    meta = head_meta(zt, et, zp, ep)
    ezt, eet, ezp, eep = esc(zt), esc(et), esc(zp), esc(ep)
    home_lbl = t("← 目录", "← Contents")
    part_lbl = t(ezp, eep)
    title_lbl = t(ezt, eet)
    foot = t(
        "对照 AgentScope 2.0 源码，核验于 2026-06。本教程为独立第三方学习材料。",
        "Aligned with AgentScope 2.0 source, verified 2026-06. "
        "Independent third-party learning material.",
    )
    return (
        "<!doctype html>\n"
        '<html lang="zh" data-lang="zh">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"{_HEAD_LANG_SCRIPT}\n"
        f"<title>{ezt} · {eet}</title>\n"
        f"{meta}\n<style>{CSS}</style>\n</head>\n<body>\n"
        '<div class="topbar"><div class="topbar-inner">\n'
        f'<a class="home" href="{home_href}">{home_lbl}</a>\n'
        f'<span class="pill">{part_lbl}</span>\n'
        '<button id="langtoggle" class="lang-toggle" type="button" '
        'aria-label="切换语言 / Switch language">EN</button>\n'
        '</div><div class="progress">'
        f'<span style="width:{progress}%"></span></div></div>\n'
        '<div class="wrap">\n<div class="hero">\n'
        f'<div class="part">{part_lbl}</div>\n<h1>{title_lbl}</h1>\n</div>\n'
        f"{content}\n"
        f'<nav class="lesson-nav">{prev_html}{next_html}</nav>\n'
        f'<footer class="foot">{foot}</footer>\n</div>\n'
        f"{_TOGGLE_SCRIPT}\n</body>\n</html>"
    )


def index_page(standalone: bool, lesson_prefix: str) -> str:
    """Render the table-of-contents index page."""
    groups, order = {}, []
    for f, zt, et, zp, ep in PAGES:
        key = (zp, ep)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append((f, zt, et))

    sections = ""
    n = 0
    for zp, ep in order:
        items = ""
        for f, zt, et in groups[(zp, ep)]:
            n += 1
            title = t(esc(zt), esc(et))
            items += (
                f'<li><a href="{lesson_prefix}{f}">'
                f'<span class="ix-num">{n:02d}</span>'
                f'<span class="ix-title">{title}</span></a></li>'
            )
        part_lbl = t(esc(zp), esc(ep))
        sections += (
            f'<section class="ix-part"><h2>{part_lbl}</h2>'
            f'<ol class="ix-list">{items}</ol></section>'
        )

    title = t("AgentScope 图解教程", "AgentScope Visual Guide")
    lead = t(
        "从零理解 AgentScope 2.0：宏观全景 + 内部源码，29 课，中英双语。",
        "Understand AgentScope 2.0 from zero: macro overview + internals, "
        "29 lessons, bilingual.",
    )
    hero = (
        '<div class="hero index-hero">'
        f'<h1>{title}</h1><p class="lead">{lead}</p></div>'
    )
    sitebar = t("图解教程", "Visual Guide")
    meta = head_meta(
        "AgentScope 图解教程", "AgentScope Visual Guide",
        "从零理解 AgentScope 2.0，中英双语图解教程。",
        "Bilingual visual guide to AgentScope 2.0.",
    )
    return (
        "<!doctype html>\n"
        '<html lang="zh" data-lang="zh">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"{_HEAD_LANG_SCRIPT}\n"
        "<title>AgentScope 图解教程 · Visual Guide</title>\n"
        f"{meta}\n<style>{CSS}</style>\n</head>\n<body>\n"
        '<div class="topbar"><div class="topbar-inner">\n'
        f'<span class="home"><b>AgentScope</b> {sitebar}</span>\n'
        '<button id="langtoggle" class="lang-toggle" type="button" '
        'aria-label="切换语言 / Switch language">EN</button>\n'
        "</div></div>\n"
        f'<div class="wrap">{hero}{sections}</div>\n'
        f"{_TOGGLE_SCRIPT}\n</body>\n</html>"
    )
