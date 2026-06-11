"""Content for Part 3 (events & streaming): lessons 09–11.

Verified against AgentScope 2.0 source (event/_event.py, agent/_agent.py,
formatter/_formatter_base.py and the per-vendor formatters).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 09 — Event system
# ---------------------------------------------------------------------------
LESSON_09 = blocks(
    lead(
        "AgentScope 把一次回复拆成一连串<strong>类型化事件</strong>，通过 "
        "<code>reply_stream</code> 实时吐出。<code>EventType</code> 枚举定义了所有事件种类，"
        "每种都有对应的事件类。",
        "AgentScope breaks one reply into a stream of <strong>typed events</strong> emitted "
        "live by <code>reply_stream</code>. The <code>EventType</code> enum defines every "
        "kind, and each has a matching event class.",
    ),
    analogy(
        "像一场体育赛事的<strong>实时解说</strong>：不是等比赛结束才告诉你比分，而是"
        "「开球了」「射门」「进球」逐条播报——你能边听边反应。",
        "Like the <strong>live commentary</strong> of a match: instead of waiting for the "
        "final score, you hear \"kick-off\", \"shot\", \"goal\" one by one — you can react "
        "as it unfolds.",
    ),
    h2("事件全谱", "The event spectrum"),
    p(
        "事件可按用途分组。同一个「块」（block）总是以 <code>START → DELTA* → END</code> 的"
        "三段式出现，方便前端增量渲染。",
        "Events group by purpose. A single \"block\" always appears as a "
        "<code>START → DELTA* → END</code> triple, which makes incremental UI rendering easy.",
    ),
    table(
        [("分组", "Group"), ("事件类型（<code>EventType</code>）", "Event types (<code>EventType</code>)")],
        [
            [("生命周期", "Lifecycle"),
             ("<code>REPLY_START</code> / <code>REPLY_END</code>",
              "<code>REPLY_START</code> / <code>REPLY_END</code>")],
            [("模型调用", "Model call"),
             ("<code>MODEL_CALL_START</code> / <code>MODEL_CALL_END</code>",
              "<code>MODEL_CALL_START</code> / <code>MODEL_CALL_END</code>")],
            [("文本块", "Text block"),
             ("<code>TEXT_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>",
              "<code>TEXT_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>")],
            [("思考块", "Thinking block"),
             ("<code>THINKING_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>",
              "<code>THINKING_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>")],
            [("数据块", "Data block"),
             ("<code>DATA_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>",
              "<code>DATA_BLOCK_START</code> / <code>_DELTA</code> / <code>_END</code>")],
            [("工具调用", "Tool call"),
             ("<code>TOOL_CALL_START</code> / <code>_DELTA</code> / <code>_END</code>",
              "<code>TOOL_CALL_START</code> / <code>_DELTA</code> / <code>_END</code>")],
            [("工具结果", "Tool result"),
             ("<code>TOOL_RESULT_START</code> / <code>_TEXT_DELTA</code> / "
              "<code>_DATA_DELTA</code> / <code>_END</code>",
              "<code>TOOL_RESULT_START</code> / <code>_TEXT_DELTA</code> / "
              "<code>_DATA_DELTA</code> / <code>_END</code>")],
            [("控制 / 人机交互", "Control / human-in-the-loop"),
             ("<code>REQUIRE_USER_CONFIRM</code>、<code>USER_CONFIRM_RESULT</code>、"
              "<code>REQUIRE_EXTERNAL_EXECUTION</code>、<code>EXTERNAL_EXECUTION_RESULT</code>、"
              "<code>EXCEED_MAX_ITERS</code>、<code>HINT_BLOCK</code>、<code>CUSTOM</code>",
              "<code>REQUIRE_USER_CONFIRM</code>, <code>USER_CONFIRM_RESULT</code>, "
              "<code>REQUIRE_EXTERNAL_EXECUTION</code>, <code>EXTERNAL_EXECUTION_RESULT</code>, "
              "<code>EXCEED_MAX_ITERS</code>, <code>HINT_BLOCK</code>, <code>CUSTOM</code>")],
        ],
    ),
    accordion(
        "每个事件都带什么？",
        "What does each event carry?",
        blocks(
            p(
                "事件类继承自 <code>EventBase</code>，带有 <code>type</code> 字段（<code>EventType</code> 之一）"
                "与该事件相关的负载，例如 <code>TextBlockDeltaEvent</code> 带增量文本、"
                "<code>ToolCallStartEvent</code> 带将要调用的工具信息。注意 "
                "<code>ReplyEndEvent</code> 只带 <code>session_id</code> / <code>reply_id</code>，"
                "<strong>不</strong>携带最终消息——最终 <code>AssistantMsg</code> 由 "
                "<code>agent.reply()</code> 返回或从流式块累积。",
                "Event classes inherit from <code>EventBase</code> with a <code>type</code> "
                "field (one of <code>EventType</code>) plus payload: e.g. "
                "<code>TextBlockDeltaEvent</code> carries the incremental text and "
                "<code>ToolCallStartEvent</code> the tool about to be called. Note that "
                "<code>ReplyEndEvent</code> carries only <code>session_id</code> / "
                "<code>reply_id</code> and does <strong>not</strong> include the final "
                "message — the final <code>AssistantMsg</code> comes from "
                "<code>agent.reply()</code> or by accumulating the streamed blocks.",
            ),
        ),
        num=1,
    ),
    source_map([
        ("event/_event.py",
         "<code>EventType</code> 枚举与所有事件类（<code>EventBase</code> 及各子类）",
         "the <code>EventType</code> enum and all event classes (<code>EventBase</code> "
         "and subclasses)"),
        ("event/__init__.py",
         "对外导出的事件名清单",
         "the exported list of event names"),
    ]),
    highlight(
        "把「输出」建模成<strong>类型化事件流</strong>，而不是一个大字符串——这让 UI、日志、"
        "权限确认、外部执行都能接进同一条通道，是 AgentScope「可观测、可干预」的基石。",
        "Modeling \"output\" as a <strong>typed event stream</strong> rather than one big "
        "string lets UIs, logging, permission prompts and external execution all plug into "
        "the same channel — the foundation of AgentScope's observability and control.",
    ),
    keypoints([
        ("<code>EventType</code> 是所有事件的统一枚举；每类事件有对应的数据类。",
         "<code>EventType</code> is the single enum of all events; each has a data class."),
        ("块类事件遵循 <code>START → DELTA* → END</code> 三段式。",
         "Block events follow the <code>START → DELTA* → END</code> triple."),
        ("控制类事件（确认 / 外部执行 / 超限）让人类与外部系统介入同一条流。",
         "Control events (confirm / external execution / limits) let humans and external "
         "systems join the same stream."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 10 — Streaming
# ---------------------------------------------------------------------------
LESSON_10 = blocks(
    lead(
        "<code>reply_stream</code> 是一个 <strong>async generator</strong>：你用 "
        "<code>async for</code> 遍历它，按 <code>evt.type</code> 分发处理。这一课给出消费事件流的"
        "实用模式。",
        "<code>reply_stream</code> is an <strong>async generator</strong>: you iterate it with "
        "<code>async for</code> and dispatch on <code>evt.type</code>. This lesson gives the "
        "practical pattern for consuming the stream.",
    ),
    analogy(
        "像看<strong>直播弹幕</strong>：消息一条条到，你按类型决定怎么显示——文字追加到气泡里，"
        "工具调用显示成一张卡片，确认请求弹出一个按钮。",
        "Like watching a <strong>live feed</strong>: messages arrive one by one and you decide "
        "how to show each by type — text appended to a bubble, a tool call rendered as a card, "
        "a confirm request popping a button.",
    ),
    h2("基本消费模式", "The basic consumption pattern"),
    code(
        "from agentscope.event import EventType\n"
        "from agentscope.message import UserMsg\n\n"
        "async def run(agent):\n"
        '    async for evt in agent.reply_stream(UserMsg("Tony", "What\'s 2+2?")):\n'
        "        match evt.type:\n"
        "            case EventType.REPLY_START:\n"
        "                ui.begin()\n"
        "            case EventType.TEXT_BLOCK_DELTA:\n"
        "                ui.append_text(evt)       # 增量文本 / streamed text\n"
        "            case EventType.TOOL_CALL_START:\n"
        "                ui.show_tool(evt)         # 模型要调用工具 / a tool call\n"
        "            case EventType.TOOL_RESULT_END:\n"
        "                ui.show_result(evt)\n"
        "            case EventType.REPLY_END:\n"
        "                ui.finish(evt)            # 回复完成（不含最终消息）/ reply complete",
        cap_zh="用 match-case 按事件类型分发。",
        cap_en="Dispatch by event type with match-case.",
    ),
    h2("流式 vs 一次性", "Streaming vs one-shot"),
    table(
        [("方法", "Method"), ("返回", "Returns"), ("何时用", "When")],
        [
            [("<code>agent.reply_stream(msg)</code>", "<code>agent.reply_stream(msg)</code>"),
             ("async generator（逐事件）", "async generator (per event)"),
             ("需要实时 UI / 人机交互", "live UI / human-in-the-loop")],
            [("<code>agent.reply(msg)</code>", "<code>agent.reply(msg)</code>"),
             ("最终的 <code>AssistantMsg</code>", "the final <code>AssistantMsg</code>"),
             ("只关心结果", "you only need the result")],
            [("<code>agent.observe(msgs)</code>", "<code>agent.observe(msgs)</code>"),
             ("无（写入记忆）", "nothing (records to memory)"),
             ("注入消息但不立即回复", "inject messages without replying")],
        ],
    ),
    accordion(
        "为什么块事件要成对？",
        "Why are block events paired?",
        blocks(
            p(
                "<code>START</code> 让 UI <strong>开一个新气泡 / 卡片</strong>，"
                "<code>DELTA</code> 不断<strong>往里追加</strong>，<code>END</code> 标记<strong>这一块结束</strong>。"
                "没有这种配对，前端就无法区分「同一句话的续写」和「新的一段」。",
                "<code>START</code> tells the UI to <strong>open a new bubble/card</strong>, "
                "<code>DELTA</code> keeps <strong>appending</strong>, and <code>END</code> marks "
                "<strong>that block done</strong>. Without the pairing a UI can't tell "
                "\"more of the same sentence\" from \"a new segment\".",
            ),
        ),
        num=1,
    ),
    important(
        "<code>reply_stream</code> 必须用 <code>async for</code> 在异步函数里消费；它不是普通"
        "可迭代对象，也不会「一次性返回全部」。",
        "<code>reply_stream</code> must be consumed with <code>async for</code> inside an async "
        "function; it is not a plain iterable and does not return everything at once.",
    ),
    source_map([
        ("agent/_agent.py",
         "<code>reply_stream</code>（async generator）、<code>reply</code>、<code>observe</code>",
         "<code>reply_stream</code> (async generator), <code>reply</code>, <code>observe</code>"),
        ("event/_event.py", "用于 <code>match</code> 的 <code>EventType</code> 成员",
         "the <code>EventType</code> members you <code>match</code> on"),
    ]),
    keypoints([
        ("<code>reply_stream</code> = async generator，用 <code>async for</code> + <code>match</code> 消费。",
         "<code>reply_stream</code> is an async generator; consume with <code>async for</code> "
         "+ <code>match</code>."),
        ("只要结果用 <code>reply</code>；要实时/可控用 <code>reply_stream</code>。",
         "Use <code>reply</code> for the result; <code>reply_stream</code> for live/controllable."),
        ("块事件成对出现，天然映射到 UI 的「开始-追加-结束」。",
         "Paired block events map naturally to a UI's open-append-close."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 11 — Formatter
# ---------------------------------------------------------------------------
LESSON_11 = blocks(
    lead(
        "不同厂商要求的请求格式各不相同。<strong>Formatter</strong> 负责把统一的 "
        "<code>Msg</code> 列表，翻译成某个厂商 API 期望的具体结构（一串 <code>dict</code>）。",
        "Every vendor wants a different request shape. A <strong>Formatter</strong> translates "
        "the unified <code>Msg</code> list into the concrete structure a given vendor's API "
        "expects (a list of <code>dict</code>s).",
    ),
    analogy(
        "像一位<strong>同声传译</strong>：你只管用「中文」（统一的 <code>Msg</code>）表达，"
        "传译会把它转成对方听得懂的「日语 / 法语」（各厂商格式）。",
        "Like a <strong>simultaneous interpreter</strong>: you speak one language (the unified "
        "<code>Msg</code>) and the interpreter renders it into whatever the other side "
        "understands (each vendor's format).",
    ),
    h2("接口", "The interface"),
    p(
        "所有 formatter 继承 <code>FormatterBase</code>，核心是<strong>异步</strong>方法 "
        "<code>format(...)</code>，返回 <code>list[dict]</code>。基类还提供 "
        "<code>supported_input_media_types</code>、消息分组等工具方法。",
        "All formatters subclass <code>FormatterBase</code>; the core is the "
        "<strong>async</strong> <code>format(...)</code> method returning "
        "<code>list[dict]</code>. The base also offers helpers like "
        "<code>supported_input_media_types</code> and message grouping.",
    ),
    code(
        "from agentscope.formatter import DashScopeChatFormatter\n"
        "from agentscope.message import UserMsg, SystemMsg\n\n"
        "formatter = DashScopeChatFormatter()\n"
        "payload = await formatter.format([\n"
        '    SystemMsg("system", "You are helpful."),\n'
        '    UserMsg("Tony", "Hi!"),\n'
        "])\n"
        "# payload is list[dict] ready to send to the vendor API",
        cap_zh="把 Msg 列表格式化成厂商请求负载（format 是 async）。",
        cap_en="Format a Msg list into the vendor payload (format is async).",
    ),
    h2("Chat vs MultiAgent", "Chat vs MultiAgent"),
    p(
        "每个厂商都有两个 formatter：<strong>Chat</strong> 用于「单一对话机器人」场景；"
        "<strong>MultiAgent</strong> 用于「多个 agent / 多方参与」场景，会把不同发言者的消息"
        "分组组织。",
        "Each vendor ships two formatters: <strong>Chat</strong> for a single chatbot dialogue, "
        "and <strong>MultiAgent</strong> for multi-party / multi-agent scenarios, which groups "
        "messages from different speakers.",
    ),
    table(
        [("厂商", "Vendor"), ("Chat", "Chat"), ("MultiAgent", "MultiAgent")],
        [
            [("DashScope", "DashScope"),
             ("<code>DashScopeChatFormatter</code>", "<code>DashScopeChatFormatter</code>"),
             ("<code>DashScopeMultiAgentFormatter</code>", "<code>DashScopeMultiAgentFormatter</code>")],
            [("OpenAI", "OpenAI"),
             ("<code>OpenAIChatFormatter</code>", "<code>OpenAIChatFormatter</code>"),
             ("<code>OpenAIMultiAgentFormatter</code>", "<code>OpenAIMultiAgentFormatter</code>")],
            [("Anthropic", "Anthropic"),
             ("<code>AnthropicChatFormatter</code>", "<code>AnthropicChatFormatter</code>"),
             ("<code>AnthropicMultiAgentFormatter</code>", "<code>AnthropicMultiAgentFormatter</code>")],
            [("Gemini / Ollama / DeepSeek / Moonshot / XAI",
              "Gemini / Ollama / DeepSeek / Moonshot / XAI"),
             ("<code>…ChatFormatter</code>", "<code>…ChatFormatter</code>"),
             ("<code>…MultiAgentFormatter</code>", "<code>…MultiAgentFormatter</code>")],
        ],
    ),
    note(
        "通常你不必手动调用 formatter——<code>Agent</code> 会根据所用模型自动选用匹配的 formatter；"
        "理解它有助于排查「为什么发给厂商的请求长这样」。",
        "Usually you don't call a formatter directly — the <code>Agent</code> picks the matching "
        "formatter for the model in use; understanding it helps you debug \"why the vendor "
        "request looks like this\".",
    ),
    source_map([
        ("formatter/_formatter_base.py",
         "<code>FormatterBase</code>：async <code>format</code>、"
         "<code>supported_input_media_types</code>、消息分组",
         "<code>FormatterBase</code>: async <code>format</code>, "
         "<code>supported_input_media_types</code>, message grouping"),
        ("formatter/_dashscope_formatter.py",
         "<code>DashScopeChatFormatter</code> / <code>DashScopeMultiAgentFormatter</code>",
         "<code>DashScopeChatFormatter</code> / <code>DashScopeMultiAgentFormatter</code>"),
        ("formatter/__init__.py",
         "每个厂商的 Chat / MultiAgent formatter 导出",
         "the Chat / MultiAgent formatter exports for every vendor"),
    ]),
    keypoints([
        ("Formatter 把统一的 <code>Msg</code> 列表翻译成厂商专属请求格式。",
         "A formatter translates the unified <code>Msg</code> list into a vendor-specific "
         "request format."),
        ("<code>FormatterBase.format</code> 是 <strong>async</strong>，返回 <code>list[dict]</code>。",
         "<code>FormatterBase.format</code> is <strong>async</strong> and returns "
         "<code>list[dict]</code>."),
        ("每个厂商都有 <strong>Chat</strong>（单对话）与 <strong>MultiAgent</strong>（多方）两种。",
         "Each vendor has both <strong>Chat</strong> (single dialogue) and "
         "<strong>MultiAgent</strong> (multi-party) variants."),
    ]),
)


LESSONS = {
    "09-event-system.html": LESSON_09,
    "10-streaming.html": LESSON_10,
    "11-formatter.html": LESSON_11,
}


QUIZZES = {
    "09-event-system.html": [
        (
            "块类事件（如文本块）遵循什么顺序？",
            "What order do block events (e.g. text blocks) follow?",
            [
                ("START → DELTA* → END", "START → DELTA* → END", True),
                ("只有一个 END 事件", "Only a single END event", False),
                ("随机顺序", "Random order", False),
            ],
            "每个块以 START 开始、若干 DELTA 增量、END 结束，便于前端增量渲染。",
            "Each block opens with START, streams DELTA chunks, and closes with END, enabling "
            "incremental rendering.",
        ),
    ],
    "10-streaming.html": [
        (
            "如何正确消费 <code>reply_stream</code>？",
            "How do you correctly consume <code>reply_stream</code>?",
            [
                ("用 <code>async for</code> 在异步函数里遍历事件",
                 "Iterate events with <code>async for</code> inside an async function", True),
                ("用普通 <code>for</code> 循环", "With a plain <code>for</code> loop", False),
                ("直接 <code>print(reply_stream)</code>", "Just <code>print(reply_stream)</code>", False),
            ],
            "reply_stream 是 async generator，必须用 async for 消费。",
            "reply_stream is an async generator and must be consumed with async for.",
        ),
    ],
    "11-formatter.html": [
        (
            "<code>FormatterBase.format</code> 的关键特征是什么？",
            "What is a key characteristic of <code>FormatterBase.format</code>?",
            [
                ("它是 async 方法，返回 <code>list[dict]</code>",
                 "It is an async method returning <code>list[dict]</code>", True),
                ("它返回一个字符串", "It returns a string", False),
                ("它训练模型", "It trains the model", False),
            ],
            "format 是异步方法，把 Msg 列表转成厂商请求所需的 list[dict]。",
            "format is async and turns the Msg list into the list[dict] the vendor request needs.",
        ),
    ],
}
