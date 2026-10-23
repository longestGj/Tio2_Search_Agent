# 客户背调 Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 同步 GitHub 全部文件后，实现自动逐家背调整份市场名单、优先复用旧报告的项目级 Agent。

**Architecture:** 复用原 OGLD Skill、SOP 和报告模板；角色负责批次调度，本地补充规范负责复用、记录与恢复。增加只读批次检查器验证保存与状态一致性，不实现自动搜索调度器。

**Tech Stack:** TOML、Markdown、JSON/JSONL、Python 3.12 标准库。

**Spec:** [已确认设计](customer-research-design.md)。用户已明确要求“把 GitHub 所有文件更新到本地，然后开发”，随后要求继续；据此在当前目录连续实施，不再增加设计或计划审批。

## Global Constraints

- 每批一个执行者，逐家完成；同公司跨批次也不并发覆盖。
- 整份有效名单，复用原有背调；历史核验不冒充本次联网核验。
- 四状态 `queued/in_progress/completed/blocked`，三种方式 `reused/supplemented/new`，商业结论单独管理。
- 保留源 SOP 和报告模板；本地保存替代 Library。不安装全局、不推送、不自动发信或邮箱获取。
- 当前主项目非 Git 仓库，不创建主项目仓库/分支，不执行 Git 提交；用同步前快照与校验清单保留基线。已有本地改进及并行任务更新不得回滚。

## Review Focus

1. 同名不同国家、共享域名和历史主体：身份必须由执行者核对，检查器不代替身份判断。
2. 报告已保存而进度未保存：恢复先对账，不能重复研究或直接推断完成。
3. 历史完整报告含未知：允许保留原未知与日期，不能强迫全量联网更新。
4. 来源名单新增公司或文件变更：固定队列不自动扩大，记录来源变化。
5. 动作执行未知、仅开始未返回：日志检查提示未完成，不能当成功或重置预算。

## Task 1: 全量同步与来源保全

**Files:** `docs/sync/github-sync-2026-10-22.{md,json}`、`备份/2026-10-22_GitHub同步_01/`、源仓库全部受管文件。

**Interfaces:** 固定提交快照、逐文件来源 SHA、已备份本地文件；供后续导入校验和最终回归使用。

- [x] 获取固定提交，列出所有文件并校验 blob SHA。
- [x] 备份活动文件；新增缺少文件，保留两处本地日志改进并合并市场索引。
- [x] 保存源文件清单及同步说明：62 个文件，32 新增、27 相同、3 处已核对差异。

## Task 2: 批次接口与只读检查器

**Files:** 新建 `skills/research-customer-ogld/references/local-batch.md`、`assets/batch-templates.md`、`scripts/check_batch.py`、`scripts/test_check_batch.py`。

**Interfaces:** 内部检查点 `logs/checkpoint.json`，动作 `logs/actions.jsonl`；正式报告仍为两份批次 Markdown 与逐公司报告。`check_batch(batch: Path) -> dict` 返回 `errors/warnings/counts/next_customer_id`；CLI `python -X utf8 .../check_batch.py --batch <目录>`，0=结构一致、1=数据或文件错误、2=有未知/未闭合动作需对账。

- [x] 先写并运行测试，确认检查器缺失导致失败。
- [x] 实现源文件指纹检查、队列唯一性、串行进度、completed 报告存在/哈希/八节/官网表/客户 ID 检查、预算合法性及日志 begin/end 一致性；只读、不联网、不判断证据真实性。
- [x] 用临时模拟目录测试：正常混合复用与新增；重复 ID；跨国家；多个进行中；完成项缺文件；缺章节；报告被改；未闭合动作；未知执行；非法 JSON/重复 end；来源变更；预算不足；跳过未完成项；统计与下一项；直接复用来源指纹不符。
- [x] 编写本地协议和模板：精确定义 JSON 字段、报告双层完成口径、单公司阻塞续行、优先恢复当前项、预算不重置、上游名单不写入。
- [x] 运行 `python -X utf8 skills/research-customer-ogld/scripts/test_check_batch.py`，预期所有测试通过；把检查范围的限制写入文档。

## Task 3: 角色与项目入口

**Files:** 新建 `.codex/agents/customer-research.toml`、`docs/agent-team/customer-research.md`；修改 `AGENTS.md`、`README.md`；源 `research-customer-ogld/SKILL.md`、SOP、原报告模板保持字节不变。

**Interfaces:** 主 Agent 读取角色完整指令，传入市场、名单、配套证据、范围、预算及输出位置；角色读原 Skill 与 Task 2 本地规范。

- [x] 角色写明规则优先级、原路径解析、整表 valid 接收、ID与主体去重、三路复用、逐家保存、日志和恢复、并发写入协调、上下游职责。
- [x] 更新项目范围为市场搜集和客户背调；保留最新市场实跑记录，联系人及发信仍独立。
- [x] 使用说明含全名单调用、续接调用、单公司调用示例及真实输出结构；不声称配置自动加载或业务联网测试已完成。
- [x] 用 Python `tomllib` 解析角色，检查引用路径，运行 skill-creator 的 `quick_validate.py`；核对 GitHub Skill 五个文件 SHA 仍与快照一致。

## Task 4: 行为验证与交付

**Files:** 新建 `docs/agent-team/customer-research-validation.md` 及 `validation-evidence/2026-10-22-customer-research/` 下本次证据；更新实施进度。

**Interfaces:** 只读测试报告，不写真实公司成果；每种验证明确类型与限制。

- [x] 保存原 Skill 基线推演：批次接口缺失不等同实际违规，不伪造失败。
- [x] 由独立执行者按完整角色在模拟资料中实际建立混合批次、复用/补核/阻塞并续接，回读结果；禁止联网和真实市场写入。覆盖 Review Focus 五项。
- [x] 作者核对角色结构、全部引用、文件版本及模拟输出；运行既有市场日志回归，核对原公司资料未被改写。
- [x] 独立只读审查整体实现，对关键发现补充失败用例并修复，再跑必要回归。
- [x] 交付角色、使用说明、验证记录与同步记录，说明尚未真实联网试跑；不自动处理全市场。

## 实施记录

- 2026-10-22：Task 1 完成，源提交和备份可回读。
- Ruling: 用户已明确要求同步后开发并继续，本地直接实施，不重复请求方法/计划审批；若判断有误，影响仅为可恢复的本地配置变更。
- Ruling: 主目录非 Git 仓库，原仓库快照只作同步依据；不为工作树流程新建 Git 仓库，保留文件快照与证据替代提交账本。
- Ruling: 为避免指令中的“已保存”与实际文件不符，采用只读检查器；不实现自动联网或通用调度平台。通过不证明语义真实性或自动截获所有调用。

- 2026-10-22：Task 2、3完成，原Skill五文件保持不变；检查器19项回归通过，角色/引用/Skill格式检查通过。
- 2026-10-22：Task 4完成，独立基线、整体审查、离线流程R2均已有证据；真实联网试跑未执行。
- Final: fixed 来源指纹误放行、已确认执行预算被释放、历史快照同文件三项问题 — 对应测试均RED→GREEN，全18项通过。
- Final: Ruling: 历史报告编号/分隔符标题变体不应迫使重写，按已观察到的英文维度与中文章节标签兼容；语义仍人工判断。新增用例RED→GREEN，最终19项通过。
- Final: Ruling: source同步清单只描述同步时点，市场搜集并行更新保留；最终验证原版快照62文件、活动59原版、OGLD五文件及114已有市场文件，不声称市场代码仍与旧备份一致。
- Final: 未遗留独立审查重要缺陷；不适用Git分支提交/合并，保留本地备份和验证证据，不删除账本。
