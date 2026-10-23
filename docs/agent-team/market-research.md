# 市场搜集 Agent

名称：`market_research`。范围：指定国家的钛白粉候选公司搜集、四项基础核验、主体去重、预算管理与断点恢复。

## 使用

在本项目的 Codex 聊天中说：

> 使用市场搜集 Agent，为英国找到累计 20 家钛白粉候选公司。先核对已有名单，按现有 SOP 执行并保存四份报告。

也可以说：

> 使用市场搜集 Agent，继续英国上一批未完成的核验，沿用剩余预算，不扩搜新公司。

> 使用市场搜集 Agent，为德国再找 10 家候选公司，限涂料和油墨企业，本批最多 20 条查询。

示例不是已执行任务。国家、数量和预算以实际指令为准。

## 运行方式

项目角色入口：`.codex/agents/market-research.toml`。项目 `AGENTS.md` 提供调用约定。原 Skill、完整 SOP 和四文件模板均保存在项目 `skills/research-country-tio2-prospects/` 中。

本会话的子 Agent 接口没有自定义角色选择参数，因此当前调用方式是读取完整角色指令并交给专门子 Agent。兼容客户端可使用原生自定义角色发现；本次不声称已验证客户端自动发现。角色不设置模型覆盖，沿用当前会话设置。

交付位置默认是 `markets/<ISO2>/prospecting/<批次编号>/`：

1. `01_候选客户总表.md`
2. `02_证据与来源.md`
3. `03_搜索与覆盖记录.md`
4. `04_批次复核与测试报告.md`

每个文件使用已有模板。四种核验条件是公司身份、官网归属、目标国经营和相关业务。五种线索状态为 pending、valid、unresolved、duplicate、excluded。采购量、联系人或采购权未知不会自行否决已通过四项条件的候选。

历史联系人名单按公司主体归并；已有邮箱不代表通过本阶段核验。继续时读取检查点；数量达标仍需完成预算内核验收尾。不会进入背调、联系人获取或邮件阶段。

## 来源与维护

业务 Skill 来自 `longestGj/Tio2_Search_Agent`，2026-10-21 获取。来源文件与 Git blob SHA：

| 相对 Skill 路径 | Git blob SHA |
| --- | --- |
| SKILL.md | 7172a51a799f3b55af2df832f41f4728174c3e4c |
| references/sop-v1.2.md | d04f6596c5f646dfc39be6a8bc574693353ebfbf |
| assets/batch-templates.md | 8de14bb871c7b1f70d2547735ce946a3737bdde1 |
| agents/openai.yaml | ee70160ff51e497ea0fb9c5a7c6a68f0b7de7509 |
| assets/icon.svg | 3aa5522d9c0f47cbeaabca31dcbcb2111d99531b |

上表是2026-10-21导入时的来源版本。2026-10-22根据秘鲁试跑结果，本地修改了SKILL.md和四文件模板，增加[执行队列与逐次日志规范](../../skills/research-country-tio2-prospects/references/execution-logging.md)及配套Python脚本；这两个文件不再与导入SHA相同。业务SOP v1.2、图标和UI元数据保持原版。Codex本地存储和职责边界通过角色指令适配。只在当前项目配置，未安装个人全局Skill，未推送GitHub。

## 队列与日志

Agent每次新发现前检查完整待核验队列；有pending时只进行已登记公司的核验及替代查询。Skill中的`research_log.py`将开始、结果及状态变更追加保存到当前批次`logs/events.jsonl`，在已登记队列仍有pending时拒绝新的发现动作。失败、重试及替代来源分别留痕，中断保留未完成或执行未知项。

脚本不拦截浏览工具：Agent负责在实际调用前后写入，并在每轮及交付前与总表、工具历史对账。自动检查通过只说明已登记日志一致，不自动证明所有工具调用都已记录。使用步骤、错误恢复和字段说明见上述规范；回归测试用`python -X utf8 skills/research-country-tio2-prospects/scripts/test_research_log.py`执行，测试仅使用临时模拟批次。

本地补充v1.1增加正式报告检查点：每轮结束、达到目标转自检、暂停及交付前，先更新并回读四报告，再记录对应日志进度和文件指纹。缺少报告、进度过期或文件在检查后改动时，脚本拒绝跨轮开始；最终用`--check-reports`检查。无新增、仍有pending或尚未自检时保存真实阶段结果。文件一致性检查不能替代正文核验，Agent仍须对账；历史批次未按时保存的事实保留，不倒填检查点。

2026-10-21 项目清理后，旧资料和全团队设计草案归档到 `备份/2026-10-21_项目清理/`。当前目录只保留市场搜集 Agent 的必要文件。英国旧名单的实际路径已同步到角色指令，历史资料不因归档变为已核验，也不自动加载备份中的规则。
