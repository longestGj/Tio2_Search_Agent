# 钛白粉外贸获客项目

当前开发与验证**市场搜集 Agent**、**客户背调 Agent**、**组织与联系人 Agent**和**开发信 Agent**，在本项目 Codex 聊天中调用。开发信承接背调、组织与已选邮箱资料，逐家公司保存本地草稿供用户审核；各阶段只在对应任务范围内执行。

## 当前文件

- [项目规则](AGENTS.md)
- [市场搜集 Agent](.codex/agents/market-research.toml)
- [国家客户搜集 Skill](skills/research-country-tio2-prospects/SKILL.md)
- [使用说明](docs/agent-team/market-research.md)
- [验证记录](docs/agent-team/market-research-validation.md)
- [客户背调 Agent](.codex/agents/customer-research.toml)
- [OGLD 背调 Skill](skills/research-customer-ogld/SKILL.md)
- [背调使用说明](docs/agent-team/customer-research.md)
- [背调验证记录](docs/agent-team/customer-research-validation.md)
- [已确认设计与实施进度](docs/agent-team/customer-research-plan.md)
- [组织与联系人 Agent](.codex/agents/company-contacts.toml)
- [完整组织与联系人 Skill](skills/research-company-contacts/SKILL.md)
- [联系人使用说明](docs/agent-team/company-contacts.md)
- [联系人验证记录](docs/agent-team/company-contacts-validation.md)
- [开发信 Agent](.codex/agents/outreach-writer.toml)：接收整批背调、组织及已选邮箱，完整调用[开发信Skill 1.4](skills/write-tio2-outreach/SKILL.md)和[当前SOP V1.2](sops/MYtio2_开发信编写SOP_Mail_Group_v1.2_审查稿.md)，默认Mail 1＋Mail 2，支持其他指定阶段及实际回复，止于本地草稿。[使用说明](docs/agent-team/outreach-writer.md) · [验证记录](docs/agent-team/outreach-writer-validation.md)。角色批次支持检查与恢复；生产统一调度接入另行验证。
- [统一调度 Agent](docs/agent-team/workflow-coordinator.md)：只管理任务与进度，完整任务默认到本地草稿；已接入市场与背调交接，联系人和撰写能力尚未接入。[设计](docs/agent-team/workflow-coordinator-design.md) · [实施计划](docs/agent-team/workflow-coordinator-plan.md) · [验证记录](docs/agent-team/workflow-coordinator-validation.md)。

调用示例：“使用市场搜集 Agent，为英国找到累计 20 家钛白粉候选公司，先核对已有名单。”

背调示例：“使用客户背调 Agent，对指定批次的有效候选逐家完成背调，优先复用已有报告。”给出名单文件或可唯一定位的市场批次即可；示例本身不是已执行任务。

背调公司报告在 `markets/<国家代码>/companies/`，批次进度、总结和内部日志在 `markets/<国家代码>/due-diligence/`。开发完成不代表已对整个市场实际运行。

联系人示例：“使用组织与联系人 Agent，处理指定背调批次，自动选人，采购和管理优先，每家公司最多3位联系人及3 credits。”两份公司报告与持久预算账本在同一公司目录，批次文件在 `markets/<国家代码>/contacts/`。工具要求的具体付费确认满足后才获取邮箱；开发验证不消费真实额度。

新任务成果在执行时写入 `markets/<国家代码>/prospecting/<批次编号>/`。已从 GitHub 下载的历史市场资料保留原有 `source-lists/` 和 `companies/` 结构：

- [日本市场资料](markets/JP/README.md)
- [秘鲁市场资料](markets/PE/README.md)
- [英国历史市场资料](markets/GB/README.md)
- [哥伦比亚候选市场](markets/CO/README.md)（2026-10-22本轮净增30家达标；最新累计90家有效、3条未解决，pending为0）

最新市场批次：[哥伦比亚净增30家至累计90家](markets/CO/prospecting/README.md)（2026-10-22，CO-20261022-03）。基线60家、本批新增32条，其中30家有效、2条未解决；累计90家有效、3条未解决、pending为0，净增30家目标达成。新增30家已全量检查，8家完成同一执行者自检（含风险项及有记录随机样本）；官网污染、替代公开主页、来源措辞修正和8条读取目标格式偏差均在报告保留。用户于11:38明确追加30查询、40新登记、60分钟主动及45分钟收尾，原用量不清零；最新累计查询66/80余14、登记93/110余17，时间账本见复核报告。五类、英西语及官网/协会/展会渠道均有本批实际尝试，未完整遍历名录或全国地区。继承60家有效记录沿用旧状态，本轮未重新全面联网核验。

上一哥伦比亚批次：[净增40家至累计60家](markets/CO/prospecting/CO-20261022-02/04_批次复核与测试报告.md)。本批新发现38家有效、历史未解决线索补核2家；40家新增/更新有效记录已全量检查并完成11条自检。原报告、预算追加和执行记录保留，不能与最新累计池简单相加。

秘鲁最新批次：[新增5家及累计65家候选池](markets/PE/prospecting/README.md)（2026-10-22，PE-20261022-02）。旧60家沿用历史核验状态，本轮新增5家完成基础核验并全部复读自检；四份报告在转自检前和结束后分别保存，轮间检查通过。以上市场的候选资格均不代表已确认采购需求。

本次下载不代表重新核验市场数据。[下载版本与校验记录](markets/download-manifest.json)。

2026-10-22 已全量同步 GitHub 仓库的62个文件，保留本地日志改进与最新秘鲁成果，新增英国资料及背调/联系人Skill；详见[同步记录](docs/sync/github-sync-2026-10-22.md)。联系人Skill已保存但未自动启动业务，也未安装到用户级目录。

同日重新获取GitHub提交`e777f802`，最新63文件快照已保存，新增开发信SOP，保留7处活动目录差异。详见[最新SOP同步记录](docs/sync/github-sync-2026-10-22-outreach-sop.md)。项目内可明确要求“读取skills/write-tio2-outreach/SKILL.md，为指定联系人起草Mail 1和Mail 2并本地保存”；未安装到用户级目录，示例不代表已执行。

## 整理前备份

[备份说明](备份/2026-10-21_项目清理/归档说明.md)及[逐文件校验清单](备份/2026-10-21_项目清理/归档清单.json)。

旧资料按原目录结构归档；当前 Agent 相关文件保留在活动目录，并在备份中另存整理前快照。无文件删除。备份中的规则和历史设计不自动用于当前任务。
