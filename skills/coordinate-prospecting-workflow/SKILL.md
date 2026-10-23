---
name: coordinate-prospecting-workflow
description: Use when coordinating an explicitly requested customer development workflow across market discovery, company research, contacts and local email drafts, or resuming its saved progress. Also applies to explicit workflow-coordinator requests; ordinary market-only and research-only work keeps its existing entrypoint.
---

# 客户开发流程调度

运行于项目主对话，只管理范围、进度、交接、阻塞及恢复。专业 Agent 决定业务结论、质量和下一步去向。调度不读报告正文做验收，不运行专业业务检查器，不评分、不改写结论。

执行前读取 [字段契约](references/contracts.md) 与 [操作和恢复](references/execution.md)。工具位于本 Skill 的 scripts/；通过 workflow_cli.py 操作，不能直接改 state.json。

1. 从用户请求确定范围和终点。完整开发默认本地草稿；“再找5家”仅市场阶段，“只背调”仅背调。保存原始指令引用。当前已接入 market/research；contacts/draft 未接入，保持阻塞，不以调度者补做。
2. 现有任务先 `--check`。不要因当前记录不全重新开任务。范围冻结、阶段预算与未知消耗继承；总表65家与本次选定5家分别保存。
3. 派发前读取完整专业角色，保存唯一 assignment。prepare 返回 dispatch_unknown 是已保存意图，不能据此重派。随后只调用一次专业子 Agent，把完整角色、任务单、预算、范围、输入版本、输出位置一并传入；获得真实执行者引用后 dispatched。未知调用必须查原执行者并 reconcile_dispatch。
4. 运行中只保存progress_ref。批次交接字段、ID及文件指纹通过且released=true后，执行生产者明确填写的advance/revisit/hold/end/finish。背调按objective-evidence-v1：已完成“继续开发”进入contacts，“排除开发”结束该公司下游，均保留证据和限制；仅research终点两类均finish。旧四分类或缺去向交回背调生产者复核并重新提交，不改历史、不由调度判断业务质量或OGLD充分性。
5. 一个工作流只运行一个专业执行者；专业 Agent 不自行派下游或再派子 Agent。只认领本任务资源；无法证明旧写入者已结束时不抢占。既有未采用资源表的任务仍须人工核对占用。
6. 每次状态变化即时更新两份正式进度；持久化不完整先恢复。读取业务成果只用于路径/字节指纹，不判断内容质量。用户暂停不等于执行者已停止；等待明确释放。
7. 汇报已完成公司、草稿份数、暂缓/终止、数量缺口、缺失能力和下一步。closed 不等于全部草稿完成。不得承诺无后台程序的自动轮询。

本 Skill 不调用邮箱、不创建发送计划，不授权真实业务查询、付费查询、跨对话消息或外部写入；沿用本任务已有授权和工具要求。
