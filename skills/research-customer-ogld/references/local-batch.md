# OGLD 本地批次补充 v1.1

供项目`customer_research`角色读取。原SOP V1.1保留来源快照；按[客观背调与筛选](objective-research.md)覆盖原意愿判断、四分类与交接规则，Skill及模板已同步。其余事实核查要求仍执行原SOP；本规范定义批次、复用与记录。

## 1. 接收与唯一队列

阅读指定总表、证据与批次说明，用原客户 ID 建有序队列，默认只纳入唯一 valid；正文和摘要同一公司只登记一次。逐项记录排除 ID 和原因。旧联系人 CSV 的邮箱状态不是 valid；无基础核验记录不能自行推定。

记录所有实际用到的输入文件路径、SHA-256、版本/日期及条目定位。用列表顺序作为执行顺序，不另维护相冲突的排序字段。临时 ID 须明示并与源条目映射。已知不同主体不能因共享域名去重，客户 ID 冲突先解决。

国家、路径或多份活跃名单有歧义时先定位，不能仅按目录日期选择。名单更新后，冻结队列不自动增删；`source_changes` 保存变更路径、当前指纹、差异及处理决定。获得明确扩展范围的指令后才能追加队列，保留原顺序和变更记录，不改预算上限。被删除的已登记公司保留记录。

## 2. 复用判定与日期

| 可观察条件 | 执行 |
| --- | --- |
| 客户ID、国家和主体依据相符；报告八节/官网表/证据齐全；无已知重大冲突；未要求更新 | reused：保持原文、路径、SHA与原调查日期；记录本次复用检查日期和未重新联网核验 |
| 同主体报告缺关键结构/来源，重要缺口有可执行补查，或出现新冲突 | supplemented：先快照，定向补查，更新同一文件；保留原日期并加更新日期、范围、结论变化 |
| 中断草稿 | 从实际完成步骤继续，不能以报告文件存在作为完成依据 |
| 无报告或只有其他主体报告 | new：为当前主体新建，别人的报告不能移用 |

已有未知及限制可继承，不为消除所有未知无限补查；旧日期本身不触发全部重做。动态事实用于当前判断时定向核实。多个版本先核对最后明确检查点和关系，不猜哪个有效。

历史报告的“1. 核心结论”“O｜官网调查”等同义章节标题可保留；检查器容纳已观察到的编号标点和章节名称变体，执行者仍逐节确认内容符合SOP。不能只因排版不同强迫重做。旧V1.0报告实际缺官网确认表或完整来源等必填内容时，复用已有证据并补齐所缺结构/资料，不默认重新调查全部事实。

更新旧报告前复制到该公司 `history/<北京时间-唯一后缀>/`，核验快照 SHA 与更新前一致；快照必须为独立文件，不得用当前文件或它的硬链接/符号链接替代。直接复用不改原报告；新元信息写入批次。原报告旧文件名保留。路径与哈希不符先解释真实原因，不能只更新哈希掩盖意外覆盖。

## 3. 状态与执行循环

| 状态 | 条件与下一动作 |
| --- | --- |
| queued | 纳入尚未执行 |
| in_progress | 唯一当前公司；保持当前 O/G/L/D/判断/复核位置 |
| completed | 复用或调查已复核，真实报告保存/回读，进度和摘要同步 |
| blocked | 必要工作受阻无法完成，保存理由、已做/未做及恢复条件，然后继续后续queued |

方式为reused/supplemented/new，判定前null。最终结论仅“继续开发／排除开发”，未完成调查不填最终结论。带真实执行限制且可行替代已调查的完整报告可completed；必要调查未做不能靠填未知宣称完成。排除开发仍计本阶段completed，与输入未纳入不同。

用户2026-10-22最终确认：背调只查客观证据，有明确证据才排除，其余继续开发；未知信息和购买意愿不作为筛除条件。完成且释放后，在授权范围内由背调Agent填写继续开发→advance/contacts、排除开发→end/null；仅背调的终点两类均finish/null。旧四分类不自动映射，由背调Agent复核原证据并另记新判定，不能只换标签；不改旧报告/已提交交接。必要漏项继续调查，充分调查后的限制随报告保留。调度不判断业务质量。

在当前公司完成或标blocked前不进入下一家。单公司blocked允许续行；系统性工具不可用、不能保存、用户要求停止或硬性预算到限暂停整批。所有纳入项completed且记录已对账才称整批处理完成；存在任何queued/in_progress/blocked时称阶段交付。完成总数与本次联网数量分开。

## 4. 文件与内部检查点

正式输出：公司报告、批次 `01_批次进度.md`、`02_批次总结.md`。内部文件 `logs/checkpoint.json` 和 `logs/actions.jsonl` 用于恢复与检查，不代替正式报告。模板见 [批次模板](../assets/batch-templates.md)。

检查点使用 UTF-8 JSON、schema=1，绝对路径或相对批次根目录的路径。必填结构：

- `batch_id`、`country`、`skill_version`、`skill_commit`：真实版本；初始源提交见项目同步记录。
- `sources`：非空数组，每项 `{path, sha256}`；sha256须为64位小写十六进制的真实初始指纹，不因变化重置。不能用缺失路径加空指纹作为已冻结来源。
- `source_changes`：数组，每项 `{path, observed_sha256, resolution}`，写明差异及队列处理；确认源不可用时 observed_sha256 为 null，另保留可恢复来源。
- `budget`：`search_limit` 为非负整数或 null（用户未设上限），`search_used` 为与本批日志已确认执行一致的非负整数；`active_minutes_limit/active_minutes_used` 为非负数或 null（未设/无法测量）。上限已设而用时未知须先对账，不能假定充足。
- `items`：有序数组。必填 `customer_id, company_name, country, source_status, source_locator, status, mode, stage, next_step, block_reason, report_path, report_sha256`。未生成报告的路径/哈希用 null。非valid必须加 `scope_exception` 记录用户具体授权。
- completed另需`identity_basis, checked_at, action`；本规范下新完成/再次复核条目必填`research_policy="objective-evidence-v1"`。排除开发另填`exclusion_reason`及`exclusion_evidence`证据ID非空数组，对应报告或本次复用判定。复用/补核另需`original_date, original_report_path, original_report_sha256`；补核另需`history_path`。未知原日期明确写“原报告未记录”，不能伪造日期。
- 阶段说明附 `updated_at, pause_reason, current_customer_id, remaining_work, ownership, exclusions, budget_notes`，用于人读对账。检查器不自动验证这些叙述。

初始输入完整读完后立即保存01与检查点，创建空动作日志。每次公司完成/阻塞、暂停前保存；检查点用同目录临时文件写入并回读后原子替换，旧检查点保存在批次history，不能截断写坏现有文件。报告更新、检查点、Markdown不是单个事务：恢复时按实际文件内容和版本对齐，不能盲信某一处completed。

同批次和同公司文件都只允许一个写入者。确认其他任务在处理时联系主Agent协调；本检查器无跨进程锁，不可把检查通过视为取得写入权。

## 5. 逐动作日志

`logs/actions.jsonl` 每行一个 JSON，追加不改旧行；每行立即写入。不要存凭据、完整请求头或无关个人资料。仅记录本批执行，继承旧报告不补造历史联网日志。

begin 必填：`event="begin", action_id, customer_id, dimension, kind, target, tool, recorded_at`。dimension 为 O/G/L/D，kind 为 search/read；target 为一个实际查询文本或页面目标，action_id 在批次中唯一。recorded_at 为带时区的真实记录时间，不冒充工具内部时间。记录开始后才能实际调用。

end 必填：`event="end", action_id, recorded_at, outcome, executed, summary, refs, error`。refs 是实际返回标识或已保存证据路径数组。无稳定返回定位时保存必要原始结果到 `logs/evidence/`，分析另写，不假造返回。

| outcome | executed | 要求 |
| --- | --- | --- |
| success | true | 真实摘要、至少一个返回定位；登录页也如实写，不等于证据充分 |
| error | true | 真实失败原因，refs可为空 |
| interrupted | true或null | 已执行但缺返回为true；无法确认执行为null；写明缺口 |
| cancelled | false | 有证据确定仅登记、未实际调用，不计执行 |

一个查询/页面目标一个action，同次调用包含多个独立目标时分别begin/end。只并行同一公司互不依赖的来源，先登记全部目标，逐个闭合。重试另用ID，附 `parent_action_id` 和 retry/alternative 原因，不能合并抹去失败。保存返回并闭合记录后才开始下一依赖动作。

恢复发现begin无end，先查工具历史/保留返回；有证据则据实end，无证据写interrupted并暂停外部调用、保存阶段交付，不能虚记失败。后来找回原结果且已有interrupted end时，可追加一次 `event="reconcile"`，沿用原ID、end字段，加 `reason` 和非空refs，结果只能success/error/cancelled；原interrupted行保留。仅确实找回原执行依据才对账，不能用新的请求冒充原返回；同action不重复reconcile。计数按最终可证实结果一次计算。

已确认executed=true的动作不得对账成false或null以释放预算；只有原执行未知时才能凭证据确认cancelled。已知执行记录本身存在错误时保留冲突、暂停并说明，本版没有用于改写已确认执行事实的自动纠错接口。

## 6. 预算与恢复入口

不继承市场搜集40查询/120分钟。未设上限记录null；计数按日志中executed=true的search动作，包含失败和重试；read不扣search。存在未知search时已确认计数是下界，不能假定精确剩余值；未知read仍需完成执行对账，不能因此扣搜索次数。主动用时只累计可靠实际研究时段，不用整段墙钟猜测。

到限停止受限动作，保存阶段成果；若用户约定的是搜索上限且已有资料足够，可在其余授权范围内完成整理和本地复用，不能借整理扩查新资料。无上限仍依有限替代路径处理，不无限重试。付费、额度和外部写入遵守当时工具说明及用户授权，不能从批次授权推导付费授权。

恢复顺序：确认写入者 → 读检查点/两份报告/当前公司文件 → 核对输入变化及报告版本 → 对账未闭合/未知动作与预算 → 恢复当前in_progress → 下一个queued。blocked仅在其恢复条件实际满足后改in_progress；后续已completed公司不重做。报告已保存但状态落后时先复核文件和证据再补记录，不重复联网。

## 7. 检查器与边界

运行：`python -X utf8 skills/research-customer-ogld/scripts/check_batch.py --batch "<批次绝对路径>"`。

返回0表示已登记结构一致；1表示字段/文件/状态/计数错误；2表示来源变化待确认或未闭合/未知动作须对账。修复后再进行外部动作。输出counts、next_customer_id、all_completed、已确认搜索次数、搜索剩余数和new_search_allowed。

**这些字段不是执行授权。** 搜索剩余值在未知search存在时仅是按已确认量算出的上界；exit_code非0时禁止据此继续。next_customer_id只是已登记队列提示；预算上限、blocked恢复、用户停止及工具授权仍由执行者判断。全部blocked时next为null不代表整批完成。空名单all_completed为false，交付“零纳入目标”说明。

检查器只检查存在/哈希/固定标题/ID、政策标识与结论取值、排除依据字段、队列顺序和已登记日志。legacy_conclusion_ids列出仍按旧规则检查的completed条目；通过不代表它们符合新标准，不自动改变历史状态。它不能核实公司身份、来源真假、OGLD覆盖或排除理由是否充分、上游是否遗漏、Markdown与JSON全部一致、所有实际调用是否记全，亦不自动调度或加锁。完成前须人工对照执行复核表、正文证据、两份批次Markdown及实际调用历史。
