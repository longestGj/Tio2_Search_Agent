# 客户背调本地批次模板 v1.1

按真实执行填写，不以占位符生成完成报告。下列文件为示例结构；字段语义以 [本地规范](../references/local-batch.md) 为准。

## 01_批次进度.md

### 任务卡

| 字段 | 实际值 |
| --- | --- |
| 批次／国家／日期 | {实际批次ID、ISO2、北京时间} |
| 输入名单及配套证据 | {路径、版本、SHA-256、条目定位} |
| 采用版本 | {OGLD V1.1、本地补充v1.1、objective-evidence-v1、原来源commit及本地版本} |
| 纳入及排除 | {唯一ID顺序、范围、排除ID与原因、范围例外授权} |
| 原报告定位范围 | {本任务指定公司目录、市场索引及明确历史文件} |
| 预算与消耗 | {本批上限或未设；已确认量、未知项、主动时间依据} |
| 写入责任 | {唯一执行者、同公司冲突检查} |
| 输出目录 | {批次位置与公司目录} |

### 公司队列

| 序号 | 客户ID／公司／国家 | 来源条目 | 状态 | 处理方式 | 原报告／原日期 | 当前报告 | 当前步骤与剩余工作 | 阻塞／恢复条件 | 行动结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {1} | {实际主体} | {原ID/文件定位} | {四状态} | {三方式或未判定} | {真实路径、日期或无} | {真实路径或未生成} | {实际完成和未做} | {真实限制或无} | {继续开发／排除开发／未形成} |

### 复用检查／变更历史

逐客户记录身份匹配依据、旧报告是否有八节及完整来源、OGLD必要覆盖、已知冲突、本次更新要求、reused/supplemented/new理由、原SHA、快照路径、本次补核范围。直接复用明确“原调查日期保留；本次未重新联网核验”。旧四分类保留原文，在本表另记按objective-evidence-v1复核的日期、新结论与证据依据，不只换标签；必要漏项先补核。

### 最新检查点

- 当前公司、OGLD位置、下一家公司、暂停原因及恢复条件。
- 输入变化、冻结队列处理决定、未纳入的新ID。
- logs/checkpoint.json 和 logs/actions.jsonl 的实际路径及检查结果。
- 未闭合/未知/事后对账动作、预算确定程度、与实际调用历史核对范围。
- 公司报告、JSON和本表是否一致；不一致时明确最后可确认状态。

## 02_批次总结.md

### 交付范围

国家、固定输入及版本、任务目标、实际处理范围。明确“整批处理完成／阶段交付／零纳入目标”，不得将直接复用说成本次重新核验。

| 项目 | 实际数量 |
| --- | --- |
| 唯一纳入公司 | {Q} |
| queued／in_progress／completed／blocked | {各实际数，合计Q} |
| completed中reused／supplemented／new | {各实际数，合计completed} |
| completed中继续开发／排除开发 | {两类实际数及证据；合计本次按新政策完成复核数} |
| 历史结论尚未按新政策复核 | {ID、原结论；单列，不冒充新政策通过} |
| 输入未纳入 | {ID、数量与原因，不计完成；不同于完成背调后排除开发} |

### 报告索引

| 客户ID／公司 | 状态／处理方式 | 调查日期／本次补核日期 | 行动结论及重要限制 | 报告链接 |
| --- | --- | --- | --- | --- |
| {真实主体} | {实际} | {不改写历史日期} | {事实、推断、未知区分} | {真实可打开路径；阶段稿标明} |

### 复核与继续

记录官网表、八节、OGLD执行复核表、证据目录、事实/推断、贸易边界及客观排除依据等复核结果；列本批预算及剩余、受阻公司恢复条件、关键矛盾反馈ID、下一步。不把购买意愿作为待补背调任务。说明自动结构检查与人工覆盖复核范围，未知项不能写0。没有邮箱获取、发送或其他外部动作时如实记录。

## logs/checkpoint.json 起始样例

以下为**虚构样例**，只展示接口，不可混入真实客户成果。文件路径相对批次目录；实际需填真实源文件SHA。

```json
{
  "schema": 1,
  "batch_id": "XX-DD-EXAMPLE",
  "country": "XX",
  "skill_version": "OGLD V1.1/local-batch v1.1/objective-evidence-v1",
  "skill_commit": "aa99ddf7583dee0cd7b6e8a472aa7b65aa802634",
  "sources": [{"path": "input.md", "sha256": "实际SHA256"}],
  "source_changes": [],
  "budget": {"search_limit": null, "search_used": 0, "active_minutes_limit": null, "active_minutes_used": null},
  "items": [{
    "customer_id": "XX-C001", "company_name": "虚构样例", "country": "XX",
    "source_status": "valid", "source_locator": "input.md内XX-C001",
    "status": "queued", "mode": null, "stage": "intake", "next_step": "核对主体和旧报告",
    "research_policy": "objective-evidence-v1",
    "block_reason": "", "report_path": null, "report_sha256": null
  }],
  "updated_at": "实际带时区时间",
  "pause_reason": "无", "current_customer_id": null,
  "remaining_work": "执行已冻结队列", "ownership": "实际执行者",
  "exclusions": [], "budget_notes": "用户未设硬性上限；主动时间尚未记录"
}
```

completed时追加：identity_basis、checked_at、action（继续开发／排除开发）、实际report_path/report_sha256；排除另记exclusion_reason和exclusion_evidence证据ID非空数组。复用另记original_date/original_report_path/original_report_sha256及本次新判定依据；补核另记history_path。阶段未定字段不伪填，research_policy只有真实按该政策复核后才代表新标准完成。
