"""Content for Part 4 (internals): lessons 12–15.

Verified against AgentScope 2.0 source (agent/_agent.py, tool/_toolkit.py,
model/_base.py, model/_model_response.py, middleware/_base.py and impls).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 12 — Agent internals
# ---------------------------------------------------------------------------
LESSON_12 = blocks(
    lead(
        "打开 <code>Agent</code> 的引擎盖：<code>reply</code> / <code>reply_stream</code> 内部是一个"
        "<strong>「推理-行动」循环</strong>，每一步都穿过一条<strong>中间件链</strong>，并在调用工具"
        "前经过<strong>权限引擎</strong>把关。",
        "Lift the <code>Agent</code>'s hood: inside <code>reply</code> / "
        "<code>reply_stream</code> is a <strong>reasoning-acting loop</strong> where each step "
        "passes through a <strong>middleware chain</strong> and tool calls are gated by a "
        "<strong>permission engine</strong>.",
    ),
    analogy(
        "像一条<strong>装配流水线</strong>：原料（消息）进来，经过若干工位（中间件钩子）层层加工，"
        "需要动用机器（工具）时先刷卡（权限），成品（回复）下线。",
        "Like an <strong>assembly line</strong>: material (messages) enters, passes through "
        "stations (middleware hooks), badges in before using a machine (permission for tools), "
        "and the finished product (reply) rolls off.",
    ),
    h2("循环的骨架", "The loop's skeleton"),
    accordion(
        "① reasoning（推理）",
        "① reasoning",
        blocks(p(
            "Agent 调用模型，得到下一步意图：要么继续输出文本（最终答案的雏形），"
            "要么产出一个或多个<strong>工具调用</strong>。",
            "The agent calls the model to get the next intent: either keep producing text (the "
            "beginnings of a final answer) or emit one or more <strong>tool calls</strong>.",
        )),
        num=1,
    ),
    accordion(
        "② acting（行动）",
        "② acting",
        blocks(p(
            "若有工具调用，Agent 通过 <code>Toolkit</code> 执行它们；执行前 "
            "<code>PermissionEngine</code> 判定是否放行（可能触发 "
            "<code>REQUIRE_USER_CONFIRM</code> 事件等待人类批准）。",
            "If there are tool calls, the agent runs them via the <code>Toolkit</code>; before "
            "execution the <code>PermissionEngine</code> decides whether to allow them (possibly "
            "raising a <code>REQUIRE_USER_CONFIRM</code> event to wait for a human).",
        )),
        num=2,
    ),
    accordion(
        "③ 循环 / 收尾",
        "③ loop / finish",
        blocks(p(
            "工具结果被「观察」回上下文，循环回到推理；如此往复直到模型给出最终答案"
            "（或触发 <code>EXCEED_MAX_ITERS</code>）。必要时 <code>compress_context</code> 压缩历史，"
            "<code>offloader</code> 卸载超长内容。",
            "Tool results are \"observed\" back into context and the loop returns to reasoning, "
            "repeating until the model produces a final answer (or hits "
            "<code>EXCEED_MAX_ITERS</code>). When needed, <code>compress_context</code> shrinks "
            "history and the <code>offloader</code> offloads oversized content.",
        )),
        num=3,
    ),
    h2("中间件链", "The middleware chain"),
    p(
        "每个阶段（reply / reasoning / acting / model call / system prompt）都被实现成一条"
        "可嵌套的<strong>处理链</strong>：每个中间件可以在调用 <code>next_handler</code> 前后插入"
        "逻辑——这就是「不改源码也能扩展行为」的机制（第 15 课展开）。",
        "Each stage (reply / reasoning / acting / model call / system prompt) is implemented as "
        "a nestable <strong>handler chain</strong>: a middleware can run logic before/after "
        "calling <code>next_handler</code> — the mechanism behind \"extend behavior without "
        "editing source\" (expanded in lesson 15).",
    ),
    source_map([
        ("agent/_agent.py",
         "推理-行动循环、中间件链（<code>execute_chain</code> / <code>next_handler</code>）、"
         "<code>PermissionEngine</code> 接入、<code>compress_context</code> / <code>offloader</code>",
         "the reasoning-acting loop, middleware chain (<code>execute_chain</code> / "
         "<code>next_handler</code>), <code>PermissionEngine</code> wiring, "
         "<code>compress_context</code> / <code>offloader</code>"),
    ]),
    keypoints([
        ("回复是一个推理→行动的<strong>循环</strong>，不是一次性调用。",
         "A reply is a reasoning→acting <strong>loop</strong>, not a one-shot call."),
        ("每个阶段穿过<strong>中间件链</strong>，工具调用经<strong>权限引擎</strong>把关。",
         "Each stage runs through a <strong>middleware chain</strong>; tool calls are gated by "
         "the <strong>permission engine</strong>."),
        ("上下文压缩与卸载防止历史无限膨胀。",
         "Context compression and offloading keep history from growing without bound."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 13 — Toolkit internals
# ---------------------------------------------------------------------------
LESSON_13 = blocks(
    lead(
        "<code>Toolkit</code> 内部做三件事：把注册的工具<strong>转成 JSON schema</strong> 给模型、"
        "在模型选定后<strong>执行</strong>对应工具、并支持<strong>分组管理</strong>（动态启用/停用）。",
        "Internally, <code>Toolkit</code> does three things: turn registered tools into "
        "<strong>JSON schemas</strong> for the model, <strong>execute</strong> the chosen tool, "
        "and support <strong>group-wise management</strong> (dynamic enable/disable).",
    ),
    analogy(
        "像一个<strong>带标签系统的工具柜</strong>：能列出每件工具的说明卡（schema），按编号取用"
        "（call），还能按抽屉分组、临时锁住某些抽屉（tool group）。",
        "Like a <strong>labeled tool cabinet</strong>: it can list each tool's spec card "
        "(schema), fetch one by number (call), and group tools into drawers it can temporarily "
        "lock (tool group).",
    ),
    h2("从工具到 schema 再到调用", "From tool to schema to call"),
    code(
        "# 1) 取所有工具的 JSON schema（异步！交给模型）\n"
        "schemas = await toolkit.get_tool_schemas()\n\n"
        "# 2) 模型选定后，按名字执行（call_tool 是 async generator，需要 state）\n"
        "async for chunk in toolkit.call_tool(tool_call, state):\n"
        "    ...   # 流式 ToolChunk，最后是完整的 ToolResponse / streamed, then final ToolResponse",
        cap_zh="get_tool_schemas 是 async；call_tool 是 async generator（带 state）。",
        cap_en="get_tool_schemas is async; call_tool is an async generator (takes state).",
    ),
    important(
        "<code>get_tool_schemas</code> 是<strong>异步</strong>方法（取代了旧版的同步 "
        "<code>get_function_schemas</code>）；务必 <code>await</code>。",
        "<code>get_tool_schemas</code> is <strong>async</strong> (it replaced the older "
        "synchronous <code>get_function_schemas</code>); be sure to <code>await</code> it.",
    ),
    h2("分组与适配器", "Groups and adapters"),
    p(
        "<code>ToolGroup</code> 让你把工具分组、并在运行时<strong>启用/停用</strong>整组——例如先只"
        "开放「只读」工具，确认后再开放「写」工具。<code>FunctionTool</code> 适配普通函数，"
        "<code>MCPTool</code> 适配来自 MCP 服务器的工具（第 18 课）。",
        "<code>ToolGroup</code> lets you group tools and <strong>enable/disable</strong> a whole "
        "group at runtime — e.g. expose only \"read-only\" tools first, then \"write\" tools "
        "after confirmation. <code>FunctionTool</code> adapts plain functions and "
        "<code>MCPTool</code> adapts tools from an MCP server (lesson 18).",
    ),
    source_map([
        ("tool/_toolkit.py",
         "<code>get_tool_schemas</code>(async)、<code>call_tool</code>、工具/MCP/技能注册",
         "<code>get_tool_schemas</code> (async), <code>call_tool</code>, tool/MCP/skill registration"),
        ("tool/_tool_group.py", "<code>ToolGroup</code>（分组与启用/停用）",
         "<code>ToolGroup</code> (grouping + enable/disable)"),
        ("tool/_adapters.py", "<code>FunctionTool</code> / <code>MCPTool</code> 适配器",
         "<code>FunctionTool</code> / <code>MCPTool</code> adapters"),
    ]),
    keypoints([
        ("<code>get_tool_schemas</code> <strong>异步</strong>生成给模型的工具 schema。",
         "<code>get_tool_schemas</code> <strong>asynchronously</strong> builds the tool schemas "
         "for the model."),
        ("<code>call_tool</code> 执行模型选定的工具。",
         "<code>call_tool</code> executes the tool the model chose."),
        ("<code>ToolGroup</code> 支持运行时分组启用/停用。",
         "<code>ToolGroup</code> supports runtime group enable/disable."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 14 — Model-call internals
# ---------------------------------------------------------------------------
LESSON_14 = blocks(
    lead(
        "模型调用的内部契约：<code>ChatModelBase</code> 定义统一调用，返回一个 "
        "<code>ChatResponse</code>——里面是<strong>内容块</strong>（文本/思考/工具调用）加上 "
        "<code>ChatUsage</code> 用量统计。",
        "The model-call contract: <code>ChatModelBase</code> defines a unified call returning a "
        "<code>ChatResponse</code> — <strong>content blocks</strong> (text/thinking/tool calls) "
        "plus a <code>ChatUsage</code> usage record.",
    ),
    analogy(
        "像统一的<strong>快递单</strong>：不管哪家快递（厂商），回执的格式都一样——里面装了什么"
        "（内容块）、花了多少（用量）一目了然。",
        "Like a standard <strong>shipping receipt</strong>: whatever the carrier (vendor), the "
        "receipt format is the same — what's inside (content blocks) and what it cost (usage) "
        "are clear at a glance.",
    ),
    h2("响应的形状", "The shape of a response"),
    table(
        [("字段 / 类型", "Field / type"), ("含义", "Meaning")],
        [
            [("内容块（<code>ChatResponse</code>）", "content blocks (<code>ChatResponse</code>)"),
             ("文本 / 思考 / 工具调用块", "text / thinking / tool-call blocks")],
            [("<code>ChatUsage</code>", "<code>ChatUsage</code>"),
             ("输入 / 输出 token 等用量", "input / output token usage")],
            [("<code>StructuredResponse</code>", "<code>StructuredResponse</code>"),
             ("需要结构化（schema 化）输出时使用", "for structured (schema'd) output")],
            [("<code>ModelCard</code>", "<code>ModelCard</code>"),
             ("模型能力元信息", "model capability metadata")],
        ],
    ),
    p(
        "<code>Agent</code> 不直接处理各厂商的原始返回，而是依赖 <code>ChatModelBase</code> 把它们"
        "归一化成 <code>ChatResponse</code>——这正是「换厂商不改业务代码」的底层保证。"
        "（消息 → 厂商请求的反方向，由 Formatter 负责，见第 11 课。）",
        "The <code>Agent</code> never handles raw vendor payloads; it relies on "
        "<code>ChatModelBase</code> to normalize them into a <code>ChatResponse</code> — the "
        "underlying guarantee behind \"swap vendors without touching business code\". (The "
        "reverse direction, messages → vendor request, is the Formatter's job, lesson 11.)",
    ),
    source_map([
        ("model/_base.py", "<code>ChatModelBase</code> 调用契约",
         "the <code>ChatModelBase</code> call contract"),
        ("model/_model_response.py", "<code>ChatResponse</code> / <code>StructuredResponse</code>",
         "<code>ChatResponse</code> / <code>StructuredResponse</code>"),
        ("model/_model_usage.py", "<code>ChatUsage</code>",
         "<code>ChatUsage</code>"),
    ]),
    keypoints([
        ("调用返回归一化的 <code>ChatResponse</code>（内容块 + 用量）。",
         "A call returns a normalized <code>ChatResponse</code> (content blocks + usage)."),
        ("<code>StructuredResponse</code> 支持结构化输出。",
         "<code>StructuredResponse</code> supports structured output."),
        ("归一化是「厂商无关」的关键。",
         "Normalization is the key to vendor independence."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 15 — Middleware
# ---------------------------------------------------------------------------
LESSON_15 = blocks(
    lead(
        "<strong>中间件（Middleware）</strong>让你在<strong>不改 Agent 源码</strong>的前提下，"
        "在循环的关键阶段插入逻辑：追踪、日志、缓存、改写系统提示、增删工具……",
        "<strong>Middleware</strong> lets you insert logic at key stages of the loop "
        "<strong>without editing the Agent's source</strong>: tracing, logging, caching, "
        "rewriting the system prompt, adding/removing tools…",
    ),
    analogy(
        "像给函数加<strong>装饰器</strong>：原函数不变，你在它前后包一层，做记录、改参数或拦截。"
        "中间件就是 agent 循环各阶段的装饰器。",
        "Like adding a <strong>decorator</strong> to a function: the original is untouched, you "
        "wrap logic around it to log, tweak arguments, or intercept. Middleware is a decorator "
        "for each stage of the agent loop.",
    ),
    h2("钩子点", "Hook points"),
    table(
        [("钩子方法", "Hook method"), ("时机", "When")],
        [
            [("<code>on_reply</code>", "<code>on_reply</code>"),
             ("整次回复的最外层", "the outermost wrap of a whole reply")],
            [("<code>on_reasoning</code>", "<code>on_reasoning</code>"),
             ("每次推理（模型决策）前后", "around each reasoning step")],
            [("<code>on_acting</code>", "<code>on_acting</code>"),
             ("每次行动（执行工具）前后", "around each acting step (tool execution)")],
            [("<code>on_model_call</code>", "<code>on_model_call</code>"),
             ("每次调用模型前后", "around each model call")],
            [("<code>on_compress_context</code>", "<code>on_compress_context</code>"),
             ("上下文压缩时", "when context is compressed")],
            [("<code>on_system_prompt</code>", "<code>on_system_prompt</code>"),
             ("取系统提示时（可动态改写）", "when fetching the system prompt (can rewrite it)")],
            [("<code>list_tools</code>", "<code>list_tools</code>"),
             ("调整暴露给模型的工具集", "adjust the tool set exposed to the model")],
        ],
    ),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.middleware import TracingMiddleware\n\n"
        "agent = Agent(\n"
        '    name="Friday",\n'
        '    system_prompt="...",\n'
        "    model=...,\n"
        "    middlewares=[TracingMiddleware()],   # attach middleware here\n"
        ")",
        cap_zh="通过 middlewares=[...] 挂载中间件。",
        cap_en="Attach middleware via middlewares=[...].",
    ),
    p(
        "内置示例：<code>TracingMiddleware</code>（可观测性 / 追踪）与 <code>TTSMiddleware</code>"
        "（把文本回复接入语音合成，见第 22 课）。自定义中间件见第 27 课。",
        "Built-in examples: <code>TracingMiddleware</code> (observability / tracing) and "
        "<code>TTSMiddleware</code> (pipe text replies into speech synthesis, lesson 22). "
        "Writing your own: lesson 27.",
    ),
    source_map([
        ("middleware/_base.py",
         "<code>MiddlewareBase</code> 与钩子：<code>on_reply</code> / <code>on_reasoning</code> / "
         "<code>on_acting</code> / <code>on_model_call</code> / <code>on_system_prompt</code> 等",
         "<code>MiddlewareBase</code> and hooks: <code>on_reply</code> / <code>on_reasoning</code> "
         "/ <code>on_acting</code> / <code>on_model_call</code> / <code>on_system_prompt</code>, etc."),
        ("middleware/_tracing/_trace.py", "<code>TracingMiddleware</code>",
         "<code>TracingMiddleware</code>"),
        ("middleware/_tts_middleware.py", "<code>TTSMiddleware</code>",
         "<code>TTSMiddleware</code>"),
    ]),
    highlight(
        "中间件把「横切关注点」（日志/追踪/限流/改写）从 agent 主逻辑里剥离出来——"
        "主循环保持干净，扩展点保持可组合。",
        "Middleware peels \"cross-cutting concerns\" (logging/tracing/throttling/rewriting) out "
        "of the agent's main logic — the loop stays clean and the extension points stay composable.",
    ),
    keypoints([
        ("中间件在循环各阶段插入逻辑，<strong>不改 Agent 源码</strong>。",
         "Middleware inserts logic at loop stages <strong>without editing Agent source</strong>."),
        ("钩子：<code>on_reply/on_reasoning/on_acting/on_model_call/on_system_prompt</code> 等。",
         "Hooks: <code>on_reply/on_reasoning/on_acting/on_model_call/on_system_prompt</code>, etc."),
        ("通过 <code>Agent(middlewares=[...])</code> 挂载。",
         "Attach via <code>Agent(middlewares=[...])</code>."),
    ]),
)


LESSONS = {
    "12-agent-internals.html": LESSON_12,
    "13-toolkit-internals.html": LESSON_13,
    "14-model-internals.html": LESSON_14,
    "15-middleware.html": LESSON_15,
}


QUIZZES = {
    "12-agent-internals.html": [
        (
            "一次回复在内部是如何进行的？",
            "How does a reply proceed internally?",
            [
                ("推理→行动的循环，工具调用经权限引擎把关",
                 "A reasoning→acting loop with tool calls gated by the permission engine", True),
                ("一次模型调用就结束", "A single model call and done", False),
                ("先执行所有工具再推理一次", "Run all tools first, then reason once", False),
            ],
            "Agent 在推理-行动循环中迭代，每个工具调用先经 PermissionEngine 判定。",
            "The agent iterates a reasoning-acting loop; each tool call is first judged by the "
            "PermissionEngine.",
        ),
    ],
    "13-toolkit-internals.html": [
        (
            "关于 <code>get_tool_schemas</code>，下列哪项正确？",
            "Which is true about <code>get_tool_schemas</code>?",
            [
                ("它是 async 方法，返回工具的 JSON schema",
                 "It is async and returns the tools' JSON schemas", True),
                ("它是同步方法", "It is synchronous", False),
                ("它执行工具", "It executes tools", False),
            ],
            "get_tool_schemas 是异步方法（取代旧的 get_function_schemas），需 await。",
            "get_tool_schemas is async (replacing the old get_function_schemas) and must be awaited.",
        ),
    ],
    "14-model-internals.html": [
        (
            "模型调用返回什么归一化结构？",
            "What normalized structure does a model call return?",
            [
                ("<code>ChatResponse</code>（内容块 + <code>ChatUsage</code>）",
                 "<code>ChatResponse</code> (content blocks + <code>ChatUsage</code>)", True),
                ("一个纯字符串", "A plain string", False),
                ("厂商的原始 JSON", "The vendor's raw JSON", False),
            ],
            "ChatModelBase 把各厂商返回归一化成 ChatResponse，含内容块与用量。",
            "ChatModelBase normalizes vendor outputs into a ChatResponse with content blocks and usage.",
        ),
    ],
    "15-middleware.html": [
        (
            "中间件的主要价值是什么？",
            "What is middleware's main value?",
            [
                ("不改 Agent 源码即可在循环各阶段插入逻辑",
                 "Insert logic at loop stages without editing Agent source", True),
                ("替换大语言模型", "Replacing the LLM", False),
                ("加密网络流量", "Encrypting network traffic", False),
            ],
            "中间件通过 on_* 钩子在循环各阶段插入逻辑，无需改动 agent 主逻辑。",
            "Middleware uses on_* hooks to inject logic at loop stages without changing the "
            "agent's core logic.",
        ),
    ],
}
