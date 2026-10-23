# 组织与联系人 Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 建设承接公司背调批次、完整使用 research-company-contacts Skill、自动选人并在每家公司3人及3 credits范围内获取工作邮箱的项目级Agent。

**Architecture:** 原Skill继续维护完整单公司流程和两报告规范；Agent增加批次调度、本地保存与恢复。轻量只读检查器核对公司账本、固定选人、付费范围和报告进度；不实现另一套调查流程或自动Apollo客户端。

**Tech Stack:** TOML、Markdown、JSON/JSONL、Python 3.12标准库和现有Apollo连接工具；不新增运行依赖。

**Spec:** [已确认设计V0.2](company-contacts-design.md)。2026-10-22用户回复“同意”。用户已选择方式1：主Agent依次实施，最终独立复核。四项任务已完成；真实Apollo查询不在本次实施范围，验证边界见company-contacts-validation.md。

## Global Constraints

- 完整使用 `skills/research-company-contacts/`，保留§0—§6、“常见偏差”、完整报告字段、元数据及图标。
- 自动选择联系人，无须用户审核候选名单。
- 采购和管理优先；两类均无合适人选才选技术和销售，第一组不足3人不自动补第二组。
- 每家公司累计最多3位具名邮箱联系人；公共部门邮箱单列，历史具名邮箱占名额。
- 本联系人流程内每家公司总上限3 credits，所有Apollo收费动作及复验计入；恢复、别名及换批次不重置。
- 先完成整批选人和阶段保存，再按当时工具要求确认具体人数及总费用；确认后的固定范围分组执行不逐家审批。
- 每批一个执行者，同公司跨批次也须协调唯一写入；不嵌套派生研究者。
- 新角色不启动真实试跑；实施验证使用虚构数据，不调用Apollo、不消费额度、不发送邮件。
- 不改写上游市场与背调成果，不安装用户级Skill，不推送GitHub；共享知识库不在本任务读取范围。
- 当前主目录不是Git仓库，不新建仓库或执行Git提交。实施前只备份将修改的文件，保留哈希清单，不覆盖其他任务更新。
- 人员ID、证据、价格和确认条件在实际业务执行时读取；本地检查器不证明事实真假、真实用户批准或全量工具调用都已登记。

## Review Focus

1. 同一公司以别名跨批次出现：引用同一company_key和账本，不能重复初始化额度；Task 2/3测试。
2. 混合公司请求超时或仅有总扣费：相关公司保留最大预留，不平均分摊或重试释放额度；Task 2测试。
3. 已有2人邮箱但其中1人需复验：最多新增1人，复验仍占费用；Task 2测试。
4. 第一轮已保存，第二轮恢复时人员ID或输入变化：核对原对象和批准范围，不偷换人或扩大队列；Task 3测试。
5. 报告写入成功而进度滞后：核对已保存结果再更新进度，不重新付费；Task 3/4测试。

## 文件职责及顺序

| 文件 | 动作 | 责任 |
| --- | --- | --- |
| `skills/research-company-contacts/SKILL.md` | 修改 | 原完整流程的本地V1.2适配及批次规范入口 |
| `skills/research-company-contacts/references/report-contract.md` | 修改 | 保留全部原字段，补充预算和批次关联 |
| `skills/research-company-contacts/agents/openai.yaml` | 必要修改 | 保留完整元数据，默认提示与已确认规则一致 |
| `skills/research-company-contacts/assets/icon.svg` | 保留 | 图标不变，校验引用 |
| `skills/research-company-contacts/references/local-batch.md` | 新增 | 两轮调度、状态、账本、日志、保存及恢复协议v1.0 |
| `skills/research-company-contacts/assets/batch-templates.md` | 新增 | 两份批次Markdown、检查点及账本的虚构样例 |
| `skills/research-company-contacts/scripts/check_batch.py` | 新增 | 只读公司预算、固定范围及批次一致性检查 |
| `skills/research-company-contacts/scripts/test_check_batch.py` | 新增 | 临时目录中的离线回归 |
| `.codex/agents/company-contacts.toml` | 新增 | company_contacts角色，读取完整Skill并组织批次 |
| `AGENTS.md`、`README.md` | 修改 | 路由、入口及当前阶段说明 |
| `docs/agent-team/company-contacts.md` | 新增 | 使用、恢复、检查器及能力边界 |
| `docs/agent-team/company-contacts-validation.md` | 新增 | 文件/回归/离线验证与尚未验证事项 |
| `docs/agent-team/validation-evidence/2026-10-22-company-contacts/` | 新增 | 基线、检查结果、虚构应用验证和来源清单 |

本计划只新增必要脚本；不从背调检查器导入OGLD专属状态和章节，也不复制一套通用框架。

## Task 1: 完整Skill适配与数据约定

**Files:** 修改原Skill入口、report-contract.md及必要的openai.yaml；新增local-batch.md、batch-templates.md；保存定向基线到上述验证目录。

**Interfaces:** 为Task 2/3定义下列schema=1数据；为Task 4提供完整Skill读取路径。所有路径保留原客户ID，company_key由执行者依据真实主体建立稳定映射，不能简单用域名代替。

- 公司 `contacts/ledger.json`：`company_key`、`customer_ids`、`aliases`、`workflow_id`、`baseline_evidence`、`credit_limit="3"`、`contact_limit=3`、`contacts`、`operations`。每个contact记录稳定`person_key`、实际搜索ID历史、工作邮箱来源/日期；同人别名映射由执行者有证据地维护。每个operation记录`operation_id`、`batch_id`、`kind`、`max_credits`、`actual_credits`、`status`（reserved/unknown/settled/cancelled）、证据引用。未知实际费用为null；reserved/unknown保留最大预留，settled须有实际费用依据，cancelled须有未执行依据。数字费用统一十进制字符串，拒绝负数、NaN/Infinity及布尔值。
- 批次 `logs/checkpoint.json`：`batch_id`、`schema`、`phase`（research/enrichment/closed）、源文件及Skill指纹、固定`items`、`approvals`、当前项/下一步/暂停原因。每个item含国家、客户ID、company_key、唯一ledger_path、status（设计五状态）、stage、背调来源、`selection`、两报告路径/哈希、完成依据及缺口。selection逐人记录固定编号、person_key、当前搜索ID与来源、角色组、适合性依据、new/reverify、单人最大费用及结果状态；另记第一组是否有合适人选和核查依据。
- approvals记录固定操作种类、选中人员集合、company_key归属、每公司及总最大费用、余额快照、工具原文和实际用户确认引用。仅声明设计获批不得登记为真实付费确认。跨会话搜索ID变更记录同人映射与来源，不能靠改ID偷换person_key。
- `logs/actions.jsonl`采用追加begin/end/reconcile：每次请求唯一action_id，begin记录工具、目标、人员/公司映射、参数、每公司预留operation_id及最大费用；end记录执行确定性、结果/失败、原始返回路径、字符串request_id及已知费用；reconcile引用原动作与新证据，禁止覆盖旧记录。混合公司单次请求在每公司账本各保留相应operation，按ID证据归属。
- 正式批次报告为`01_批次进度.md`和`02_批次总结.md`；公司报告完整遵循report-contract.md。表格分别呈现人次、唯一人数、历史/本轮邮箱及实际/预留/未知费用。

- [x] 1. 读取当前AGENTS、已确认设计和原Skill四文件；为将修改的已有文件保存定向快照、SHA-256及来源记录。检查并行变更，不恢复旧快照覆盖现状。
- [x] 2. 更新原Skill流程V1.2：替换选人优先级，加入3-credit限制、批次条件及本地保存入口；保留§0—§6全部职责和原报告字段。用逐节对照表记录保留与变化。
- [x] 3. 编写local-batch.md，落实以上数据约定、两轮调度、缺背调的最小核查、冻结输入/人选、确认与费用预留、单写入责任、断点对账。明确不完整账本不能推断余额为3。
- [x] 4. 编写batch-templates.md及补充report-contract.md；样例只用XX国家、虚构公司及example.invalid，不能提前写成功结果。明确每家公司和待确认时正式报告落盘，未知不能写0。
- [x] 5. 校验原四文件均存在、图标SHA不变、原章节与报告字段仍完整、全部相对链接可定位；保留人工对照结果。文档格式检查不声称业务验证通过。

## Task 2: 公司预算与选人范围检查

**Files:** 新增scripts/check_batch.py和scripts/test_check_batch.py。

**Interfaces:** `validate_ledger(ledger: dict) -> dict` 返回`errors`、`warnings`、`spent`、`reserved`、`remaining`（费用十进制字符串）、`existing_contacts`、`new_slots`；`validate_selection(ledger: dict, selection: dict) -> dict` 返回`errors`、`warnings`、`new_count`、`reverify_count`、`max_credits`。非法数据返回错误，不崩溃，不联网、不写文件。使用Python Decimal精确计算。

测试文件提供`make_ledger(existing: int = 0, spent: str = "0", held: str = "0") -> dict`和`make_selection(new: int = 0, reverify: int = 0, primary_available: bool = True) -> dict`虚构工厂，按Task 1生成有效记录；spent生成有证据的settled操作，held生成unknown操作，人员类别按用例明确设置。

- [x] 1. 写预算失败测试，首次运行确认缺实现导致失败：

```python
assert validate_ledger(make_ledger(spent="1", held="1"))["remaining"] == "1"
assert validate_selection(make_ledger(spent="1"), make_selection(new=3))["errors"]
assert not validate_selection(make_ledger(spent="1"), make_selection(new=2))["errors"]
assert validate_selection(make_ledger(held="3"), make_selection(new=1))["errors"]
```

- [x] 2. 实现上述两个函数：只累计唯一操作，不信任手填总数；settled不再重复计预留；actual超过max、重复operation_id、缺费用依据、非法金额和未知基线返回错误/需对账，不释放额度。已结算历史费用不可从后续快照中静默消失。
- [x] 3. 增加并运行人数、优先级和异常费用测试：existing=2,new=1,reverify=1允许且计划费用2；existing=2,new=2拒绝；existing≥3拒绝新增并保留历史超限说明；公共邮箱不占名额。同一person_key去重，重复请求ID/人选不得增加有效人数；无稳定映射时保留需核对状态。
- [x] 4. 增加优先级测试：第一组有1人却选第二组补满拒绝；第一组均无合适人选且有核查依据时技术/销售允许；所有selected必须有主体/适合性依据。检查器只检查声明及一致性，不判断职位语义本身。
- [x] 5. 覆盖混合请求无法分摊费用仍保留预留、匹配无邮箱仍消耗1、未匹配有明确免费依据才计0、复验扣费、非法Decimal、同操作重复结算。运行`python -X utf8 skills/research-company-contacts/scripts/test_check_batch.py`，预期全部通过；保存真实结果。

## Task 3: 批次、确认、报告与恢复检查

**Files:** 扩展上述两个scripts；必要时同步local-batch.md及batch-templates.md的精确字段。

**Interfaces:** `check_batch(batch: Path) -> dict`调用Task 2函数，返回`errors/warnings/counts/company_budgets/all_completed/next_step/exit_code`。CLI：`python -X utf8 skills/research-company-contacts/scripts/check_batch.py --batch <实际目录>`；0=登记内容结构一致，1=结构/上限/文件错误，2=未闭合、执行或费用未知、来源变化等需要对账。waiting_confirmation可以是结构一致的阶段结果，但不得all_completed=true。

- [x] 1. 以临时中文路径生成完整虚构批次，测试CLI输出JSON、UTF-8/BOM输入、错误返回码与只读行为；缺失/非法JSON及截断JSONL应明确报错，原文件SHA保持不变。
- [x] 2. 先写失败测试再实现输入和账本关联检查：重复公司键不得使用两个账本；同名不同国家不合并；每个账本身份与item匹配；历史操作有对应原始记录，不能通过新建空账本重置额度。来源/Skill指纹变化须明确处理记录，不静默换队列或版本。
- [x] 3. 先写失败测试再实现人员与确认范围检查：整批未批准不得登记已执行收费动作；具体请求人数≤10；每组人员、公司、种类和费用均属于固定批准范围，分组累计不超过范围；new/reverify均计请求费用。跨会话搜索ID变更须有同人映射证据，新增person_key须重新办理适用确认。
- [x] 4. 先写失败测试再实现日志及费用对账：begin/end唯一配对，reconcile只追加有证据的更正；请求ID按字符串保留，超长ID不得变浮点。已确认执行不能改为未执行释放费用；reserved/unknown未闭合不得all_completed；混合公司返回缺少可归属字段时保留未知。
- [x] 5. 检查公司两报告及正式批次文件真实存在、指纹和客户ID一致、report-contract全部章节存在；容忍旧标题编号/标点差异，不能为通过检查强制改写旧报告。完成或待确认项缺两报告应拒绝；整批完成必须满足各公司状态与阶段，组织结果完成不能当邮箱成功。
- [x] 6. 增加恢复用例：报告已写但进度落后先报不一致，人工对账后更新检查点，不增加付费动作；同公司另批继续仍读取相同账本；无合适人选或额度耗尽可以明确结束处理但保留结果缺口；费用未知不冒充处理全部完成。
- [x] 7. 运行全套回归，预期正常虚构批次0、非法/超限批次1、未知/未闭合批次2；比较运行前后所有fixture哈希确认只读。同步模板使其可由同一检查器读取，不能文档和代码使用不同字段。

## Task 4: 角色接入与完整离线应用验证

**Files:** 新建company-contacts.toml、company-contacts.md、company-contacts-validation.md；修改AGENTS.md/README.md；验证证据保存在本计划指定目录。

**Interfaces:** 新角色`company_contacts`读取完整Skill、report-contract、本地批次规范和模板；每次付费前及阶段保存后调用Task 3检查器。仍由Agent执行实际工具与文件操作，检查器不拦截Apollo或提供并发锁。

- [x] 1. 编写角色，覆盖批次输入、唯一写入、两轮调度、持久预算、工具前置条件、阶段保存和恢复；引用完整Skill，禁止仅执行enrichment。保持角色指令精简，不复制整份单公司SOP。
- [x] 2. 更新项目路由和README，增加调用示例与输出链接；仅“组织与联系人/工作邮箱”任务触发该角色。设计或查看请求不触发实搜；已有市场/背调路由及其他任务修改保留。使用说明解释工具确认、限额与恢复。
- [x] 3. 解析TOML，核对name/description/developer_instructions与完整引用路径；检查Skill元数据、图标及Markdown链接。没有角色选项时记录完整指令委派方式，不将配置存在冒称客户端原生加载成功。
- [x] 4. 在验证目录建立虚构离线批次，逐步模拟：A有采购及销售只选采购；B无第一组选技术/销售；C已有2位邮箱、已耗1 credit，仅剩1个新人名额和2 credits；D主体冲突受阻；E含结果未知的收费动作。记录第一轮阶段报告、整批模拟确认、模拟返回、待定费用和恢复；全部材料标明虚构，模拟确认绝不用于真实调用。
- [x] 5. 逐检查点运行CLI，核对预期状态及费用，保留原始stdout/stderr、指纹和人工审阅。模拟E在未知时保留预留，找回原模拟返回后只追加对账；模拟报告先存而进度落后时不增加请求。独立检查两份公司报告全部字段，确认组织台账包含未选人员。
- [x] 6. 对最终文件及离线证据复核，修复实际发现的问题后只重跑受影响与必要回归。输出验证记录，分开列文件检查、代码回归、离线应用；真实Apollo搜索、付费、长期运行和客户端发现仍标尚未验证。
- [x] 7. 交付角色、完整Skill入口、使用说明和验证记录链接，更新本计划勾选状态；不自动开始真实批次。未执行检查不得填“通过”。

## 自检与执行交接

本计划覆盖设计§1—§11：Task 1负责完整Skill与两报告契约，Task 2负责两项上限和优先级，Task 3负责全批确认/保存/恢复，Task 4负责角色路由与全流程离线验证。Review Focus五项均已分配测试；函数名、schema字段和返回码在任务间一致。

实际采用用户选择的方式1：主Agent依次实施，最终由独立上下文审查者复核。发现的两个恢复问题及报告字段缺口已在一轮修复中完成RED→GREEN；最终114项项目回归通过。审查后未重复派生复核，原审查结论及修复证据一并保留。
