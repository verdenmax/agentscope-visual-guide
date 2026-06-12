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
        "重点在<strong>「按类型分别渲染」</strong>：同一条流里，文字增量追加进气泡、工具调用画成一张卡片、"
        "确认请求弹出一个按钮——你的代码用 <code>match evt.type</code> 决定每种怎么处理。",
        "The point is <strong>rendering each type differently</strong>: in one stream, text deltas "
        "append into a bubble, a tool call becomes a card, a confirm request pops a button — your "
        "code uses <code>match evt.type</code> to decide how to handle each.",
    ),
    h2("基本消费模式", "The basic consumption pattern"),
    code(
        "from agentscope.event import EventType\n"
        "from agentscope.message import UserMsg\n\n"
        "async def run(agent):\n"
        '    answer = []\n'
        '    async for evt in agent.reply_stream(UserMsg("Tony", "What\'s 2+2?")):\n'
        "        match evt.type:\n"
        "            case EventType.REPLY_START:\n"
        "                ...\n"
        "            case EventType.TEXT_BLOCK_DELTA:\n"
        "                print(evt.delta, end=\"\", flush=True)  # 增量文本 / streamed text\n"
        "                answer.append(evt.delta)               # 累积出最终答案 / accumulate\n"
        "            case EventType.TOOL_CALL_START:\n"
        "                ...        # 模型要调用工具 / a tool call\n"
        "            case EventType.REPLY_END:\n"
        '                ...        # 回复完成（不含最终消息）/ reply complete\n'
        '    return "".join(answer)                            # 最终文本 / the final text',
        cap_zh="关键：用 evt.delta 取增量文本，并自行累积成最终答案。",
        cap_en="Key: read incremental text from evt.delta and accumulate the final answer.",
    ),
    important(
        "事件对象不是字符串：增量文本在 <code>evt.delta</code> 里。直接 "
        "<code>print(evt)</code> 会打印一长串事件 repr，而不是「Hi Tony!」。",
        "An event is not a string: the incremental text lives in <code>evt.delta</code>. "
        "<code>print(evt)</code> dumps a long event repr, not \"Hi Tony!\".",
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


QUIZZES: dict = {}

QUIZZES["09-event-system.html"] = [
    (
        "关于 <code>REPLY_END</code> 和块的 <code>END</code> 事件，下面哪句正确？",
        "Which statement about <code>REPLY_END</code> and a block's <code>END</code> event is correct?",
        [
            ("它们只标记「结束」，<strong>不</strong>携带最终消息；最终 <code>AssistantMsg</code> 要靠累积 DELTA 或用 <code>reply()</code> 拿",
             "They only mark \u201cdone\u201d and do <strong>not</strong> carry the final message; the final <code>AssistantMsg</code> comes from accumulating DELTAs or from <code>reply()</code>", True),
            ("<code>REPLY_END</code> 里就装着完整的最终回复文本",
             "<code>REPLY_END</code> contains the complete final reply text", False),
            ("<code>TEXT_BLOCK_END</code> 携带这一块拼好的完整文本",
             "<code>TEXT_BLOCK_END</code> carries the fully assembled text of that block", False),
        ],
        "<code>END</code> 类事件只表示「这一段结束」，<code>ReplyEndEvent</code> 只带 <code>session_id</code> / <code>reply_id</code>。要完整内容：累积各 <code>DELTA</code>，或直接用 <code>agent.reply()</code>。",
        "<code>END</code> events only signal \u201cthis segment is done\u201d; <code>ReplyEndEvent</code> carries just <code>session_id</code> / <code>reply_id</code>. For the full content, accumulate the <code>DELTA</code>s or use <code>agent.reply()</code>.",
    ),
]

QUIZZES["10-streaming.html"] = [
    (
        "流式输出时，想把模型的文字实时打印出来，应该读取什么？",
        "While streaming, to print the model's text live, what should you read?",
        [
            ("直接 <code>print(evt)</code>，事件本身就是那段文字",
             "Just <code>print(evt)</code> — the event itself is the text", False),
            ("在 <code>TEXT_BLOCK_DELTA</code> 事件上读取 <code>evt.delta</code>（增量文本）并自行累积",
             "Read <code>evt.delta</code> (the incremental text) on <code>TEXT_BLOCK_DELTA</code> events and accumulate it yourself", True),
            ("等 <code>REPLY_END</code>，从它里面取完整文本",
             "Wait for <code>REPLY_END</code> and read the full text from it", False),
        ],
        "增量文本在 <code>evt.delta</code> 里，<code>print(evt)</code> 只会打印事件的 repr。把每个 <code>DELTA</code> 的 <code>delta</code> 拼起来就是最终文本；<code>REPLY_END</code> 不含文本。",
        "The incremental text lives in <code>evt.delta</code>; <code>print(evt)</code> only dumps the event's repr. Concatenate each <code>DELTA</code>'s <code>delta</code> for the final text; <code>REPLY_END</code> carries none.",
    ),
]

QUIZZES["11-formatter.html"] = [
    (
        "每个厂商都提供 <strong>Chat</strong> 和 <strong>MultiAgent</strong> 两个 formatter，它们的区别是什么？",
        "Each vendor ships both a <strong>Chat</strong> and a <strong>MultiAgent</strong> formatter. What is the difference?",
        [
            ("Chat 给单个 agent 用；MultiAgent 会自己同时调用多个模型并做编排",
             "Chat is for one agent; MultiAgent itself calls several models at once and orchestrates them", False),
            ("Chat 面向单一对话机器人；MultiAgent 面向多方 / 多 agent 场景，会按发言者分组消息",
             "Chat targets a single chatbot dialogue; MultiAgent targets multi-party / multi-agent settings and groups messages by speaker", True),
            ("Chat 的 <code>format</code> 是同步的，MultiAgent 的是异步的",
             "Chat's <code>format</code> is synchronous; MultiAgent's is asynchronous", False),
        ],
        "两者都只把 <code>Msg</code> 列表转成 <code>list[dict]</code>（<code>format</code> 都是 async），不做模型编排。区别在场景：Chat 单对话，MultiAgent 多方并按发言者分组。",
        "Both only turn the <code>Msg</code> list into <code>list[dict]</code> (their <code>format</code> is async) and do no model orchestration. The difference is the scenario: Chat for single dialogue, MultiAgent for multi-party with speaker grouping.",
    ),
]
