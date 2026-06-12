"""Content for Part 4 (internals): lessons 12–15.

Verified against AgentScope 2.0 source (agent/_agent.py, tool/_toolkit.py,
model/_base.py, model/_model_response.py, middleware/_base.py and impls).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t, steps, flow,
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
    flow(
        [("收到消息", "Message in"), ("reasoning 推理", "reasoning"),
         ("有工具调用？", "tool calls?"), ("acting 执行（经权限）", "acting (gated)"),
         ("结果回灌记忆", "results → memory"), ("无工具 → 收尾", "no tools → finish")],
        "循环条件很简单：模型这一轮<strong>提出工具调用</strong>就继续 acting，<strong>不提</strong>就结束并返回最终回复。",
        "The loop rule is simple: if this round <strong>proposes tool calls</strong> it goes to "
        "acting; if <strong>none</strong>, it stops and returns the final reply.",
    ),
    analogy(
        "像一条<strong>装配流水线</strong>：原料（消息）进来，经过若干工位（中间件钩子）层层加工，"
        "需要动用机器（工具）时先刷卡（权限），成品（回复）下线。",
        "Like an <strong>assembly line</strong>: material (messages) enters, passes through "
        "stations (middleware hooks), badges in before using a machine (permission for tools), "
        "and the finished product (reply) rolls off.",
    ),
    h2("循环的骨架", "The loop's skeleton"),
    steps([
        ("reasoning（推理）", "reasoning",
         "Agent 调用模型，得到下一步意图：要么继续输出文本（最终答案的雏形），"
         "要么产出一个或多个<strong>工具调用</strong>。",
         "The agent calls the model for the next intent: keep producing text (the beginnings of "
         "a final answer), or emit one or more <strong>tool calls</strong>."),
        ("acting（行动）", "acting",
         "若有工具调用，Agent 通过 <code>Toolkit</code> 执行它们；执行前 "
         "<code>PermissionEngine</code> 判定是否放行（可能触发 "
         "<code>REQUIRE_USER_CONFIRM</code> 等待人类批准）。",
         "If there are tool calls, the agent runs them via the <code>Toolkit</code>; first the "
         "<code>PermissionEngine</code> decides whether to allow them (possibly raising "
         "<code>REQUIRE_USER_CONFIRM</code> to wait for a human)."),
        ("循环 / 收尾", "loop / finish",
         "工具结果被「观察」回上下文，循环回到推理，直到模型给出最终答案。必要时 "
         "<code>compress_context</code> 压缩历史、<code>offloader</code> 卸载超长内容。",
         "Tool results are \"observed\" back into context and the loop returns to reasoning, "
         "until the model gives a final answer. When needed, <code>compress_context</code> "
         "shrinks history and the <code>offloader</code> offloads oversized content."),
    ]),
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
    h2("中间件链：洋葱模型", "The middleware chain: an onion"),
    accordion(
        "一次 reply 如何层层穿过中间件",
        "How one reply passes through the middleware layers",
        blocks(
            p(
                "Agent 把每个阶段都实现成一条<strong>可嵌套的处理链</strong>。以模型调用为例，每个中间件的 "
                "<code>on_model_call</code> 在调用 <code>next_handler</code> <strong>之前</strong>可以改写"
                "入参（如系统提示、工具集），<strong>之后</strong>可以观测 / 改写结果——一层包一层，"
                "正是「洋葱」。",
                "The Agent implements each stage as a <strong>nestable handler chain</strong>. For the "
                "model call, each middleware's <code>on_model_call</code> can rewrite the inputs "
                "(system prompt, tool set) <strong>before</strong> calling <code>next_handler</code>, "
                "and observe / rewrite the result <strong>after</strong> — layer wrapping layer, the "
                "\"onion\".",
            ),
            code(
                "async def on_model_call(self, agent, input_kwargs, next_handler):\n"
                "    # —— 进入更内层之前 / before going deeper ——\n"
                "    response = await next_handler(**input_kwargs)\n"
                "    # —— 结果向外返回之后 / after the result comes back ——\n"
                "    return response",
                cap_zh="每个钩子都是「前 → next_handler → 后」的洋葱结构。",
                cap_en="Every hook is a before → next_handler → after onion.",
            ),
        ),
        num=1,
    ),
    table(
        [("钩子", "Hook"), ("环绕的阶段", "Wraps")],
        [
            [("<code>on_reply</code>", "<code>on_reply</code>"),
             ("整次回复（最外层）", "the whole reply (outermost)")],
            [("<code>on_reasoning</code> / <code>on_acting</code>", "<code>on_reasoning</code> / <code>on_acting</code>"),
             ("每轮推理 / 行动", "each reasoning / acting round")],
            [("<code>on_model_call</code>", "<code>on_model_call</code>"),
             ("每次调用模型", "each model call")],
            [("<code>on_system_prompt</code> / <code>list_tools</code>", "<code>on_system_prompt</code> / <code>list_tools</code>"),
             ("取系统提示 / 暴露的工具集（可动态改写）", "fetching the system prompt / exposed tools (rewritable)")],
        ],
    ),
    note(
        "<strong>权限</strong>与<strong>上下文卸载</strong>就接在这条链路上：行动阶段执行工具前由 "
        "<code>PermissionEngine</code> 把关，上下文过长时 <code>compress_context</code> 压缩、"
        "<code>offloader</code> 卸载（第 16 / 17 课）。",
        "<strong>Permission</strong> and <strong>context offloading</strong> hook into this chain: "
        "before a tool runs in the acting stage the <code>PermissionEngine</code> gates it, and when "
        "context grows too long <code>compress_context</code> shrinks it and the "
        "<code>offloader</code> offloads it (lessons 16 / 17).",
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
        "# 2) 模型选定后，按名字执行（call_tool 是 async generator，需要 state；AgentState 见第 19 课）\n"
        "async for chunk in toolkit.call_tool(tool_call, state):\n"
        "    ...   # 流式 ToolChunk，最后是完整的 ToolResponse / streamed, then final ToolResponse",
        cap_zh="get_tool_schemas 是 async；call_tool 是 async generator（带 state）。",
        cap_en="get_tool_schemas is async; call_tool is an async generator (takes state).",
    ),
    important(
        "<code>get_tool_schemas</code> 是<strong>异步</strong>方法，务必 <code>await</code>。",
        "<code>get_tool_schemas</code> is <strong>async</strong> — be sure to <code>await</code> it.",
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
    h2("函数如何变成 schema · 分组激活", "Function → schema · group activation"),
    accordion(
        "签名 + docstring → JSON schema（前后对照）",
        "Signature + docstring → JSON schema (before / after)",
        blocks(
            p(
                "<code>Toolkit</code> 读取每个工具的<strong>类型注解</strong>推断参数类型、读取 "
                "<strong>docstring</strong> 提取名称与描述，自动产出模型能理解的 JSON schema：",
                "<code>Toolkit</code> reads each tool's <strong>type hints</strong> to infer "
                "parameter types and its <strong>docstring</strong> for the name and description, "
                "auto-producing a JSON schema the model understands:",
            ),
            code(
                "def get_weather(city: str) -> str:\n"
                '    """Look up the weather for a city.\n\n'
                "    Args:\n"
                "        city (str): the city name\n"
                '    """',
                cap_zh="你写的函数……",
                cap_en="The function you write…",
            ),
            code(
                '{"name": "get_weather",\n'
                ' "description": "Look up the weather for a city.",\n'
                ' "parameters": {"type": "object",\n'
                '   "properties": {"city": {"type": "string", "description": "the city name"}},\n'
                '   "required": ["city"]}}',
                lang="json",
                cap_zh="……Toolkit 自动生成的 schema（经 get_tool_schemas 交给模型）。",
                cap_en="…the schema Toolkit auto-builds (handed to the model via get_tool_schemas).",
            ),
        ),
        num=1,
    ),
    table(
        [("职责", "Responsibility"), ("方法 / 机制", "Method / mechanism")],
        [
            [("注册工具 / MCP / 技能", "register tools / MCP / skills"),
             ("<code>Toolkit(tools=, mcps=, skills_or_loaders=)</code>", "<code>Toolkit(tools=, mcps=, skills_or_loaders=)</code>")],
            [("生成 schema", "produce schemas"),
             ("<code>await get_tool_schemas()</code>", "<code>await get_tool_schemas()</code>")],
            [("执行工具", "execute a tool"),
             ("<code>call_tool(tool_call, state)</code>（async generator）", "<code>call_tool(tool_call, state)</code> (async generator)")],
            [("分组启用 / 停用", "enable / disable groups"),
             ("<code>ToolGroup</code> + 激活集", "<code>ToolGroup</code> + the active set")],
        ],
    ),
    p(
        "<strong>工具分组</strong>让你按需暴露能力：把工具归入 <code>ToolGroup</code>，运行时只激活"
        "需要的组——例如先只给「只读」组，确认后再激活「写」组，从而缩小模型一次能用的工具面。",
        "<strong>Tool groups</strong> let you expose capabilities on demand: put tools into a "
        "<code>ToolGroup</code> and activate only the groups you need at runtime — e.g. expose a "
        "\"read-only\" group first and activate a \"write\" group after confirmation, shrinking the "
        "tool surface the model sees at once.",
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
    h2("结构化输出", "Structured output"),
    p(
        "想让模型直接产出<strong>符合某个 schema 的结构化数据</strong>（而非自由文本）？用 "
        "<code>ChatModelBase.generate_structured_output(messages, structured_model=...)</code>，"
        "传入一个 Pydantic 模型，返回 <code>StructuredResponse</code>，其 <code>.content</code> 是"
        "符合该 schema 的 <code>dict</code>。",
        "Need the model to emit <strong>structured data matching a schema</strong> instead of "
        "free text? Use <code>ChatModelBase.generate_structured_output(messages, "
        "structured_model=...)</code> with a Pydantic model; it returns a "
        "<code>StructuredResponse</code> whose <code>.content</code> is a <code>dict</code> "
        "matching that schema.",
    ),
    code(
        "from pydantic import BaseModel\n\n"
        "class Person(BaseModel):\n"
        "    name: str\n"
        "    age: int\n\n"
        "resp = await model.generate_structured_output(\n"
        "    messages, structured_model=Person)\n"
        "data = resp.content        # a dict matching Person's schema",
        cap_zh="用 Pydantic 模型约束输出，从 StructuredResponse.content 取 dict。",
        cap_en="Constrain output with a Pydantic model; read the dict from StructuredResponse.content.",
    ),
    h2("读懂一个 ChatResponse", "Reading a ChatResponse"),
    code(
        "resp = await model(messages)          # 直接调用模型 / call the model directly\n"
        "for block in resp.content:            # 内容块序列 / a sequence of content blocks\n"
        "    if block.type == \"text\":\n"
        "        print(block.text)\n"
        "    elif block.type == \"tool_call\":  # ToolCallBlock：模型想调用工具\n"
        "        print(block.name, block.input)\n"
        "if resp.usage:                        # ChatUsage：token 用量\n"
        "    print(resp.usage.input_tokens, resp.usage.output_tokens, resp.usage.time)",
        cap_zh="ChatResponse = 内容块序列 + 可选的 ChatUsage。",
        cap_en="A ChatResponse = a sequence of content blocks + an optional ChatUsage.",
    ),
    table(
        [("类型", "Type"), ("装着什么", "Holds")],
        [
            [("<code>ChatResponse</code>", "<code>ChatResponse</code>"),
             ("<code>content</code>（文本/思考/工具调用块）+ <code>usage</code> + <code>is_last</code>",
              "<code>content</code> (text/thinking/tool-call blocks) + <code>usage</code> + <code>is_last</code>")],
            [("<code>StructuredResponse</code>", "<code>StructuredResponse</code>"),
             ("<code>content</code>：符合你给定 schema 的 <code>dict</code>",
              "<code>content</code>: a <code>dict</code> matching your schema")],
            [("<code>ChatUsage</code>", "<code>ChatUsage</code>"),
             ("<code>input_tokens</code> / <code>output_tokens</code> / <code>time</code> 等",
              "<code>input_tokens</code> / <code>output_tokens</code> / <code>time</code>, …")],
        ],
    ),
    accordion(
        "流式 vs 一次性：同一个响应形状",
        "Streaming vs one-shot: the same response shape",
        blocks(
            p(
                "一次性调用返回单个 <code>ChatResponse</code>（<code>is_last=True</code>）。流式时，模型"
                "会陆续产出多个 <code>ChatResponse</code> 片段，每个带累积到当下的 <code>content</code>，"
                "最后一个 <code>is_last=True</code>。<strong>形状始终一致</strong>，所以上层（Agent / 你的代码）"
                "无需为两种模式写两套解析逻辑。",
                "A one-shot call returns a single <code>ChatResponse</code> (<code>is_last=True</code>). "
                "When streaming, the model yields successive <code>ChatResponse</code> pieces, each "
                "with the <code>content</code> accumulated so far, the last one "
                "<code>is_last=True</code>. <strong>The shape is always the same</strong>, so callers "
                "(the Agent / your code) need not write two parsers.",
            ),
        ),
        num=1,
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
    flow(
        [("on_reply（整次）", "on_reply (whole)"), ("on_reasoning / on_acting（每步）", "per step"),
         ("on_model_call（每次模型调用）", "on_model_call"), ("真正执行", "real call")],
        "中间件像洋葱：外层包内层；同一请求自外向内进入、自内向外返回——多个中间件按注册顺序嵌套。",
        "Middleware nests like an onion: outer wraps inner; a request goes in outside-to-inside "
        "and returns inside-to-outside — multiple middlewares nest in registration order.",
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


QUIZZES: dict = {}

QUIZZES["12-agent-internals.html"] = [
    (
        "随着「推理-行动」多轮迭代，对话上下文会越来越长。Agent 内部靠什么避免上下文<strong>无限膨胀</strong>？",
        "As the reason-act loop iterates, the context keeps growing. Internally, what keeps it "
        "from <strong>growing without bound</strong>?",
        [
            ("<code>compress_context</code> 压缩历史 + <code>offloader</code> 把超长内容卸载到工作区、按需取回",
             "<code>compress_context</code> compresses history + the <code>offloader</code> offloads "
             "oversized content to the workspace and fetches it back on demand", True),
            ("每轮都丢弃之前所有历史，只保留最新一条消息",
             "Each round discards all prior history, keeping only the latest message", False),
            ("不做处理，靠模型自己忽略多余的上下文",
             "Nothing — it relies on the model to ignore the excess context itself", False),
        ],
        "长循环会撑大上下文。Agent 用 <code>compress_context</code> 压缩历史、用 <code>offloader</code> "
        "把超长上下文 / 工具结果卸载出去并按需取回——既不无限膨胀，也不会粗暴丢掉历史。",
        "A long loop bloats the context. The Agent uses <code>compress_context</code> to compress "
        "history and the <code>offloader</code> to offload oversized context / tool results and fetch "
        "them back — neither growing unbounded nor crudely throwing history away.",
    ),
]

QUIZZES["13-toolkit-internals.html"] = [
    (
        "一个工具明明已注册进 <code>Toolkit</code>，模型却「看不到」、用不了。最可能的原因是？",
        "A tool is registered in the <code>Toolkit</code>, yet the model can't \u201csee\u201d or use it. "
        "The most likely reason?",
        [
            ("它所在的 <code>ToolGroup</code> 当前未激活——分组的「启用/停用」把它挡在了模型可见列表之外",
             "Its <code>ToolGroup</code> is currently inactive — the group enable/disable mechanism "
             "keeps it out of the list the model sees", True),
            ("必须重启进程，注册的工具才会对模型生效",
             "You must restart the process before registered tools take effect", False),
            ("<code>get_tool_schemas</code> 默认隐藏所有工具，需手动逐个开启",
             "<code>get_tool_schemas</code> hides all tools by default; you enable them one by one", False),
        ],
        "Toolkit 支持按 <code>ToolGroup</code> 分组并在运行时启用/停用：未激活分组里的工具不会出现在 "
        "<code>get_tool_schemas</code> 给模型的清单里（强行调用会触发 <code>ToolGroupInactiveError</code>）。",
        "The Toolkit groups tools into <code>ToolGroup</code>s that can be enabled/disabled at runtime: "
        "tools in an inactive group don't appear in the list <code>get_tool_schemas</code> hands the "
        "model (calling one anyway raises <code>ToolGroupInactiveError</code>).",
    ),
]

QUIZZES["14-model-internals.html"] = [
    (
        "为什么换模型厂商（如 OpenAI → DashScope）通常不必改业务代码？",
        "Why can you usually swap model vendors (e.g. OpenAI \u2192 DashScope) without touching business code?",
        [
            ("<code>ChatModelBase</code> 把各厂商返回归一化成统一的 <code>ChatResponse</code>（内容块 + 用量），"
             "Agent 只面对这个统一结构",
             "<code>ChatModelBase</code> normalizes every vendor's output into a uniform "
             "<code>ChatResponse</code> (content blocks + usage) the Agent works against", True),
            ("Agent 直接解析每家厂商的原始 JSON，并为每家写了适配分支",
             "The Agent parses each vendor's raw JSON with a per-vendor branch", False),
            ("各家厂商的 API 返回格式本来就完全一样，无需任何转换",
             "All vendors' APIs already return the exact same format, so no conversion is needed", False),
        ],
        "归一化发生在 ChatModelBase 层：它把不同厂商的原始返回统一成 ChatResponse，Agent 从不直接碰原始 JSON。",
        "Normalization happens in ChatModelBase: it unifies vendors' raw outputs into a ChatResponse "
        "and the Agent never touches raw JSON.",
    ),
]

QUIZZES["15-middleware.html"] = [
    (
        "关于中间件（Middleware），下列哪项正确？",
        "Which statement about middleware is correct?",
        [
            ("它通过 <code>on_*</code> 钩子在循环各阶段插入逻辑，无需修改 Agent 源码",
             "It inserts logic at loop stages via <code>on_*</code> hooks, with no change to the "
             "Agent's source", True),
            ("它只能被动记录日志，不能改写系统提示或增删工具",
             "It can only passively log; it cannot rewrite the system prompt or add/remove tools", False),
            ("要使用它必须继承并改写 <code>Agent</code> 类",
             "To use it you must subclass and modify the <code>Agent</code> class", False),
        ],
        "中间件正是为「不改 Agent 源码」而生：通过 on_system_prompt、list_tools 等钩子既能观测也能改写，"
        "用 Agent(middlewares=[...]) 挂载。",
        "Middleware exists precisely to avoid editing Agent source: hooks like on_system_prompt and "
        "list_tools let it both observe and modify; attach via Agent(middlewares=[...]).",
    ),
]
