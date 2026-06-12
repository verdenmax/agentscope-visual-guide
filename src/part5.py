"""Content for Part 5 (advanced capabilities): lessons 16–22.

Verified against AgentScope 2.0 source (permission/, workspace/, mcp/, state/,
skill/, embedding/, tts/).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t, flow,
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
            [("<code>PermissionMode</code>", "<code>PermissionMode</code>"),
             ("总体模式（如默认询问、bypass 放行）", "the overall mode (e.g. default-ask, bypass)")],
            [("<code>PermissionDecision</code>", "<code>PermissionDecision</code>"),
             ("放行 / 拒绝 / 需确认", "allow / deny / needs-confirm")],
            [("<code>PermissionContext</code>", "<code>PermissionContext</code>"),
             ("承载模式与规则的上下文", "the context holding the mode and rules")],
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
        "其他模式中最实用的是 <code>ACCEPT_EDITS</code>（自动允许工作目录内的读写，适合开发期快速迭代）。",
        "Among the other modes, the practical one is <code>ACCEPT_EDITS</code> (auto-allow "
        "reads/writes inside working directories — handy for rapid development).",
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
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.workspace import DockerWorkspace\n\n"
        "agent = Agent(\n"
        '    name="Friday", system_prompt="...", model=..., toolkit=...,\n'
        "    offloader=DockerWorkspace(...),  # tools/code run inside the sandbox\n"
        ")",
        cap_zh="把一个 workspace 交给 Agent，工具/代码即在隔离环境中执行。",
        cap_en="Hand a workspace to the Agent; tools/code then run in the sandbox.",
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
    h2("后端对比与卸载协议", "Backends compared + the offload protocol"),
    table(
        [("后端", "Backend"), ("隔离性", "Isolation"), ("速度 / 启动", "Speed / setup"), ("适用", "Use case")],
        [
            [("<code>LocalWorkspace</code>", "<code>LocalWorkspace</code>"),
             ("无（就是本机）", "none (your machine)"),
             ("最快、零配置", "fastest, zero setup"),
             ("本地开发 / 受信任", "local dev / trusted")],
            [("<code>DockerWorkspace</code>", "<code>DockerWorkspace</code>"),
             ("容器级", "container-level"),
             ("需 Docker，启动稍慢", "needs Docker, slower start"),
             ("限制副作用 / 不可信代码", "contain side effects / untrusted code")],
            [("<code>E2BWorkspace</code>", "<code>E2BWorkspace</code>"),
             ("云端沙箱、强隔离", "cloud sandbox, strong"),
             ("需 e2b 账号 / 网络", "needs an e2b account / network"),
             ("弹性 / 多租户生产", "elastic / multi-tenant prod")],
        ],
    ),
    accordion(
        "为什么 workspace 能直接当 offloader 用？",
        "Why can a workspace be used directly as the offloader?",
        blocks(
            p(
                "<code>WorkspaceBase</code> 实现了 <code>Offloader</code> 协议的 "
                "<code>offload_context</code> 与 <code>offload_tool_result</code> 两个方法——它本来就管着"
                "一个可读写的环境，把超长内容写进去再返回一个引用是顺理成章的。所以你可以直接 "
                "<code>Agent(offloader=DockerWorkspace(...))</code>，让「执行环境」与「卸载存储」是同一个东西。",
                "<code>WorkspaceBase</code> implements the <code>Offloader</code> protocol's "
                "<code>offload_context</code> and <code>offload_tool_result</code> — it already owns a "
                "read/write environment, so writing oversized content there and returning a reference "
                "is natural. Hence you can pass <code>Agent(offloader=DockerWorkspace(...))</code>, "
                "making the execution environment and the offload store one and the same.",
            ),
        ),
        num=1,
    ),
    note(
        "依赖提示：<code>DockerWorkspace</code> 需要本机有 Docker（<code>pip install agentscope[workspace]</code> "
        "装上 <code>aiodocker</code>），<code>E2BWorkspace</code> 需要 <code>e2b</code> 与一个 API key；"
        "<code>LocalWorkspace</code> 则无额外依赖。",
        "Dependency note: <code>DockerWorkspace</code> needs Docker locally "
        "(<code>pip install agentscope[workspace]</code> brings <code>aiodocker</code>), "
        "<code>E2BWorkspace</code> needs <code>e2b</code> and an API key; <code>LocalWorkspace</code> "
        "has no extra dependency.",
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
    h2("连接与使用：完整流程", "Connect and use: the full flow"),
    code(
        "from agentscope.mcp import MCPClient, StdioMCPConfig, HttpMCPConfig\n"
        "from agentscope.tool import Toolkit\n"
        "from agentscope.agent import Agent\n\n"
        "# A) 本地子进程服务器 / a local subprocess server\n"
        "client = MCPClient(StdioMCPConfig(\n"
        '    command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "."],\n'
        "))\n"
        "# B) 远程 HTTP 服务器 / a remote HTTP server\n"
        "# client = MCPClient(HttpMCPConfig(url=\"https://my-mcp.example.com/mcp\"))\n\n"
        "await client.connect()\n"
        "toolkit = Toolkit(mcps=[client])      # 其工具自动注册进 Toolkit\n"
        "agent = Agent(name=\"Friday\", system_prompt=\"...\", model=..., toolkit=toolkit)\n"
        "# ... 用完记得 await client.close()",
        cap_zh="连上 MCP 服务器，把它的工具接进 Toolkit，再交给 Agent。",
        cap_en="Connect to an MCP server, register its tools into a Toolkit, then hand it to an Agent.",
    ),
    table(
        [("配置", "Config"), ("用于", "For"), ("关键字段", "Key fields")],
        [
            [("<code>StdioMCPConfig</code>", "<code>StdioMCPConfig</code>"),
             ("本地子进程（通过 stdio 通信）", "a local subprocess (talks over stdio)"),
             ("<code>command</code> · <code>args</code> · <code>env</code> · <code>cwd</code>",
              "<code>command</code> · <code>args</code> · <code>env</code> · <code>cwd</code>")],
            [("<code>HttpMCPConfig</code>", "<code>HttpMCPConfig</code>"),
             ("远程 HTTP 端点", "a remote HTTP endpoint"),
             ("<code>url</code> · <code>headers</code> · <code>timeout</code>",
              "<code>url</code> · <code>headers</code> · <code>timeout</code>")],
        ],
    ),
    accordion(
        "MCP 是什么，为什么值得用？",
        "What is MCP, and why bother?",
        blocks(
            p(
                "MCP（Model Context Protocol）是一套<strong>开放标准</strong>，让工具 / 数据源以统一方式"
                "暴露给任意 agent 框架。这意味着你不必为每个能力重新造轮子——社区已有大量现成的 MCP "
                "服务器（文件系统、数据库、浏览器、Git 等），<code>MCPClient</code> 连上即用。",
                "MCP (Model Context Protocol) is an <strong>open standard</strong> for exposing tools / "
                "data sources to any agent framework in a uniform way. So you don't reinvent every "
                "capability — there's a large ecosystem of ready MCP servers (filesystem, databases, "
                "browsers, Git, …) that <code>MCPClient</code> can plug into.",
            ),
            p(
                "<code>client.list_tools()</code> 返回的是一组标准 <code>ToolBase</code>（实为 "
                "<code>MCPTool</code>），所以它们和本地内置工具走<strong>完全相同</strong>的注册、"
                "schema 生成与权限流程。",
                "<code>client.list_tools()</code> returns standard <code>ToolBase</code>s (actually "
                "<code>MCPTool</code>), so they go through the <strong>exact same</strong> "
                "registration, schema-generation and permission flow as local built-in tools.",
            ),
        ),
        num=1,
    ),
    note(
        "两个易错点：① 用前必须 <code>await client.connect()</code>，用完 <code>await client.close()</code>；"
        "② MCP 工具<strong>同样受权限系统管控</strong>——别因为它来自外部就以为会绕过确认（见第 16 课）。",
        "Two gotchas: (1) you must <code>await client.connect()</code> before use and "
        "<code>await client.close()</code> after; (2) MCP tools are <strong>gated by the permission "
        "system too</strong> — don't assume \"external\" means it skips confirmation (see lesson 16).",
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
        "「多会话隔离」与「断点续聊」。<code>TaskContext</code> 是 <code>AgentState</code> 里"
        "专门存放<strong>任务清单</strong>的那部分（即下文规划工具读写的 <code>tasks_context</code>）。",
        "In the service setting (lesson 23) each session has its own state, persisted by the "
        "storage backend — enabling \"multi-session isolation\" and \"resume a conversation\". "
        "<code>TaskContext</code> is the part of <code>AgentState</code> that holds the "
        "<strong>task list</strong> (the <code>tasks_context</code> the planning tools below "
        "read and write).",
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
        "一个 <code>Skill</code> 本质上就是一个<strong>目录 + 一份 Markdown 文档</strong>："
        "带有 <code>name</code>、<code>description</code> 和 <code>markdown</code>（具体做法），"
        "放在某个目录（<code>dir</code>）下。<code>Toolkit</code> 把已注册技能的说明汇集给 agent，"
        "内置的 skill 工具让 agent 在运行时按需调用——所以「写一个技能」≈ 写一份结构化的操作手册。",
        "A <code>Skill</code> is essentially a <strong>directory + a Markdown document</strong>: "
        "it has a <code>name</code>, a <code>description</code>, and the <code>markdown</code> "
        "(the actual how-to), living under a <code>dir</code>. The <code>Toolkit</code> surfaces "
        "registered skills' instructions to the agent, and the built-in skill tool lets the agent "
        "invoke them at runtime — so \"writing a skill\" ≈ writing a structured playbook.",
    ),
    h2("一个技能长什么样", "What a skill looks like"),
    accordion(
        "技能目录与 SKILL.md 示例",
        "A skill directory and its SKILL.md",
        blocks(
            p(
                "一个技能就是磁盘上的<strong>一个目录</strong>，核心是一份 Markdown「操作手册」。"
                "<code>LocalSkillLoader</code> 从目录读出它的 <code>name</code> / <code>description</code> / "
                "<code>markdown</code>：",
                "A skill is just <strong>a directory</strong> on disk whose heart is a Markdown "
                "\"playbook\". <code>LocalSkillLoader</code> reads its <code>name</code> / "
                "<code>description</code> / <code>markdown</code> from that directory:",
            ),
            code(
                "skills/\n"
                "└── refund_policy/\n"
                "    ├── SKILL.md        # name + description (front matter) + the how-to\n"
                "    └── examples.md     # optional supporting files\n",
                lang="text",
            ),
            code(
                "# Refund policy        <-- name\n"
                "How to process a customer refund request.   <-- description\n\n"
                "## Steps\n"
                "1. Verify the order id with the `lookup_order` tool.\n"
                "2. Check it is within 30 days.\n"
                "3. If eligible, call `issue_refund`; otherwise explain why.\n",
                lang="text",
                cap_zh="SKILL.md 本质上是一份结构化的操作手册，模型据此「照着做」。",
                cap_en="SKILL.md is essentially a structured playbook the model follows.",
            ),
        ),
        num=1,
    ),
    table(
        [("机制", "Mechanism"), ("是什么", "What it is"), ("何时用", "When to use")],
        [
            [("技能 Skill", "Skill"),
             ("一份 Markdown 操作手册（如何做某类任务）", "a Markdown playbook (how to do a class of task)"),
             ("把可复用的「做法 / 流程」教给 agent", "teach the agent a reusable procedure")],
            [("工具 Tool", "Tool"),
             ("一段可执行的代码（函数 / 类）", "executable code (a function / class)"),
             ("让 agent 真正「动手」执行某操作", "let the agent actually perform an action")],
            [("MCP", "MCP"),
             ("接入外部服务器提供的工具", "tools from an external server"),
             ("复用别人已实现的能力", "reuse capabilities others built")],
        ],
    ),
    code(
        "from agentscope.tool import Toolkit\n"
        "from agentscope.skill import LocalSkillLoader\n\n"
        "toolkit = Toolkit(\n"
        '    skills_or_loaders=["./skills", LocalSkillLoader("./more_skills")],\n'
        ")\n"
        "# Toolkit 汇集各技能的说明，agent 在运行时按需取用",
        cap_zh="把技能目录交给 Toolkit；说明会作为提示提供给 agent。",
        cap_en="Hand skill directories to the Toolkit; their instructions are surfaced to the agent.",
    ),
    tip(
        "<strong>技能 vs 工具</strong>：要「教做法 / 知识 / 流程」用技能（纯 Markdown，无需写代码）；"
        "要「执行动作」（读写文件、调 API）用工具。两者常配合：技能里引用工具名，告诉模型何时调用。",
        "<strong>Skill vs tool</strong>: use a skill to teach a procedure / knowledge / workflow "
        "(pure Markdown, no code); use a tool to perform an action (read/write files, call an API). "
        "They pair up: a skill references tool names and tells the model when to call them.",
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
    flow(
        [("文档", "Documents"), ("切块", "Chunk"), ("嵌入为向量", "Embed → vectors"),
         ("存入向量库", "Vector store"), ("查询时检索 Top-K", "Retrieve Top-K"),
         ("拼进上下文", "Into context")],
        "这就是 RAG 的标准管线：离线把语料嵌入入库，在线把问题嵌入后找最近的若干块喂给模型。",
        "This is the standard RAG pipeline: embed the corpus offline, then at query time embed "
        "the question and feed the nearest chunks to the model.",
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
    h2("从嵌入到 RAG", "From embeddings to RAG"),
    code(
        "from agentscope.embedding import DashScopeEmbeddingModel, FileEmbeddingCache\n\n"
        "embed = DashScopeEmbeddingModel(\n"
        "    credential=...,\n"
        '    model="text-embedding-v4",\n'
        "    embedding_cache=FileEmbeddingCache(...),   # 命中缓存就不再请求 API\n"
        ")\n"
        'resp = await embed(["退款政策是什么？", "如何修改收货地址？"])\n'
        "vectors = resp.embeddings        # 每条文本一个向量 / one vector per input",
        cap_zh="嵌入模型是 async 可调用对象，返回 EmbeddingResponse；缓存可选但很省钱。",
        cap_en="An embedding model is async-callable, returns an EmbeddingResponse; caching is optional but saves money.",
    ),
    accordion(
        "RAG 全流程：嵌入只是其中一环",
        "The full RAG flow: embeddings are just one link",
        blocks(
            p(
                "检索增强生成（RAG）的典型链路如下。AgentScope 负责其中的<strong>嵌入与缓存</strong>这块基石，"
                "而<strong>向量库</strong>（存向量、做最近邻检索）由你的应用自选（如 FAISS / Qdrant / pgvector）。",
                "A typical retrieval-augmented-generation (RAG) pipeline looks like this. AgentScope "
                "provides the <strong>embedding + caching</strong> foundation; the <strong>vector "
                "store</strong> (holding vectors and doing nearest-neighbor search) is your "
                "application's choice (e.g. FAISS / Qdrant / pgvector).",
            ),
            code(
                "文档 → 切块 → 嵌入(AgentScope) → 存入向量库(你选) →\n"
                "    查询时：问题嵌入 → 最近邻检索 → 把相关片段拼进上下文 → 交给 Agent\n\n"
                "Document -> chunk -> embed (AgentScope) -> vector store (yours) ->\n"
                "    at query time: embed the question -> nearest-neighbor search ->\n"
                "    stuff the relevant chunks into context -> hand to the Agent",
                lang="text",
            ),
        ),
        num=1,
    ),
    table(
        [("厂商", "Vendor"), ("类", "Class")],
        [
            [("DashScope", "DashScope"), ("<code>DashScopeEmbeddingModel</code>", "<code>DashScopeEmbeddingModel</code>")],
            [("OpenAI", "OpenAI"), ("<code>OpenAIEmbeddingModel</code>", "<code>OpenAIEmbeddingModel</code>")],
            [("Gemini / Ollama", "Gemini / Ollama"),
             ("<code>GeminiEmbeddingModel</code> / <code>OllamaEmbeddingModel</code>",
              "<code>GeminiEmbeddingModel</code> / <code>OllamaEmbeddingModel</code>")],
        ],
    ),
    note(
        "嵌入调用通常是<strong>批量且重复</strong>的（同一批文档反复嵌入）。<code>FileEmbeddingCache</code> "
        "把结果缓存到磁盘，命中即跳过 API 调用——既省钱又提速。缓存基类是 <code>EmbeddingCacheBase</code>，可自定义后端。",
        "Embedding calls are often <strong>batched and repetitive</strong> (re-embedding the same "
        "documents). <code>FileEmbeddingCache</code> caches results to disk and skips the API call "
        "on a hit — saving money and time. The base is <code>EmbeddingCacheBase</code>, so you can "
        "plug in your own backend.",
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
    h2("接入与选型", "Wiring and choosing a model"),
    code(
        "from agentscope.agent import Agent\n"
        "from agentscope.middleware import TTSMiddleware\n"
        "from agentscope.tts import DashScopeRealtimeTTSModel\n\n"
        "agent = Agent(\n"
        '    name="Friday", system_prompt="...", model=...,\n'
        "    middlewares=[TTSMiddleware(tts_model=DashScopeRealtimeTTSModel(...))],\n"
        ")\n"
        "# agent 产出文本时，中间件自动把它送去合成语音——agent 主逻辑无感知",
        cap_zh="把 TTSMiddleware 挂到 Agent 上，文本回复即自动转语音。",
        cap_en="Attach TTSMiddleware to the Agent; text replies are synthesized to speech automatically.",
    ),
    table(
        [("模型", "Model"), ("合成方式", "Synthesis"), ("适用", "Use case")],
        [
            [("<code>DashScopeTTSModel</code>", "<code>DashScopeTTSModel</code>"),
             ("整段文本就绪后一次性合成", "one-shot, after the full text is ready"),
             ("离线 / 不在意首字延迟", "offline / latency not critical")],
            [("<code>DashScopeRealtimeTTSModel</code>", "<code>DashScopeRealtimeTTSModel</code>"),
             ("边生成边推送、流式合成", "streaming — push as text is generated"),
             ("语音对话 / 低延迟", "voice chat / low latency")],
        ],
    ),
    accordion(
        "实时 TTS 的工作方式",
        "How realtime TTS works",
        blocks(
            p(
                "<code>TTSModelBase</code> 是一个<strong>异步上下文管理器</strong>：先 "
                "<code>connect()</code> 建立会话，随着模型不断吐字，用 <code>push(text)</code> "
                "把增量文本送进去，底层<strong>边收边合成</strong>音频，最后 <code>close()</code>。"
                "一次性的 <code>synthesize()</code> 则是把整段文本一口气合成。",
                "<code>TTSModelBase</code> is an <strong>async context manager</strong>: "
                "<code>connect()</code> opens a session, then as the model streams text you "
                "<code>push(text)</code> the increments and the backend <strong>synthesizes audio "
                "as it arrives</strong>, ending with <code>close()</code>. The one-shot "
                "<code>synthesize()</code> instead renders the whole text at once.",
            ),
        ),
        num=1,
    ),
    tip(
        "按<strong>延迟需求</strong>选型：做语音助手 / 实时对话用 <code>DashScopeRealtimeTTSModel</code>"
        "（首字更快、可打断）；批量生成音频文件用 <code>DashScopeTTSModel</code> 即可。无论哪种，"
        "都通过 <code>TTSMiddleware</code> 接入，不动 agent 主逻辑。",
        "Choose by <strong>latency</strong>: for a voice assistant / live dialogue use "
        "<code>DashScopeRealtimeTTSModel</code> (faster first sound, interruptible); for batch "
        "audio files <code>DashScopeTTSModel</code> is fine. Either way you wire it via "
        "<code>TTSMiddleware</code> without touching the agent's core logic.",
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
        ("一次性合成用 <code>DashScopeTTSModel</code>，低延迟流式用 <code>DashScopeRealtimeTTSModel</code>。",
         "Use <code>DashScopeTTSModel</code> for one-shot synthesis, "
         "<code>DashScopeRealtimeTTSModel</code> for low-latency streaming."),
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


QUIZZES: dict = {}

QUIZZES["16-permission.html"] = [
    (
        "关于默认权限模式（<code>PermissionMode.DEFAULT</code>），下列哪项正确？",
        "Which statement about the default permission mode (<code>PermissionMode.DEFAULT</code>) is correct?",
        [
            ("写文件等敏感操作会暂停并发出 <code>REQUIRE_USER_CONFIRM</code>，把确认结果回传后才继续",
             "Sensitive ops like writing files pause and emit <code>REQUIRE_USER_CONFIRM</code>; "
             "you feed the confirmation back to continue", True),
            ("默认就是 <code>BYPASS</code>，所有工具调用都直接放行",
             "The default is <code>BYPASS</code>, so every tool call is allowed straight through", False),
            ("被拦下的工具会直接抛错并终止整个回复",
             "A gated tool throws an error and aborts the whole reply", False),
        ],
        "默认模式并非 BYPASS：敏感操作会暂停等待人类批准（回传 UserConfirmResultEvent 即可继续），"
        "既不会静默放行，也不会崩溃。",
        "The default is not BYPASS: sensitive ops pause for human approval (feed a "
        "UserConfirmResultEvent back to resume) — neither silently allowed nor crashing.",
    ),
]

QUIZZES["17-workspace.html"] = [
    (
        "<code>Offloader</code> 在工作区里解决什么问题？",
        "What problem does the <code>Offloader</code> solve in a workspace?",
        [
            ("把超长上下文 / 大工具结果卸载到工作区（如写入文件），需要时再取回，避免撑爆上下文窗口",
             "It offloads oversized context / large tool results to the workspace (e.g. to files) "
             "and fetches them back when needed, so the context window doesn't overflow", True),
            ("它对每次工具调用作出放行 / 拒绝 / 需确认的裁决",
             "It renders an allow / deny / needs-confirm decision for each tool call", False),
            ("它在多台机器间做负载均衡，把任务分发出去",
             "It load-balances tasks by distributing them across multiple machines", False),
        ],
        "Offloader 负责「卸载」超长上下文与被截断的工具结果并按需取回；放行/拒绝是权限引擎（第 16 课）的职责。",
        "The Offloader offloads oversized context and truncated tool results and fetches them back; "
        "allow/deny is the permission engine's job (lesson 16).",
    ),
]

QUIZZES["18-mcp.html"] = [
    (
        "关于通过 <code>MCPClient</code> 接入的工具，下列哪项正确？",
        "Which statement about tools brought in via an <code>MCPClient</code> is correct?",
        [
            ("它们在 <code>Toolkit</code> 中表现为 <code>MCPTool</code>，和本地工具一样受权限系统管控",
             "They appear as <code>MCPTool</code> in the <code>Toolkit</code> and are gated by the "
             "permission system just like local tools", True),
            ("它们来自外部服务器，因此绕过权限系统直接执行",
             "Because they come from an external server, they bypass the permission system and run "
             "directly", False),
            ("只能用 <code>HttpMCPConfig</code> 连远程服务器，不支持本地进程",
             "You can only use <code>HttpMCPConfig</code> for remote servers; local processes aren't "
             "supported", False),
        ],
        "MCP 工具在 Toolkit 内是 MCPTool，同样经权限引擎把关；连接方式有 StdioMCPConfig（本地子进程）"
        "与 HttpMCPConfig（远程 HTTP）两种。",
        "MCP tools are MCPTool inside the Toolkit and are gated by the permission engine; connect via "
        "StdioMCPConfig (local subprocess) or HttpMCPConfig (remote HTTP).",
    ),
]

QUIZZES["19-state-tasks.html"] = [
    (
        "关于 <code>AgentState</code> 与任务规划工具（<code>TaskCreate</code> 等），下列哪项正确？",
        "Which statement about <code>AgentState</code> and the task-planning tools "
        "(<code>TaskCreate</code>, \u2026) is correct?",
        [
            ("规划工具读写的任务清单（<code>tasks_context</code>）就保存在 <code>AgentState</code> 里，"
             "因此存档能连同计划一起续聊",
             "The task list (<code>tasks_context</code>) the planning tools read/write lives inside "
             "<code>AgentState</code>, so a saved state resumes with the plan intact", True),
            ("任务清单单独存放，与 <code>AgentState</code> 无关",
             "The task list is stored separately and has nothing to do with <code>AgentState</code>", False),
            ("必须显式传入 <code>state</code>，否则 Agent 无法启动",
             "You must pass <code>state</code> explicitly, or the Agent won't start", False),
        ],
        "TaskContext 是 AgentState 的一部分（tasks_context），规划工具就读写它；不传 state 时 Agent 会自动新建。",
        "TaskContext is part of AgentState (tasks_context) that the planning tools read/write; if no "
        "state is passed the Agent creates one.",
    ),
]

QUIZZES["20-skills.html"] = [
    (
        "在 AgentScope 里，「写一个技能（Skill）」本质上是在做什么？",
        "In AgentScope, what does \u201cwriting a skill\u201d essentially amount to?",
        [
            ("写一份结构化的操作手册——一个带 <code>name</code>/<code>description</code>/<code>markdown</code> "
             "的目录，由 <code>LocalSkillLoader</code> 从本地加载",
             "Writing a structured playbook — a directory with <code>name</code>/"
             "<code>description</code>/<code>markdown</code>, loaded from disk by "
             "<code>LocalSkillLoader</code>", True),
            ("微调 / 重训模型，把新能力「学」进权重里",
             "Fine-tuning / retraining the model so the new ability is baked into its weights", False),
            ("写一个新的 Python 工具类并注册为 <code>FunctionTool</code>",
             "Writing a new Python tool class and registering it as a <code>FunctionTool</code>", False),
        ],
        "技能 = 目录 + Markdown 文档（name/description/具体做法），用 Toolkit(skills_or_loaders=[...]) 加载——"
        "既不改模型权重，也不等同于写一个工具类。",
        "A skill = a directory + a Markdown doc (name/description/how-to), loaded via "
        "skills_or_loaders — no weight changes, and not the same as coding a tool class.",
    ),
]

QUIZZES["21-embeddings.html"] = [
    (
        "关于 AgentScope 的嵌入（embedding）支持，下列哪项正确？",
        "Which statement about AgentScope's embedding support is correct?",
        [
            ("它提供嵌入模型 + 缓存这块基石，但向量库（最近邻检索）留给你的应用自选",
             "It provides the embedding-model + caching foundation, but leaves the vector store "
             "(nearest-neighbor search) to your application", True),
            ("它自带向量数据库，开箱即可存储并检索向量",
             "It ships a built-in vector database, so you can store and search vectors out of the box", False),
            ("嵌入模型调用是同步的，直接返回向量列表",
             "Embedding model calls are synchronous and return a plain list of vectors", False),
        ],
        "AgentScope 只提供嵌入与缓存的基石，向量库由你选型；嵌入模型是 async 可调用对象，返回 EmbeddingResponse。",
        "AgentScope provides only the embedding + cache foundation; you choose the vector store. "
        "Embedding models are async-callable and return an EmbeddingResponse.",
    ),
]

QUIZZES["22-tts.html"] = [
    (
        "想要「边生成边出声」的低延迟语音，应选用哪种 TTS 模型？",
        "For low-latency \u201cspeak as it's generated\u201d audio, which TTS model should you use?",
        [
            ("<code>DashScopeRealtimeTTSModel</code>（实时流式合成）",
             "<code>DashScopeRealtimeTTSModel</code> (realtime streaming synthesis)", True),
            ("<code>DashScopeTTSModel</code>（等整段文本就绪后一次性合成）",
             "<code>DashScopeTTSModel</code> (one-shot synthesis after the full text is ready)", False),
            ("<code>TTSMiddleware</code>，它本身就是一个能直接发声的模型",
             "<code>TTSMiddleware</code>, which is itself a model that produces audio", False),
        ],
        "低延迟流式用 DashScopeRealtimeTTSModel，整段一次性合成用 DashScopeTTSModel；"
        "TTSMiddleware 只是把所选 TTS 模型接进回复流的中间件，本身不合成。",
        "Use DashScopeRealtimeTTSModel for low-latency streaming and DashScopeTTSModel for one-shot; "
        "TTSMiddleware is just the wiring that pipes a chosen TTS model into the reply flow, not a synthesizer.",
    ),
]
