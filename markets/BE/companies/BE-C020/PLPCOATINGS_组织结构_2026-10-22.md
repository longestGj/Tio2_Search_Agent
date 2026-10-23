# PLPCOATINGS｜组织结构

## 元信息

- 客户ID：BE-C020；公司PLPCOATINGS；BE；首次2026-10-22；更新2026-10-22T19:25:00+08:00；批次BE-CONTACTS-20261022-02，执行者/root/be_contacts。
- Skill V1.5/local-batch v1.3，实际冻结指纹见checkpoint。company_key=BE:BE-C020；持久账本D:/02钛白粉外贸/markets/BE/companies/BE-C020/contacts/ledger.json。
- 官网https://plpcoatings.com/fr/；主体依据：G01/G05现PPC BE0478442602同Havenlaan8，G04 UBAtc/BCCA ATG2560p1直接列ProfessionalPaintCompanybv/同址电话/plpcoatings.com；G02/G03另销售法人0820950194独立保留；业务/地址/法人/制造分工原值见关联背调，不把集团数当本体。
- [关联背调](D:/02钛白粉外贸/markets/BE/companies/BE-C020/PLPCOATINGS_背调报告_2026-10-22.md)：2026-10-22读取，沿用当日原调查证据，不称本次重新核验。当前状态completed；组织调查完成不代表取得邮箱。
- [四项材料与本次收件组](D:/02钛白粉外贸/markets/BE/companies/BE-C020/PLPCOATINGS_联系人邮箱_2026-10-22.md#人员详情与交接开发信准备)。

## 公司主体及关系

| 主体/品牌/部门 | 注册号及地点 | 关系或职能 | 制造/采购线索 | 来源/状态 | 待核实 |
| --- | --- | --- | --- | --- | --- |
| PPC/Professional Paint Company | BE0478442602；Havenlaan8 Tessenderlo-Ham | 本ID制造主体，历史PaulyPaint名 | ATG2560直接列官网/同址，本体生产检验线索 | 背调G01/G04/G05 | 旧称/法律形式差异保留 |
| PLP销售法人 | BE0820950194，同址共享plpcoatings.com品牌 | 独立销售主体 | 不合并制造VAT或账本 | 背调G02/G03 | Apollo只给品牌雇主，不揭法律实体 |
| 海外区域销售网络 | NL/FR/PL/UKIE/IT | 品牌网络 | 不当BE制造采购 | 官网公共邮箱区域 | 地点/雇主未确认者分列 |

## 检索日志及覆盖

| 接口 | 实际查询日期 | 完整参数/分页 | total/返回 | 原始证据 |
| --- | --- | --- | --- | --- |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:22:41+08:00 | {'_rationale': 'Read-only staff and role investigation; legal manufacturer and shared-brand seller remain distinct', 'q_organization_domains_list': ['plpcoatings.com'], 'page': 1, 'per_page': 100} | 24/24 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| mcp__codex_apps__apollo_io_apollo_mixed_people_api_search | 2026-10-22T19:22:55+08:00 | {'_rationale': 'Read-only purchasing and legal-management gap check within shared brand', 'q_organization_domains_list': ['plpcoatings.com'], 'person_titles': ['purchaser', 'procurement', 'purchasing', 'CEO', 'managing director', 'owner', 'general manager'], 'include_similar_titles': True, 'page': 1, 'per_page': 100} | 2/2 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-6cb366612b8a.json |

实际返回26，按ID唯一24；检索人数不等于当前在职人数。共享品牌域无岗位/无国家过滤首轮24/24；采购管理补查2条重复，总26/唯一24。对Sandra Owner与Liesbeth Purchaser作必要公开核对：搜索摘要可见关联但个人页实际失败999/InternalError；限制原样记录，未称个人页已读。无别地本体猜配，无付费公司查询。

## 全量人员台账

搜索姓氏遮挡为接口预期，未收费揭示；已有公开来源全名另列，不猜补。原始更新时间含时区，未返回字段如实保留。

| 人员编号 | Apollo ID | 原始姓名 | 全名/来源 | 原始职位 | 公司/分支 | 地区 | 职能归类 | 归属/现职 | has_email | 原始更新时间 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-C020-P001 | 54a13a2169702d1e3f1c9300 | Sandra Ca***a | Sandra Cavicchia（继承官方职业公司页姓名；Owner职责范围未确认） | Owner | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 管理 | Owner true但具体哪个企业拥有权未知；本人第三方转引摘要有个人附件网店Owner，不能确认PPCOwner | True | 2026-10-15T04:31:56.900+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P002 | 60c34c3d1e483200011f8ffe | Ines Me***s | 未揭示 | Human Resources Officer | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-10T16:05:30.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P003 | 54a53f6c7468693b8c830489 | Annick Dr***s | Annick Dries（继承公司页姓名） | Administrative Employee | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-02T12:38:54.928+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P004 | 59fa332da6da98a941e55eba | Yves Kn***n | 未揭示 | Sales Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-07T15:24:52.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P005 | 54a47c7e74686938ac46bd4b | Lenny Pi***i | 未揭示 | Laborant, Colorist | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-08T09:56:55.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P006 | 54a4038e7468693209a79b25 | Jorg Ge***s | 未揭示 | Production Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 生产运营 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-09T10:02:52.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P007 | 54a26a4d7468693fdad05321 | Ihsan Oz***r | 未揭示 | SHE / ERP Coordinator | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-05T12:01:51.331+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P008 | 6002e6bd3fac0c0001ba3091 | Christophe Sc***s | 未揭示 | Commercial Director Benelux-Export | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-01T16:33:39.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P009 | 5570ad6373696418d8e74900 | Ronny St***s | Ronny Stans（继承公司页姓名） | Veiligheidsadviseur ADR | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-07T14:11:11.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P010 | 57e07006a6da981c29dbbc1e | Izabela Ku***k | 未揭示 | Office Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-15T15:11:23.485+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P011 | 54aa820474686908c84f0008 | Bas Br***s | Bas Brons（继承公司页姓名） | Commercial Technical Advisor | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | False | 2026-10-05T10:14:03.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P012 | 65d2987852b6c000019821c7 | Anne Gy***s | 未揭示 | Human Resources Officer | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | Anne Gy***s HR true；原招聘邮箱仍未核实完整持有人，不从字符串推身份 | True | 2026-10-07T10:01:32.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P013 | 5f4ef18e649a1300011da4fb | Dominiek Re***s | 未揭示 | Laboratory Assistant | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-09T13:06:11.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P014 | 671c992caca4d00001616a00 | Dawid Ol***k | 未揭示 | Technical Proces Menager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-10-04T20:55:27.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P015 | 65353c470c9406000112f638 | Guy D'***s | 未揭示 | R&D Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-12T14:23:48.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P016 | 563adb4ca6da9870880014b2 | Jo Va***l | 未揭示 | 未返回 | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | True | 2026-05-03T09:56:23.017+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P017 | 54a3ae047468692fa2f6200a | Agnieszka Pi***a | 未揭示 | Administrative Asissant | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-07T11:56:51.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P018 | 5e7715872f14bd000185b675 | Karen Je***x | 未揭示 | HR Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | False | 2026-10-04T22:01:22.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P019 | 63229afd5b092700019bb0d6 | Magdalena Pa***a | 未揭示 | Administrative Assistant | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 财务人事行政 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-19T03:42:03.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P020 | 60ce235b1d75920001b4872c | Julien Ma***x | 未揭示 | ... | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-08T13:22:48.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P021 | 54a8e8be7468692d1c0f5e08 | Marc Va***s | 未揭示 | Laborer | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 研发技术 | 平台组织关联/现职线索，非独立核验 | True | 2026-09-03T19:32:52.819+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P022 | 6467730ff0e9f800017ca4f2 | Dirk He***t | 未揭示 | Marketing Manager | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 销售渠道 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-08T11:28:07.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P023 | 57d6c186a6da98546250da29 | Liesbeth Ge***n | Liesbeth Geenen（本轮搜索摘要，原个人页999） | Purchaser | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 采购供应链 | Purchaser false；共享品牌采购职称，不等于已核实制造PPC雇员/原料采购权 | False | 2026-10-04T15:42:57.353+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |
| BE-C020-P024 | 68ef8a25d251b4000116688d | Robby Du***t | 未揭示 | Worker | PLP COATINGS | 未返回，has_city/country仅可用性标志 | 其他/未知 | 平台组织关联/现职线索，非独立核验 | False | 2026-09-07T07:09:57.000+00:00 | D:/02钛白粉外贸/markets/BE/contacts/BE-CONTACTS-20261022-02/logs/evidence/BE2-19a8fe92bad6.json |

### 继承背调全部公开人员与职责线索

以下为原L节全量承接，原来源编号、公开邮箱归属/历史/异地/占位限制保留；不是本轮Apollo确认人数。与Apollo可能重叠，不能相加为员工数。



L01匹配TessenderloHavenlaan8和plpcoatings.com，员工名单SandraCavicchia/BasBrons/AnnickDries/RonnyStans只有名单/雇主自述，无现职权限。L02实际当前Havenlaan8 AssistantLaboratoryTechnician岗位做原料/半成品/成品质检、颜色/遮盖/黏度、色彩配方协同；ProductionWorker混合原料并灌装，AdministrativeAssistant给采购和销售部门下单追单/供应商发票/库存。这些是岗位职责与招聘，不是已有具名任职或原料决策权。Anne.Gybels@plpcoatings.com公开为三个岗位投递地址，网页未另写全名与其职位，A0281针对全名+公司未取得可确认个人页，不从邮箱猜现职。G05确认Philip/Herman管理代表，2014BBT摘要PhilipCEO/JoVanDaalSeniorChemist只作历史未采用线索，当前技术部门由L02覆盖；不为读尽旧人员材料扩大。其他LinkedIn搜索人名当前只显示PLP关联/活动，没有岗位原文，不代替contacts独立组织调查。

| 人员/部门 | 已取得职务事实 | 归属/现职边界 | 来源 | 邮箱/状态 |
| --- | --- | --- | --- | --- |
| Philip Jennen | Insieme永久代表执行PPC董事职能 | G05当前；不把旧本人董事离职当全部离职，原料权限未知 | G05 | 未获取 |
| Herman Jennen | D&S永久代表 | G05当前管理关联；原料权限未知 | G05 | 未获取 |
| Anne.Gybels地址标识 | 招聘收件入口 | 页面未独立署个人全名/职位；不能由邮箱拼出事实性身份 | L01/L02 | anne.gybels@plpcoatings.com，大小写去重1，公开未验证；姓名/部门归属待核 |
| SandraCavicchia/BasBrons/AnnickDries/RonnyStans | LinkedIn员工名单 | 具体职责/现职未知 | L01 | 未获取 |
| DominiekReynders/YvesKnaepen/IhsanOzdemir/DirkHeyvaert/ChristopheSchoenmaeckers/DawidOlejniczak | 搜索返回PLP关联人员 | 仅摘要及活动，不当当前BE原料岗位；波兰地区不转本地 | A0253原始返回/来源处理表未采用线索 | 未获取 |
| 实验室/生产/采购行政 | 真实招聘职责 | 公开岗位，不是现职具名人 | L02 | career@plpcoatings.com公共招聘邮箱 |
| 公司及网络公共入口 | BE/info/sales与国外网络 | 下表列明地域，不自动变成本地采购入口 | O01/O03/L01/L02 | 见下段9公共地址 |


## 职能分布与管理线索

PhilipJennen与HermanJennen按当前PPC管理实体永久代表登记保留，不沿2014CEO称号当现职。Liesbeth Ge***n Purchaser false，为品牌采购转介线索，搜索摘要LiesbethGeenen Tessenderlo关联但个人页999，法律雇主/原料品类未知。SandraCa***a Owner true虽然官网职业集团页姓名关联，但本人转引搜索摘要说PLP日常工作外另有forty7accessories店主，不据ApolloOwner判PPC所有者；实际页失败，仅作冲突线索不付费。AnneGy***s HR true仍不足将原未归属anne.gybels地址确认给她，保留未归属与HR线索分开，不能由邮箱拼名。

| 职能 | 人员/原始职位 | 负责人/职责依据 | 汇报关系 | 缺口 |
| --- | --- | --- | --- | --- |
| 管理 | BE-C020-P001 Sandra Owner | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 采购供应链 | BE-C020-P023 Liesbeth Purchaser | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 研发技术 | BE-C020-P005 Lenny Laborant, Colorist；BE-C020-P011 Bas Commercial Technical Advisor；BE-C020-P013 Dominiek Laboratory Assistant；BE-C020-P014 Dawid Technical Proces Menager；BE-C020-P015 Guy R&D Manager；BE-C020-P021 Marc Laborer | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 生产运营 | BE-C020-P006 Jorg Production Manager | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 质量 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 仓储物流 | 本次Apollo未检出；继承官方线索见上文 | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 销售渠道 | BE-C020-P004 Yves Sales Manager；BE-C020-P008 Christophe Commercial Director Benelux-Export；BE-C020-P022 Dirk Marketing Manager | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 财务人事行政 | BE-C020-P002 Ines Human Resources Officer；BE-C020-P003 Annick Administrative Employee；BE-C020-P012 Anne Human Resources Officer；BE-C020-P017 Agnieszka Administrative Asissant；BE-C020-P018 Karen HR Manager；BE-C020-P019 Magdalena Administrative Assistant | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |
| 其他/未知 | BE-C020-P007 Ihsan SHE / ERP Coordinator；BE-C020-P009 Ronny Veiligheidsadviseur ADR；BE-C020-P010 Izabela Office Manager；BE-C020-P016 Jo None；BE-C020-P020 Julien ...；BE-C020-P024 Robby Worker | 仅按原职位分析标签，非官方部门设置 | 未核实，明确例外见本节说明 | 不代表公司无该部门 |

## 自动选择、名额与执行

当前PPC法律管理入口与品牌Purchaser均存在；Liesbeth false不enrich，Philip未检出ID。Sandra true的Owner作用域有冲突且法律雇主未知，不按邮箱准入代替岗位核对；固定0，不跨组选研发/销售/HR。

相关岗位候选3；原始has_email=true邮箱可用候选0；固定付费0。接收历史已选/已付费0；当前含本次正式公开复用累计0，未选公开线索不计名额；本次已明确联系对象2、其中拟新获取0、复验0。每公司3 credits：已耗0、预留0、未知0、剩余3；本次拟最高0 credits。本公司无收费范围；本批固定C0112/C0151已获真实批准并执行，不沿用旧批批准。

| 固定编号 | 人员ID | 姓名 | 原始职位 | 联系价值 | 职责/现职疑点 | has_email | 优先组 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 仅候选 | 57d6c186a6da98546250da29 | Liesbeth Ge***n | Purchaser | 采购职称可作转介对象，但无邮箱且具体本体/品类未知 | Purchaser false；共享品牌采购职称，不等于已核实制造PPC雇员/原料采购权 | False | primary | 未调用，已公开/本次未选/范围限制见说明 |

相关3（Liesbeth、Philip/Herman法律管理），邮箱可用0、固定0；本次只选Philip管理+Liesbeth品牌采购2个转介目标。To采用info@plpcoatings.com官方公共总入口，明确请求PPC制造主体原料采购转介，不扩加各国外销/招聘邮箱。

## 冲突、来源与更新

新增24条品牌人员全部保留，不假定同一法人/BE雇主。SandraOwner疑点是受限搜索摘要线索，未强认冲突结论。原anne地址仍未归属；本轮AnneGy***s HR线索并不揭全名/邮箱。所有上游VAT/ATG内部旧称差异照录，未改上游。

### 继承完整证据目录（原来源日期/范围）



| 证据ID | 支持事实／用途 | 发布者／标题 | 完整来源URL | 内容日期／版本／页码 | 访问日期 | 状态与限制 |
| --- | --- | --- | --- | --- | --- | --- |
| O01 | 产品/代工研发及Havenlaan8、国家网络公共邮箱 | plpcoatings.com（实际来源域名）／PLPCOATINGS - Quality for professionals | [https://plpcoatings.com/fr/](https://plpcoatings.com/fr/) | 未标注 | 2026-10-22 | 已读原文；A0255Contact链接返回首页，A0287后部实际读取；不是专门contact详情 |
| O02 | 1969品牌起点/家族经营自述 | plpcoatings.com（实际来源域名）／Qui sommes-nous - PLPCOATINGS | [https://plpcoatings.com/fr/qui-sommes-nous/](https://plpcoatings.com/fr/qui-sommes-nous/) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O03 | 具体双组分PU高光面漆及ventes公共销售入口 | plpcoatings.com（实际来源域名）／P-THANE FINISH 1200: 2C I Finition I Polyuréthane I Haute brillance - PLPCOATINGS | [https://plpcoatings.com/fr/p-thane-finish-1200-2c-i-finition-i-polyurethane-i-haute-brillance/](https://plpcoatings.com/fr/p-thane-finish-1200-2c-i-finition-i-polyurethane-i-haute-brillance/) | 2022-06-23 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O04 | 真实跳客户登录，无TDS正文；替代公开O05及G04 | plpcoatings.com（实际来源域名）／Accès client - PLPCOATINGS | [https://plpcoatings.com/fr/fiches-techniques/](https://plpcoatings.com/fr/fiches-techniques/) | 未标注 | 2026-10-22 | 尝试后受限；原返回带动态登录参数，不含用户凭据；报告用原技术入口定位 |
| O05 | 改性PVB防腐附着底漆/颜料磷酸锌与填料/同址电话域名 | www.plpcoatings.com（实际来源域名）／Microsoft Word - AGROPRIM E | [https://www.plpcoatings.com/wp-content/uploads/2017/04/AGROPRIM-E.pdf](https://www.plpcoatings.com/wp-content/uploads/2017/04/AGROPRIM-E.pdf) | 02/2017；3页 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| O06 | 招聘总述及公共career，英文详细岗位另L02 | plpcoatings.com（实际来源域名）／Offres d’emplois - PLPCOATINGS | [https://plpcoatings.com/fr/offres-demplois/](https://plpcoatings.com/fr/offres-demplois/) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G01 | PPC活跃制造主体/VAT0478442602/同地址；自动财务预警不作排除 | www.firmo.be（实际来源域名）／PROFESSIONAL PAINT COMPANY (SRL) · Tessenderlo-Ham · BE0478442602 | [https://www.firmo.be/en/0478442602/professional-paint-company](https://www.firmo.be/en/0478442602/professional-paint-company) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G02 | 同址销售PLP另一VAT0820950194，独立保留 | www.companyweb.be（实际来源域名）／Plp Coatings (BV) - Tessenderlo-Ham (3980) - BE0820950194 | [https://www.companyweb.be/nl/0820950194/plp-coatings](https://www.companyweb.be/nl/0820950194/plp-coatings) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G03 | PLP销售主体LEI/0820号，不属于PPC | lei.bloomberg.com（实际来源域名）／PLP coatings - LEI: 967600LHLOZRMILOCL04 | [https://lei.bloomberg.com/leis/view/967600LHLOZRMILOCL04](https://lei.bloomberg.com/leis/view/967600LHLOZRMILOCL04) | 未标注 | 2026-10-22 | 已读原文；nextrenew2025-12-06，不能称本次已续期/代PPC |
| G04 | PPC批准持有人官网同址电话、制造销售分别说明 | api.butgb-ubatc.be（实际来源域名）／Agrément Technique ATG avec Certification | [https://api.butgb-ubatc.be/api/public/file/ATG2560F.pdf](https://api.butgb-ubatc.be/api/public/file/ATG2560F.pdf) | ATG2560/2022-09-06–2027-09-05；p1–3部分 | 2026-10-22 | 已读原文；p2仍旧PaulySA及PLPbvba，不擅自改原文；未审全7页 |
| G05 | PPC同VAT/活跃机构/Philip和Herman现管理代表，旧任期区分 | www.pappers.be（实际来源域名）／PROFESSIONAL PAINT COMPANY (0478.442.602) : Omzet & bestuurders | [https://www.pappers.be/nl/company/professional-paint-company-0478442602](https://www.pappers.be/nl/company/professional-paint-company-0478442602) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G06 | 同PPC/旧LEI Paulypaint名称及2010吸收旧Pauly线索 | b2bhint.com（实际来源域名）／PPC - 0478.442.602 - België | [https://b2bhint.com/nl/company/be/ppc--0478.442.602](https://b2bhint.com/nl/company/be/ppc--0478.442.602) | 未标注 | 2026-10-22 | 已读原文；平台VAT否有差异不作税务有效性结论；历史沿革非完整法律审计 |
| G07 | 波兰扩厂计划预计2022，非本次当地运营证明 | plpcoatings.com（实际来源域名）／LE NOUVEAU SITE DE PRODUCTION A WROCLAW EN POLOGNE - PLPCOATINGS | [https://plpcoatings.com/fr/le-nouveau-site-de-production-a-wroclaw-en-pologne/](https://plpcoatings.com/fr/le-nouveau-site-de-production-a-wroclaw-en-pologne/) | 2021-09-21 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G08 | 官网同址电话品牌，无VAT；失败法语路径的实质替代 | plpcoatings.com（实际来源域名）／Privacy Disclaimer - PLPCOATINGS | [https://plpcoatings.com/en/privacy-disclaimer-en/](https://plpcoatings.com/en/privacy-disclaimer-en/) | v2.0/2018-05-24 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| G09 | 400 Timeout；英文G08替代，身份由G04认证落实 | plpcoatings.com（实际来源域名）／来源 | [https://plpcoatings.com/privacy-disclaimer/](https://plpcoatings.com/privacy-disclaimer/) | 未标注 | 2026-10-22 | 尝试后受限；自述/平台材料不等于独立证明全部事实 |
| L01 | 同址域名企业、招聘邮箱、公共sales及员工列表 | be.linkedin.com（实际来源域名）／PLP COATINGS ／ LinkedIn | [https://be.linkedin.com/company/plpcoatings](https://be.linkedin.com/company/plpcoatings) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| L02 | 三个当前岗位全文职责/Anne地址标识/采购支持及原料配方质检 | plpcoatings.com（实际来源域名）／Jobs - PLPCOATINGS | [https://plpcoatings.com/en/jobs/](https://plpcoatings.com/en/jobs/) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| D01 | 具体同址PLP出口样本SHPT17418636/5477kg/9PKG | www.importgenius.cn（实际来源域名）／Aikg, Llc ／ 获取完整的进口商历史记录 ／ 进口数据库 | [https://www.importgenius.cn/importers/aikg-llc](https://www.importgenius.cn/importers/aikg-llc) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |
| D02 | 销售方同样本主体页，去重不转PPC交易 | www.importgenius.cn（实际来源域名）／Plp Coatings Bv ／ 搜索近期的海运记录 ／ 进口数据库 | [https://www.importgenius.cn/suppliers/plp-coatings-bv](https://www.importgenius.cn/suppliers/plp-coatings-bv) | 未标注 | 2026-10-22 | 已读原文；自述/平台材料不等于独立证明全部事实 |


新增原始返回与动作全部位于本批logs。初始主体/历史账本审核在_work/intake-audit.json；实际付费0/预留0/未知0。未写信、未发送。
