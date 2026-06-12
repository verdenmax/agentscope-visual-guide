"""Content for Part 1 (macro overview): lessons 01–03.

This module is the exemplar for the authoring pattern used across all content
modules. Every code example and source-mapping entry is verified against the
AgentScope 2.0 source tree (``src/agentscope/...``).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t, steps,
)

# ---------------------------------------------------------------------------
# Lesson 00 — Setup & first run
# ---------------------------------------------------------------------------
LESSON_00 = blocks(
    lead(
        "真正的「从零开始」：本课带你<strong>装好 AgentScope、配好密钥、跑通第一个程序</strong>，"
        "然后再进入后面的概念。",
        "Truly \"from zero\": this lesson gets you to <strong>install AgentScope, set your key, "
        "and run your first program</strong> before any concepts.",
    ),
    analogy(
        "像组装家具前先<strong>清点零件、备好螺丝刀</strong>：环境配好，后面每一课的代码才能直接跑。",
        "Like <strong>laying out the parts and a screwdriver</strong> before assembling "
        "furniture: with the environment ready, every later lesson's code just runs.",
    ),
    h2("1 · 安装", "1 · Install"),
    important(
        "AgentScope 需要 <strong>Python 3.11 或更高</strong>版本。",
        "AgentScope requires <strong>Python 3.11 or higher</strong>.",
    ),
    code(
        "# 推荐用 uv（也可用 pip）/ recommended via uv (pip works too)\n"
        "uv pip install agentscope\n"
        "# 或 / or:  pip install agentscope\n\n"
        "# 需要服务化 / 全部可选依赖时 / for the service & all extras:\n"
        "# uv pip install \"agentscope[full]\"",
        lang="bash",
        cap_zh="安装核心包；服务化场景再装 [full]。",
        cap_en="Install the core package; add [full] for the service.",
    ),
    h2("2 · 配置密钥", "2 · Configure your key"),
    p(
        "模型需要 API key。<strong>从环境变量读取，不要写进代码</strong>（详见第 6 课）。"
        "以阿里云百炼 / 通义千问（DashScope）为例：",
        "Models need an API key. <strong>Read it from an environment variable, never hardcode "
        "it</strong> (see lesson 6). Using DashScope (Qwen) as the example:",
    ),
    code(
        "# 在你的 shell 里设置（key 从厂商控制台获取）\n"
        "# set it in your shell (get the key from the vendor console)\n"
        "export DASHSCOPE_API_KEY=\"sk-your-key-here\"",
        lang="bash",
        cap_zh="把密钥放进环境变量。",
        cap_en="Put the key in an environment variable.",
    ),
    h2("3 · 第一个程序", "3 · Your first program"),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.model import DashScopeChatModel\n"
        "from agentscope.credential import DashScopeCredential\n"
        "from agentscope.message import UserMsg\n"
        "import os, asyncio\n\n"
        "agent = Agent(\n"
        '    name="Friday",\n'
        '    system_prompt="You\'re a helpful assistant named Friday.",\n'
        "    model=DashScopeChatModel(\n"
        "        credential=DashScopeCredential(\n"
        '            api_key=os.environ["DASHSCOPE_API_KEY"]),\n'
        '        model="qwen3.6-plus",\n'
        "    ),\n"
        ")\n\n"
        "async def main():\n"
        '    reply = await agent.reply(UserMsg("Tony", "Hi, Friday!"))\n'
        "    print(reply)\n\n"
        "asyncio.run(main())",
        cap_zh="最小可运行程序：构造 Agent，await reply()，打印回复。",
        cap_en="The smallest runnable program: build an Agent, await reply(), print the reply.",
    ),
    note(
        "几个新手要点：代码是<strong>异步</strong>的，用 <code>asyncio.run(main())</code> 启动；"
        "<code>agent.reply(...)</code> 返回最终的 <code>AssistantMsg</code>（要流式输出见第 10 课）；"
        "这个 <code>Agent</code> 没有工具，后面第 7 课再加。",
        "A few beginner notes: the code is <strong>async</strong>, started with "
        "<code>asyncio.run(main())</code>; <code>agent.reply(...)</code> returns the final "
        "<code>AssistantMsg</code> (for streaming see lesson 10); this <code>Agent</code> has no "
        "tools yet — we add them in lesson 7.",
    ),
    source_map([
        ("pyproject.toml", "依赖与可选分组（<code>service</code> / <code>full</code> 等）",
         "dependencies and optional groups (<code>service</code> / <code>full</code>, …)"),
        ("agent/_agent.py", "<code>Agent</code> 与 <code>reply</code>",
         "<code>Agent</code> and <code>reply</code>"),
        ("README.md", "官方 Quickstart（安装与 Hello 示例）",
         "the official Quickstart (install + Hello example)"),
    ]),
    keypoints([
        ("先 <code>uv pip install agentscope</code>（Python 3.11+），再开始写代码。",
         "First <code>uv pip install agentscope</code> (Python 3.11+), then start coding."),
        ("API key 放环境变量；代码里 <code>os.environ[...]</code> 读取。",
         "Put the API key in an env var; read it via <code>os.environ[...]</code> in code."),
        ("AgentScope 是异步的——用 <code>asyncio.run(main())</code> 启动。",
         "AgentScope is async — start with <code>asyncio.run(main())</code>."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 01 — What is AgentScope
# ---------------------------------------------------------------------------
LESSON_01 = blocks(
    lead(
        "AgentScope 2.0 是一个<strong>生产级、易用</strong>的多智能体（multi-agent）框架。"
        "它不替你训练模型，而是把模型的<strong>推理与工具使用能力</strong>接进真实应用——"
        "并顺应越来越强的 agentic LLM，用<strong>事件驱动</strong>的方式编排「推理-行动」循环。",
        "AgentScope 2.0 is a <strong>production-ready, easy-to-use</strong> multi-agent "
        "framework. It doesn't train models for you; it wires a model's "
        "<strong>reasoning and tool-use</strong> abilities into real applications — "
        "leaning into increasingly agentic LLMs with an <strong>event-driven</strong> "
        "reasoning-acting loop.",
    ),
    analogy(
        "把大语言模型想象成一台<strong>很强但很孤立的发动机</strong>：它能输出文字，"
        "却看不到你的数据库、不会自己调用工具、也不知道何时该停下来。"
        "AgentScope 就是那套<strong>传动系统 + 仪表盘 + 配件接口</strong>，"
        "把这台发动机接到工具、权限、工作区，并把整个过程通过仪表盘（事件流）实时显示出来。",
        "Picture an LLM as a <strong>powerful but isolated engine</strong>: it emits "
        "text, but it can't see your database, can't call tools by itself, and doesn't "
        "know when to stop. AgentScope is the <strong>drivetrain + dashboard + "
        "connectors</strong> that bolt that engine to tools, permissions and a "
        "workspace — and surface the whole process live through a dashboard (the event "
        "stream).",
    ),
    h2("它解决什么问题", "What problems it solves"),
    p(
        "直接调用某个厂商的 SDK 当然能跑通一个 demo，但真实应用很快会遇到四类麻烦，"
        "这正是 AgentScope 替你抹平的：",
        "Calling a single vendor's SDK is fine for a demo, but real applications quickly "
        "hit four kinds of friction — exactly what AgentScope smooths over:",
    ),
    table(
        [("能力 / 痛点", "Capability / pain point"),
         ("AgentScope 的做法", "AgentScope's approach")],
        [
            [("厂商锁定", "Vendor lock-in"),
             ("<code>ChatModelBase</code> 统一接口 + 各厂商子类，换模型基本只改配置",
              "<code>ChatModelBase</code> unifies vendors; swapping models is mostly "
              "a config change")],
            [("结构化对话", "Structured dialogue"),
             ("<code>Msg</code> 家族 + 内容块（文本 / 思考 / 工具调用 / 结果）",
              "the <code>Msg</code> family + typed content blocks (text / thinking / "
              "tool-call / result)")],
            [("调用工具", "Calling tools"),
             ("<code>Toolkit</code> 自动从函数签名生成 schema 并解析调用",
              "<code>Toolkit</code> auto-generates a JSON schema from signatures and "
              "parses the calls")],
            [("可观测 / 可控", "Observability / control"),
             ("事件系统 + 权限系统 + 中间件，让循环透明且可干预",
              "an event system + permission system + middleware make the loop "
              "transparent and steerable")],
        ],
    ),
    h2("最小示例", "Minimal example"),
    p(
        "给模型配上工具，就得到一个能动手的 agent（安装与运行见"
        "<a href=\"00-setup.html\">第 0 课</a>，流式输出见<a href=\"10-streaming.html\">第 10 课</a>）：",
        "Give the model some tools and you get an agent that can act (install/run in "
        "<a href=\"00-setup.html\">lesson 0</a>; streaming in "
        "<a href=\"10-streaming.html\">lesson 10</a>):",
    ),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.model import DashScopeChatModel\n"
        "from agentscope.credential import DashScopeCredential\n"
        "from agentscope.tool import Toolkit, Bash, Read, Write\n"
        "from agentscope.message import UserMsg\n"
        "import os, asyncio\n\n"
        "agent = Agent(\n"
        '    name="Friday",\n'
        '    system_prompt="You\'re a helpful assistant named Friday.",\n'
        "    model=DashScopeChatModel(\n"
        "        credential=DashScopeCredential(\n"
        '            api_key=os.environ["DASHSCOPE_API_KEY"]),\n'
        '        model="qwen3.6-plus",\n'
        "    ),\n"
        "    toolkit=Toolkit(tools=[Bash(), Read(), Write()]),\n"
        ")\n\n"
        "async def main():\n"
        '    reply = await agent.reply(UserMsg("Tony", "List files here."))\n'
        "    print(reply)\n\n"
        "asyncio.run(main())",
        cap_zh="模型 + 工具 = 能动手的 agent。",
        cap_en="Model + tools = an agent that can act.",
    ),
    source_map([
        ("agent/_agent.py",
         "<code>Agent</code> 类与 <code>reply</code> / <code>reply_stream</code>",
         "the <code>Agent</code> class and <code>reply</code> / <code>reply_stream</code>"),
        ("model/_dashscope/_model.py",
         "<code>DashScopeChatModel</code> 等厂商模型实现",
         "vendor model implementations such as <code>DashScopeChatModel</code>"),
        ("tool/_toolkit.py",
         "<code>Toolkit</code> 工具注册与 schema 生成",
         "<code>Toolkit</code> tool registration and schema generation"),
        ("event/_event.py",
         "<code>EventType</code> 与全部事件类型",
         "<code>EventType</code> and all event variants"),
    ]),
    highlight(
        "设计哲学：<strong>不用死板的提示词和编排去约束模型</strong>，而是放大它本身的推理与工具"
        "使用能力。模型越强，框架越省力——这正是「为 agentic LLM 设计」的含义。",
        "Design philosophy: rather than constraining the model with rigid prompts and "
        "orchestration, <strong>amplify its own reasoning and tool use</strong>. The "
        "stronger the model, the less the framework fights it — that is what "
        "\"designed for agentic LLMs\" means.",
    ),
    keypoints([
        ("AgentScope 负责模型<strong>周边的管道</strong>，而不是训练模型本身。",
         "AgentScope handles the <strong>plumbing around</strong> the model, not "
         "training the model itself."),
        ("核心心智模型：<strong>Agent = 模型 + 工具 + 系统提示</strong>，运行「推理-行动」循环。",
         "Core mental model: <strong>Agent = model + tools + system prompt</strong>, "
         "running a reasoning-acting loop."),
        ("一切交互通过<strong>事件流</strong>暴露，天然支持 UI 与人类介入（human-in-the-loop）。",
         "All interaction is exposed via an <strong>event stream</strong>, naturally "
         "supporting UIs and human-in-the-loop."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 02 — Architecture panorama
# ---------------------------------------------------------------------------
LESSON_02 = blocks(
    lead(
        "AgentScope 由一组<strong>职责清晰、可独立理解</strong>的模块组成。"
        "先建立这张「全景地图」，后面每一课都能对号入座。",
        "AgentScope is built from a set of <strong>clearly-scoped, independently "
        "understandable</strong> modules. Build this panorama first and every later "
        "lesson will slot neatly into place.",
    ),
    analogy(
        "把它想成一间<strong>智能工坊</strong>：模型是「大脑」，工具是「手」，"
        "权限是「门禁」，工作区是「车间」，事件流是「监控大屏」，而服务层（app）是「前台与调度室」。",
        "Think of it as a <strong>smart workshop</strong>: the model is the brain, "
        "tools are the hands, permissions are the door access, the workspace is the "
        "shop floor, the event stream is the monitoring wall, and the service layer "
        "(app) is the front desk and dispatch room.",
    ),
    h2("模块地图", "The module map"),
    table(
        [("模块", "Module"), ("职责", "Responsibility")],
        [
            [("<code>agent</code>", "<code>agent</code>"),
             ("<code>Agent</code> 类与「推理-行动」循环的编排者",
              "the <code>Agent</code> class and orchestrator of the reasoning-acting loop")],
            [("<code>model</code>", "<code>model</code>"),
             ("聊天模型抽象 <code>ChatModelBase</code> + 各厂商实现",
              "the <code>ChatModelBase</code> abstraction + per-vendor implementations")],
            [("<code>formatter</code>", "<code>formatter</code>"),
             ("把 <code>Msg</code> 列表转成各厂商要求的请求格式",
              "turns a <code>Msg</code> list into each vendor's request format")],
            [("<code>credential</code>", "<code>credential</code>"),
             ("API key / 密钥的管理，与模型配置解耦",
              "manages API keys / secrets, decoupled from model config")],
            [("<code>message</code>", "<code>message</code>"),
             ("<code>Msg</code> 家族与内容块（文本 / 思考 / 工具调用 / 结果 / 数据）",
              "the <code>Msg</code> family and content blocks (text/thinking/tool-call/"
              "result/data)")],
            [("<code>event</code>", "<code>event</code>"),
             ("类型化的事件流（<code>EventType</code> 及各事件类）",
              "the typed event stream (<code>EventType</code> and event classes)")],
            [("<code>tool</code>", "<code>tool</code>"),
             ("<code>Toolkit</code>、<code>ToolBase</code>、内置工具与 MCP/函数适配器",
              "<code>Toolkit</code>, <code>ToolBase</code>, built-in tools and "
              "MCP/function adapters")],
            [("<code>middleware</code>", "<code>middleware</code>"),
             ("围绕循环的可组合钩子（追踪、TTS 等）",
              "composable hooks around the loop (tracing, TTS, …)")],
            [("<code>permission</code>", "<code>permission</code>"),
             ("对工具与资源的细粒度授权",
              "fine-grained authorization for tools and resources")],
            [("<code>workspace</code>", "<code>workspace</code>"),
             ("隔离执行后端（本地 / Docker / E2B）与 <code>Offloader</code>",
              "isolated execution backends (local/Docker/E2B) and the <code>Offloader</code>")],
            [("<code>mcp</code>", "<code>mcp</code>"),
             ("连接外部 MCP 服务器并暴露其工具",
              "connect external MCP servers and expose their tools")],
            [("<code>state</code>", "<code>state</code>"),
             ("<code>AgentState</code> 与 <code>Task</code> 的持久化",
              "persistence of <code>AgentState</code> and <code>Task</code>")],
            [("<code>skill</code>", "<code>skill</code>"),
             ("打包可复用的能力（<code>Skill</code> + 加载器）",
              "packaged reusable capabilities (<code>Skill</code> + loaders)")],
            [("<code>embedding</code>", "<code>embedding</code>"),
             ("嵌入模型与缓存，检索 / RAG 的基础",
              "embedding models and caching — the basis for retrieval/RAG")],
            [("<code>tts</code>", "<code>tts</code>"),
             ("文本转语音（含实时 TTS）",
              "text-to-speech (including realtime TTS)")],
            [("<code>app</code>", "<code>app</code>"),
             ("基于 FastAPI 的多租户 / 多会话服务与消息总线",
              "the FastAPI-based multi-tenant/multi-session service and message bus")],
        ],
    ),
    h2("它们如何协作", "How they fit together"),
    p(
        "一次调用里，<code>agent</code> 居中调度，按这个顺序串起其余模块：",
        "In a single call, the <code>agent</code> coordinates, threading the other modules in "
        "this order:",
    ),
    steps([
        ("推理 Reason", "推理 Reason",
         "用 <code>credential</code> 配好的 <code>model</code> 思考下一步。",
         "think with a <code>model</code> configured via <code>credential</code>."),
        ("格式化 Format", "格式化 Format",
         "把对话历史交给 <code>formatter</code> 转成厂商请求格式。",
         "hand the dialogue history to a <code>formatter</code> for the vendor's format."),
        ("行动 Act", "行动 Act",
         "需要时调用 <code>tool</code>——受 <code>permission</code> 把关，可在 "
         "<code>workspace</code> 中执行。",
         "call <code>tool</code>s when needed — gated by <code>permission</code>, run in a "
         "<code>workspace</code>."),
        ("播报 Broadcast", "播报 Broadcast",
         "整个过程由 <code>event</code> 流向外播报，并可被 <code>middleware</code> 拦截增强。",
         "broadcast the whole process over the <code>event</code> stream, interceptable by "
         "<code>middleware</code>."),
    ]),
    source_map([
        ("agent/__init__.py", "<code>Agent</code> 与配置类的入口",
         "entry for <code>Agent</code> and its config classes"),
        ("model/__init__.py", "模型抽象与厂商实现的入口",
         "entry for the model abstraction and vendor implementations"),
        ("tool/__init__.py", "<code>Toolkit</code> 与工具体系的入口",
         "entry for <code>Toolkit</code> and the tool system"),
        ("app/__init__.py", "<code>create_app</code> 服务入口",
         "the <code>create_app</code> service entry"),
    ]),
    keypoints([
        ("模块边界清晰：每个模块都能<strong>单独理解、单独替换</strong>。",
         "Boundaries are clear: each module can be <strong>understood and replaced "
         "independently</strong>."),
        ("<code>agent</code> 是中枢，其余模块围绕它提供能力。",
         "The <code>agent</code> is the hub; the other modules provide capabilities "
         "around it."),
        ("<code>app</code> 层把单个 agent 升级成可部署的<strong>多租户服务</strong>。",
         "The <code>app</code> layer turns a single agent into a deployable "
         "<strong>multi-tenant service</strong>."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 03 — Lifecycle of a reply
# ---------------------------------------------------------------------------
LESSON_03 = blocks(
    lead(
        "本课跟随一次 <code>reply_stream</code> 调用，看一条用户消息如何穿过整个框架，"
        "最终变成一连串<strong>事件</strong>和一条助手回复。",
        "This lesson follows one <code>reply_stream</code> call to see how a single user "
        "message travels through the whole framework and becomes a stream of "
        "<strong>events</strong> plus an assistant reply.",
    ),
    analogy(
        "像点一杯手冲咖啡：你下单（<code>UserMsg</code>），咖啡师先<strong>想</strong>用什么豆"
        "（推理），可能<strong>去取</strong>器具（调用工具），过程里不断<strong>报进度</strong>"
        "（事件），最后端上成品（<code>AssistantMsg</code>）。",
        "Like ordering a pour-over: you place an order (<code>UserMsg</code>), the barista "
        "first <strong>thinks</strong> about which beans (reasoning), may <strong>fetch</strong> "
        "equipment (tool calls), keeps <strong>announcing progress</strong> (events), and "
        "finally serves the cup (<code>AssistantMsg</code>).",
    ),
    h2("数据流：从消息到事件", "Data flow: from message to events"),
    steps([
        ("起步", "Start",
         "你构造一条 <code>UserMsg(name, content)</code>，用 <code>async for</code> 遍历 "
         "<code>agent.reply_stream(msg)</code>；回复开始。",
         "You build a <code>UserMsg(name, content)</code> and iterate "
         "<code>agent.reply_stream(msg)</code> with <code>async for</code>; the reply begins."),
        ("推理 Reason",
         "推理 Reason",
         "Agent 调用模型，流式产出<strong>文本 / 思考</strong>，或决定<strong>调用工具</strong>。",
         "The agent calls the model, streaming <strong>text / thinking</strong> or deciding to "
         "<strong>call tools</strong>."),
        ("行动 Act", "行动 Act",
         "若模型请求了工具，Agent 执行它们并把结果<strong>观察</strong>回上下文；"
         "受管控的工具会先<strong>暂停等待权限确认</strong>（第 16 课）。",
         "If the model requested tools, the agent runs them and <strong>observes</strong> the "
         "results back into context; gated tools first <strong>pause for permission</strong> "
         "(lesson 16)."),
        ("循环与收尾", "Loop & finish",
         "推理 → 行动循环往复，直到模型给出最终答案，回复结束。"
         "（事件的细节与命名见<a href=\"09-event-system.html\">第 9 课</a>。）",
         "Reason → act repeats until the model gives a final answer and the reply ends. "
         "(The events and their names are detailed in "
         "<a href=\"09-event-system.html\">lesson 9</a>.)"),
    ]),
    h2("消费事件流", "Consuming the stream"),
    code(
        "from agentscope.event import EventType\n\n"
        "async for evt in agent.reply_stream(UserMsg(\"Tony\", \"What's 2+2?\")):\n"
        "    match evt.type:\n"
        "        case EventType.REPLY_START:\n"
        "            ...        # 开始 / start\n"
        "        case EventType.TEXT_BLOCK_DELTA:\n"
        "            ...        # 增量文本 / streamed text\n"
        "        case EventType.TOOL_CALL_START:\n"
        "            ...        # 模型要调用工具 / model wants a tool\n"
        "        case EventType.REPLY_END:\n"
        "            ...        # 完成 / done",
        cap_zh="用 match 按事件类型分发处理。",
        cap_en="Dispatch by event type with match.",
    ),
    important(
        "<code>reply_stream</code> 是 <strong>async generator</strong>，必须用 "
        "<code>async for</code> 消费；如果只想要最终结果，用 <code>agent.reply(...)</code>。",
        "<code>reply_stream</code> is an <strong>async generator</strong> consumed with "
        "<code>async for</code>; if you only want the final result, use "
        "<code>agent.reply(...)</code>.",
    ),
    source_map([
        ("agent/_agent.py",
         "<code>reply_stream</code> / <code>reply</code> / <code>observe</code> 的实现",
         "the implementations of <code>reply_stream</code> / <code>reply</code> / "
         "<code>observe</code>"),
        ("event/_event.py",
         "<code>EventType</code> 及 <code>ReplyStart/End</code>、<code>ModelCall*</code>、"
         "<code>ToolCall*</code>、<code>ToolResult*</code> 等事件",
         "<code>EventType</code> and events like <code>ReplyStart/End</code>, "
         "<code>ModelCall*</code>, <code>ToolCall*</code>, <code>ToolResult*</code>"),
    ]),
    keypoints([
        ("一次回复 = <strong>推理 → 行动</strong>的循环，全程以事件播报。",
         "One reply = a <strong>reason → act</strong> loop, narrated throughout by events."),
        ("事件是<strong>成对</strong>出现的（START → DELTA* → END），便于 UI 渲染。",
         "Events come in <strong>pairs</strong> (START → DELTA* → END), which makes UI "
         "rendering straightforward."),
        ("权限确认通过 <code>REQUIRE_USER_CONFIRM</code> 事件融入同一条流。",
         "Permission confirmation is woven into the same stream via the "
         "<code>REQUIRE_USER_CONFIRM</code> event."),
    ]),
)


LESSONS = {
    "00-setup.html": LESSON_00,
    "01-what-is-agentscope.html": LESSON_01,
    "02-architecture.html": LESSON_02,
    "03-lifecycle.html": LESSON_03,
}


QUIZZES = {
    "00-setup.html": [
        (
            "运行 AgentScope 代码前，最先要做的两件事是？",
            "What are the first two things to do before running AgentScope code?",
            [
                ("安装包（Python 3.11+）并把 API key 设为环境变量",
                 "Install the package (Python 3.11+) and set the API key as an env var", True),
                ("先训练一个模型", "Train a model first", False),
                ("搭一个前端", "Build a frontend first", False),
            ],
            "先 uv pip install agentscope（Python 3.11+），再用环境变量配置 API key。",
            "First uv pip install agentscope (Python 3.11+), then set the API key via an env var.",
        ),
    ],
    "01-what-is-agentscope.html": [
        (
            "AgentScope 的核心定位是什么？",
            "What is AgentScope's core role?",
            [
                ("训练大语言模型", "Training large language models", False),
                ("为模型提供周边管道（工具/事件/权限等）的多智能体框架",
                 "A multi-agent framework providing the plumbing (tools/events/"
                 "permissions) around a model", True),
                ("一个向量数据库", "A vector database", False),
            ],
            "AgentScope 不训练模型，而是把模型接进真实应用，负责工具、事件、权限等周边能力。",
            "AgentScope does not train models; it wires a model into real apps, handling "
            "tools, events, permissions and other surrounding capabilities.",
        ),
    ],
    "02-architecture.html": [
        (
            "哪个模块负责把 <code>Msg</code> 列表转换成各厂商要求的请求格式？",
            "Which module turns a <code>Msg</code> list into each vendor's request format?",
            [
                ("<code>formatter</code>", "<code>formatter</code>", True),
                ("<code>permission</code>", "<code>permission</code>", False),
                ("<code>workspace</code>", "<code>workspace</code>", False),
            ],
            "formatter 模块负责把统一的消息对象适配成不同厂商的具体请求格式。",
            "The formatter module adapts the unified message objects into each vendor's "
            "concrete request format.",
        ),
    ],
    "03-lifecycle.html": [
        (
            "<code>reply_stream</code> 返回的是什么，应如何消费？",
            "What does <code>reply_stream</code> return and how is it consumed?",
            [
                ("一个普通字符串，直接打印",
                 "A plain string you print directly", False),
                ("一个 async generator，用 <code>async for</code> 遍历事件",
                 "An async generator iterated with <code>async for</code> over events",
                 True),
                ("一个文件路径", "A file path", False),
            ],
            "reply_stream 是异步生成器，逐个产出事件；只要最终结果时用 reply()。",
            "reply_stream is an async generator that yields events one by one; use "
            "reply() when you only need the final result.",
        ),
    ],
}
