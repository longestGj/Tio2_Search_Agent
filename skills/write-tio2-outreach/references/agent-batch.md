# 开发信 Agent 批次记录契约 v1.1

仅项目角色outreach_writer使用本契约；正文写作仍完整执行Skill和当前SOP。手动Skill批次schema=1保持原样；新Agent批次schema=2，避免把旧字段误读成新验收记录。格式检查不改变业务规则。

## 保存顺序

1. 开始读取实际指定批次和各公司报告，冻结公司ID、顺序、已选收件人、所需邮件阶段及联合组。输入有缺口保留记录，不遗漏公司。
2. 初次写两份正式报告及checkpoint。未写邮件不创建空文件凑数；pending/in_progress允许草稿未齐。
3. 每家公司完成/受阻时：保存每封或原合并稿、计数JSON并回读 → 更新两份批次报告 → 记录输入/输出/报告指纹及checkpoint → 运行检查器 → 回读结果后继续下一家。
4. 报告不互相写入对方指纹，checkpoint单向引用报告及草稿，避免循环指纹。检查结果另存logs，不回写已指纹化报告而不更新checkpoint。
5. 恢复先核对实际文件和原执行者，任何输入改变保留旧检查点及来源引用，记录差异/采用版本，不为使hash通过而抹掉差异。旧稿修订先快照。

## schema=2 checkpoint

顶层：schema=2、batch_id、country（ISO2）、owner、updated_at（含时区）、request_ref、source_artifacts、reports、frozen_companies、drafts、company_status、company_notes、next_action。建议附rule_versions、input_changes、reused/revised/new统计、last_saved及assignment_ref（有实际assignment时）。

- artifact：`{path, sha256}`。相对路径相对项目根目录；源文件可为外部绝对路径（例如用户提供的TDS）；输出必须在项目内。文件SHA256小写。source_artifacts记录实际读取的报告、Skill、SOP和拟用产品资料。缺失文件不编造artifact，写company_notes及blockers。
- reports：两份artifact，分别精确对应本批次01_批次进度.md、02_批次总结.md。
- frozen_companies：按处理顺序排列。每项`customer_id, selected_recipients, required_drafts`；required_drafts每项`draft_id, recipients, stage`。selected_recipients仅已选邮箱；recipients为此封实际收件组。默认同公司已选联系人为一个联合组，Mail 1和Mail 2各一封；只有用户明确要求分写时拆分并保存依据。手动或Agent都不能靠此登记证明选择本身获得授权。
- 无法确定任何有效已选邮箱/应交付范围时：该公司selected_recipients与required_drafts可暂为空，必须blocked且company_notes说明缺口；不得标completed或伪造邮箱。恢复获得真实资料后保存原范围版本和差异，再明确更新计划。
- drafts：只登记已保存的真实稿件，每项包括`draft_id, customer_id, recipients, stage, version, section, artifact, count_input, counts, content_status, send_status, followup_status, user_review, review, blockers`。
- count_input：仅可见邮件字段的JSON artifact，格式见local-execution.md；counts为count_words.py真实返回的body_words/full_words/mail2_within_limit。用下述唯一注释边界定位本封完整正文并比较可见文字，不在整个文件中搜索片段。检查器只核对正文与计数内容对应，完整邮件头/签名/附件及引用须由Agent人工复核。
- review：`{"value": true/false, "facts": true/false}`，表示执行者真实完成的两项业务审核，不是工具自动判定。content_status为已复核待用户审阅时两项均true且blockers为空；待补资料必须列具体blockers。
- company_status：全部冻结ID到pending/in_progress/completed/blocked/skipped的映射。completed必须全部required_drafts保存并逐封已复核待用户审阅。blocked/skipped在company_notes中注明原因和恢复条件/排除依据。归入原始输入但明确排除写作的公司仍列记录，不以跳过掩盖漏稿。
- user_review仅取未审阅/已认可具体内容/需修改；反馈原文及引用另存user_feedback。需修改不得与已复核待用户审阅或公司completed并存；尚未修订的稿件标需重写，修订且复核后新版本记未审阅并保留旧反馈。send_status新稿未发送、继承发送稿按真实记录；followup_status未核查或实际事实。不能把文件格式通过当用户批准。

### 收件组变更

由分写改合写时，先保存旧checkpoint与原稿快照，记录plan_changes及用户依据。旧drafts移入superseded_drafts，原稿标需重写并保留原ID、版本、反馈、资料缺口及指纹；不计入当前应交付或完成数。按新收件组创建新的计划ID，required_drafts更新为联合组，尚未写成的联合稿不创建占位文件。重写后记录replaces关联旧ID。检查器核对当前计划，历史快照和superseded_drafts由执行者回读核对。

### 正文定位

schema=2草稿在称呼之后、落款之前用独占行的HTML注释包住**全部实际正文**，将ID替换为稳定draft_id；同一合并文件每封分别标记，不能在内部说明中重复该标记。注释不计入邮件文字，不进入实际邮件内容。保存旧稿用于schema=2时先快照再加标记；旧schema=1文件不自动改写。

```text
Hi Name,

<!-- outreach-body:GB-COMPANY-M1:start -->
完整正文，包括CTA与正文内资料链接行。
<!-- outreach-body:GB-COMPANY-M1:end -->

Best regards,
```

正文支持普通文本、简单Markdown内联链接、加粗/斜体/行内代码及硬换行；计数JSON只存可见文字。复杂HTML/脚注/嵌套链接不在支持格式内，应改为普通正文或可见直接URL。正确划分正文边界仍需Agent人工核对，检查器不凭语义猜测边界。缺失、重复、逆序边界或跨封正文误配均拒绝。

## 检查命令

```text
python -X utf8 skills/write-tio2-outreach/scripts/check_batch.py --root "<项目根>" --batch "<批次目录>"
```

正常阶段检查允许合法pending/blocked，返回0仅说明记录一致。声称全批所有应交付文稿完成前追加`--require-complete`，任何非completed公司都会失败。退出1表示结构/文件/计数问题或严格完成条件不足。逐公司不能用严格检查迫使其他pending公司伪造完成。

检查器只读；不联网、锁定、发信、重新选人、确定产品适配、审核授权或判定REACH真伪。它不能自动识别以错误指纹来源自证、造假的业务review或错误的冻结写作范围；上述仍须专业角色核对真实输入并承担质量判断。

## 与原批次模板及调度衔接

沿用assets/batch-templates.md的两报告内容。报告区分业务自检、用户审阅、发送/跟进；逐封完成不外推全公司完成。独立任务不生成调度交接。显式assignment时按现有contracts.md输出handoff，不把schema=2内部检查点直接交给调度当handoff，也不启用未接入的生产能力。
