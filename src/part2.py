"""Content for Part 2 (user's view): lessons 04–08.

Verified against AgentScope 2.0 source (message/_base.py, message/_block.py,
model/, credential/, tool/, agent/_agent.py).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t, flow,
)

# ---------------------------------------------------------------------------
# Lesson 04 — Messages
# ---------------------------------------------------------------------------
LESSON_04 = blocks(
    lead(
        "AgentScope 用结构化的<strong>消息对象</strong>承载对话。一条 <code>Msg</code> 记录"
        "「谁说的」（name + role）和「说了什么」——内容是一个<strong>内容块列表</strong>"
        "（下表详列各类型）。",
        "AgentScope carries dialogue in structured <strong>message objects</strong>. A "
        "<code>Msg</code> records \"who spoke\" (name + role) and \"what was said\" — the "
        "content is a <strong>list of content blocks</strong> (the table below lists the types).",
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
    h2("深入：content 永远是「块列表」", "Deeper: content is always a list of blocks"),
    p(
        "用 <code>UserMsg</code>/<code>AssistantMsg</code>/<code>SystemMsg</code> 传入一个字符串时，"
        "这些工厂会把它<strong>归一化成单元素的块列表</strong>（一个 <code>TextBlock</code>）。所以构造出的 "
        "<code>msg.content</code> 永远是 <code>list[ContentBlock]</code>，不是 <code>str</code>——想拿纯文本请用 "
        "<code>get_text_content()</code>。",
        "When you pass a plain string to <code>UserMsg</code>/<code>AssistantMsg</code>/"
        "<code>SystemMsg</code>, these factories <strong>normalize it into a one-element list of "
        "blocks</strong> (a single <code>TextBlock</code>). So the resulting <code>msg.content</code> "
        "is always a <code>list[ContentBlock]</code>, never a <code>str</code> — to get plain text "
        "use <code>get_text_content()</code>.",
    ),
    code(
        'msg = AssistantMsg("Friday", "Hi!")\n'
        "type(msg.content)            # list  —— 不是 str / not str\n"
        "msg.get_text_content()       # 'Hi!'  —— 拼接所有文本块 / joins text blocks\n\n"
        "# 按 block.type 分发 / dispatch on block.type\n"
        "for block in msg.content:\n"
        '    if block.type == "tool_call":      # 注意：tool_call，不是 tool_use\n'
        "        handle(block)\n"
        '    elif block.type == "text":\n'
        "        show(block.text)",
        cap_zh="content 是块列表；取文本用 get_text_content()，分发看 block.type。",
        cap_en="content is a list of blocks; use get_text_content() for text, block.type to dispatch.",
    ),
    important(
        "块的判别字段是 <code>type</code> 字面量：<code>ToolCallBlock.type == \"tool_call\"</code>"
        "（<strong>不是</strong>某些厂商原生的 <code>\"tool_use\"</code>），"
        "<code>ToolResultBlock.type == \"tool_result\"</code>。跨厂商代码统一按这些字面量判断，"
        "不要去比对各家 SDK 的原始命名。",
        "A block's discriminator is its <code>type</code> literal: "
        "<code>ToolCallBlock.type == \"tool_call\"</code> (<strong>not</strong> the "
        "<code>\"tool_use\"</code> some vendors use natively), and "
        "<code>ToolResultBlock.type == \"tool_result\"</code>. Cross-vendor code keys off these, "
        "never the raw per-SDK names.",
    ),
    note(
        "<code>name</code> 与 <code>role</code> 是两回事：<code>role</code> 只能是 "
        "<code>user</code>/<code>assistant</code>/<code>system</code> 三选一，而 <code>name</code> "
        "区分<strong>具体是谁</strong>。多 agent 协作时，会有许多 role 同为 <code>assistant</code> "
        "但 <code>name</code> 不同的消息；另有 <code>metadata</code> 字典可挂任意附加信息。",
        "<code>name</code> and <code>role</code> differ: <code>role</code> is only one of "
        "<code>user</code>/<code>assistant</code>/<code>system</code>, while <code>name</code> "
        "identifies <strong>who exactly</strong>. In multi-agent work many messages share role "
        "<code>assistant</code> but differ by <code>name</code>; a <code>metadata</code> dict "
        "carries arbitrary extra info.",
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
        ("<code>content</code> 永远是块列表；取文本用 <code>get_text_content()</code>，分发看 <code>block.type</code>。",
         "<code>content</code> is always a list of blocks; use <code>get_text_content()</code> "
         "for text and <code>block.type</code> to dispatch."),
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
    flow(
        [("发起调用", "Call model"), ("失败？自动重试 ×N", "Fail? retry ×N"),
         ("仍失败→备用模型", "Still failing → fallback"), ("ChatResponse", "ChatResponse")],
        "重试与回退都封装在统一接口内：你的业务代码不变，可靠性靠 ModelConfig 配置。",
        "Retries and fallback live inside the unified interface: your business code is unchanged; "
        "reliability is configured via ModelConfig.",
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
        [("厂商", "Vendor"), ("类", "Class")],
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
    tip(
        "生产可靠性：通过 <code>Agent(model_config=ModelConfig(max_retries=2, "
        "fallback_model=backup))</code> 配置<strong>重试</strong>与<strong>降级到备用模型</strong>，"
        "无需改业务代码。",
        "Production reliability: configure <strong>retries</strong> and a "
        "<strong>fallback model</strong> via <code>Agent(model_config=ModelConfig("
        "max_retries=2, fallback_model=backup))</code> — no business-code change.",
    ),
    h2("深入：流式与一次性调用", "Deeper: streaming vs one-shot calls"),
    p(
        "聊天模型有一个 <code>stream</code> 属性（<strong>默认 True</strong>）。直接调用模型时："
        "流式返回一个 <strong>async generator</strong>，逐块产出 <code>ChatResponse</code>，每块带 "
        "<code>is_last</code>、内容随产随增；非流式则直接返回<strong>单个</strong> "
        "<code>ChatResponse</code>。",
        "A chat model has a <code>stream</code> attribute (<strong>default True</strong>). When "
        "you call the model directly: streaming returns an <strong>async generator</strong> "
        "yielding <code>ChatResponse</code> chunks (each with <code>is_last</code>, content "
        "growing as it arrives); non-streaming returns a <strong>single</strong> "
        "<code>ChatResponse</code>.",
    ),
    table(
        [("<code>stream</code>", "<code>stream</code>"), ("调用返回", "The call returns"),
         ("如何取最终结果", "Getting the final result")],
        [
            [("<code>True</code>（默认）", "<code>True</code> (default)"),
             ("<code>AsyncGenerator[ChatResponse]</code>", "<code>AsyncGenerator[ChatResponse]</code>"),
             ("<code>async for</code> 直到 <code>chunk.is_last</code>",
              "<code>async for</code> until <code>chunk.is_last</code>")],
            [("<code>False</code>", "<code>False</code>"),
             ("单个 <code>ChatResponse</code>", "a single <code>ChatResponse</code>"),
             ("直接读 <code>resp.content</code>", "read <code>resp.content</code> directly")],
        ],
    ),
    code(
        "model = DashScopeChatModel(..., stream=True)\n"
        "async for chunk in model(messages, tools=tool_schemas):\n"
        "    # chunk.content 随产随增；chunk.usage 是 ChatUsage\n"
        "    if chunk.is_last:\n"
        "        final = chunk          # 最后一块含完整内容 / last chunk has full content\n"
        "print(final.usage.input_tokens, final.usage.output_tokens, final.usage.time)",
        cap_zh="流式直调：累积到 is_last；usage 给出 token 数与耗时。",
        cap_en="Direct streaming call: accumulate until is_last; usage gives tokens and time.",
    ),
    important(
        "区分两层「流式」：<strong>模型层</strong>流式产出的是 <code>ChatResponse</code> 块（本课）；"
        "<strong>Agent 层</strong>的 <code>reply_stream</code> 产出的是<strong>类型化事件</strong>"
        "（第 9 / 10 课）。后者是把前者再加工成 UI 友好的事件流——别把两者混为一谈。",
        "Two layers of \"streaming\": the <strong>model layer</strong> streams "
        "<code>ChatResponse</code> chunks (this lesson); the <strong>agent layer</strong>'s "
        "<code>reply_stream</code> streams <strong>typed events</strong> (lessons 9/10). The "
        "latter refines the former into a UI-friendly event stream — don't conflate them.",
    ),
    note(
        "只有传入 <code>tools=</code>（一组工具的函数规格，内含参数 JSON schema）时，模型才可能产出 "
        "<code>ToolCallBlock</code>；<code>tool_choice</code> 可进一步约束「自动 / 禁用 / 必须 / 指定某个」工具。",
        "A model only emits <code>ToolCallBlock</code>s when you pass <code>tools=</code> (a list "
        "of function specs, each wrapping a parameter JSON schema); <code>tool_choice</code> can "
        "further constrain \"auto / none / required / a specific\" tool.",
    ),
    source_map([
        ("model/_base.py", "<code>ChatModelBase</code> 统一接口",
         "<code>ChatModelBase</code> unified interface"),
        ("model/_model_response.py", "<code>ChatResponse</code> / <code>StructuredResponse</code>",
         "<code>ChatResponse</code> / <code>StructuredResponse</code>"),
        ("model/_dashscope/_model.py", "<code>DashScopeChatModel</code> 等厂商实现",
         "<code>DashScopeChatModel</code> and other vendor implementations"),
    ]),
    keypoints([
        ("所有模型继承 <code>ChatModelBase</code>，接口统一。",
         "All models subclass <code>ChatModelBase</code> with a unified interface."),
        ("调用返回 <code>ChatResponse</code>（内容块 + <code>ChatUsage</code>）。",
         "A call returns a <code>ChatResponse</code> (content blocks + <code>ChatUsage</code>)."),
        ("换厂商基本只改模型类与配置。",
         "Switching vendors is mostly changing the model class + config."),
        ("模型默认 <code>stream=True</code>，直调返回 async generator（块带 <code>is_last</code>）。",
         "Models default to <code>stream=True</code>; a direct call returns an async generator "
         "(chunks carry <code>is_last</code>)."),
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
    flow(
        [("环境变量 / 密钥库", "Env var / secret store"), ("Credential 对象", "Credential object"),
         ("注入 ChatModel", "Inject into ChatModel"), ("调用时用于鉴权", "Used to authenticate")],
        "密钥与模型配置分离：配置可公开，密钥单独保管、运行时才注入——绝不写进源码。",
        "Secrets are decoupled from model config: config can be public, the secret is held "
        "separately and injected at runtime — never in source.",
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
    h2("多厂商凭证 + 环境变量模式", "Credentials across vendors + the env-var pattern"),
    table(
        [("厂商", "Vendor"), ("凭证类", "Credential class")],
        [
            [("DashScope", "DashScope"), ("<code>DashScopeCredential</code>", "<code>DashScopeCredential</code>")],
            [("OpenAI", "OpenAI"), ("<code>OpenAICredential</code>", "<code>OpenAICredential</code>")],
            [("Anthropic", "Anthropic"), ("<code>AnthropicCredential</code>", "<code>AnthropicCredential</code>")],
            [("Gemini / DeepSeek / Moonshot / XAI / Ollama", "Gemini / DeepSeek / Moonshot / XAI / Ollama"),
             ("<code>GeminiCredential</code> 等", "<code>GeminiCredential</code>, etc.")],
        ],
    ),
    accordion(
        "推荐：环境变量 / .env 模式",
        "Recommended: the env-var / .env pattern",
        blocks(
            p(
                "把密钥放进环境变量（或 <code>.env</code> 文件 + 加载器），代码只读取、绝不写死。"
                "这样同一份代码在开发 / 测试 / 生产用不同的 key，且 key 永远不进版本库。",
                "Put keys in environment variables (or a <code>.env</code> file + loader); code only "
                "reads them, never hardcodes. The same code then uses different keys across "
                "dev / test / prod, and keys never enter version control.",
            ),
            code(
                "# .env（加入 .gitignore，切勿提交）\n"
                "DASHSCOPE_API_KEY=sk-xxxxxxxx\n",
                lang="bash",
            ),
            code(
                "import os\n"
                "from agentscope.credential import DashScopeCredential\n\n"
                "cred = DashScopeCredential(api_key=os.environ[\"DASHSCOPE_API_KEY\"])\n"
                "# 配置驱动的场景可用 CredentialFactory 按「类型 + 字段」批量创建凭证",
                cap_zh="从环境变量读取；多凭证可用 CredentialFactory 统一创建。",
                cap_en="Read from the environment; CredentialFactory can create many by type.",
            ),
        ),
        num=1,
    ),
    tip(
        "解耦带来的实际好处：<strong>轮换</strong>（换 key 不动模型代码）、<strong>最小权限</strong>"
        "（每个环境 / 服务独立 key）、<strong>可观测</strong>（按凭证统计用量）。这些都建立在"
        "「密钥不在代码里」的前提上。",
        "What decoupling buys you: <strong>rotation</strong> (swap a key without touching model "
        "code), <strong>least privilege</strong> (a separate key per env / service), and "
        "<strong>observability</strong> (usage attributed per credential) — all premised on "
        "\"keys are not in the code\".",
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
    flow(
        [("写普通函数", "Write a function"), ("注册进 Toolkit", "Register in Toolkit"),
         ("自动生成 schema", "Auto schema"), ("模型据此选择调用", "Model picks &amp; calls"),
         ("执行得到结果", "Execute"), ("结果回灌上下文", "Result → context")],
        "你只写函数；schema 自动生成，模型据此决定调用，结果再观察回对话——无需手写工具描述。",
        "You only write the function; the schema is generated, the model decides the call, and "
        "results flow back into context — no hand-written tool descriptions.",
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
        ("<code>Toolkit</code> 注册管理工具，并自动从签名 + docstring 生成 JSON schema。",
         "<code>Toolkit</code> registers tools and auto-generates JSON schemas from "
         "signature + docstring."),
        ("内置工具：<code>Bash/Read/Write/Edit/Grep/Glob</code>。",
         "Built-ins: <code>Bash/Read/Write/Edit/Grep/Glob</code>."),
        ("模型选定后，<code>Toolkit</code> 负责实际执行对应工具并回收结果。",
         "Once the model chooses, the <code>Toolkit</code> executes the tool and collects "
         "the result."),
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
    h2("三种驱动方式：reply / reply_stream / observe",
       "Three ways to drive it: reply / reply_stream / observe"),
    table(
        [("方法", "Method"), ("产生回复？", "Produces a reply?"), ("返回", "Returns")],
        [
            [("<code>await agent.reply(msg)</code>", "<code>await agent.reply(msg)</code>"),
             ("会（跑完整 ReAct 循环）", "yes (runs the full ReAct loop)"),
             ("最终 <code>AssistantMsg</code>", "the final <code>AssistantMsg</code>")],
            [("<code>async for e in agent.reply_stream(msg)</code>",
              "<code>async for e in agent.reply_stream(msg)</code>"),
             ("会（同一循环，边跑边播）", "yes (same loop, streamed)"),
             ("逐个<strong>事件</strong>（第 10 课）", "<strong>events</strong> one by one (lesson 10)")],
            [("<code>await agent.observe(msgs)</code>", "<code>await agent.observe(msgs)</code>"),
             ("<strong>不会</strong>", "<strong>no</strong>"),
             ("<code>None</code>（只写入记忆）", "<code>None</code> (records to memory only)")],
        ],
    ),
    important(
        "三者都是 <strong>async</strong>：<code>reply</code> / <code>observe</code> 要 "
        "<code>await</code>，<code>reply_stream</code> 要 <code>async for</code>。漏掉会拿到一个"
        "协程 / 异步生成器对象，而不是结果。",
        "All three are <strong>async</strong>: <code>await</code> <code>reply</code> / "
        "<code>observe</code>, and <code>async for</code> over <code>reply_stream</code>. Forget "
        "it and you get a coroutine / async-generator object, not a result.",
    ),
    note(
        "Agent 是<strong>有状态</strong>的：每次 <code>reply</code> 都会把这一轮消息并入记忆，"
        "所以下一次调用记得上文。<code>observe</code> 用来<strong>预置上下文</strong>"
        "（背景资料、其他 agent 的发言）而不触发回复——「先喂料，稍后再问」。",
        "An agent is <strong>stateful</strong>: each <code>reply</code> folds the turn's messages "
        "into memory, so the next call remembers the context. Use <code>observe</code> to "
        "<strong>pre-load context</strong> (background, other agents' messages) without producing "
        "a reply — \"feed first, ask later\".",
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
    keypoints([
        ("<code>Agent</code> = name + system_prompt + model + toolkit。",
         "<code>Agent</code> = name + system_prompt + model + toolkit."),
        ("它运行 ReAct（推理-行动）循环，自动编排工具调用。",
         "It runs a ReAct (reason-act) loop, orchestrating tool calls automatically."),
        ("<code>reply</code> 要结果，<code>reply_stream</code> 要过程。",
         "<code>reply</code> for the result, <code>reply_stream</code> for the process."),
        ("<code>observe</code> 只写入记忆、不回复；三个方法都是 async。",
         "<code>observe</code> only records to memory and doesn't reply; all three are async."),
    ]),
)


LESSONS = {
    "04-messages.html": LESSON_04,
    "05-chat-models.html": LESSON_05,
    "06-credentials.html": LESSON_06,
    "07-tools.html": LESSON_07,
    "08-agents-intro.html": LESSON_08,
}


QUIZZES: dict = {}

QUIZZES["04-messages.html"] = [
    (
        "关于 <code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code>，哪一项正确？",
        "Which statement about <code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code> is correct?",
        [
            ("它们是 <code>Msg</code> 的三个子类，可用 <code>isinstance</code> 区分",
             "They are three subclasses of <code>Msg</code>, distinguishable via <code>isinstance</code>", False),
            ("它们是三种字段互不相同的独立消息类",
             "They are three independent message classes with different fields", False),
            ("它们是工厂函数，都返回同一个 <code>Msg</code> 类，只是 <code>role</code> 不同",
             "They are factory functions that all return the same <code>Msg</code> class, differing only in <code>role</code>", True),
        ],
        "三者都是<strong>工厂函数</strong>，返回的都是同一个 <code>Msg</code>（仅 <code>role</code> 不同），不是子类——<code>isinstance(m, UserMsg)</code> 并不成立。",
        "All three are <strong>factory functions</strong> returning the same <code>Msg</code> (only <code>role</code> differs), not subclasses — <code>isinstance(m, UserMsg)</code> would not work.",
    ),
]

QUIZZES["05-chat-models.html"] = [
    (
        "直接调用一个 <code>ChatModelBase</code> 模型，返回的是什么？",
        "When you call a <code>ChatModelBase</code> model directly, what comes back?",
        [
            ("一个纯文本字符串", "A plain text string", False),
            ("一条最终的 <code>AssistantMsg</code>", "A final <code>AssistantMsg</code>", False),
            ("一个 <code>ChatResponse</code>：内容块（文本/思考/工具调用）加 token 用量",
             "A <code>ChatResponse</code>: content blocks (text / thinking / tool calls) plus token usage", True),
        ],
        "模型调用返回 <code>ChatResponse</code>（内容块 + <code>ChatUsage</code> 用量），不是字符串；把它整理成 <code>AssistantMsg</code> 是 <code>Agent</code> 的事。",
        "A model call returns a <code>ChatResponse</code> (content blocks + <code>ChatUsage</code>), not a string; turning it into an <code>AssistantMsg</code> is the <code>Agent</code>'s job.",
    ),
]

QUIZZES["06-credentials.html"] = [
    (
        "把<strong>凭证（Credential）</strong>从模型配置里分离出来，主要好处是什么？",
        "What is the main benefit of separating the <strong>credential</strong> from the model config?",
        [
            ("这样就能把密钥安全地硬编码进凭证对象里",
             "So the key can be safely hardcoded into the credential object", False),
            ("密钥可独立保管与轮换，同一份模型配置能在多环境复用",
             "Secrets can be held and rotated independently, and one model config reused across environments", True),
            ("凭证会自动帮你选择最便宜的模型",
             "The credential auto-selects the cheapest model for you", False),
        ],
        "解耦让密钥单独保管、便于轮换，并能在多环境复用同一模型配置——但密钥仍应从环境变量 / 密钥库读取，<strong>绝不</strong>硬编码（写进凭证对象也不行）。",
        "Decoupling lets secrets be held separately, rotated, and reused across environments — but keys should still come from env vars / a secret store and be <strong>never</strong> hardcoded (not even into the credential object).",
    ),
]

QUIZZES["07-tools.html"] = [
    (
        "用 <code>FunctionTool</code> 把一个 Python 函数变成工具时，模型看到的「工具说明」来自哪里？",
        "When you wrap a Python function as a tool with <code>FunctionTool</code>, where does the model's \u201ctool spec\u201d come from?",
        [
            ("函数的<strong>签名 + 类型注解 + docstring</strong>，由 <code>Toolkit</code> 自动生成 JSON schema",
             "The function's <strong>signature + type hints + docstring</strong>, auto-generated into a JSON schema by <code>Toolkit</code>", True),
            ("你必须手写一份 JSON schema 再注册进去",
             "You must hand-write a JSON schema and register it", False),
            ("只取函数名，参数说明会被忽略",
             "Just the function name; parameter docs are ignored", False),
        ],
        "<code>FunctionTool</code> 从签名 / 类型注解推断参数，从 docstring 提取描述，自动生成 schema——所以<strong>清晰的类型注解和 docstring 直接决定模型能否正确调用</strong>。",
        "<code>FunctionTool</code> infers parameters from the signature / type hints and the description from the docstring to auto-build the schema — so <strong>clear type hints and docstrings directly determine whether the model calls the tool correctly</strong>.",
    ),
]

QUIZZES["08-agents-intro.html"] = [
    (
        "你想先把一段背景资料「喂」给 agent、记进对话历史，但<strong>这一步先别让它回复</strong>。该用哪个方法？",
        "You want to feed the agent some background and record it in the conversation, but "
        "<strong>without making it reply yet</strong>. Which method do you use?",
        [
            ("<code>agent.observe(msgs)</code>——只把消息写入记忆/历史，不触发回复",
             "<code>agent.observe(msgs)</code> — records messages into memory/history, no reply", True),
            ("<code>agent.reply(msg)</code>——它会记录消息但不会生成回复",
             "<code>agent.reply(msg)</code> — it records the message but doesn't generate a reply", False),
            ("<code>agent.reply_stream(msg)</code>——流式模式下只记录、不回复",
             "<code>agent.reply_stream(msg)</code> — in streaming mode it only records, no reply", False),
        ],
        "三个方法别混：<code>reply</code> 返回最终 <code>AssistantMsg</code>，<code>reply_stream</code> 流式产出"
        "事件，<code>observe</code> 则<strong>只把消息并入记忆而不回复</strong>——常用于「先给上下文，稍后再让它答」。",
        "Don't conflate the three: <code>reply</code> returns the final <code>AssistantMsg</code>, "
        "<code>reply_stream</code> streams events, and <code>observe</code> <strong>only folds messages "
        "into memory without replying</strong> — handy to \"give context now, ask later\".",
    ),
]
