# BASIN CHEMECO｜组织结构

## 元信息

- 客户ID：BE-C012；公司BASIN CHEMECO；BE；首次2026-10-22；更新2026-10-22T19:25:00+08:00；批次BE-CONTACTS-20261022-02，执行者/root/be_contacts。
- Skill V1.5/local-batch v1.3，实际冻结指纹见checkpoint。company_key=BE:BE-C012；持久账本D:/02钛白粉外贸/markets/BE/companies/BE-C012/contacts/ledger.json。
- 官网https://basin.be/；主体依据：O02法律页明确SA、VAT0403102504及Gravestraat7A,8750Wingene，与G01登记整理原文一致；SA/NV为语言称呼，Basin-Chemie为已发现旧名；业务/地址/法人/制造分工原值见关联背调，不把集团数当本体。
- [关联背调](D:/02钛白粉外贸/markets/BE/companies/BE-C012/Basin_ChemEco_背调报告_2026-10-22.md)：2026-10-22读取，沿用当日原调查证据，不称本次重新核验。当前状态completed；组织调查完成不代表取得邮箱。
- [四项材料与本次收件组](D:/02钛白粉外贸/markets/BE/companies/BE-C012/Basin_ChemEco_联系人邮箱_2026-10-22.md#人员详情与交接开发信准备)。

## 公司主体及关系

| 主体/品牌/部门 | 注册号及地点 | 关系或职能 | 制造/采购线索 | 来源/状态 | 待核实 |
| --- | --- | --- | --- | --- | --- |
| Basin ChemEco SA/NV | BE0403102504，Gravestraat7A Wingene | 木材清漆/油/胶配方生产分销自述 | 采购岗位未检出 | 背调O02/G01/G02/G03 | CEO与董事是不同职能，旧名Basin-Chemie不拆公司 |
| 管理实体Peter Sergeant | 2025登记常任代表线索 | 法律管理关联，非独立采购人 | 不推采购权限 | 背调G02/G03 | 年报/现职分类与官网口径分开 |

## 检索日志及覆盖

| 接口 | 实际查询日期 | 完整参数/分页 | total/返回 | 原始证据 |
| --- | --- | --- | --- | --- |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:11:22+08:00 | {'_rationale': 'Research all indexed personnel for the confirmed company domain without title restrictions.', 'q_organization_domains_list': ['basin.be'], 'page': 1, 'per_page': 100} | 4/4 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-387d4f04b5e2.json |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:11:46+08:00 | {'_rationale': 'Check missing purchasing and operational management roles without changing the company scope.', 'q_organization_domains_list': ['basin.be'], 'person_titles': ['procurement', 'purchase', 'aankoop', 'buyer', 'CEO', 'chief operations', 'managing director', 'production', 'quality'], 'page': 1, 'per_page': 100} | 0/0 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-064fb2954db0.json |

实际返回4，按ID唯一4；检索人数不等于当前在职人数。首轮basin.be无职位过滤4/4已取完；采购、CEO/COO、制造及质量关键词补查0。官网研发/生产人员全量继承，不把未检出当公司无采购。针对Alain CEO现职口径有限公开检索，官网1.7年前发表的法律页/团队仍称CEO，登记索引仍列2025历史董事；没有独立确认目前运营岗位。

## 全量人员台账

搜索姓氏遮挡为接口预期，未收费揭示；已有公开来源全名另列，不猜补。原始更新时间含时区，未返回字段如实保留。

| 人员编号 | Apollo ID | 原始姓名 | 全名/来源 | 原始职位 | 公司/分支 | 地区 | 职能归类 | 归属/现职 | has_email | 原始更新时间 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C012-P001 | 5e8acd0b5b6eb60001b2a91a | Mark Po***r | Mark Portier（继承公司名单，职位平台） | Senior Sales Executive | Basin ChemEco nv | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-09T10:02:36.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-387d4f04b5e2.json |
| BE-C012-P002 | 5f587c98a867f20001300aed | Jemin Mo***n | 未揭示 | Reasearch | Basin ChemEco nv | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-09T19:33:31.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-387d4f04b5e2.json |
| BE-C012-P003 | 54c1c87f7468697af7e91c47 | Dominique De***t | Dominique Desmedt（继承官方Head of Research） | Head of R&D | Basin ChemEco nv | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-08-24T22:08:11.792+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-387d4f04b5e2.json |
| BE-C012-P004 | 5eaa912ab73a0d0001cd7b28 | Alain Go***n | Alain Goldstein（继承官网；当前CEO未独立确认） | Ingénieur Chimiste | Basin ChemEco nv | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台Ingénieur Chimiste；官网未标任期CEO与2025董事结束、年报在任口径并列；当前运营管理范围未独立确认，因此不付费 | True | 2026-08-24T22:10:35.497+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-387d4f04b5e2.json |

### 继承背调全部公开人员与职责线索

以下为原L节全量承接，原来源编号、公开邮箱归属/历史/异地/占位限制保留；不是本轮Apollo确认人数。与Apollo可能重叠，不能相加为员工数。



L01 LinkedIn公司页同域名、Wingene地址及木材配方业务匹配，1958为历史口径，PublicCompany标签不解释为上市。官网O03公开的姓名/职称完整保留，其部分简介是占位文字，职责、任期及汇报关系不能补全。L02 Jobs入口Timeout，两次有限尝试均失败；A0037/38/40岗位及官网替代检索没有得到可用Basin具体采购职位，已有官网研发/技术/生产角色来源已读。A0043点击Dominique返回同一团队页，不是独立个人详情。Pappers/Welipro管理人员原文一并交接，不把董事名等同原料采购权限。完整个人页归属及实际当前职责仍有限，未启动组织Agent或Apollo。 A0051 Pedro个人详情页返回999；已有G03年报董事与L01公司关联作替代，未证明完整现职。

| 姓名／部门 | 原始职称／归属／地区 | 现职及职责边界 | 来源 | 邮箱及验证 |
| --- | --- | --- | --- | --- |
| Alain Goldstein | 官网CEO；Basin，Wingene | 官方法律页与团队页自述；G02列历史董事，G03列年报董事，现职范围待确认 | O02/O03/G02/G03 | 未获取 |
| Peter Sergeant | 管理实体常任代表 | G02登记整理显示现任；不推定采购权 | G02/G03 | 未获取 |
| Pedro Vanhoe | G03列2025年报董事；L01员工名单 | 现职具体经营职责未知 | G03/L01 | 未获取 |
| Fatima Rejraji | 官网ChiefOperationsOfficer | 简介占位，缺任期及独立佐证 | O03 | 未获取 |
| Dominique Desmedt | Head of Research | 官网自述；完整职责/任期未标 | O03/A0043 | 未获取 |
| Philippe Legrand | Technical and sales advisor | 官网自述；权限未知 | O03 | 未获取 |
| Katrien Schoutteet | Accounting Assistant | 官网自述 | O03 | 未获取 |
| Benjamin Deboeuf | Logistiek supervisor | 官网自述 | O03 | 未获取 |
| Luc Rotte | Foreman | 官网自述 | O03 | 未获取 |
| Ramunas Kolaitis、Olexander Dobryanski | Production worker | 官网自述 | O03 | 未获取 |
| Mark Portier | LinkedIn员工列表（重复姓名去重1人） | 实际职务/现职未知 | L01 | 未获取 |
| 公司公共入口 | info@basin.be | 官网公开；非个人，不代表采购部门 | O02 | 官方公开，未验证投递 |


## 职能分布与管理线索

Apollo Alain Go***n原称Ingénieur Chimiste，与官网CEO并列，不据此断言晋升/降职或CEO离职。官网职位与CEO/董事不同口径不能互相代替；Peter法律常任代表不推经营/采购权，Pedro年报董事不是现任经营证明。团队Fatima COO简介占位，不能补职责或现职日期。Dominique官网Head of Research/ApolloHead of R&D一致，仍不因有邮箱跨组。无具名汇报证据。

| 职能 | 人员/原始职位 | 负责人/职责依据 | 汇报关系 | 缺口 |
| --- | --- | --- | --- | --- |
| 管理 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 采购供应链 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 研发技术 | BE-C012-P003 Dominique Head of R&D | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 生产运营 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 质量 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 仓储物流 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 销售渠道 | BE-C012-P001 Mark Senior Sales Executive | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 财务人事行政 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 其他/未知 | BE-C012-P002 Jemin Reasearch；BE-C012-P004 Alain Ingénieur Chimiste | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |

## 自动选择、名额与执行

第一组管理入口已有官网Alain CEO及登记Peter常任代表线索，可通过公司公共入口确认采购/管理团队；但Alain当前运营职位存在日期/原称限制，不为取邮箱就当现任CEO确定。本轮固定付费0；不因管理人未满足邮箱/现职准入改选研发/销售。

相关岗位候选3；原始has_email=true邮箱可用候选1；固定付费0。接收历史已选/已付费0；当前含本次正式公开复用累计0，未选公开线索不计名额；本次已明确联系对象2、其中拟新获取0、复验0。每公司3 credits：已耗0、预留0、未知0、剩余3；本次拟最高0 credits。本公司无收费范围；本批固定C0112/C0151已获真实批准并执行，不沿用旧批批准。

| 固定编号 | 人员ID | 姓名 | 原始职位 | 联系价值 | 职责/现职疑点 | has_email | 优先组 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 仅候选 | 5eaa912ab73a0d0001cd7b28 | Alain Go***n | Ingénieur Chimiste | 官网已刊CEO可作管理转介线索，岗位/现职不明不付费 | 平台Ingénieur Chimiste；官网未标任期CEO与2025董事结束、年报在任口径并列；当前运营管理范围未独立确认，因此不付费 | True | primary | 未调用，已公开/本次未选/范围限制见说明 |

相关3（Alain平台/官网、Peter登记管理、Fatima官网COO占位），Apollo邮箱可用1，但固定0；邮箱可用不替代角色/现职准入。选定通过公开info联系管理/采购职能，不把董事/CEO矛盾当公司排除，也不向技术销售补邮箱。

## 冲突、来源与更新

主体/全部官方团队、占位简介、Alain/Peter/Pedro分类差异承接原背调O/G/L与完整目录。新增BE2-387d4f04b5e2完整4人、BE2-064fb2954db0职能缺口0。有限CEO公开搜索只采用官网现刊及登记索引的口径边界；完整原文已在上游读取，本轮搜索不是重新认证管理权。无收费。

### 继承完整证据目录（原来源日期/范围）



| 证据ID | 支持事实／用途 | 发布者／标题 | 完整来源URL | 内容日期／版本／页码 | 访问日期 | 状态与限制 |
| --- | --- | --- | --- | --- | --- | --- |
| O01 | 主营木材涂层和胶黏剂；比利时生产自述 | basin.be（实际来源域名）／Produits pour Bois Intérieur & Extérieur ／ Basin ChemEco | [https://basin.be/](https://basin.be/) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O02 | SA名称、VAT、地址及公共info；CEO自述 | basin.be（实际来源域名）／Mentions légales - Basin ChemEco | [https://basin.be/mentions-legales/](https://basin.be/mentions-legales/) | 未标注 | 2026-10-22 | 已读原文；官网未标内容日期，人员现职有G差异 |
| O03 | 历史、制造自述及团队姓名/职称；部分简介占位 | basin.be（实际来源域名）／Produits pour bois – L’histoire de Basin, fabricant belge depuis 1958 | [https://basin.be/a-propos/](https://basin.be/a-propos/) | 未标注 | 2026-10-22 | 已读原文；企业自述；占位文字不作职责或现职确认 |
| O04 | NO VISIBLE OIL HPU5001单组分木材混合清漆 | basin.be（实际来源域名）／NO VISIBLE OIL1K | [https://basin.be/wp-content/uploads/2025/11/TF_HPU-5001_EN-1.pdf](https://basin.be/wp-content/uploads/2025/11/TF_HPU-5001_EN-1.pdf) | March2024 FT HPU001V002 EN；p1/2/4 of5 | 2026-10-22 | 已读原文；不含完整成分，未证明采购TiO₂；使用口径有差异不做技术定型 |
| O05 | 实际产品链接redirect/不可达，用具体TDS替代 | basin.be（实际来源域名）／来源 | [https://basin.be/produit/neutralator-2/](https://basin.be/produit/neutralator-2/) | 未标注 | 2026-10-22 | 尝试后受限；自述/平台材料不等于独立证明全部事实 |
| G01 | 活跃SA，同VAT/地址及1968注册 | Companyweb／Basin ChemEco (SA) - Wingene (8750) - BE0403102504 | [https://www.companyweb.be/en/0403102504/basin-chem-eco](https://www.companyweb.be/en/0403102504/basin-chem-eco) | 未标注 | 2026-10-22 | 已读原文；登记整理平台非本次官方直接查询 |
| G02 | 登记整理人员现/历史分类，Peter管理实体现任、Alain历史 | Pappers／Basin ChemEco (0403.102.504) : Chiffre d'affaires & dirigeants | [https://www.pappers.be/fr/company/basin-chemeco-0403102504](https://www.pappers.be/fr/company/basin-chemeco-0403102504) | 页面BCE更新2026-10-01 | 2026-10-22 | 已读原文；CEO与董事不同；与G03口径差异保留，不认定权限 |
| G03 | 旧名及地址、2025年报董事Alain/Pedro/Peter实体；近两年亏损 | Welipro／Basin ChemEco: jaarrekening, gezondheid, btw 0403.102.504 | [https://be.welipro.com/nl/bedrijf/basin-chemeco-29625431](https://be.welipro.com/nl/bedrijf/basin-chemeco-29625431) | 页面更新2026-10-20；2025年报口径 | 2026-10-22 | 已读原文；非原始年报本次审计；不采用评分/信用限额，不推股权 |
| L01 | 域名/地址/业务、Pedro/Mark姓名线索 | LinkedIn／Basin ChemEco nv ／ LinkedIn | [https://be.linkedin.com/company/basinchemeco](https://be.linkedin.com/company/basinchemeco) | 未标注 | 2026-10-22 | 已读原文；11–50为平台自述，不采用为当前精确规模 |
| L02 | Jobs实际入口两次Timeout，官网公开人员及岗位检索作有限替代 | basin.be（实际来源域名）／来源 | [https://basin.be/?page_id=19](https://basin.be/?page_id=19) | 未标注 | 2026-10-22 | 尝试后受限；未得到具体招聘正文，不宣称无采购部门 |
| D01 | 同VAT贸易目录，非交易；1959口径不替代注册日 | Kompass／Basin Chemeco - Primers to Wingene, Belgium ／ Kompass | [https://gb.kompass.com/c/basin-chemeco/be0334531/](https://gb.kompass.com/c/basin-chemeco/be0334531/) | 未标注 | 2026-10-22 | 已读原文；不采用其旧规模/年代为当前事实 |
| D02 | 402；摘要成品/色浆Belgium→Turkey，汇总及方向口径不同 | Eximpedia／Basin Chemeco Nv Import Export Data & Shipment Details | [https://www.eximpedia.app/companies/basin-chemeco-nv/19780462](https://www.eximpedia.app/companies/basin-chemeco-nv/19780462) | 未标注 | 2026-10-22 | 尝试后受限；仅摘要；日期/地址/提单/单位及双方不可核，不作原粉采购 |
| D03 | 供应商颜料浆页面Timeout；摘要1笔 | Volza／Pigment Pastes Suppliers from Belgium - Volza | [https://www.volza.com/p/pigment-pastes/manufacturers/manufacturers-in-belgium/](https://www.volza.com/p/pigment-pastes/manufacturers/manufacturers-in-belgium/) | 未标注 | 2026-10-22 | 尝试后受限；非原粉采购，公开覆盖/期间未知 |
| L03 | Pedro个人页999，年报董事与公司页替代；完整职责未知 | LinkedIn／来源 | [https://be.linkedin.com/in/pedrovanhoe?trk=org-employees](https://be.linkedin.com/in/pedrovanhoe?trk=org-employees) | 未标注 | 2026-10-22 | 尝试后受限；自述/平台材料不等于独立证明全部事实 |


新增原始返回与动作全部位于本批logs。初始主体/历史账本审核在_work/intake-audit.json；实际付费0/预留0/未知0。未写信、未发送。
