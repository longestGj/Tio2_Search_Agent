# 批次记录模板

下文schema=1字段用于已有手动Skill任务。由outreach_writer执行的新Agent批次使用[Agent批次契约](../references/agent-batch.md)的schema=2，报告内容仍沿用本模板；不自动迁移历史记录。

## 01_批次进度.md

任务ID、国家、用户要求及引用、冻结公司及收件人范围、阶段要求、默认值依据、执行者、SOP/Skill指纹、输入清单、开始/更新时间。

| 客户ID | 公司 | 已选收件人 | 应交付draft_id及阶段 | 逐封内容状态及用户审阅结果 | 文件及锚点/指纹 | 公司状态 | 缺口/恢复条件 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

每完成一家公司、暂停、收到用户修改意见或输入变化时更新。默认同公司每阶段一封，收件组含全部已选联系人；分写须登记用户依据。反馈登记后未修订稿标需重写，不能仍算已复核；分写改合写时单列历史稿数量和新计划数量，不混算。记录公司数、收件人数、应交付/已保存/已复核草稿数，合并文件数另计。只读回看旧报告，不覆盖上游。

## 02_批次总结.md

- 范围：计划/实际处理公司、收件人及草稿数量。
- 结果：分别记录客户价值审核、事实资料审核及用户审阅；复用、修订、新写分别计数；completed、blocked、skipped及未处理公司分别列明。
- 限制：资料缺口、历史未核查、产品适用性、通道限制及未执行验证。
- 输出：草稿绝对链接、批次进度、检查点。
- 恢复：最后完整保存位置、待处理ID、输入变化、下一动作及条件。
- 外部动作：本写作Skill未执行发信/邮箱获取/CRM/外部上传；历史动作按来源另列。

## logs/checkpoint.json 字段

schema=1、batch_id、country、updated_at、owner、request_ref、skill_version、source_artifacts（path/sha256）、frozen_companies（customer_id/selected_recipients/required_stages）、drafts（draft_id/customer_id/recipient/stage/version/path/section/sha256/content_status/send_status/followup_status/blockers）、company_status、last_saved、next_action。

字段用于人工保存/恢复，不是现有自动检查器接口。只有文件写入并回读后更新对应指纹与状态；同一合并文件中的多封共享文件指纹但使用不同draft_id及section。未完成项保持真实内容，不能用空占位文件充当成果。
