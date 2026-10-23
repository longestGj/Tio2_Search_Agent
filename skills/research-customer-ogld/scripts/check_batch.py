"""Read-only structural checks. No network, writes, semantic verification or scheduling."""
import argparse
import hashlib
import json
import re
from pathlib import Path

HEADINGS = ['经确认的公司官网', '1 核心结论', '2 O 官网', '3 G 公开核实',
            '4 L LinkedIn', '5 D 海关', '6 商业匹配', '7 下一步', '8 证据目录与所有信息来源网址']
# Existing reports use dotted numbering and full-width separators. Accept their
# section labels without rewriting history; report meaning still needs review.
HEADING_PATTERNS = [r'经确认的公司官网(?:\s|$)', r'1[.．、]?\s+核心结论',
                    r'2[.．、]?\s+O(?:\s|[｜|：:]).*官网', r'3[.．、]?\s+G(?:\s|[｜|：:]).*公开.*核实',
                    r'4[.．、]?\s+L(?:\s|[｜|：:]).*LinkedIn', r'5[.．、]?\s+D(?:\s|[｜|：:]).*海关',
                    r'6[.．、]?\s+商业.*匹配', r'7[.．、]?\s+下一步', r'8[.．、]?\s+证据目录与所有信息来源网址']
STATUSES = ('queued', 'in_progress', 'completed', 'blocked')
MODES = ('reused', 'supplemented', 'new')
ACTIONS = ('继续开发', '先补充核实', '暂缓开发', '不匹配当前产品')
OBJECTIVE_POLICY = 'objective-evidence-v1'
OBJECTIVE_ACTIONS = ('继续开发', '排除开发')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_batch(batch: Path) -> dict:
    errors, warnings = [], []
    result = {'errors': errors, 'warnings': warnings, 'counts': {}, 'next_customer_id': None,
              'all_completed': False, 'new_search_allowed': False,
              'search_used_confirmed': 0, 'search_remaining': None, 'reconciled_actions': [],
              'legacy_conclusion_ids': [], 'exit_code': 1}
    batch = Path(batch).resolve()

    def path(value):
        if not isinstance(value, str) or not value:
            raise ValueError('file path must be nonempty string')
        p = Path(value)
        return p if p.is_absolute() else batch / p

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def nonnegative(value):
        return type(value) in (int, float) and value >= 0

    try:
        state = json.loads((batch / 'logs/checkpoint.json').read_text(encoding='utf-8-sig'))
        if not isinstance(state, dict) or state.get('schema') != 1:
            raise ValueError('checkpoint schema must be 1')
        for field in ('batch_id', 'country', 'skill_version', 'skill_commit'):
            if not text(state.get(field)):
                errors.append(f'missing {field}')
        sources, items = state.get('sources'), state.get('items')
        changes = state.get('source_changes', [])
        if not isinstance(sources, list) or not sources or not isinstance(items, list) or not isinstance(changes, list):
            raise ValueError('sources must be nonempty list; items/source_changes must be lists')
        for source in sources:
            if not isinstance(source, dict) or not isinstance(source.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', source['sha256']):
                errors.append('source requires original lowercase SHA-256 fingerprint')
                continue
            p = path(source['path'])
            current = digest(p) if p.is_file() else None
            if current != source.get('sha256'):
                acknowledged = any(isinstance(c, dict) and c.get('path') == source['path']
                                   and c.get('observed_sha256') == current and text(c.get('resolution')) for c in changes)
                if not acknowledged:
                    warnings.append(f'source changed or unavailable: {p}; reconcile frozen queue')

        counts = {k: 0 for k in STATUSES + MODES}
        result['counts'] = counts
        seen, active, waiting = set(), [], []
        predecessor_queued = False
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('each item must be an object')
            cid, status = item.get('customer_id'), item.get('status')
            if not text(cid):
                errors.append('missing customer_id')
                continue
            if cid in seen:
                errors.append(f'duplicate customer_id: {cid}')
            seen.add(cid)
            if item.get('country') != state.get('country'):
                errors.append(f'{cid}: country mismatch')
            for field in ('company_name', 'source_locator', 'stage', 'next_step'):
                if not text(item.get(field)):
                    errors.append(f'{cid}: missing {field}')
            if item.get('source_status') != 'valid' and not text(item.get('scope_exception')):
                errors.append(f'{cid}: non-valid input requires explicit scope_exception')
            if status not in STATUSES:
                errors.append(f'{cid}: invalid status')
                continue
            counts[status] += 1
            if status != 'queued' and predecessor_queued:
                errors.append(f'{cid}: queued predecessor was skipped')
            if status == 'queued':
                predecessor_queued = True
                waiting.append(cid)
            if status == 'in_progress':
                active.append(cid)
            if status == 'blocked' and not text(item.get('block_reason')):
                errors.append(f'{cid}: blocked needs block_reason')
            if item.get('mode') is not None and item['mode'] not in MODES:
                errors.append(f'{cid}: invalid mode')
            if status != 'completed':
                continue
            mode = item.get('mode')
            if mode not in MODES:
                errors.append(f'{cid}: completed needs mode')
                continue
            counts[mode] += 1
            for field in ('identity_basis', 'checked_at'):
                if not text(item.get(field)):
                    errors.append(f'{cid}: completed needs {field}')
            policy = item.get('research_policy')
            if policy == OBJECTIVE_POLICY:
                if item.get('action') not in OBJECTIVE_ACTIONS:
                    errors.append(f'{cid}: objective policy requires continue or exclude conclusion')
                if item.get('action') == '排除开发':
                    evidence = item.get('exclusion_evidence')
                    if (not text(item.get('exclusion_reason')) or not isinstance(evidence, list)
                            or not evidence or not all(text(ref) for ref in evidence)):
                        errors.append(f'{cid}: exclusion requires reason and evidence IDs; verify meaning manually')
            elif policy is not None:
                errors.append(f'{cid}: unknown research_policy')
            else:
                result['legacy_conclusion_ids'].append(cid)
                if item.get('action') not in ACTIONS:
                    errors.append(f'{cid}: missing valid legacy business action; new conclusions require research_policy')
            report = path(item.get('report_path'))
            if not report.is_file():
                errors.append(f'{cid}: missing report: {report}')
                continue
            current_hash = digest(report)
            if current_hash != item.get('report_sha256'):
                errors.append(f'{cid}: report hash mismatch')
            body = report.read_text(encoding='utf-8-sig')
            if not re.search(r'(?<![\w-])' + re.escape(cid) + r'(?![\w-])', body):
                errors.append(f'{cid}: customer ID missing from report')
            for heading, pattern in zip(HEADINGS, HEADING_PATTERNS):
                if not re.search(r'^#{1,3}\s+' + pattern, body, re.M):
                    errors.append(f'{cid}: missing heading {heading}')
            if re.search(r'\{\{[^\n]*\}\}', body):
                errors.append(f'{cid}: unresolved template placeholder')
            if mode != 'new':
                if not text(item.get('original_date')) or not text(item.get('original_report_sha256')):
                    errors.append(f'{cid}: reuse needs original date and hash')
                if path(item.get('original_report_path')).resolve() != report.resolve():
                    errors.append(f'{cid}: existing report identity/path changed')
            if mode == 'reused' and current_hash != item.get('original_report_sha256'):
                errors.append(f'{cid}: reused hash changed; use supplemented with snapshot')
            if mode == 'supplemented':
                old = item.get('history_path')
                if not old or not path(old).is_file() or digest(path(old)) != item.get('original_report_sha256'):
                    errors.append(f'{cid}: missing or mismatched history snapshot')
                elif path(old).samefile(report):
                    errors.append(f'{cid}: history must be an independent snapshot, not current report or alias')
        if len(active) > 1:
            errors.append('multiple in_progress companies')

        begins, ends = {}, {}
        action_text = (batch / 'logs/actions.jsonl').read_text(encoding='utf-8-sig')
        for lineno, line in enumerate(action_text.splitlines(), 1):
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError(f'log line {lineno} must be object')
            aid, kind = event.get('action_id'), event.get('event')
            if not text(aid) or not text(event.get('recorded_at')):
                errors.append(f'log line {lineno}: missing action ID/time')
                continue
            if kind == 'begin':
                if aid in begins:
                    errors.append(f'duplicate begin: {aid}')
                    continue
                if event.get('customer_id') not in seen or event.get('kind') not in ('search', 'read'):
                    errors.append(f'{aid}: invalid customer/kind')
                if event.get('dimension') not in ('O', 'G', 'L', 'D') or not text(event.get('target')) or not text(event.get('tool')):
                    errors.append(f'{aid}: invalid dimension/target/tool')
                if any(b['customer_id'] != event.get('customer_id') for a, b in begins.items() if a not in ends):
                    errors.append(f'{aid}: previous company action still open')
                begins[aid] = event
            elif kind in ('end', 'reconcile'):
                if aid not in begins:
                    errors.append(f'end without begin: {aid}')
                    continue
                if kind == 'end' and aid in ends:
                    errors.append(f'duplicate end: {aid}')
                    continue
                if kind == 'reconcile':
                    if (ends.get(aid, {}).get('outcome') != 'interrupted'
                            or aid in result['reconciled_actions'] or not text(event.get('reason'))
                            or not event.get('refs') or event.get('outcome') == 'interrupted'):
                        errors.append(f'{aid}: invalid reconciliation; needs interrupted end and recovered evidence')
                        continue
                    if ends[aid].get('executed') is True and event.get('executed') is not True:
                        errors.append(f'{aid}: reconciliation cannot erase confirmed execution')
                        continue
                    result['reconciled_actions'].append(aid)
                outcome, executed = event.get('outcome'), event.get('executed')
                if executed is not None and type(executed) is not bool:
                    errors.append(f'{aid}: executed must be true/false/null')
                valid = ((outcome in ('success', 'error') and executed is True)
                         or (outcome == 'cancelled' and executed is False)
                         or (outcome == 'interrupted' and (executed is True or executed is None)))
                if not valid or not text(event.get('summary')) or not isinstance(event.get('refs'), list):
                    errors.append(f'{aid}: invalid end/outcome/executed/summary/refs')
                if outcome == 'success' and not event.get('refs'):
                    errors.append(f'{aid}: success needs result reference')
                if outcome in ('error', 'interrupted') and not text(event.get('error')):
                    errors.append(f'{aid}: missing error/limitation')
                ends[aid] = event
            else:
                errors.append(f'log line {lineno}: invalid event')
        for aid in begins.keys() - ends.keys():
            warnings.append(f'{aid}: open action; reconcile')
        for aid, event in ends.items():
            if event.get('outcome') == 'interrupted':
                warnings.append(f'{aid}: interrupted/unknown execution; reconcile')
        search_used = sum(b['kind'] == 'search' and ends.get(a, {}).get('executed') is True for a, b in begins.items())
        result['search_used_confirmed'] = search_used
        budget = state.get('budget')
        if not isinstance(budget, dict):
            raise ValueError('budget must be object')
        limit, used = budget.get('search_limit'), budget.get('search_used')
        if (limit is not None and (type(limit) is not int or limit < 0)) or type(used) is not int or used != search_used:
            errors.append('budget search_limit/search_used invalid or disagrees with recorded execution')
        if type(limit) is int and limit >= 0:
            result['search_remaining'] = max(0, limit - search_used)
            if search_used > limit:
                errors.append('search budget exceeded')
        minutes_limit, minutes_used = budget.get('active_minutes_limit'), budget.get('active_minutes_used')
        if minutes_limit is not None and not nonnegative(minutes_limit):
            errors.append('invalid active_minutes_limit')
        if minutes_used is not None and not nonnegative(minutes_used):
            errors.append('invalid active_minutes_used')
        if minutes_limit is not None and minutes_used is None:
            warnings.append('active time budget cannot be established')
        time_available = minutes_limit is None or (nonnegative(minutes_used) and minutes_used < minutes_limit)
        if not errors and not warnings:
            result['next_customer_id'] = (active + waiting + [None])[0]
            result['all_completed'] = bool(items) and counts['completed'] == len(items)
            result['new_search_allowed'] = time_available and (limit is None or search_used < limit)
        result['exit_code'] = 1 if errors else 2 if warnings else 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(f'invalid checkpoint/log: {exc}')
        result['exit_code'] = 1
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    args = parser.parse_args()
    result = check_batch(args.batch)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
