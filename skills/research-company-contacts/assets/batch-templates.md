# 本地批次模板 v1.2

配合[完整业务入口](../SKILL.md)、[两报告字段](../references/report-contract.md)和[本地协议](../references/local-batch.md)。用真实数据填写，下面XX均为虚构结构示例，不得作为真实执行记录。

## 01_批次进度.md

任务卡：批次、日期、输入文件/指纹、完整Skill版本/指纹、固定范围及顺序、执行者、每公司3人及3 credits、当前轮次、既有资料定位。

| 顺序/客户ID/国家/公司 | company_key/账本及接收快照 | 状态/Skill步骤 | 第一组核查/固定选人 | 已有/新增/复验 | 已耗/预留/未知/剩余credits | 两报告链接 | 下一步/受阻原因 |
| --- | --- | --- | --- | --- | --- | --- | --- |

分开列出已确认与等待确认范围、公司查询与人员enrichment种类、全批人数/最大费用/余额快照。记录输入变化、跨会话同人ID映射、未闭合动作、报告先存而进度滞后等对账；不把尚未执行填成功。

另列准入统计：岗位相关候选数、邮箱可用候选数（原始has_email=true）、固定付费人数、false/未知未调用人数。费用确认N仅取固定付费人数；无邮箱人员保留在组织报告，不补入付费队列。

## 02_批次总结.md

写明“整批处理结束／阶段交付”，公司总数及五状态数量；组织调查覆盖、选中人次、唯一人数、历史复用与本轮邮箱、匹配无邮箱/未匹配/未知分别计数。费用按公司列实际、预留、未知及可用，不将账户差额算成本批费用。

| 客户ID/公司 | 组织结果及限制 | 固定人选/角色/理由 | 联系人/渠道缺项 | 实际/预留/未知费用 | 组织报告 | 四项材料入口（联系人邮箱报告） |
| --- | --- | --- | --- | --- | --- | --- |

列来源/恢复位置、只读检查结果、人工对账范围及未验证事项。获取邮箱与发送状态分开；不得声称全部员工、全部采购关系或投递有效性已确认。

四项材料入口直接链接联系人邮箱报告的“人员详情与交接（开发信准备）”。缺项用简短事实表达，如“无个人邮箱，已有公司转介入口”“未确认具名人员，仅公共入口”或“对象及渠道均未取得”。个人邮箱已取得也照实保留部门/职责疑点；汇总不把阶段交付写成已可发送，不重复复制公司四项全文。

## 最小公司账本（虚构起点）

```json
{
  "schema": 1,
  "company_key": "XX:fictional-a",
  "workflow_id": "XX-contacts-a",
  "customer_ids": ["XX-C001"],
  "aliases": [],
  "credit_limit": "3",
  "contact_limit": 3,
  "baseline_evidence": {"confirmed": true, "source_ref": "虚构示例：已核对本流程无历史消耗；实际执行须填真实依据"},
  "contacts": [],
  "operations": [],
  "history": []
}
```

新建真实账本前先核对原有记录。后续每次更新先快照，不复制此空样例重置预算。批次checkpoint中引用该公司实际ledger_path和独立ledger_anchor指纹。

## 检查点填充顺序

1. 填schema/batch_id/phase=research/sources/skill_sources/source_changes=[]及next_step；指纹按真实文件计算。
2. items逐家填customer_id/country/company_key/ledger_path/ledger_anchor、status=queued/stage=intake、selection={primary_available:false, primary_basis:"尚未检索，不表示第一组不存在", people:[]}、reports={}、next_step。
3. 开始调查改in_progress；保存完整两报告并固定selection后改waiting_confirmation或在无可执行邮箱动作时据实结束。
   selection.people仅列通过岗位和邮箱准入的拟付费者，每人含has_email:true及email_evidence:{path:"实际原始搜索文件",sha256:"实际SHA-256"}；检查原返回同一ID确为true。非true人员另列报告；采购/管理有合适人但无邮箱时primary_available仍为true、people可为空。
4. approvals只填已经形成的实际工具确认资料；无确认保持[]。每个实际收费begin引用approval_id及已预留operation_id。
5. 第二轮更新phase=enrichment；每次实际返回同步日志/账本/报告；全部处理结束且无未知后phase=closed。受阻或等待确认保留实际状态。

JSON字段完整定义见本地协议，不用样例中的虚构确认或人名进行真实调用。


最终交付同时列出`outreach-recipient-handoff.json/.md`当前固定收件组入口；累计邮箱数与本次To人数分别统计。每组返回后先更新正式报告和检查点再继续下一组。
