"""Append-only research journal and pending gate. Python 3.10+, stdlib only.

Records agent-reported tool results; it neither browses nor intercepts tools.
One writer owns each batch. See references/execution-logging.md.
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
import hashlib
import os
from pathlib import Path
import re
import sys
import uuid

STATES = {'pending', 'valid', 'unresolved', 'duplicate', 'excluded'}
REPORTS = ('01_候选客户总表.md', '02_证据与来源.md',
           '03_搜索与覆盖记录.md', '04_批次复核与测试报告.md')
FIELDS = {
    'init': {'source', 'leads'},
    'lead': {'lead_id', 'status', 'stage', 'reason'},
    'begin': {'kind', 'purpose', 'target', 'tool', 'round_id', 'lead_ids',
              'parent_action_id', 'relation'},
    'end': {'action_id', 'outcome', 'executed', 'summary', 'refs', 'error'},
    'checkpoint': {'round_id'},
    'check': set(),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and all(nonempty(x) for x in value)


def validate_lead(row):
    require(isinstance(row, dict), 'lead must be an object')
    require(set(row) == FIELDS['lead'], 'lead requires lead_id/status/stage/reason')
    require(nonempty(row['lead_id']) and nonempty(row['reason']), 'lead_id and reason required')
    require(row['status'] in STATES, 'invalid lead status')
    stages = {'not_started', 'in_progress'} if row['status'] == 'pending' else {'complete'}
    require(row['stage'] in stages, 'stage inconsistent with status')


def state_new():
    return {'initialized': False, 'leads': {}, 'actions': {},
            'current_round': None, 'last_work_seq': 0, 'checkpoint': None}


def unfinished(state):
    return [key for key, value in state['actions'].items() if 'end' not in value]


def apply(state, event):
    op = event['op']
    if op == 'init':
        require(not state['initialized'], 'already initialized; do not reset journal')
        require(nonempty(event.get('source')), 'source required, including explicit empty baseline')
        require(isinstance(event.get('leads'), list), 'leads must be a complete baseline list')
        for row in event['leads']:
            validate_lead(row)
            require(row['lead_id'] not in state['leads'], 'duplicate baseline lead_id')
            state['leads'][row['lead_id']] = dict(row)
        state['initialized'] = True
        state['last_work_seq'] = event['seq']
        return
    require(state['initialized'], 'initialize from current full queue first')
    if op == 'lead':
        require(not unfinished(state), 'unfinished action; record result before changing queue')
        row = {key: event.get(key) for key in FIELDS['lead']}
        validate_lead(row)
        if row['lead_id'] not in state['leads']:
            require(row['status'] == 'pending' and row['stage'] == 'not_started',
                    'new lead must start pending/not_started')
        state['leads'][row['lead_id']] = row
    elif op == 'begin':
        require(not unfinished(state), 'unfinished action; close it truthfully before next tool call')
        require(event.get('kind') in {'search', 'read'}, 'kind must be search or read')
        require(event.get('purpose') in {'discovery', 'verify'}, 'purpose must be discovery or verify')
        for key in ('target', 'tool', 'round_id', 'action_id'):
            require(nonempty(event.get(key)), key + ' required')
        ids = event.get('lead_ids')
        require(strings(ids) and len(ids) == len(set(ids)), 'lead_ids must be unique strings')
        require(all(key in state['leads'] for key in ids), 'unknown lead_id')
        if event['purpose'] == 'discovery':
            pending = [key for key, row in state['leads'].items() if row['status'] == 'pending']
            require(not pending, 'pending blocks discovery: ' + ', '.join(pending))
        else:
            require(bool(ids), 'verification needs registered lead_ids')
        parent = event.get('parent_action_id')
        relation = event.get('relation')
        if parent is not None or relation is not None:
            require(parent in state['actions'], 'parent_action_id must identify a previous attempt')
            require(relation in {'retry', 'alternative'}, 'relation must be retry or alternative')
        require(event['action_id'] not in state['actions'], 'duplicate action_id')
        state['actions'][event['action_id']] = {'begin': event}
        state['current_round'] = event['round_id']
    elif op == 'end':
        action = state['actions'].get(event.get('action_id'))
        require(action is not None and 'end' not in action, 'unknown or already completed action')
        outcome = event.get('outcome')
        require(outcome in {'success', 'error', 'interrupted', 'cancelled'}, 'invalid outcome')
        executed = event.get('executed')
        require(executed is None or type(executed) is bool, 'executed must be true/false/null')
        require(nonempty(event.get('summary')), 'result summary required')
        require(strings(event.get('refs')), 'refs must list tool output references or evidence paths')
        require(isinstance(event.get('error'), str), 'error field required (empty when none)')
        if outcome in {'success', 'error'}:
            require(executed is True, 'success/error requires executed=true')
        if outcome == 'success':
            require(bool(event['refs']), 'success needs a tool output reference or evidence file')
        if outcome in {'error', 'interrupted'}:
            require(nonempty(event['error']), 'failure or interruption needs error details')
        if outcome == 'cancelled':
            require(executed is False, 'cancelled means tool was never invoked')
        if outcome == 'interrupted':
            require(executed is not False, 'use cancelled for a known unexecuted action')
        action['end'] = event
    elif op == 'checkpoint':
        require(not unfinished(state), 'unfinished action; recover result before report checkpoint')
        require(nonempty(event.get('round_id')), 'round_id required')
        require(state['current_round'] is None or event['round_id'] == state['current_round'],
                'checkpoint round does not match current round')
        require(event.get('through_seq') == state['last_work_seq'], 'checkpoint sequence is stale')
        require(isinstance(event.get('files'), dict) and set(event['files']) == set(REPORTS),
                'checkpoint must include four reports')
        require(all(isinstance(v, str) and re.fullmatch(r'[0-9a-f]{64}', v)
                    for v in event['files'].values()), 'invalid report fingerprint')
        state['checkpoint'] = event
        state['current_round'] = event['round_id']
    else:
        raise ValueError('unknown event operation')
    if op != 'checkpoint':
        state['last_work_seq'] = event['seq']


def report_files(batch, round_id, through_seq):
    """Bind four actual report versions to the progress the author reviewed.

    The marker records an author's assertion; content accuracy still needs review.
    """
    fingerprints = {}
    expected = {'round_id': round_id, 'through_seq': through_seq}
    for name in REPORTS:
        path = Path(batch)/name
        require(path.is_file(), 'missing report: ' + name)
        raw = path.read_bytes()
        content = raw.decode('utf-8-sig')
        markers = re.findall(r'<!-- research-checkpoint:\s*(.*?)\s*-->', content)
        require(len(markers) == 1 and json.loads(markers[0]) == expected,
                'report marker must match current progress: ' + name)
        body = re.sub(r'<!-- research-checkpoint:.*?-->', '', content, flags=re.S).strip()
        require(bool(body), 'empty report body: ' + name)
        fingerprints[name] = hashlib.sha256(raw).hexdigest()
    return fingerprints


def reports_status(batch, state):
    checkpoint = state['checkpoint']
    if checkpoint is None:
        return False, 'no report checkpoint recorded'
    if (checkpoint['through_seq'] != state['last_work_seq'] or
            checkpoint['round_id'] != state['current_round']):
        return False, 'work continued after last report checkpoint'
    try:
        actual = report_files(batch, state['current_round'], state['last_work_seq'])
        if actual != checkpoint['files']:
            return False, 'report content changed after checkpoint'
    except (ValueError, OSError) as exc:
        return False, str(exc)
    return True, 'four report versions match recorded progress; semantic review still required'


def read_journal(path):
    state = state_new()
    events = []
    if not path.exists():
        return state, events
    raw = path.read_bytes()
    require(not raw or raw.endswith(b'\n'), 'corrupt journal: truncated final line; preserve before repair')
    try:
        for number, line in enumerate(raw.decode('utf-8').splitlines(), 1):
            event = json.loads(line)
            require(event['schema'] == 1 and event['seq'] == number, 'invalid schema or sequence')
            require(datetime.fromisoformat(event['recorded_at']).utcoffset() is not None,
                    'timestamp needs timezone')
            apply(state, event)
            events.append(event)
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError('corrupt journal: ' + str(exc)) from exc
    return state, events


def report(state, count):
    actions = state['actions']
    unknown = [key for key, row in actions.items()
               if row.get('end', {}).get('executed') is None]
    interrupted = [key for key, row in actions.items()
                   if row.get('end', {}).get('outcome') == 'interrupted']
    pending = {key: row['stage'] for key, row in state['leads'].items() if row['status'] == 'pending'}
    totals = Counter(row['status'] for row in state['leads'].values())
    executed = Counter(row['begin']['kind'] for row in actions.values()
                       if row.get('end', {}).get('executed') is True)
    return {
        'current_round': state['current_round'], 'last_work_seq': state['last_work_seq'],
        'event_count': count, 'statuses': {key: totals[key] for key in sorted(STATES)},
        'pending': pending, 'unfinished_actions': unfinished(state),
        'unknown_execution': unknown, 'interrupted_actions': interrupted,
        'failed_actions': [key for key, row in actions.items() if row.get('end', {}).get('outcome') == 'error'],
        'executed_searches': executed['search'], 'executed_reads': executed['read'],
        'journal_complete': not (unfinished(state) or unknown or interrupted),
        'discovery_allowed': not pending and not unfinished(state),
        'scope': 'Only journaled actions; counts require reconciliation with actual tool history.',
    }


def execute(batch, payload):
    require(isinstance(payload, dict), 'input must be a JSON object')
    op = payload.get('op')
    require(isinstance(op, str) and op in FIELDS, 'op must be a supported operation string')
    require(not (set(payload) - FIELDS[op] - {'op'}), 'unexpected input fields')
    directory = Path(batch).resolve() / 'logs'
    if op != 'init':
        require((directory/'events.jsonl').exists(), 'initialize from current full queue first')
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory/'.writer.lock'
    try:
        handle = lock.open('x', encoding='utf-8')
    except FileExistsError as exc:
        raise ValueError('writer lock exists; confirm ownership before recovering a stale lock') from exc
    try:
        with handle:
            handle.write(str(os.getpid()))
        journal = directory/'events.jsonl'
        state, events = read_journal(journal)
        if op == 'check':
            require(state['initialized'], 'journal missing initialization')
            result = report(state, len(events))
            result['reports_current'], result['reports_detail'] = reports_status(Path(batch), state)
            return result
        if (op == 'begin' and state['current_round'] is not None
                and payload.get('round_id') != state['current_round']):
            current, detail = reports_status(Path(batch), state)
            require(current, 'report checkpoint required before changing round: ' + detail)
        event = dict(payload, schema=1, seq=len(events)+1,
                     recorded_at=datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='milliseconds'))
        if op == 'begin':
            event['action_id'] = 'A-' + uuid.uuid4().hex
        if op == 'checkpoint':
            event['through_seq'] = state['last_work_seq']
            event['files'] = report_files(Path(batch), payload.get('round_id'), state['last_work_seq'])
        apply(state, event)
        with journal.open('ab') as stream:
            stream.write((json.dumps(event, ensure_ascii=False) + '\n').encode('utf-8'))
            stream.flush()
            os.fsync(stream.fileno())
        result = {'saved': True, 'seq': event['seq'], 'recorded_at': event['recorded_at']}
        if 'action_id' in event:
            result['action_id'] = event['action_id']
        return result
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True, type=Path, help='Current batch directory')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', type=Path, help='UTF-8 JSON event file (op: init/lead/begin/end/checkpoint)')
    group.add_argument('--check', action='store_true', help='Read journal; exit 2 for incomplete trace')
    group.add_argument('--check-reports', action='store_true', help='Delivery check: require current four reports too')
    args = parser.parse_args()
    try:
        payload = {'op': 'check'} if args.check or args.check_reports else json.loads(args.input.read_text(encoding='utf-8-sig'))
        result = execute(args.batch, payload)
        print(json.dumps(result, ensure_ascii=False))
        incomplete = payload['op'] == 'check' and (not result['journal_complete'] or
                      (args.check_reports and not result['reports_current']))
        return 2 if incomplete else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
