# Fontenova del Perú SAC｜秘鲁｜商业背景调查

- 客户ID：PE-C049；lead_id：PE-L054。
- 调查日期／资料截止：2026-10-22；执行者：customer_research（/root/peru_customer_three）。
- 目的：主动开发公开背景核查；模式new，无同主体旧背调。标准OGLD SOP V1.1＋local-batch v1.1＋objective-evidence-v1具体动作规范v1.1；原Skill来源commit aa99ddf7583dee0cd7b6e8a472aa7b65aa802634，本地当前规范。
- 输入：PE-20261022-02正式01总表第100行；复用PE-20261021-02 research-data.json的PE2-E029为发现线索，未将旧资料冒充本次联网。原始返回均保存在本批logs/evidence。
- 本次11次搜索、37次页面读取；未付费、未Apollo、未获取非公开邮箱、未联系。

## 经确认的公司官网

| 字段 | 结果 |
| --- | --- |
| 经确认的公司官网 | [https://fontenova.com.pe/](https://fontenova.com.pe/) |
| 对应主体 | FONTENOVA DEL PERÚ S.A.C.，RUC 20610272399；商号Fontenova |
| 网站类型 | 独立公司与品牌站 |
| 核实依据 | O02/O10/O21公司名、Camino Real Mz20 Lt73与G03/G04/G08登记原页一致；G06运输单另提供同名同RUC。登记交叉页见[https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php](https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php)。G09官方经销商名单所列同址Monpar电话又与旧TDS一致，仅支持经营联系，不能合并法人。 |
| 核实日期与访问状态 | 2026-10-22；首页和联系页web超时后HTTP读到正文；若干当前PDF404，旧官方PDF可读。 |
| 其他相关官网 | 未确认集团官网；fontenova.pe的饮料企业页不作本公司官网；同址Monpar为独立RUC主体。 |

## 1 核心结论

**执行状态：completed。最终结论：继续开发。**

具体业务为瓷砖胶、填缝剂及建筑辅助清洁剂；白胶和填缝剂存在白水泥、聚合物及矿物颜料的配方说明，尚未证实采购TiO₂或色母。未取得足以客观排除的证据；不判断购买意愿。官网生产自述与登记建材批发可以并存，现有证据不能确定实际制造法人或厂址。已登记分支为仓库，不能升级成工厂。

| 问题 | 证据与边界 |
| --- | --- |
| 主体 | G03/G04/G08及G06同名同RUC/地址相互支持；当前ACTIVO/HABIDO为第三方登记转载，非本次SUNAT实时回执。 |
| 角色 | 自有品牌建筑化学品供应及制造自述O02/O05/O06；登记批发G08；独立工厂许可证/产能未取得。 |
| 产品 | O05白色柔性胶，O06矿物颜料填缝剂；O21旧白色Extrafuerte技术PDF直接可读。白色不等于使用TiO₂。 |
| 采购 | 原粉/色母采购形态、供应商、价格、年度用量均未知。G06为国内成品订单文件且Fontenova是运输方；不是原料采购或海关进口。 |
| 人员 | L08/G08第三方原页列Luis Alberto Monroy Paredes为目标总经理；岗位日期2022-10-28，未获得公司当前人员页佐证、采购权限未知。 |

### 相关来源处理表

| 编号／维度 | 发现动作 | 具体URL | 待核事项 | 原页与替代 | 结果 | 所得事实／限制 |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | S01/上批PE2-E029 | [https://fontenova.com.pe/](https://fontenova.com.pe/) | 主体/产品/工厂与联系 | C049-O01/O02 | 已读原文 | web超时后HTTP正文取得；FontenovaDelPeruSAC，CaminoRealMz20Lt73，制造自述；外省厂Próximamente非现厂 |
| F02 | O02 | [https://fontenova.com.pe/contactanos/](https://fontenova.com.pe/contactanos/) | 联系方式与法名 | C049-O03/O10 | 已读原文 | contacto@fontenova.com.pe及952625585；CaminoReal地址 |
| F03 | O02 | [https://fontenova.com.pe/productos/](https://fontenova.com.pe/productos/) | 产品及技术文件目录 | C049-O04 | 已读原文 | 白胶/灰胶产品目录 |
| F04 | O02 | [https://fontenova.com.pe/product/pegamento-blanco-flexible/](https://fontenova.com.pe/product/pegamento-blanco-flexible/) | 白胶成分技术要求 | C049-O05 | 已读原文 | 白水泥/聚合物粉状胶；所链接PDF失败，原产品成分文字已读 |
| F05 | O02 | [https://fontenova.com.pe/product/fragua-premium/](https://fontenova.com.pe/product/fragua-premium/) | 填缝剂颜料成分 | C049-O06 | 已读原文 | 矿物颜料/白水泥填缝剂；PDF失败，未确认TiO2 |
| F06 | O02 | [https://fontenova.com.pe/puntos-de-venta/](https://fontenova.com.pe/puntos-de-venta/) | 地址与工厂/分销区分 | C049-O07/O11 | 已读原文 | web验证页后HTTP取得经销商列表，不是自有工厂；后半页面程序warning不影响已读正文 |
| F07 | O05 link4 | [https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-FLEXIBLE-25.pdf](https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-FLEXIBLE-25.pdf) | 白胶技术PDF真实目标待点击取得 | C049-O08/O12/O05 | 尝试后受限 | 官网PDF链接web/直连均404；具体产品页成分和技术文字可作公开替代，文件版本/完整SDS未取得 |
| F08 | O06 link4 | [https://fontenova.com.pe/wp-content/uploads/2026/03/FT-FRAGUA-PREMIUM.pdf](https://fontenova.com.pe/wp-content/uploads/2026/03/FT-FRAGUA-PREMIUM.pdf) | 填缝剂技术PDF真实目标待点击取得 | C049-O09/O13/O06 | 尝试后受限 | 官网PDF链接web/直连均404；具体产品页成分和技术文字可作公开替代，文件版本/完整SDS未取得 |
| F09 | G01 | [https://www.universidadperu.com/empresas/fontenova-del-peru.php](https://www.universidadperu.com/empresas/fontenova-del-peru.php) | RUC/法律地址/登记状态 | C049-G02/G03/G04 | 尝试后受限 | restricted；其他两原页同RUC/地址可读，四员工仅摘要不采用规模 |
| F10 | G01 | [https://tramitesperu.com/empresas/fontenova-del-peru-s-a-c-20610272399/](https://tramitesperu.com/empresas/fontenova-del-peru-s-a-c-20610272399/) | 独立RUC地址匹配 | C049-G03 | 已读原文 | RUC20610272399，ACTIVO/HABIDO及CaminoReal地址；第三方转载非SUNAT实时查询 |
| F11 | G01 | [https://ubicania.com/empresas/fontenova-del-peru-s-a-c_id_3DB158D4A10C4BEF](https://ubicania.com/empresas/fontenova-del-peru-s-a-c_id_3DB158D4A10C4BEF) | 成立/活动及制造登记 | C049-G04 | 已读原文 | 2022-11-21注册/2023-01-02开业；建材批发；Ventanilla/SMP两分支，未证明厂；SINACTIVIDAD为2022旧数据 |
| F12 | G01 | [https://es.scribd.com/document/722245786/pegamento-blanco-bx](https://es.scribd.com/document/722245786/pegamento-blanco-bx) | 白胶Extrafuerte旧TDS技术替代 | C049-O14/O21 | 尝试后受限 | Scribd验证失败；同名官方白胶Extrafuerte旧TDS已实际读取O21，2022版本不代表最新版 |
| F13 | G01 | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf) | 灰胶TDS原件 | C049-O15/O18 | 已读原文 | 直连404但web取得4页Ed2 10.11.22，灰水泥胶及同法名地址 |
| F14 | G01 | [https://saeusceprod01.blob.core.windows.net/contentidad/uploads/b32657b2-e63b-4e25-bb97-e0879967143c.pdf](https://saeusceprod01.blob.core.windows.net/contentidad/uploads/b32657b2-e63b-4e25-bb97-e0879967143c.pdf) | 政府采购文件同RUC物流身份 | C049-G06 p1–2/6–9 | 已读原文 | 2024采购附件Fontenova同RUC为运输方，品牌白胶FT010425B；合同方Selvaleva，不把其终止申请认作Fontenova处罚 |
| F15 | G01 | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf) | 清洁剂技术文件边界 | C049-O16/O19 | 已读原文 | 直连404但web取得2页Ed1 27.12.22，蓝色液体清洁剂，不是颜料粉 |
| F16 | G01 | [https://pe.linkedin.com/in/luis-alberto-monroy-paredes-855596124](https://pe.linkedin.com/in/luis-alberto-monroy-paredes-855596124) | 公开具名岗位 | C049-L02/L04/L08 | 尝试后受限 | 个人页999；DatosPeru提供目标经理同名记录，但个人LinkedIn所链饮料公司不同域/地址，不能确认该URL属于目标经理；保留同名公开管理线索及身份限制 |
| F17 | G01 | [https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf](https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf) | 白瓷砖胶TDS | C049-O17/O20/O05 | 尝试后受限 | 直连404/web验证页；白胶同官网产品原文作替代，2025文件全文未知 |
| F18 | G01 | [https://pe.computrabajo.com/empresas/acerca-de-fontenova-del-peru-sac-FB7683F8231DDC9D](https://pe.computrabajo.com/empresas/acerca-de-fontenova-del-peru-sac-FB7683F8231DDC9D) | 公开招聘公司与岗位 | C049-L03/L06/L07 | 尝试后受限 | 公司页403，职位列表返回验证页；定向招聘搜索仅列公司/一个职位但未取得职位名称和职责，无可用具体岗位原页，现职人员未知。 |
| F19 | L01 | [https://pe.linkedin.com/company/fontenova-peru](https://pe.linkedin.com/company/fontenova-peru) | 同名企业是否目标 | C049-L04 | 有据判定不相关 | 企业原页为Breña食品饮料、2018成立、fontenova.pe，与本公司域名地址业务不同 |
| F20 | L05 | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-BLANCO-EXTRAFUERTE.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-BLANCO-EXTRAFUERTE.pdf) | 白胶TDS替代Scribd | C049-O21 | 已读原文 | 4页Ed2 10.11.22白水泥/聚合物胶FT010525B；无TiO2明确成分 |
| F21 | L06 | [https://pe.computrabajo.com/empresas/empresas-en-lima-en-la-victoria%26gclid%3DEAIaIQobChMIwrSzs7zT5wIVBpSzCh1G6QIaEAAYASAAEgJ7TvD_BwE?p=416](https://pe.computrabajo.com/empresas/empresas-en-lima-en-la-victoria%26gclid%3DEAIaIQobChMIwrSzs7zT5wIVBpSzCh1G6QIaEAAYASAAEgJ7TvD_BwE?p=416) | 招聘替代入口与实际职位链接 | C049-L07/L06/L03 | 尝试后受限 | 公司页403，职位列表返回验证页；定向招聘搜索仅列公司/一个职位但未取得职位名称和职责，无可用具体岗位原页，现职人员未知。 |
| F22 | C049-D03 | [https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php](https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php) | 同址Fontenova商标及LuisMonroy关系/贸易 | C049-D04 /C049-D07 | 已读原文 | 同址不同RUC20606304669，MonroyParedesLuisAlberto列2020起总经理；公开原页未显示索引所列Fontenova商标/陶瓷HS69，不能认集团或采购关系；HTTP403替代未恢复商标/贸易区；商标与HS69九记录保留为仅索引，不合并为目标贸易。 |
| F23 | C049-D04 link7 | [https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php](https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php) | 同址经营方经理是否本公司岗位 | C049-L08 | 已读原文 | 原页列LuisAlbertoMonroyParedes为目标RUC20610272399总经理，起2022-10-28；另列Monpar与ConstructTower；同经理不自动证明控股集团或本公司继承他企状态 |
| F24 | C049-L08 link6 | [https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php](https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php) | 目标法人登记/经理及贸易原页 | C049-G08 | 已读原文 | 目标RUC/经理/地址匹配，三分支标DE.DEPOSITO仓库非工厂；日期比Ubicania早一天有冲突；SINACTIVIDAD/无HS明细不等于没有进口 |
| F25 | C049-D06 | [https://www.linkedin.com/company/fontenova-per%C3%BA](https://www.linkedin.com/company/fontenova-per%C3%BA) | Monpar企业页与Fontenova品牌域名/人员关系 | C049-L09/D04/L08/G09 | 尝试后受限 | LinkedIn原页robots拒绝；DatosPeru经理/公司页及Celima官方经销商PDF替代证实同址/电话与经理；具体LinkedIn员工未取得 |
| F26 | C049-D06 | [https://www.celima-trebol.com/wp-content/uploads/2022/03/Distribuidores-Participantes-Celima-Trebol-Te-Moviliza.pdf](https://www.celima-trebol.com/wp-content/uploads/2022/03/Distribuidores-Participantes-Celima-Trebol-Te-Moviliza.pdf) | 官方渠道名单同址核对 | C049-G09 p2行46 | 已读原文 | Celima经销商名单列Monpar，CaminoRealMz20Lt73，电话961729634与Fontenova旧TDS相同；非工厂或股权关系证明 |
| F27 | C049-L06 | [https://pe.computrabajo.com/empresas/empresas-en--con-ofertas-activas?p=493](https://pe.computrabajo.com/empresas/empresas-en--con-ofertas-activas?p=493) | 岗位替代列表是否具体职责 | C049-L10 | 已读原文 | 列表原页列目标Carabayllo/批发/一空缺，详情F28已尝试受限 |
| F28 | C049-L10 link168 | [https://pe.computrabajo.com/empresas/ofertas-de-trabajo-de-fontenova-del-peru-sac-FB7683F8231DDC9D](https://pe.computrabajo.com/empresas/ofertas-de-trabajo-de-fontenova-del-peru-sac-FB7683F8231DDC9D) | 唯一职位原页职责 | C049-L11/L06/L03/L10 | 尝试后受限 | 具体招聘列表仅JS机器人验证；公司简介403/定向搜索及通用列表无岗位名称，不猜采购或技术岗 |

**来源对账记录：** 2026-10-22T12:13:00.859Z（UTC；本地北京时间+8）。已对照C049-O01–O21、G01–G09、L01–L11、D01–D07的全部原始搜索/读取返回与S01，并回读具体采用PDF页。共28项＝已读原文17＋尝试后受限10＋有据判定不相关1＋待处理0。G06核读p1–2和p6–9，不声称无文本的中间附件已完整视觉审阅。重复出现的原网页/技术PDF合并；一般灰胶零售、地址目录与同域同事项链接无新增成分/身份矛盾时按有限延伸结束；Monpar其他招聘为明确不同雇主且未见目标兼岗，不转写目标岗位。D05他国水/饮料贸易及无关专利仅留原返回。D03后发现同址/同经理新线索后追加F22–26，改正F16早先过强的“不相关”，最终为个人URL受限且身份未确认。F27为收尾核对时补登记，L10实际读取并继续处理新F28；这一次补表不称实时登记已通过。所有来源已按实际结果关闭，没有以访问失败替代尚未尝试工作。


### OGLD执行复核

| 维度 | 已执行范围／证据 | 状态 | 替代与限制 | 尚未执行的必要工作 |
| --- | --- | --- | --- | --- |
| O | F01–08、F12–15、F17/F20；首页/联系/产品/经销商/三份旧技术PDF，O01–O21 | 已执行但受限 | web失败转HTTP；当前白胶/填缝PDF404，产品原文及旧官方技术PDF可读，版本边界保留；工厂为自述 | 无；未发现可用独立厂证或完整现行SDS |
| G | G01–G09；F09–11/F14/F22–24/F26，名称、RUC、地址、经理、分支、采购附件核对 | 已执行但受限 | 登记转载日期差一天不擅定；分支仓库及经营同址不等于制造/股权关系；采购附件非处罚决定 | 无；实时官方登记与许可证未知 |
| L | L01–L11；F16/F18–19/F23/F25/F27–28；企业/个人/准确公司招聘及关联方企业核查 | 已执行但受限 | 同名饮料页排除公司归属；个人URL未确认，目标经理另有RUC关联原页；招聘具体页验证受限 | 无；已尝试具体岗位页及可行公开替代，不编造岗位 |
| D | D01–D07＋G08；现名/简称、RUC、Camino Real地址、TiO₂/二氧化钛/masterbatch/320611检索、平台索引及同址Monpar核查 | 已执行但受限 | 没有目标可核对进出口记录；Monpar陶瓷贸易仅缓存且独立RUC；Paraguay Fontenova不作秘鲁目标 | 无；未发现可另取的目标海关明细；无已证实旧法人名称/控股集团须扩查 |

## 2 O 官网

O02自述由多年胶粘剂经验发展而来，超过25年的表述是经验口径，不能作为本法人2022年登记之前的成立日期。网站称分散制造布局并标Chiclayo、Arequipa为“Próximamente”；这两地规划不能写成已运行工厂。实际联系地址Av. Camino Real Mz20 Lt73，San Pedro de Carabayllo，Lima；未证实该地址就是制造厂。

| 产品／应用 | 原页与版本 | 原料和性能证据及边界 |
| --- | --- | --- |
| Pegamento Blanco Flexible，瓷砖/瓷质砖胶 | O05现行产品页；其2025目录PDF O08/O12均404 | 白水泥、聚合物、防水添加物及骨料；未披露TiO₂，不解释为完整配方不含。 |
| Fragua Premium填缝剂 | O06产品页；2026路径PDF O09/O13均404 | 白水泥、再分散树脂、骨料、有机/无机添加物与矿物颜料；未披露矿物颜料种类。 |
| Blanco Extrafuerte | O21官方4页，Edición2，10.11.22；p1成分/p3规格/p4联系 | 白水泥聚合物胶，25kg，FT010525B；旧版本参数仅支持该文件，不是当前配方证明。 |
| Gris Extrafuerte | O18官方4页，Edición2，10.11.22；p1/p3 | 灰水泥胶，FT010225G；不是白色颜料采购证据。 |
| Limpiador de Porcelanato | O19官方2页，Edición1，27.12.22，p1 | 蓝色液体清洁剂；与粉体颜料区分。 |
| Blanco Porcelanato技术资料 | O17/O20：直连404、web验证页 | 2025 PDF完整正文未取；不采用搜索缓存性能为已核实数据。 |

官方公开联系：contacto@fontenova.com.pe，+51 952625585（O10）；旧TDS电话+51 961729634（O21），历史渠道保留不冒称当前复验。未猜个人邮箱。O11经销商列表包括Centro Cerámico C&S、Cerámicos Cáceres、Ledisa等，为销售网络而非目标工厂。LABISER/UNI测试为官网自述；未取得独立检测报告。

## 3 G 公开核实

G03/G04/G08交叉匹配RUC20610272399及Camino Real Mz20 Lt73。登记日期有一天差异：Ubicania为21/11/2022、开业02/01/2023；DatosPeru为20/11/2022、开业01/01/2023。保留两种记录，不用技术文件2022日期或官网25年经验消除矛盾；该差异不影响本次RUC/地址识别，精确法律日期尚无官方回执。

G08的Ventanilla Parque Porcino IV、SMP Santa Leonor6342-A、Chiclayo Chosica del Norte Mz26 Lt03均标“DE.DEPOSITO”。这是仓库登记，不是工厂证据。规模、收入、产能未知，不使用第三方估值或集团数字推算。

D04/L08显示独立主体Distribuciones Monpar S.A.C.（RUC20606304669）与目标同址并共享公开登记经理。G09为Celima–Trebol官方历史经销商PDF，p2第46行列Monpar同址及961729634，与Fontenova旧TDS电话相同。可支持经营关联线索，不能证明母子公司、受控集团、品牌产权转移或制造归属。D03/D06搜索索引显示Monpar拥有FONTENOVA商标、陶瓷HS69九条记录，但D04原页未显示该部分、D07直连403，故这两项保留仅缓存。另一经理任职企业Construct Tower独立RUC20603892233的注销状态不得转移给Fontenova。

G06：2024-06-19 Selvaleva向UNI提出终止订单的函件；附件p6–7订单OCAM-2024-92-2760-1涉及450袋25kg Fontenova Blanco Flexible FT010425B、金额S/16673.40。p8运输单EG07-00000058（2024-06-12）列Fontenova同RUC为运输方；p9发票卖方Selvaleva、买方UNI。函件对品牌不被接受的说法为Selvaleva单方陈述，不是政府产品缺陷认定、处罚或Fontenova违约决定；也不构成该公司的进口量。

## 4 L LinkedIn

检索分开覆盖公司、采购/经理/生产岗位及精确法名招聘（L01/L05/L06）。F19的LinkedIn“Fontenova Perú”原页为Breña食品饮料、fontenova.pe，不能当作建筑胶公司；没有据此导入其员工。F25的“fontenova-perú”企业页搜索标题为Distribuciones Monpar，原页robots拒绝；另用登记与官方经销商证据核对经营身份。

| 公开线索 | 岗位／雇主／地区与依据 | 职责及现职限制 | 个人页与联系 |
| --- | --- | --- | --- |
| Luis Alberto Monroy Paredes | L08/G08原页列目标RUC的Gerente General，自2022-10-28；Carabayllo法人地址 | 属管理线索，未证实负责原料采购；公司现职自述未取得。与Monpar共享经理不推出采购授权或上下级关系。 | [https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php](https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php)。同名LinkedIn URL见F16，999且饮料企业关联存在歧义，未确认是该经理；个人邮箱未获取。 |
| 官网业务入口 | O10联系方式，无公开姓名/部门职责 | 可供后续授权工作转介；非已确定采购岗 | contacto@fontenova.com.pe为官方公开公司邮箱；2026-10-22读取，无邮箱服务验证，不等于可送达或已联系。 |
| 招聘线索 | L10原页目标法名、Carabayllo/批发、一空缺 | L03简介403、L07/L11具体列表JS验证；没有岗位名称与职责，不能补作采购或技术现职 | F18/F21/F27/F28；未获取姓名或邮箱。 |

本阶段不优选收件人，不做独立组织图谱。保留全部与当前主体有关的已见公开线索。

## 5 D 海关

本次D01检索Fontenova与titanium dioxide/dióxido de titanio/masterbatch/importaciones；D02精确RUC与进出口；D03现商号＋Camino Real＋import/titanium/320611/masterbatch；D05加入Panjiva/Veritrade/Volza；D06核查已发现同址经理关联企业Monpar。未发现已确认英文旧名或前身法人，不能虚构；Monpar不是自动视为旧名。HS320611仅搜索线索，未取得秘鲁当年商品归类记录，不由编码确定产品。

| 记录 | 可见信息 | 边界 |
| --- | --- | --- |
| 目标Fontenova | G08/D02登记显示SIN ACTIVIDAD，未见可核对提单、进口日期、供应商、品名/HS、净重或金额 | 登记聚合页面与旧Ubicania2022资料不证明2026没有进口。公开平台搜索覆盖年份未知。 |
| Monpar | D03/D06索引提示陶瓷HS69、9记录、图表范围2023–2025；D04仅能读登记与经理，D07 403 | 仅搜索缓存，未取得明细方向/单位/交易对手；不同RUC，不计目标交易或TiO₂采购。 |
| Paraguay Fontenova/Lorentz | D05平台结果国家为Paraguay，出现2017进口线索 | 与本秘鲁2022登记RUC无匹配依据，明显同名他国结果，不采用为目标进口证据。 |
| G06国内采购附件 | 成品胶粘剂与运输记录 | 非跨境贸易，也非目标原料采购。 |

没有可计入目标的合格海关明细，因此不计算重量/订单次数/年度用量；跨平台同一索引重复不累计。供应商、原产地、价格和频率未知。

## 6 商业匹配

| 应用／采购形态 | 客观依据 | 产品方向与待验证条件 |
| --- | --- | --- |
| 水泥基白胶和矿物颜料填缝剂 | O05/O06/O21；仅证实产品文字及旧技术版本 | 用户固定规则仅涵盖涂料M-510、塑料/色母M-340、油墨M-52；本案水泥胶/填缝应用未明确涵盖，须由用户明确后才定牌号，不自行归成涂料或增加备选。最新版TDS和配方测试均未开展。 |
| 颜料原粉／配制料 | 矿物颜料有产品自述，未确认具体颜料、直接采购与自制/外包 | 不把白水泥视为TiO₂，不声称已匹配原粉。 |
| 色母与塑料制品 | 没有本公司树脂加工、载体或母粒配方证据 | 不由清洁剂瓶包装推断色母采购；目前未形成此应用推荐。 |

继续开发仅意味着没有客观排除依据，不代表需求量、具体技术适配或采购意愿已证实。

## 7 下一步

本次公开必要调查已执行，以下为完成后的交接事项，不自动启动：

| 项 | 对象 | 后续工作及条件 | 负责人 |
| --- | --- | --- | --- |
| 1 | 目标业务/管理入口 | 后续获授权时确认原料采购由Fontenova还是同址独立法人负责、制造与仓库分工；不得默认总经理个人页面归属。 | 业务负责人 |
| 2 | 应用技术岗位 | 若进入技术交流，确认填缝剂矿物颜料及白胶配方所用材料/生产归属，再由用户明确未覆盖应用牌号并核对最新TDS、测试条件。 | 技术负责人 |
| 3 | 下游资料使用者 | 沿用本报告的同名公司、登记日期差异、旧技术版本及招聘受限记录；订单附件不作负面定论或原料采购证据。 | 后续专业Agent |

调查completed；公开管理线索1人但未优选、无已验证个人邮箱；邮件未发送。

## 8 证据目录与所有信息来源网址

下表按具体URL列发布者、用途、版本和原始动作。访问日期均2026-10-22；未标注日期的网页不推定发布日期。F编号与正文O/G/L/D动作一一对应，失败亦保留。

| 证据／F编号 | 发布者与具体用途 | 完整URL | 内容版本／日期 | 访问／状态 |
| --- | --- | --- | --- | --- |
| C049-O01/O02／F01 | fontenova.com.pe；主体/产品/工厂与联系 | [https://fontenova.com.pe/](https://fontenova.com.pe/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；web超时后HTTP正文取得；FontenovaDelPeruSAC，CaminoRealMz20Lt73，制造自述；外省厂Próximamente非现厂 |
| C049-O03/O10／F02 | fontenova.com.pe；联系方式与法名 | [https://fontenova.com.pe/contactanos/](https://fontenova.com.pe/contactanos/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；contacto@fontenova.com.pe及952625585；CaminoReal地址 |
| C049-O04／F03 | fontenova.com.pe；产品及技术文件目录 | [https://fontenova.com.pe/productos/](https://fontenova.com.pe/productos/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；白胶/灰胶产品目录 |
| C049-O05／F04 | fontenova.com.pe；白胶成分技术要求 | [https://fontenova.com.pe/product/pegamento-blanco-flexible/](https://fontenova.com.pe/product/pegamento-blanco-flexible/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；白水泥/聚合物粉状胶；所链接PDF失败，原产品成分文字已读 |
| C049-O06／F05 | fontenova.com.pe；填缝剂颜料成分 | [https://fontenova.com.pe/product/fragua-premium/](https://fontenova.com.pe/product/fragua-premium/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；矿物颜料/白水泥填缝剂；PDF失败，未确认TiO2 |
| C049-O07/O11／F06 | fontenova.com.pe；地址与工厂/分销区分 | [https://fontenova.com.pe/puntos-de-venta/](https://fontenova.com.pe/puntos-de-venta/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；web验证页后HTTP取得经销商列表，不是自有工厂；后半页面程序warning不影响已读正文 |
| C049-O08/O12/O05／F07 | fontenova.com.pe；白胶技术PDF真实目标待点击取得 | [https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-FLEXIBLE-25.pdf](https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-FLEXIBLE-25.pdf) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；官网PDF链接web/直连均404；具体产品页成分和技术文字可作公开替代，文件版本/完整SDS未取得 |
| C049-O09/O13/O06／F08 | fontenova.com.pe；填缝剂技术PDF真实目标待点击取得 | [https://fontenova.com.pe/wp-content/uploads/2026/03/FT-FRAGUA-PREMIUM.pdf](https://fontenova.com.pe/wp-content/uploads/2026/03/FT-FRAGUA-PREMIUM.pdf) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；官网PDF链接web/直连均404；具体产品页成分和技术文字可作公开替代，文件版本/完整SDS未取得 |
| C049-G02/G03/G04／F09 | www.universidadperu.com；RUC/法律地址/登记状态 | [https://www.universidadperu.com/empresas/fontenova-del-peru.php](https://www.universidadperu.com/empresas/fontenova-del-peru.php) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；restricted；其他两原页同RUC/地址可读，四员工仅摘要不采用规模 |
| C049-G03／F10 | tramitesperu.com；独立RUC地址匹配 | [https://tramitesperu.com/empresas/fontenova-del-peru-s-a-c-20610272399/](https://tramitesperu.com/empresas/fontenova-del-peru-s-a-c-20610272399/) | 详见正文；未标注者未知 | 2026-10-22；已读原文；RUC20610272399，ACTIVO/HABIDO及CaminoReal地址；第三方转载非SUNAT实时查询 |
| C049-G04／F11 | ubicania.com；成立/活动及制造登记 | [https://ubicania.com/empresas/fontenova-del-peru-s-a-c_id_3DB158D4A10C4BEF](https://ubicania.com/empresas/fontenova-del-peru-s-a-c_id_3DB158D4A10C4BEF) | 详见正文；未标注者未知 | 2026-10-22；已读原文；2022-11-21注册/2023-01-02开业；建材批发；Ventanilla/SMP两分支，未证明厂；SINACTIVIDAD为2022旧数据 |
| C049-O14/O21／F12 | es.scribd.com；白胶Extrafuerte旧TDS技术替代 | [https://es.scribd.com/document/722245786/pegamento-blanco-bx](https://es.scribd.com/document/722245786/pegamento-blanco-bx) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；Scribd验证失败；同名官方白胶Extrafuerte旧TDS已实际读取O21，2022版本不代表最新版 |
| C049-O15/O18／F13 | fontenova.com.pe；灰胶TDS原件 | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf) | Ed2 10.11.22，4页 | 2026-10-22；已读原文；直连404但web取得4页Ed2 10.11.22，灰水泥胶及同法名地址 |
| C049-G06 p1–2/6–9／F14 | saeusceprod01.blob.core.windows.net；政府采购文件同RUC物流身份 | [https://saeusceprod01.blob.core.windows.net/contentidad/uploads/b32657b2-e63b-4e25-bb97-e0879967143c.pdf](https://saeusceprod01.blob.core.windows.net/contentidad/uploads/b32657b2-e63b-4e25-bb97-e0879967143c.pdf) | 2024-06-19函、2024-06-12运单，p1–2/6–9 | 2026-10-22；已读原文；2024采购附件Fontenova同RUC为运输方，品牌白胶FT010425B；合同方Selvaleva，不把其终止申请认作Fontenova处罚 |
| C049-O16/O19／F15 | fontenova.com.pe；清洁剂技术文件边界 | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf) | Ed1 27.12.22，2页 | 2026-10-22；已读原文；直连404但web取得2页Ed1 27.12.22，蓝色液体清洁剂，不是颜料粉 |
| C049-L02/L04/L08／F16 | pe.linkedin.com；公开具名岗位 | [https://pe.linkedin.com/in/luis-alberto-monroy-paredes-855596124](https://pe.linkedin.com/in/luis-alberto-monroy-paredes-855596124) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；个人页999；DatosPeru提供目标经理同名记录，但个人LinkedIn所链饮料公司不同域/地址，不能确认该URL属于目标经理；保留同名公开管理线索及身份限制 |
| C049-O17/O20/O05／F17 | fontenova.com.pe；白瓷砖胶TDS | [https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf](https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；直连404/web验证页；白胶同官网产品原文作替代，2025文件全文未知 |
| C049-L03/L06/L07／F18 | pe.computrabajo.com；公开招聘公司与岗位 | [https://pe.computrabajo.com/empresas/acerca-de-fontenova-del-peru-sac-FB7683F8231DDC9D](https://pe.computrabajo.com/empresas/acerca-de-fontenova-del-peru-sac-FB7683F8231DDC9D) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；公司页403，职位列表返回验证页；定向招聘搜索仅列公司/一个职位但未取得职位名称和职责，无可用具体岗位原页，现职人员未知。 |
| C049-L04／F19 | pe.linkedin.com；同名企业是否目标 | [https://pe.linkedin.com/company/fontenova-peru](https://pe.linkedin.com/company/fontenova-peru) | 详见正文；未标注者未知 | 2026-10-22；有据判定不相关；企业原页为Breña食品饮料、2018成立、fontenova.pe，与本公司域名地址业务不同 |
| C049-O21／F20 | fontenova.com.pe；白胶TDS替代Scribd | [https://fontenova.com.pe/wp-content/uploads/2023/10/FT-BLANCO-EXTRAFUERTE.pdf](https://fontenova.com.pe/wp-content/uploads/2023/10/FT-BLANCO-EXTRAFUERTE.pdf) | Ed2 10.11.22，4页 | 2026-10-22；已读原文；4页Ed2 10.11.22白水泥/聚合物胶FT010525B；无TiO2明确成分 |
| C049-L07/L06/L03／F21 | pe.computrabajo.com；招聘替代入口与实际职位链接 | [https://pe.computrabajo.com/empresas/empresas-en-lima-en-la-victoria%26gclid%3DEAIaIQobChMIwrSzs7zT5wIVBpSzCh1G6QIaEAAYASAAEgJ7TvD_BwE?p=416](https://pe.computrabajo.com/empresas/empresas-en-lima-en-la-victoria%26gclid%3DEAIaIQobChMIwrSzs7zT5wIVBpSzCh1G6QIaEAAYASAAEgJ7TvD_BwE?p=416) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；公司页403，职位列表返回验证页；定向招聘搜索仅列公司/一个职位但未取得职位名称和职责，无可用具体岗位原页，现职人员未知。 |
| C049-D04 /C049-D07／F22 | www.datosperu.org；同址Fontenova商标及LuisMonroy关系/贸易 | [https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php](https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php) | 详见正文；未标注者未知 | 2026-10-22；已读原文；同址不同RUC20606304669，MonroyParedesLuisAlberto列2020起总经理；公开原页未显示索引所列Fontenova商标/陶瓷HS69，不能认集团或采购关系；HTTP403替代未恢复商标/贸易区；商标与HS69九记录保留为仅索引，不合并为目标贸易。 |
| C049-L08／F23 | www.datosperu.org；同址经营方经理是否本公司岗位 | [https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php](https://www.datosperu.org/ejecutivos-3d137f0c14c4ed15cae64d9684ab5d47.php) | 详见正文；未标注者未知 | 2026-10-22；已读原文；原页列LuisAlbertoMonroyParedes为目标RUC20610272399总经理，起2022-10-28；另列Monpar与ConstructTower；同经理不自动证明控股集团或本公司继承他企状态 |
| C049-G08／F24 | www.datosperu.org；目标法人登记/经理及贸易原页 | [https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php](https://www.datosperu.org/empresa-fontenova-del-peru-sac-20610272399.php) | 详见正文；未标注者未知 | 2026-10-22；已读原文；目标RUC/经理/地址匹配，三分支标DE.DEPOSITO仓库非工厂；日期比Ubicania早一天有冲突；SINACTIVIDAD/无HS明细不等于没有进口 |
| C049-L09/D04/L08/G09／F25 | www.linkedin.com；Monpar企业页与Fontenova品牌域名/人员关系 | [https://www.linkedin.com/company/fontenova-per%C3%BA](https://www.linkedin.com/company/fontenova-per%C3%BA) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；LinkedIn原页robots拒绝；DatosPeru经理/公司页及Celima官方经销商PDF替代证实同址/电话与经理；具体LinkedIn员工未取得 |
| C049-G09 p2行46／F26 | www.celima-trebol.com；官方渠道名单同址核对 | [https://www.celima-trebol.com/wp-content/uploads/2022/03/Distribuidores-Participantes-Celima-Trebol-Te-Moviliza.pdf](https://www.celima-trebol.com/wp-content/uploads/2022/03/Distribuidores-Participantes-Celima-Trebol-Te-Moviliza.pdf) | URL目录2022/03；p2行46，正文未标日期 | 2026-10-22；已读原文；Celima经销商名单列Monpar，CaminoRealMz20Lt73，电话961729634与Fontenova旧TDS相同；非工厂或股权关系证明 |
| C049-L10／F27 | pe.computrabajo.com；岗位替代列表是否具体职责 | [https://pe.computrabajo.com/empresas/empresas-en--con-ofertas-activas?p=493](https://pe.computrabajo.com/empresas/empresas-en--con-ofertas-activas?p=493) | 详见正文；未标注者未知 | 2026-10-22；已读原文；列表原页列目标Carabayllo/批发/一空缺，详情F28已尝试受限 |
| C049-L11/L06/L03/L10／F28 | pe.computrabajo.com；唯一职位原页职责 | [https://pe.computrabajo.com/empresas/ofertas-de-trabajo-de-fontenova-del-peru-sac-FB7683F8231DDC9D](https://pe.computrabajo.com/empresas/ofertas-de-trabajo-de-fontenova-del-peru-sac-FB7683F8231DDC9D) | 详见正文；未标注者未知 | 2026-10-22；尝试后受限；具体招聘列表仅JS机器人验证；公司简介403/定向搜索及通用列表无岗位名称，不猜采购或技术岗 |

输入S01：[正式名单](<D:/02钛白粉外贸/markets/PE/prospecting/PE-20261022-02/01_候选客户总表.md>)第100行PE-C049/PE-L054；[历史发现材料](<D:/02钛白粉外贸/markets/PE/prospecting/PE-20261021-02/_work/research-data.json>)PE2-E029，作为线索复用。输入未修改。

原始返回与动作索引（包括失败，保存不等于来源已证实）：

- C049-O01 read error：[C049-O01.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O01.json>)；https://fontenova.com.pe/
- C049-O02 read success：[C049-O02.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O02.json>)；https://fontenova.com.pe/
- C049-O03 read error：[C049-O03.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O03.json>)；https://fontenova.com.pe/contactanos/
- C049-O04 read success：[C049-O04.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O04.json>)；https://fontenova.com.pe/productos/
- C049-O05 read success：[C049-O05.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O05.json>)；https://fontenova.com.pe/product/pegamento-blanco-flexible/
- C049-O06 read success：[C049-O06.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O06.json>)；https://fontenova.com.pe/product/fragua-premium/
- C049-O07 read success：[C049-O07.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O07.json>)；https://fontenova.com.pe/puntos-de-venta/
- C049-O08 read error：[C049-O08.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O08.json>)；https://fontenova.com.pe/product/pegamento-blanco-flexible/ link4 technical PDF
- C049-O09 read error：[C049-O09.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O09.json>)；https://fontenova.com.pe/product/fragua-premium/ link4 technical PDF
- C049-O10 read success：[C049-O10.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O10.json>)；https://fontenova.com.pe/contactanos/
- C049-O11 read success：[C049-O11.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O11.json>)；https://fontenova.com.pe/puntos-de-venta/
- C049-O12 read error：[C049-O12.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O12.json>)；https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-FLEXIBLE-25.pdf
- C049-O13 read error：[C049-O13.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O13.json>)；https://fontenova.com.pe/wp-content/uploads/2026/03/FT-FRAGUA-PREMIUM.pdf
- C049-G01 search success：[C049-G01.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G01.json>)；"Fontenova del Peru" RUC fabrica
- C049-G02 read error：[C049-G02.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G02.json>)；https://www.universidadperu.com/empresas/fontenova-del-peru.php
- C049-G03 read success：[C049-G03.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G03.json>)；https://tramitesperu.com/empresas/fontenova-del-peru-s-a-c-20610272399/
- C049-G04 read success：[C049-G04.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G04.json>)；https://ubicania.com/empresas/fontenova-del-peru-s-a-c_id_3DB158D4A10C4BEF
- C049-G05 search success：[C049-G05.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G05.json>)；"20610272399" "Fontenova" planta gerente
- C049-O14 read success：[C049-O14.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O14.json>)；https://es.scribd.com/document/722245786/pegamento-blanco-bx
- C049-O15 read error：[C049-O15.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O15.json>)；https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf
- C049-G06 read success：[C049-G06.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G06.json>)；https://saeusceprod01.blob.core.windows.net/contentidad/uploads/b32657b2-e63b-4e25-bb97-e0879967143c.pdf
- C049-O16 read error：[C049-O16.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O16.json>)；https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf
- C049-O17 read error：[C049-O17.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O17.json>)；https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf
- C049-O18 read success：[C049-O18.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O18.json>)；https://fontenova.com.pe/wp-content/uploads/2023/10/FT-GRIS-EXTRAFUERTE.pdf
- C049-O19 read success：[C049-O19.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O19.json>)；https://fontenova.com.pe/wp-content/uploads/2023/10/FT-LIMPIADOR-DE-PORCELANATO.pdf
- C049-O20 read success：[C049-O20.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O20.json>)；https://fontenova.com.pe/wp-content/uploads/2025/10/FT-BLANCO-PORCELANATO-25.pdf
- C049-G07 search success：[C049-G07.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G07.json>)；"Fontenova" "planta" "Ventanilla" OR "Santa Leonor" OR sancion
- C049-L01 search success：[C049-L01.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L01.json>)；"Fontenova" LinkedIn compras gerente produccion empleo
- C049-L02 read error：[C049-L02.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L02.json>)；https://pe.linkedin.com/in/luis-alberto-monroy-paredes-855596124
- C049-L03 read error：[C049-L03.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L03.json>)；https://pe.computrabajo.com/empresas/acerca-de-fontenova-del-peru-sac-FB7683F8231DDC9D
- C049-L04 read success：[C049-L04.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L04.json>)；https://pe.linkedin.com/company/fontenova-peru
- C049-L05 search success：[C049-L05.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L05.json>)；"Fontenova" "pegamentos" (compras OR gerente OR produccion OR empleo)
- C049-O21 read success：[C049-O21.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-O21.json>)；https://fontenova.com.pe/wp-content/uploads/2023/10/FT-BLANCO-EXTRAFUERTE.pdf
- C049-L06 search success：[C049-L06.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L06.json>)；"FONTENOVA DEL PERU SAC" empleo compras produccion
- C049-D01 search success：[C049-D01.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D01.json>)；"Fontenova" ("titanium dioxide" OR "dioxido de titanio" OR masterbatch OR importaciones)
- C049-L07 read success：[C049-L07.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L07.json>)；https://pe.computrabajo.com/empresas/empresas-en-lima-en-la-victoria%26gclid%3DEAIaIQobChMIwrSzs7zT5wIVBpSzCh1G6QIaEAAYASAAEgJ7TvD_BwE?p=416
- C049-D02 search success：[C049-D02.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D02.json>)；"20610272399" import export OR "Fontenova del Peru" aduana
- C049-D03 search success：[C049-D03.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D03.json>)；"Fontenova" "Camino Real" (import OR titanium OR 320611 OR masterbatch)
- C049-D04 read success：[C049-D04.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D04.json>)；https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php
- C049-D05 search success：[C049-D05.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D05.json>)；"Fontenova" Peru (Panjiva OR Veritrade OR Volza)
- C049-L08 read success：[C049-L08.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L08.json>)；C049-D04 link7 person
- C049-G08 read success：[C049-G08.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G08.json>)；C049-L08 link6 Fontenova RUC20610272399
- C049-D06 search success：[C049-D06.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D06.json>)；"Distribuciones Monpar" (importaciones OR titanium OR pigmentos OR Fontenova)
- C049-L09 read error：[C049-L09.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L09.json>)；https://www.linkedin.com/company/fontenova-per%C3%BA
- C049-G09 read success：[C049-G09.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-G09.json>)；https://www.celima-trebol.com/wp-content/uploads/2022/03/Distribuidores-Participantes-Celima-Trebol-Te-Moviliza.pdf
- C049-D07 read error：[C049-D07.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-D07.json>)；https://www.datosperu.org/empresa-distribuciones-monpar-sac-20606304669.php
- C049-L10 read success：[C049-L10.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L10.json>)；https://pe.computrabajo.com/empresas/empresas-en--con-ofertas-activas?p=493
- C049-L11 read success：[C049-L11.json](<D:/02钛白粉外贸/markets/PE/due-diligence/PE-DD-20261022-02/logs/evidence/C049-L11.json>)；C049-L10 link168 actual company jobs
