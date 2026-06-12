"""Content for Part 8 (reference): lesson 29 — the bilingual glossary.

A concept index for the whole guide. Every row names a real AgentScope 2.0
symbol (verified against ``src/agentscope/...`` and each module's
``__init__.py`` exports) and deep-links to the lesson that introduces it.

Source-accuracy notes worth knowing while reading:
  * ``UserMsg`` / ``AssistantMsg`` / ``SystemMsg`` are *factory functions* that
    build a :class:`Msg` with a fixed role — they are not subclasses.
  * ``ContentBlock`` is a ``TypeAlias`` (the union of block types), not a class.
  * ``MessageBus`` is exported from ``agentscope.app.message_bus`` (a sub-package
    of ``app``), not from the top-level ``agentscope.app`` namespace.
  * ``ReAct loop`` is a concept (the reasoning-acting loop), backed by the
    ``Agent`` class and its ``ReActConfig`` in ``agent/_agent.py``.
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 29 — Glossary · concept index
# ---------------------------------------------------------------------------
# Rows are ordered alphabetically by symbol so the index reads like a glossary.
# Each row: (term, term), (zh one-line def, en one-line def), (zh link, en link).
_HEADERS = [
    ("术语", "Term"),
    ("一句话解释", "One-line definition"),
    ("出处课", "Lesson"),
]

_ROWS = [
    [("<code>Agent</code>", "<code>Agent</code>"),
     ("智能体核心类，编排「推理-行动」循环，把模型、工具与系统提示组合在一起。",
      "The core agent class that runs the reasoning-acting loop, combining a "
      "model, tools and a system prompt."),
     ('<a href="08-agents-intro.html">第08课</a>',
      '<a href="08-agents-intro.html">Lesson 08</a>')],

    [("<code>AgentState</code>", "<code>AgentState</code>"),
     ("可持久化的智能体状态对象，保存会话 id、记忆与任务上下文等，可存取于存储。",
      "The persistable agent state (session id, memory, task context) saved to "
      "and loaded from storage."),
     ('<a href="19-state-tasks.html">第19课</a>',
      '<a href="19-state-tasks.html">Lesson 19</a>')],

    [("<code>AssistantMsg</code>", "<code>AssistantMsg</code>"),
     ("工厂函数，创建 <code>role=\"assistant\"</code> 的 <code>Msg</code>"
      "（可含文本/思考/工具调用等块）。",
      "A factory that builds a <code>Msg</code> with "
      "<code>role=\"assistant\"</code> (text/thinking/tool-call blocks, etc.)."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>ChatModelBase</code>", "<code>ChatModelBase</code>"),
     ("聊天模型基类，为各厂商模型提供统一的调用接口。",
      "The base class that unifies all vendor chat models behind one calling "
      "interface."),
     ('<a href="05-chat-models.html">第05课</a>',
      '<a href="05-chat-models.html">Lesson 05</a>')],

    [("<code>ChatResponse</code>", "<code>ChatResponse</code>"),
     ("模型一次调用的返回，包含一串内容块（文本/工具调用/思考/数据）。",
      "A model call's response — a sequence of content blocks "
      "(text / tool-call / thinking / data)."),
     ('<a href="05-chat-models.html">第05课</a>',
      '<a href="05-chat-models.html">Lesson 05</a>')],

    [("<code>ChatUsage</code>", "<code>ChatUsage</code>"),
     ("一次模型调用的用量统计（输入/输出 token 等）。",
      "The token-usage record (input/output tokens) for a single model call."),
     ('<a href="05-chat-models.html">第05课</a>',
      '<a href="05-chat-models.html">Lesson 05</a>')],

    [("<code>ContentBlock</code>", "<code>ContentBlock</code>"),
     ("类型别名，所有消息内容块类型的联合（文本/思考/提示/工具调用/工具结果/数据）。",
      "A type alias — the union of all message content block types "
      "(text/thinking/hint/tool-call/tool-result/data)."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>create_app</code>", "<code>create_app</code>"),
     ("服务工厂函数，用存储、消息总线与工作区管理器组装出 FastAPI 智能体服务。",
      "A factory that assembles the FastAPI agent service from storage, a "
      "message bus and a workspace manager."),
     ('<a href="23-agent-service.html">第23课</a>',
      '<a href="23-agent-service.html">Lesson 23</a>')],

    [("<code>CredentialBase</code>", "<code>CredentialBase</code>"),
     ("凭证基类，管理 API key/密钥，与模型配置解耦。",
      "The base class for API keys/secrets, decoupled from model "
      "configuration."),
     ('<a href="06-credentials.html">第06课</a>',
      '<a href="06-credentials.html">Lesson 06</a>')],

    [("<code>CredentialFactory</code>", "<code>CredentialFactory</code>"),
     ("凭证注册表与反序列化器，按类型从配置重建 <code>CredentialBase</code> 子类。",
      "A registry/deserializer that reconstructs <code>CredentialBase</code> "
      "subclasses from config."),
     ('<a href="06-credentials.html">第06课</a>',
      '<a href="06-credentials.html">Lesson 06</a>')],

    [("<code>DataBlock</code>", "<code>DataBlock</code>"),
     ("二进制内容块，承载图像/音频/视频等数据（base64 或 URL 来源）。",
      "A content block carrying binary data (image/audio/video) via a base64 "
      "or URL source."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>DockerWorkspace</code>", "<code>DockerWorkspace</code>"),
     ("在 Docker 容器中执行工具的工作区后端。",
      "A workspace backend that executes tools inside a Docker container."),
     ('<a href="17-workspace.html">第17课</a>',
      '<a href="17-workspace.html">Lesson 17</a>')],

    [("<code>E2BWorkspace</code>", "<code>E2BWorkspace</code>"),
     ("在 E2B 云沙箱中执行工具的工作区后端。",
      "A workspace backend that executes tools inside an E2B cloud sandbox."),
     ('<a href="17-workspace.html">第17课</a>',
      '<a href="17-workspace.html">Lesson 17</a>')],

    [("<code>EmbeddingCacheBase</code>", "<code>EmbeddingCacheBase</code>"),
     ("嵌入缓存基类，存取嵌入向量以避免重复计算。",
      "The base class for caching embedding vectors to avoid recomputation."),
     ('<a href="21-embeddings.html">第21课</a>',
      '<a href="21-embeddings.html">Lesson 21</a>')],

    [("<code>EmbeddingModelBase</code>", "<code>EmbeddingModelBase</code>"),
     ("嵌入模型基类，是检索/RAG 的基础。",
      "The base class for embedding models — the foundation for "
      "retrieval/RAG."),
     ('<a href="21-embeddings.html">第21课</a>',
      '<a href="21-embeddings.html">Lesson 21</a>')],

    [("<code>EventType</code>", "<code>EventType</code>"),
     ("字符串枚举，列举智能体事件流中的所有事件类型。",
      "A string enum naming every event emitted on the agent's stream."),
     ('<a href="09-event-system.html">第09课</a>',
      '<a href="09-event-system.html">Lesson 09</a>')],

    [("<code>FormatterBase</code>", "<code>FormatterBase</code>"),
     ("格式化器基类，把 <code>Msg</code> 列表转换成各厂商要求的请求格式。",
      "The base class that turns a <code>Msg</code> list into each vendor's "
      "request format."),
     ('<a href="11-formatter.html">第11课</a>',
      '<a href="11-formatter.html">Lesson 11</a>')],

    [("<code>FunctionTool</code>", "<code>FunctionTool</code>"),
     ("适配器，把普通 Python 函数包装成工具，并据签名自动生成 schema。",
      "An adapter that wraps a plain Python function as a tool, auto-deriving "
      "its schema from the signature."),
     ('<a href="07-tools.html">第07课</a>',
      '<a href="07-tools.html">Lesson 07</a>')],

    [("<code>HttpMCPConfig</code>", "<code>HttpMCPConfig</code>"),
     ("描述以 HTTP 方式连接 MCP 服务器的配置。",
      "Configuration describing an HTTP-based MCP server connection."),
     ('<a href="18-mcp.html">第18课</a>',
      '<a href="18-mcp.html">Lesson 18</a>')],

    [("<code>LocalSkillLoader</code>", "<code>LocalSkillLoader</code>"),
     ("从本地目录加载技能的技能加载器。",
      "A skill loader that loads skills from a local directory."),
     ('<a href="20-skills.html">第20课</a>',
      '<a href="20-skills.html">Lesson 20</a>')],

    [("<code>LocalWorkspace</code>", "<code>LocalWorkspace</code>"),
     ("直接在本地文件系统上执行工具的工作区后端。",
      "A workspace backend that executes tools directly on the local "
      "filesystem."),
     ('<a href="17-workspace.html">第17课</a>',
      '<a href="17-workspace.html">Lesson 17</a>')],

    [("<code>MCPClient</code>", "<code>MCPClient</code>"),
     ("统一的 MCP 客户端，连接 MCP 服务器并暴露其工具。",
      "The unified client for connecting to MCP servers and exposing their "
      "tools."),
     ('<a href="18-mcp.html">第18课</a>',
      '<a href="18-mcp.html">Lesson 18</a>')],

    [("<code>MCPTool</code>", "<code>MCPTool</code>"),
     ("适配器，把远端 MCP 工具适配为符合工具协议的工具。",
      "An adapter that exposes a remote MCP tool through the tool protocol."),
     ('<a href="18-mcp.html">第18课</a>',
      '<a href="18-mcp.html">Lesson 18</a>')],

    [("<code>MessageBus</code>", "<code>MessageBus</code>"),
     ("跨会话消息的实时传输抽象基类（队列消费/回放/广播），"
      "从 <code>agentscope.app.message_bus</code> 导出。",
      "An abstract live transport for cross-session messages "
      "(drain/replay/broadcast); exported from "
      "<code>agentscope.app.message_bus</code>."),
     ('<a href="24-message-bus.html">第24课</a>',
      '<a href="24-message-bus.html">Lesson 24</a>')],

    [("<code>MiddlewareBase</code>", "<code>MiddlewareBase</code>"),
     ("中间件基类，提供围绕回复/模型/工具生命周期的可组合钩子。",
      "The base class for composable hooks around the reply/model/tool "
      "lifecycle."),
     ('<a href="15-middleware.html">第15课</a>',
      '<a href="15-middleware.html">Lesson 15</a>')],

    [("<code>Msg</code>", "<code>Msg</code>"),
     ("核心消息对象，负责智能体之间的信息存储与传递。",
      "The core message object responsible for storing and passing information "
      "between agents."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>Offloader</code>", "<code>Offloader</code>"),
     ("协议接口，把压缩后的上下文卸载到工作区可访问的存储。",
      "A protocol for offloading compressed context to workspace-accessible "
      "storage."),
     ('<a href="17-workspace.html">第17课</a>',
      '<a href="17-workspace.html">Lesson 17</a>')],

    [("<code>ParamsBase</code>", "<code>ParamsBase</code>"),
     ("工具参数基类，导出 JSON schema 时去除 title 字段。",
      "A base class for tool parameters that removes the title field from the "
      "exported JSON schema."),
     ('<a href="07-tools.html">第07课</a>',
      '<a href="07-tools.html">Lesson 07</a>')],

    [("<code>PermissionDecision</code>", "<code>PermissionDecision</code>"),
     ("权限检查的结果（允许/拒绝/需用户确认）。",
      "The outcome of a permission check (allow / deny / require "
      "confirmation)."),
     ('<a href="16-permission.html">第16课</a>',
      '<a href="16-permission.html">Lesson 16</a>')],

    [("<code>PermissionEngine</code>", "<code>PermissionEngine</code>"),
     ("权限引擎，按权限规则评估并执行工具调用请求。",
      "The engine that evaluates tool requests against permission rules and "
      "enforces them."),
     ('<a href="16-permission.html">第16课</a>',
      '<a href="16-permission.html">Lesson 16</a>')],

    [("<code>PermissionContext</code>", "<code>PermissionContext</code>"),
     ("承载权限模式与规则的上下文；存于 <code>AgentState</code>（设 bypass 模式即在此）。",
      "The context holding the permission mode and rules; lives on "
      "<code>AgentState</code> (set bypass mode here)."),
     ('<a href="16-permission.html">第16课</a>',
      '<a href="16-permission.html">Lesson 16</a>')],

    [("<code>PermissionMode</code>", "<code>PermissionMode</code>"),
     ("枚举，选择整体权限策略（如默认/最严格等模式）。",
      "An enum selecting the overall permission strategy (e.g. default / "
      "most-secure)."),
     ('<a href="16-permission.html">第16课</a>',
      '<a href="16-permission.html">Lesson 16</a>')],

    [("<code>PermissionRule</code>", "<code>PermissionRule</code>"),
     ("权限规则，决定某个工具/操作是允许、拒绝还是需要确认。",
      "A rule deciding whether a specific tool/operation is allowed, denied or "
      "needs confirmation."),
     ('<a href="16-permission.html">第16课</a>',
      '<a href="16-permission.html">Lesson 16</a>')],

    [("<code>ReAct loop</code>（概念）", "<code>ReAct loop</code> (concept)"),
     ("「推理-行动」循环：智能体在推理（模型）与行动（工具）间交替，直到给出最终答案。",
      "The reason-act cycle: the agent alternates reasoning (model) and acting "
      "(tools) until it produces a final answer."),
     ('<a href="03-lifecycle.html">第03课</a>',
      '<a href="03-lifecycle.html">Lesson 03</a>')],

    [("<code>Skill</code>", "<code>Skill</code>"),
     ("可打包复用的智能体能力单元。",
      "A packaged, reusable capability that an agent can load and use."),
     ('<a href="20-skills.html">第20课</a>',
      '<a href="20-skills.html">Lesson 20</a>')],

    [("<code>StdioMCPConfig</code>", "<code>StdioMCPConfig</code>"),
     ("描述以 stdio（子进程）方式连接 MCP 服务器的配置。",
      "Configuration describing a stdio (subprocess) MCP server connection."),
     ('<a href="18-mcp.html">第18课</a>',
      '<a href="18-mcp.html">Lesson 18</a>')],

    [("<code>StructuredResponse</code>", "<code>StructuredResponse</code>"),
     ("结构化模型响应，其内容是一个结构化字典（如 JSON 对象）。",
      "A model response whose content is a structured dict (e.g. a JSON "
      "object)."),
     ('<a href="05-chat-models.html">第05课</a>',
      '<a href="05-chat-models.html">Lesson 05</a>')],

    [("<code>SubAgentTemplate</code>", "<code>SubAgentTemplate</code>"),
     ("可复用的子智能体蓝图，用于在团队中创建子智能体。",
      "A reusable blueprint for creating sub-agents within a team."),
     ('<a href="25-agent-team.html">第25课</a>',
      '<a href="25-agent-team.html">Lesson 25</a>')],

    [("团队工具 <code>TeamCreate/AgentCreate/TeamSay/TeamDelete</code>",
      "Team tools <code>TeamCreate/AgentCreate/TeamSay/TeamDelete</code>"),
     ("领导 agent 用来组队的内置工具：建队、按模板生成队员、向队员发消息、解散。",
      "Built-in tools a leader agent uses to form a team: create a team, spawn a "
      "worker from a template, message a teammate, disband."),
     ('<a href="25-agent-team.html">第25课</a>',
      '<a href="25-agent-team.html">Lesson 25</a>')],

    [("<code>AgentOrientedException</code> / <code>DeveloperOrientedException</code>",
      "<code>AgentOrientedException</code> / <code>DeveloperOrientedException</code>"),
     ("工具错误的两种基类：前者回喂给模型让其自纠，后者抛给开发者。",
      "The two tool-error base classes: the former is fed back to the model to "
      "self-correct; the latter propagates to the developer."),
     ('<a href="26-custom-tools.html">第26课</a>',
      '<a href="26-custom-tools.html">Lesson 26</a>')],

    [("<code>SystemMsg</code>", "<code>SystemMsg</code>"),
     ("工厂函数，创建 <code>role=\"system\"</code> 的 <code>Msg</code>。",
      "A factory that builds a <code>Msg</code> with "
      "<code>role=\"system\"</code>."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>Task</code>", "<code>Task</code>"),
     ("描述单个智能体任务的对象（含主题等字段）。",
      "A model describing a single agent task (subject, etc.)."),
     ('<a href="19-state-tasks.html">第19课</a>',
      '<a href="19-state-tasks.html">Lesson 19</a>')],

    [("<code>TaskContext</code>", "<code>TaskContext</code>"),
     ("任务上下文，保存会话中跟踪的一组 <code>Task</code>。",
      "The task context holding the list of <code>Task</code>s tracked in a "
      "session."),
     ('<a href="19-state-tasks.html">第19课</a>',
      '<a href="19-state-tasks.html">Lesson 19</a>')],

    [("<code>TextBlock</code>", "<code>TextBlock</code>"),
     ("文本内容块，承载纯文本（type 为 \"text\"）。",
      "A content block holding plain text (its type is \"text\")."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>ThinkingBlock</code>", "<code>ThinkingBlock</code>"),
     ("思考内容块，承载模型的推理/思考文本。",
      "A content block holding the model's reasoning/thinking text."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>ToolBase</code>", "<code>ToolBase</code>"),
     ("工具协议基类，定义名称、描述、输入 schema 与执行约定。",
      "The tool protocol defining a tool's name, description, input schema and "
      "execution contract."),
     ('<a href="07-tools.html">第07课</a>',
      '<a href="07-tools.html">Lesson 07</a>')],

    [("<code>ToolCallBlock</code>", "<code>ToolCallBlock</code>"),
     ("工具调用块，表示模型请求调用某个工具（含名称与参数）。",
      "A content block representing the model's request to call a tool (name "
      "and arguments)."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>ToolGroup</code>", "<code>ToolGroup</code>"),
     ("一组相关工具/MCP/技能的集合，可被智能体整体激活（由 <code>ResetTools</code> 元工具触发）。",
      "A named bundle of tools/MCPs/skills an agent can activate together "
      "(via the <code>ResetTools</code> meta tool)."),
     ('<a href="13-toolkit-internals.html">第13课</a>',
      '<a href="13-toolkit-internals.html">Lesson 13</a>')],

    [("<code>Toolkit</code>", "<code>Toolkit</code>"),
     ("核心模块，注册、管理并调用工具、MCP 客户端与技能。",
      "The core module to register, manage and call tools, MCP clients and "
      "skills."),
     ('<a href="07-tools.html">第07课</a>',
      '<a href="07-tools.html">Lesson 07</a>')],

    [("<code>ToolResponse</code>", "<code>ToolResponse</code>"),
     ("工具执行完成后的结果（文本/数据块及状态）。",
      "The completed result of a tool execution (text/data blocks plus "
      "state)."),
     ('<a href="07-tools.html">第07课</a>',
      '<a href="07-tools.html">Lesson 07</a>')],

    [("<code>ToolResultBlock</code>", "<code>ToolResultBlock</code>"),
     ("工具结果块，承载一次工具调用返回的结果。",
      "A content block carrying the result returned from a tool call."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>TracingMiddleware</code>", "<code>TracingMiddleware</code>"),
     ("中间件，为回复/模型/工具生命周期添加 OpenTelemetry 链路追踪。",
      "Middleware that adds OpenTelemetry tracing to the reply/model/tool "
      "lifecycles."),
     ('<a href="15-middleware.html">第15课</a>',
      '<a href="15-middleware.html">Lesson 15</a>')],

    [("<code>TTSMiddleware</code>", "<code>TTSMiddleware</code>"),
     ("中间件，为文本块合成语音，并以数据块事件注入音频。",
      "Middleware that synthesizes speech for text blocks and injects audio as "
      "data-block events."),
     ('<a href="15-middleware.html">第15课</a>',
      '<a href="15-middleware.html">Lesson 15</a>')],

    [("<code>TTSModelBase</code>", "<code>TTSModelBase</code>"),
     ("文本转语音模型基类（支持非实时与实时）。",
      "The base class for text-to-speech models (both non-realtime and "
      "realtime)."),
     ('<a href="22-tts.html">第22课</a>',
      '<a href="22-tts.html">Lesson 22</a>')],

    [("<code>UserMsg</code>", "<code>UserMsg</code>"),
     ("工厂函数，创建 <code>role=\"user\"</code> 的 <code>Msg</code>"
      "（纯字符串会自动包成 <code>TextBlock</code>）。",
      "A factory that builds a <code>Msg</code> with <code>role=\"user\"</code> "
      "(a plain string is auto-wrapped in a <code>TextBlock</code>)."),
     ('<a href="04-messages.html">第04课</a>',
      '<a href="04-messages.html">Lesson 04</a>')],

    [("<code>WorkspaceBase</code>", "<code>WorkspaceBase</code>"),
     ("工作区抽象基类，统一工具的执行后端（本地/Docker/E2B）。",
      "The abstract base for execution backends (local/Docker/E2B) where tools "
      "run."),
     ('<a href="17-workspace.html">第17课</a>',
      '<a href="17-workspace.html">Lesson 17</a>')],
]

LESSON_29 = blocks(
    lead(
        "这是一张<strong>双语术语速查表</strong>：左列是 AgentScope 2.0 的真实符号"
        "（类 / 函数 / 枚举 / 类型别名），中列给出一句话解释，右列链接到首次系统讲解它的课程。"
        "用浏览器的 <code>Ctrl/Cmd+F</code> 直接定位术语，或点右上角的语言开关切换中英文。",
        "This is a <strong>bilingual quick-reference</strong>: the left column lists "
        "real AgentScope 2.0 symbols (classes / functions / enums / type aliases), "
        "the middle gives a one-line definition, and the right links to the lesson "
        "that first explains it in depth. Use your browser's <code>Ctrl/Cmd+F</code> "
        "to jump to a term, or the language toggle (top-right) to switch languages.",
    ),
    note(
        "表中部分条目并非类：<code>UserMsg</code> / <code>AssistantMsg</code> / "
        "<code>SystemMsg</code> 是返回 <code>Msg</code> 的<strong>工厂函数</strong>，"
        "<code>ContentBlock</code> 是一个<strong>类型别名</strong>（各内容块的联合），"
        "<code>create_app</code> 是函数，而 <code>ReAct loop</code> 是一个<strong>概念</strong>"
        "（由 <code>Agent</code> 与 <code>ReActConfig</code> 落地）。",
        "A few entries aren't classes: <code>UserMsg</code> / "
        "<code>AssistantMsg</code> / <code>SystemMsg</code> are <strong>factory "
        "functions</strong> returning a <code>Msg</code>, <code>ContentBlock</code> "
        "is a <strong>type alias</strong> (the union of content blocks), "
        "<code>create_app</code> is a function, and <code>ReAct loop</code> is a "
        "<strong>concept</strong> (realized by <code>Agent</code> and "
        "<code>ReActConfig</code>).",
    ),
    table(_HEADERS, _ROWS),
    tip(
        "建议把本页当作「跳板」：遇到不熟悉的术语，先看一句话解释，再点「出处课」深入；"
        "学完一课后回到这里，能快速串起整张知识地图。",
        "Treat this page as a springboard: skim the one-line definition for any "
        "unfamiliar term, then click its lesson to go deeper; coming back after a "
        "lesson helps you stitch the whole map together.",
    ),
)


LESSONS = {
    "29-glossary.html": LESSON_29,
}


QUIZZES: dict = {}

QUIZZES["29-glossary.html"] = [
    (
        "下列哪一项不是类，而是返回 <code>Msg</code> 的工厂函数？",
        "Which of these is not a class, but a factory function that returns a <code>Msg</code>?",
        [
            ("<code>UserMsg</code>", "<code>UserMsg</code>", True),
            ("<code>Msg</code>（消息核心类本身）",
             "<code>Msg</code> (the core message class itself)", False),
            ("<code>ContentBlock</code>", "<code>ContentBlock</code>", False),
        ],
        "<code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code> 是工厂函数，"
        "按固定 role 构造一个 <code>Msg</code>；<code>Msg</code> 是它们返回的核心类，而 "
        "<code>ContentBlock</code> 既不是类也不是工厂，而是各内容块类型的联合（类型别名）。",
        "<code>UserMsg</code> / <code>AssistantMsg</code> / <code>SystemMsg</code> are factory "
        "functions that build a <code>Msg</code> with a fixed role; <code>Msg</code> is the core "
        "class they return, while <code>ContentBlock</code> is neither a class nor a factory but "
        "a type alias (the union of content-block types).",
    ),
    (
        "<code>FormatterBase</code> 的职责是什么？",
        "What is the responsibility of <code>FormatterBase</code>?",
        [
            ("把 <code>Msg</code> 列表转换成各厂商要求的请求格式",
             "Turn a <code>Msg</code> list into each vendor's request format", True),
            ("管理 API key 与密钥", "Manage API keys and secrets", False),
            ("在沙箱中执行工具", "Execute tools inside a sandbox", False),
        ],
        "<code>FormatterBase</code> 负责把统一的 <code>Msg</code> 列表适配成不同厂商的具体请求"
        "格式；管理密钥的是 <code>CredentialBase</code>，沙箱执行属于 <code>WorkspaceBase</code>。",
        "<code>FormatterBase</code> adapts the unified <code>Msg</code> list into each vendor's "
        "concrete request format; secrets are handled by <code>CredentialBase</code> and "
        "sandboxed execution by <code>WorkspaceBase</code>.",
    ),
]
