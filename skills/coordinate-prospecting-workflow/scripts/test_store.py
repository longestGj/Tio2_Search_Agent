import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from test_support import *
import workflow_store as store

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='调度测试');self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name);self.w=self.project/'markets/XX/workflows/XX-WF-20261022-01'
        store.commit_command(self.project,self.w,cmd('init',task=make_task()))

    def test_replay_and_readonly(self):
        c=cmd('prepare',assignment=make_assignment());s=store.commit_command(self.project,self.w,c)
        before=(self.w/'events.jsonl').read_bytes()
        self.assertEqual(store.commit_command(self.project,self.w,c),s)
        self.assertEqual((self.w/'events.jsonl').read_bytes(),before)
        self.assertEqual(store.load_state(self.w),s)
        self.assertTrue((self.w/'assignments/A1-r1.json').is_file())

    def test_alias_and_competing_workflow(self):
        p=self.project/'报告';p.mkdir()
        self.assertEqual(store.canonical_resource(self.project,'batch','报告'),store.canonical_resource(self.project,'batch',str(p).upper()))
        store.claim_resources(self.project,self.w,'A1',['company:XX:C1'])
        with self.assertRaises(ValueError): store.claim_resources(self.project,self.w.parent/'other','A2',['company:XX:C1'])
        with self.assertRaises(ValueError): store.release_resources(self.project,self.w,'A1','invented')

    def test_two_real_processes_one_owner(self):
        script="from pathlib import Path; from workflow_store import claim_resources; import sys; claim_resources(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3],['company:XX:C9'])"
        env=dict(os.environ,PYTHONPATH=str(Path(__file__).parent))
        ps=[subprocess.Popen([sys.executable,'-c',script,str(self.project),str(self.w.parent/f'w{i}'),f'A{i}'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for i in range(2)]
        codes=[]
        for p in ps: p.communicate();codes.append(p.returncode)
        self.assertEqual(sorted(codes),[0,1])

    def test_stale_lock_not_taken(self):
        lock=self.project/'.codex/workflow-runtime/.registry.lock';lock.write_text('old',encoding='utf8')
        with self.assertRaises(ValueError): store.commit_command(self.project,self.w,cmd('pause'))
        self.assertEqual(lock.read_text(),'old')

    def test_event_written_snapshot_failed_recovers(self):
        original=store.atomic_json
        def fail(path,data):
            if Path(path).name=='state.json': raise OSError('injected snapshot failure')
            original(path,data)
        with patch.object(store,'atomic_json',side_effect=fail):
            with self.assertRaises(OSError):store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))
        with self.assertRaises(store.RecoveryRequired):store.load_state(self.w)
        s=store.recover_workflow(self.project,self.w)
        self.assertEqual(s['dispatch'],'unknown')
        self.assertEqual(len((self.w/'events.jsonl').read_text().splitlines()),2)

    def test_missing_assignment_and_immutable_conflict(self):
        store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))
        path=self.w/'assignments/A1-r1.json';path.unlink()
        with self.assertRaises(store.RecoveryRequired):store.load_state(self.w)
        store.recover_workflow(self.project,self.w);self.assertTrue(path.exists())
        path.write_text('{}',encoding='utf8')
        with self.assertRaises(store.RecoveryRequired):store.recover_workflow(self.project,self.w)
        self.assertEqual(path.read_text(),'{}')

    def test_claim_before_event_failure_stays_claimed(self):
        with patch.object(store,'append_event',side_effect=OSError('injected journal failure')):
            with self.assertRaises(OSError):store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))
        registry=json.loads((self.project/'.codex/workflow-runtime/resource-owners.json').read_text())
        self.assertIn('company:XX:C1',registry)
        with self.assertRaises(ValueError):store.claim_resources(self.project,self.w.parent/'other','A2',['company:XX:C1'])
        store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))

    def test_truncated_journal_preserved(self):
        p=self.w/'events.jsonl';p.write_bytes(p.read_bytes()+b'{"broken"')
        before=p.read_bytes()
        with self.assertRaises(store.RecoveryRequired):store.recover_workflow(self.project,self.w)
        self.assertEqual(p.read_bytes(),before)

    def test_duplicate_sequence_preserved(self):
        p=self.w/'events.jsonl';p.write_bytes(p.read_bytes()*2);before=p.read_bytes()
        with self.assertRaises(store.RecoveryRequired):store.load_state(self.w)
        self.assertEqual(p.read_bytes(),before)

    def test_release_only_owned_assignment(self):
        store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))
        store.commit_command(self.project,self.w,cmd('reconcile_dispatch',resolution='not_dispatched',evidence_ref='lookup:none'))
        store.commit_command(self.project,self.w,cmd('prepare',command_id='p2',assignment=make_assignment(assignment_id='A2')))
        store.release_resources(self.project,self.w,'A1','lookup:none')
        registry=json.loads((self.project/'.codex/workflow-runtime/resource-owners.json').read_text())
        self.assertEqual(registry['company:XX:C1']['assignment_id'],'A2')
        self.assertTrue(list((self.w/'history').glob('*.json')))

    def test_claim_lost_requires_reconciliation_not_recovery_success(self):
        store.commit_command(self.project,self.w,cmd('prepare',assignment=make_assignment()))
        (self.project/'.codex/workflow-runtime/resource-owners.json').write_text('{}',encoding='utf8')
        with self.assertRaises(store.RecoveryRequired):store.recover_workflow(self.project,self.w)

    def test_recover_invalid_snapshot_preserves_original_bytes(self):
        p=self.w/'state.json';p.write_bytes(b'{invalid snapshot')
        s=store.recover_workflow(self.project,self.w)
        self.assertEqual(s['status'],'running')
        self.assertTrue(any(x.read_bytes()==b'{invalid snapshot' for x in (self.w/'history').glob('*.json')))

    @unittest.skipUnless(os.name=='nt','Windows path regression')
    def test_deep_directory_history_does_not_double_filename_length(self):
        p=self.project/('p'*85);w=p/'markets/XX/workflows/XX-WF-20261022-01'
        store.commit_command(p,w,cmd('init',task=make_task()))
        s=store.commit_command(p,w,cmd('pause'))
        self.assertEqual(s['status'],'paused')

    def test_init_retry_is_idempotent(self):
        before=(self.w/'events.jsonl').read_bytes()
        s=store.commit_command(self.project,self.w,cmd('init',task=make_task()))
        self.assertEqual(s['status'],'running')
        self.assertEqual((self.w/'events.jsonl').read_bytes(),before)

if __name__=='__main__':unittest.main()
