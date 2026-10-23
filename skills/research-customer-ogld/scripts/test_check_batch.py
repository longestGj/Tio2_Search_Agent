"""Offline structural tests; fixtures are fictional, not customer research."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('check_batch', Path(__file__).with_name('check_batch.py'))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BatchChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name) / '中文测试批次'
        (self.batch / 'logs').mkdir(parents=True)
        self.source = self.batch / 'source.md'
        self.source.write_text('Fictional frozen input', encoding='utf-8')
        self.state = {
            'schema': 1, 'batch_id': 'XX-DD-TEST', 'country': 'XX',
            'sources': [{'path': str(self.source), 'sha256': MODULE.digest(self.source)}],
            'source_changes': [], 'skill_version': 'OGLD V1.1/local-batch v1.0',
            'skill_commit': 'aa99ddf7583dee0cd7b6e8a472aa7b65aa802634',
            'budget': {'search_limit': 8, 'search_used': 0,
                       'active_minutes_limit': None, 'active_minutes_used': None},
            'items': [self.item('XX-C001'), self.item('XX-C002')]
        }
        self.events = []

    def item(self, cid):
        return {'customer_id': cid, 'company_name': 'Fictional ' + cid,
                'country': 'XX', 'source_status': 'valid', 'source_locator': 'source.md record ' + cid,
                'status': 'queued', 'mode': None, 'stage': 'intake', 'next_step': 'review identity',
                'block_reason': '', 'report_path': None, 'report_sha256': None}

    def complete(self, index=0, mode='new'):
        item = self.state['items'][index]
        report = self.batch / (item['customer_id'] + '.md')
        report.write_text('# Fictional report\n客户 ID：' + item['customer_id'] + '\n'
                          + '\n'.join('## ' + h + '\nOffline fixture.' for h in MODULE.HEADINGS), encoding='utf-8')
        item.update(status='completed', mode=mode, report_path=str(report), report_sha256=MODULE.digest(report),
                    identity_basis='Fictional source ID + country + registry match', checked_at='2026-10-22T10:00:00+08:00',
                    original_date='2025-01-01' if mode != 'new' else None,
                    action='先补充核实', next_step='None', stage='review')
        if mode != 'new':
            item.update(original_report_path=str(report), original_report_sha256=MODULE.digest(report))
        return report

    def run_check(self):
        (self.batch / 'logs/checkpoint.json').write_text(json.dumps(self.state, ensure_ascii=False), encoding='utf-8')
        (self.batch / 'logs/actions.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in self.events), encoding='utf-8')
        return MODULE.check_batch(self.batch)

    def test_objective_policy_accepts_evidence_based_exclusion(self):
        self.complete()
        self.state['items'][0].update(research_policy='objective-evidence-v1',
                                     action='排除开发', exclusion_reason='仅施工业务，来源O01',
                                     exclusion_evidence=['O01'])
        self.assertEqual(self.run_check()['errors'], [])

    def test_objective_policy_rejects_legacy_final_actions(self):
        self.complete()
        self.state['items'][0]['research_policy'] = 'objective-evidence-v1'
        for action in ('先补充核实', '暂缓开发', '不匹配当前产品'):
            self.state['items'][0]['action'] = action
            self.assertIn('objective policy', '\n'.join(self.run_check()['errors']))

    def test_objective_exclusion_requires_reason_and_evidence(self):
        self.complete()
        item = self.state['items'][0]
        item.update(research_policy='objective-evidence-v1', action='排除开发')
        self.assertIn('exclusion', '\n'.join(self.run_check()['errors']))
        item['exclusion_reason'] = '纯施工业务'
        self.assertIn('exclusion', '\n'.join(self.run_check()['errors']))

    def test_objective_policy_keeps_unknown_information(self):
        self.complete()
        self.state['items'][0].update(research_policy='objective-evidence-v1',
                                     action='继续开发', next_step='采购量和联系人未知；交接后续')
        self.assertEqual(self.run_check()['errors'], [])

    def test_legacy_completion_is_identified_without_rewriting(self):
        self.complete()
        result = self.run_check()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result.get('legacy_conclusion_ids'), ['XX-C001'])

    def begin(self, kind='read'):
        return {'event': 'begin', 'action_id': 'A01', 'customer_id': 'XX-C001', 'dimension': 'O',
                'kind': kind, 'target': 'https://fixture.invalid/', 'tool': 'offline.fixture',
                'recorded_at': '2026-10-22T10:00:00+08:00'}

    def end(self, executed=True, outcome='success'):
        return {'event': 'end', 'action_id': 'A01', 'recorded_at': '2026-10-22T10:01:00+08:00',
                'executed': executed, 'outcome': outcome, 'summary': 'Fixture only',
                'refs': ['fixture:1'], 'error': 'interrupted' if outcome == 'interrupted' else ''}

    def test_mixed_reuse_and_new_and_next(self):
        self.complete(mode='reused')
        result = self.run_check()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['next_customer_id'], 'XX-C002')
        self.assertEqual(result['counts']['reused'], 1)
        self.complete(1)
        result = self.run_check()
        self.assertTrue(result['all_completed'])
        self.assertEqual(result['counts']['new'], 1)

    def test_duplicate_and_country_mismatch(self):
        self.state['items'][1]['customer_id'] = 'XX-C001'
        self.state['items'][1]['country'] = 'YY'
        errors = '\n'.join(self.run_check()['errors'])
        self.assertIn('duplicate', errors)
        self.assertIn('country', errors)

    def test_multiple_in_progress_and_skipped_queued(self):
        for i in self.state['items']:
            i['status'] = 'in_progress'
        self.assertTrue(self.run_check()['errors'])
        self.state['items'][0]['status'] = 'queued'
        self.assertIn('queued predecessor', '\n'.join(self.run_check()['errors']))

    def test_missing_report_and_changed_hash(self):
        report = self.complete()
        report.write_text('changed', encoding='utf-8')
        self.assertIn('hash', '\n'.join(self.run_check()['errors']))
        report.unlink()
        self.assertIn('missing report', '\n'.join(self.run_check()['errors']))

    def test_missing_heading_and_customer_identity(self):
        report = self.complete()
        report.write_text(report.read_text(encoding='utf-8').replace('## 5 D 海关', '## unrelated').replace('XX-C001', 'XX-C0010'), encoding='utf-8')
        self.state['items'][0]['report_sha256'] = MODULE.digest(report)
        errors = '\n'.join(self.run_check()['errors'])
        self.assertIn('heading', errors)
        self.assertIn('customer ID', errors)

    def test_legacy_equivalent_section_titles_allow_reuse(self):
        report = self.complete(mode='reused')
        body = report.read_text(encoding='utf-8')
        alternatives = ['经确认的公司官网', '1. 核心结论', '2. O｜官网调查',
                        '3. G｜公开信息与主体交叉核实', '4. L｜LinkedIn与联系人线索',
                        '5. D｜海关与贸易数据', '6. 商业判断与产品匹配',
                        '7. 下一步行动（最多三项）', '8. 证据目录与所有信息来源网址']
        for old, new in zip(MODULE.HEADINGS, alternatives):
            body = body.replace('## ' + old, '## ' + new)
        report.write_text(body, encoding='utf-8')
        item = self.state['items'][0]
        item['report_sha256'] = item['original_report_sha256'] = MODULE.digest(report)
        self.assertEqual(self.run_check()['errors'], [])

    def test_reused_report_must_be_unchanged(self):
        report = self.complete(mode='reused')
        report.write_text(report.read_text(encoding='utf-8') + '\nNew evidence', encoding='utf-8')
        self.state['items'][0]['report_sha256'] = MODULE.digest(report)
        self.assertIn('reused hash', '\n'.join(self.run_check()['errors']))

    def test_supplement_needs_snapshot(self):
        report = self.complete(mode='supplemented')
        self.assertIn('snapshot', '\n'.join(self.run_check()['errors']))
        snapshot = self.batch / 'old.md'
        snapshot.write_bytes(report.read_bytes())
        self.state['items'][0]['history_path'] = str(snapshot)
        self.assertEqual(self.run_check()['errors'], [])

    def test_snapshot_cannot_be_current_report_or_alias(self):
        report = self.complete(mode='supplemented')
        self.state['items'][0]['history_path'] = str(report)
        self.assertIn('independent snapshot', '\n'.join(self.run_check()['errors']))
        alias = self.batch / 'alias.md'
        try:
            alias.hardlink_to(report)
        except OSError:
            return  # Same-path assertion still runs on filesystems without hardlinks.
        self.state['items'][0]['history_path'] = str(alias)
        self.assertIn('independent snapshot', '\n'.join(self.run_check()['errors']))

    def test_open_action_and_unknown_read_do_not_consume_search(self):
        self.state['items'][0]['status'] = 'in_progress'
        self.events = [self.begin()]
        result = self.run_check()
        self.assertEqual(result['exit_code'], 2)
        self.assertIsNone(result['next_customer_id'])
        self.events.append(self.end(None, 'interrupted'))
        result = self.run_check()
        self.assertEqual(result['search_used_confirmed'], 0)
        self.assertEqual(result['search_remaining'], 8)
        self.assertEqual(result['exit_code'], 2)

    def test_search_budget_matches_actual_execution(self):
        self.events = [self.begin('search'), self.end()]
        self.assertIn('search_used', '\n'.join(self.run_check()['errors']))
        self.state['budget'].update(search_used=1, search_limit=1)
        result = self.run_check()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['search_remaining'], 0)
        self.assertFalse(result['new_search_allowed'])

    def test_invalid_end_and_duplicate_end(self):
        self.events = [self.begin(), self.end(False, 'success')]
        self.assertTrue(self.run_check()['errors'])
        self.events = [self.begin(), self.end(), self.end()]
        self.assertIn('duplicate end', '\n'.join(self.run_check()['errors']))

    def test_reconcile_interrupted_without_faking_new_call(self):
        self.events = [self.begin('search'), self.end(None, 'interrupted')]
        reconciliation = self.end()
        reconciliation.update(event='reconcile', reason='Recovered original tool return')
        self.events.append(reconciliation)
        self.state['budget']['search_used'] = 1
        result = self.run_check()
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['search_used_confirmed'], 1)
        self.assertEqual(result['reconciled_actions'], ['A01'])
        self.events.append(reconciliation)
        self.assertTrue(self.run_check()['errors'])

    def test_reconciliation_cannot_erase_confirmed_execution(self):
        self.events = [self.begin('search'), self.end(True, 'interrupted')]
        cancelled = self.end(False, 'cancelled')
        cancelled.update(event='reconcile', reason='Claimed not executed')
        self.events.append(cancelled)
        self.state['budget'].update(search_limit=1, search_used=0)
        result = self.run_check()
        self.assertEqual(result['exit_code'], 1)
        self.assertEqual(result['search_used_confirmed'], 1)
        self.assertFalse(result['new_search_allowed'])

    def test_missing_source_hash_never_passes(self):
        for value in (None, '', 'invalid', 'a' * 63):
            with self.subTest(value=value):
                self.state['sources'] = [{'path': 'missing-input.md', 'sha256': value}]
                result = self.run_check()
                self.assertEqual(result['exit_code'], 1)
                self.assertFalse(result['new_search_allowed'])
        self.state['sources'] = [{'path': 'missing-input.md'}]
        self.assertEqual(self.run_check()['exit_code'], 1)

    def test_changed_source_requires_acknowledgment(self):
        self.source.write_text('Added C005', encoding='utf-8')
        self.assertEqual(self.run_check()['exit_code'], 2)
        self.state['source_changes'] = [{'path': str(self.source), 'observed_sha256': MODULE.digest(self.source),
                                         'resolution': 'Frozen queue unchanged; C005 not admitted'}]
        self.assertEqual(self.run_check()['exit_code'], 0)
        self.assertEqual(len(self.state['items']), 2)

    def test_blocked_moves_forward_but_does_not_finish(self):
        self.state['items'][0].update(status='blocked', block_reason='identity unresolved', next_step='registry access')
        result = self.run_check()
        self.assertEqual(result['next_customer_id'], 'XX-C002')
        self.assertFalse(result['all_completed'])

    def test_malformed_json_and_wrong_types(self):
        (self.batch / 'logs/checkpoint.json').write_text('{broken', encoding='utf-8')
        self.assertEqual(MODULE.check_batch(self.batch)['exit_code'], 1)
        self.state['items'] = 'bad'
        self.assertEqual(self.run_check()['exit_code'], 1)
        self.state['items'] = [None]
        self.assertEqual(self.run_check()['exit_code'], 1)

    def test_unresolved_input_needs_explicit_scope_reason(self):
        self.state['items'][0]['source_status'] = 'unresolved'
        self.assertTrue(self.run_check()['errors'])
        self.state['items'][0]['scope_exception'] = 'Explicit user requested this company'
        self.assertEqual(self.run_check()['errors'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
