# 开发信智能体开发前 GitHub 核对

日期：2026-10-22（Asia/Shanghai）。本次是重新联网核对，不改写此前同步记录。

- 仓库：<https://github.com/longestGj/Tio2_Search_Agent>。
- GitHub 连接器确认默认分支为 main；实时 `git ls-remote` 确认分支提交为 `aa99ddf7583dee0cd7b6e8a472aa7b65aa802634`。
- 与上次同步提交一致，没有新提交需要下载。最新内容已在项目及上游快照中。
- 从固定提交读取全部62个 Git blob，并核对对象哈希；与活动目录逐文件比较：55个一致，7个有本地差异，0个缺失。本地差异全部保留，没有覆盖文件。
- 本次只写核对记录，没有推送 GitHub、安装技能或启动业务。

## 保留的本地差异

1. `markets/JP/README.md`
2. `markets/README.md`
3. `skills/research-company-contacts/SKILL.md`
4. `skills/research-company-contacts/agents/openai.yaml`
5. `skills/research-company-contacts/references/report-contract.md`
6. `skills/research-country-tio2-prospects/SKILL.md`
7. `skills/research-country-tio2-prospects/assets/batch-templates.md`

以上是字节差异登记，不代表重新验证这些文件中的业务结论。

## 开发信来源与缺口

上游包含市场搜集、背调、联系人三个 Skill，没有开发信专用 Skill。英国历史资料包含 `Annie_Sloan_Shahriar_Mail_1_2_2026-10-21.md`，可作为输出形式参考。该案例引用的《英国市场开发信编写SOP_Mail_Group_v1.0.docx》不在本次62文件的上游树中，当前活动资料也未提供这份原文。

不能把一份历史样稿宣称为完整业务 SOP，也不能把样稿中的发件身份、牌号推荐、收件人和长度要求自动推广到所有任务。新角色的业务设计须明确哪些是本次建议、哪些来自已确认项目约束。

机器核对清单：[github-check-2026-10-22-outreach.json](github-check-2026-10-22-outreach.json)。
