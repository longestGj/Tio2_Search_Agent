# 开发信 Agent 实施计划

> 由主对话使用 executing-plans 逐项实施，保留变更快照和检查证据。

目标：以项目角色 outreach_writer 接收批次资料，完整调用现行开发信Skill，交付可逐封审核的本地草稿。
设计依据：[设计V0.3](outreach-writer-design.md)。本轮用户明确要求使用OpenAI Developers开发，沿用此前确认方案；执行本地文件修改，不重开API架构选择。

## 约束与检查重点

- 角色位于项目.codex/agents/；现行Skill1.4和SOP V1.2负责写法，角色负责批次推进和自身质量判断。
- 只沿用已选联系人，每公司最多3人；默认同公司已选联系人合写两封，仅用户明确要求分写时拆分。
- 合并文件与单封文件均支持；相同草稿ID跨修订不变；旧schema=1记录不自动转换。
- 单公司资料缺口不影响其他公司；保存失败等整体问题则暂停。
- 检查器只读，不发信、联网、加锁或判断文案事实；不启用生产调度能力。

## Task 1：只读批次检查

文件：skills/write-tio2-outreach/scripts/check_batch.py、test_check_batch.py、references/agent-batch.md。
接口：check_batch(batch: Path, root: Path, require_complete: bool=False) -> dict，返回ok/errors/counts。CLI --batch、--root、--require-complete；成功0，结构或输入错误1。

- [x] 编写正反例：合法完整批次、联合收件、漏稿、重复ID、越界收件人、3人上限、指纹变化、缺文件、误报完成、超90词、路径越界、部分完成、只读重复执行。
- [x] 运行并确认新增检查器尚未实现时测试失败。
- [x] 实现schema=2检查器；保留count_words.py计数语义。
- [x] 运行回归并保存结果。

## Task 2：专业角色与项目入口

文件：.codex/agents/outreach-writer.toml、AGENTS.md、README.md、docs/agent-team/outreach-writer.md；调整Skill本地执行说明与批次模板入口。

- [x] 完整读取Skill/SOP及输入；冻结公司、收件人与草稿计划，按职责写两封。
- [x] 明确单写入、阶段保存、历史复用/修订、缺口继续和恢复规则。
- [x] 显式assignment分支只按既有契约交接；独立模式无调度副作用。
- [x] 使用tomllib解析角色、核对引用及Skill元数据；运行离线场景复核。

## Task 3：验证与交付

- [x] 核对SOP与Skill写作规则未被另行复制/改写，用户数据及旧批次不变。
- [x] 最终独立只读审阅，重要问题修复后回归。
- [x] 保存验证报告，区分静态检查、结构测试、离线推演与未执行的新Agent真实批次。

当前不是Git仓库；文件快照在validation-evidence/2026-10-22-outreach-agent/before，不创建工作树/提交/推送。验证及实施过程追加同目录记录。

实施记录：已创建项目角色与schema=2只读检查器，31项结构/计数测试通过，CLI合成完整批次通过。旧schema=1历史记录及生产调度能力保持原状。最终独立审阅发现两项正文比对问题，已修复并复核通过。
