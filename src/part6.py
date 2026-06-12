"""Content for Part 6 (productionization): lessons 23–25.

Verified against AgentScope 2.0 source (app/_app.py, app/_types.py,
app/message_bus/_base.py, app/_tools/, examples/agent_service).
"""

from i18n import (
    lead, h2, h3, p, card, code, table, accordion, keypoints,
    source_map, analogy, note, tip, important, highlight, blocks, t,
)

# ---------------------------------------------------------------------------
# Lesson 23 — Agent Service
# ---------------------------------------------------------------------------
LESSON_23 = blocks(
    lead(
        "把单个 agent 升级成可部署的<strong>服务</strong>：<code>create_app(...)</code> 返回一个 "
        "FastAPI 应用，内置多租户、多会话隔离，并把 agent 的事件流接到前端。",
        "Turn a single agent into a deployable <strong>service</strong>: "
        "<code>create_app(...)</code> returns a FastAPI app with built-in multi-tenancy and "
        "multi-session isolation, wiring the agent's event stream to a frontend.",
    ),
    analogy(
        "前面几课像在自家厨房做菜；本课是开一家<strong>餐厅</strong>：要同时接待很多客人"
        "（多租户）、每桌各点各的（多会话），还要有前台、传菜和后厨调度。",
        "Earlier lessons were cooking in your own kitchen; this one opens a "
        "<strong>restaurant</strong>: serve many guests at once (multi-tenancy), each table "
        "with its own orders (multi-session), plus a front desk, runners and kitchen dispatch.",
    ),
    h2("create_app", "create_app"),
    p(
        "<code>create_app</code> 需要三个基础设施后端：<strong>存储</strong>（会话/状态持久化）、"
        "<strong>消息总线</strong>（事件分发，见下一课）、<strong>工作区管理器</strong>"
        "（为每个会话提供隔离的执行环境）。其余都是可选扩展点。",
        "<code>create_app</code> takes three infrastructure backends: <strong>storage</strong> "
        "(session/state persistence), a <strong>message bus</strong> (event dispatch — next "
        "lesson), and a <strong>workspace manager</strong> (an isolated execution environment "
        "per session). Everything else is an optional extension point.",
    ),
    code(
        "from agentscope.app import create_app\n"
        "import uvicorn\n\n"
        "app = create_app(\n"
        "    storage=RedisStorage(),\n"
        "    message_bus=RedisMessageBus(),\n"
        "    workspace_manager=LocalWorkspaceManager(),\n"
        "    # optional extension points:\n"
        "    custom_subagent_templates=[...],   # team blueprints (lesson 25)\n"
        "    extra_agent_tools=...,\n"
        '    title="AgentScope",\n'
        ")\n"
        'uvicorn.run(app, host="0.0.0.0", port=8000)',
        cap_zh="独立启动：create_app 返回一个标准 FastAPI 应用。",
        cap_en="Standalone: create_app returns a standard FastAPI app.",
    ),
    accordion(
        "挂载到已有的 FastAPI 应用",
        "Mounting onto an existing FastAPI app",
        blocks(
            code(
                "root = FastAPI()\n"
                "agentscope_app = create_app(\n"
                "    storage=RedisStorage(),\n"
                "    message_bus=RedisMessageBus(),\n"
                "    workspace_manager=LocalWorkspaceManager(),\n"
                ")\n"
                'root.mount("/agentscope", agentscope_app)',
                cap_zh="作为子应用挂载，与你现有服务共存。",
                cap_en="Mount as a sub-app alongside your existing service.",
            ),
        ),
        num=1,
    ),
    p(
        "可选参数支持注入：额外凭证类型、FastAPI 中间件、每个 agent 的中间件与工具、"
        "自定义 agent 类，以及<strong>子代理模板</strong>（<code>SubAgentTemplate</code>，"
        "供 Agent Team 使用，见第 25 课）。",
        "Optional parameters let you inject: extra credential types, FastAPI middlewares, "
        "per-agent middlewares and tools, a custom agent class, and "
        "<strong>sub-agent templates</strong> (<code>SubAgentTemplate</code>, used by Agent "
        "Team — lesson 25).",
    ),
    source_map([
        ("app/_app.py", "<code>create_app(storage, message_bus, workspace_manager, ...)</code>",
         "<code>create_app(storage, message_bus, workspace_manager, ...)</code>"),
        ("app/__init__.py", "导出 <code>create_app</code> 与 <code>SubAgentTemplate</code>",
         "exports <code>create_app</code> and <code>SubAgentTemplate</code>"),
        ("app/_service/_session.py", "会话级服务逻辑（多会话隔离）",
         "session-level service logic (multi-session isolation)"),
        ("examples/agent_service", "可运行的服务示例（<code>main.py</code>）",
         "a runnable service example (<code>main.py</code>)"),
    ]),
    important(
        "运行前置条件：服务自带的 <strong>storage 与 message_bus 实现是 Redis-only</strong>"
        "（只有 workspace 有本地实现）。需要先跑起 Redis（如 "
        "<code>docker run -p 6379:6379 redis:7</code>），安装 <code>agentscope[full]</code>，"
        "后端从 <code>agentscope.app.storage</code> / <code>.message_bus</code> / "
        "<code>.workspace_manager</code> 导入；Web UI（<code>examples/web_ui</code>）需 Node ≥ 20。",
        "Runtime prerequisites: the shipped <strong>storage and message_bus implementations are "
        "Redis-only</strong> (only the workspace has a local backend). Run Redis first (e.g. "
        "<code>docker run -p 6379:6379 redis:7</code>), install <code>agentscope[full]</code>, "
        "and import the backends from <code>agentscope.app.storage</code> / "
        "<code>.message_bus</code> / <code>.workspace_manager</code>; the Web UI "
        "(<code>examples/web_ui</code>) needs Node ≥ 20.",
    ),
    highlight(
        "三大后端都是<strong>统一接口</strong>：工作区已有本地/Docker/E2B 多种实现，存储与消息总线"
        "目前只有 Redis 实现——接口留出了扩展空间，未来可接入更多后端。",
        "All three backends sit behind <strong>uniform interfaces</strong>: the workspace already "
        "has local/Docker/E2B implementations, while storage and the message bus ship only Redis "
        "today — the interfaces leave room to plug in more backends later.",
    ),
    keypoints([
        ("<code>create_app</code> 返回标准 FastAPI 应用，可独立运行或挂载。",
         "<code>create_app</code> returns a standard FastAPI app you can run standalone or mount."),
        ("三大后端：<strong>storage · message_bus · workspace_manager</strong>。",
         "Three backends: <strong>storage · message_bus · workspace_manager</strong>."),
        ("多租户 + 多会话隔离是内置能力。",
         "Multi-tenancy + multi-session isolation are built in."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 24 — Message Bus
# ---------------------------------------------------------------------------
LESSON_24 = blocks(
    lead(
        "<strong>消息总线（MessageBus）</strong>是服务的中枢神经：它把 agent 事件 "
        "<strong>发布 / 订阅</strong>给前端，并提供分布式的<strong>注册表</strong>与"
        "<strong>后台任务</strong>追踪、跨 worker 取消。",
        "The <strong>MessageBus</strong> is the service's nervous system: it "
        "<strong>publishes/subscribes</strong> agent events to the frontend and provides a "
        "distributed <strong>registry</strong> plus <strong>background-task</strong> tracking "
        "and cross-worker cancellation.",
    ),
    analogy(
        "像一个<strong>广播电台 + 公告栏</strong>：agent 把进展广播出去（publish），前端调台收听"
        "（subscribe）；公告栏（registry）记录「谁在跑什么任务」，任何 worker 都能查到并叫停。",
        "Like a <strong>radio station + notice board</strong>: agents broadcast progress "
        "(publish), frontends tune in (subscribe); the notice board (registry) records \"who "
        "is running what\", and any worker can look it up and stop it.",
    ),
    h2("三组能力", "Three groups of capability"),
    table(
        [("能力", "Capability"), ("方法（节选）", "Methods (selected)")],
        [
            [("发布 / 订阅事件", "Publish / subscribe events"),
             ("<code>publish</code>、<code>subscribe</code>",
              "<code>publish</code>, <code>subscribe</code>")],
            [("分布式注册表", "Distributed registry"),
             ("<code>registry_set</code> / <code>registry_getall</code> / "
              "<code>registry_del</code> / <code>registry_exists</code> / <code>registry_drop</code>",
              "<code>registry_set</code> / <code>registry_getall</code> / "
              "<code>registry_del</code> / <code>registry_exists</code> / <code>registry_drop</code>")],
            [("后台任务 + 唤醒/取消", "Background tasks + wakeup/cancel"),
             ("<code>bg_task_register</code> / <code>bg_task_list</code> / "
              "<code>bg_task_purge</code>、<code>subscribe_wakeup_signal</code>",
              "<code>bg_task_register</code> / <code>bg_task_list</code> / "
              "<code>bg_task_purge</code>, <code>subscribe_wakeup_signal</code>")],
        ],
    ),
    p(
        "这套原语正是 README 里那些能力的底座：<strong>后台任务卸载</strong>（长任务转后台、"
        "完成后唤醒 agent 继续对话）与<strong>跨 worker 取消</strong>（一个进程发起取消，"
        "另一个正在执行的进程能收到并停下）。",
        "These primitives underpin the README features: <strong>background-task offloading</strong> "
        "(a long task goes to the background and later wakes the agent to resume) and "
        "<strong>cross-worker cancellation</strong> (one process issues a cancel and another, "
        "mid-execution, receives it and stops).",
    ),
    code(
        "# 通常由服务内部使用；形态如下 / used internally by the service:\n"
        "await bus.publish(session_id, event)        # 广播一个事件 / broadcast an event\n"
        "async for event in bus.subscribe(session_id):\n"
        "    push_to_frontend(event)                 # 前端实时接收 / live to frontend\n\n"
        'await bus.registry_set("bg_tasks", task_id, info)   # 记录后台任务 / record a task\n'
        'tasks = await bus.registry_getall("bg_tasks")       # 任意 worker 可查 / any worker can read',
        cap_zh="发布/订阅 + 注册表原语（方法均为 async）。",
        cap_en="Publish/subscribe + registry primitives (all async).",
    ),
    note(
        "目前只提供 <code>RedisMessageBus</code> 这一实现（面向多进程 / 分布式部署）。"
        "<code>MessageBus</code> 是统一接口，未来可据此接入更轻量（本地 / 单进程）的实现。",
        "Only the <code>RedisMessageBus</code> implementation ships today (for multi-process / "
        "distributed deployments). <code>MessageBus</code> is the uniform interface, designed so "
        "lighter (local / single-process) buses can be added later.",
    ),
    source_map([
        ("app/message_bus/_base.py",
         "<code>MessageBus</code>：<code>publish</code>/<code>subscribe</code>、"
         "<code>registry_*</code>、<code>bg_task_*</code>、唤醒/取消原语",
         "<code>MessageBus</code>: <code>publish</code>/<code>subscribe</code>, "
         "<code>registry_*</code>, <code>bg_task_*</code>, wakeup/cancel primitives"),
        ("app/message_bus/_redis_message_bus.py", "Redis 实现（分布式）",
         "the Redis implementation (distributed)"),
        ("app/_manager/_cancel_dispatcher.py", "跨 worker 取消的分发",
         "dispatching cross-worker cancellation"),
    ]),
    keypoints([
        ("消息总线 = <strong>发布/订阅 + 注册表 + 后台任务/取消</strong>。",
         "The bus = <strong>pub/sub + registry + background tasks/cancel</strong>."),
        ("它支撑后台任务卸载与跨 worker 取消等分布式能力。",
         "It powers distributed features like background-task offloading and cross-worker cancel."),
        ("目前仅 <code>RedisMessageBus</code> 一种实现；接口统一，未来可扩展。",
         "Only <code>RedisMessageBus</code> ships today; the interface is uniform and extensible."),
    ]),
)

# ---------------------------------------------------------------------------
# Lesson 25 — Agent Team
# ---------------------------------------------------------------------------
LESSON_25 = blocks(
    lead(
        "<strong>Agent Team</strong> 让一个<strong>领导 agent</strong> 动态<strong>创建并协调</strong>"
        "多个工作 agent：通过内置的「团队工具」生成队员、分派任务、汇集结果。",
        "<strong>Agent Team</strong> lets a <strong>leader agent</strong> dynamically "
        "<strong>spawn and coordinate</strong> worker agents: it creates teammates, hands out "
        "tasks and gathers results through built-in \"team tools\".",
    ),
    analogy(
        "像一位<strong>项目负责人</strong>：自己不写全部代码，而是按需招募「研究员」「程序员」等"
        "角色（按模板），分配任务、互相沟通，最后汇总交付。",
        "Like a <strong>project lead</strong>: instead of doing everything alone, they recruit "
        "roles like \"researcher\" or \"coder\" on demand (from templates), assign tasks, "
        "communicate, and assemble the final delivery.",
    ),
    h2("团队工具", "The team tools"),
    table(
        [("工具", "Tool"), ("作用", "Purpose")],
        [
            [("<code>TeamCreate</code>", "<code>TeamCreate</code>"),
             ("创建一个团队", "create a team")],
            [("<code>AgentCreate</code>", "<code>AgentCreate</code>"),
             ("按 <code>subagent_type</code> 模板生成一个工作 agent",
              "spawn a worker agent from a <code>subagent_type</code> template")],
            [("<code>TeamSay</code>", "<code>TeamSay</code>"),
             ("领导通过 <code>to=name</code> 向某个队员发消息",
              "the leader messages a teammate via <code>to=name</code>")],
            [("<code>TeamDelete</code>", "<code>TeamDelete</code>"),
             ("解散团队 / 回收资源", "disband a team / reclaim resources")],
        ],
    ),
    h2("SubAgentTemplate：队员蓝图", "SubAgentTemplate: the worker blueprint"),
    p(
        "你在 <code>create_app(custom_subagent_templates=[...])</code> 处注册若干 "
        "<code>SubAgentTemplate</code>。每个模板的 <code>type</code> 字段（如 "
        "<code>'researcher'</code>）会成为 <code>AgentCreate</code> 工具里 "
        "<code>subagent_type</code> 参数的一个可选值，<code>description</code> 则告诉模型该类型"
        "适合干什么。",
        "You register <code>SubAgentTemplate</code>s at "
        "<code>create_app(custom_subagent_templates=[...])</code>. Each template's "
        "<code>type</code> field (e.g. <code>'researcher'</code>) becomes an allowed value of "
        "the <code>subagent_type</code> parameter in the <code>AgentCreate</code> tool, and "
        "<code>description</code> tells the model what that type is good for.",
    ),
    code(
        "from agentscope.app import SubAgentTemplate\n\n"
        "templates = [\n"
        "    SubAgentTemplate(\n"
        '        type="researcher",\n'
        '        description="Searches and summarizes information.",\n'
        "        # ...further pure-data config (model, tools, prompt, ...)\n"
        "    ),\n"
        "]\n"
        "# passed in at startup:\n"
        "# create_app(..., custom_subagent_templates=templates)",
        cap_zh="注册一个「研究员」队员蓝图，供领导按需生成。",
        cap_en="Register a 'researcher' worker blueprint for the leader to spawn on demand.",
    ),
    accordion(
        "领导与队员如何协作？",
        "How do leader and workers collaborate?",
        blocks(
            p(
                "领导 agent 调用 <code>AgentCreate(subagent_type=\"researcher\", name=\"r1\")</code> "
                "生成一个队员，再用 <code>TeamSay(to=\"r1\", ...)</code> 分派任务；队员完成后把结果"
                "回传，领导汇总。整个过程仍以<strong>事件流</strong>对外播报，前端可见每个队员的进展。",
                "The leader calls <code>AgentCreate(subagent_type=\"researcher\", name=\"r1\")</code> "
                "to spawn a worker, then <code>TeamSay(to=\"r1\", ...)</code> to assign work; the "
                "worker returns its result and the leader aggregates. The whole process is still "
                "narrated over the <strong>event stream</strong>, so a frontend sees each "
                "worker's progress.",
            ),
        ),
        num=1,
    ),
    source_map([
        ("app/_tools/_team_create.py", "<code>TeamCreate</code> 团队工具",
         "the <code>TeamCreate</code> team tool"),
        ("app/_tools/_agent_create.py", "<code>AgentCreate</code>：按模板生成队员",
         "<code>AgentCreate</code>: spawn a worker from a template"),
        ("app/_tools/_team_say.py", "<code>TeamSay</code>：向队员发消息",
         "<code>TeamSay</code>: message a teammate"),
        ("app/_types.py", "<code>SubAgentTemplate</code> 队员蓝图（纯数据、可序列化）",
         "<code>SubAgentTemplate</code>: the worker blueprint (pure data, serializable)"),
    ]),
    highlight(
        "团队协作不是写死的编排，而是<strong>暴露成工具</strong>交给领导 agent 自己决定何时招人、"
        "分派什么——再次体现「放大模型能力，而非约束它」的设计哲学。",
        "Team collaboration isn't hard-wired orchestration; it's <strong>exposed as tools</strong> "
        "for the leader agent to decide when to recruit and what to delegate — again reflecting "
        "\"amplify the model, don't constrain it\".",
    ),
    keypoints([
        ("领导 agent 用团队工具（<code>TeamCreate</code>/<code>AgentCreate</code>/<code>TeamSay</code>）动态组队。",
         "The leader uses team tools (<code>TeamCreate</code>/<code>AgentCreate</code>/<code>TeamSay</code>) to form a team on the fly."),
        ("<code>SubAgentTemplate</code> 是队员蓝图，在 <code>create_app</code> 处注册。",
         "<code>SubAgentTemplate</code> is the worker blueprint, registered at <code>create_app</code>."),
        ("协作过程仍走统一事件流，全程可观测。",
         "Collaboration still flows over the unified, observable event stream."),
    ]),
)


LESSONS = {
    "23-agent-service.html": LESSON_23,
    "24-message-bus.html": LESSON_24,
    "25-agent-team.html": LESSON_25,
}


QUIZZES: dict = {}

QUIZZES["23-agent-service.html"] = [
    (
        "关于 <code>create_app</code> 三大后端自带的实现，下列哪项正确？",
        "Which statement about the backend implementations shipped with "
        "<code>create_app</code> is correct?",
        [
            ("<code>storage</code> 与 <code>message_bus</code> 目前只有 Redis 实现，"
             "只有 <code>workspace_manager</code> 有本地后端",
             "<code>storage</code> and <code>message_bus</code> ship Redis-only today; "
             "only <code>workspace_manager</code> has a local backend", True),
            ("三大后端都有本地实现，不依赖 Redis 也能直接跑起来",
             "All three backends have local implementations, so you can run without Redis",
             False),
            ("<code>storage</code> 有本地实现，但 <code>message_bus</code> 与 "
             "<code>workspace_manager</code> 必须用 Redis",
             "<code>storage</code> has a local backend, but <code>message_bus</code> and "
             "<code>workspace_manager</code> must use Redis", False),
        ],
        "三大后端（storage / message_bus / workspace_manager）都是统一接口，但 storage 与 "
        "message_bus 目前只发布了 Redis 实现，运行前需先启动 Redis；只有 workspace 有本地 / "
        "Docker / E2B 等实现。",
        "The three backends (storage / message_bus / workspace_manager) sit behind uniform "
        "interfaces, but storage and the message bus ship Redis-only today, so you must start "
        "Redis first; only the workspace has local / Docker / E2B implementations.",
    ),
]

QUIZZES["24-message-bus.html"] = [
    (
        "除了发布 / 订阅事件，消息总线还承担什么职责？",
        "Beyond publishing / subscribing events, what else does the message bus do?",
        [
            ("分布式注册表 + 后台任务追踪 + 跨 worker 取消",
             "A distributed registry + background-task tracking + cross-worker cancellation",
             True),
            ("它只负责事件的发布与订阅，没有其他职责",
             "Nothing else — it only publishes and subscribes events", False),
            ("持久化会话状态与记忆，取代 storage 后端",
             "Persisting session state and memory, replacing the storage backend", False),
        ],
        "<code>registry_*</code> 与 <code>bg_task_*</code> 原语让总线支撑后台任务卸载与跨 "
        "worker 取消等分布式能力；持久化会话状态是 storage 后端（第23课）的职责，并非消息总线。",
        "The <code>registry_*</code> and <code>bg_task_*</code> primitives let the bus power "
        "background-task offloading and cross-worker cancellation; persisting session state is "
        "the storage backend's job (lesson 23), not the message bus's.",
    ),
]

QUIZZES["25-agent-team.html"] = [
    (
        "领导 agent 在运行时如何获得一个工作 agent？",
        "At runtime, how does a leader agent get a worker agent?",
        [
            ("调用 <code>AgentCreate</code>，传入与已注册模板匹配的 <code>subagent_type</code>",
             "By calling <code>AgentCreate</code> with a <code>subagent_type</code> matching a "
             "registered template", True),
            ("队员是预先写死的固定角色，运行时不能动态创建",
             "Workers are hard-coded fixed roles and cannot be created at runtime", False),
            ("直接用 <code>TeamSay</code> 向一个尚不存在的名字发消息，系统会自动建好队员",
             "By calling <code>TeamSay</code> to a name that doesn't exist yet, which "
             "auto-creates the worker", False),
        ],
        "领导用 <code>AgentCreate(subagent_type=...)</code> 按 <code>SubAgentTemplate</code> "
        "动态生成队员（模板在 <code>create_app</code> 处注册）；<code>TeamSay</code> 只能向"
        "已存在的队员发消息，不会创建 agent。",
        "The leader spawns a worker dynamically with <code>AgentCreate(subagent_type=...)</code> "
        "from a <code>SubAgentTemplate</code> (registered at <code>create_app</code>); "
        "<code>TeamSay</code> only messages an existing teammate and never creates one.",
    ),
]
