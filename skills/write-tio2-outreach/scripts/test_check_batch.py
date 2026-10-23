"""Batch integrity tests with temporary synthetic artifacts; no customer operations."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from check_batch import check_batch
from count_words import count_mail


class BatchTests(unittest.TestCase):
    @staticmethod
    def body_block(did, body):
        return f'{did}\n<!-- outreach-body:{did}:start -->\n{body}\n<!-- outreach-body:{did}:end -->'

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.batch = self.root / 'batch'
        (self.batch / 'logs').mkdir(parents=True)
        self.cp = self.batch / 'logs/checkpoint.json'
        self.data = dict(schema=2, batch_id='TEST-01', country='GB', owner='test',
                         updated_at='2026-10-22T15:00:00+08:00', request_ref='offline test',
                         source_artifacts=[self.artifact('input.md', 'synthetic input')],
                         reports=[self.artifact('batch/01_批次进度.md', 'progress'),
                                  self.artifact('batch/02_批次总结.md', 'summary')],
                         frozen_companies=[dict(customer_id='A', selected_recipients=['a@example.test'],
                                                required_drafts=[])], drafts=[], company_status={'A': 'completed'})
        for i in [1, 2]:
            did = f'A-M{i}'
            self.data['frozen_companies'][0]['required_drafts'].append(
                dict(draft_id=did, recipients=['a@example.test'], stage=f'Mail {i}'))
            payload = dict(stage=f'Mail {i}', subject='Malaysia test', greeting='Hi A,',
                           body='Synthetic product facts. May we send details?', closing='Best regards,', signature='Test')
            self.data['drafts'].append(dict(draft_id=did, customer_id='A', recipients=['a@example.test'],
                stage=f'Mail {i}', version='1', section=f'Mail {i}',
                artifact=self.artifact(f'draft{i}.md', self.body_block(did, payload['body'])),
                count_input=self.artifact(f'count{i}.json', json.dumps(payload)),
                counts=count_mail(payload), content_status='已复核待用户审阅', send_status='未发送',
                followup_status='未核查', user_review='未审阅', review={'value': True, 'facts': True}, blockers=[]))

    def artifact(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return {'path': name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

    def run_check(self, complete=False):
        self.cp.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        return check_batch(self.batch, self.root, complete)

    def test_complete(self):
        result = self.run_check(True)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['counts']['drafts'], 2)

    def test_user_changes_cannot_remain_review_ready(self):
        self.data['drafts'][0]['user_review'] = '需修改'
        result = self.run_check(True)
        self.assertFalse(result['ok'])
        self.assertTrue(any('user requested changes' in e for e in result['errors']))

    def test_user_rewrite_can_be_saved_but_not_complete(self):
        d = self.data['drafts'][0]
        d.update(user_review='需修改', content_status='需重写',
                 user_feedback='同公司联系人合写')
        self.data['company_status']['A'] = 'in_progress'
        self.assertTrue(self.run_check()['ok'])
        self.assertFalse(self.run_check(True)['ok'])

    def test_unknown_user_review_rejected(self):
        self.data['drafts'][0]['user_review'] = '随便填入的状态'
        self.assertFalse(self.run_check()['ok'])

    def test_user_accepted_content_can_complete(self):
        self.data['drafts'][0]['user_review'] = '已认可具体内容'
        self.assertTrue(self.run_check(True)['ok'])

    def test_missing_draft(self):
        self.data['drafts'].pop()
        self.assertFalse(self.run_check()['ok'])

    def test_duplicate_draft(self):
        self.data['drafts'].append(copy.deepcopy(self.data['drafts'][0]))
        self.assertFalse(self.run_check()['ok'])

    def test_wrong_recipient(self):
        self.data['drafts'][0]['recipients'] = ['outsider@example.test']
        self.assertFalse(self.run_check()['ok'])

    def test_recipient_cap(self):
        self.data['frozen_companies'][0]['selected_recipients'] = [f'{i}@example.test' for i in range(4)]
        self.assertFalse(self.run_check()['ok'])

    def test_joint_combined_file(self):
        c = self.data['frozen_companies'][0]
        c['selected_recipients'].append('b@example.test')
        combined = self.artifact('combined.md', '\n'.join(self.body_block(f'A-M{i}', 'Synthetic product facts. May we send details?') for i in [1, 2]))
        for plan, draft in zip(c['required_drafts'], self.data['drafts']):
            plan['recipients'] = c['selected_recipients'][:]
            draft['recipients'] = c['selected_recipients'][:]
            draft['artifact'] = combined
        self.assertTrue(self.run_check(True)['ok'])

    def test_changed_source(self):
        (self.root / 'input.md').write_text('changed', encoding='utf-8')
        self.assertFalse(self.run_check()['ok'])

    def test_missing_output(self):
        (self.root / 'draft1.md').unlink()
        self.assertFalse(self.run_check()['ok'])

    def test_blocked_is_not_complete(self):
        d = self.data['drafts'][1]
        d['content_status'] = '待补资料'
        d['review']['facts'] = False
        d['blockers'] = ['REACH date conflict']
        self.assertFalse(self.run_check()['ok'])
        self.data['company_status']['A'] = 'blocked'
        self.data['company_notes'] = {'A': 'Resolve REACH date conflict'}
        self.assertTrue(self.run_check()['ok'])
        self.assertFalse(self.run_check(True)['ok'])

    def test_false_review(self):
        self.data['drafts'][0]['review']['value'] = False
        self.assertFalse(self.run_check()['ok'])

    def test_word_limit_and_mismatched_counts(self):
        d = self.data['drafts'][1]
        p = json.loads((self.root / 'count2.json').read_text())
        p['body'] = ' '.join(['word'] * 91)
        d['count_input'] = self.artifact('count2.json', json.dumps(p))
        d['counts'] = count_mail(p)
        d['artifact'] = self.artifact('draft2.md', self.body_block('A-M2', p['body']))
        self.assertFalse(self.run_check()['ok'])

    def test_unknown_company_and_plan_duplicates(self):
        self.data['frozen_companies'].append(copy.deepcopy(self.data['frozen_companies'][0]))
        self.assertFalse(self.run_check()['ok'])

    def test_readonly_repeat(self):
        self.assertTrue(self.run_check()['ok'])
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertTrue(check_batch(self.batch, self.root)['ok'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_output_outside_root(self):
        self.data['drafts'][0]['artifact']['path'] = '../outside.md'
        self.assertFalse(self.run_check()['ok'])

    def test_source_path_can_be_external(self):
        with tempfile.TemporaryDirectory() as external:
            p = Path(external) / 'tds.txt'
            p.write_text('TDS')
            self.data['source_artifacts'].append({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
            self.assertTrue(self.run_check()['ok'])

    def test_pending_without_placeholder_drafts(self):
        self.data['company_status']['A'] = 'pending'
        self.data['drafts'] = []
        self.assertTrue(self.run_check()['ok'])
        self.assertFalse(self.run_check(True)['ok'])

    def test_legacy_and_malformed_json(self):
        self.data['schema'] = 1
        self.assertFalse(self.run_check()['ok'])
        self.cp.write_text('{', encoding='utf-8')
        self.assertFalse(check_batch(self.batch, self.root)['ok'])

    def test_missing_report(self):
        (self.batch / '01_批次进度.md').unlink()
        self.assertFalse(self.run_check()['ok'])

    def test_count_body_not_in_draft(self):
        self.data['drafts'][0]['artifact'] = self.artifact('draft1.md', 'A-M1\nDifferent body')
        self.assertFalse(self.run_check()['ok'])

    def test_missing_selected_email_can_be_recorded_blocked(self):
        self.data['frozen_companies'][0]['selected_recipients'] = []
        self.data['frozen_companies'][0]['required_drafts'] = []
        self.data['drafts'] = []
        self.data['company_status']['A'] = 'blocked'
        self.data['company_notes'] = {'A': 'No selected email; recover from contact producer'}
        self.assertTrue(self.run_check()['ok'])
        self.assertFalse(self.run_check(True)['ok'])
        self.data['company_status']['A'] = 'completed'
        self.assertFalse(self.run_check()['ok'])

    def test_full_body_cannot_be_truncated_for_count(self):
        body = 'Synthetic product facts. May we send details? ' + ' '.join(['extra'] * 95)
        self.data['drafts'][1]['artifact'] = self.artifact('draft2.md', self.body_block('A-M2', body))
        self.assertFalse(self.run_check(True)['ok'])

    def test_markdown_visible_text(self):
        d = self.data['drafts'][1]
        payload = json.loads((self.root / 'count2.json').read_text())
        payload['body'] = 'Review TDS for M510.'
        d['count_input'] = self.artifact('count2.json', json.dumps(payload))
        d['counts'] = count_mail(payload)
        d['artifact'] = self.artifact('draft2.md', self.body_block('A-M2', 'Review [TDS](https://example.test/tds) for **M510**.'))
        self.assertTrue(self.run_check(True)['ok'])

    def test_combined_cannot_match_other_body_or_internal_summary(self):
        original = 'Synthetic product facts. May we send details?'
        content = self.body_block('A-M1', original) + '\n' + self.body_block('A-M2', 'A different actual message.') + '\nInternal summary: '+original
        ref = self.artifact('combined.md', content)
        for d in self.data['drafts']:
            d['artifact'] = ref
        self.assertFalse(self.run_check(True)['ok'])

    def test_duplicate_body_markers_rejected(self):
        content = self.body_block('A-M2', 'Synthetic product facts. May we send details?')
        self.data['drafts'][1]['artifact'] = self.artifact('draft2.md', content+'\n'+content)
        self.assertFalse(self.run_check()['ok'])


if __name__ == '__main__':
    unittest.main()
