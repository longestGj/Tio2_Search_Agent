"""SOP word-count contract: changes to whitespace or field boundaries break these tests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('count_words.py')


class WordCountTests(unittest.TestCase):
    def run_count(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'mail.json'
            path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            original = path.read_bytes()
            result = subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPT), str(path)], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(path.read_bytes(), original, 'counter must not edit input')
            return result

    def data(self, body='One two', stage='Mail 2'):
        return dict(stage=stage, subject='Malaysia TiO2', greeting='Hi Jamie,', body=body,
                    closing='Best regards,', signature='Ai Long', to='jamie@alba.example', from_email='ai-long@mytio2.com')

    def test_body_excludes_subject_greeting_closing_signature_and_addresses(self):
        result = self.run_count(self.data())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['body_words'], 2)
        self.assertEqual(json.loads(result.stdout)['full_words'], 10)

    def test_90_words_passes(self):
        result = self.run_count(self.data(' '.join(['word'] * 90)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['mail2_within_limit'], True)

    def test_91_words_reports_limit_failure(self):
        result = self.run_count(self.data(' '.join(['word'] * 91)))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)['body_words'], 91)
        self.assertEqual(json.loads(result.stdout)['mail2_within_limit'], False)

    def test_links_hyphens_and_unicode_whitespace(self):
        result = self.run_count(self.data('Water-based\tTiO₂\nhttps://example.test/a?b=c\u00a0sales@example.test'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['body_words'], 4)

    def test_other_stages_have_no_imposed_90_word_limit(self):
        for stage in ['Mail 1', 'Mail 3', 'Mail 4', 'reply']:
            with self.subTest(stage=stage):
                result = self.run_count(self.data(' '.join(['word'] * 91), stage))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIsNone(json.loads(result.stdout)['mail2_within_limit'])

    def test_missing_or_non_text_fields_and_unknown_stage_are_errors(self):
        for field, value in [('stage', 'Mail2'), ('body', 90), ('signature', None)]:
            with self.subTest(field=field):
                data = self.data(); data[field] = value
                result = self.run_count(data)
                self.assertEqual(result.returncode, 2)
                self.assertIn('error', result.stdout)
        data = self.data(); del data['body']
        self.assertEqual(self.run_count(data).returncode, 2)

    def test_empty_body_not_presented_as_valid(self):
        result = self.run_count(self.data('  \n'))
        self.assertEqual(result.returncode, 2)
        self.assertIn('error', result.stdout)


if __name__ == '__main__':
    unittest.main()
