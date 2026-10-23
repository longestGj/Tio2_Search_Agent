# 调度字段契约 v1

内容：task → assignment → handoff → command → state。全部 JSON 为 UTF-8，可带 BOM；时间必须带时区。ID 只用字母、数字、短横线和下划线；公司 ID 大小写保留，不按名称或域名合并。国家使用 ISO2 大写。所有文件版本为 SHA256。

## Task

必填 schema=1、workflow_id、country、request_ref、entry_stage、scope、order、capabilities、budgets、overall_budgets。target_stage 默认 draft；显式单阶段填对应终点。阶段顺序 market → research → contacts → draft。

scope：mode 为 discovery_new/explicit_ids；requested_count 是授权公司数量；baseline_ids 是已存在的去重基线；selected_ids 是本次冻结名单；source_artifacts 是源文件引用。order 可给显式顺序，其余按 selected_ids 顺序。发现模式入口必须 market，首次无 ID；released 的市场交接冻结已选 items 中的 ID，累计数量不得超过 requested_count、不得包含 baseline_ids 或重复已选 ID。未达到原请求数量时可派新的空ID market assignment 补足剩余额度，已选公司与其进度不变；这不增加原授权数量。不能把整个累计表的 ID 填入 selected_ids。多余发现留在专业成果内。init_scope 是执行前已有明确市场选择引用时的替代入口，不能对已冻结名单扩容。

capabilities 为阶段到 {available, role_path, role_version} 映射。现有生产配置只将 market/research 置 true，角色路径分别为 .codex/agents/market-research.toml、customer-research.toml；role_version 使用实际文件指纹。未列出的能力为 false。测试的模拟能力不能复制到生产任务。首版能力表在任务内冻结；未来新角色接入需要明确迁移，不能改 JSON 偷偷绕过阻塞。

budgets 数组条目：budget_id、stage、unit、limit、used、unknown、authorization_ref。limit=null 是无用户硬性上限；unknown=true 不是消耗0。overall_budgets 条目为 unit/limit，只有同单位合计。每阶段分开记录并传给专业 Agent，额度不随任务/批次重置。

artifact 统一为 {path, sha256}，path 是项目内相对或绝对文件路径，可另附业务条目定位。检查存在、可读和指纹一致，不检查正文。业务结论及报告适用性均由生产者承担。

## Assignment

必填 assignment_id、revision（正整数）、stage、customer_ids、input_artifacts、owner、allowed_routes、budget_reservations、resources。

- assignment_id 每次实际尝试唯一，不能复用已释放编号；revision 是该尝试的输入版本。
- owner 是专业生产者的稳定标识。dispatched.executor_ref 是工具真实返回的执行者引用，不伪造。
- customer_ids 必须是当前阶段排队的冻结范围；发现模式首次 market 可为空。
- input_artifacts 引用实际输入和上游交接成果；后续输入不得省略所使用的成果版本。
- allowed_routes 从 advance/revisit/hold/end/finish 选取；不扩大任务终点。
- budget_reservations 是 budget_id→本次最大预留量；与已有消耗共同约束整体上限。执行者依预算约束执行，每次交接报告实际消耗。
- resources 使用 pool:PE、company:PE:客户ID、batch:项目内路径。工具自动补充公司 ID 和 market 国家池；实际报告写入路径也须用 batch 声明。路径归一化解析链接及 Windows 大小写，不能绕过同一文件写入占用。

任务单可附 workflow_id、country、instructions_ref、authorization_ref、output_location、resume_ref；主对话派发时必须传递完整任务卡和角色，不只发送短描述。额外字段不会作为脚本命令执行。

## Handoff

必填 handoff_id、assignment_id、revision、producer、stage、issued_at、batch_status、released、items、budget_used、uncertainty。

每个 item 必填 customer_id、execution_status（completed/blocked/cancelled）、business_conclusion（原文）、conclusion_ref、route、next_stage、route_reason、resume_condition、artifacts。completed 必须有非空成果清单，CLI逐份核对文件与指纹；blocked/cancelled 可以没有已完成成果，不伪造空报告。本批所有 assignment 公司均须交接，不能遗漏受阻项。业务原状态（如 valid/unresolved）可附 business_status，不转成调度质量评分。

| route | next_stage | 处理 |
| --- | --- | --- |
| advance | 紧邻下一阶段 | completed 且 released 后入队；未接入则 blocked/dependency_unavailable |
| revisit | 已授权范围内当前或更早阶段 | blocked，保存具体未完成事项与恢复条件；reopen 需新的查证引用 |
| hold | null | on_hold，保留专业暂缓结论 |
| end | null | ended，保留专业终止结论 |
| finish | null | 仅当前阶段是任务终点且 completed；draft_done 或 target_done |

draft 的 finish 另需非空 draft_ids 和 draft_files（草稿ID→artifact.path）。公司数与草稿文件数分别统计。专业角色负责确认所有应交付文件均已保存，调度不判断文案。

### 背调交接映射（用户2026-10-22最终确认：客观证据筛选）

在授权终点包含后续阶段、背调completed且released=true时，由背调生产者填写：

| 背调最终结论 | route / next_stage |
| --- | --- |
| 继续开发 | advance / contacts |
| 排除开发（生产者引用客观排除依据） | end / null |

调查完成后，有明确客观证据不适合的由背调Agent排除，其余进入组织结构/联系人及开发信；未知采购信息、联系人或购买意愿不是排除理由。背调生产者按objective-evidence-v1复核并明确填写去向，调度不读正文重新筛选或判断证据质量。充分调查后的限制随business_conclusion、route_reason、conclusion_ref及完整报告传递，不写成采购已证实。

旧“先补充核实／暂缓开发／不匹配当前产品”不作为新最终分流；历史标签不自动转换，交回背调生产者复核并提交新的判定/交接，已提交历史不改写。明确仅背调的任务两种结论均finish/null，保留筛选结果、不启动下游；未完成、未释放、缺能力或缺文件仍据实阻塞。通用hold/revisit保留给用户暂停或实际执行恢复，不用旧商业标签代替执行状态。

budget_used 是 budget_id→本 assignment 的累计实际消耗，不是全工作流累计；阶段中间交接和最终交接不得回退。最终遗漏的阶段预算标 unknown。uncertainty 数组填写消耗未知的 budget_id；其他业务限制写 items/route_reason，调用未知记录在 dispatch 中。budget_uncertainties 按 budget_id 保存未决 assignment ID；任务初始未知记 baseline。最终明确数字且未声明未知时，仅解除本 assignment 的未决项，不清除其他未决消耗。

released=false 不释放资源、不推进公司，后续生产者使用新 handoff_id 提交释放交接。同 handoff_id 同内容幂等，不同内容拒绝；旧 revision 仅留历史，不覆盖现有状态。生产者不得改写已提交文件。

## Command 与记录

统一 command_id、op、recorded_at。ID 重复且全部内容相同幂等；不同内容冲突。操作：

| op | 额外字段 |
| --- | --- |
| init | task |
| init_scope | selected_ids, evidence_ref |
| prepare | assignment |
| dispatched | assignment_id, executor_ref |
| progress | assignment_id, progress_ref |
| receive | handoff；artifact_check 由 CLI 生成，不能自行冒充检查 |
| reconcile_dispatch | resolution=existing_executor/not_dispatched、evidence_ref，前者另需 executor_ref |
| reconcile_budget | budget_id、used（核对后的工作流累计消耗，不得低于已确认值）、resolved_assignments（本次已核对的未决ID，可含baseline）、evidence_ref；只能在无活跃执行者时对账，不改变上限或授权 |
| reopen | customer_id、evidence_ref，必须对应已改变条件/新输入或可执行剩余步骤，不能重复旧引用 |
| source_change | customer_ids、evidence_ref，仅登记受影响项，不扩展名单 |
| pause / resume | 无 |
| cancel | customer_ids、request_ref；运行项只标 stop_requested，待执行者释放 |
| close | 全部公司闭合且无数量缺口可关闭；否则需用户明确关闭未完成范围的 request_ref；活跃执行者不能关闭 |

首版单写入者；events 每行含 schema/seq/event_id/recorded_at/command/state_after。不可变任务和交接按 ID/revision 保存。命令无业务质量字段；技术错误以 CLI error 或 technical_issues 返回，未通过的交接保留在输入文件，纠正后重交，不能声称 accepted。已入 handoffs 的当前版本代表机械接收，尚未释放不代表下游可用。

state 的 status=running/paused/closed；公司 status=waiting/queued/running/completed/blocked/cancelled，outcome=active/draft_done/target_done/on_hold/ended/cancelled。target_done 支持用户明确的更早终点，不能计为 draft_done。
