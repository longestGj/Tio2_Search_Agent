# Isamu Paint Co., Ltd.｜联系人邮箱

## 1. 元信息与执行状态

| 字段 | 内容 |
| --- | --- |
| 客户／主体 | JP-C001（JP-L001）；イサム塗料株式会社／Isamu Paint Co., Ltd. |
| 日期／版本 | 2026-10-21（北京时间）；V1.0 |
| 法人番号／官网 | 8120001034242；https://www.isamu.co.jp/ |
| 关联背调 | Isamu_Paint_背调报告_2026-10-21.md；libfile_bbef7f5e96408191bb49c3a63ae58872 |
| 组织结构文件 | Isamu_Paint_组织结构_2026-10-21.md |
| 当前状态 | 自动选人及公共入口整理完成；个人工作邮箱Enrichment等待Apollo工具强制确认，尚未调用 |
| 已有具名／剩余名额 | 当前已查记录中0人／3人；公共部门邮箱不计入 |
| 本次拟新增尝试／复验 | 1人／0人；若取得邮箱，累计为1人 |
| 本轮实际取得具名邮箱／累计 | 0人／0人；不得将拟获取视为已获取 |
| 邮件状态 | 未起草、未发送；未提交联系表单 |

用户2026-10-21持续业务授权：“每一家公司获取联系人邮箱不要超过3个。同时不需要我审批了”。已按该授权自动筛选；无需再选候选。当前唯一待确认事项来自Apollo接口的具体人数及费用强制要求。

## 2. 固定执行范围

| 固定编号 | 搜索人员ID | 原始姓名／映射姓名 | 原始职位 | 选人理由 | 疑点／状态 |
| --- | --- | --- | --- | --- | --- |
| C01／P01 | 67439e4b8e4370000160ac0f | Jumpei Ka***i；背调摘要映射Jumpei Kawai | Overseas Sales，Isamu Paint Co Ltd | 作为海外业务转介入口，询问滋贺工厂采购课或技术部负责人；并非已确认TiO₂采购人 | has_email=false；全名未由本轮Enrichment揭示；LinkedIn本轮打开失败；等待工具强制确认 |

C02／P02 Kobayashi Ta***i（ID 67438faf09c93e0001965012）职位仅Employee，职责不明，未选中，不获取。印尼3人不属于已确认日本主体，排除。本轮不会因为C01无邮箱而自动换人或扩大付费范围。

## 3. 费用与接口摘要

| 项目 | 记录 |
| --- | --- |
| 拟接口 | Apollo apollo_people_bulk_match |
| 拟参数 | details=[{id:"67439e4b8e4370000160ac0f"}]；reveal_personal_emails=false；reveal_phone_number=false |
| 工具计费 | 精确1 credit／匹配人，未匹配0；本次最大1 credit。匹配但无邮箱仍可能收费 |
| 查询余额 | apollo_users_api_profile(include_credit_usage=true)返回2405 credits；本轮查询快照，非调用后余额 |
| 强制确认 | 尚未取得本次1人、最多1 credit的工具要求确认；不能把一般任务指令当作费用确认 |
| 实际请求数／匹配数 | 0／不适用（未执行） |
| 实际返回有邮箱／无邮箱／失败 | 均不适用（未执行），不能记作接口未返回邮箱或请求失败 |
| 实际Enrichment费用 | 0 credits，原因是尚未执行 |
| 批次请求ID | 未生成 |
| 成功后应核对 | 按人员ID映射姓名、公司与域名，记录email_status、match_confidence、catch-all/verdict、任职及费用，未返回字段明确标注 |

工具要求的确认原文（本轮仅选定1人）：
> Found 1 contacts. Enriching all will use up to 1 credits. You have 2405 credits remaining. Want to proceed, or narrow the scope?

上文“all”只指固定选定的C01，不是搜索返回5人或日本公司2人。另有通用确认模板：
> This will enrich 1 people and consume up to 1 credits (1 credit per match, no charge for unmatched). Do you want to proceed?

## 4. 具名工作邮箱表

| 固定候选／ID | 姓名／职位 | 工作邮箱 | email_status | match_confidence | catch-all／verdict | LinkedIn | 来源／疑点 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01／67439e4b8e4370000160ac0f | Jumpei Ka***i；疑似Jumpei Kawai；Overseas Sales | 尚未获取；等待工具确认 | 未返回（未执行） | 未返回 | 未返回 | https://jp.linkedin.com/in/jumpei-kawai-412699203 | Apollo搜索＋背调职业摘要；本轮个人页读取失败，未独立确认现职 |

历史具名邮箱：已读背调及本轮Isamu文件查询未发现，当前记录0人。不猜测姓名拼音邮箱或邮箱格式。

## 5. 已有公共部门邮箱及官方联系入口

| 对象 | 地址／入口 | 来源、日期与状态 | 适用目的与限制 |
| --- | --- | --- | --- |
| 滋贺工厂品质管理课 | is-hinkan@isamu.co.jp | 已读背调引用企业署名SDS；https://www.tacmina.co.jp/tacmina/public/download/sds/Z1546.pdf ；SDS修订2025-07-03，背调2026-10-21读取；本轮复访返回维护页 | 公共部门邮箱，不计具名上限；可请求转介原料采购／技术，不是采购个人地址；未验证投递 |
| 滋贺工厂总机 | +81 77 562 1360 | https://www.isamu.co.jp/company/company-list/ ；本轮读取 | 可询问購買課／技術部负责人 |
| 本社总机 | +81 6 6458 0036 | https://www.isamu.co.jp/company/summary/ ；本轮读取 | 公司转介入口 |
| 官网联系表单 | https://www.isamu.co.jp/contact/ | 已读背调继承；本轮未提交 | 询问供应商准入负责部门；未发送 |

SDS托管站本轮显示TACMINA维护联系方式，它们不是Isamu联系方式，已排除。公共邮箱不是本轮Apollo获取成果，不标记verified或catch-all。没有已知email_status、match_confidence或实际投递结果。

## 6. 交接与来源

优先沟通目的：确认日本工厂TiO₂购粉或分散体、直接采购还是经商社、原料新供应商准入及技术评估负责人。C01为销售转介线索，不能预设采购权限或当前进口需求；不凭不完整指标推荐M系列牌号。

- 完整组织、搜索参数、5条Apollo原始人员、7位官方披露人员及所有来源网址，见配套组织文件。
- 本轮Apollo人员接口 apollo_mixed_people_api_search 的英文公司关键词查询返回5人，按ID去重5人；日本公司2人，印尼3人。域名、日文别名及关键职位补查均为0；不宣称搜全206名员工。
- 本轮来源：https://app.apollo.io/ （无公开单次查询链接；ID及参数已记录）；https://www.isamu.co.jp/company/summary/ ；https://www.isamu.co.jp/company/company-list/ ；https://www.isamu.co.jp/csr/env-efforts/ ；https://www.isamu.co.jp/company/quality-control-system/ ；https://www.isamu.co.jp/wp-content/uploads/2026/06/ir20260624_u4.pdf ；https://www.isamu.co.jp/wp-content/uploads/2026/06/80_Annual-report.pdf 。
- 继承且本轮访问受限：https://www.tacmina.co.jp/tacmina/public/download/sds/Z1546.pdf ；https://jp.linkedin.com/in/jumpei-kawai-412699203 ；https://jp.linkedin.com/in/kobayashi-tadashi-b49570208 。
- V1.0／2026-10-21：保存工具确认前实际成果。个人邮箱待获取，不能宣布全部任务完成。确认后沿用这两份文件身份更新，不新建重复文件；仅对固定C01执行，关闭私人邮箱和电话。
