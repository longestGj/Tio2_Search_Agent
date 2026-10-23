# 操作与恢复

这是由主对话调用的本地进度工具，没有自主后台进程，也不调用模型、Apollo、邮箱或网页。首次使用先读取 contracts.md。开发角色不等于授权执行真实客户任务。

## 命令入口

在项目根目录运行（替换为本次实际路径，不原样创建示例任务）：

```powershell
python -X utf8 skills/coordinate-prospecting-workflow/scripts/workflow_cli.py --project "D:/02钛白粉外贸" --workflow "D:/02钛白粉外贸/markets/PE/workflows/PE-WF-YYYYMMDD-01" --input "本次命令.json"
```

把 --input 和路径换为 --check 可只读检查；换为 --recover 可从已保存事件重建快照、任务单、交接单和正式进度。输入 JSON 使用当前真实带时区时间，不能用固定示例时间伪称实际执行。

每次调用读取 JSON 的 status、next_action、blocked_reasons、technical_issues。退出码0是记录成功，不代表全流程或草稿全部完成；1是参数/文件/资源冲突；2是需要恢复、派发未知或源版本变化。prepare 成功通常返回2，因为尚未获得真实执行者回执；此时只允许首次调用已准备的 assignment，不能重新 prepare。同一个保存不完整的命令先恢复，原 ID 和原内容重试不得重做业务。

## 执行循环

1. 定位唯一任务；已有工作流先 check。新任务 init 时路径必须为 markets/ISO2/workflows/任务ID，任务卡国家/ID与目录一致。
2. 选择排队的同阶段公司，按 task.order。根据任务和专业约束编写任务单、预留预算、声明写入路径。专业输入引用必须做指纹检查。主对话加载完整专业角色及其 Skill。
3. prepare 保存意图及资源占用。随后调用专业子 Agent 一次，并将工具真实引用通过 dispatched 保存。若工具结果丢失，检查原执行者列表/调用记录，不依据超时认定失败；查明后 reconcile_dispatch，evidence_ref 指向真实查证。
4. 进度回报使用 progress_ref；专业 Agent 保持其报告、日志、自检机制。主对话不运行专业检查器，不读业务正文做验收。执行者可在任务指定的临时位置交回 handoff JSON；由主对话 receive 保存不可变正式交接，专业 Agent 不写 state/events/资源表。
5. 交接缺字段、范围错误或文件不可读时，保留输入，交回原执行者纠正；调用成功后依已提交 route 排队。只有 released=true 才释放该 assignment 占用。返回0而联系人能力缺失时保留 blocked；不创建虚构执行者。
6. 暂停保存状态；需要停止运行者时请求其停止并等真实回报。取消尚未开始公司可立即记录，运行项不能假称已经停止。暂缓单家公司不阻止其他排队公司。
7. 每次命令自动更新 01_任务与进度.md、02_交接与待办.md。状态或 Markdown 落盘失败先 recover；不要直接改正式进度或 state 以绕过。

## 恢复与边界

- 项目资源表在 .codex/workflow-runtime/resource-owners.json。先项目锁、后工作流锁；锁排他创建，不能凭年龄/PID自动抢占。查证原写入者已经退出并保存查证记录后，人工明确处理异常锁；本工具不自动删除未知旧锁。
- 资源已认领但事件未写时，占用会保留。核对原准备命令与执行者；确证从未调用后可以用同一 assignment 和同一命令重试保存，再 reconcile_dispatch=not_dispatched。不能用新 assignment 绕过占用；不要手改资源表释放未知工作。
- 已写事件但快照、交接文件或进度缺失，recover 只重建调度记录，不再次调用外部业务。journal 尾行截断/序号冲突保留原字节并报错，不自动截短。
- 已接收的同一 command/handoff 重试先在锁内识别幂等；即使业务报告后来更新，也不重新接收或重查旧成果。旧revision迟到只登记历史；新的当前版本仍检查每份文件。init 的完全相同重试同样幂等，不覆盖任务。
- budget_uncertainties 给出尚未核对的 assignment/baseline。专业执行者补交明确最终消耗可解除自己的未决项；遗留基线或已释放任务的遗漏消耗，在取得实际查证后用 reconcile_budget 保存累计值和已核对ID。不得扣回已知消耗、改额度或清除其他未决项。
- 市场分批交付未到原授权数量时，可在原任务内另派空ID的 market assignment 补足剩余额度；已有ID不重选，预算和基线继承。没有新条件且专业阶段已明确暂停时仍须先满足恢复条件，不因剩余数量自动无限重试。
- 活跃占用记录缺失或被其他任务持有会报恢复异常；查证原执行者并修复占用关系后再恢复，不能重派。旧交接不能释放新 assignment 的资源。
- 来源变化使用 source_change，受影响公司等待专业核对。reopen 必须有实际新证据/新输入版本引用，不是任意改一个编号自动重试；语义是否满足条件仍由专业生产者确认。
- 工具只能协调使用本资源表的任务。已有独立专业任务和其他对话可能未登记，派发前仍须核对是否正在写同一池/报告；不声称全机排他。
- 正式输出和引用都限项目内；工作流路径按 resolve 检查。脚本不执行输入字符串、不扫描凭据或共享知识。

## 最小虚构示例

仅说明结构，不代表生产能力已就绪：

```json
{
  "command_id": "pause-001",
  "op": "pause",
  "recorded_at": "2026-10-22T10:00:00+08:00"
}
```

完整可运行虚构夹具位于 scripts/test_support.py，带 simulation 角色版本，仅用于测试。生产任务使用实际用户指令、角色指纹、预算与来源，不能复制模拟能力表。
