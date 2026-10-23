# 客户背调 Agent

角色 `customer_research` 承接市场搜集 Agent 的成果，按名单顺序逐家完成 OGLD 背调，优先复用已有报告。业务 Skill 是 GitHub 导入的 `research-customer-ogld`，原 Skill、SOP V1.1和报告模板保持源版本；本地补充负责批次管理。

## 调用示例

> 使用客户背调 Agent，对 markets/PE/prospecting/PE-20261022-01/01_候选客户总表.md 中所有有效公司逐家完成背调，优先复用已有报告。

> 使用客户背调 Agent，继续秘鲁上一批未完成的背调，沿用原队列和剩余预算。

> 使用客户背调 Agent，只调查日本名单中的 JP-C001；复用既有报告，有重要缺口再补核。

示例不是执行记录。指定名单以其实际内容为准，不能把不同批次公司数直接相加；用户明确限定范围时按限定执行。缺失国家或多份活跃任务不能唯一定位时才补问。

## 默认行为

- 全部唯一 valid 公司按首次出现顺序处理，其他状态列明未纳入原因。原ID和证据关联保留。
- 同主体完整旧报告直接复用，原文件与日期不变；缺口或新冲突定向补核，先保留历史快照。没有旧报告才新建。
- 每家公司报告保存、回读和进度同步后自动进入下一家，不逐家审批。
- 单公司无法完成时保存blocked及恢复条件并处理下一家；整体故障、不能记录或预算到限则暂停。恢复不重置队列和预算。
- 每家交付官网确认表、八节报告及OGLD执行复核表；按objective-evidence-v1，以客观证据作“继续开发／排除开发”结论，不判断购买意愿、不评分。必要调查未完成不交付为completed；充分调查后的未知保留。历史四分类再次使用须由背调Agent复核，原报告保持不变。

公司报告在 `markets/<ISO2>/companies/<已有目录或客户ID>/`；批次文件在 `markets/<ISO2>/due-diligence/<ISO2>-DD-<日期>-<序号>/`：

1. `01_批次进度.md`：任务、冻结队列、复用依据、进度与恢复点。
2. `02_批次总结.md`：处理结果、复用/补核/新增统计、结论、限制和报告索引。
3. `logs/checkpoint.json`、`logs/actions.jsonl`：内部恢复与对账记录，不代替正式报告。

首版没有设置默认查询数或时长上限，未指定就明确记录“用户未设硬性上限”；仍按有限替代路径调查，不无限重试。可在指令中设置本批预算，暂停与续接沿用同一额度。不会继承市场搜集阶段的40条查询预算。

## 实际运行与检查

项目入口由 AGENTS.md 路由。当前会话若未提供 `customer_research` 原生角色选择，主 Agent 读取完整TOML指令再交给专门子Agent；不能声称工具已自动加载新角色。无子Agent时主Agent依同一规则执行并说明。仅保存配置不证明桌面客户端的原生角色发现已测试。

角色会读取 [本地批次规范](../../skills/research-customer-ogld/references/local-batch.md)与[模板](../../skills/research-customer-ogld/assets/batch-templates.md)。只读检查命令：

```powershell
python -X utf8 skills/research-customer-ogld/scripts/check_batch.py --batch "<真实批次目录>"
```

0为已登记结构一致；1为错误；2为未知/未闭合动作或来源变更待对账。检查器不联网、不修改文件、不核验公司身份或来源语义、不保证所有实际调用都记入日志，也不提供并发锁。Agent仍需核对正式报告、源名单与实际工具历史。

原有报告复用不等于重新联网核验。公司调查完成不等于公司全部事实已查明，更不代表已获取有效个人邮箱或已发信。

## 维护与验证

角色：[customer-research.toml](../../.codex/agents/customer-research.toml)。源提交 `aa99ddf7583dee0cd7b6e8a472aa7b65aa802634`；同步与备份见[记录](../sync/github-sync-2026-10-22.md)。

原Skill五文件与源版本的对应关系保留在同步清单；新增本地规范、模板及检查脚本另行维护。没有用户级安装或GitHub推送。后续更新源Skill需核对差异并为新批次记录版本，不在运行中的批次切换。

开发验证及尚未覆盖的情况见[验证记录](customer-research-validation.md)。回归测试：`python -X utf8 skills/research-customer-ogld/scripts/test_check_batch.py`，仅使用虚构数据与临时文件。
