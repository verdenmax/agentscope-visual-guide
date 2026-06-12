"""Content for Part 7 (build your own): lessons 26–28.

Verified against AgentScope 2.0 source (tool/_base.py, tool/_adapters.py,
tool/_response.py, middleware/_base.py, agent/_agent.py).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 26 — Custom tools
# ---------------------------------------------------------------------------
LESSON_26 = blocks(
    lead(
        "给 agent 加一件你自己的工具有两条路：最简单的是用 <code>FunctionTool</code> 包装一个"
        "普通函数；要更精细的控制则<strong>继承 <code>ToolBase</code></strong>。",
        "There are two ways to give an agent a tool of your own: the simplest is to wrap a "
        "plain function with <code>FunctionTool</code>; for finer control you "
        "<strong>subclass <code>ToolBase</code></strong>.",
    ),
    analogy(
        "像往工具箱里<strong>自制一件工具</strong>：贴上清楚的标签（类型注解 + docstring），"
        "助手就知道它叫什么、要什么参数、什么时候用。",
        "Like <strong>making your own tool</strong> for the box: put a clear label on it (type "
        "hints + docstring) and the assistant knows its name, its arguments, and when to use it.",
    ),
    h2("方式一：包装一个函数（推荐）", "Option 1: wrap a function (recommended)"),
    code(
        "from agentscope.tool import FunctionTool, Toolkit, ToolResponse\n"
        "from agentscope.message import TextBlock\n\n"
        "def add(a: int, b: int) -> ToolResponse:\n"
        '    """Add two integers and return the sum.\n\n'
        "    Args:\n"
        "        a (int): the first number\n"
        "        b (int): the second number\n"
        '    """\n'
        "    return ToolResponse(content=[TextBlock(text=str(a + b))])\n\n"
        "toolkit = Toolkit(tools=[FunctionTool(add)])",
        cap_zh="FunctionTool 从签名+docstring 自动生成 schema；返回 ToolResponse。",
        cap_en="FunctionTool builds the schema from signature+docstring; return a ToolResponse.",
    ),
    h2("方式二：继承 ToolBase", "Option 2: subclass ToolBase"),
    p(
        "需要自定义权限、流式输出或有状态行为时，继承 <code>ToolBase</code>：设置 "
        "<code>name</code> / <code>description</code>，实现 <code>__call__</code>，并实现"
        "抽象方法 <code>check_permissions</code>（与权限系统对接，第 16 课）。返回值统一为 "
        "<code>ToolResponse</code>（或流式 <code>ToolChunk</code>）。",
        "When you need custom permissions, streaming, or stateful behavior, subclass "
        "<code>ToolBase</code>: set <code>name</code> / <code>description</code>, implement "
        "<code>__call__</code>, and implement the abstract <code>check_permissions</code> "
        "(it ties into the permission system, lesson 16). Results are <code>ToolResponse</code> "
        "(or streaming <code>ToolChunk</code>).",
    ),
    important(
        "错误语义很关键：工具里抛出 <code>AgentOrientedException</code>（如内置的 "
        "<code>ToolNotFoundError</code>）会把错误<strong>作为工具结果回喂给模型</strong>，让 agent "
        "有机会自行纠错；而 <code>DeveloperOrientedException</code> 会<strong>向上抛给开发者</strong>。"
        "据此选择：可恢复的错误用前者，编程 / 配置错误用后者。",
        "Error semantics matter: raising an <code>AgentOrientedException</code> (e.g. the "
        "built-in <code>ToolNotFoundError</code>) feeds the error <strong>back to the model as a "
        "tool result</strong> so the agent can recover, whereas a "
        "<code>DeveloperOrientedException</code> <strong>propagates to the developer</strong>. "
        "Choose accordingly: recoverable errors → the former, programming/config errors → the latter.",
    ),
    source_map([
        ("tool/_adapters.py", "<code>FunctionTool</code>（包装函数）",
         "<code>FunctionTool</code> (wraps a function)"),
        ("tool/_base.py", "<code>ToolBase</code> / <code>ParamsBase</code>、"
         "<code>check_permissions</code>、<code>__call__</code>",
         "<code>ToolBase</code> / <code>ParamsBase</code>, <code>check_permissions</code>, "
         "<code>__call__</code>"),
        ("tool/_response.py", "<code>ToolResponse</code> / <code>ToolChunk</code>",
         "<code>ToolResponse</code> / <code>ToolChunk</code>"),
    ]),
    keypoints([
        ("最简路径：<code>FunctionTool(your_function)</code>。",
         "Simplest path: <code>FunctionTool(your_function)</code>."),
        ("类型注解 + docstring 决定模型看到的工具说明。",
         "Type hints + docstring define the tool spec the model sees."),
        ("进阶：继承 <code>ToolBase</code>，实现 <code>__call__</code> 与 <code>check_permissions</code>。",
         "Advanced: subclass <code>ToolBase</code>, implement <code>__call__</code> and "
         "<code>check_permissions</code>."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 27 — Custom middleware
# ---------------------------------------------------------------------------
LESSON_27 = blocks(
    lead(
        "写一个中间件，就是<strong>继承 <code>MiddlewareBase</code></strong> 并实现你关心的钩子。"
        "每个钩子拿到 <code>agent</code>、本阶段的 <code>input_kwargs</code> 和一个 "
        "<code>next_handler</code>——在调用它前后插入你的逻辑。",
        "Writing middleware means <strong>subclassing <code>MiddlewareBase</code></strong> and "
        "implementing the hooks you care about. Each hook receives the <code>agent</code>, this "
        "stage's <code>input_kwargs</code>, and a <code>next_handler</code> — insert your logic "
        "before/after calling it.",
    ),
    analogy(
        "像<strong>洋葱</strong>的一层：请求向内穿过你这层（你可以记录/改写），到达核心后结果再向外"
        "穿回来（你可以再处理一次）。",
        "Like one layer of an <strong>onion</strong>: the request passes inward through your "
        "layer (you can log/rewrite), reaches the core, and the result passes back outward "
        "through you (you can post-process).",
    ),
    h2("一个日志中间件", "A logging middleware"),
    code(
        "from agentscope.middleware import MiddlewareBase\n\n"
        "class LoggingMiddleware(MiddlewareBase):\n"
        "    async def on_model_call(self, agent, input_kwargs, next_handler):\n"
        "        msgs = input_kwargs.get(\"messages\", [])\n"
        '        print(f"[{agent.name}] model call with {len(msgs)} messages")\n'
        "        response = await next_handler(**input_kwargs)   # proceed inward\n"
        '        print(f"[{agent.name}] model call done")\n'
        "        return response                                 # pass result outward",
        cap_zh="实现 on_model_call：调用 next_handler 前后插入逻辑。",
        cap_en="Implement on_model_call: insert logic around next_handler.",
    ),
    p(
        "把它挂到 agent 上即可生效（顺序即洋葱层次）：",
        "Attach it to the agent to take effect (order = onion layering):",
    ),
    code(
        "agent = Agent(\n"
        '    name="Friday", system_prompt="...", model=...,\n'
        "    middlewares=[LoggingMiddleware()],\n"
        ")",
        cap_zh="通过 middlewares=[...] 挂载你的中间件。",
        cap_en="Attach your middleware via middlewares=[...].",
    ),
    accordion(
        "可用的钩子有哪些？",
        "Which hooks are available?",
        blocks(p(
            "<code>on_reply</code>、<code>on_reasoning</code>、<code>on_acting</code>、"
            "<code>on_model_call</code>、<code>on_compress_context</code>、<code>on_system_prompt</code>、"
            "<code>list_tools</code>。只实现你需要的；其余保持默认即可（框架用 "
            "<code>is_implemented</code> 判断是否启用某钩子）。",
            "<code>on_reply</code>, <code>on_reasoning</code>, <code>on_acting</code>, "
            "<code>on_model_call</code>, <code>on_compress_context</code>, "
            "<code>on_system_prompt</code>, <code>list_tools</code>. Implement only what you "
            "need; leave the rest as defaults (the framework uses <code>is_implemented</code> to "
            "decide whether a hook is active).",
        )),
        num=1,
    ),
    source_map([
        ("middleware/_base.py",
         "<code>MiddlewareBase</code> 及钩子签名（<code>on_model_call(agent, input_kwargs, "
         "next_handler)</code> 等）",
         "<code>MiddlewareBase</code> and hook signatures (<code>on_model_call(agent, "
         "input_kwargs, next_handler)</code>, etc.)"),
        ("middleware/_tracing/_trace.py", "<code>TracingMiddleware</code>（参考实现）",
         "<code>TracingMiddleware</code> (reference implementation)"),
    ]),
    keypoints([
        ("继承 <code>MiddlewareBase</code>，实现需要的 <code>on_*</code> 钩子。",
         "Subclass <code>MiddlewareBase</code> and implement the <code>on_*</code> hooks you need."),
        ("每个钩子：在 <code>await next_handler(**input_kwargs)</code> 前后插逻辑。",
         "Each hook: insert logic around <code>await next_handler(**input_kwargs)</code>."),
        ("通过 <code>Agent(middlewares=[...])</code> 挂载；列表顺序决定包裹次序。",
         "Attach via <code>Agent(middlewares=[...])</code>; list order decides the wrapping order."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 28 — Capstone
# ---------------------------------------------------------------------------
LESSON_28 = blocks(
    lead(
        "把全书拼起来：一个真实的 agent = "
        '<a href="05-chat-models.html">模型</a> + '
        '<a href="06-credentials.html">凭证</a> + '
        '<a href="07-tools.html">工具箱</a> + '
        '<a href="16-permission.html">权限</a> + '
        '<a href="17-workspace.html">工作区</a> + '
        '<a href="27-custom-middleware.html">自定义中间件</a>，'
        '通过 <a href="10-streaming.html">事件流</a> 消费。',
        "Put the whole book together: a real agent = "
        '<a href="05-chat-models.html">model</a> + '
        '<a href="06-credentials.html">credential</a> + '
        '<a href="07-tools.html">toolkit</a> + '
        '<a href="16-permission.html">permission</a> + '
        '<a href="17-workspace.html">workspace</a> + '
        'a <a href="27-custom-middleware.html">custom middleware</a>, '
        'consumed via the <a href="10-streaming.html">event stream</a>.',
    ),
    analogy(
        "前面每一课是一块<strong>乐高积木</strong>；这一课把它们<strong>拼成一台完整的机器</strong>。",
        "Each earlier lesson was one <strong>Lego brick</strong>; this lesson "
        "<strong>assembles them into a complete machine</strong>.",
    ),
    h2("端到端示例", "End-to-end example"),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.model import DashScopeChatModel\n"
        "from agentscope.credential import DashScopeCredential\n"
        "from agentscope.tool import Toolkit, Bash, Read, Write, Edit\n"
        "from agentscope.middleware import MiddlewareBase\n"
        "from agentscope.state import AgentState\n"
        "from agentscope.permission import PermissionContext, PermissionMode\n"
        "from agentscope.message import UserMsg\n"
        "from agentscope.event import EventType\n"
        "import os, asyncio\n\n"
        "class LoggingMiddleware(MiddlewareBase):\n"
        "    async def on_model_call(self, agent, input_kwargs, next_handler):\n"
        '        print(f"[{agent.name}] thinking...")\n'
        "        return await next_handler(**input_kwargs)\n\n"
        "agent = Agent(\n"
        '    name="Friday",\n'
        '    system_prompt="You are a careful coding assistant.",\n'
        "    model=DashScopeChatModel(\n"
        "        credential=DashScopeCredential(\n"
        '            api_key=os.environ["DASHSCOPE_API_KEY"]),\n'
        '        model="qwen3.6-plus",\n'
        "    ),\n"
        "    toolkit=Toolkit(tools=[Bash(), Read(), Write(), Edit()]),\n"
        "    middlewares=[LoggingMiddleware()],\n"
        "    # BYPASS so the Write tool runs without pausing for confirmation\n"
        "    # (see lesson 16 for the confirm round-trip instead):\n"
        "    state=AgentState(\n"
        "        permission_context=PermissionContext(mode=PermissionMode.BYPASS)),\n"
        ")\n\n"
        "async def main():\n"
        '    prompt = UserMsg("Tony", "Create hello.py that prints Hello.")\n'
        "    async for evt in agent.reply_stream(prompt):\n"
        "        if evt.type == EventType.TEXT_BLOCK_DELTA:\n"
        "            print(evt.delta, end=\"\", flush=True)   # stream the text\n"
        "    print(\"\\n[done]\")\n\n"
        "asyncio.run(main())",
        cap_zh="模型+凭证+工具+中间件，BYPASS 放行，经 reply_stream 流式消费。",
        cap_en="Model+credential+tools+middleware, BYPASS-allowed, streamed via reply_stream.",
    ),
    accordion(
        "把它升级成服务",
        "Leveling it up to a service",
        blocks(p(
            "当你要对外提供多用户、多会话的能力时，用 "
            '<a href="23-agent-service.html">create_app</a> 把它包成 FastAPI 服务，'
            '用 <a href="24-message-bus.html">消息总线</a> 把事件推给前端，'
            '甚至用 <a href="25-agent-team.html">Agent Team</a> 让一个领导 agent 协调多个工作 agent。',
            "When you need multi-user, multi-session capability, wrap it as a FastAPI service "
            'with <a href="23-agent-service.html">create_app</a>, push events to the frontend '
            'over the <a href="24-message-bus.html">message bus</a>, and even let a leader agent '
            'coordinate workers with <a href="25-agent-team.html">Agent Team</a>.',
        )),
        num=1,
    ),
    source_map([
        ("agent/_agent.py", "把一切编排起来的 <code>Agent</code>",
         "the <code>Agent</code> that orchestrates everything"),
        ("examples/agent_service", "可运行的端到端服务示例",
         "a runnable end-to-end service example"),
    ]),
    highlight(
        "你已经走完「<strong>会用 → 懂原理 → 自己造</strong>」的全程：组合少数清晰的构件，就能"
        "搭出可观测、可控、可扩展、可部署的 agent。",
        "You've gone the full \"<strong>use it → understand it → build it</strong>\" arc: "
        "composing a few clear building blocks yields an agent that is observable, controllable, "
        "extensible and deployable.",
    ),
    keypoints([
        ("真实 agent = 模型 + 凭证 + 工具 + 权限 + 工作区 + 中间件，经事件流消费。",
         "A real agent = model + credential + tools + permission + workspace + middleware, "
         "consumed via the event stream."),
        ("同一个 agent 可用 <code>create_app</code> 升级为多租户服务。",
         "The same agent levels up to a multi-tenant service via <code>create_app</code>."),
        ("组合清晰构件 > 堆砌复杂编排。",
         "Composing clear building blocks beats piling on complex orchestration."),
    ]),
)


LESSONS = {
    "26-custom-tools.html": LESSON_26,
    "27-custom-middleware.html": LESSON_27,
    "28-capstone.html": LESSON_28,
}


QUIZZES: dict = {}

QUIZZES["26-custom-tools.html"] = [
    (
        "把一个普通 Python 函数变成工具，最简单的方式是？",
        "What's the simplest way to turn a plain Python function into a tool?",
        [
            ("用 <code>FunctionTool</code> 包装它——schema 由签名 + docstring 自动生成",
             "Wrap it with <code>FunctionTool</code> — the schema is auto-generated from the "
             "signature + docstring", True),
            ("自己手写 JSON schema 并解析参数",
             "Hand-write the JSON schema and parse the arguments yourself", False),
            ("继承 <code>ToolBase</code> 并实现 <code>check_permissions</code>",
             "Subclass <code>ToolBase</code> and implement <code>check_permissions</code>", False),
        ],
        "<code>FunctionTool(your_function)</code> 会从类型注解与 docstring 自动生成 schema，"
        "无需手写；继承 <code>ToolBase</code> 是需要自定义权限 / 流式 / 有状态时的进阶（更繁琐）路径。",
        "<code>FunctionTool(your_function)</code> auto-derives the schema from type hints and "
        "the docstring — no hand-writing; subclassing <code>ToolBase</code> is the more involved "
        "path for custom permissions / streaming / stateful behavior.",
    ),
]

QUIZZES["27-custom-middleware.html"] = [
    (
        "在自定义中间件的钩子里，如何正确地把控制传给下一层？",
        "Inside a custom middleware hook, how do you correctly pass control to the next layer?",
        [
            ("调用并 await：<code>response = await next_handler(**input_kwargs)</code>，再返回结果",
             "Call and await it: <code>response = await next_handler(**input_kwargs)</code>, "
             "then return the result", True),
            ("调用 <code>next_handler(**input_kwargs)</code> 但不加 <code>await</code>",
             "Call <code>next_handler(**input_kwargs)</code> but without <code>await</code>",
             False),
            ("直接 <code>return None</code>，框架会自动继续往下执行",
             "Just <code>return None</code>; the framework continues down the chain automatically",
             False),
        ],
        "钩子是 async 的，必须 <code>await next_handler(...)</code> 才会真正进入下一层；忘记 "
        "<code>await</code> 只会拿到一个未执行的协程，而 <code>return None</code> 会中断洋葱链、"
        "丢掉下游结果。",
        "Hooks are async, so you must <code>await next_handler(...)</code> to actually enter the "
        "next layer; forgetting <code>await</code> yields an un-executed coroutine, and "
        "<code>return None</code> breaks the onion chain and drops the downstream result.",
    ),
]

QUIZZES["28-capstone.html"] = [
    (
        "一个可用于生产的完整 agent 通常如何构成？",
        "How is a complete, production-ready agent typically composed?",
        [
            ("模型 + 凭证 + 工具 + 权限 + 工作区 + 中间件，经统一事件流消费",
             "model + credential + tools + permission + workspace + middleware, consumed via "
             "the unified event stream", True),
            ("只要一个足够好的系统提示词就够了",
             "A single, good-enough system prompt is all you need", False),
            ("把所有逻辑写进一段复杂的编排代码，而不是组合清晰的构件",
             "Hand-write all the logic in one complex orchestration script instead of composing "
             "clear building blocks", False),
        ],
        "真实 agent 由少数清晰构件组合而成（模型 / 凭证 / 工具 / 权限 / 工作区 / 中间件），并经"
        "事件流消费；这正体现「组合清晰构件 > 堆砌复杂编排」，单靠一个提示词远远不够。",
        "A real agent composes a few clear building blocks (model / credential / tools / "
        "permission / workspace / middleware) consumed via the event stream; this embodies "
        "\u201ccomposing clear building blocks beats piling on complex orchestration\u201d — a single "
        "prompt is nowhere near enough.",
    ),
]
