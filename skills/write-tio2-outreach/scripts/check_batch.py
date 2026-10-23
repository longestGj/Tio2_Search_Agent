"""Read-only integrity check for outreach Agent schema=2; not a quality judge."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from count_words import count_mail

READY = '已复核待用户审阅'
STATUSES = {READY, '待补资料', '已起草', '需重写'}
STAGES = {'Mail 1', 'Mail 2', 'Mail 3', 'Mail 4', 'reply'}


def visible_body(content, draft_id):
    """Only the explicitly delimited body; supports the project's small Markdown subset."""
    start = f'<!-- outreach-body:{draft_id}:start -->'
    end = f'<!-- outreach-body:{draft_id}:end -->'
    lines = content.splitlines()
    if lines.count(start) != 1 or lines.count(end) != 1:
        raise ValueError(f'{draft_id}: require one unique pair of body markers on separate lines')
    a, b = lines.index(start), lines.index(end)
    if b <= a:
        raise ValueError(f'{draft_id}: body markers out of order')
    body = '\n'.join(lines[a + 1:b])
    if '<!--' in body:
        raise ValueError(f'{draft_id}: nested comments or markers in body')
    # Plain prose, inline Markdown links, emphasis and hard line breaks are supported.
    body = re.sub(r'(?<!!)\[([^\]\n]+)\]\([^\s()]+\)', r'\1', body)
    for marker in ('**', '__', '*', '_', '`'):
        escaped = re.escape(marker)
        body = re.sub(escaped + r'([^\n]+?)' + escaped, r'\1', body)
    body = re.sub(r'\\\s*\n', '\n', body)
    return ' '.join(body.split())


def check_batch(batch: Path, root: Path, require_complete: bool = False) -> dict:
    errors = []
    counts = {'companies': 0, 'drafts': 0, 'required_drafts': 0, 'review_ready': 0, 'files': 0}
    root, batch = Path(root).resolve(), Path(batch).resolve()

    def need(condition, message):
        if not condition:
            errors.append(message)
        return condition

    def artifact(ref, label, output=False):
        if not isinstance(ref, dict) or not isinstance(ref.get('path'), str) or not ref['path']:
            errors.append(f'{label}: missing artifact path')
            return None
        p = Path(ref['path'])
        p = (root / p).resolve() if not p.is_absolute() else p.resolve()
        if output and not p.is_relative_to(root):
            errors.append(f'{label}: output outside project')
            return None
        try:
            content = p.read_bytes()
            need(bool(content.strip()), f'{label}: empty artifact')
            need(hashlib.sha256(content).hexdigest() == ref.get('sha256'), f'{label}: hash mismatch')
            return content.decode('utf-8-sig') if output else ''
        except (OSError, UnicodeError) as exc:
            errors.append(f'{label}: unreadable artifact ({exc})')
            return None

    def recipients(value, label):
        if not need(isinstance(value, list) and bool(value), f'{label}: empty recipient list'):
            return set()
        if not need(all(isinstance(x, str) and x.strip() == x and '@' in x for x in value),
                    f'{label}: invalid email strings'):
            return set()
        result = {x.casefold() for x in value}
        need(len(result) == len(value), f'{label}: duplicate recipients')
        return result

    try:
        data = json.loads((batch / 'logs/checkpoint.json').read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict) or data.get('schema') != 2:
            raise ValueError('Agent checker requires schema=2; do not silently convert legacy batches')
        for key in ['batch_id', 'country', 'owner', 'request_ref', 'updated_at']:
            need(isinstance(data.get(key), str) and bool(data[key].strip()), f'missing {key}')
        stamp = datetime.fromisoformat(data['updated_at'])
        need(stamp.utcoffset() is not None, 'updated_at requires timezone')
        need(len(data['country']) == 2 and data['country'].isalpha() and data['country'].isupper(), 'invalid country')
        sources = data['source_artifacts']
        need(isinstance(sources, list) and bool(sources), 'missing source_artifacts')
        for i, ref in enumerate(sources):
            artifact(ref, f'source {i}')
        reports = data['reports']
        report_paths = set()
        for i, ref in enumerate(reports):
            artifact(ref, f'report {i}', True)
            p = Path(ref['path'])
            report_paths.add((root / p).resolve())
        for name in ['01_批次进度.md', '02_批次总结.md']:
            need(batch / name in report_paths, f'missing batch report reference: {name}')

        companies, planned = {}, {}
        need(isinstance(data['frozen_companies'], list) and bool(data['frozen_companies']), 'empty company scope')
        for c in data['frozen_companies']:
            cid = c['customer_id']
            need(isinstance(cid, str) and bool(cid), 'invalid customer_id')
            need(cid not in companies, f'duplicate company {cid}')
            empty_blocked = (c['selected_recipients'] == [] and c['required_drafts'] == []
                             and data['company_status'].get(cid) in {'blocked', 'skipped'}
                             and bool(data.get('company_notes', {}).get(cid)))
            selected = set() if empty_blocked else recipients(c['selected_recipients'], cid)
            need(len(selected) <= 3, f'{cid}: over 3 recipients')
            companies[cid] = c
            required = c['required_drafts']
            need(isinstance(required, list) and (bool(required) or empty_blocked), f'{cid}: missing required draft plan')
            for item in required:
                did = item['draft_id']
                need(isinstance(did, str) and bool(did), f'{cid}: invalid draft ID')
                need(did not in planned, f'duplicate planned ID {did}')
                group = recipients(item['recipients'], did)
                need(group <= selected, f'{did}: plan recipient outside selected scope')
                need(item['stage'] in STAGES, f'{did}: invalid planned stage')
                planned[did] = (cid, item['stage'], group)
        counts['companies'], counts['required_drafts'] = len(companies), len(planned)
        need(set(data['company_status']) == set(companies), 'company status scope mismatch')

        actual, paths = {}, set()
        for d in data['drafts']:
            did = d['draft_id']
            need(did not in actual, f'duplicate draft {did}')
            actual[did] = d
            group = recipients(d['recipients'], did)
            need(planned.get(did) == (d['customer_id'], d['stage'], group), f'{did}: draft differs from frozen plan')
            need(d['content_status'] in STATUSES, f'{did}: unknown content status')
            for key in ['version', 'section', 'send_status', 'followup_status', 'user_review']:
                need(isinstance(d.get(key), str) and bool(d[key].strip()), f'{did}: missing {key}')
            user_review = d.get('user_review')
            need(user_review in {'未审阅', '已认可具体内容', '需修改'},
                 f'{did}: unknown user review status')
            if user_review == '需修改':
                need(d['content_status'] != READY,
                     f'{did}: user requested changes but draft is review ready')
            need(isinstance(d.get('blockers'), list), f'{did}: blockers must be list')
            content = artifact(d['artifact'], f'{did} draft', True)
            if content is not None:
                need(did in content, f'{did}: stable ID absent from file')
            paths.add(str((root / d['artifact']['path']).resolve()))
            raw = artifact(d['count_input'], f'{did} count input', True)
            if raw is not None:
                mail = json.loads(raw)
                computed = count_mail(mail)
                need(mail['stage'] == d['stage'], f'{did}: count stage mismatch')
                need(computed == d['counts'], f'{did}: counts mismatch')
                need(computed['mail2_within_limit'] is not False, f'{did}: Mail 2 exceeds 90 words')
                if content is not None:
                    need(visible_body(content, did) == ' '.join(mail['body'].split()), f'{did}: full visible body differs from count input')
            if d['content_status'] == READY:
                counts['review_ready'] += 1
                need(d.get('review') == {'value': True, 'facts': True}, f'{did}: incomplete review')
                need(d.get('blockers') == [], f'{did}: review ready with blockers')
            if d['content_status'] == '待补资料':
                need(bool(d.get('blockers')), f'{did}: missing data without recovery reason')
        counts['drafts'], counts['files'] = len(actual), len(paths)
        for cid in companies:
            status = data['company_status'].get(cid)
            need(status in {'pending', 'in_progress', 'completed', 'blocked', 'skipped'}, f'{cid}: invalid company status')
            required = {did for did, p in planned.items() if p[0] == cid}
            if status == 'completed':
                need(required <= set(actual), f'{cid}: completed with missing drafts')
                need(all(actual.get(did, {}).get('content_status') == READY for did in required),
                     f'{cid}: completed with unfinished drafts')
            if status in {'blocked', 'skipped'}:
                need(bool(data.get('company_notes', {}).get(cid)), f'{cid}: missing blocked/skipped reason')
            if require_complete:
                need(status == 'completed', f'{cid}: not complete')
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(f'invalid checkpoint: {exc}')
    return {'ok': not errors, 'errors': errors, 'counts': counts,
            'scope': 'structure, file integrity and declared review only; not factual or writing-quality validation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    result = check_batch(args.batch, args.root, args.require_complete)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
