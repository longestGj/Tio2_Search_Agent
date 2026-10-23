"""One approved local batch. Sequential send, 30-second gaps, stop on error.

Default CLI mode checks files only. --send is an explicit external action.
No retries, resume, background installation or automatic Sent queries.
"""
import argparse
import contextlib
import hashlib
import io
import json
import re
import time
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Missing {name}')
    return value


def load_batch(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    for field in ('batch_id', 'approval_ref', 'send_at', 'signature_image'):
        _text(data.get(field), field)
    at = datetime.fromisoformat(data['send_at'])
    if at.utcoffset() is None:
        raise ValueError('send_at must include timezone offset')
    files = {}

    def file_ref(value):
        p = (path.parent / _text(value, 'file path')).resolve()
        raw = p.read_bytes()
        if not raw:
            raise ValueError(f'Empty input: {p.name}')
        files[str(p)] = hashlib.sha256(raw).hexdigest()
        return str(p)

    signature = file_ref(data['signature_image'])
    messages = data.get('messages')
    if not isinstance(messages, list) or not messages:
        raise ValueError('messages must be a nonempty list')
    ids = set()
    for item in messages:
        did = _text(item.get('draft_id'), 'draft_id')
        if did in ids:
            raise ValueError('Duplicate draft_id')
        ids.add(did)
        subject = _text(item.get('subject'), 'subject')
        if '\r' in subject or '\n' in subject:
            raise ValueError('Invalid subject')
        recipients = item.get('to')
        if (not isinstance(recipients, list) or not 1 <= len(recipients) <= 3
                or not all(isinstance(a, str) and re.fullmatch(r'[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+', a)
                           for a in recipients)
                or len({a.casefold() for a in recipients}) != len(recipients)):
            raise ValueError('to must contain 1–3 unique bare email addresses')
        if item.get('cc') or item.get('bcc'):
            raise ValueError('Simple batch uses To only; no implicit Cc/Bcc')
        item['body_file'] = file_ref(item.get('body_file'))
        body = Path(item['body_file']).read_text(encoding='utf-8-sig')
        if '<!-- outreach-body:' in body:
            raise ValueError('Use customer-facing text only, without draft markers')
        item['body'] = body
        attachments = item.get('attachments', [])
        if not isinstance(attachments, list):
            raise ValueError('attachments must be a list')
        item['attachments'] = [file_ref(p) for p in attachments]
    files[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(batch_id=data['batch_id'], approval_ref=data['approval_ref'],
                send_at=at, signature_image=signature, messages=messages, files=files)


def _unchanged(batch):
    for name, expected in batch['files'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise ValueError('Input changed; check approved version before sending')


def _save(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def run_batch(batch, result_path, sender, *, now=None, sleep=time.sleep):
    now = now or (lambda: datetime.now().astimezone())
    result_path = Path(result_path).resolve()
    if result_path.exists():
        raise FileExistsError('Results already exist. Do not resume; reconcile manually.')
    _unchanged(batch)
    if batch['send_at'] < now():
        raise ValueError('Start time has passed; set an explicitly agreed new time')
    result = dict(batch_id=batch['batch_id'], approval_ref=batch['approval_ref'],
                  send_at=batch['send_at'].isoformat(), status='waiting',
                  messages=[dict(draft_id=m['draft_id'], to=m['to'], subject=m['subject'],
                                 status='pending') for m in batch['messages']])
    # A result file is single-use evidence, not an account lock or resume engine.
    with result_path.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    current = None

    def wait(seconds):
        start = now()
        sleep(seconds)
        if (now() - start).total_seconds() > seconds + 60:
            raise TimeoutError('Wait interrupted for over 60 seconds; arrange a new time')

    try:
        while (seconds := (batch['send_at'] - now()).total_seconds()) > 0:
            wait(min(seconds, 30))
        result['status'] = 'running'
        for i, item in enumerate(batch['messages']):
            _unchanged(batch)
            current = result['messages'][i]
            current.update(status='sending', started_at=now().isoformat())
            _save(result_path, result)
            outcome = sender(item, batch['signature_image'])
            current.update(outcome)
            refused = outcome['refused']
            current.update(status='partial' if refused else 'accepted', ended_at=now().isoformat())
            if refused:
                result['status'] = 'stopped'
            _save(result_path, result)
            if refused:
                return result
            current = None
            if i + 1 < len(batch['messages']):
                wait(30)
        result['status'] = 'finished'
    except (Exception, SystemExit, KeyboardInterrupt) as exc:
        result['status'] = 'stopped'
        result['note'] = f'{type(exc).__name__}: stopped; verify the last attempt before any new batch.'
        if isinstance(getattr(exc, 'smtp_code', None), int):
            result['smtp_code'] = exc.smtp_code
        if current is not None and current['status'] == 'sending':
            current.update(status='unknown', ended_at=now().isoformat())
    _save(result_path, result)
    return result


def aliyun_sender(item, signature):
    # Reuse the local source copy of the existing Skill; no duplicate SMTP code.
    import email_cli
    with contextlib.redirect_stdout(io.StringIO()):
        config = email_cli.get_config()
    if not config or config['user'].casefold() != 'ai-long@mytio2.com':
        raise ValueError('Expected IKHLAS sender account')
    config = dict(config, signature_img=signature, sender_name='Ai Long', reply_to='ai-long@mytio2.com')
    args = SimpleNamespace(to=', '.join(item['to']), subject=item['subject'], body=item['body'],
                           attachment=item['attachments'], cc=None, bcc=None)
    with contextlib.redirect_stdout(io.StringIO()):
        return email_cli.send_mail_cli(args, config_override=config)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch', type=Path)
    parser.add_argument('--send', action='store_true', help='Actually wait and send the approved batch')
    parser.add_argument('--results', type=Path, help='New result file; default: batch directory/send-results.json')
    args = parser.parse_args()
    try:
        batch = load_batch(args.batch)
        if not args.send:
            print(json.dumps(dict(check='passed; no mailbox connection', batch_id=batch['batch_id'],
                                  messages=len(batch['messages']), send_at=batch['send_at'].isoformat()),
                             ensure_ascii=False))
            return 0
        result_path = args.results or args.batch.resolve().parent / 'send-results.json'
        result = run_batch(batch, result_path, aliyun_sender)
        print(json.dumps(dict(status=result['status'], results=str(result_path)), ensure_ascii=False))
        return 0 if result['status'] == 'finished' else 1
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'{type(exc).__name__}: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
