# 统一调度 Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 实现只管理任务、进度、交接和恢复的项目级调度 Agent，完整开发任务默认推进到本地开发信草稿。

**Architecture:** 主对话承载调度角色，专业子 Agent承担业务执行和质量判断。调度工具仅处理明确的任务字段、专业 Agent提交的去向、文件引用与状态；不联网、不调用模型、不自行研究公司。事件记录、进度快照和资源占用记录支持中断恢复与防止重复派发。

**Tech Stack:** Python 3.10+标准库、TOML、Markdown、JSON/JSONL；Windows中文路径。角色TOML检查使用当前环境Python的tomllib。

**Spec:** [统一调度 Agent 设计稿](workflow-coordinator-design.md)。用户已同意设计及推荐的当前对话顺序实施、最终独立审查方式。实施证据见[执行记录](validation-evidence/2026-10-22-workflow-coordinator/progress.md)。

## Global Constraints

- “调度 Agent 只管理任务、进度、交接、阻塞和恢复。”业务判断及质量检查全部保留在专业 Agent。
- “默认终点为开发信草稿完成。”本地草稿不等于邮箱草稿箱写入；发送对接以后另行设计，本计划不增加发送接口。
- “首版一个工作流只派一个专业执行者，按阶段批次推进。”专业 Agent不嵌套派生。
- “首版只在 released=true 后派发后续工作。”运行中进度不是阶段交接。
- 范围、执行状态、业务去向分开；来源名单变化不自动扩大授权范围。按客户ID处理重复，主体匹配问题交回专业 Agent。
- 联系人与撰写Agent当前未接入；开发调度不等于开发这些业务Agent，不以主调度代替缺失阶段。
- 不为调度再设业务审核门槛，不读取报告正文评估质量，不重跑专业Agent的业务检查器。
- 持久化未知派发与未知消耗；恢复不重新派发未知任务、不重置预算、不自动抢占活跃执行者。
- 本地开发不运行真实市场、Apollo、邮箱、外部写入或定时任务，不安装全局Skill、不推送GitHub。
- 当前根目录不是Git仓库；不为本任务初始化Git或建工作树。实施前保存本次拟修改文件的独立快照与SHA-256，任务检查点代替Git提交；保留其他对话的并行改动。
- 文档沿用项目docs/agent-team目录；当前任务不读取共享知识库及历史备份规则。

## Review Focus

1. 上游总表65家而本次仅新增5家：只采用明确授权的5家；测试归Task 1。
2. 派发成功但调用回执丢失：保留未知并查原执行者，不能自动派第二次；测试归Task 1/2。
3. 交接重复、旧版本迟到和同ID不同内容：分别幂等、保留历史、拒绝覆盖；测试归Task 1/2。
4. 占用登记或事件已写但后续保存失败：保持保守占用、恢复记录，不重复业务动作；测试归Task 2。
5. 同公司路径大小写/相对路径变化或两个工作流竞争：认定同一资源，只允许一个认领者；测试归Task 2。

---

## 文件与职责

以下均为预计实施文件，除本计划及设计稿外尚未创建。

| 文件 | 职责 |
| --- | --- |
| `.codex/agents/workflow-coordinator.toml` | 主对话调度角色、工具调用顺序、阶段边界和恢复要求 |
| `skills/coordinate-prospecting-workflow/SKILL.md` | 调度入口与必要规则，链接字段规范和使用说明 |
| `skills/coordinate-prospecting-workflow/references/contracts.md` | task、assignment、handoff、state和事件字段、枚举、固定路由 |
| `skills/coordinate-prospecting-workflow/references/execution.md` | 调用、资源认领、派发未知、交接纠正与恢复操作 |
| `skills/coordinate-prospecting-workflow/scripts/workflow_model.py` | 无文件写入的字段校验、状态变更、下一项与统计 |
| `skills/coordinate-prospecting-workflow/scripts/workflow_store.py` | 事件、快照、资源锁、版本及恢复；不包含业务路由判断 |
| `skills/coordinate-prospecting-workflow/scripts/workflow_cli.py` | 命令入口、文件引用检查、输出JSON和进度Markdown |
| 同scripts目录的`test_model.py`、`test_store.py`、`test_cli.py` | 各组件针对性回归，只用虚构临时数据 |
| 同scripts目录的`test_support.py` | 小型虚构task/assignment/handoff构造函数，避免重复夹具 |
| `docs/agent-team/workflow-coordinator.md` | 项目使用方式、进度口径和当前未接入能力 |
| `docs/agent-team/workflow-coordinator-validation.md` | 实际验证证据及未验证事项 |

预计修改：`AGENTS.md`、`README.md`、现有两个角色TOML。只增加全流程入口及显式受调度任务的交接规则；不改专业Skill的业务SOP、检查器和历史报告。

依赖顺序：Task 1 → Task 2 → Task 3 → Task 4。运行工具时项目路径与工作流路径均显式传入，测试不能默认写真实markets。

## Task 1: 字段契约与确定的进度变更

**Files:** 新建contracts.md、workflow_model.py、test_model.py、test_support.py。

**Interfaces:**

- `validate_task(task: dict) -> None`；非法输入抛ValueError并给出字段名。
- `new_state(task: dict) -> dict`：建立schema=1状态，不生成公司事实。
- `apply_command(state: dict, command: dict) -> dict`：返回新状态，不修改原参数、不做I/O。
- `summarize(state: dict) -> dict`：返回各阶段计数、公司流程结果、草稿文件数、目标缺口与next_action。
- 测试辅助：`make_task(**overrides) -> dict`、`make_assignment(**overrides) -> dict`、`make_handoff(**overrides) -> dict`；返回可独立修改的合法虚构对象。

**锁定字段与操作：**

- task必含`schema, workflow_id, country, request_ref, entry_stage, target_stage, scope, order, capabilities, budgets, overall_budgets`。默认target_stage=draft；明确阶段任务按其终点，阶段枚举仅market/research/contacts/draft。
- scope含`mode, requested_count, baseline_ids, selected_ids, source_artifacts`。mode为discovery_new或explicit_ids。前者由market交接明确selected_ids后冻结；当用户明确“新增K家进入后续”时，选择最多K个不在baseline_ids内的ID，多余发现保留在市场成果不静默交给下游。explicit_ids模式不接受交接新增ID。
- `capabilities`为阶段到`{available, role_path, role_version}`的映射。缺能力默认false；测试中的模拟能力须显式声明，不写入真实项目能力表。
- budget按`budget_id, stage, unit, limit, used, unknown, authorization_ref`记录；limit=null表示用户未设硬性上限，unknown=true不能推算精确余额。整体预算按同unit分配；已有消耗和已预留额度都占用上限。
- 所有变更command必含`command_id, op, recorded_at`，时间为调用端生成的带时区时间，不接受补造过去执行时刻；command_id重复且内容一致返回原结果，不新增任务。
- op固定为`init_scope, prepare, dispatched, progress, receive, reconcile_dispatch, reopen, source_change, pause, resume, cancel, close`。本计划不增加通用任意状态patch。
- prepare含完整assignment：`assignment_id, revision, stage, customer_ids, input_artifacts, owner, allowed_routes, budget_reservations, resources`。一个工作流只允许一个未释放派发；其执行状态依设计稿waiting/queued/running/completed/blocked/cancelled。
- dispatched记录真实`executor_ref`；未收到回执的prepare保持dispatch_unknown。reconcile_dispatch必须给出`resolution`为existing_executor/not_dispatched及真实查证引用；前者接续原assignment，后者解除该次派发意图后才能重新准备，不扣回已确认消耗。
- receive含完整handoff：`handoff_id, assignment_id, revision, producer, stage, issued_at, batch_status, released, items, budget_used, uncertainty`。每个item必含`customer_id, execution_status, business_conclusion, conclusion_ref, route, next_stage, route_reason, resume_condition, artifacts`；完成草稿另含`draft_ids`及对应文件映射。执行状态与业务去向分开。
- 交接技术结果为accepted/needs_correction/unknown；文件检查结果由Task 3提供，不允许接收未检查的完成交接。语义结论只保存与传递。
- reopen须提供新输入版本或恢复条件已改变的引用；同公司/阶段/问题/输入版本未变化时拒绝重复补核。source_change只登记受影响ID与版本，不自动扩队或重做下游。
- close必须满足设计稿闭合条件，或带用户明确关闭未完成任务的指令引用；数量未达标、hold/end/cancelled不报告“全部草稿完成”。

- [x] **Step 1: 编写合法虚构夹具及Task 1失败测试。** 明确断言：默认draft、显式market只到market；65条基线下仅交接选定5条；越界ID不入队；research completed+revisit不进contacts；相同专业结论不因正文长短改变路由（模型根本不接收正文）；未released不派下游。
- [x] **Step 2: 运行失败基线。** `python -X utf8 -m unittest discover -s skills/coordinate-prospecting-workflow/scripts -p test_model.py -v`；预期因实现缺失失败，不声称已验证业务。
- [x] **Step 3: 实现上述纯函数及contracts.md。** 路由advance/revisit/hold/end/finish只按结构化字段处理；终点必须属于任务卡。现有背调四种明确结论的固定映射由专业交接适配填写；模型不从自由文本推断。
- [x] **Step 4: 加入并通过恢复与预算测试。** 断言prepare回执未知阻止二次prepare；重复handoff无第二个下游任务；旧revision保留历史且不覆盖；同handoff_id不同内容拒绝。缺能力blocked且目标仍draft；hold不阻止其他公司；无新条件不reopen；未知消耗阻止受限派发；整体额度预留和已用之和不越限；不同阶段/单位不混算。
- [x] **Step 5: 验证汇总边界。** 零目标不报100%；一家公司三份草稿计1家公司/3份；市场数量缺口与草稿完成分别保留；暂停不取消已执行动作；用户缩小范围只取消尚待范围，运行项标待停止并等待执行者回报，不伪称立即中止。重复运行Step 2命令，预期全部通过。
- [x] **Step 6: 保存本任务检查点。** 在开发验证记录记失败/通过命令及实际结果，不修改真实工作流。

## Task 2: 持久化、资源认领与恢复

**Files:** 新建workflow_store.py、test_store.py，扩充contracts.md的记录部分。

**Interfaces:**

- `canonical_resource(project: Path, kind: str, value: str) -> str`：规范project内路径及资源ID，kind为pool/batch/company。
- `claim_resources(project: Path, workflow: Path, assignment_id: str, resources: list[str]) -> None`。
- `release_resources(project: Path, workflow: Path, assignment_id: str, release_ref: str) -> None`。
- `load_state(workflow: Path) -> dict`：只读核对事件与快照，不暗中修复。
- `commit_command(project: Path, workflow: Path, command: dict) -> dict`：串行提交及维护资源占用。
- `recover_workflow(project: Path, workflow: Path) -> dict`：重建落后的快照与派发文件，保留未知业务执行和资源占用。

**记录决定：**

- 项目资源表固定在`.codex/workflow-runtime/resource-owners.json`，互斥锁`.codex/workflow-runtime/.registry.lock`；工作流锁为其目录`.writer.lock`。统一按项目锁→工作流锁顺序获取；锁冲突直接返回结构化错误，不自动移除旧锁。
- 资源表存workflow绝对路径、assignment_id、资源键、owner和认领时间。country池按ISO2键；公司资源优先按国家+稳定客户ID，实际报告路径同时认领。路径用resolve及Windows大小写规范；相对/绝对、大小写及可解析链接指向相同路径时不能重复认领。
- 派发前先在项目锁内认领资源并持久保存，再提交工作流prepare事件。任何后续失败都保留认领，不在异常处理中自动释放；恢复时对照assignment_id和执行情况核实。释放必须有released交接或明确未派发/已结束的查证引用；不凭进程ID或时间长短抢占。
- events.jsonl每行含`schema, seq, event_id, recorded_at, command, state_after`；首版小批量采用完整状态快照随事件保存，避免不完整事件不能恢复。仅实际状态变更追加，轮询不写事件。
- 顺序：验证→追加事件并flush/fsync→原子替换state.json→落盘不可变assignment/handoff文件→更新正式进度。相同command_id重试先对账；快照或交接文件缺失可由已提交事件恢复，不重新调用外部业务。正式进度写入由Task 3接续；记录未齐全时禁止新prepare。
- 缺事件但资源已认领时保留为待核对占用；事件尾行截断、序号冲突或不可重放时拒绝继续写，保留原字节；不自动截短。未知锁恢复只在查证原写入者已结束后由执行规范明确处理。
- 已提交assignment/handoff不可覆盖。state替换前保留history快照；派发和交接同ID不同内容拒绝写入。所有文件只允许写入指定工作流或项目运行记录目录，不写业务报告。

- [x] **Step 1: 编写临时中文目录的失败测试。** 两个工作流认领同公司只允许一个；路径大小写/相对写法一致；旧锁不抢占；assignment_id重复不重复占用。增加两个真实独立进程竞争同资源的测试，断言恰好一个成功。
- [x] **Step 2: 运行失败基线。** `python -X utf8 -m unittest discover -s skills/coordinate-prospecting-workflow/scripts -p test_store.py -v`；预期实现缺失或预期保护未发生。
- [x] **Step 3: 实现资源记录和事件保存接口。** 仅标准库；锁使用排他文件创建，原子替换在同目录临时文件完成。禁止工具网络调用。
- [x] **Step 4: 加入断点失败测试并修复。** 注入资源已认领/prepare尚未落盘、事件已写/state尚未替换、state已写/assignment文件缺失三个失败点；恢复后事件不重复、认领不误释放、不会产生第二次派发。截断journal和同seq不同内容拒绝，原字节保留。
- [x] **Step 5: 验证释放和历史。** released交接只释放本assignment占用；旧结果不可释放新assignment；跨工作流active状态不能伪装结束；历史快照独立且指纹正确。运行Task 1和Task 2测试，预期全部通过。
- [x] **Step 6: 保存本任务验证检查点。** 明确并发测试的覆盖范围，不声明能阻止未使用该资源表的旧任务写入。

## Task 3: 可使用的CLI与正式进度输出

**Files:** 新建workflow_cli.py、test_cli.py、references/execution.md。

**Interfaces:**

- `validate_artifacts(project: Path, artifacts: list[dict]) -> list[dict]`：核对path/sha256是否存在、可读且版本一致，返回结构化错误；不检查章节、事实、邮箱或文案。
- `render_progress(workflow: Path, state: dict) -> None`：输出设计稿的01_任务与进度.md、02_交接与待办.md，来源为state；不渲染或改写业务报告。
- CLI：`python -X utf8 .../workflow_cli.py --project <项目目录> --workflow <工作流目录> (--input <UTF-8 JSON> | --check | --recover)`。
- `--input`支持init及Task 1的固定操作。init输入含task；不覆盖已有工作流。项目、工作流路径由CLI参数确定，payload不能指定任意写入目标。
- 返回码0=本次记录成功或所选检查通过；1=非法输入、文件错误或资源冲突；2=有待恢复的持久化/派发未知/源版本问题。业务hold、终止或未接入能力本身不等于CLI故障，须读取状态而非把返回0当全流程完成。
- `--check`只读，输出schema、status、counts、next_action、blocked_reasons、technical_issues；`--recover`仅恢复调度记录，不修正专业报告或重做外部动作。
- 所有输出JSON含`scope: progress_and_handoff_only`；包含任务和公司完成口径、预算未知、未接入能力、结果文件及恢复位置。

- [x] **Step 1: 编写真实子进程CLI失败测试。** 覆盖中文路径、JSON BOM、非法JSON、同ID不同内容、目录穿越或工作流外写入拒绝、缺少文件/版本不符返回1。对正文完全不同但指纹各自匹配、结论相同的两份模拟报告，断言路由完全相同。
- [x] **Step 2: 运行失败基线。** `python -X utf8 -m unittest discover -s skills/coordinate-prospecting-workflow/scripts -p test_cli.py -v`，预期CLI不存在或指定行为失败。
- [x] **Step 3: 实现CLI、文件引用检查及进度渲染。** workflow必须在显式项目的markets/<ISO2>/workflows中；读取引用允许项目内已声明来源；测试项目根目录为临时目录。输入文件可由用户放在工作目录；实现不把其内容作为shell命令。角色/Skill外部依赖由主对话加载，CLI不读取邮箱配置或凭据。
- [x] **Step 4: 加入正式报告写入失败的测试。** 事件已保存但Markdown失败时返回2并阻止新派发；--recover据state重建文档后解除，既有assignment_id不变。--check不改变任何已有字节。
- [x] **Step 5: 用CLI跑3家公司模拟流程。** 明确虚构国家XX：一家模拟finish、一家专业hold、一家contacts能力未接入；预期draft_done=1/on_hold=1/active=1、工作流未全部完成，blocked项有dependency_unavailable。补一组所有任务闭合但含hold的情境，closed可以成立但不得报告全部草稿完成。
- [x] **Step 6: 写execution.md并跑完整新增测试。** 命令`python -X utf8 -m unittest discover -s skills/coordinate-prospecting-workflow/scripts -p 'test_*.py' -v`，预期全部通过。说明没有自主后台进程，资源锁异常须查证后处理，执行者未知不能自动重派。

## Task 4: 角色接入、使用说明和独立验证

**Files:** 新建调度TOML、SKILL.md、使用说明、验证记录；修改AGENTS.md、README.md及现有market/customer角色的明确调度交接段落。

**Interfaces:**

- 主对话加载完整workflow_coordinator指令；调用专业子Agent前传完整专业角色、assignment及输出位置。普通业务单阶段入口继续保持现有路由。
- 只有传入有效调度assignment的调用才采用统一handoff；独立调用现有专业Agent的输出不受新增交接字段影响。
- market适配返回本次范围内selected_ids、原五状态、产出报告和路由，不把整个累计池交下游。
- research适配显式customer_ids覆盖原“全部valid”默认；采用专业阶段已有四种明确结论固定填route。缺明确结论时返回交接待补，不由调度猜测。
- 两个专业Agent仍负责自己的自检、预算、日志和阶段报告；提交不可变handoff后释放本次任务资源，不自行继续下游。

- [x] **Step 1: 实施前保存拟改已有文件快照。** 范围只含AGENTS.md、README.md、两个角色和本任务文档；记录SHA，不递归搬动项目。核对实施时新增并行改动，按当前内容局部修改。
- [x] **Step 2: 编写精简角色和Skill。** SKILL.md只放触发条件、进度边界、执行循环与references链接；不复制业务SOP。不增加邮箱、发送、质量评分或自动市场研究工具。
- [x] **Step 3: 修改现有角色交接说明及项目入口。** 全流程入口默认draft，明确“只搜集/只背调”不扩大范围；所有商业去向由生产者填写。将职责边界和未接入能力写入使用说明。
- [x] **Step 4: 检查配置与原业务约束。** Python解析三个角色TOML；运行skill-creator的quick_validate.py检查新Skill；逐一确认引用路径。检查器输出/角色指令均不得含调度业务评分、调度重新审查质量、发送入口。
- [x] **Step 5: 独立离线使用验证。** 实施方式确定后安排独立执行者读取完整角色和规范，在临时项目用真实CLI验证设计稿16个验收场景；market/research使用模拟业务交接，contacts/draft明确模拟。不联网、不触碰真实市场资料。保存输入、stdout、退出码、指纹及人工复核至docs/agent-team/validation-evidence/2026-10-22-workflow-coordinator/。
- [x] **Step 6: 整体审查与必要修复。** 独立审查只检查实现是否符合本设计，不扩大为市场业务质量审计；问题先复现再修复，运行受影响测试。
- [x] **Step 7: 最终验证并交付。** 新增测试全部通过；既有市场日志和背调检查器回归各跑一次，确认局部接口说明未破坏原有用法；核对本任务未写真实markets业务文件。记录文件检查、自动测试、独立模拟的不同结论，明确真实业务调度尚未试跑。

## 设计覆盖与计划自检

| 设计内容 | 负责实现 |
| --- | --- |
| §1–3职责与首版方式 | Task 1结构不接收业务正文；Task 4角色约束及独立验证 |
| §4任务入口与范围 | Task 1 scope/终点；Task 4主对话路由 |
| §5–7交接、去向、完成口径 | Task 1模型；Task 3机械文件检查与计数输出 |
| §8–9持久化、资源、恢复 | Task 2与Task 3失败恢复 |
| §10预算与授权 | Task 1预算模型；Task 4传递授权引用和工具阻塞 |
| §11现有角色适配 | Task 4显式assignment分支，不改业务SOP |
| §12全部验收场景 | Task 1–3针对性测试＋Task 4独立离线应用 |

计划自检：四任务顺序依赖明确；所有脚本接口有生产者与消费者；Review Focus五项均有对应测试；第一版缺失能力保持显式阻塞；无实现发送或调度质量判断的任务。锁/业务执行未知/文件已保存但进度落后均明确保守恢复；没有“检查返回0即所有业务完成”的混淆。

建议执行方式：由主Agent在当前会话顺序实施，完成后独立审查。四个任务共享状态契约和持久化接口，顺序执行便于保持一致，也避免每任务重复加载上下文；独立离线使用验证仍保留。也可选择逐任务由子Agent实施并逐项独立审查，检查更密集但开销更高。

本计划已完成本地实施与最终核对；偏差、审查修复和验证边界以执行记录和验证报告为准。
