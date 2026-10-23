import pathlib,json,hashlib,datetime,shutil
R=pathlib.Path('D:/02钛白粉外贸');B=R/'markets/BE/due-diligence/BE-DD-20261022-02'
assert sorted(p.name for p in B.iterdir())==['_init.py'],'batch conflict'
(B/'_work').mkdir()
old=R/'markets/BE/due-diligence/BE-DD-20261022-01/_work'
s=(old/'batch.py').read_text(encoding='utf-8')
s=s.replace('BE-DD-20261022-01','BE-DD-20261022-02').replace('BE-20261022-01','BE-20261022-02').replace('BE-C001–BE-C010','BE-C011–BE-C020').replace("h['companies']","h['items']")
s=s.replace("'_work/market-handoff.json']","'_work/leads.json','_work/evidence-index.json','_work/market-handoff.json']")
s=s.replace('纳入唯一valid10家，未纳入0。原报告定位限markets/BE/companies，启动时无该目录；无同主体旧背调，逐家new；不扫描其他市场。','纳入本批唯一valid10家C011–020；未纳入BE-L017 Libert（duplicate→旧C002），旧10家在本次范围之外。启动时companies仅旧C001–010，无新ID目录；按ID、名称、VAT、域名与市场身份关系未见同主体旧报告，本批逐家new。主对话确认本批唯一写入者；不扫描其他市场。')
s=s.replace("ROOT/'.codex/agents/customer-research.toml'","ROOT/'AGENTS.md',ROOT/'.codex/agents/customer-research.toml'")
(B/'_work/batch.py').write_text(s,encoding='utf-8')
s=(old/'report.py').read_text(encoding='utf-8').replace('BE-20261022-01','BE-20261022-02')
s=s.replace("state=e.get('state','已读原文') if e else", "state=e.get('state','已读原文') if e else")
s=s.replace("## 4 L LinkedIn\\n\\n{d['l']}","## 4 L LinkedIn\\n\\n{d['l']}\\n\\n{d.get('people_table','| 姓名／部门 | 职位、雇主、地区 | 职责/现职边界 | 来源 | 邮箱及验证 |'+chr(10)+'| --- | --- | --- | --- | --- |'+chr(10)+'| 未取得具名人员 | 未知 | 不推定现职/权限 | 见L证据及动作 | 未获取 |')}")
s=s.replace("具体产品/技术资料：{d['product']}；详见O证据。","具体产品/技术资料：{d['product']}；详见O证据。\\n\\n{d.get('product_table','')}")
s=s.replace("{d['d']}\\n\\nD检索","{d['d']}\\n\\n{d.get('trade_table','| 记录ID/日期 | 主体与方向 | 品名/HS | 数量金额/单位 | 对手方/国家 | 来源及限制 |'+chr(10)+'| --- | --- | --- | --- | --- | --- |'+chr(10)+'| 未取得可核交易明细 | 未知 | 未知 | 未知 | 未知 | 见D证据 |')}\\n\\nD检索")
s=s.replace("path.write_text(text,encoding='utf-8');", "path.write_text(text,encoding='utf-8');")
(B/'_work/report.py').write_text(s,encoding='utf-8')
import importlib.util
sp=importlib.util.spec_from_file_location('batch',B/'_work/batch.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.init()
test={'中文':'原始返回测试','quotes':'" \\ $ ` \n','nested':[1,None,True]}
p=B/'logs/evidence/_storage-test.json';m.write(p,test);assert json.loads(p.read_text(encoding='utf-8'))==test
h=json.loads((R/'markets/BE/prospecting/BE-20261022-02/_work/market-handoff.json').read_text(encoding='utf-8'))
assert m.sha(R/'markets/BE/prospecting/BE-20261022-02/_work/market-handoff.json')=='120d75ceb30e8c92705ef41e4b7554343380a6e0c57cc5dc5aedcbaed4702fdb'
for x in h['artifacts']:assert m.sha(R/x['path'])==x['sha256']
for n in ['01_批次进度.md','02_批次总结.md','logs/checkpoint.json']:assert (B/n).read_text(encoding='utf-8')
print('INITIAL SAVED/READBACK; source fingerprints match; storage roundtrip passed')

