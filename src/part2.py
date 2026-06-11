"""Content for Part 2 (user's view): lessons 04–08.

Verified against AgentScope 2.0 source (message/_base.py, message/_block.py,
model/, credential/, tool/, agent/_agent.py).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 04 — Messages
# ---------------------------------------------------------------------------
LESSON_04 = blocks(
    lead(
        "AgentScope 用结构化的<strong>消息对象</strong>承载对话。一条 <code>Msg</code> 记录"
        "「谁说的」（name + role）和「说了什么」——而内容是一个<strong>内容块列表</strong>，"
        "可以是文本、思考、工具调用、工具结果或多模态数据。",
        "AgentScope carries dialogue in structured <strong>message objects</strong>. A "
        "<code>Msg</code> records \"who spoke\" (name + role) and \"what was said\" — where "
        "the content is a <strong>list of content blocks</strong>: text, thinking, tool calls, "
        "tool results, or multimodal data.",
    ),
    analogy(
        "把 <code>Msg</code> 想成一个<strong>信封</strong>：信封上写着寄件人与身份（name/role），"
        "里面可以装好几张<strong>卡片</strong>（内容块）——一张是文字，一张是图片，一张是"
        "「我要调用某工具」的请求。",
        "Think of a <code>Msg</code> as an <strong>envelope</strong>: the outside shows the "
        "sender and role (name/role), and inside are several <strong>cards</strong> (content "
        "blocks) — one text, one image, one \"please call this tool\" request.",
    ),
    h2("消息家族", "The message family"),
    p(
        "<code>Msg</code> 是核心数据类。<code>UserMsg</code>、<code>AssistantMsg</code>、"
        "<code>SystemMsg</code> 是<strong>工厂函数</strong>，分别构造带固定 role 的 "
        "<code>Msg</code>（不是子类）。",
        "<code>Msg</code> is the core data class. <code>UserMsg</code>, "
        "<code>AssistantMsg</code> and <code>SystemMsg</code> are <strong>factory "
        "functions</strong> that each build a <code>Msg</code> with a fixed role (they are not "
        "subclasses).",
    ),
    code(
        "from agentscope.message import UserMsg, AssistantMsg, SystemMsg\n\n"
        'sys = SystemMsg("system", "You are helpful.")\n'
        'user = UserMsg("Tony", "Hello!")          # role = user\n'
        'reply = AssistantMsg("Friday", "Hi Tony!")  # role = assistant\n'
        "print(user.name, user.role)               # Tony user",
        cap_zh="工厂函数构造带固定 role 的 Msg。",
        cap_en="Factory functions build a Msg with a fixed role.",
    ),
    h2("内容块", "Content blocks"),
    table(
        [("块类型", "Block type"), ("用途", "Purpose")],
        [
            [("<code>TextBlock</code>", "<code>TextBlock</code>"),
             ("普通文本", "plain text")],
            [("<code>ThinkingBlock</code>", "<code>ThinkingBlock</code>"),
             ("模型的思考 / 推理过程", "the model's thinking / reasoning")],
            [("<code>ToolCallBlock</code>", "<code>ToolCallBlock</code>"),
             ("模型请求调用某个工具", "the model requesting a tool call")],
            [("<code>ToolResultBlock</code>", "<code>ToolResultBlock</code>"),
             ("工具执行的返回结果", "the result of running a tool")],
            [("<code>DataBlock</code>", "<code>DataBlock</code>"),
             ("多模态数据（图片/音频等，含 <code>Base64Source</code> / <code>URLSource</code>）",
              "multimodal data (image/audio, via <code>Base64Source</code> / <code>URLSource</code>)")],
        ],
    ),
    p(
        "<code>content</code> 既可以是一个字符串（自动包装成文本块），也可以是一个内容块列表，"
        "用于多模态或携带工具调用 / 结果。",
        "<code>content</code> may be a plain string (auto-wrapped as a text block) or a list of "
        "content blocks, used for multimodal input or to carry tool calls / results.",
    ),
    source_map([
        ("message/_base.py",
         "<code>Msg</code> 类，及 <code>UserMsg</code> / <code>AssistantMsg</code> / "
         "<code>SystemMsg</code> 工厂函数、<code>Usage</code>",
         "the <code>Msg</code> class, the <code>UserMsg</code> / <code>AssistantMsg</code> / "
         "<code>SystemMsg</code> factories, and <code>Usage</code>"),
        ("message/_block.py",
         "<code>TextBlock</code> / <code>ThinkingBlock</code> / <code>ToolCallBlock</code> / "
         "<code>ToolResultBlock</code> / <code>DataBlock</code> 等",
         "<code>TextBlock</code> / <code>ThinkingBlock</code> / <code>ToolCallBlock</code> / "
         "<code>ToolResultBlock</code> / <code>DataBlock</code>, etc."),
    ]),
    keypoints([
        ("<code>Msg</code> = 发送者 + role + <strong>内容块列表</strong>。",
         "<code>Msg</code> = sender + role + a <strong>list of content blocks</strong>."),
        ("<code>UserMsg</code>/<code>AssistantMsg</code>/<code>SystemMsg</code> 是工厂函数，不是子类。",
         "<code>UserMsg</code>/<code>AssistantMsg</code>/<code>SystemMsg</code> are factory "
         "functions, not subclasses."),
        ("内容块统一表达文本、思考、工具调用/结果与多模态数据。",
         "Content blocks uniformly express text, thinking, tool calls/results and multimodal data."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 05 — Chat Models
# ---------------------------------------------------------------------------
LESSON_05 = blocks(
    lead(
        "聊天模型是 agent 的「大脑」。所有厂商实现都继承 <code>ChatModelBase</code>，暴露统一"
        "接口；调用返回一个 <code>ChatResponse</code>（含内容块与用量）。",
        "The chat model is the agent's \"brain\". Every vendor implementation subclasses "
        "<code>ChatModelBase</code> and exposes a unified interface; a call returns a "
        "<code>ChatResponse</code> (content blocks + usage).",
    ),
    analogy(
        "像一个<strong>万能遥控器</strong>：不管电视是哪个牌子，按钮都一样。换模型 = 换一个"
        "<code>ChatModelBase</code> 子类，调用代码几乎不动。",
        "Like a <strong>universal remote</strong>: whatever the TV brand, the buttons are the "
        "same. Swapping models = swapping a <code>ChatModelBase</code> subclass, with almost "
        "no change to calling code.",
    ),
    h2("支持的厂商", "Supported vendors"),
    table(
        [("厂商 / Vendor", "厂商 / Vendor"), ("类 / Class", "类 / Class")],
        [
            [("DashScope（通义千问）", "DashScope (Qwen)"),
             ("<code>DashScopeChatModel</code>", "<code>DashScopeChatModel</code>")],
            [("OpenAI", "OpenAI"),
             ("<code>OpenAIChatModel</code> / <code>OpenAIResponseModel</code>",
              "<code>OpenAIChatModel</code> / <code>OpenAIResponseModel</code>")],
            [("Anthropic", "Anthropic"),
             ("<code>AnthropicChatModel</code>", "<code>AnthropicChatModel</code>")],
            [("Gemini / Ollama / DeepSeek / Moonshot / XAI",
              "Gemini / Ollama / DeepSeek / Moonshot / XAI"),
             ("<code>GeminiChatModel</code> 等", "<code>GeminiChatModel</code>, etc.")],
        ],
    ),
    code(
        "from agentscope.model import DashScopeChatModel\n"
        "from agentscope.credential import DashScopeCredential\n"
        "import os\n\n"
        "model = DashScopeChatModel(\n"
        "    credential=DashScopeCredential(\n"
        '        api_key=os.environ["DASHSCOPE_API_KEY"]),\n'
        '    model="qwen3.6-plus",\n'
        ")\n"
        "# the Agent calls the model for you; a direct call returns a ChatResponse",
        cap_zh="构造一个聊天模型（凭证见下一课）。",
        cap_en="Construct a chat model (credentials in the next lesson).",
    ),
    accordion(
        "ChatResponse 里有什么？",
        "What's in a ChatResponse?",
        blocks(
            p(
                "<code>ChatResponse</code> 携带模型产出的<strong>内容块</strong>（文本/思考/工具调用）"
                "与 <code>ChatUsage</code>（token 用量）。需要结构化输出时用 "
                "<code>StructuredResponse</code>。<code>ModelCard</code> 描述模型能力元信息。",
                "<code>ChatResponse</code> carries the model's <strong>content blocks</strong> "
                "(text/thinking/tool calls) plus <code>ChatUsage</code> (token usage). For "
                "structured output use <code>StructuredResponse</code>; <code>ModelCard</code> "
                "describes a model's capability metadata.",
            ),
        ),
        num=1,
    ),
    source_map([
        ("model/_base.py", "<code>ChatModelBase</code> 统一接口",
         "<code>ChatModelBase</code> unified interface"),
        ("model/_model_response.py", "<code>ChatResponse</code> / <code>StructuredResponse</code>",
         "<code>ChatResponse</code> / <code>StructuredResponse</code>"),
        ("model/_dashscope.py", "<code>DashScopeChatModel</code> 等厂商实现",
         "<code>DashScopeChatModel</code> and other vendor implementations"),
    ]),
    keypoints([
        ("所有模型继承 <code>ChatModelBase</code>，接口统一。",
         "All models subclass <code>ChatModelBase</code> with a unified interface."),
        ("调用返回 <code>ChatResponse</code>（内容块 + <code>ChatUsage</code>）。",
         "A call returns a <code>ChatResponse</code> (content blocks + <code>ChatUsage</code>)."),
        ("换厂商基本只改模型类与配置。",
         "Switching vendors is mostly changing the model class + config."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 06 — Credentials
# ---------------------------------------------------------------------------
LESSON_06 = blocks(
    lead(
        "<strong>凭证（Credential）</strong>把「密钥」从「模型配置」里分离出来。每个厂商有自己的"
        "<code>CredentialBase</code> 子类，<code>CredentialFactory</code> 可按需创建。",
        "<strong>Credentials</strong> separate \"secrets\" from \"model config\". Each vendor "
        "has its own <code>CredentialBase</code> subclass, and <code>CredentialFactory</code> "
        "can create them on demand.",
    ),
    analogy(
        "像<strong>门禁卡</strong>与<strong>办公室</strong>分开：办公室（模型）的布置是公开的，"
        "门禁卡（密钥）单独保管、单独发放，不写死在墙上。",
        "Like keeping the <strong>access card</strong> separate from the <strong>office</strong>: "
        "the office (model) layout is public, while the card (secret) is held and issued "
        "separately — never written on the wall.",
    ),
    important(
        "<strong>绝不要把 API key 硬编码进源码</strong>。从环境变量或安全配置读取，例如 "
        "<code>os.environ[\"DASHSCOPE_API_KEY\"]</code>。",
        "<strong>Never hardcode an API key in source.</strong> Read it from an environment "
        "variable or a secret store, e.g. <code>os.environ[\"DASHSCOPE_API_KEY\"]</code>.",
    ),
    code(
        "from agentscope.credential import DashScopeCredential\n"
        "import os\n\n"
        "cred = DashScopeCredential(api_key=os.environ[\"DASHSCOPE_API_KEY\"])\n"
        "# pass `credential=cred` into the matching ChatModel",
        cap_zh="从环境变量读取密钥构造凭证。",
        cap_en="Build a credential from an environment variable.",
    ),
    p(
        "其他厂商类似：<code>OpenAICredential</code>、<code>AnthropicCredential</code>、"
        "<code>GeminiCredential</code> 等；<code>CredentialFactory</code> 提供按类型创建的统一入口。",
        "Other vendors are analogous: <code>OpenAICredential</code>, "
        "<code>AnthropicCredential</code>, <code>GeminiCredential</code>, …; "
        "<code>CredentialFactory</code> offers a unified create-by-type entry point.",
    ),
    source_map([
        ("credential/_base.py", "<code>CredentialBase</code>",
         "<code>CredentialBase</code>"),
        ("credential/_factory.py", "<code>CredentialFactory</code>",
         "<code>CredentialFactory</code>"),
        ("credential/_dashscope.py", "<code>DashScopeCredential</code> 等厂商凭证",
         "<code>DashScopeCredential</code> and other vendor credentials"),
    ]),
    keypoints([
        ("凭证与模型配置<strong>解耦</strong>，便于轮换与多环境管理。",
         "Credentials are <strong>decoupled</strong> from model config — easy to rotate and "
         "manage across environments."),
        ("永远从环境变量 / 密钥库读取，<strong>不要硬编码</strong>。",
         "Always read from env vars / a secret store — <strong>never hardcode</strong>."),
        ("每个厂商一个 <code>CredentialBase</code> 子类；工厂可按类型创建。",
         "One <code>CredentialBase</code> subclass per vendor; the factory creates them by type."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 07 — Tools
# ---------------------------------------------------------------------------
LESSON_07 = blocks(
    lead(
        "<strong>工具（Tool）</strong>是 agent 的「手」。<code>Toolkit</code> 负责注册和管理工具，"
        "并自动从函数签名 / 文档字符串生成 JSON schema，让模型知道有哪些工具可用、怎么调用。",
        "<strong>Tools</strong> are the agent's \"hands\". <code>Toolkit</code> registers and "
        "manages tools and auto-generates a JSON schema from each tool's signature / docstring, "
        "so the model knows what's available and how to call it.",
    ),
    analogy(
        "像给助手配一套<strong>工具箱</strong>：每件工具都贴有「说明标签」（schema）。你只管把工具"
        "放进箱子（<code>Toolkit</code>），助手自己读标签决定用哪个。",
        "Like giving an assistant a <strong>toolbox</strong>: each tool has a \"label\" "
        "(schema). You just put tools in the box (<code>Toolkit</code>) and the assistant reads "
        "the labels to pick the right one.",
    ),
    h2("内置工具", "Built-in tools"),
    p(
        "AgentScope 自带一组开箱即用的工具，常用于「能动手的」agent：",
        "AgentScope ships a set of ready-to-use tools, common for \"hands-on\" agents:",
    ),
    code(
        "from agentscope.tool import Toolkit, Bash, Read, Write, Edit, Grep, Glob\n\n"
        "toolkit = Toolkit(tools=[Bash(), Read(), Write(), Edit(), Grep(), Glob()])",
        cap_zh="把内置工具放进一个 Toolkit。",
        cap_en="Put built-in tools into a Toolkit.",
    ),
    accordion(
        "一个 Python 函数如何变成工具？",
        "How does a Python function become a tool?",
        blocks(
            p(
                "<code>FunctionTool</code> 包装一个普通函数：它从函数<strong>签名</strong>推断参数 "
                "schema，从<strong>文档字符串</strong>提取描述。于是模型看到的「工具说明」就是你函数"
                "的签名 + docstring——所以写清楚类型注解和 docstring 很重要。",
                "<code>FunctionTool</code> wraps a plain function: it infers the parameter "
                "schema from the function's <strong>signature</strong> and the description from "
                "its <strong>docstring</strong>. So the \"tool spec\" the model sees is your "
                "function's signature + docstring — which is why clear type hints and docstrings "
                "matter.",
            ),
            code(
                "from agentscope.tool import FunctionTool, Toolkit\n\n"
                "def get_weather(city: str) -> str:\n"
                '    """Look up the weather for a city.\n\n'
                "    Args:\n"
                "        city (str): the city name\n"
                '    """\n'
                "    ...\n\n"
                "toolkit = Toolkit(tools=[FunctionTool(get_weather)])",
                cap_zh="用 FunctionTool 包装函数，schema 自动生成。",
                cap_en="Wrap a function with FunctionTool; the schema is auto-generated.",
            ),
        ),
        num=1,
    ),
    p(
        "Agent 内部通过 <code>Toolkit.get_tool_schemas()</code>（<strong>异步</strong>）取得所有工具"
        "的 JSON schema 交给模型；模型选定后由 <code>Toolkit.call_tool(...)</code> 执行。",
        "Internally the agent obtains every tool's JSON schema via "
        "<code>Toolkit.get_tool_schemas()</code> (<strong>async</strong>) and hands it to the "
        "model; once the model chooses, <code>Toolkit.call_tool(...)</code> runs it.",
    ),
    source_map([
        ("tool/_toolkit.py",
         "<code>Toolkit</code>：注册、<code>get_tool_schemas</code>(async)、<code>call_tool</code>",
         "<code>Toolkit</code>: registration, <code>get_tool_schemas</code> (async), "
         "<code>call_tool</code>"),
        ("tool/_base.py", "<code>ToolBase</code> / <code>ParamsBase</code>",
         "<code>ToolBase</code> / <code>ParamsBase</code>"),
        ("tool/_adapters.py", "<code>FunctionTool</code>（包装函数）、<code>MCPTool</code>",
         "<code>FunctionTool</code> (wraps a function), <code>MCPTool</code>"),
        ("tool/_builtin/", "内置工具：<code>Bash</code>/<code>Read</code>/<code>Write</code>/"
         "<code>Edit</code>/<code>Grep</code>/<code>Glob</code>",
         "built-ins: <code>Bash</code>/<code>Read</code>/<code>Write</code>/"
         "<code>Edit</code>/<code>Grep</code>/<code>Glob</code>"),
    ]),
    keypoints([
        ("<code>Toolkit</code> 注册并管理工具，自动生成 JSON schema。",
         "<code>Toolkit</code> registers/manages tools and auto-generates JSON schemas."),
        ("内置工具：<code>Bash/Read/Write/Edit/Grep/Glob</code>。",
         "Built-ins: <code>Bash/Read/Write/Edit/Grep/Glob</code>."),
        ("<code>FunctionTool</code> 把函数的签名 + docstring 变成工具说明。",
         "<code>FunctionTool</code> turns a function's signature + docstring into its tool spec."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 08 — Agent intro
# ---------------------------------------------------------------------------
LESSON_08 = blocks(
    lead(
        "把前面拼起来：<code>Agent</code> = 名字 + 系统提示 + 模型 + 工具箱。它运行一个"
        "<strong>「推理-行动」（ReAct）循环</strong>：想 → 用工具 → 观察结果 → 再想，直到给出答案。",
        "Putting it together: an <code>Agent</code> = name + system prompt + model + toolkit. "
        "It runs a <strong>reasoning-acting (ReAct) loop</strong>: think → use a tool → observe "
        "→ think again, until it answers.",
    ),
    analogy(
        "像一位<strong>助理</strong>：你给他一个身份设定（系统提示）、一个大脑（模型）和一套工具"
        "（工具箱），他就能自己边想边干活，而不是只会背稿子。",
        "Like an <strong>assistant</strong>: give them a persona (system prompt), a brain "
        "(model) and a set of tools (toolkit), and they can think and act on their own rather "
        "than just reciting a script.",
    ),
    h2("构造一个 Agent", "Constructing an Agent"),
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
        '    msg = await agent.reply(UserMsg("Tony", "List files here."))\n'
        "    print(msg)\n\n"
        "asyncio.run(main())",
        cap_zh="最小可用 agent；reply 返回最终 AssistantMsg。",
        cap_en="A minimal working agent; reply returns the final AssistantMsg.",
    ),
    h2("构造参数", "Constructor parameters"),
    table(
        [("参数", "Parameter"), ("含义", "Meaning")],
        [
            [("<code>name</code>", "<code>name</code>"),
             ("agent 标识", "the agent identifier")],
            [("<code>system_prompt</code>", "<code>system_prompt</code>"),
             ("系统提示（人设/指令）", "the system prompt (persona/instructions)")],
            [("<code>model</code>", "<code>model</code>"),
             ("<code>ChatModelBase</code> 实例", "a <code>ChatModelBase</code> instance")],
            [("<code>toolkit</code>", "<code>toolkit</code>"),
             ("可选的工具箱", "an optional toolkit")],
            [("<code>middlewares</code>", "<code>middlewares</code>"),
             ("可选的中间件列表（第 15 课）", "an optional middleware list (lesson 15)")],
            [("<code>state</code> / <code>offloader</code>", "<code>state</code> / <code>offloader</code>"),
             ("可选的状态与上下文卸载（第 19 / 17 课）",
              "optional state and context offloading (lessons 19 / 17)")],
            [("<code>*_config</code>", "<code>*_config</code>"),
             ("<code>ModelConfig</code> / <code>ContextConfig</code> / <code>ReActConfig</code>",
              "<code>ModelConfig</code> / <code>ContextConfig</code> / <code>ReActConfig</code>")],
        ],
    ),
    note(
        "用 <code>reply</code> 拿最终结果；用 <code>reply_stream</code> 拿事件流（第 10 课）；"
        "用 <code>observe</code> 注入消息而不立即回复。",
        "Use <code>reply</code> for the final result; <code>reply_stream</code> for the event "
        "stream (lesson 10); <code>observe</code> to inject messages without replying.",
    ),
    source_map([
        ("agent/_agent.py",
         "<code>Agent</code> 构造器与 <code>reply</code> / <code>reply_stream</code> / "
         "<code>observe</code> / <code>compress_context</code>",
         "the <code>Agent</code> constructor and <code>reply</code> / <code>reply_stream</code> "
         "/ <code>observe</code> / <code>compress_context</code>"),
        ("agent/_config.py",
         "<code>ContextConfig</code> / <code>ModelConfig</code> / <code>ReActConfig</code>",
         "<code>ContextConfig</code> / <code>ModelConfig</code> / <code>ReActConfig</code>"),
    ]),
    highlight(
        "Agent 不靠死板脚本，而是把模型放进一个「想—做—再想」的循环里，并用工具与事件让它"
        "<strong>真正能干活、且过程可见</strong>。",
        "The Agent doesn't rely on a rigid script; it places the model in a think-act-think "
        "loop and uses tools + events to make it <strong>actually capable and observable</strong>.",
    ),
    keypoints([
        ("<code>Agent</code> = name + system_prompt + model + toolkit。",
         "<code>Agent</code> = name + system_prompt + model + toolkit."),
        ("它运行 ReAct（推理-行动）循环，自动编排工具调用。",
         "It runs a ReAct (reason-act) loop, orchestrating tool calls automatically."),
        ("<code>reply</code> 要结果，<code>reply_stream</code> 要过程。",
         "<code>reply</code> for the result, <code>reply_stream</code> for the process."),
    ]),
)


LESSONS = {
    "04-messages.html": LESSON_04,
    "05-chat-models.html": LESSON_05,
    "06-credentials.html": LESSON_06,
    "07-tools.html": LESSON_07,
    "08-agents-intro.html": LESSON_08,
}


QUIZZES = {
    "04-messages.html": [
        (
            "<code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code> 是什么？",
            "What are <code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code>?",
            [
                ("构造带固定 role 的 <code>Msg</code> 的工厂函数",
                 "Factory functions that build a <code>Msg</code> with a fixed role", True),
                ("<code>Msg</code> 的三个子类", "Three subclasses of <code>Msg</code>", False),
                ("三种不同的模型", "Three different models", False),
            ],
            "它们是工厂函数，返回 role 固定的 Msg，而不是子类。",
            "They are factory functions returning a Msg with a fixed role, not subclasses.",
        ),
    ],
    "05-chat-models.html": [
        (
            "所有聊天模型的共同基类是什么？",
            "What is the common base class of all chat models?",
            [
                ("<code>ChatModelBase</code>", "<code>ChatModelBase</code>", True),
                ("<code>Agent</code>", "<code>Agent</code>", False),
                ("<code>Toolkit</code>", "<code>Toolkit</code>", False),
            ],
            "每个厂商实现都继承 ChatModelBase，统一调用接口。",
            "Every vendor implementation subclasses ChatModelBase for a unified interface.",
        ),
    ],
    "06-credentials.html": [
        (
            "API key 应该怎么管理？",
            "How should an API key be managed?",
            [
                ("从环境变量 / 密钥库读取，不要硬编码",
                 "Read from an env var / secret store; never hardcode", True),
                ("直接写进源码", "Write it directly into the source", False),
                ("提交到 git", "Commit it to git", False),
            ],
            "凭证应从环境变量读取并与模型配置解耦，绝不硬编码。",
            "Credentials should be read from env vars, decoupled from model config, never hardcoded.",
        ),
    ],
    "07-tools.html": [
        (
            "<code>Toolkit</code> 如何让模型知道某个工具怎么调用？",
            "How does <code>Toolkit</code> tell the model how to call a tool?",
            [
                ("自动从函数签名 / docstring 生成 JSON schema",
                 "It auto-generates a JSON schema from the signature / docstring", True),
                ("要求你手写 schema", "It requires you to hand-write the schema", False),
                ("它不暴露任何信息", "It exposes nothing", False),
            ],
            "Toolkit 通过 get_tool_schemas() 自动生成并提供工具的 JSON schema。",
            "Toolkit auto-generates and provides each tool's JSON schema via get_tool_schemas().",
        ),
    ],
    "08-agents-intro.html": [
        (
            "<code>Agent</code> 运行的核心循环是什么？",
            "What core loop does an <code>Agent</code> run?",
            [
                ("推理-行动（ReAct）循环", "A reasoning-acting (ReAct) loop", True),
                ("一次性返回，无循环", "One-shot, no loop", False),
                ("无限随机循环", "An infinite random loop", False),
            ],
            "Agent 在 ReAct 循环里「想—用工具—观察—再想」，直到给出答案。",
            "The Agent thinks, uses tools, observes, and thinks again in a ReAct loop until it answers.",
        ),
    ],
}
