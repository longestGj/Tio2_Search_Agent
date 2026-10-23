# 简单发送Agent验证记录

日期：2026-10-22。范围：项目outreach_sender角色、阿里云Skill项目源和send_batch.py。按用户最新要求，不实施旧设计的账户锁、跨批次索引、自动恢复或逐封Sent核验。

## 已完成

- 复用5个现有阿里云Skill依赖源码，来源及原始指纹保存在[upstream.json](validation-evidence/2026-10-22-simple-sender/upstream.json)。未复制凭据、旧队列或邮箱数据；用户级源码指纹保持不变。
- 先添加测试，初始因缺send_batch模块失败；实现后测试通过。联合收件地址在现有连接函数中改为分开的SMTP地址列表，并返回逐地址拒绝结果。
- 简单批次支持指定带时区时间、到点执行、逐封30秒间隔、发送前后结果保存、异常停止、已有结果拒绝重跑。
- 独立只读审阅发现“挂起后迟发”和“错误类型丢失”两项；分别先加失败测试再修复。等待比预期多60秒以上直接停止；批次调用保留异常类型和整数SMTP状态码，不保存原始服务器错误文本。
- 当前18项离线测试全部通过，包括10家公司模拟、联合收件、异常/部分拒绝/中断停止、初始及封间挂起、修改输入、缺附件、未带时区、无授权引用、重复运行、只检查不连接、实际MIME签名图片及Reply-To和HTML转义。
- Skill格式检查、Agent TOML解析和CLI帮助检查通过。测试中的SMTP为模拟对象，时钟为可控时钟，不消费真实等待时间。

## 实际限制

没有连接邮箱、读取账户密码、发送邮件、创建系统定时任务或启动后台真实批次。未验证真实SMTP、实际投递、长时间后台运行或电脑在线条件。代码开发完成不等于这些验证已经通过。

本版只允许主对话协调一个批次运行，没有技术账户锁或跨批次去重。结果文件保护仅针对同一路径；人工另建清单前必须核对实际发送情况。程序必须保持运行，不能代替阿里云原生网页定时发送。

结果accepted只表示SMTP调用确认接受，尚未确认客户收件或阅读；unknown、partial或被强制终止遗留sending均需人工核对。正常发送不强制逐封查询Sent。

## 使用入口

[发送Agent](../../.codex/agents/outreach-sender.toml)、[项目阿里云Skill](../../skills/aliyun-email/SKILL.md)、[简单批次格式与操作](../../skills/aliyun-email/references/simple-batch.md)。

验证证据：[checks.json](validation-evidence/2026-10-22-simple-sender/checks.json)。原复杂设计快照保留在同证据目录，当前执行依据为[简单设计](outreach-sender-design.md)。
