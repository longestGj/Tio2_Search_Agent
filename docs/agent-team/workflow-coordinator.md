# 统一调度 Agent

角色：`.codex/agents/workflow-coordinator.toml`；入口 Skill：`skills/coordinate-prospecting-workflow/SKILL.md`。

主对话负责调度，专业子 Agent 负责业务。默认链路为市场搜集 → 客户背调 → 联系人与邮箱 → 本地开发信草稿。调度只管理进度和交接，专业 Agent 的质量判断不增加第二道调度审核。

“秘鲁再找5家”仍只做市场搜集；“这5家一直做到草稿”才建立对应完整流程。累计名单只作为背景和去重基线，本次选择的 ID 单独冻结。

背调衔接按用户2026-10-22最终确认的objective-evidence-v1：背调Agent完成客观调查后，有明确证据不适合的“排除开发”→end，其余“继续开发”→contacts及草稿；仅背调终点两类均finish。旧四分类由背调生产者复核后给新判定，不自动映射。必要调查未做完仍属执行未完成，充分调查后的未知不阻断；调度不重判质量，实际文件/能力缺口据实记录。

当前 market/research 已接入。contacts/draft 尚未开发接入，因此真实全流程会在相应依赖处阻塞，仍保留草稿终点；不表示今天已能完成整条业务链。邮件发送及邮箱对接按用户约定留待全部业务 Agent 完成后讨论。

后续统一测试安排（用户2026-10-22确认）：先完成开发信 Agent，再用比利时（BE）市场测试从市场搜集到本地草稿的完整流程。暂不执行此前建议的秘鲁3家调度试跑；比利时测试数量与预算尚未确定，当前不启动真实查询或邮件发送。

每个国家任务保存至 `markets/<ISO2>/workflows/<任务ID>/`，包含任务进度、交接待办、状态、事件、不可变任务单/交接单和历史。正式进度随每次状态变化更新，不拖到收尾。业务成果仍在原 prospecting/、due-diligence/、companies/ 中。

用户可以说“继续这个工作流”“暂停”“只做背调”。恢复先定位原执行者和记录；派发未知时不盲目重派。运行中的取消先请求停止，只有收到释放交接才视为结束。无新条件的补核不会自动反复执行。

进度区分草稿完成公司、草稿份数、暂缓/终止公司和未完成缺口；关闭工作流不等于所有公司草稿完成。本角色没有后台进程，不会自行定时唤醒。

使用字段和命令见 [操作规范](../../skills/coordinate-prospecting-workflow/references/execution.md) 与 [字段契约](../../skills/coordinate-prospecting-workflow/references/contracts.md)。实际验证范围见 [验证记录](workflow-coordinator-validation.md)。项目源文件未安装到用户级 Skill 目录，未发布 GitHub。
