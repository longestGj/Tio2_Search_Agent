# Bartoline Ltd｜联系人工作邮箱

- 版本V1.0；日期2026-10-21（北京时间）。
- 客户ID：TIO2-GB-C36CD8CD4B；名单名Bartoline Ltd。
- 经确认官网：https://bartoline.co.uk/；本轮人员主域名bartoline.co.uk。
- 现经营主体：BARTOLINE INTERNATIONAL LIMITED（14468441）；与旧BARTOLINE LIMITED（00122306）分开。
- 关联背调：Bartoline_Ltd_背调报告_2026-10-21.md，2026-10-21读取。
- 关联组织文件：Bartoline_Ltd_组织结构_2026-10-21.md。
- 状态：已按用户“获取1，2”完成两人Enrichment；其余候选未获取，未发送邮件。

## 1. 固定候选名单

| 候选编号 | 台账编号 | Apollo显示姓名 | 原始职位 | has_email | 建议与限制 | Apollo人员ID |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P13 | Malgorzata Muller（原Malgorzata Mu***r） | Supply Chain Coordinator | true | 已获准并完成Enrichment；确认原料采购入口、采购主体与供应链归属；不等同TiO₂采购决策人。历史全名Malgorzata Muller，ID与背调一致。 | 67e05f089b09020001901598 |
| 2 | P03 | Alan Garrigan（原Alan Ga***n） | Head of Operations | true | 已获准并完成Enrichment；核实Beverley生产范围、目标SKU是否自产，并转介配方负责人；不直接认定拥有采购权。公开姓名线索Alan Garrigan。 | 66f57704d63893000126b785 |
| 3 | P02 | Paul Ra***e | Quality Lead | true | 备选：质量与来料测试入口；不是已确认的研发/配方负责人，采购权限未知。 | 681670715899150001f083e0 |
| 4 | P15 | Charles We***n | Production Manager | false | 备选：确认生产应用、工厂及产品线；has_email=false不证明没有邮箱。 | 686cda9dd1f59f0001fd292c |
| 5 | P16 | Fred Ch***s | Works Manager | false | 备选：工厂运营转介；Works Manager与Production Manager的分工、现职和邮箱均待核。 | 54a527f47468693442d66281 |

候选编号与ID固定。1、2号全名来自本次A04 Enrichment，原搜索遮挡值并列保留；其余姓名不猜补。

## 2. 已有地址及来源

| 对象 | 邮箱/渠道 | 来源 | 状态 |
| --- | --- | --- | --- |
| Malgorzata Muller（历史；与1号ID一致） | m.muller@bartoline.co.uk | S01转引H04历史Apollo enrichment | 历史verified，验证日期未知；本次A04另行返回相同地址及verified状态，见第3节；未测试投递 |
| Bartoline公共入口 | info@bartoline.co.uk | W06本轮读取；S01亦有官方技术文件依据 | 公开业务邮箱，非采购专用，未验证投递 |
| 官方电话 | +44 (0)1482 678710 | W02 | 可请求采购/技术转介，未拨打 |

历史个人链接：https://www.linkedin.com/in/malgorzata-muller-17196134b （H03，继承背调；本轮未读个人正文）。
Alan公开线索：https://uk.linkedin.com/in/alan-garrigan-607560a7 （W07，搜索摘要；直接读取429）。
以上历史/公开链接与A04返回来源分开保留；1、2号本次返回链接见第5节。其余候选LinkedIn地址未返回。

## 3. 本轮工作邮箱结果

获取日期2026-10-21；来源A04。按返回人员ID映射，两条公司/域名均与Bartoline目标相符。

| 编号/台账 | 姓名 | 原始职位 | 工作邮箱 | email_status | match_confidence | email_domain_catchall | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1/P13 | Malgorzata Muller | Supply Chain Coordinator | m.muller@bartoline.co.uk | verified | high | false | allow |
| 2/P03 | Alan Garrigan | Head of Operations | a.garrigan@bartoline.co.uk | verified | high | false | allow |

两人revealed_for_current_team=true；平台组织为Bartoline International Limited，organization_id=556994aa736964254f796000，primary_domain=bartoline.co.uk。
Malgorzata邮箱与历史记录一致，本次重新取得状态；Alan邮箱本轮新取得。verified是Apollo状态，非实际投递成功，不保证可达。
3、4、5号未授权、未调用，不能写成接口未返回；两人的职位和current标记也不等于独立现职核验。

## 4. 授权范围与实际费用

- 用户原文：“获取1，2”；日期2026-10-21。
- 候选1：67e05f089b09020001901598；候选2：66f57704d63893000126b785。仅传原搜索ID，未包含其他人。
- 调用apollo_people_bulk_match一次；reveal_personal_emails=false、reveal_phone_number=false。
- total_requested_enrichments=2；unique_enriched_records=2；missing_records=0；有邮箱2、无邮箱0、失败0；credits_consumed=2。
- request_id_str：5472287873868214062。
- 获取前余额2409 credits（A03快照），实际消耗2 credits；未重新查询剩余余额。
- 未获取个人邮箱或个人电话，未起草、未发送邮件。

## 5. 个人任职及组织证据

| 对象 | 本次返回 | 限制 |
| --- | --- | --- |
| Malgorzata Muller | Supply Chain Coordinator；headline为Supply Chain Coordinator at Bartoline International Limited；employment_history.current=true；组织名同现主体 | 未返回任职起始日期；个人地区只有United Kingdom，city/state未返回；不能补用公司Beverley地址作其个人所在地 |
| Alan Garrigan | Head of Operations；headline为Head of Operations at Bartoline International Limited；current履历title同上，start_date=2024-12-01，但organization_name= Bartoline Limited | 新旧公司名并存，不自行确定法律雇佣主体；开始日期为平台履历，未独立验证 |
| 组织及部门 | 两人organization_id相同；Malgorzata为master_operations/supply_chain、seniority=entry、functions=[]；Alan为master_operations/operations、seniority=head、functions=[operations] | 平台分类不等于实际部门设置或两人汇报关系 |

- 本次LinkedIn：Malgorzata http://www.linkedin.com/in/malgorzata-muller-17196134b ；Alan http://www.linkedin.com/in/alan-garrigan-607560a7 。链接由A04返回，未声称完整个人页已读取。
- Alan个人地区Beverley, England, United Kingdom，postal_code=HU17；两人time_zone=Europe/London。
- Alan历史平台任职：Head of Business Systems & Improvement（2023-02-01至2024-12-01）、Business Systems Manager（2020-02-01至2023-02-01）、Quality Manager（2010-01-01至2020-02-01），雇主使用BARTOLINE LIMITED；更早Hodgson Sealants Ltd Quality Manager（1986-09-01至2009-01-01）。不由历史质量经历直接认定其当前负责配方研发。
- 组织附带founded_year=1876反映业务历史，不能覆盖现法人2022成立；不据平台收入/人数估算采购量。

## 6. 各人疑点与沟通目的

| 编号 | 沟通价值 | 必须核实 |
| --- | --- | --- |
| 1 Malgorzata | 供应链协作及采购转介；已有历史记录 | 是否仍任职、TiO₂品类归属、Bartoline或Tetrosyl采购主体、审批人 |
| 2 Alan | 运营及制造归属；公开职位线索较吻合 | 现职、目标SKU是否自产、原料评估团队、技术负责人；不假定掌握采购审批 |
| 3 Paul | 来料/产品质量评价备选 | 是否负责目标配方质量、试样程序、是否可转介研发 |
| 4 Charles | 生产线和产品应用备选 | 哪个工厂/产品线、TiO₂原粉使用、与运营经理的实际分工 |
| 5 Fred | 工厂运营和负责人转介备选 | 现职及与Production Manager的分工；邮箱未知 |

公司背景仅有历史白色密封胶TiO₂线索，先确认现售、现配方、制造方和采购权；不据此推算年用量或推荐具体牌号。技术/研发负责人本轮未检出，不能将Quality Lead替代为研发负责人。
现主体为Bartoline International Limited；官网仍用旧名，须确认交易抬头。集团控制不等于集中采购。详细结构及23条全量人员见关联文件。

## 来源与完整网址

查询/读取日期：2026-10-21（北京时间）。继承背调信息不称本轮独立核验；网页抓取时间不代表内容更新日期。

| 编号 | 来源/完整网址 | 使用与限制 |
| --- | --- | --- |
| S01 | Bartoline_Ltd_背调报告_2026-10-21.md；libfile_31466e1bec38819181bfcb6f8f0f9a35 | 已读全文；客户ID、历史邮箱、TiO₂产品线索、旧主体与名单顺序 |
| S02 | 公司组织结构与联系人邮箱获取_SOP_V1.0.md；libfile_078cc28c38748191a0e67aa9719caa94；research-company-contacts技能及报告模板 | 当前执行标准 |
| A01 | Apollo People API Search；apollo_mixed_people_api_search；https://app.apollo.io/ | q_organization_domains_list=[bartoline.co.uk]；page=1、per_page=100；无职位/地区筛选；total=23，返回23 |
| A02 | 同上；https://app.apollo.io/ | q_organization_domains_list=[bartoline.net]；page=1、per_page=100；total=0，返回0；已反馈覆盖缺口 |
| A03 | Apollo Profile；apollo_users_api_profile；https://app.apollo.io/ | include_credit_usage=true；num_credits_remaining=2409；获取前快照 |
| A04 | Apollo Bulk People Enrichment；apollo_people_bulk_match；https://app.apollo.io/ | 2026-10-21；仅获准1、2号原搜索ID；请求5472287873868214062；请求2、匹配2、有邮箱2、缺失0、实际消耗2 credits；均verified、high、catchall=false、verdict=allow |
| W01 | https://bartoline.co.uk/about-us/ | 本轮直接读取；装修辅料制造、内部开发、贴牌/toll manufacturing；仍用旧名 |
| W02 | https://bartoline.co.uk/contact/ | 本轮直接读取；Beverley地址、电话，页面链接bartoline.net包装规范 |
| W03 | https://find-and-update.company-information.service.gov.uk/company/14468441 | 本轮直接读取；现主体名称、编号、Active、注册地址、2022成立及更名 |
| W04 | https://find-and-update.company-information.service.gov.uk/company/14468441/persons-with-significant-control | 本轮直接读取；Tetrosyl Group Limited（05204036）控制、日期及权利 |
| W05 | https://find-and-update.company-information.service.gov.uk/company/14468441/officers | 本轮读取登记页面；3位在任董事及历史离任；搜索服务缓存标记较旧，不能等同实时申报尽调 |
| W06 | https://uk.linkedin.com/company/bartoline-international-limited | 本轮直接读取；现公司名、域名、HU17 0LW、info邮箱及公开人员片段；51–200区间/41关联人员均非审计人数 |
| W07 | https://uk.linkedin.com/in/alan-garrigan-607560a7 | 本轮搜索摘要为Head of Operations at Bartoline International Limited，经历字段仍列Bartoline Limited；个人主页打开429，未读完整现职正文 |
| W08 | https://uk.linkedin.com/in/adamfeve | 本轮搜索摘要；headline为其他公司的resin layer，经历仍含Bartoline Production Operator；有冲突，不确认为当前员工 |
| W09 | https://www.surfex.co.uk/wp-content/uploads/sites/7/2019/04/SURF2002_Sales_Pack.pdf | 本轮搜索摘要有Bartoline Technical Manager/Operations Director历史岗位，未给姓名、未读取整份PDF；不用于现职确认 |
| W10 | https://bartoline.co.uk/wp-content/uploads/2018/08/BARTOLINE-Decorators-Caulk-380ml-Trade-MSDS-DC1-DOP.pdf | 搜索索引含Product Compliance Manager及2019-04-30；打开为2页但无可用文本，本轮未取得可核对的签名姓名，只作历史岗位线索 |
| H01 | https://find-and-update.company-information.service.gov.uk/company/00122306 | 继承背调：旧BARTOLINE LIMITED为In Administration，本轮未重查；不套用到现主体 |
| H02 | https://www.bartoline.co.uk/wp-content/uploads/2022/08/1876-Frame-Sealant-White-SDS-SEP22-Bartoline.pdf | 继承背调：2022版白色框架密封胶SDS列TiO₂ <5%；本轮未重读PDF，现售/现配方/自产待核 |
| H03 | https://www.linkedin.com/in/malgorzata-muller-17196134b | 继承背调的历史个人链接；背调访问失败，本轮未读全文 |
| H04 | agent05_handoff.csv；libfile_0804254daac48191ab7fe2fd2fa3751a | S01转引历史Malgorzata记录及verified邮箱；历史验证日期不明，本轮未重读CSV |
| H05 | https://iaaf.co.uk/tetrosyl-acquires-bartoline-international/ | 继承背调的2025收购报道；本轮集团关系以W04为依据 |

Apollo无可公开复现的单次搜索URL，记录工具名、参数和人员ID，不编造个人结果链接。

## 更新日志

- V0.1／2026-10-21：保存5位候选、历史Malgorzata邮箱、公共渠道与费用快照；等待选择后获取。
- V1.0／2026-10-21：按用户确认获取1、2号，匹配2人并取得2个工作邮箱，均verified且catchall=false；实际2 credits；保留Alan任职主体差异，未发送邮件。
