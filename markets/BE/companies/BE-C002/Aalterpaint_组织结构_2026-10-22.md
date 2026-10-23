# Aalterpaint｜组织结构

## 元信息

- 客户ID：BE-C002；公司：Aalterpaint；国家BE；日期2026-10-22；批次BE-CONTACTS-20261022-01。
- 当前Skill V1.4/local-batch v1.2；company_key=BE:BE-C002；账本：D:\02钛白粉外贸\markets\BE\companies\BE-C002\contacts\ledger.json。
- 已确认官网/主体：https://www.aalterpaint.be/；AALTERPAINT bv，BE0658743331，Venecolaan8,9880Aalter；不同于Aalterpaint Holding，继承背调O/G。
- 关联背调：[原报告](D:\02钛白粉外贸\markets\BE\companies\BE-C002\Aalterpaint_背调报告_2026-10-22.md)，2026-10-22读取；业务与公开人员为继承证据，未称本轮重新背调。
- 本轮状态：completed：固定人选已补全并结算；更新2026-10-22T16:20:01+08:00。原免费阶段及修订前内容已留history快照。
- 四项材料入口：[联系人邮箱报告](D:/02钛白粉外贸/markets/BE/companies/BE-C002/Aalterpaint_联系人邮箱_2026-10-22.md#人员详情与交接开发信准备)。

## 公司主体及关系

| 主体/品牌/部门 | 注册号及地点 | 关系或职能 | 制造/采购主体线索 | 来源与状态 | 待核实事项 |
| --- | --- | --- | --- | --- | --- |
| AALTERPAINT bv | BE0658743331；Aalter | 工业涂料/包装涂料制造 | 原料采购主体及权限未知 | 背调O01/O02/G01/G02 | Holding与旧Libert法人不混同 |
| Libert Paints品牌/人员平台记录 | 关联品牌，具体员工法人待核 | 本次缺口搜索返回2名生产/质量线索 | 不当成已确认Aalterpaint雇员 | 背调G01及本轮Apollo | 当前雇主/采购权限未独立确认 |

## 检索日志及覆盖

| 动作 | 实际参数/分页 | total/实际返回 | 原始证据 |
| --- | --- | --- | --- |
| C-e76b691a255648 | {'_conversation_ref': 'bepersonq82n3', '_rationale': 'Research complete personnel scope of the approved organization', 'q_organization_domains_list': ['aalterpaint.be'], 'page': 1, 'per_page': 100} | 6/6 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json |
| C-d226dd5bf13949 | {'_conversation_ref': 'bepersonq82n3', '_rationale': 'Check missing production and quality functions without paid enrichment', 'q_organization_domains_list': ['aalterpaint.be', 'libertpaints.com'], 'person_titles': ['Production', 'Operations', 'Quality', 'Plant'], 'include_similar_titles': True, 'page': 1, 'per_page': 100} | 2/2 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-d226dd5bf13949.json |

原始返回8条，按Apollo ID唯一8人；另继承公开人员0条（匹配存在时不重复计员工）。aalterpaint.be首轮无职位过滤6/6已取完。生产/质量缺口按aalterpaint.be+已证品牌libertpaints.com及职位同义词补查，返回2/2，单列品牌关联、has_email=false，非独立确认本法人员工。管理、采购、研发、HSE/生产/质量线索已有，其他未检出不强补整图。

## 全量人员台账

姓名遮挡保留平台原值；揭示全名须收费补全或明确公开来源，本轮未收费。地区字段未返回，不从has_city/has_country布尔值推断地区。

| 人员编号 | Apollo人员ID | 原始姓名/遮挡姓名 | 已揭示全名及来源 | 原始职位 | 公司/分支 | 地区 | 职能归类 | 归属/现职状态 | has_email | 原始更新时间及时区 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C002-P001 | 5ffa09aad4b2620001313087 | Pieter Ve***n | Pieter Verheyen（2026-10-22 Apollo补全，同ID；公开原称另列） | CEO | AALTERPAINT | {'city': 'Ghent', 'state': 'Flanders', 'country': 'Belgium', 'time_zone': 'Europe/Brussels'} | 管理 | Apollo当前组织关联；非独立现职证明；补全平台current任职记录见下表，非独立任职核验 | True | 2026-10-07T14:08:25.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json；D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/BE-ENRICH-G1-20261022.json |
| BE-C002-P002 | 5eee0aa77a56fc0001fdd622 | Elisabeth Ch***x | 未揭示 | Responsable Marketing | AALTERPAINT | 未返回（has_city等仅可用性） | 销售市场渠道 | Apollo当前组织关联；非独立现职证明 | True | 2026-09-12T15:18:23.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json |
| BE-C002-P003 | 66f00a6e664fa9000163aad3 | Maxim Ve***e | 未揭示 | Preventieadviseur & HSE | AALTERPAINT | 未返回（has_city等仅可用性） | 其他/未明 | Apollo当前组织关联；非独立现职证明 | True | 2026-10-07T20:34:01.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json |
| BE-C002-P004 | 6426d703692628000138ba26 | Emile Na***t | Emile Naeyaert（继承公司页L01） | R&D Engineer | AALTERPAINT | 未返回（has_city等仅可用性） | 技术研发 | Apollo当前组织关联；非独立现职证明 | True | 2026-10-07T16:54:07.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json |
| BE-C002-P005 | 54a41a6d746869367600b82c | Hans Va***n | Hans Vanderbeken（2026-10-22 Apollo补全，同ID；公开原称另列） | Aankoop | AALTERPAINT | {'city': 'Ghent', 'state': 'Flanders', 'country': 'Belgium', 'time_zone': 'Europe/Brussels'} | 采购供应链 | Apollo当前组织关联；非独立现职证明；补全平台current任职记录见下表，非独立任职核验 | True | 2026-10-05T21:58:53.124+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json；D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/BE-ENRICH-G1-20261022.json |
| BE-C002-P006 | 66e70503ba52c90001d62f1e | Christophe Bo***t | 未揭示 | Kaderlid | AALTERPAINT | 未返回（has_city等仅可用性） | 其他/未明 | Kaderlid泛称，职责未知不选 | True | 2026-08-24T18:49:39.726+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-e76b691a255648.json |
| BE-C002-P007 | 62147788975b440001fd0937 | Martine Me***r | 未揭示 | Assistant Production Manager | Libert Paints | 未返回（has_city等仅可用性） | 生产运营 | Libert Paints平台关联/历史或品牌岗位，当前法律归属未核 | False | 2026-09-09T18:54:51.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-d226dd5bf13949.json |
| BE-C002-P008 | 54a7a1db74686965d93d3f47 | Cathy Ra***o | 未揭示 | Quality Control | Libert Paints | 未返回（has_city等仅可用性） | 质量 | Libert Paints平台关联，当前法律雇佣未独立确认 | False | 2026-09-12T04:59:09.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/C-d226dd5bf13949.json |

## 职能分布与管理线索

Pieter Verheyen经营CEO线索来自历史收购公告+当前Apollo CEO组织关联，今日经营职位未独立证实；Hans采购岗位以Apollo原称Aankoop记录，Exact历史客户案例确认其Aalterpaint关联但不证明当前岗位。Emile研发、Maxim HSE，生产/质量2名属于Libert平台记录，法律雇佣归属待核。未证实任一具名汇报关系。

| 职能/部门线索 | 台账人员/职位 | 负责人/职责证据 | 汇报关系 | 缺口 |
| --- | --- | --- | --- | --- |
| 管理 | BE-C002-P001 Pieter CEO | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 采购供应链 | BE-C002-P005 Hans Aankoop | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 技术研发 | BE-C002-P004 Emile R&D Engineer | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 生产运营 | BE-C002-P007 Martine Assistant Production Manager | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 质量 | BE-C002-P008 Cathy Quality Control | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 销售市场渠道 | BE-C002-P002 Elisabeth Responsable Marketing | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 财务人事行政 | 本次Apollo未检出；继承线索另见台账 | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |
| 其他/未明 | BE-C002-P003 Maxim Preventieadviseur & HSE；BE-C002-P006 Christophe Kaderlid | 按职位归类，非官方部门设置 | 未核实（明确例外见组织说明） | 非全体员工确认 |

## 自动选择、名额与执行

初选理由、剩余名额及当时未选原因按初选时点保留；当前实际执行结果以本节统计及末尾补全表为准。

本体有CEO Pieter及Aankoop Hans采购入口，选择2名第一组，不跨组补研发/销售到3；Kaderlid泛称无明确职责不纳入优选。采购是否为TiO₂原料未知。

相关岗位候选2；其中原始has_email=true 2；固定付费2。历史具名0，初选剩余名额3；本轮新增具名邮箱2、复验0，现累计2。公司流程上限3credits，已确认消耗2、未结算预留0、费用未知0、剩余可用1。

| 固定候选 | 台账/人员ID | 显示姓名 | 原始职位 | 联系价值 | 现职/职责疑点 | has_email | 优先组 | 状态/原因 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C002-C02 | BE-C002-P001/5ffa09aad4b2620001313087 | Pieter Ve***n → Pieter Verheyen | CEO | 与采购/经营职能有联系；具体原料权限未知 | 现职仅平台组织关联，职责品类未知 | True | primary | 已执行/匹配/有邮箱；实际1credit；BE-OP-BE-C002-C02-01 |
| BE-C002-C01 | BE-C002-P005/54a41a6d746869367600b82c | Hans Va***n → Hans Vanderbeken | Aankoop | 与采购/经营职能有联系；具体原料权限未知 | 现职仅平台组织关联，职责品类未知 | True | primary | 已执行/匹配/有邮箱；实际1credit；BE-OP-BE-C002-C01-01 |

2名均原始has_email=true，固定2人最多2credits，未批准/未预留/未调用。无历史个人邮箱；保留公共转介。品牌生产/质量人员false，不付费；不以其邮箱不可用改变第一组优先。

## 冲突、来源与更新

完整主体、品牌及产品证据继承[Aalterpaint背调](D:/02钛白粉外贸/markets/BE/companies/BE-C002/Aalterpaint_背调报告_2026-10-22.md) O01–O04/G01–G03/L01–L03。新增Apollo C-e76b691a255648（6人全页）、C-d226dd5bf13949（2品牌岗位缺口），原始参数/更新日期见文件。新增公开核对：https://www.exact.com/benl/klantervaringen/productie/aalterpaint-nv-benl （原文已读，案例未标发布日期，不能作现职证明）；https://be.linkedin.com/company/aalterpaint 本轮搜索摘要及背调L01原文复用。其他搜索重复/无关细节不采用。



相关岗位候选2；其中原始has_email=true 2；固定付费2。历史具名0，初选剩余名额3；本轮新增具名邮箱2、复验0，现累计2。公司流程上限3credits，已确认消耗2、未结算预留0、费用未知0、剩余可用1。

## 本轮实际补全、结算与交付核对

相关岗位候选2；其中原始has_email=true 2；固定付费2。历史具名0，初选剩余名额3；本轮新增具名邮箱2、复验0，现累计2。公司流程上限3credits，已确认消耗2、未结算预留0、费用未知0、剩余可用1。

用户已对工具总范围原文作出批准：

> Found 11 contacts. Enriching all will use up to 11 credits. You have 2484 credits remaining. Want to proceed, or narrow the scope?

用户原答：Proceed：按固定11人执行，最多11 credits。批准来源：主对话send_user_message_question_reply，questionItemId ["request_user_input_async","call_f14e757fbf6d49cfafd5f6ce6c88b944",0]。11人分10＋1，第二组在主对话确认已告知第一组结果后继续；无二次用户审批。原始工具说明：[固定清单](D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/03_固定付费清单.md)。

| 固定人员/操作 | 新全名/原始职位 | 组织/平台现职记录 | 地区 | 邮箱及服务状态 | match/catch-all/verdict | LinkedIn | 请求/证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C002-C01/54a41a6d746869367600b82c/BE-OP-BE-C002-C01-01 | Hans Vanderbeken / Aankoop | AALTERPAINT；[{'_id': '6ac41db26693cf0001dc2080', 'current': True, 'org_matched_by_name': False, 'organization_id': '5e576a8705b1890001e81e15', 'organization_name': 'Aalterpaint', 'start_date': '1992-09-01', 'title': 'Aankoop', 'id': '6ac41db26693cf0001dc2080', 'key': '6ac41db26693cf0001dc2080'}] | {'city': 'Ghent', 'state': 'Flanders', 'country': 'Belgium', 'time_zone': 'Europe/Brussels'} | hansvanderbeken@aalterpaint.be / verified | high / False / allow | http://www.linkedin.com/in/hans-vanderbeken-4a126b8a | 7757118278113307596；D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/BE-ENRICH-G1-20261022.json |
| BE-C002-C02/5ffa09aad4b2620001313087/BE-OP-BE-C002-C02-01 | Pieter Verheyen / CEO | AALTERPAINT；[{'_id': '6ad237bb29d2cb00017576ce', 'current': True, 'org_matched_by_name': False, 'organization_id': '5e576a8705b1890001e81e15', 'organization_name': 'AALTERPAINT', 'start_date': '2021-06-01', 'title': 'CEO', 'id': '6ad237bb29d2cb00017576ce', 'key': '6ad237bb29d2cb00017576ce'}] | {'city': 'Ghent', 'state': 'Flanders', 'country': 'Belgium', 'time_zone': 'Europe/Brussels'} | pieterverheyen@aalterpaint.be / verified | high / False / allow | http://www.linkedin.com/in/pieter-verheyen-a9a02ab8 | 7757118278113307596；D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-01/logs/evidence/BE-ENRICH-G1-20261022.json |

返回字段缺失均写未返回；request_id按字符串保留。按实际匹配ID与工具每匹配1credit费率逐对象结算，各组credits_consumed=10及1一致；不按账户余额差额分摊。平台current/起始日期并非独立现职证明，采购品类和权限未知仍保留。公司剩余名额不用于自动扩大本轮固定尝试。

本轮完成四项材料/渠道回读，全部原始证据、历史、费用及疑点保留。未起草或发送邮件。REWAH历史超限技术警告保留，结构检查不能证明事实、采购权或投递有效性。
