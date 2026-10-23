"""Offline invariants; fictional people, no Apollo calls or charges."""
import copy
import importlib.util
import json
import hashlib
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('contacts_check', Path(__file__).with_name('check_batch.py'))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_ledger(existing=0, spent='0', held='0'):
    ledger = {'schema': 1, 'company_key': 'XX:company-a', 'customer_ids': ['XX-C001'],
              'aliases': [], 'workflow_id': 'contacts-a', 'credit_limit': '3', 'contact_limit': 3,
              'baseline_evidence': {'confirmed': True, 'source_ref': 'fictional baseline'},
              'history': [], 'contacts': [], 'operations': []}
    for i in range(existing):
        ledger['contacts'].append({'person_key': f'old-{i}', 'email': f'old{i}@example.invalid',
                                   'kind': 'named', 'source_ref': 'fictional history', 'date': '2026-10-22'})
    for opid, amount, status in [('spent', spent, 'settled'), ('held', held, 'unknown')]:
        if amount != '0':
            ledger['operations'].append({'operation_id': opid, 'batch_id': 'XX-OLD',
                                        'kind': 'organization_search', 'max_credits': amount,
                                        'actual_credits': amount if status == 'settled' else None,
                                        'status': status, 'evidence_ref': 'fictional receipt'})
    return ledger


def make_selection(new=0, reverify=0, primary_available=True):
    people = []
    for mode, count in [('new', new), ('reverify', reverify)]:
        for i in range(count):
            key = f'new-{i}' if mode == 'new' else f'old-{i}'
            people.append({'candidate_id': f'C-{key}', 'person_key': key, 'apollo_id': f'id-{key}',
                           'source_ref': 'fictional current search', 'group': 'primary' if primary_available else 'secondary',
                           'mode': mode, 'max_credits': '1', 'operation_id': None,
                           'has_email': True,
                           'email_evidence': {'path': 'search.json', 'sha256': '0' * 64},
                           'identity_basis': 'fictional employer', 'relevance_basis': 'fictional role'})
    return {'primary_available': primary_available, 'primary_basis': 'fictional coverage', 'people': people}


class BudgetChecks(unittest.TestCase):
    def test_research_public_people_do_not_consume_selected_slots(self):
        ledger = make_ledger(existing=8)
        for c in ledger['contacts']:
            c.update(counts_toward_limit=False, scope_basis='Public research evidence; not selected')
        result = MODULE.validate_ledger(ledger)
        self.assertEqual(result['existing_contacts'], 0)
        self.assertEqual(result['new_slots'], 3)
        self.assertFalse(result['warnings'])
        self.assertFalse(MODULE.validate_selection(ledger, make_selection(new=3))['errors'])

    def test_research_person_promoted_to_selected_still_counts(self):
        ledger = make_ledger(existing=4)
        for c in ledger['contacts']:
            c.update(counts_toward_limit=False, scope_basis='Public research evidence; not selected')
        self.assertFalse(MODULE.validate_selection(ledger, make_selection(reverify=3))['errors'])
        self.assertTrue(MODULE.validate_selection(ledger, make_selection(reverify=4))['errors'])

    def test_paid_person_cannot_be_exempted_as_research(self):
        ledger = make_ledger(existing=3)
        for c in ledger['contacts']:
            c.update(counts_toward_limit=False, scope_basis='Incorrect claimed research scope')
            ledger['operations'].append(dict(operation_id=c['person_key'], batch_id='OLD',
                kind='people_enrichment', person_key=c['person_key'], max_credits='1',
                actual_credits='1', status='settled', evidence_ref='actual paid history'))
        self.assertEqual(MODULE.validate_ledger(ledger)['existing_contacts'], 3)

    def test_scope_exemption_requires_basis(self):
        ledger = make_ledger(existing=1)
        ledger['contacts'][0]['counts_toward_limit'] = False
        self.assertTrue(MODULE.validate_ledger(ledger)['errors'])

    def test_paid_selection_requires_literal_true_email_flag(self):
        for value in [False, None, 'true', 'false', 1, 0, 'unknown']:
            with self.subTest(value=value):
                selection = make_selection(new=1)
                selection['people'][0]['has_email'] = value
                self.assertIn('has_email must be true', MODULE.validate_selection(make_ledger(), selection)['errors'])
        selection['people'][0].pop('has_email')
        self.assertIn('has_email must be true', MODULE.validate_selection(make_ledger(), selection)['errors'])

    def test_paid_selection_requires_email_evidence_fingerprint(self):
        for value in [None, {}, {'path': 'search.json', 'sha256': 'bad'}]:
            selection = make_selection(new=1)
            selection['people'][0]['email_evidence'] = value
            self.assertIn('email evidence path and SHA-256 required', MODULE.validate_selection(make_ledger(), selection)['errors'])

    def test_reverification_cannot_bypass_email_availability(self):
        selection = make_selection(reverify=1)
        selection['people'][0]['has_email'] = False
        self.assertIn('has_email must be true', MODULE.validate_selection(make_ledger(existing=1), selection)['errors'])

    def test_confirmed_and_unknown_costs_reduce_available(self):
        result = MODULE.validate_ledger(make_ledger(spent='1', held='1'))
        self.assertEqual((result['spent'], result['reserved'], result['remaining']), ('1', '1', '1'))
        self.assertTrue(result['warnings'])

    def test_company_query_leaves_two_credits(self):
        ledger = make_ledger(spent='1')
        self.assertFalse(MODULE.validate_selection(ledger, make_selection(new=2))['errors'])
        self.assertTrue(MODULE.validate_selection(ledger, make_selection(new=3))['errors'])

    def test_unknown_charge_cannot_be_retried_on_fresh_budget(self):
        self.assertTrue(MODULE.validate_selection(make_ledger(held='3'), make_selection(new=1))['errors'])

    def test_old_contacts_and_reverification_have_different_limits(self):
        ledger = make_ledger(existing=2)
        result = MODULE.validate_selection(ledger, make_selection(new=1, reverify=1))
        self.assertFalse(result['errors'])
        self.assertEqual((result['new_count'], result['reverify_count'], result['max_credits']), (1, 1, '2'))
        self.assertTrue(MODULE.validate_selection(ledger, make_selection(new=2))['errors'])

    def test_full_or_legacy_excess_stops_new_contacts(self):
        for count in [3, 4]:
            self.assertTrue(MODULE.validate_selection(make_ledger(existing=count), make_selection(new=1))['errors'])
        self.assertTrue(MODULE.validate_ledger(make_ledger(existing=4))['warnings'])

    def test_public_address_does_not_take_named_slot(self):
        ledger = make_ledger(existing=2)
        ledger['contacts'].append({'person_key': 'public', 'kind': 'public', 'email': 'info@example.invalid',
                                   'source_ref': 'fictional official', 'date': '2026-10-22'})
        self.assertEqual(MODULE.validate_ledger(ledger)['new_slots'], 1)

    def test_secondary_group_cannot_top_up_primary(self):
        selection = make_selection(new=2)
        selection['people'][1]['group'] = 'secondary'
        self.assertTrue(MODULE.validate_selection(make_ledger(), selection)['errors'])
        self.assertFalse(MODULE.validate_selection(make_ledger(), make_selection(new=2, primary_available=False))['errors'])

    def test_duplicate_person_or_candidate_not_extra_slot(self):
        selection = make_selection(new=1)
        selection['people'].append(copy.deepcopy(selection['people'][0]))
        self.assertTrue(MODULE.validate_selection(make_ledger(), selection)['errors'])

    def test_reverify_must_refer_to_existing_person(self):
        self.assertTrue(MODULE.validate_selection(make_ledger(), make_selection(reverify=1))['errors'])

    def test_settled_match_without_email_still_costs(self):
        ledger = make_ledger(spent='1')
        ledger['operations'][0]['outcome'] = 'matched_no_email'
        self.assertEqual(MODULE.validate_ledger(ledger)['remaining'], '2')
        ledger['operations'][0].update(actual_credits='0', outcome='unmatched')
        self.assertEqual(MODULE.validate_ledger(ledger)['remaining'], '3')
        ledger['operations'][0]['evidence_ref'] = ''
        self.assertTrue(MODULE.validate_ledger(ledger)['errors'])

    def test_duplicate_or_excess_settlement_rejected(self):
        ledger = make_ledger(spent='1')
        ledger['operations'].append(copy.deepcopy(ledger['operations'][0]))
        self.assertTrue(MODULE.validate_ledger(ledger)['errors'])
        ledger = make_ledger(spent='1')
        ledger['operations'][0]['actual_credits'] = '2'
        self.assertTrue(MODULE.validate_ledger(ledger)['errors'])

    def test_invalid_money_and_types_are_errors(self):
        for value in ['NaN', 'Infinity', '-1', True, 1, None, '']:
            ledger = make_ledger(spent='1')
            ledger['operations'][0]['actual_credits'] = value
            self.assertTrue(MODULE.validate_ledger(ledger)['errors'], repr(value))
        for value in [None, [], 'bad', {'operations': 1}]:
            self.assertTrue(MODULE.validate_ledger(value)['errors'])

    def test_unknown_baseline_is_not_zero_cost(self):
        ledger = make_ledger()
        ledger['baseline_evidence']['confirmed'] = False
        self.assertIsNone(MODULE.validate_ledger(ledger)['remaining'])
        self.assertTrue(MODULE.validate_selection(ledger, make_selection(new=1))['errors'])

    def test_evidence_and_scope_are_required(self):
        selection = make_selection(new=1)
        selection['people'][0]['relevance_basis'] = ''
        self.assertTrue(MODULE.validate_selection(make_ledger(), selection)['errors'])
        ledger = make_ledger()
        ledger['credit_limit'] = '4'
        self.assertTrue(MODULE.validate_ledger(ledger)['errors'])


ORG = ['元信息', '公司主体及关系', '检索日志及覆盖', '全量人员台账', '职能分布与管理线索', '自动选择、名额与执行', '冲突、来源与更新']
EMAIL = ['元信息、持续授权与执行范围', '执行摘要', '邮箱总表', '人员详情与交接', '来源、日志与验收']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class BatchChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name) / '中文批次'
        self.batch.mkdir()
        (self.batch / 'logs').mkdir()
        (self.batch / 'source.md').write_text('fictional input', encoding='utf-8')
        (self.batch / 'skill.md').write_text('fictional skill version', encoding='utf-8')
        (self.batch / 'receipt.json').write_text('{"fictional":true}', encoding='utf-8')
        for name in ['01_批次进度.md', '02_批次总结.md']:
            (self.batch / name).write_text('虚构离线阶段记录', encoding='utf-8')
        self.ledger = make_ledger()
        self.write_json('anchor.json', self.ledger)
        reports = {}
        for kind, headings in [('organization', ORG), ('email', EMAIL)]:
            path = self.batch / (kind + '.md')
            path.write_text('# 虚构报告\n客户ID：XX-C001\n' + '\n'.join('## ' + h + '\n虚构记录。' for h in headings), encoding='utf-8')
            reports[kind] = {'path': path.name, 'sha256': sha(path)}
        self.state = {'schema': 1, 'batch_id': 'XX-TEST', 'phase': 'research',
                      'sources': [{'path': 'source.md', 'sha256': sha(self.batch / 'source.md')}],
                      'skill_sources': [{'path': 'skill.md', 'sha256': sha(self.batch / 'skill.md')}],
                      'source_changes': [], 'approvals': [], 'next_step': 'prepare', 'items': [
                          {'customer_id': 'XX-C001', 'country': 'XX', 'company_key': 'XX:company-a',
                           'ledger_path': 'ledger.json', 'ledger_anchor': {'path': 'anchor.json', 'sha256': sha(self.batch / 'anchor.json')},
                           'status': 'waiting_confirmation', 'stage': 'selected', 'selection': make_selection(new=1),
                           'reports': reports, 'next_step': 'confirm'}]}
        self.events = []
        self.search_people = [{'id': f'id-{mode}-{i}', 'has_email': True}
                              for mode in ('new', 'old') for i in range(3)]
        self.set_search_evidence({'people': self.search_people})

    def set_search_evidence(self, value):
        self.write_json('search.json', value)
        self.state['items'][0]['selection']['people'][0]['email_evidence'] = {
            'path': 'search.json', 'sha256': sha(self.batch / 'search.json')}

    def test_search_evidence_must_confirm_same_id_with_email(self):
        for people in [[], [{'id': 'other', 'has_email': True}],
                       [{'id': 'id-new-0', 'has_email': False}],
                       [{'id': 'id-new-0'}], [{'id': 'id-new-0', 'has_email': 'true'}],
                       [{'id': 'id-new-0', 'has_email': True}, {'id': 'id-new-0', 'has_email': False}]]:
            with self.subTest(people=people):
                self.set_search_evidence({'people': people})
                result = self.check()
                self.assertEqual(result['exit_code'], 1, result)
                self.assertTrue(any('search evidence must confirm has_email=true' in e for e in result['errors']))

    def test_email_evidence_missing_or_changed_blocks_selection(self):
        (self.batch / 'search.json').unlink()
        self.assertEqual(self.check()['exit_code'], 1)
        self.set_search_evidence({'people': self.search_people})
        self.write_json('search.json', {'people': []})
        self.assertEqual(self.check()['exit_code'], 1)

    def test_search_payload_supports_mcp_envelopes(self):
        for value in [{'content': [{'type': 'text', 'text': json.dumps({'people': self.search_people})}]},
                      {'structuredContent': {'people': self.search_people}}]:
            self.set_search_evidence(value)
            self.assertEqual(self.check()['exit_code'], 0)

    def test_paid_approval_does_not_bypass_missing_email(self):
        self.paid()
        self.state['items'][0]['selection']['people'][0]['has_email'] = False
        self.assertEqual(self.check()['exit_code'], 1)

    def test_primary_with_no_email_does_not_allow_secondary_top_up(self):
        selection = self.state['items'][0]['selection']
        selection['people'][0]['group'] = 'secondary'
        self.assertEqual(self.check()['exit_code'], 1)
        selection['people'] = []
        self.state['items'][0].update(status='completed', completion_basis='suitable primary exists but has no email; preserved in organization report')
        self.state['phase'] = 'closed'
        self.assertEqual(self.check()['exit_code'], 0)

    def write_json(self, path, value):
        (self.batch / path).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8-sig')

    def save(self):
        self.write_json('ledger.json', self.ledger)
        self.write_json('logs/checkpoint.json', self.state)
        (self.batch / 'logs/actions.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in self.events), encoding='utf-8')

    def check(self):
        self.save()
        return MODULE.check_batch(self.batch)

    def paid(self, outcome='success'):
        p = self.state['items'][0]['selection']['people'][0]
        p['operation_id'] = 'op1'
        self.ledger['operations'] = [{'operation_id': 'op1', 'batch_id': 'XX-TEST', 'kind': 'people_enrichment',
                                      'person_key': p['person_key'], 'max_credits': '1', 'actual_credits': '1',
                                      'status': 'settled', 'evidence_ref': 'receipt.json'}]
        allocation = {'company_key': 'XX:company-a', 'person_key': p['person_key'], 'apollo_id': p['apollo_id'], 'max_credits': '1'}
        self.state['approvals'] = [{'approval_id': 'approved1', 'kind': 'people_enrichment', 'confirmed': True,
                                   'user_confirmation_ref': 'fictional user approval', 'confirmation_text': 'fictional confirmation',
                                   'balance_snapshot': 'fictional balance 10', 'max_credits': '1', 'allocations': [allocation]}]
        self.events = [{'event': 'begin', 'action_id': 'a1', 'recorded_at': '2026-10-22T10:00:00+08:00',
                        'tool': 'offline.people', 'kind': 'people_enrichment', 'target': 'fictional person',
                        'approval_id': 'approved1', 'params': {'reveal_personal_emails': False, 'reveal_phone_number': False},
                        'allocations': [dict(allocation, operation_id='op1')]},
                       {'event': 'end', 'action_id': 'a1', 'recorded_at': '2026-10-22T10:01:00+08:00',
                        'executed': True, 'outcome': outcome, 'evidence_path': 'receipt.json',
                        'request_id': '99999999999999999999999999999', 'error': ''}]
        self.state['items'][0].update(status='completed', stage='done', completion_basis='fictional matched no email; saved')
        self.state['phase'] = 'closed'

    def test_waiting_confirmation_is_not_complete(self):
        result = self.check()
        self.assertEqual(result['exit_code'], 0, result)
        self.assertFalse(result['all_completed'])

    def test_company_paid_call_needs_allocation_and_confirmation(self):
        self.events = [{'event': 'begin', 'action_id': 'company-call', 'recorded_at': '2026-10-22',
                        'tool': 'offline.company', 'kind': 'organization_search', 'target': 'fictional company',
                        'allocations': []}]
        self.assertEqual(self.check()['exit_code'], 1)

    def test_completed_items_need_closed_phase(self):
        self.paid()
        self.state['phase'] = 'research'
        self.assertFalse(self.check()['all_completed'])

    def test_approved_paid_result_completes_and_preserves_credit(self):
        self.paid()
        result = self.check()
        self.assertEqual(result['exit_code'], 0, result)
        self.assertTrue(result['all_completed'])
        self.assertEqual(result['company_budgets']['XX:company-a']['spent'], '1')

    def test_unapproved_or_changed_person_cannot_spend(self):
        self.paid()
        self.state['approvals'][0]['confirmed'] = False
        self.assertEqual(self.check()['exit_code'], 1)
        self.state['approvals'][0]['confirmed'] = True
        self.events[0]['allocations'][0]['person_key'] = 'someone-else'
        self.assertEqual(self.check()['exit_code'], 1)

    def test_bulk_limit_and_phone_reveal_rejected(self):
        self.paid()
        self.events[0]['params']['reveal_phone_number'] = True
        self.assertEqual(self.check()['exit_code'], 1)
        self.events[0]['params']['reveal_phone_number'] = False
        self.events[0]['allocations'] *= 11
        self.assertEqual(self.check()['exit_code'], 1)

    def test_missing_company_report_and_wrong_identity_rejected(self):
        self.state['items'][0]['reports'].pop('email')
        self.assertEqual(self.check()['exit_code'], 1)
        self.state['items'][0]['reports']['email'] = {'path': 'email.md', 'sha256': sha(self.batch / 'email.md')}
        self.state['items'][0]['customer_id'] = 'XX-C002'
        self.assertEqual(self.check()['exit_code'], 1)

    def test_missing_section_but_legacy_numbered_headings_supported(self):
        path = self.batch / 'organization.md'
        path.write_text(path.read_text(encoding='utf-8').replace('## 全量人员台账', '## 4. 全量人员台账'), encoding='utf-8')
        self.state['items'][0]['reports']['organization']['sha256'] = sha(path)
        self.assertEqual(self.check()['exit_code'], 0)
        path.write_text(path.read_text(encoding='utf-8').replace('全量人员台账', 'selected only'), encoding='utf-8')
        self.state['items'][0]['reports']['organization']['sha256'] = sha(path)
        self.assertEqual(self.check()['exit_code'], 1)

    def test_changed_source_requires_acknowledgment(self):
        (self.batch / 'source.md').write_text('changed', encoding='utf-8')
        self.assertEqual(self.check()['exit_code'], 2)
        self.state['source_changes'] = [{'path': 'source.md', 'observed_sha256': sha(self.batch / 'source.md'), 'resolution': 'keep frozen scope'}]
        self.assertEqual(self.check()['exit_code'], 0)

    def test_cross_session_id_change_requires_same_person_mapping(self):
        self.paid()
        self.state['items'][0]['selection']['people'][0]['apollo_id'] = 'new-session-id'
        self.events[0]['allocations'][0]['apollo_id'] = 'new-session-id'
        self.assertEqual(self.check()['exit_code'], 1)
        self.state['id_mappings'] = [{'person_key': 'new-0', 'old_id': 'id-new-0',
                                     'new_id': 'new-session-id', 'evidence_ref': 'fictional re-search same person'}]
        self.set_search_evidence({'people': [{'id': 'new-session-id', 'has_email': True}]})
        self.assertEqual(self.check()['exit_code'], 0)

    def test_next_batch_alias_reuses_cost_and_ledger(self):
        self.paid()
        self.ledger['customer_ids'].append('XX-ALIAS')
        self.ledger['aliases'].append('fictional old name')
        self.write_json('anchor2.json', self.ledger)
        item = self.state['items'][0]
        item.update(status='waiting_confirmation', selection=make_selection(new=2),
                    ledger_anchor={'path': 'anchor2.json', 'sha256': sha(self.batch / 'anchor2.json')})
        self.state.update(batch_id='XX-NEXT', phase='research', approvals=[])
        self.events = []
        for person in item['selection']['people']:
            person['email_evidence']['sha256'] = sha(self.batch / 'search.json')
        result = self.check()
        self.assertEqual(result['exit_code'], 0, result)
        self.assertEqual(result['company_budgets']['XX:company-a']['remaining'], '2')
        item['selection'] = make_selection(new=3)
        self.assertEqual(self.check()['exit_code'], 1)

    def test_mixed_company_total_only_keeps_each_maximum_reserved(self):
        self.paid()
        first = self.state['items'][0]
        first.update(status='blocked', block_reason='only total charge known')
        self.ledger['operations'][0].update(status='unknown', actual_credits=None)
        second = copy.deepcopy(first)
        second.update(company_key='XX:company-b', customer_id='XX-C002', ledger_path='second.json', reports={})
        other = copy.deepcopy(self.ledger)
        other.update(company_key='XX:company-b', customer_ids=['XX-C002'], workflow_id='contacts-b')
        anchor = copy.deepcopy(other)
        anchor['operations'] = []
        self.write_json('second-anchor.json', anchor)
        second['ledger_anchor'] = {'path': 'second-anchor.json', 'sha256': sha(self.batch / 'second-anchor.json')}
        self.write_json('second.json', other)
        self.state['items'].append(second)
        allocation = dict(self.state['approvals'][0]['allocations'][0], company_key='XX:company-b')
        self.state['approvals'][0]['allocations'].append(allocation)
        self.state['approvals'][0]['max_credits'] = '2'
        self.events[0]['allocations'].append(dict(allocation, operation_id='op1'))
        self.write_json('receipt.json', {'fictional': True, 'total_credits': '1', 'attribution': None})
        result = self.check()
        self.assertEqual(result['exit_code'], 2, result)
        for key in ['XX:company-a', 'XX:company-b']:
            self.assertEqual(result['company_budgets'][key]['reserved'], '1')
            self.assertEqual(result['company_budgets'][key]['spent'], '0')

    def test_duplicate_company_cannot_use_fresh_ledger(self):
        duplicate = copy.deepcopy(self.state['items'][0])
        duplicate['customer_id'] = 'XX-ALIAS'
        duplicate['ledger_path'] = 'another.json'
        self.write_json('another.json', make_ledger())
        self.state['items'].append(duplicate)
        self.assertEqual(self.check()['exit_code'], 1)

    def test_anchor_preserves_spent_and_history_contacts(self):
        self.write_json('anchor.json', make_ledger(existing=2, spent='1'))
        self.state['items'][0]['ledger_anchor']['sha256'] = sha(self.batch / 'anchor.json')
        self.assertEqual(self.check()['exit_code'], 1)

    def test_anchor_cannot_be_live_ledger(self):
        self.save()
        self.state['items'][0]['ledger_anchor'] = {'path': 'ledger.json', 'sha256': sha(self.batch / 'ledger.json')}
        self.assertEqual(self.check()['exit_code'], 1)

    def test_unknown_then_reconcile_does_not_create_second_call(self):
        self.paid()
        self.ledger['operations'][0].update(status='unknown', actual_credits=None)
        self.events[1].update(executed=None, outcome='unknown', error='interrupted')
        self.state['items'][0]['status'] = 'blocked'
        self.state['items'][0]['block_reason'] = 'unknown result'
        self.assertEqual(self.check()['exit_code'], 2)
        self.events.append(dict(self.events[1], event='reconcile', executed=True, outcome='success', reason='found original receipt', error=''))
        self.ledger['operations'][0].update(status='settled', actual_credits='1')
        self.state['items'][0]['status'] = 'completed'
        result = self.check()
        self.assertEqual(result['exit_code'], 0, result)
        self.assertEqual(len(self.ledger['operations']), 1)

    def test_interrupted_after_begin_can_reconcile_original_result(self):
        self.paid()
        original = self.events.pop()
        self.ledger['operations'][0].update(status='unknown', actual_credits=None)
        self.state['items'][0].update(status='blocked', block_reason='crash after begin')
        self.assertEqual(self.check()['exit_code'], 2)
        self.events.append(dict(original, event='reconcile', reason='recovered original receipt after crash'))
        self.ledger['operations'][0].update(status='settled', actual_credits='1')
        self.state['items'][0]['status'] = 'completed'
        self.assertEqual(self.check()['exit_code'], 0)
        self.assertEqual(sum(e['event'] == 'begin' for e in self.events), 1)

    def test_confirmed_nonexecution_allows_same_person_new_approved_attempt(self):
        self.paid()
        old = self.ledger['operations'][0]
        new = dict(old, operation_id='retry1')
        old.update(status='cancelled', actual_credits='0', executed=False)
        self.events[1].update(executed=False, outcome='not_sent', error='confirmed nonexecution')
        self.state['items'][0]['selection']['people'][0]['operation_id'] = 'retry1'
        self.ledger['operations'].append(new)
        approval = copy.deepcopy(self.state['approvals'][0])
        approval['approval_id'] = 'retry-approved'
        self.state['approvals'].append(approval)
        begin = copy.deepcopy(self.events[0])
        begin.update(action_id='retry-action', approval_id='retry-approved')
        begin['allocations'][0]['operation_id'] = 'retry1'
        end = dict(self.events[1], action_id='retry-action', executed=True, outcome='success', error='')
        self.events.extend([begin, end])
        result = self.check()
        self.assertEqual(result['exit_code'], 0, result)
        self.assertEqual(result['company_budgets']['XX:company-a']['spent'], '1')
        self.events[-2]['approval_id'] = 'approved1'
        self.assertEqual(self.check()['exit_code'], 1, 'cannot reuse exhausted approval')
        self.events[-2]['approval_id'] = 'retry-approved'
        old.update(status='unknown', actual_credits=None)
        self.events[1].update(executed=None, outcome='unknown')
        self.assertEqual(self.check()['exit_code'], 1, 'unknown original attempt cannot be replaced by retry')

    def test_open_event_and_numeric_request_id(self):
        self.paid()
        self.ledger['operations'][0].update(status='reserved', actual_credits=None)
        self.events.pop()
        self.state['items'][0]['status'] = 'in_progress'
        self.assertEqual(self.check()['exit_code'], 2)
        self.paid()
        self.events[1]['request_id'] = 999999999999999999
        self.assertEqual(self.check()['exit_code'], 1)

    def test_reconciliation_cannot_erase_execution(self):
        self.paid()
        self.events.append(dict(self.events[1], event='reconcile', executed=False, reason='bad cancellation', error='bad'))
        self.assertEqual(self.check()['exit_code'], 1)

    def test_report_saved_but_old_hash_recovery_no_new_call(self):
        self.paid()
        path = self.batch / 'email.md'
        path.write_text(path.read_text(encoding='utf-8') + '\nnew saved result', encoding='utf-8')
        self.assertEqual(self.check()['exit_code'], 1)
        self.state['items'][0]['reports']['email']['sha256'] = sha(path)
        self.assertEqual(self.check()['exit_code'], 0)
        self.assertEqual(len(self.events), 2)

    def test_no_suitable_people_can_finish_without_paid_call(self):
        self.state['items'][0]['selection'] = make_selection()
        self.state['items'][0].update(status='completed', completion_basis='no suitable contacts after coverage')
        self.state['phase'] = 'closed'
        self.assertTrue(self.check()['all_completed'])

    def test_cli_readonly_bom_and_malformed_input(self):
        self.save()
        paths = [p for p in self.batch.rglob('*') if p.is_file()]
        before = {str(p): sha(p) for p in paths}
        command = [sys.executable, '-X', 'utf8', str(Path(__file__).with_name('check_batch.py')), '--batch', str(self.batch)]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertFalse(json.loads(result.stdout)['all_completed'])
        self.assertEqual(before, {str(p): sha(p) for p in paths})
        (self.batch / 'logs/actions.jsonl').write_text('{', encoding='utf-8')
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)['errors'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
