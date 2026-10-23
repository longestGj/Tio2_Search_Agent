import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from test_support import *

CLI=Path(__file__).with_name('workflow_cli.py')

class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='完整流程');self.addCleanup(self.tmp.cleanup)
        self.p=Path(self.tmp.name);self.w=self.p/'markets/XX/workflows/XX-WF-20261022-01'
    def run_cli(self,c=None,flag=None,workflow=None):
        args=[sys.executable,'-X','utf8',str(CLI),'--project',str(self.p),'--workflow',str(workflow or self.w)]
        if c is not None:
            f=self.p/'输入.json';f.write_text(json.dumps(c,ensure_ascii=False),encoding='utf-8-sig');args+=['--input',str(f)]
        else:args+=[flag]
        r=subprocess.run(args,capture_output=True,text=True,encoding='utf8')
        self.assertTrue(r.stdout.strip(),r.stderr)
        return r.returncode,json.loads(r.stdout)
    def init(self,t=None):
        code,out=self.run_cli(cmd('init',task=t or make_task()));self.assertEqual(code,0,out)
    def send(self,c,expected=0):
        code,out=self.run_cli(c);self.assertEqual(code,expected,out);return out
    def test_bom_readonly_and_invalid_paths(self):
        self.init();files={p:p.read_bytes() for p in self.w.rglob('*') if p.is_file()}
        self.assertEqual(self.run_cli(flag='--check')[0],0)
        self.assertEqual(files,{p:p.read_bytes() for p in self.w.rglob('*') if p.is_file()})
        code,_=self.run_cli(cmd('init',task=make_task()),workflow=self.p.parent/'escape');self.assertEqual(code,1)
    def test_unknown_and_recovery(self):
        self.init();self.send(cmd('prepare',assignment=make_assignment()),2)
        self.assertEqual(self.run_cli(flag='--recover')[0],2)
        self.send(cmd('reconcile_dispatch',resolution='not_dispatched',evidence_ref='lookup:none'))
        self.assertEqual(self.run_cli(flag='--check')[0],0)
    def test_invalid_json_and_hash(self):
        self.init();f=self.p/'report.md';f.write_text('简短报告',encoding='utf8')
        a=make_assignment(input_artifacts=[dict(path='report.md',sha256='0'*64)])
        self.send(cmd('prepare',assignment=a),1)
        a['input_artifacts'][0]['path']='../outside';self.send(cmd('prepare',assignment=a),1)
        inp=self.p/'bad.json';inp.write_text('{bad',encoding='utf8')
        r=subprocess.run([sys.executable,str(CLI),'--project',str(self.p),'--workflow',str(self.w),'--input',str(inp)],capture_output=True,text=True)
        self.assertEqual(r.returncode,1)
    def test_projection_failure_blocks_dispatch_then_recover(self):
        import workflow_cli as cli
        from workflow_store import load_state,RecoveryRequired
        self.init()
        with patch.object(cli,'render_progress',side_effect=OSError('disk error')):
            with self.assertRaises(RecoveryRequired):cli.execute(self.p,self.w,cmd('pause'))
        with self.assertRaises(RecoveryRequired):load_state(self.w)
        self.assertEqual(self.run_cli(flag='--recover')[0],0)
        self.assertEqual(self.run_cli(flag='--check')[1]['status'],'paused')

    def test_snapshot_write_failure_is_recovery_error(self):
        import workflow_cli as cli
        import workflow_store as store
        self.init();original=store.atomic_json
        def fail(path,data):
            if Path(path).name=='state.json':raise OSError('disk full after event')
            return original(path,data)
        with patch.object(store,'atomic_json',side_effect=fail):
            with self.assertRaises(store.RecoveryRequired):cli.execute(self.p,self.w,cmd('pause'))
        self.assertEqual(self.run_cli(flag='--recover')[0],0)
    def test_three_company_simulation(self):
        t=make_task(order=['C1','C2','C3'],scope=dict(mode='explicit_ids',requested_count=3,baseline_ids=[],selected_ids=['C1','C2','C3'],source_artifacts=[]))
        # Three outcomes at the draft stage; missing contacts is verified separately.
        t['capabilities']['contacts']['available']=False
        t['entry_stage']='draft'
        self.init(t)
        a=make_assignment(stage='draft',customer_ids=['C1','C2','C3'])
        self.send(cmd('prepare',assignment=a),2);self.send(cmd('dispatched',assignment_id='A1',executor_ref='mock:1'))
        f=self.p/'草稿.txt';f.write_text('fictional draft',encoding='utf8');art=dict(path='草稿.txt',sha256=hashlib.sha256(f.read_bytes()).hexdigest())
        h=make_handoff(stage='draft',items=[item('C1','finish',None,draft_ids=['D1'],draft_files={'D1':'草稿.txt'},artifacts=[art]),item('C2','hold',None,artifacts=[art]),item('C3','revisit','draft',artifacts=[art])])
        out=self.send(cmd('receive',handoff=h));self.assertEqual(out['outcomes'],dict(active=1,draft_done=1,target_done=0,on_hold=1,ended=0,cancelled=0))
        self.assertFalse(out['all_drafts_done']);self.send(cmd('close'),1)
    def test_report_content_not_a_quality_gate(self):
        from workflow_cli import validate_artifacts
        for body in ['短','不同章节与长度'*100]:
            f=self.p/'report';f.write_text(body,encoding='utf8')
            self.assertEqual(validate_artifacts(self.p,[dict(path='report',sha256=hashlib.sha256(f.read_bytes()).hexdigest())]),[])

if __name__=='__main__':unittest.main()
