# MARTIN MATHYS｜组织结构

## 元信息

- 客户ID：BE-C013；公司MARTIN MATHYS；BE；首次2026-10-22；更新2026-10-22T19:25:00+08:00；批次BE-CONTACTS-20261022-02，执行者/root/be_contacts。
- Skill V1.5/local-batch v1.3，实际冻结指纹见checkpoint。company_key=BE:BE-C013；持久账本D:/02钛白粉外贸/markets/BE/companies/BE-C013/contacts/ledger.json。
- 官网https://www.mathyspaints.eu/；主体依据：O02官方Offices与G01登记整理的VAT0437896404、Kolenbergstraat23及3545一致；官网Zelem和登记Halen地点口径保留；G03集团原文同VAT与当前代表进一步匹配；业务/地址/法人/制造分工原值见关联背调，不把集团数当本体。
- [关联背调](D:/02钛白粉外贸/markets/BE/companies/BE-C013/Martin_Mathys_背调报告_2026-10-22.md)：2026-10-22读取，沿用当日原调查证据，不称本次重新核验。当前状态completed；组织调查完成不代表取得邮箱。
- [四项材料与本次收件组](D:/02钛白粉外贸/markets/BE/companies/BE-C013/Martin_Mathys_联系人邮箱_2026-10-22.md#人员详情与交接开发信准备)。

## 公司主体及关系

| 主体/品牌/部门 | 注册号及地点 | 关系或职能 | 制造/采购线索 | 来源/状态 | 待核实 |
| --- | --- | --- | --- | --- | --- |
| Martin Mathys NV/SA | BE0437896404；Kolenbergstraat23，Zelem/Halen | 涂料制造主体/Mathys品牌 | Halen Planning招聘含原料采购 | 背调O02/G01/G03/L04 | 不把法国SIREN休眠或美国集团数据套BE |
| Rust-Oleum Europe/RPM | 欧洲集团/品牌体系 | 集团职能可能覆盖本体，独立采购权未知 | 地区角色分列 | 背调G02/G04 | 不混为本地全部员工 |

## 检索日志及覆盖

| 接口 | 实际查询日期 | 完整参数/分页 | total/返回 | 原始证据 |
| --- | --- | --- | --- | --- |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:12:58+08:00 | {'_rationale': 'Research all indexed local personnel across the confirmed company and European group domains, retaining legal-entity limits.', 'q_organization_domains_list': ['mathyspaints.eu', 'rustoleum.eu', 'rust-oleum.eu'], 'person_locations': ['Belgium'], 'page': 1, 'per_page': 100} | 22/22 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:13:10+08:00 | {'_rationale': 'Check procurement and management gaps across the confirmed parent-company domain in the local region.', 'q_organization_domains_list': ['rustoleum.com', 'mathyspaints.eu', 'rustoleum.eu', 'rust-oleum.eu'], 'person_locations': ['Belgium'], 'person_titles': ['purchase', 'procurement', 'planning', 'managing director', 'director', 'president'], 'page': 1, 'per_page': 100} | 2/2 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-e52671f26da2.json |

实际返回24，按ID唯一22；检索人数不等于当前在职人数。首轮已确认Mathys/Europe三域，Belgium地区且无岗位过滤22/22完成；追加Rustoleum.com集团域及采购/Planning/管理关键词2条均原ID。唯一22、实际24。平台未检出官网Frank/Tom，不等于离职；继承已读当期官网代表证据。技术/制造/质量已见，不为补名收费。

## 全量人员台账

搜索姓氏遮挡为接口预期，未收费揭示；已有公开来源全名另列，不猜补。原始更新时间含时区，未返回字段如实保留。

| 人员编号 | Apollo ID | 原始姓名 | 全名/来源 | 原始职位 | 公司/分支 | 地区 | 职能归类 | 归属/现职 | has_email | 原始更新时间 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C013-P001 | 57dfb529a6da980b0b57607b | Lieselotte Br***s | 未揭示 | Human Resources Officer | Mathys Paints | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-07T19:24:01.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P002 | 57d8e262a6da98726a96b96a | Bart Ca***s | 未揭示 | Maintenance Engineering Manager | Mathys Paints | 未返回，has_city/country仅可用性标志 | 生产运营 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-07T15:37:46.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P003 | 609cea3e297d150001413f9e | Sietse La***e | Sietse Lapeirre（继承L01） | Product Manager Industrial | Rust-Oleum Industrial Europe | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-09T14:28:04.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P004 | 6277db90f84332000101ea96 | Robin Ca***s | 未揭示 | IT Support Medewerker | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-12T12:08:23.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P005 | 54c29ba97468691639134fae | Mieke Co***s | 未揭示 | Marketing Department - Graphic Design | Mathys Paints | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-08T20:17:27.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P006 | 54a1f9ae7468693825024702 | Iris Va***n | 未揭示 | Accounting Manager | Mathys Paints | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-01T23:13:29.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P007 | 54a325e97468693fda9a7457 | Vincent Go***t | 未揭示 | Key Account Manager Belgium & Luxemburg Consumer Brands | Rust-Oleum Industrial Europe | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-13T20:17:40.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P008 | 5e99435537a9a700985e398f | Tom Kn***n | 未揭示 | Reverse Logistics Employee | Mathys Paints | 未返回，has_city/country仅可用性标志 | 仓储物流 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-08T02:05:59.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P009 | 5f67e1e16c67400001bbef1f | Ward Ad***s | 未揭示 | Manufacturing Chemist | Mathys Paints | 未返回，has_city/country仅可用性标志 | 生产运营 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-09T01:08:21.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P010 | 657c0bae348072000193d10a | Femke Da***s | 未揭示 | Planner | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | Planner不自动等同采购；职责/品类未知，虽has_email=true仍不付费 | True | 2026-10-05T20:38:24.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P011 | 642855875ca76e000112de7a | Bedir As***u | 未揭示 | Customer Contact Officer | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-15T07:14:50.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P012 | 60a59287379f260001ef59eb | Ken Se***s | 未揭示 | Project Employee | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-07T13:34:57.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P013 | 642ed665fa6fcc0001ef36a8 | Beau Ca***e | 未揭示 | Kwaliteitsanaliste | Mathys Paints | 未返回，has_city/country仅可用性标志 | 质量 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-08T09:50:42.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P014 | 6111c7bf680bbc00013216cd | Liesbeth Ma***t | 未揭示 | Production Planner | Rust-Oleum Industrial Europe | 未返回，has_city/country仅可用性标志 | 生产运营 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-12T19:51:57.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P015 | 5d5839bca3ae61e06fd7eab3 | Mia Ve***n | 未揭示 | Colorist | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-08T11:48:52.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P016 | 54a601fb7468692cf02271ba | Gerben Br***s | Gerben Brands（继承L02） | Prevention Advisor | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-22T10:13:08.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P017 | 54a46f7d7468693442ee4347 | Kris Wu***s | 未揭示 | Production Manager | Mathys Paints | 未返回，has_city/country仅可用性标志 | 生产运营 | 平台组织关联/现职线索，非独立核验 | False | 2026-10-06T20:47:21.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P018 | 54a5a1af7468692fa246aa9e | Ann Ge***s | Ann Gerrits（继承L06历史招聘，现职仍平台线索） | Planning Manager Mainland Europe | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台规划管理与历史职衔一致，原始has_email=false；未付费 | False | 2026-10-13T04:31:17.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P019 | 55705cc27369643873788a00 | Marc Vl***e | 未揭示 | 未返回 | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2025-11-21T18:11:31.457+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P020 | 64ea324f82f2290001c427bb | Jan Hu***s | 未揭示 | Continuous Improvement | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-10T10:10:12.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P021 | 6122e3eed4cd7300018f141c | Kevin V | 未揭示 | Team Lead | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-08-07T22:38:13.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |
| BE-C013-P022 | 68f0e27b0ec8e60001f7c712 | Mario Gu***n | 未揭示 | Colleague | Mathys Paints | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-10-04T21:32:23.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-5c80fbcb082d.json |

### 继承背调全部公开人员与职责线索

以下为原L节全量承接，原来源编号、公开邮箱归属/历史/异地/占位限制保留；不是本轮Apollo确认人数。与Apollo可能重叠，不能相加为员工数。



L01从集团官网实际LinkedIn链接进入Rust-OleumIndustrialEurope，再经相关页L02匹配MathysPaints；域名、Kolenbergstraat23/Zelem、涂料业务相符，为品牌/业务页不是独立法人证明，平台规模不套用本案。L03官方招聘概况及L04 Aankoopmedewerker原文：Halen Operations，Planning部门覆盖原料、包装、营销和成品采购及国际供应商对接，证明岗位职能，未点名任职人或决定新供应商权。L05维护技师采购为维修件/备件，明确不同于原料采购。L06两年前已停申请的LinkedIn采购招聘显示发帖者AnnGerrits、PlanningManagerMainlandEurope；L07个人页999，当前职衔仍未证，采用历史招聘和原官网岗位作替代。两名官网代表及其他相关公开姓名保留，不选人。

| 姓名／部门 | 职位、雇主、地区 | 现职/职责边界 | 来源 | 邮箱及验证 |
| --- | --- | --- | --- | --- |
| Frank Costermans | 官网ManagingDirector，MartinMathys，Zelem | 官方自述现职；未证明原料采购权限 | O02/G03/L02 | 未获取 |
| Tom Lowdon | 官网Director，MartinMathys | 同VAT两官网一致；采购权未知 | O02/G03 | 未获取 |
| Ann Gerrits | 历史招聘PlanningManagerMainlandEurope，MartinMathys，Halen | 2年前岗位发帖者；个人页999，完整当前任职未核实 | L06/L07 | 未获取 |
| 采购/Planning部门 | Aankoopmedewerker，Halen | 原料至包装等范围，招聘不等于任职人 | L04 | 无个人邮箱 |
| 维护部门 | Onderhoudstechnieker，Halen | 维修备件采购，非原料采购候选结论 | L05 | 无个人邮箱 |
| Bart Coolman、Gerben Brands | MathysPaints员工名单 | 具体职责/现职未知 | L02 | 未获取 |
| Sietse Lapeirre、Patricia Nagels、Raimond Loeffen、Jan Jacobsen | RustOleumIndustrialEurope公司员工名单 | 集团/国家权限未核实，后两人为跨国线索 | L01 | 未获取 |
| 公司/集团公共入口 | info@rust-oleum.eu、rpmeurohas@rustoleum.eu | 前者集团通用；后者SDS责任部门，不是具名个人 | O04/O05 | 官方公开未验证 |
| 招聘系统入口 | apply.martinmathysnv@recruitee-mail.com | 招聘技术协助，不作业务收件人 | L04/L05 | 官方招聘公开未验证 |


## 职能分布与管理线索

Ann Ge***s当前平台Planning Manager Mainland Europe，与背调两年前Ann Gerrits招聘原称一致；只加强平台现职线索，不把历史招聘时间倒写2026。原始has_email=false，保留不付费。Femke Planner是否实际承担L04采购范围未知，不因has_email=true加入。生产Kris/维修Bart等不是已证原料采购。Frank ManagingDirector与Tom Director沿用官方同VAT当前联系页，无对应搜索ID/邮箱。无具名采购汇报图。

| 职能 | 人员/原始职位 | 负责人/职责依据 | 汇报关系 | 缺口 |
| --- | --- | --- | --- | --- |
| 管理 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 采购供应链 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 研发技术 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 生产运营 | BE-C013-P002 Bart Maintenance Engineering Manager；BE-C013-P009 Ward Manufacturing Chemist；BE-C013-P014 Liesbeth Production Planner；BE-C013-P017 Kris Production Manager | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 质量 | BE-C013-P013 Beau Kwaliteitsanaliste | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 仓储物流 | BE-C013-P008 Tom Reverse Logistics Employee | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 销售渠道 | BE-C013-P005 Mieke Marketing Department - Graphic Design；BE-C013-P006 Iris Accounting Manager；BE-C013-P007 Vincent Key Account Manager Belgium & Luxemburg Consumer Brands | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 财务人事行政 | BE-C013-P001 Lieselotte Human Resources Officer | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 其他/未知 | BE-C013-P003 Sietse Product Manager Industrial；BE-C013-P004 Robin IT Support Medewerker；BE-C013-P010 Femke Planner；BE-C013-P011 Bedir Customer Contact Officer；BE-C013-P012 Ken Project Employee；BE-C013-P015 Mia Colorist；BE-C013-P016 Gerben Prevention Advisor；BE-C013-P018 Ann Planning Manager Mainland Europe；BE-C013-P019 Marc None；BE-C013-P020 Jan Continuous Improvement；BE-C013-P021 Kevin Team Lead；BE-C013-P022 Mario Colleague | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |

## 自动选择、名额与执行

第一组存在官网Frank经营管理及Ann规划管理/原料采购部门线索；Ann无邮箱、Frank无准入ID；Femke普通Planner缺少采购职责证据。不改选R&D/销售补数，固定付费0。

相关岗位候选4；原始has_email=true邮箱可用候选1；固定付费0。接收历史已选/已付费0；当前含本次正式公开复用累计0，未选公开线索不计名额；本次已明确联系对象2、其中拟新获取0、复验0。每公司3 credits：已耗0、预留0、未知0、剩余3；本次拟最高0 credits。本公司无收费范围；本批固定C0112/C0151已获真实批准并执行，不沿用旧批批准。

| 固定编号 | 人员ID | 姓名 | 原始职位 | 联系价值 | 职责/现职疑点 | has_email | 优先组 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 仅候选 | 54a5a1af7468692fa246aa9e | Ann Ge***s | Planning Manager Mainland Europe | Planning部门包含采购，但具体本人当前采购权未知 | 平台规划管理与历史职衔一致，原始has_email=false；未付费 | False | primary | 未调用，已公开/本次未选/范围限制见说明 |
| 仅候选 | 657c0bae348072000193d10a | Femke Da***s | Planner | 规划相关候选，不能只凭部门/同名岗位认本人采购职责 | Planner不自动等同采购；职责/品类未知，虽has_email=true仍不付费 | True | primary | 未调用，已公开/本次未选/范围限制见说明 |

相关4（Ann/Femke＋官方Frank/Tom），原始邮箱可用1，实际固定0。最终选Frank＋Ann作为共同转介目标，不选Tom补满。集团info公共入口不是他们个人邮箱；招聘apply及SDS rpmeurohas均不选业务To。

## 冲突、来源与更新

完整人员/职责与来源目录沿用MartinMathys背调。新Apollo三EU域Belgium22、父集团域职能补查2均已保存原始；只按国家/域名关联，未做收费公司匹配。历史Ann、法国机构、制造与备件采购限制不改变。

### 继承完整证据目录（原来源日期/范围）



| 证据ID | 支持事实／用途 | 发布者／标题 | 完整来源URL | 内容日期／版本／页码 | 访问日期 | 状态与限制 |
| --- | --- | --- | --- | --- | --- | --- |
| O01 | 涂料品牌及产品范围 | www.mathyspaints.eu（实际来源域名）／Decorative paints for indoor and outdoor use | [https://www.mathyspaints.eu/](https://www.mathyspaints.eu/) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O02 | VAT/地址及TomLowdon、FrankCostermans官方职衔 | www.mathyspaints.eu（实际来源域名）／Offices | [https://www.mathyspaints.eu/about/offices](https://www.mathyspaints.eu/about/offices) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O03 | 现售水性合成树脂墙面漆及资料入口 | www.mathyspaints.eu（实际来源域名）／PARACEM® DECO EASY FINISH XTRA MATT | [https://www.mathyspaints.eu/product/paracem-deco-easy-finish-xtra-matt](https://www.mathyspaints.eu/product/paracem-deco-easy-finish-xtra-matt) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O04 | 墙面漆用途、遮盖/耐擦洗要求及集团通用邮箱 | www.mathyspaints.eu（实际来源域名）／PARACEM® DECO EASY FINISH XTRA MATT | [https://www.mathyspaints.eu/static/datasheet_paracem_deco_easy_finish_xtra_matt_en.pdf](https://www.mathyspaints.eu/static/datasheet_paracem_deco_easy_finish_xtra_matt_en.pdf) | 06/02/2026；2页 | 2026-10-22 | 已读原文；不是客户采购规格或原料采购量 |
| O06 | 新版4.02：第3节限定披露；p20法规表有TiO₂词；不作原粉采购证明 | www.mathyspaints.eu（实际来源域名）／Mathys Paracem Deco Easy Finish Xtra Matt, EU-EN, 4,01, 21-05-2026 | [https://www.mathyspaints.eu/static/safetysheet_msds_paracem_deco_easy_finish_xtra_matt_en.pdf](https://www.mathyspaints.eu/static/safetysheet_msds_paracem_deco_easy_finish_xtra_matt_en.pdf) | 28/09/2026 v4.02；定向p3–5、20–22 of27 | 2026-10-22 | 已读原文；仅实际返回页段；未读全27页，不与May4.01混并 |
| O07 | 旧美版Noxyde技术PDF502；TiO₂仅摘要，当前具体业务用O04/O06替代 | www.rust-oleum.com（实际来源域名）／ACRYLIC ／ TECHNICAL DATA MM-01 MARTIN MATHYS NOXYDE (NOXYDE PLUS) --- ／ ---DESCRIPTION A single component, rust preventative water-based acrylic elastomeric coating. Noxyde Plus is the lead and chromate free version of Noxyde sold in the U.S. market. USES This self priming, high build coating is designed for minimally prepared sound rusted or clean steel in mild to moderate industrial environments. Two coats are required. It can also be used on concrete and the excellent elongation properties, 200%, makes it suitable for bridging small cracks. Noxyde is not recommended for exposure to most hydrocarbon solvents. ／ COMPATIBLE TOPCOATS A topcoat is optional. Noxyde has a light after tack, which can result in slight dirt accumulation. Topcoat if a higher fnial gloss is desired. 5200 System High Performance Acrylic 9800 System Urethane Mastic --- ／ --- DESCRIPTION None ／ COMPATIBLE TOPCOATS PACKAGING DESCRIPTION None ／ COMPATIBLE TOPCOATS 20 kg. pails DESCRIPTION None ／ COMPATIBLE TOPCOATS CONSUMPTION DESCRIPTION APPEARANCE ／ COMPATIBLE TOPCOATS One pail will cover approximately 470 sq. ft. @ 7 mils (175µ) dry flim thickness. DESCRIPTION Satin ／ COMPATIBLE TOPCOATS None DESCRIPTION None ／ COMPATIBLE TOPCOATS PRODUCT APPLICATION DESCRIPTION PRODUCTS ／ COMPATIBLE TOPCOATS None DESCRIPTION None ／ COMPATIBLE TOPCOATS SURFACE PREPARATION ALL SURFACES: Remove all dirt, grease, oil, salt or other contaminants by washing the surface with 3599 Industrial Pure Strength® Cleaner/Degreaser, detergent, or other suitable cleaner. Rinse thoroughly with fresh water and allow to fully dry. Thoroughly cured, hard or glossy previous coatings which are very smooth may require scuff sanding to maximize adhesion. Hand tool (SSPC-SP-2) or power tool (SSPC-SP-3) clean to remove loose rust, scale and deteriorated coatings to obtain a sound rusted surface. A rusted surface is considered to be sound when rust can no further be removed by scraping the surface by hand using a dull putty knife under moderate pressure. The surface may also be prepared by the use of High Pressure Water Jetting (HPWJ) in accordance to SSPC-SP-12/NACE 5 to a Visual Surface Preparation Condition of WJ-4. DESCRIPTION Item # Description 201630 Off White 201631 Blue Gray 201632 Beige Gray 201634 Reseda Green 201638 White 202541 Black 202770 English Red 210120 Brown ／ COMPATIBLE TOPCOATS None DESCRIPTION RECOMMENDED PRIMERS ／ COMPATIBLE TOPCOATS None DESCRIPTION Noxyde is self-priming when applied to minimally prepared rusted steel and aged galvanized steel. See PRIMING Section on page 2 for more information. Item # Description 3202504 3200 System Clear Blue Undercoat 202600 Pegalink ／ COMPATIBLE TOPCOATS NoneForm: 2900100 | [https://www.rust-oleum.com/tds/Noxyde_MM-01_2900100.pdf](https://www.rust-oleum.com/tds/Noxyde_MM-01_2900100.pdf) | 未标注 | 2026-10-22 | 尝试后受限；旧产品配方未原文核实，不转移为比利时采购 |
| G01 | 活跃SA、1989注册、同VAT及Halen地址 | Companyweb／Martin Mathys (SA) - Halen (3545) - BE0437896404 | [https://www.companyweb.be/en/0437896404/martin-mathys](https://www.companyweb.be/en/0437896404/martin-mathys) | 未标注 | 2026-10-22 | 已读原文；整理平台，不是本次KBO直接检索 |
| G02 | 品牌在RustOleumEurope专业/消费业务体系 | www.mathyspaints.eu（实际来源域名）／About Rust-Oleum Europe | [https://www.mathyspaints.eu/about/about-rust-oleum-europe](https://www.mathyspaints.eu/about/about-rust-oleum-europe) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G03 | 重读当前联系页TomLowdon/FrankCostermans及同VAT | RustOleumEurope／Contact | [https://www.rustoleum.eu/contact/](https://www.rustoleum.eu/contact/) | 未标注 | 2026-10-22 | 已读原文；搜索旧缓存AndrewWhite不作当前事实 |
| G04 | 集团/RPM关系、生产Zelem及Mathys官方回链 | RustOleumEurope／About us - English GB | [https://www.rust-oleum.eu/en-gb/about-us](https://www.rust-oleum.eu/en-gb/about-us) | 未标注 | 2026-10-22 | 已读原文；集团自述；规模不套用本公司 |
| G05 | 法国SIREN原页403；摘要法国机构inactive，与本案VAT主体活动范围分开 | 法国企业公开目录／Société MARTIN MATHYS NV (STE) - SIREN 403 010 481 ／ L’Annuaire des Entreprises | [https://annuaire-entreprises.data.gouv.fr/entreprise/martin-mathys-nv-ste-403010481](https://annuaire-entreprises.data.gouv.fr/entreprise/martin-mathys-nv-ste-403010481) | 未标注 | 2026-10-22 | 尝试后受限；不移植法国登记状态为比利时停业 |
| L01 | 官方链接之集团工业品牌页，同Zelem地址，人员名单 | LinkedIn／Rust-Oleum Industrial Europe ／ LinkedIn | [https://www.linkedin.com/company/rust-oleum-industrial-europe](https://www.linkedin.com/company/rust-oleum-industrial-europe) | 未标注 | 2026-10-22 | 已读原文；集团页，具体国家/职责未知 |
| L02 | Mathys域名/地址/业务匹配，员工姓名 | LinkedIn／Mathys Paints ／ LinkedIn | [https://be.linkedin.com/company/mathys-paints?trk=similar-pages](https://be.linkedin.com/company/mathys-paints?trk=similar-pages) | 未标注 | 2026-10-22 | 已读原文；品牌页，人数与1845年代不作法人信息 |
| L03 | 制造/集团自述、Halen岗位列表 | MartinMathys官方招聘／Homepage | [https://martinmathysnv.recruitee.com/](https://martinmathysnv.recruitee.com/) | 未标注 | 2026-10-22 | 已读原文；集团规模旧自述未采用 |
| L04 | Planning原料/包装/其他采购及国际供应商协调 | MartinMathys官方招聘／Rust-Oleum Europe - Martin Mathys n.v. - Aankoopmedewerker | [https://martinmathysnv.recruitee.com/o/aankoopmedewerker-3](https://martinmathysnv.recruitee.com/o/aankoopmedewerker-3) | 未标注 | 2026-10-22 | 已读原文；招聘职责不是具名现职/决策权限 |
| L05 | Halen生产环境维护与备件采购，与原料采购分开 | MartinMathys官方招聘／Rust-Oleum Europe - Martin Mathys n.v. - Onderhoudstechnieker | [https://martinmathysnv.recruitee.com/o/onderhoudstechnieker](https://martinmathysnv.recruitee.com/o/onderhoudstechnieker) | 未标注 | 2026-10-22 | 已读原文；A0070 begin误写/onderhoudstechnieker-3；真实参数click(turn340view0,8)及返回为本URL；旧事件保留 |
| L06 | AnnGerrits发帖PlanningManagerMainlandEurope及历史采购团队岗位 | LinkedIn招聘／Inkoopmedewerker at Martin Mathys N.V. — Halen, Flemish Region, Belgium ／ LinkedIn Jobs | [https://be.linkedin.com/jobs/view/inkoopmedewerker-at-martin-mathys-n-v-3898219037](https://be.linkedin.com/jobs/view/inkoopmedewerker-at-martin-mathys-n-v-3898219037) | 相对时间2年前，已停止申请 | 2026-10-22 | 已读原文；不证明2026完整现职 |
| L07 | 个人页999，历史岗位及官方当前部门替代 | LinkedIn／Ann Gerrits - Mathys Paints ／ LinkedIn | [https://be.linkedin.com/in/ann-gerrits-b7436016](https://be.linkedin.com/in/ann-gerrits-b7436016) | 未标注 | 2026-10-22 | 尝试后受限；当前完整职务未知 |
| D01 | 403，仅出口PAINT摘要；HTS与品名不一致 | Seair／Hagemeyer 904 south 20th USA Import & Buyer Data | [https://www.seair.co.in/us-importers/hagemeyer-904-south-20th.aspx](https://www.seair.co.in/us-importers/hagemeyer-904-south-20th.aspx) | 摘要2014-06-11 | 2026-10-22 | 尝试后受限；不是原粉进口或采购量 |
| D02 | 403，仅出口PAINTS摘要，原产国家字段未核 | Seair／Kiska construction USA Import & Buyer Data | [https://www.seair.co.in/us-importers/kiska-construction.aspx](https://www.seair.co.in/us-importers/kiska-construction.aspx) | 摘要2014-10-20 | 2026-10-22 | 尝试后受限；不是已核实交易，不能累计 |
| D03 | 同VAT/地址贸易目录，非海关样本 | Kompass／Martin Mathys - Halen 3545 (Hasselt), Kolenbergstraat 23 , REGISTRATIO | [https://gb.kompass.com/c/martin-mathys/be0016640/](https://gb.kompass.com/c/martin-mathys/be0016640/) | 未标注 | 2026-10-22 | 已读原文；进口区域仅索引，不能推TiO₂采购 |
| O05 | 首次实际返回May版4.01，仅供应方/识别及初段成分页；后续取得新版4.02分列O06 | www.mathyspaints.eu（实际来源域名）／Paracem SDS旧返回4.01 | [https://www.mathyspaints.eu/static/safetysheet_msds_paracem_deco_easy_finish_xtra_matt_en.pdf](https://www.mathyspaints.eu/static/safetysheet_msds_paracem_deco_easy_finish_xtra_matt_en.pdf) | 21/05/2026 v4.01；p1–4 of27 | 2026-10-22 | 已读原文；保留旧真实返回；不将新数据倒填旧版 |


新增原始返回与动作全部位于本批logs。初始主体/历史账本审核在_work/intake-audit.json；实际付费0/预留0/未知0。未写信、未发送。
