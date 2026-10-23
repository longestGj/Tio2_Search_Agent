# 组织与联系人 Agent 验证记录

日期：2026-10-22。以下开发阶段记录保留原验证范围；随后已完成一次秘鲁真实查询，并按用户批准修正邮箱准入。最新修正见文末，不把早期离线检查通过当作邮箱获取效果通过。

## 基线与范围

本地完整复用Skill四资源，定向备份AGENTS.md、README.md及四文件，见[基线清单](validation-evidence/2026-10-22-company-contacts/baseline-manifest.json)。来源为项目2026-10-22同步记录中的原Skill，当前本地适配为流程V1.2/local-batch v1.0，不再声称修改文件与GitHub源逐字节相同。

独立执行者只读原Skill快照，按五个虚构场景应用。原Skill与本次用户指令能确定业务决策，但缺少批次恢复和持久公司费用接口；未人为捏造真实失败。见[基线应用](validation-evidence/2026-10-22-company-contacts/baseline-application.md)。

## 文件与完整Skill检查

TOML、UI YAML解析成功；原图标SHA-256不变；6份基线原值保持；原报告全部三级标题及表格32行逐行保留；完整Skill§0—§6及常见偏差存在。指定文档49个本地链接在首次文件检查时均可定位，新增链接由最终检查再核对。见[文件证据](validation-evidence/2026-10-22-company-contacts/file-checks.json)及[逐节保留和字段核对](validation-evidence/2026-10-22-company-contacts/skill-preservation.md)。

## 代码回归

- 新测试先因检查器文件不存在失败；实现预算与选人函数后14项通过。
- 新批次测试先因check_batch函数缺失失败；实现批次检查后30项通过。
- 公司收费必须登记预算、未关闭阶段不能标为全批完成：新增2项先失败后修复；再补同公司下批、跨会话ID映射和混合总扣费3项覆盖，联系人合计35项通过。
- 独立审查后新增两个恢复回归先失败后修复，联系人共37项通过。项目最终回归：联系人37、客户背调19、市场日志16、现有协调器42，共114项通过。原始输出见证据目录tests-final-*.txt；本任务没有修改其他三个业务检查器。

## 完整离线应用

五家虚构公司均保存两份公司报告，以及两份正式批次报告。A仅选采购、不补销售；B无第一组才技术/销售；C历史2邮箱及1 credit后仅一个新人名额；D身份冲突受阻；E结果未知保留最大预留并恢复原返回。报告先存而检查点滞后的恢复没有新增请求。

五个实际保存检查点的CLI退出码为0、2、1、2、0，符合预期；D始终受阻，所有all_completed=false。E仅一个operation，恢复只增加reconcile，两次模拟begin总数未变。见[阶段结果](validation-evidence/2026-10-22-company-contacts/offline-results.json)、[批次进度](validation-evidence/2026-10-22-company-contacts/offline-flow/01_批次进度.md)、[批次总结](validation-evidence/2026-10-22-company-contacts/offline-flow/02_批次总结.md)。

这是一份可复现的离线数据流应用，不是实际Apollo查询，也不是另一个Agent真实执行整批业务。旧阶段快照内绝对路径仍指模拟工作目录，只作审计快照。

## 独立审查与修复

[独立报告](validation-evidence/2026-10-22-company-contacts/final-review.md)基于修复前35项测试版本，发现两项Important：只有begin的中断无法追加reconcile；确认未执行后同人新操作被旧日志绑定阻拦。已各用新增测试复现失败，再修改并通过全套37项；保留未知不可重试、已执行不可抹除及确认范围不能重复使用的约束。

报告另指出离线组织报告缺逐动作证据，实施者按完整报告验收要求纳入同轮修复：独立字段检查先在op-a1缺失处失败，再补两报告共用逐动作表；最终10份模拟报告的operation_id、可用request_id和证据引用均通过。未将标题检查扩展为事实判断。

修复由原实施者以测试验证，没有第二次独立审查，不把原“需修复”报告改写成审查者复核通过。没有遗留的已确认审查问题。实际过程、审查边界裁定和证据见[实施进度](validation-evidence/2026-10-22-company-contacts/progress.md)。

## 限制

上述开发阶段未执行真实人员搜索、余额查询、付费enrichment、邮件发送、CRM写入、用户级安装或GitHub推送。文件解析和离线测试不能证明真实公司身份、岗位相关性、Apollo覆盖或邮箱可投递。客户端按名称发现新角色、长批次稳定性和跨进程写入协调仍需实际验证。

检查器只读核验登记数据、结构和引用，不提供自动调用拦截、并发锁、真实确认校验或完整历史防篡改。预算安全还依赖执行者核对实时工具费用、唯一公司映射及完整调用记录；报告字段完整性需按report-contract人工核对，标题检查不能替代内容验收。

## 秘鲁真实验证与邮箱准入修正

V1.2真实批次PE-CONTACTS-20261022-01覆盖14家公司，批准15人，实际15 credits，返回6个具名工作邮箱及1个部门邮箱，8人无邮箱；10家公司本轮处理完成、4家受阻。完整记录见[真实验证](validation-evidence/2026-10-22-contacts-peru-live/validation.md)。

用户指出产出问题后，逐人对照发现：搜索阶段7人has_email=true，均返回地址；8人false，均未返回邮箱却已收费。旧Skill仅要求记录标记，未将其作为付费准入；旧检查通过只证明其登记约束，并未验证邮箱队列是否值得付费。

用户批准后更新至Skill V1.3/local-batch v1.1。保留完整组织调查及岗位优先级，只有原始搜索has_email=true的人可进入固定付费队列；新增email_evidence路径/指纹和同ID原值核对。旧报告、批准和费用不改写，不再次获取邮箱。本轮测试及原始记录离线复核见[修正验证](validation-evidence/2026-10-22-contacts-email-gate/validation.md)。

## V1.3五家公司真实续测

用户随后授权另选5家秘鲁公司，批次PE-CONTACTS-20261022-02固定C007—C011。原始搜索共3个唯一平台人员，2人has_email=false未付费；唯一合格true候选在用户具体批准后取得1个具名工作邮箱，实际1 credit，实查余额2484。4家公司本轮处理完成、Grafinal因主体归属受阻；10份公司报告及2份批次报告已保存。

邮箱准入在本轮生效，但最终日志检查exit 1：旧end使用response_received且error为空，检查器未读取后续成功reconcile即报错。另有3次免费查询先于规则文件变化正式登记、旧end短暂修改后已撤回的执行偏差。保留真实记录，不把业务邮箱成功当作整个流程通过。完整结果、父Agent独立核对与待修复事项见[五家公司真实验证](validation-evidence/2026-10-22-contacts-peru-v13-live/validation.md)。


## V1.4四项开发信准备（2026-10-22）

按用户确认，组织与联系人阶段以向开发信交付联系对象、选择理由、沟通切入点和联系渠道为目标。四项材料放在联系人邮箱报告的简短元信息后；组织报告及批次总结直接引用。背调公开人员和业务证据直接承接，必要疑点就地简注，不另设使用边界栏目。详细调查、来源及费用保留在后；无个人邮箱或完整组织图本身不要求无限补查。原主体阻塞、准入、累计名额、预算及工具确认仍有效。

Skill V1.4 / local-batch与批次模板v1.2，schema=1不变。修改前快照、差异和指纹见[本次记录](validation-evidence/2026-10-22-contacts-outreach-handoff/manifest.json)。文件格式、Agent TOML及相对引用检查通过，原有45项检查器回归通过。

独立基线使用V1.3资料，缺少专门四项呈现；修改后另一独立执行者对PE-C008、PE-C007、PE-C051离线整理[三份交接样例](validation-evidence/2026-10-22-contacts-outreach-handoff/forward-samples.json)，覆盖既有个人邮箱、公共入口、公开具名人员无个人邮箱。主Agent回读并核对原报告事实、人员编号和来源；三种样例均正确区分材料交接、付费与执行状态，C051保持blocked。旧背调分类与法定后缀疑点保留，未借本次呈现更新旧判定。

[检查记录](validation-evidence/2026-10-22-contacts-outreach-handoff/checks.json)。本次只修改规则及做离线验证，未查询Apollo、收费、发信或重写历史业务报告。在途批次遵守原版本变化检查，不能静默切换规则。此前PE-CONTACTS-20261022-02的日志收尾故障未在本次修复；回归通过不代表该真实批次终检通过，也不代表真实端到端业务已验证。
