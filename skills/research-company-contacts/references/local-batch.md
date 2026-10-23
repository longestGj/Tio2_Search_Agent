# 本地批次与预算规范 v1.3

业务依据为完整[SKILL.md](../SKILL.md)流程V1.5及[两报告规范](report-contract.md)。本文件仅定义本地调度和记录，单公司任务同样建立单项队列。日期为Asia/Shanghai。

## 接收与两轮执行

读取用户指定的背调批次、公司报告及已有组织/邮箱文件，冻结公司ID、国家、company_key、顺序与来源指纹。按objective-evidence-v1承接已完成且释放的“继续开发”；“排除开发”保留理由与证据，不进入后续执行。旧四分类交背调生产者复核并提交新判定，不自行按旧标签放行或排除。所有指定公司保留记录，显式assignment不扩队；原证据及未知交下游，不改背调。用户单独授权的联系人任务依明确范围执行。缺背调先查找，仍缺按Skill最小核实主体，身份冲突未解不付费。不能只凭名字或共享域名合并。

第一轮逐家执行Skill§0—§4及§6阶段保存：完整检索、组织台账、固定人选、两份真实阶段报告。第二轮从保存的§4续接§5—§6：汇总全批固定人选及费用，按当时工具要求确认后分组获取。预算、名额和身份已明确且已有适用具体确认时不重复询问。每阶段保存回读后自动继续，不逐家审批；无合适人选不凑数。

首轮就按report-contract整理四项开发信材料，邮箱阶段更新实际渠道结果；批次总结链接到该处并注明缺项。已确认的公开人员无Apollo ID/邮箱时仍可交接，不进入固定付费队列。材料交接与公司执行状态分开，不因存在公共入口自动解除主体冲突等blocked。

首轮公司付费查询也受上限和对应工具确认约束；非必要不付费查公司，仅域名人员搜索可用时记录主体匹配限制。需要确认则保存待办，继续其他独立公司后汇总该类操作。不能承诺任何情况全程只有一次费用确认。

实际运行先发现当前Apollo工具并读取参数、费率、确认规则。搜索后enrichment使用本会话返回的ID，不以遮挡姓名匹配；跨会话重搜同一人并记录ID映射，固定person_key和候选编号不变。用户设计同意、预算上限和模拟确认都不是实际付费许可。

## 目录、写入与版本

- 公司报告沿用 `markets/<ISO2>/companies/<已有目录或客户ID>/`；公司持久账本为其 `contacts/ledger.json`。
- 批次为 `markets/<ISO2>/contacts/<ISO2>-CONTACTS-<YYYYMMDD>-<序号>/`，包含两份正式批次报告、`logs/checkpoint.json`、`logs/actions.jsonl`和原始返回`logs/evidence/`。
- 已有两报告沿用路径/首次日期；更新前存 `history/<北京时间-唯一后缀>/`，增加更新日期与差异。账本每次修改前也保存不可变快照，history记录快照路径/指纹，不使用当前文件或硬链接充作快照。
- 每公司同一流程使用稳定company_key、workflow_id、同一账本。换批次先核对旧报告、旧批次与实际账本；不能新建空账本重置3 credits。每批冻结接收时的账本快照ledger_anchor，持续核对历史操作不丢失。
- 同公司只有一个写入者；主Agent协调跨批次冲突。本规范/检查器不自动加锁，不拦截Apollo；文件与调用历史仍由执行者对账。
- 首次记录Skill V1.5/local-batch v1.3及实际文件SHA-256，固定本批版本；完整Skill包的四个原资源保留。来源指纹变化记录影响和处理依据，不静默扩队或切版本。V1.5澄清背调公开线索与优选名额，补最终收件组及分组保存要求；schema=1与3 credits、has_email准入保持。旧报告/日志不自动重写，在途批次按既有版本变化规则处理。

## 人数与费用

采购和管理为primary；两类均无合适人选才用secondary（技术/销售）。角色组是执行者据职责证据做的分类，不是平台官方部门或真实汇报关系。组织台账保留范围内所有人员，邮箱只获取固定选中的人。

邮箱可用性是付费队列的额外准入条件：原始搜索中同一ID必须为布尔`has_email=true`。false、null、缺失和未知只留作组织线索，不进入selection.people，不预留/请求费用。先判断岗位组再筛邮箱；primary_available描述岗位是否合适，不得因第一组无邮箱改为false来补选技术/销售。历史邮箱免费复用不受此队列约束，付费复验仍需准入。true不保证具名地址或投递成功。

历史已选或已付费获取的人按稳定person_key去重，占累计3人名额；仅背调公开线索不占名额，公共邮箱单列。公开线索被正式选用时再纳入累计，已执行付费操作不能通过改为公开线索豁免。new仅表示本次初选时无邮箱的新人，成功后仍保留原new标签及已执行operation_id；reverify必须是已有具名联系人。每人一个首选工作地址。选定的新人尝试范围不因无邮箱/失败而自动替换扩大。

费用字符串用非负十进制（如`"1"`、`"0.5"`），不接受浮点数、负数或NaN。恒定上限3。已结算费用＋所有未结算最大预留＋本次尚未预留最大费用≤3；已经预留的动作不得重复加一次。匹配无邮箱仍按实际工具扣费，不以缺邮箱归零。费用或执行未知保留最大预留，先对账；无可用请求状态接口时记录受阻，不假称查询成功。

账户余额差不能分摊公司费用；混合公司返回无法归属时保留各公司原预留。核对实际记录后追加结算，不能直接改写已确认消耗。可执行已授权调查继续，未知公司的新增付费先暂停。

## 数据约定 schema=1

下列内容是内部恢复接口，不替代正式报告。未执行字段为null或明确阶段，不能预填成功。

### 公司账本

必填 `schema=1/company_key/workflow_id/customer_ids/aliases/credit_limit="3"/contact_limit=3/baseline_evidence/contacts/operations/history`。

- baseline_evidence：`confirmed`布尔及`source_ref`。证实本流程起点与既有消耗，未知不得默认零。首次无历史消耗须记录查阅范围与依据。旧的无关流程消费另列背景，不冒充本流程费用。
- contacts：`person_key`（具名必需）、`kind=named|public`、`email`、`source_ref`、`date`；同人不同来源可重复保留但仅计一次；冲突首选地址先解决。仅背调公开且未选用者可标counts_toward_limit=false并写scope_basis；正式选用时改true。旧字段缺省沿用历史计数，采用新口径时先快照并明确来源/选择范围，不批量假定旧记录均未选用。任何已有人员付费操作仍计人数与费用。
- operations：每次实际拟调用、每公司/人员一条，字段为`operation_id/batch_id/kind/max_credits/actual_credits/status/evidence_ref`；人员操作另含`person_key`。kind如people_enrichment、organization_search、organization_enrichment。status为reserved/unknown/settled/cancelled。
- reserved/unknown的actual_credits为null，整笔max_credits仍占预算；settled须真实actual及证据；cancelled须actual="0"、executed=false及未执行证据。成功匹配无邮箱为settled，绝非cancelled。
- history为不可变旧账本的`path/sha256`列表，路径相对账本父目录或绝对路径。历史company_key/workflow_id/客户ID、具名联系人和操作不得静默丢失；已settled的金额和状态不能退回未执行。修正异常费用必须保留证据并停下核查，不能用直接改账强行通过。

### 固定选人

selection含 `primary_available`布尔、`primary_basis`及`people`列表。每个people项：`candidate_id/person_key/apollo_id/source_ref/group(primary|secondary)/mode(new|reverify)/identity_basis/relevance_basis/has_email/email_evidence/max_credits/operation_id`。has_email必须是布尔true；email_evidence为本会话原始搜索返回文件的`{path,sha256}`，相对批次目录或绝对路径。检查器校验文件指纹、人员ID及原值true，支持直接API JSON或MCP的content文本/structuredContent封装；不能引用自行归纳的候选表代替原返回。Agent还须核对查询动作、公司目标、会话及时间，不把文件指纹当作真实性证明。

尚未申请时operation_id=null；预留或执行后指向当前人员operation。只有原尝试已有明确未执行证据、cancelled且actual=0时，才允许在取得新的适用确认后为同一固定人员登记新operation_id；原操作、确认和begin/end仍全部保留。检查旧日志按固定人员身份及其已确认取消状态关联，不能删除旧记录或复用已用完的确认额度。原尝试仍未知时不得以更新当前operation_id发起重试。公司费用无person_key，不得挪作选中人费用。has_email只决定邮箱准入，不能单凭它认定岗位适合。

相关岗位候选、邮箱可用候选、固定付费队列分别计数，前两类完整记录在组织/邮箱报告。仅第三类写入selection.people和费用确认N。无邮箱者仍保留原人员编号和来源，不算已尝试。跨会话重搜须同时更新同人ID映射与邮箱证据；若结果为false/未知，暂停该人的新付费请求，保留原选择、批准与已发生操作的历史。

若暂停者尚未执行且未预留费用，先保存原选择快照，再将其移出当前selection.people，保留报告中的固定编号、暂停原因和原批准；其余仍符合条件的原选人可继续，不新增替补。已有预留或执行未知者先对账，不删除操作或释放未知额度。已执行的旧名单属于历史记录，不用此规则删改。

### 批次检查点

必填 `schema=1/batch_id/phase/sources/skill_sources/source_changes/items/approvals/next_step`。phase为research/enrichment/closed。sources与skill_sources各为非空`path/sha256`列表；指纹变化用source_changes中的`path/observed_sha256/resolution`说明已核对处理；指纹不匹配期间不自动放行调用。

items逐公司保存：`customer_id/country/company_key/ledger_path/ledger_anchor/status/stage/selection/reports/next_step`，完成时加`completion_basis`；受阻时`block_reason`。ledger_anchor为接收时另存的账本`path/sha256`，不能指向当前账本。sources包含背调/名单或最小主体核查记录，保留条目定位。

status为queued/in_progress/waiting_confirmation/completed/blocked。同一时刻最多一家in_progress；queued按输入顺序推进，waiting_confirmation/blocked允许其他公司继续。reports包含organization、email两个`path/sha256`对象；待确认和完成项必须已有两报告，queued尚未生成时reports={}。两报告完整章节和当前客户ID必须可定位；旧报告编号、标点差异可保留，语义仍由执行者检查。

每个批次路径均相对批次目录或绝对路径。所有报告与证据真实可读。正式批次文件也必须实际存在；内部检查点不能代替阶段报告。

### 费用确认

approvals每条：`approval_id/kind/confirmed/user_confirmation_ref/confirmation_text/balance_snapshot/max_credits/allocations`。allocations固定`company_key/person_key/apollo_id/max_credits`；公司查询时person_key和apollo_id为null。仅确切费用确认记录confirmed=true。kind、人员/公司与金额不能扩大，分组总额不能重复使用。

搜索后获取邮箱先查实际Profile余额并按当前工具原文确认整批。例如当前适用文本：`Found [N] contacts. Enriching all will use up to [N] credits. You have [X] credits remaining. Want to proceed, or narrow the scope?` 替换真实N/X。已有同人跨会话ID变化时在检查点id_mappings记录`person_key/old_id/new_id/evidence_ref`，核对原对象和批准范围，不能批准新的人。

### 动作日志

JSONL追加事件，均含`event/action_id/recorded_at`。begin：`tool/kind/target/approval_id/allocations`，每个allocation含`company_key/operation_id/person_key/apollo_id/max_credits`。人员enrichment最多10个allocation，关闭个人邮箱与电话并记录params。免费查询/读取allocations=[]，单目标记录所属company_key。

end：`executed=true|false|null/outcome/evidence_path/request_id/error`。request_id为字符串或null，evidence_path为实际原始返回文件；executed=false/null记录原因，失败也保留证据。每begin最多一个end；中断后凭原动作的真实证据追加reconcile（相同字段及reason），可用于只有begin尚未保存end的情况，也可补核已有end。不能为通过检查伪造end；reconcile不得抹掉已确认执行或已结算费用。收费begin前必须在公司账本预留并登记对应许可。

先保存预留、begin，再调用工具；返回立即保存原始结果、end及费用账本，再同步报告和checkpoint。开始登记不证明实际执行。中断先找回真实返回；未闭合/未知项对账前暂停对应付费，不凭记忆伪造调用。全部状态一致后再继续。

## 检查与完成口径

在开始调用前、每家公司/阶段结束、待确认和交付前运行：

```powershell
python -X utf8 skills/research-company-contacts/scripts/check_batch.py --batch "<实际批次目录>"
```

0表示已登记结构一致；1表示结构、上限或文件错误；2表示未知、未闭合或来源变更等需对账。waiting_confirmation可返回0但all_completed=false。完成处理不保证有邮箱，预算不足/无合适人选按真实限制交付。费用未知不得称整批完成；存在blocked则明确阶段交付。

检查器只读，不能核实网页真假、判断岗位是否合适、认证用户确认来源、证明没有绕过记录的调用，或在文件整体被替换时发现所有历史丢失。Agent必须核对工具历史、同公司旧资料和账本。通过检查不等于工具已经获准执行。

## V1.3恢复与历史兼容

本次新增准入字段不改变schema=1的账本金额、联系人或已执行事实。旧选择缺字段、原值非true或证据不符时，新检查器返回错误，不能将旧批次无错误结果沿用为新请求许可。已执行记录不得伪填true、删人、撤销扣费或重建空账本来通过检查。旧结果按原执行版本审计；新执行使用新版本并引用同一公司账本和旧批次，保留历史原件。旧未执行队列升级前先记录版本/范围差异、按原证据重新筛选并保存新阶段报告；确认范围变动依工具当前要求处理。未知执行项先按原证据对账，不以版本升级重新调用。


## 分组保存与最终收件组

每组enrichment返回后，必须按“原始返回→end和账本→受影响公司两报告→批次进度/总结→checkpoint→回读检查”的顺序完成保存，再发下一组；只保存日志或账本不能代替正式报告。保存失败停止后续调用，保留真实缺口，不倒填过去时点。

最终释放前，按report-contract.md生成本次固定收件组交接；它不是新增的调查或发送授权，不因已有邮箱就自动全选。
