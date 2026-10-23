# 开发信 Agent 验证记录

日期：2026-10-22。实现：项目角色outreach_writer、Agent schema=2批次契约及只读检查器。写作业务入口仍为Skill1.4与SOP V1.2。

## 已执行检查

| 范围 | 实际执行与结果 | 证明边界 |
| --- | --- | --- |
| 官方配置依据 | 通过OpenAI Developers搜索并读取[官方Custom agents文档](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) | 项目.codex/agents/与name/description/developer_instructions结构有依据；不证明当前会话已热加载新角色 |
| 角色文件 | Python tomllib解析通过；三必需字段完整；引用文件存在；未覆写模型/权限 | 静态格式与引用检查 |
| 批次及计数回归 | 初始缺检查器时失败；实现后26项通过；补充缺邮箱受阻场景先失败、修复后27项通过；独立审阅后增加4项回归先失败后修复，最终31项通过 | 合成文件与机器可核对条件，不是文案质量或真实客户测试 |
| CLI | 合成1公司/2草稿完整批次，--require-complete退出0；报告与文件指纹核对 | 命令行可执行与结构完整 |
| 只读性与恢复基础 | 重复运行检查器前后临时目录文件字节一致；改源文件/删输出/漏草稿均被拒绝 | 无自动写入；恢复决策仍由Agent执行，未注入真实中断 |
| 独立审阅 | 初审2项P2已修复，原审阅者复核通过；24项批次测试复跑通过 | 只读代码/规则审阅，不是生产客户运行 |

证据：[测试输出](validation-evidence/2026-10-22-outreach-agent/tests.txt)、[静态检查](validation-evidence/2026-10-22-outreach-agent/static-checks.json)、[CLI结果](validation-evidence/2026-10-22-outreach-agent/cli-complete.json)。[独立审阅与修复](validation-evidence/2026-10-22-outreach-agent/review.md)。测试数据均为example.test虚构地址，无外部操作。

## 角色指令的离线场景核对（主对话）

| 情景 | 指令规定的行为 | 核对结果 |
| --- | --- | --- |
| 10家已选公司、上游资料可定位 | 冻结原ID/顺序/收件人，逐家执行完整Skill，不逐家索要下一步 | 角色第二至四节覆盖；未实际运行10家 |
| 2位联系人分别写 vs 用户明确联合 | 默认每人2封；明确联合组共2封，不能仅换名字或自动抄送 | 角色第二节及联合文件结构测试覆盖 |
| 油漆/塑料/油墨 | 读取现行固定对应表，不由Agent选择或新增型号 | 角色第三节引用Skill；本轮无产品选型测试 |
| Mail 1通过、Mail 2 REACH日期冲突 | 保留两稿；Mail 2待补资料，公司blocked，继续其他公司 | 角色第三四节及部分完成反例覆盖 |
| 缺已选邮箱 | 公司受阻说明缺口，原计划未确定不伪造收件人/空草稿 | schema=2支持空范围受阻；结构测试覆盖 |
| 旧稿、用户否定稿、已发送原文 | 分别核对复用、留快照重写、保护发送原文；保持ID | 指令覆盖；未在真实客户文件上执行 |
| 已有流程解释型句子 | 完整读取当前SOP，按专业读者与逐句信息增量审核 | 指令覆盖；人工质量不能由检查器保证 |
| 没有真实回复证据 | Mail 2仅备稿，未查邮箱记未核查，不虚构发送/回复 | 指令覆盖 |
| 显式assignment | 读取完整契约、冻结范围、提交全部项及draft ID/路径；无assignment不写handoff | 指令审阅；未运行生产调度集成 |
| Agent角色已新增但contacts未接入 | 不改生产能力表或旧任务冻结配置，不宣布全链路贯通 | 本轮没有修改调度代码与能力表 |

## 尚未验证

新角色的真实客户整批试跑、长期中断恢复、运行界面原生名称加载、实际邮件投递/客户反馈、生产contacts→draft调度集成均未执行。此前Bailey、Becker、Annie Sloan属于主对话Skill试写，不计作本Agent试跑。

## 变更与保存

旧设计、AGENTS、README及被修改Skill辅助文件的快照在[before](validation-evidence/2026-10-22-outreach-agent/before)。本轮不修改客户草稿、客户报告、当前SOP正文或Skill入口业务规则。当前工作目录不是Git仓库，因此无Git提交/推送；所有新增与修订文件只保存在项目中。


## 2026-10-22 同公司合写与反馈状态修正（当前Skill 1.5）

上文按人默认为旧版验证记录，已被本节和现行规则取代。真实英国试写已暴露同公司默认分写问题；本次同步Agent、Skill、SOP、模板及使用文档，默认同公司每阶段一封。

- 检查器新增4项回归：先观察2项失败，修复后共35项通过。拒绝需修改仍复核通过及未知审阅状态；允许保存真实重写进度，且严格完成检查拒绝。
- Skill格式与Agent TOML检查通过；独立规则场景核对通过，收件组变化的ID规则已澄清。
- 英国GB-OUTREACH-20261022-04：8封原稿保留正文并标需重写，当前改为4封联合计划，尚未生成；正常检查通过，严格完成检查如实失败。原REACH缺口保留。
- 本次未重写英文正文或发送；未验证新联合文案效果。

证据：[检查结果](validation-evidence/2026-10-22-outreach-joint-fix/checks.json)、[变更前快照](validation-evidence/2026-10-22-outreach-joint-fix/before)、[场景核对](validation-evidence/2026-10-22-outreach-joint-fix/rule-scenarios.md)。
