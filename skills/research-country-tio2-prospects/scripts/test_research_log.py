"""Offline regression tests; temporary batches never touch market data."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('research_log.py')
spec = importlib.util.spec_from_file_location('research_log', SCRIPT)
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.batch = Path(self.tmp.name) / '模拟批次'

    def send(self, op, **fields):
        return log.execute(self.batch, {'op': op, **fields})

    def init(self, pending=True):
        self.send('init', source='offline fixture; not market evidence', leads=[{
            'lead_id': 'TEST-L001', 'status': 'pending' if pending else 'valid',
            'stage': 'not_started' if pending else 'complete', 'reason': 'fixture'}])

    def begin(self, purpose='verify', **extra):
        return self.send('begin', kind='read', purpose=purpose,
                         target='https://example.invalid/company', tool='offline-fixture',
                         round_id='R01', lead_ids=['TEST-L001'] if purpose == 'verify' else [],
                         **extra)['action_id']

    def end(self, action_id, outcome='success', **extra):
        return self.send('end', action_id=action_id, outcome=outcome,
                         executed=True, summary='fixture result',
                         refs=['fixture:response-1'], error='timeout' if outcome == 'error' else '',
                         **extra)

    def test_pending_blocks_discovery_but_allows_verification(self):
        self.init()
        with self.assertRaisesRegex(ValueError, 'pending'):
            self.begin('discovery')
        action = self.begin()
        self.end(action)
        self.send('lead', lead_id='TEST-L001', status='valid', stage='complete', reason='four checks fixture')
        self.end(self.begin('discovery'))
        self.assertTrue(self.send('check')['discovery_allowed'])

    def test_unfinished_read_survives_restart_and_blocks_next_action(self):
        self.init(False)
        action = self.begin()
        self.assertEqual(self.send('check')['unfinished_actions'], [action])
        with self.assertRaisesRegex(ValueError, 'unfinished'):
            self.begin()
        self.send('end', action_id=action, outcome='interrupted', executed=None,
                  summary='process ended; invocation unknown', refs=[], error='no return captured')
        check = self.send('check')
        self.assertFalse(check['journal_complete'])
        self.assertEqual(check['unknown_execution'], [action])

    def test_error_retry_alternative_keep_separate_records(self):
        self.init()
        first = self.begin()
        self.end(first, 'error')
        second = self.begin(parent_action_id=first, relation='retry')
        self.end(second, 'error')
        third = self.send('begin', kind='read', purpose='verify', tool='offline-fixture',
                          round_id='R01', target='https://example.invalid/contact',
                          lead_ids=['TEST-L001'], parent_action_id=first, relation='alternative')['action_id']
        self.end(third)
        check = self.send('check')
        self.assertEqual(check['executed_reads'], 3)
        self.assertEqual(check['failed_actions'], [first, second])
        events = [json.loads(x) for x in (self.batch/'logs/events.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len([e for e in events if e['op'] == 'begin']), 3)
        self.assertTrue(all(e['recorded_at'].endswith('+08:00') for e in events))

    def test_unknown_leads_duplicate_init_and_terminal_new_lead_rejected(self):
        with self.assertRaises(ValueError):
            self.begin()
        self.init()
        with self.assertRaises(ValueError):
            self.init(False)
        with self.assertRaises(ValueError):
            self.send('lead', lead_id='TEST-L002', status='valid', stage='complete', reason='cannot skip pending')
        with self.assertRaises(ValueError):
            self.send('begin', kind='search', purpose='verify', target='test query',
                      tool='fixture', round_id='R01', lead_ids=['MISSING'])

    def test_failure_needs_error_and_duplicate_completion_rejected(self):
        self.init()
        action = self.begin()
        with self.assertRaises(ValueError):
            self.send('end', action_id=action, outcome='error', executed=True,
                      summary='failed', refs=[], error='')
        self.end(action)
        with self.assertRaises(ValueError):
            self.end(action)

    def test_truncated_journal_refuses_to_hide_corruption(self):
        self.init()
        journal = self.batch/'logs/events.jsonl'
        with journal.open('ab') as f:
            f.write(b'{"partial":')
        before = journal.read_bytes()
        with self.assertRaisesRegex(ValueError, 'corrupt'):
            self.begin()
        self.assertEqual(journal.read_bytes(), before)

    def test_lock_conflict_does_not_append(self):
        self.init()
        journal = self.batch/'logs/events.jsonl'
        before = journal.read_bytes()
        (self.batch/'logs/.writer.lock').write_text('other writer', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'lock'):
            self.begin()
        self.assertEqual(journal.read_bytes(), before)

    def test_cancelled_plan_is_not_counted_as_executed_search(self):
        self.init(False)
        action = self.send('begin', kind='search', purpose='discovery', target='fixture query',
                           tool='fixture', round_id='R01', lead_ids=[])['action_id']
        self.send('end', action_id=action, outcome='cancelled', executed=False,
                  summary='never invoked', refs=[], error='')
        self.assertEqual(self.send('check')['executed_searches'], 0)

    def test_cli_utf8_and_nonzero_for_incomplete_journal(self):
        self.init(False)
        self.begin()
        result = subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPT), '--batch',
                                 str(self.batch), '--check'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)['journal_complete'])

    def test_invalid_operation_type_returns_structured_cli_error(self):
        event = Path(self.tmp.name)/'bad-event.json'
        event.write_text('{"op":[]}', encoding='utf-8')
        result = subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPT), '--batch',
                                 str(self.batch), '--input', str(event)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1)
        self.assertIn('error', json.loads(result.stderr))
        self.assertFalse((self.batch/'logs/events.jsonl').exists())

    def next_round(self):
        return self.send('begin', kind='read', purpose='verify',
                         target='https://example.invalid/company', tool='fixture',
                         round_id='R02-CHECK', lead_ids=['TEST-L001'])

    def save_reports(self, seq=None):
        check = self.send('check')
        marker = json.dumps({'round_id': check['current_round'],
                             'through_seq': check['last_work_seq'] if seq is None else seq})
        names = ['01_候选客户总表.md', '02_证据与来源.md',
                 '03_搜索与覆盖记录.md', '04_批次复核与测试报告.md']
        for name in names:
            (self.batch/name).write_text('# Offline fixture report\n\n'
                'Only a software test; no company facts.\n\n'
                '<!-- research-checkpoint: ' + marker + ' -->\n', encoding='utf-8')

    def test_next_round_requires_saved_reports(self):
        self.init(False)
        self.end(self.begin())
        with self.assertRaisesRegex(ValueError, 'report checkpoint'):
            self.next_round()

    def test_checkpoint_rejects_missing_and_old_report_versions(self):
        self.init(False)
        self.end(self.begin())
        with self.assertRaises(ValueError):
            self.send('checkpoint', round_id='R01')
        self.save_reports(seq=1)
        with self.assertRaisesRegex(ValueError, 'marker'):
            self.send('checkpoint', round_id='R01')
        self.save_reports()
        self.send('checkpoint', round_id='R01')
        self.assertTrue(self.send('check')['reports_current'])
        self.next_round()

    def test_modified_report_blocks_transition(self):
        self.init(False)
        self.end(self.begin())
        self.save_reports()
        self.send('checkpoint', round_id='R01')
        with (self.batch/'02_证据与来源.md').open('a', encoding='utf-8') as f:
            f.write('Later edit not yet reviewed.\n')
        self.assertFalse(self.send('check')['reports_current'])
        with self.assertRaisesRegex(ValueError, 'report checkpoint'):
            self.next_round()

    def test_queue_change_invalidates_checkpoint_and_pending_can_be_saved(self):
        self.init(False)
        self.end(self.begin())
        self.save_reports()
        self.send('checkpoint', round_id='R01')
        self.send('lead', lead_id='TEST-L001', status='pending', stage='in_progress', reason='new conflict')
        with self.assertRaisesRegex(ValueError, 'report checkpoint'):
            self.next_round()
        self.save_reports()
        self.send('checkpoint', round_id='R01')
        self.assertTrue(self.send('check')['reports_current'])
        self.assertFalse(self.send('check')['discovery_allowed'])
        self.next_round()  # May continue verification with truthful pending reports.

    def test_delivery_check_requires_reports_from_latest_round(self):
        self.init(False)
        self.end(self.begin())
        self.save_reports()
        self.send('checkpoint', round_id='R01')
        action = self.next_round()['action_id']
        self.end(action)
        args = [sys.executable, '-X', 'utf8', str(SCRIPT), '--batch', str(self.batch), '--check-reports']
        result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)['reports_current'])
        self.save_reports()
        self.send('checkpoint', round_id='R02-CHECK')
        result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['reports_current'])

    def test_zero_action_stage_reports_can_be_checkpointed(self):
        self.init()
        for name in log.REPORTS:
            (self.batch/name).write_text('# Offline stage report\nNo tools available; pending remains.\n'
                '<!-- research-checkpoint: {"round_id":"R00","through_seq":1} -->\n', encoding='utf-8')
        self.send('checkpoint', round_id='R00')
        self.assertTrue(self.send('check')['reports_current'])
        self.assertEqual(self.send('check')['pending'], {'TEST-L001':'not_started'})


if __name__ == '__main__':
    unittest.main()
