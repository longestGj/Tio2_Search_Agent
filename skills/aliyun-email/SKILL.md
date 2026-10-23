---
name: aliyun-email
description: Send an explicitly approved MYtio2 email batch through Aliyun at a specified time, one email at a time with 30-second gaps; stop on any error. Also inspect server Sent records when reconciling an interrupted batch. Not email writing or contact discovery.
---

# 阿里云邮箱：项目简单批次版

沿用既有阿里云邮箱Skill的连接与邮件构建代码。本项目只增加一个简单批次脚本，不修改用户级安装、不读取旧定时队列。读取[简单批次约定](references/simple-batch.md)后执行。

## 工作方式

1. 接收用户认可的邮件版本、已选收件组及发送时间。明确发送授权已经覆盖本批时直接执行，不逐封再问。只认可文案、设计或开发不等于允许发送。
2. 把完整对外纯文本（含称呼、正文、落款和完整文字签名）保存成每封一个UTF-8文本文件；不传整份内部Markdown报告。沿用原主题、联系人和附件，不改写业务内容。
3. 建立batch.json。一个公司同阶段合写为一项，最多3名已选收件人；公共部门入口用对应称呼。Mail 1与Mail 2分别按用户时间安排，不自动生成跟进序列。
4. 先运行不带`--send`的文件检查。只有资料齐全且本批发送授权明确，才加`--send`启动。程序等待到点，发一封、保存结果、等待30秒，继续下一封；任何异常即停，不自动重试。
5. 查看send-results.json并用自然语言总结实际结果。accepted仅指SMTP接受，不能写成客户已收到/阅读。正常情况下无需逐封查询Sent。

开发时用虚构数据和模拟传输，不连接邮箱。不用真实客户测试代码。

## 唯一执行者与中断

同时只运行一个批次，由主对话协调；不做账户锁、跨批次索引或自动恢复。已经产生结果文件的批次拒绝再次执行，不删除结果文件绕过限制。

中断、unknown或partial后先人工核对。按需要调用现有Sent查询，并核对最后发送记录；无匹配也不直接推断未发送。保留原批次，明确剩余范围和新时间后建立新批次。此人工处理不冒称能自动防止跨批次重复发送。

## 发件人与签名

本版发送账户固定ai-long@mytio2.com，Reply-To相同，显示名Ai Long。账户不符就停止，不打印凭据。完整文字签名由批准的body_file提供，图片由signature_image显式指定，不自动添加旧默认图。

当前用户指定图片：`D:/13钛白粉外贸开发之全面重启/公司资料/06邮件签名/IKHLAS_Ai_long_CHINACOAT_signature_compact.jpg`。正文中签名只保留一次；图片是内嵌签名，不是Mail 1产品附件。用户后续更换图片时按其要求使用。

凭据仅复用已有账户配置，禁止复制到本项目或日志。全局原Skill路径为`C:/Users/longe/.codex/skills/aliyun-email/SKILL.md`；本项目源代码来源记录见`docs/agent-team/validation-evidence/2026-10-22-simple-sender/upstream.json`。

## 命令

下列路径均从项目根解析，执行时转成绝对路径：

```text
python -X utf8 skills/aliyun-email/scripts/send_batch.py <batch.json绝对路径>
python -X utf8 skills/aliyun-email/scripts/send_batch.py <batch.json绝对路径> --send
```

第一条仅检查文件、时间格式和清单，不读取邮箱配置或连接网络；不证明用户批准、附件内容或图片显示正确。第二条有真实发送副作用。退出0表示本轮全部SMTP调用被接受；退出1表示检查失败或发送停止，具体以结果文件为准。进程被强行终止可能只留下sending，应视为待核对。

本版不使用复制来的`schedule`/`schedule-run`旧队列。邮件传输及Sent查询继续复用`email_cli.py`。异常核对时可只读运行`sent-search --message-id <实际ID> --save-dir <本批证据目录>`；记录没有ID时按实际日期、收件人和主题缩小范围。


## 卖方确认与结果回写

发送前读取sops/MYtio2_卖方资料与签名确认.md，复用有效用户确认，只有本次差异或新承诺才补核。结束或停止后，将实际send-results.json按draft_id关联回原写信批次：更新checkpoint中send_status、send_evidence（结果路径/指纹、Message-ID、收件组、时间）及两份报告、审阅汇总、源稿当前发送状态。先存history快照，已发送英文原文不改；未执行Mail 2保持未发送。SMTP接受不等于用户审阅、文案质量或投递验证，不能仅凭发送成功伪造内容审核。对应写信批次存在其他写入者时先协调，未完成回写则明确待办，不称全部交接完成。
