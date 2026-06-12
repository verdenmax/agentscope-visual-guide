"""Content for Part 5 (advanced capabilities): lessons 16–22.

Verified against AgentScope 2.0 source (permission/, workspace/, mcp/, state/,
skill/, embedding/, tts/).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 16 — Permission
# ---------------------------------------------------------------------------
LESSON_16 = blocks(
    lead(
        "当 agent 能执行命令、改文件时，<strong>权限系统</strong>是安全闸门。"
        "<code>PermissionEngine</code> 依据一组 <code>PermissionRule</code> 与当前 "
        "<code>PermissionMode</code>，对每次工具调用作出 <code>PermissionDecision</code>。",
        "Once an agent can run commands and edit files, the <strong>permission system</strong> "
        "is the safety gate. The <code>PermissionEngine</code> makes a "
        "<code>PermissionDecision</code> for each tool call from a set of "
        "<code>PermissionRule</code>s and the current <code>PermissionMode</code>.",
    ),
    analogy(
        "像公司的<strong>门禁与审批</strong>：有的门随便进（允许），有的要刷卡（按规则），"
        "有的必须主管点头（人工确认），紧急演练时可临时全开（bypass）。",
        "Like corporate <strong>access control</strong>: some doors are open (allow), some need "
        "a badge (rule-based), some need a manager's nod (human confirm), and during a drill you "
        "can temporarily open everything (bypass).",
    ),
    h2("决策要素", "The decision pieces"),
    table(
        [("组件", "Component"), ("职责", "Role")],
        [
            [("<code>PermissionEngine</code>", "<code>PermissionEngine</code>"),
             ("对每次调用作出裁决", "renders a decision per call")],
            [("<code>PermissionRule</code>", "<code>PermissionRule</code>"),
             ("匹配工具 / 参数的规则", "rules matching tools / arguments")],
            [("<code>PermissionMode</code> / <code>PermissionBehavior</code>",
              "<code>PermissionMode</code> / <code>PermissionBehavior</code>"),
             ("总体模式（含 bypass）与默认行为", "overall mode (incl. bypass) + default behavior")],
            [("<code>PermissionDecision</code>", "<code>PermissionDecision</code>"),
             ("放行 / 拒绝 / 需确认", "allow / deny / needs-confirm")],
            [("<code>PermissionContext</code>", "<code>PermissionContext</code>"),
             ("上下文（如附加工作目录 <code>AdditionalWorkingDirectory</code>）",
              "context (e.g. <code>AdditionalWorkingDirectory</code>)")],
        ],
    ),
    p(
        "当裁决为「需确认」时，agent 会发出 <code>REQUIRE_USER_CONFIRM</code> 事件（见第 9 课），"
        "暂停并等待人类批准——这就是 README 里「permission control」与 bypass 模式的来源。",
        "When the decision is \"needs confirm\", the agent emits a "
        "<code>REQUIRE_USER_CONFIRM</code> event (lesson 9), pausing for human approval — this "
        "is the source of the README's \"permission control\" and bypass mode.",
    ),
    h2("两种实操：放行或绕过", "Two practical paths: confirm or bypass"),
    p(
        "默认模式（<code>PermissionMode.DEFAULT</code>）下，写文件等操作会<strong>暂停等待确认</strong>："
        "<code>reply_stream</code> 发出 <code>REQUIRE_USER_CONFIRM</code> 后即结束。要继续，你需要把一个 "
        "<code>UserConfirmResultEvent</code>（含 <code>ConfirmResult</code>）<strong>回传</strong>给 "
        "<code>reply_stream</code>；或在受控场景下改用 <code>PermissionMode.BYPASS</code> 一路放行。",
        "In the default mode (<code>PermissionMode.DEFAULT</code>), operations like writing files "
        "<strong>pause for confirmation</strong>: <code>reply_stream</code> emits "
        "<code>REQUIRE_USER_CONFIRM</code> and then ends. To continue you feed a "
        "<code>UserConfirmResultEvent</code> (carrying a <code>ConfirmResult</code>) "
        "<strong>back into</strong> <code>reply_stream</code>; or, in controlled settings, use "
        "<code>PermissionMode.BYPASS</code> to allow everything.",
    ),
    code(
        "from agentscope.event import EventType, UserConfirmResultEvent, ConfirmResult\n\n"
        "async for evt in agent.reply_stream(user_msg):\n"
        "    if evt.type == EventType.REQUIRE_USER_CONFIRM:\n"
        "        # ask the human, then resume by feeding the decision back\n"
        "        results = [\n"
        "            ConfirmResult(confirmed=True, tool_call=tc)\n"
        "            for tc in evt.tool_calls\n"
        "        ]\n"
        "        async for evt2 in agent.reply_stream(\n"
        "            UserConfirmResultEvent(reply_id=evt.reply_id,\n"
        "                                   confirm_results=results)):\n"
        "            ...   # continue consuming the resumed stream",
        cap_zh="确认回路：把 UserConfirmResultEvent 回传给 reply_stream 以继续。",
        cap_en="The confirm round-trip: feed a UserConfirmResultEvent back to resume.",
    ),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.state import AgentState\n"
        "from agentscope.permission import PermissionContext, PermissionMode\n\n"
        "agent = Agent(\n"
        '    name="Friday", system_prompt="...", model=..., toolkit=...,\n'
        "    state=AgentState(\n"
        "        permission_context=PermissionContext(mode=PermissionMode.BYPASS),\n"
        "    ),\n"
        ")   # no confirmation prompts — runs end-to-end (use only when safe)",
        cap_zh="无人值守：用 BYPASS 模式跳过确认（仅在可信场景）。",
        cap_en="Unattended: BYPASS skips confirmation (only when it's safe).",
    ),
    note(
        "模式还有 <code>ACCEPT_EDITS</code>（自动允许工作目录内的读写）、<code>EXPLORE</code>、"
        "<code>DONT_ASK</code> 等，适配不同信任级别。",
        "Other modes include <code>ACCEPT_EDITS</code> (auto-allow reads/writes inside working "
        "directories), <code>EXPLORE</code> and <code>DONT_ASK</code>, for different trust levels.",
    ),
    source_map([
        ("permission/_engine.py", "<code>PermissionEngine</code>",
         "<code>PermissionEngine</code>"),
        ("permission/_rule.py", "<code>PermissionRule</code>",
         "<code>PermissionRule</code>"),
        ("permission/_types.py", "<code>PermissionMode</code> / <code>PermissionBehavior</code>",
         "<code>PermissionMode</code> / <code>PermissionBehavior</code>"),
        ("permission/_decision.py", "<code>PermissionDecision</code>",
         "<code>PermissionDecision</code>"),
        ("permission/_context.py",
         "<code>PermissionContext</code> / <code>AdditionalWorkingDirectory</code>",
         "<code>PermissionContext</code> / <code>AdditionalWorkingDirectory</code>"),
    ]),
    keypoints([
        ("<code>PermissionEngine</code> 对每次工具调用作出放行/拒绝/确认决策。",
         "<code>PermissionEngine</code> decides allow/deny/confirm per tool call."),
        ("「需确认」通过 <code>REQUIRE_USER_CONFIRM</code> 事件接入人机交互。",
         "\"Needs confirm\" plugs into human-in-the-loop via the <code>REQUIRE_USER_CONFIRM</code> event."),
        ("bypass 模式可在受控场景下端到端运行不打断。",
         "Bypass mode runs end-to-end without interruption in controlled scenarios."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 17 — Workspace & Sandbox
# ---------------------------------------------------------------------------
LESSON_17 = blocks(
    lead(
        "<strong>工作区（Workspace）</strong>是 agent 执行工具/代码的<strong>隔离环境</strong>。"
        "<code>WorkspaceBase</code> 抽象出统一接口，内置本地、Docker、E2B 三种后端；"
        "<code>Offloader</code> 负责把超长上下文 / 工具结果卸载出去。",
        "A <strong>Workspace</strong> is the <strong>isolated environment</strong> where an "
        "agent runs tools/code. <code>WorkspaceBase</code> abstracts a unified interface with "
        "built-in local, Docker and E2B backends; an <code>Offloader</code> offloads oversized "
        "context / tool results.",
    ),
    analogy(
        "像给实习生一间<strong>独立车间</strong>而不是让他在你的主控室乱动：本地车间最快，"
        "Docker 车间更隔离，E2B 是云端租来的车间。",
        "Like giving an intern a <strong>separate workshop</strong> instead of letting them "
        "loose in your control room: the local one is fastest, Docker is more isolated, and E2B "
        "is a rented cloud workshop.",
    ),
    h2("后端选择", "Choosing a backend"),
    table(
        [("后端", "Backend"), ("适用", "Use case")],
        [
            [("<code>LocalWorkspace</code>", "<code>LocalWorkspace</code>"),
             ("本地开发，最快、最简单", "local development — fastest, simplest")],
            [("<code>DockerWorkspace</code>", "<code>DockerWorkspace</code>"),
             ("容器隔离，限制副作用", "container isolation, contained side effects")],
            [("<code>E2BWorkspace</code>", "<code>E2BWorkspace</code>"),
             ("云端沙箱，弹性 / 强隔离", "cloud sandbox, elastic / strong isolation")],
        ],
    ),
    accordion(
        "Offloader 解决什么？",
        "What does the Offloader solve?",
        blocks(p(
            "长对话和大工具结果会撑爆上下文窗口。<code>Offloader</code> 把<strong>压缩后的上下文</strong>"
            "与<strong>被截断的工具结果</strong>卸载到工作区（如写入文件），需要时再取回——"
            "在「带得动」和「不丢信息」之间取得平衡。",
            "Long conversations and large tool results blow up the context window. The "
            "<code>Offloader</code> offloads <strong>compressed context</strong> and "
            "<strong>truncated tool results</strong> to the workspace (e.g. to files), fetching "
            "them back when needed — balancing \"fits in the window\" against \"loses no info\".",
        )),
        num=1,
    ),
    source_map([
        ("workspace/_base.py", "<code>WorkspaceBase</code> 统一接口",
         "<code>WorkspaceBase</code> unified interface"),
        ("workspace/_local_workspace.py", "<code>LocalWorkspace</code>",
         "<code>LocalWorkspace</code>"),
        ("workspace/_docker/_docker_workspace.py", "<code>DockerWorkspace</code>",
         "<code>DockerWorkspace</code>"),
        ("workspace/_e2b/_e2b_workspace.py", "<code>E2BWorkspace</code>",
         "<code>E2BWorkspace</code>"),
        ("workspace/_offload_protocol.py", "<code>Offloader</code> 协议",
         "the <code>Offloader</code> protocol"),
    ]),
    keypoints([
        ("工作区为工具/代码执行提供<strong>隔离环境</strong>。",
         "A workspace provides an <strong>isolated environment</strong> for tool/code execution."),
        ("三种后端：本地 / Docker / E2B，接口统一可替换。",
         "Three backends — local / Docker / E2B — behind one swappable interface."),
        ("<code>Offloader</code> 卸载超长上下文与工具结果。",
         "The <code>Offloader</code> offloads oversized context and tool results."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 18 — MCP
# ---------------------------------------------------------------------------
LESSON_18 = blocks(
    lead(
        "<strong>MCP（Model Context Protocol）</strong>是连接外部工具服务器的标准协议。"
        "<code>MCPClient</code> 连上一个 MCP 服务器，把它提供的工具<strong>变成 AgentScope 工具</strong>，"
        "直接注册进 <code>Toolkit</code>。",
        "<strong>MCP (Model Context Protocol)</strong> is a standard for connecting to external "
        "tool servers. An <code>MCPClient</code> connects to an MCP server and turns its tools "
        "<strong>into AgentScope tools</strong> you register straight into a <code>Toolkit</code>.",
    ),
    analogy(
        "像给工具箱接上一个<strong>外部供应商目录</strong>：你不必自己造每件工具，连上供应商"
        "（MCP 服务器）就能直接调用他们的工具。",
        "Like plugging an <strong>external supplier catalog</strong> into your toolbox: instead "
        "of building every tool yourself, connect to a supplier (MCP server) and call their "
        "tools directly.",
    ),
    h2("连接与暴露", "Connect and expose"),
    code(
        "from agentscope.mcp import MCPClient, StdioMCPConfig, HttpMCPConfig\n"
        "from agentscope.tool import Toolkit\n\n"
        "# stdio server (a local process) or http server (a remote endpoint)\n"
        "client = MCPClient(StdioMCPConfig(...))   # or MCPClient(HttpMCPConfig(...))\n"
        "await client.connect()\n\n"
        "# expose the server's tools through a Toolkit\n"
        "toolkit = Toolkit(mcps=[client])\n"
        "tools = await client.list_tools()         # -> list[ToolBase]",
        cap_zh="连接 MCP 服务器并把其工具注册进 Toolkit。",
        cap_en="Connect to an MCP server and register its tools into a Toolkit.",
    ),
    p(
        "两种配置：<code>StdioMCPConfig</code>（启动本地子进程，通过 stdio 通信）与 "
        "<code>HttpMCPConfig</code>（连接远程 HTTP 端点）。这些外部工具在 Toolkit 内表现为 "
        "<code>MCPTool</code>，同样受权限系统管控。",
        "Two configs: <code>StdioMCPConfig</code> (spawn a local subprocess, talk over stdio) "
        "and <code>HttpMCPConfig</code> (connect to a remote HTTP endpoint). Inside the Toolkit "
        "these external tools appear as <code>MCPTool</code> and are gated by the permission "
        "system just the same.",
    ),
    source_map([
        ("mcp/_mcp_client.py",
         "<code>MCPClient</code>：<code>connect</code> / <code>list_tools</code> / "
         "<code>get_tool</code> / <code>close</code>",
         "<code>MCPClient</code>: <code>connect</code> / <code>list_tools</code> / "
         "<code>get_tool</code> / <code>close</code>"),
        ("mcp/_config.py", "<code>StdioMCPConfig</code> / <code>HttpMCPConfig</code>",
         "<code>StdioMCPConfig</code> / <code>HttpMCPConfig</code>"),
        ("tool/_adapters.py", "<code>MCPTool</code>（MCP 工具适配器）",
         "<code>MCPTool</code> (the MCP tool adapter)"),
    ]),
    keypoints([
        ("<code>MCPClient</code> 把外部 MCP 服务器的工具接进 <code>Toolkit</code>。",
         "<code>MCPClient</code> brings an external MCP server's tools into a <code>Toolkit</code>."),
        ("配置二选一：<code>StdioMCPConfig</code> 或 <code>HttpMCPConfig</code>。",
         "Pick a config: <code>StdioMCPConfig</code> or <code>HttpMCPConfig</code>."),
        ("MCP 工具同样受权限系统管控。",
         "MCP tools are gated by the permission system too."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 19 — State & Tasks
# ---------------------------------------------------------------------------
LESSON_19 = blocks(
    lead(
        "<code>AgentState</code> 保存一个 agent 的<strong>可持久化状态</strong>（如记忆、权限上下文）；"
        "<code>Task</code> / <code>TaskContext</code> 描述「正在做的任务」及其上下文。",
        "<code>AgentState</code> holds an agent's <strong>persistable state</strong> (e.g. "
        "memory, permission context); <code>Task</code> / <code>TaskContext</code> describe the "
        "task in progress and its context.",
    ),
    analogy(
        "像游戏的<strong>存档</strong>：<code>AgentState</code> 是存档文件，下次读档即可从原处继续；"
        "<code>Task</code> 则像「当前任务清单」。",
        "Like a game <strong>save file</strong>: <code>AgentState</code> is the save you reload "
        "to continue where you left off, while <code>Task</code> is the \"current quest log\".",
    ),
    h2("把状态交给 Agent", "Handing state to the Agent"),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.state import AgentState\n\n"
        "state = AgentState()           # or a previously persisted one\n"
        "agent = Agent(\n"
        '    name="Friday", system_prompt="...", model=...,\n'
        "    state=state,               # the agent reads/updates this state\n"
        ")",
        cap_zh="构造时传入 AgentState；不传则自动新建。",
        cap_en="Pass an AgentState at construction; a new one is created if omitted.",
    ),
    p(
        "在服务化场景（第 23 课），每个会话有自己的状态，由存储后端持久化，从而实现"
        "「多会话隔离」与「断点续聊」。<code>TaskContext</code> 则承载与某个 <code>Task</code> "
        "相关的运行上下文。",
        "In the service setting (lesson 23) each session has its own state, persisted by the "
        "storage backend — enabling \"multi-session isolation\" and \"resume a conversation\". "
        "<code>TaskContext</code> carries the runtime context tied to a given <code>Task</code>.",
    ),
    h2("任务规划工具", "Task-planning tools"),
    p(
        "前面讲的是<strong>被动的数据</strong>（<code>Task</code> / <code>TaskContext</code>）。"
        "AgentScope 还提供一组<strong>主动的规划工具</strong>，让 agent 自己把复杂工作"
        "拆成一份<strong>可追踪、可更新的计划</strong>——这正是 README 里「Task planning」那张动图。"
        "在 Agent Service（第 23 课）中，这些工具会被<strong>自动加入每个会话的工具箱</strong>。",
        "Above we covered the <strong>passive data</strong> (<code>Task</code> / "
        "<code>TaskContext</code>). AgentScope also ships <strong>active planning tools</strong> "
        "that let the agent break complex work into a <strong>tracked, updatable plan</strong> — "
        "this is the README's \"Task planning\" gif. In the Agent Service (lesson 23) these tools "
        "are <strong>auto-added to every session's toolkit</strong>.",
    ),
    table(
        [("工具", "Tool"), ("作用", "Purpose")],
        [
            [("<code>TaskCreate</code>", "<code>TaskCreate</code>"),
             ("创建一份结构化任务清单", "create a structured task list")],
            [("<code>TaskUpdate</code>", "<code>TaskUpdate</code>"),
             ("更新某个任务的状态 / 内容", "update a task's status / content")],
            [("<code>TaskList</code> / <code>TaskGet</code>", "<code>TaskList</code> / <code>TaskGet</code>"),
             ("列出 / 读取任务", "list / read tasks")],
        ],
    ),
    code(
        "from agentscope.tool import Toolkit, TaskCreate, TaskUpdate, TaskList, TaskGet\n\n"
        "toolkit = Toolkit(tools=[TaskCreate(), TaskUpdate(), TaskList(), TaskGet()])\n"
        "# the agent calls these to plan: create a list, then mark items done as it goes\n"
        "# (they read/write AgentState.tasks_context)",
        cap_zh="把规划工具放进 Toolkit；agent 用它们边做边更新计划。",
        cap_en="Put the planning tools in a Toolkit; the agent plans and updates as it goes.",
    ),
    source_map([
        ("state/_state.py", "<code>AgentState</code> / <code>TaskContext</code>",
         "<code>AgentState</code> / <code>TaskContext</code>"),
        ("state/_task.py", "<code>Task</code> 数据模型",
         "the <code>Task</code> data model"),
        ("tool/_task/", "规划工具 <code>TaskCreate</code> / <code>TaskUpdate</code> / "
         "<code>TaskList</code> / <code>TaskGet</code>",
         "planning tools <code>TaskCreate</code> / <code>TaskUpdate</code> / "
         "<code>TaskList</code> / <code>TaskGet</code>"),
        ("app/_service/_toolkit.py", "服务里把规划工具自动加入会话工具箱",
         "the service auto-adds the planning tools to each session's toolkit"),
    ]),
    keypoints([
        ("<code>AgentState</code> 是 agent 的可持久化状态（记忆、权限上下文等）。",
         "<code>AgentState</code> is the agent's persistable state (memory, permission context, …)."),
        ("不传 <code>state</code> 时 Agent 会自动新建一个。",
         "If no <code>state</code> is passed, the Agent creates one."),
        ("持久化状态是多会话隔离与续聊的基础。",
         "Persisted state underpins multi-session isolation and conversation resume."),
        ("规划工具（<code>TaskCreate</code>/<code>TaskUpdate</code> 等）让 agent 自己拆解并追踪计划。",
         "Planning tools (<code>TaskCreate</code>/<code>TaskUpdate</code>, …) let the agent break "
         "down and track its own plan."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 20 — Skills
# ---------------------------------------------------------------------------
LESSON_20 = blocks(
    lead(
        "<strong>技能（Skill）</strong>把「一组提示 + 用法 + 可能的工具」打包成可复用、可加载的能力。"
        "<code>SkillLoaderBase</code> 定义加载协议，<code>LocalSkillLoader</code> 从本地目录加载。",
        "A <strong>Skill</strong> packages \"a set of prompts + usage + possibly tools\" into a "
        "reusable, loadable capability. <code>SkillLoaderBase</code> defines the loading "
        "protocol and <code>LocalSkillLoader</code> loads from a local directory.",
    ),
    analogy(
        "像给助手一本<strong>操作手册</strong>：把「如何做某类任务」整理成一份可复用的技能，"
        "需要时加载进来，agent 就「学会」了这套做法。",
        "Like handing the assistant a <strong>playbook</strong>: package \"how to do a class of "
        "task\" as a reusable skill, load it when needed, and the agent \"knows\" that approach.",
    ),
    h2("加载技能", "Loading skills"),
    code(
        "from agentscope.tool import Toolkit\n"
        "from agentscope.skill import LocalSkillLoader\n\n"
        "toolkit = Toolkit(\n"
        '    skills_or_loaders=["./skills", LocalSkillLoader(...)],\n'
        ")\n"
        "# the toolkit exposes skill instructions to the agent",
        cap_zh="通过 Toolkit 的 skills_or_loaders 加载技能。",
        cap_en="Load skills via the Toolkit's skills_or_loaders.",
    ),
    p(
        "<code>Toolkit</code> 会汇集已注册技能的说明（instructions）提供给 agent；内置的 skill 工具"
        "（<code>tool/_builtin/_skill.py</code>）让 agent 能在运行时使用技能。",
        "The <code>Toolkit</code> gathers the instructions of registered skills for the agent; "
        "the built-in skill tool (<code>tool/_builtin/_skill.py</code>) lets the agent use "
        "skills at runtime.",
    ),
    source_map([
        ("skill/_base.py", "<code>Skill</code> / <code>SkillLoaderBase</code>",
         "<code>Skill</code> / <code>SkillLoaderBase</code>"),
        ("skill/_local_loader.py", "<code>LocalSkillLoader</code>",
         "<code>LocalSkillLoader</code>"),
        ("tool/_builtin/_skill.py", "内置 skill 工具",
         "the built-in skill tool"),
    ]),
    keypoints([
        ("技能 = 可复用、可加载的能力包（提示/用法/工具）。",
         "A skill = a reusable, loadable capability pack (prompts/usage/tools)."),
        ("通过 <code>Toolkit(skills_or_loaders=[...])</code> 加载。",
         "Load via <code>Toolkit(skills_or_loaders=[...])</code>."),
        ("<code>LocalSkillLoader</code> 从本地目录加载技能。",
         "<code>LocalSkillLoader</code> loads skills from a local directory."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 21 — Embeddings
# ---------------------------------------------------------------------------
LESSON_21 = blocks(
    lead(
        "<strong>嵌入（Embedding）</strong>把文本变成向量，是<strong>检索 / RAG</strong> 的基础。"
        "<code>EmbeddingModelBase</code> 统一各厂商嵌入模型；<code>EmbeddingCacheBase</code> / "
        "<code>FileEmbeddingCache</code> 提供缓存以省钱省时。",
        "<strong>Embeddings</strong> turn text into vectors — the basis for "
        "<strong>retrieval / RAG</strong>. <code>EmbeddingModelBase</code> unifies vendor "
        "embedding models; <code>EmbeddingCacheBase</code> / <code>FileEmbeddingCache</code> "
        "add caching to save time and money.",
    ),
    analogy(
        "像给每段文字一个<strong>语义坐标</strong>：意思相近的句子坐标也相近，于是「找相似」就变成"
        "「找最近的点」。",
        "Like giving each piece of text a <strong>semantic coordinate</strong>: similar "
        "sentences land near each other, so \"find similar\" becomes \"find the nearest point\".",
    ),
    h2("调用嵌入模型", "Calling an embedding model"),
    code(
        "from agentscope.embedding import DashScopeEmbeddingModel, FileEmbeddingCache\n\n"
        "embed = DashScopeEmbeddingModel(\n"
        "    ...,                       # credential + model name\n"
        "    embedding_cache=FileEmbeddingCache(...),  # optional: reuse past results\n"
        ")\n"
        "resp = await embed([\"hello\", \"world\"])   # -> EmbeddingResponse",
        cap_zh="嵌入模型可调用（async），返回 EmbeddingResponse；缓存可选。",
        cap_en="Embedding models are async-callable, returning an EmbeddingResponse; cache optional.",
    ),
    p(
        "拿到向量后，配合向量库（检索最近邻）即可实现 RAG：把相关文档喂回模型上下文。"
        "AgentScope 提供嵌入与缓存这块基石；向量库的选择留给你的应用。",
        "With vectors in hand, pair them with a vector store (nearest-neighbor search) to do "
        "RAG: feed relevant documents back into the model's context. AgentScope provides the "
        "embedding + caching foundation; the vector store choice is left to your application.",
    ),
    source_map([
        ("embedding/_embedding_base.py", "<code>EmbeddingModelBase</code>（可调用，async）",
         "<code>EmbeddingModelBase</code> (async-callable)"),
        ("embedding/_dashscope/_model.py", "<code>DashScopeEmbeddingModel</code> 等厂商实现",
         "<code>DashScopeEmbeddingModel</code> and other vendor implementations"),
        ("embedding/_file_cache.py", "<code>FileEmbeddingCache</code>（<code>EmbeddingCacheBase</code>）",
         "<code>FileEmbeddingCache</code> (<code>EmbeddingCacheBase</code>)"),
        ("embedding/_embedding_response.py", "<code>EmbeddingResponse</code>",
         "<code>EmbeddingResponse</code>"),
    ]),
    keypoints([
        ("嵌入把文本变向量，是检索 / RAG 的基础。",
         "Embeddings turn text into vectors — the basis for retrieval / RAG."),
        ("<code>EmbeddingModelBase</code> 统一各厂商；调用是 async。",
         "<code>EmbeddingModelBase</code> unifies vendors; calls are async."),
        ("缓存（<code>FileEmbeddingCache</code>）避免重复计算。",
         "Caching (<code>FileEmbeddingCache</code>) avoids recomputation."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 22 — TTS
# ---------------------------------------------------------------------------
LESSON_22 = blocks(
    lead(
        "<strong>TTS（文本转语音）</strong>把 agent 的文字回复变成声音。"
        "<code>TTSModelBase</code> 定义统一接口（含<strong>实时</strong>模式），"
        "<code>TTSMiddleware</code> 把它接进 agent 的回复流。",
        "<strong>TTS (text-to-speech)</strong> turns an agent's text replies into audio. "
        "<code>TTSModelBase</code> defines a unified interface (including a <strong>realtime</strong> "
        "mode), and <code>TTSMiddleware</code> wires it into the agent's reply flow.",
    ),
    analogy(
        "像给文字配一位<strong>配音演员</strong>：模型负责写台词，TTS 负责念出来；实时模式则像"
        "「边写边念」。",
        "Like giving the text a <strong>voice actor</strong>: the model writes the lines and TTS "
        "speaks them; realtime mode is like \"speaking as it's written\".",
    ),
    h2("接口与实时", "Interface and realtime"),
    table(
        [("类型", "Type"), ("说明", "Description")],
        [
            [("<code>TTSModelBase</code>", "<code>TTSModelBase</code>"),
             ("统一 TTS 接口（异步，支持连接/推送/合成）",
              "unified TTS interface (async; connect/push/synthesize)")],
            [("<code>DashScopeTTSModel</code>", "<code>DashScopeTTSModel</code>"),
             ("一次性合成", "one-shot synthesis")],
            [("<code>DashScopeRealtimeTTSModel</code>", "<code>DashScopeRealtimeTTSModel</code>"),
             ("实时流式合成", "realtime streaming synthesis")],
            [("<code>TTSResponse</code> / <code>TTSUsage</code>",
              "<code>TTSResponse</code> / <code>TTSUsage</code>"),
             ("合成结果与用量", "synthesis result + usage")],
        ],
    ),
    p(
        "把 <code>TTSMiddleware</code> 加入 <code>Agent(middlewares=[...])</code>（第 15 课），"
        "agent 产出文本时即可自动合成语音——无需改动 agent 主逻辑。",
        "Add <code>TTSMiddleware</code> to <code>Agent(middlewares=[...])</code> (lesson 15) and "
        "the agent's text output is synthesized to speech automatically — no change to the "
        "agent's core logic.",
    ),
    source_map([
        ("tts/_tts_base.py", "<code>TTSModelBase</code>（connect/push/synthesize，async）",
         "<code>TTSModelBase</code> (connect/push/synthesize, async)"),
        ("tts/_dashscope/_model.py", "<code>DashScopeTTSModel</code> / <code>DashScopeRealtimeTTSModel</code>",
         "<code>DashScopeTTSModel</code> / <code>DashScopeRealtimeTTSModel</code>"),
        ("tts/_tts_response.py", "<code>TTSResponse</code> / <code>TTSUsage</code>",
         "<code>TTSResponse</code> / <code>TTSUsage</code>"),
        ("middleware/_tts_middleware.py", "<code>TTSMiddleware</code>",
         "<code>TTSMiddleware</code>"),
    ]),
    keypoints([
        ("<code>TTSModelBase</code> 统一文本转语音，含实时模式。",
         "<code>TTSModelBase</code> unifies text-to-speech, including a realtime mode."),
        ("<code>TTSMiddleware</code> 让语音能力即插即用。",
         "<code>TTSMiddleware</code> makes speech plug-and-play."),
        ("再次体现「用中间件扩展，不改主逻辑」。",
         "Again: \"extend via middleware, don't touch the core\"."),
    ]),
)


LESSONS = {
    "16-permission.html": LESSON_16,
    "17-workspace.html": LESSON_17,
    "18-mcp.html": LESSON_18,
    "19-state-tasks.html": LESSON_19,
    "20-skills.html": LESSON_20,
    "21-embeddings.html": LESSON_21,
    "22-tts.html": LESSON_22,
}


QUIZZES = {
    "16-permission.html": [
        (
            "当权限裁决为「需确认」时会发生什么？",
            "What happens when a permission decision is \"needs confirm\"?",
            [
                ("发出 <code>REQUIRE_USER_CONFIRM</code> 事件，等待人类批准",
                 "It emits a <code>REQUIRE_USER_CONFIRM</code> event and waits for a human", True),
                ("直接拒绝并报错", "It rejects with an error immediately", False),
                ("忽略权限", "It ignores permissions", False),
            ],
            "需确认会触发 REQUIRE_USER_CONFIRM 事件，把人类介入接进事件流。",
            "Needs-confirm triggers a REQUIRE_USER_CONFIRM event, bringing the human into the stream.",
        ),
    ],
    "17-workspace.html": [
        (
            "AgentScope 内置哪几种工作区后端？",
            "Which workspace backends does AgentScope ship?",
            [
                ("本地 / Docker / E2B", "Local / Docker / E2B", True),
                ("只有本地", "Local only", False),
                ("只有云端", "Cloud only", False),
            ],
            "WorkspaceBase 有 LocalWorkspace、DockerWorkspace、E2BWorkspace 三种实现。",
            "WorkspaceBase has LocalWorkspace, DockerWorkspace and E2BWorkspace implementations.",
        ),
    ],
    "18-mcp.html": [
        (
            "<code>MCPClient</code> 的作用是什么？",
            "What does an <code>MCPClient</code> do?",
            [
                ("连接外部 MCP 服务器并把其工具接入 <code>Toolkit</code>",
                 "Connect an external MCP server and bring its tools into a <code>Toolkit</code>", True),
                ("训练嵌入模型", "Train embedding models", False),
                ("渲染语音", "Render speech", False),
            ],
            "MCPClient 连接 MCP 服务器，通过 list_tools 把外部工具暴露为 ToolBase。",
            "MCPClient connects to an MCP server and exposes its tools as ToolBase via list_tools.",
        ),
    ],
    "19-state-tasks.html": [
        (
            "<code>AgentState</code> 的作用是什么？",
            "What is <code>AgentState</code> for?",
            [
                ("保存 agent 的可持久化状态，支撑多会话隔离与续聊",
                 "Holds the agent's persistable state, enabling multi-session isolation and resume",
                 True),
                ("存储 CSS 样式", "Storing CSS styles", False),
                ("替换模型", "Replacing the model", False),
            ],
            "AgentState 持久化记忆/权限上下文等，是多会话与断点续聊的基础。",
            "AgentState persists memory/permission context, the basis for multi-session and resume.",
        ),
    ],
    "20-skills.html": [
        (
            "如何把一个技能加载给 agent？",
            "How do you load a skill for an agent?",
            [
                ("通过 <code>Toolkit(skills_or_loaders=[...])</code>",
                 "Via <code>Toolkit(skills_or_loaders=[...])</code>", True),
                ("重新训练模型", "Retrain the model", False),
                ("修改系统环境变量", "Edit system environment variables", False),
            ],
            "Toolkit 的 skills_or_loaders 接受路径 / Skill / 加载器来加载技能。",
            "The Toolkit's skills_or_loaders accepts paths / Skills / loaders to load skills.",
        ),
    ],
    "21-embeddings.html": [
        (
            "嵌入（embedding）在 agent 应用里主要支撑什么？",
            "What do embeddings primarily enable in agent apps?",
            [
                ("检索 / RAG（按语义找相关内容）",
                 "Retrieval / RAG (finding relevant content by meaning)", True),
                ("权限控制", "Permission control", False),
                ("语音合成", "Speech synthesis", False),
            ],
            "嵌入把文本变向量，用于按语义检索，是 RAG 的基础。",
            "Embeddings turn text into vectors for semantic retrieval — the basis of RAG.",
        ),
    ],
    "22-tts.html": [
        (
            "如何把语音能力接入 agent 而不改其主逻辑？",
            "How do you add speech to an agent without changing its core logic?",
            [
                ("把 <code>TTSMiddleware</code> 加入 <code>middlewares=[...]</code>",
                 "Add <code>TTSMiddleware</code> to <code>middlewares=[...]</code>", True),
                ("重写 Agent 类", "Rewrite the Agent class", False),
                ("改 LLM 的权重", "Edit the LLM's weights", False),
            ],
            "TTSMiddleware 作为中间件挂载，自动把文本回复合成语音。",
            "TTSMiddleware is attached as middleware and automatically synthesizes text replies to speech.",
        ),
    ],
}
