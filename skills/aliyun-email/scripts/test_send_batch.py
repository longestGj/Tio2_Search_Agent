import json
import base64
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
import email_cli
from send_batch import load_batch, run_batch


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.now = datetime(2026, 10, 22, tzinfo=timezone.utc)
        (self.root / 'body.txt').write_text('Hi A,\nTest body.\nBest regards,\nAi Long', encoding='utf-8')
        (self.root / 'signature.jpg').write_bytes(b'test signature')
        self.data = dict(batch_id='TEST', send_at=(self.now + timedelta(seconds=10)).isoformat(),
                         approval_ref='Synthetic approval', signature_image='signature.jpg',
                         messages=[dict(draft_id=str(i), to=['a@example.test', 'b@example.test'],
                                        subject='Malaysia test', body_file='body.txt', attachments=[])
                                   for i in range(3)])
        self.path = self.root / 'batch.json'
        self.result = self.root / 'result.json'
        self.elapsed = 0
        self.calls = []

    def load(self):
        self.path.write_text(json.dumps(self.data), encoding='utf-8')
        return load_batch(self.path)

    def clock(self):
        return self.now + timedelta(seconds=self.elapsed)

    def sleep(self, seconds):
        self.elapsed += seconds

    def send(self, item, signature):
        saved = json.loads(self.result.read_text(encoding='utf-8'))
        self.assertEqual(saved['messages'][len(self.calls)]['status'], 'sending')
        self.calls.append((self.elapsed, item['to']))
        self.elapsed += 2
        return dict(message_id='<test@example.test>', accepted=item['to'], refused={})

    def run_it(self, sender=None):
        return run_batch(self.load(), self.result, sender or self.send,
                         now=self.clock, sleep=self.sleep)

    def test_due_order_interval_and_joint_recipients(self):
        result = self.run_it()
        self.assertEqual([t for t, _ in self.calls], [10, 42, 74])
        self.assertEqual(result['status'], 'finished')
        self.assertTrue(all(len(x[1]) == 2 for x in self.calls))

    def test_ten_company_batch(self):
        first = self.data['messages'][0]
        self.data['messages'] = [dict(first, draft_id=f'C{i}-M1') for i in range(10)]
        result = self.run_it()
        self.assertEqual([t for t, _ in self.calls], [10 + 32*i for i in range(10)])
        self.assertEqual(len(result['messages']), 10)

    def test_keyboard_interrupt_stops(self):
        def interrupted(item, signature):
            raise KeyboardInterrupt()
        result = self.run_it(interrupted)
        self.assertEqual(result['status'], 'stopped')
        self.assertEqual(result['messages'][0]['status'], 'unknown')
        self.assertEqual(result['messages'][1]['status'], 'pending')

    def test_check_command_does_not_connect_or_create_results(self):
        import send_batch
        self.load()
        with patch('sys.argv', ['send_batch.py', str(self.path)]), patch.object(email_cli, 'get_config') as config:
            self.assertEqual(send_batch.main(), 0)
            config.assert_not_called()
        self.assertFalse((self.root/'send-results.json').exists())

    def test_exception_stops_without_retry(self):
        def broken(item, signature):
            if self.calls:
                raise TimeoutError('synthetic failure')
            return self.send(item, signature)
        result = self.run_it(broken)
        self.assertEqual([m['status'] for m in result['messages']], ['accepted', 'unknown', 'pending'])
        self.assertEqual(result['status'], 'stopped')

    def test_partial_acceptance_stops(self):
        result = self.run_it(lambda item, sig: dict(message_id='<p@test>', accepted=[item['to'][0]],
                                                    refused={item['to'][1]: 550}))
        self.assertEqual([m['status'] for m in result['messages']], ['partial', 'pending', 'pending'])

    def test_existing_result_is_not_resumed(self):
        self.result.write_text('old evidence', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            self.run_it()
        self.assertEqual(self.result.read_text(), 'old evidence')

    def test_missed_start_does_not_send(self):
        self.data['send_at'] = (self.now-timedelta(seconds=1)).isoformat()
        with self.assertRaises(ValueError):
            self.run_it()
        self.assertEqual(self.calls, [])

    def test_sleeping_machine_does_not_catch_up_next_day(self):
        def suspended(seconds):
            self.elapsed += seconds + 86400
        result = run_batch(self.load(), self.result, self.send, now=self.clock, sleep=suspended)
        self.assertEqual(result['status'], 'stopped')
        self.assertEqual(self.calls, [])
        self.assertTrue(all(m['status'] == 'pending' for m in result['messages']))

    def test_suspension_between_messages_stops_remaining(self):
        def suspended(seconds):
            self.elapsed += seconds + (3600 if self.calls else 0)
        result = run_batch(self.load(), self.result, self.send, now=self.clock, sleep=suspended)
        self.assertEqual(result['status'], 'stopped')
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(result['messages'][0]['status'], 'accepted')

    def test_missing_attachment_rejected_before_send(self):
        self.data['messages'][-1]['attachments'] = ['missing.pdf']
        with self.assertRaises(FileNotFoundError):
            self.load()

    def test_naive_time_rejected(self):
        self.data['send_at'] = '2026-10-22T10:00:00'
        with self.assertRaises(ValueError):
            self.load()

    def test_approval_required(self):
        self.data['approval_ref'] = ''
        with self.assertRaises(ValueError):
            self.load()

    def test_modified_input_stops(self):
        batch = self.load()
        (self.root/'body.txt').write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError):
            run_batch(batch, self.result, self.send, now=self.clock, sleep=self.sleep)


class ConnectorTests(unittest.TestCase):
    def test_mime_signature_reply_to_and_literal_text(self):
        with tempfile.TemporaryDirectory() as td:
            image = Path(td)/'sig.png'
            image.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB0kAAAAASUVORK5CYII='))
            cfg = dict(user='ai-long@mytio2.com', sender_name='Ai Long',
                       reply_to='ai-long@mytio2.com', signature_img=str(image))
            body = 'Hi A and B,\nA < B & C\nBest regards,\nAi Long'
            msg = email_cli.build_message(cfg, 'a@example.test, b@example.test', 'Test', body)
            self.assertEqual(msg['Reply-To'], cfg['user'])
            images = [p for p in msg.walk() if p.get_content_maintype() == 'image']
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].get_payload(decode=True), image.read_bytes())
            plain = next(p for p in msg.walk() if p.get_content_type() == 'text/plain')
            self.assertEqual(plain.get_payload(decode=True).decode('utf-8'), body)
            html = next(p for p in msg.walk() if p.get_content_type() == 'text/html')
            self.assertIn('A &lt; B &amp; C', html.get_payload(decode=True).decode('utf-8'))

    def test_joint_envelope_addresses_are_separate(self):
        self.assertEqual(email_cli.all_recipients('a@example.test, b@example.test'),
                         ['a@example.test', 'b@example.test'])

    def test_partial_result_returned(self):
        from types import SimpleNamespace
        args = SimpleNamespace(to='a@example.test, b@example.test', subject='Test', body='A < B', attachment=[])
        config = dict(user='ai-long@mytio2.com', password='test', smtp_server='example.test', smtp_port=465,
                      signature_img=None, sender_name='Ai Long', reply_to='ai-long@mytio2.com')
        with patch.object(email_cli.smtplib, 'SMTP_SSL') as smtp:
            smtp.return_value.__enter__.return_value.sendmail.return_value = {'b@example.test': (550, b'no')}
            result = email_cli.send_mail_cli(args, config_override=config)
        self.assertEqual(result['accepted'], ['a@example.test'])
        self.assertEqual(result['refused'], {'b@example.test': 550})

    def test_batch_caller_receives_error_type(self):
        from types import SimpleNamespace
        import smtplib
        args = SimpleNamespace(to='a@example.test', subject='Test', body='Test', attachment=[])
        config = dict(user='ai-long@mytio2.com', password='test', smtp_server='example.test', smtp_port=465,
                      signature_img=None, sender_name='Ai Long')
        with patch.object(email_cli.smtplib, 'SMTP_SSL') as smtp:
            smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPAuthenticationError(535, b'do not log raw data')
            with self.assertRaises(smtplib.SMTPAuthenticationError):
                email_cli.send_mail_cli(args, config_override=config)


if __name__ == '__main__':
    unittest.main()
