import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from test_support import *
from workflow_model import apply_command,new_state

def documented(**overrides):
    return item(artifacts=[dict(path='report.md',sha256='0'*64)],**overrides)

class ReviewRegressions(unittest.TestCase):
    def test_budget_final_resolves_only_own_uncertainty(self):
        b=dict(budget_id='q',stage='research',unit='queries',limit=10,used=0,unknown=False,authorization_ref='user:cap')
        s=started(make_task(budgets=[b]),make_assignment(budget_reservations={'q':5}))
        s=receive(s,make_handoff(released=False,uncertainty=['q'],items=[documented()]))
        s=receive(s,make_handoff(handoff_id='H2',budget_used={'q':2},items=[documented(route='revisit',stage='research')]),command_id='final')
        self.assertFalse(s['task']['budgets'][0]['unknown'])
        s=apply_command(s,cmd('reopen',customer_id='C1',evidence_ref='new:report'))
        s=apply_command(s,cmd('prepare',command_id='again',assignment=make_assignment(assignment_id='A2',budget_reservations={'q':3})))
        self.assertEqual(s['task']['budgets'][0]['used'],2)

    def test_baseline_budget_reconciliation_keeps_used_and_cap(self):
        b=dict(budget_id='q',stage='research',unit='queries',limit=10,used=2,unknown=True,authorization_ref='user:cap')
        s=new_state(make_task(budgets=[b]))
        for used,ref in [(1,'proof'),(3,'')]:
            with self.assertRaises(ValueError):apply_command(s,cmd('reconcile_budget',budget_id='q',used=used,resolved_assignments=['baseline'],evidence_ref=ref))
        s=apply_command(s,cmd('reconcile_budget',budget_id='q',used=3,resolved_assignments=['baseline'],evidence_ref='actual:ledger'))
        self.assertEqual(s['task']['budgets'][0]['limit'],10)
        self.assertEqual(s['task']['budgets'][0]['used'],3)
        self.assertFalse(s['task']['budgets'][0]['unknown'])

    def test_partial_discovery_can_fill_original_allowance(self):
        t=make_task(entry_stage='market',order=[],scope=dict(mode='discovery_new',requested_count=5,baseline_ids=['OLD'],selected_ids=[],source_artifacts=[]))
        s=started(t,make_assignment(stage='market',customer_ids=[]))
        s=receive(s,make_handoff(stage='market',items=[documented(cid='N1',stage='research')]))
        s=apply_command(s,cmd('prepare',command_id='discover-more',assignment=make_assignment(assignment_id='A2',stage='market',customer_ids=[])))
        for ids in [['OLD'],['N1'],['N2','N3','N4','N5','N6']]:
            with self.assertRaises(ValueError):receive(s,make_handoff(handoff_id='H2',assignment_id='A2',stage='market',items=[documented(cid=c,stage='research') for c in ids]),command_id='bad')
        s=receive(s,make_handoff(handoff_id='H2',assignment_id='A2',stage='market',items=[documented(cid=c,stage='research') for c in ['N2','N3','N4','N5']]),command_id='more')
        self.assertEqual(list(s['companies']),['N1','N2','N3','N4','N5'])
        self.assertEqual(s['companies']['N1']['stage'],'research')

    def test_completed_requires_artifact_but_blocked_may_have_none(self):
        with self.assertRaises(ValueError):receive(started(),make_handoff(items=[item(artifacts=[])]))
        s=receive(started(),make_handoff(items=[item(route='hold',stage=None,execution_status='blocked',artifacts=[])]))
        self.assertEqual(s['companies']['C1']['outcome'],'on_hold')

    def test_cli_accepted_retry_and_historical_version_skip_new_file_check(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);w=p/'markets/XX/workflows/XX-WF-20261022-01';f=p/'report.md';f.write_text('v1')
            from workflow_cli import execute
            execute(p,w,cmd('init',task=make_task()));execute(p,w,cmd('prepare',assignment=make_assignment()));execute(p,w,cmd('dispatched',assignment_id='A1',executor_ref='real:fixture'))
            h=make_handoff(items=[item(artifacts=[dict(path='report.md',sha256=hashlib.sha256(f.read_bytes()).hexdigest())])]);c=cmd('receive',handoff=h)
            execute(p,w,c);f.write_text('v2')
            s=execute(p,w,c);self.assertEqual(s['companies']['C1']['stage'],'contacts')
            s=execute(p,w,cmd('receive',command_id='duplicate-handoff',handoff=h));self.assertEqual(s['companies']['C1']['stage'],'contacts')
            s=execute(p,w,cmd('receive',command_id='old',handoff=dict(h,handoff_id='old',revision=0)));self.assertEqual(s['companies']['C1']['stage'],'contacts')

    def test_check_reports_missing_active_resource(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);w=p/'markets/XX/workflows/XX-WF-20261022-01'
            from workflow_cli import execute
            execute(p,w,cmd('init',task=make_task()));execute(p,w,cmd('prepare',assignment=make_assignment()));execute(p,w,cmd('dispatched',assignment_id='A1',executor_ref='real:fixture'))
            (p/'.codex/workflow-runtime/resource-owners.json').write_text('{}')
            r=subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).with_name('workflow_cli.py')),'--project',str(p),'--workflow',str(w),'--check'],capture_output=True,text=True,encoding='utf8')
            self.assertEqual(r.returncode,2,r.stdout)
            self.assertTrue(json.loads(r.stdout)['technical_issues'])

if __name__=='__main__':unittest.main()
