"""Read-only validation of recorded contacts work. No network, locks or writes."""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re


def text(value):
    return isinstance(value, str) and bool(value.strip())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def money(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'\d+(?:\.\d+)?', value)), 'credits must be nonnegative decimal strings')
    amount = Decimal(value)
    require(amount.is_finite(), 'credits must be finite')
    return amount


def fmt(amount):
    return format(amount, 'f').rstrip('0').rstrip('.') if '.' in format(amount, 'f') else format(amount, 'f')


def limited_people(ledger):
    """Selected/history contacts count; public research alone has no person cap."""
    attempted = {o.get('person_key') for o in ledger['operations']
                 if isinstance(o, dict) and o.get('person_key') and o.get('status') != 'cancelled'}
    return {c['person_key'] for c in ledger['contacts'] if c['kind'] == 'named'
            and (c.get('counts_toward_limit', True) or c['person_key'] in attempted)}


def validate_ledger(ledger: dict) -> dict:
    result = {'errors': [], 'warnings': [], 'spent': '0', 'reserved': '0', 'remaining': None,
              'existing_contacts': 0, 'new_slots': 0}
    try:
        require(isinstance(ledger, dict) and ledger.get('schema') == 1, 'ledger schema must be 1')
        for field in ('company_key', 'workflow_id'):
            require(text(ledger.get(field)), f'missing {field}')
        require(money(ledger.get('credit_limit')) == 3 and type(ledger.get('contact_limit')) is int
                and ledger['contact_limit'] == 3, 'limits must be 3 credits and 3 people')
        for field in ('customer_ids', 'aliases', 'contacts', 'operations', 'history'):
            require(isinstance(ledger.get(field), list), f'{field} must be a list')
        require(ledger['customer_ids'] and all(text(x) for x in ledger['customer_ids']), 'customer_ids required')
        baseline = ledger.get('baseline_evidence')
        require(isinstance(baseline, dict) and text(baseline.get('source_ref')), 'baseline evidence required')
        confirmed = baseline.get('confirmed') is True
        if not confirmed:
            result['warnings'].append('baseline costs/identity need reconciliation')
        named = {}
        for contact in ledger['contacts']:
            require(isinstance(contact, dict), 'invalid contact')
            require(contact.get('kind') in ('named', 'public'), 'contact kind required')
            for field in ('email', 'source_ref', 'date'):
                require(text(contact.get(field)), f'contact {field} required')
            if contact['kind'] == 'named':
                key = contact.get('person_key')
                require(text(key), 'named contact person_key required')
                require(key not in named or named[key] == contact['email'], 'conflicting preferred emails for one person')
                named[key] = contact['email']
                require(type(contact.get('counts_toward_limit', True)) is bool, 'contact scope must be boolean')
                if contact.get('counts_toward_limit') is False:
                    require(text(contact.get('scope_basis')), 'research-only scope requires basis')
        counted = limited_people(ledger)
        result['existing_contacts'] = len(counted)
        result['new_slots'] = max(0, 3 - len(counted))
        if len(counted) > 3:
            result['warnings'].append('legacy contact count exceeds 3; no additions allowed')
        spent, reserved, seen = Decimal(0), Decimal(0), set()
        for op in ledger['operations']:
            require(isinstance(op, dict), 'invalid operation')
            for field in ('operation_id', 'batch_id', 'kind'):
                require(text(op.get(field)), f'operation {field} required')
            require(op['operation_id'] not in seen, 'duplicate operation_id')
            seen.add(op['operation_id'])
            maximum, actual = money(op.get('max_credits')), op.get('actual_credits')
            status = op.get('status')
            require(status in ('reserved', 'unknown', 'settled', 'cancelled'), 'invalid operation status')
            if status in ('reserved', 'unknown'):
                require(actual is None, 'unsettled actual credits must be null')
                reserved += maximum
                result['warnings'].append(f"{op['operation_id']}: {status}")
            else:
                actual = money(actual)
                require(actual <= maximum, 'actual exceeds reserved maximum')
                require(text(op.get('evidence_ref')), 'settlement evidence required')
                if status == 'cancelled':
                    require(actual == 0 and op.get('executed') is False, 'cancellation needs confirmed nonexecution')
                spent += actual
        result.update(spent=fmt(spent), reserved=fmt(reserved))
        require(spent + reserved <= 3, 'company credit ceiling exceeded')
        if confirmed:
            result['remaining'] = fmt(Decimal(3) - spent - reserved)
    except (ValueError, TypeError, KeyError, InvalidOperation) as exc:
        result['errors'].append(str(exc))
    return result


def validate_selection(ledger: dict, selection: dict) -> dict:
    budget = validate_ledger(ledger)
    result = {'errors': list(budget['errors']), 'warnings': list(budget['warnings']),
              'new_count': 0, 'reverify_count': 0, 'max_credits': '0'}
    if result['errors']:
        return result
    try:
        require(isinstance(selection, dict) and isinstance(selection.get('people'), list), 'selection people required')
        require(type(selection.get('primary_available')) is bool and text(selection.get('primary_basis')), 'primary coverage evidence required')
        existing = {c['person_key'] for c in ledger['contacts'] if c['kind'] == 'named'}
        ops = {op['operation_id']: op for op in ledger['operations']}
        seen, candidates, ids, assigned_ops = set(), set(), set(), set()
        total, prospective = Decimal(0), Decimal(0)
        for person in selection['people']:
            require(isinstance(person, dict), 'invalid selected person')
            for field in ('candidate_id', 'person_key', 'apollo_id', 'source_ref', 'identity_basis', 'relevance_basis'):
                require(text(person.get(field)), f'selected {field} required')
            require(person.get('has_email') is True, 'has_email must be true')
            evidence = person.get('email_evidence')
            require(isinstance(evidence, dict) and text(evidence.get('path'))
                    and isinstance(evidence.get('sha256'), str)
                    and re.fullmatch('[0-9a-f]{64}', evidence['sha256']),
                    'email evidence path and SHA-256 required')
            key, cid, pid = person['person_key'], person['candidate_id'], person['apollo_id']
            require(key not in seen and cid not in candidates and pid not in ids, 'duplicate selected person/candidate/ID')
            seen.add(key); candidates.add(cid); ids.add(pid)
            require(person.get('group') == ('primary' if selection['primary_available'] else 'secondary'), 'role priority violated')
            mode = person.get('mode')
            require(mode in ('new', 'reverify'), 'new/reverify mode required')
            result['new_count' if mode == 'new' else 'reverify_count'] += 1
            if mode == 'reverify':
                require(key in existing, 'reverify person has no historical email')
            maximum = money(person.get('max_credits'))
            total += maximum
            opid = person.get('operation_id')
            if opid is None:
                require(mode != 'new' or key not in existing, 'existing person cannot masquerade as new')
                prospective += maximum
            else:
                require(opid in ops and opid not in assigned_ops, 'missing or reused selected operation')
                assigned_ops.add(opid)
                require(ops[opid].get('person_key') == key and money(ops[opid]['max_credits']) == maximum,
                        'selected operation/person/cost mismatch')
        require(len(seen - limited_people(ledger)) <= budget['new_slots']
                and result['new_count'] <= 3, 'named contact ceiling exceeded')
        require(budget['remaining'] is not None or not selection['people'], 'unknown baseline cannot fund selection')
        if budget['remaining'] is not None:
            require(prospective <= money(budget['remaining']), 'selected cost exceeds remaining credits')
        result['max_credits'] = fmt(total)
    except (ValueError, TypeError, KeyError, InvalidOperation) as exc:
        result['errors'].append(str(exc))
    return result


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def search_people(value):
    """Read people from raw API JSON or an MCP response, without inventing flags."""
    if not isinstance(value, dict):
        return
    if isinstance(value.get('people'), list):
        yield from (p for p in value['people'] if isinstance(p, dict))
    if isinstance(value.get('structuredContent'), dict):
        yield from search_people(value['structuredContent'])
    content = value.get('content')
    for block in content if isinstance(content, list) else []:
        if isinstance(block, dict) and block.get('type') == 'text':
            try:
                nested = json.loads(block['text'])
            except (ValueError, TypeError, KeyError):
                continue
            yield from search_people(nested)


def preserve_history(current, previous):
    for field in ('company_key', 'workflow_id'):
        require(current[field] == previous[field], f'historical {field} mismatch')
    require(set(previous['customer_ids']).issubset(current['customer_ids']), 'historical customer IDs removed')
    now_people = {p['person_key'] for p in current['contacts'] if p['kind'] == 'named'}
    require({p['person_key'] for p in previous['contacts'] if p['kind'] == 'named'}.issubset(now_people), 'historical named people removed')
    now_ops = {op['operation_id']: op for op in current['operations']}
    for old in previous['operations']:
        require(old['operation_id'] in now_ops, 'historical operation removed; cannot reset budget')
        new = now_ops[old['operation_id']]
        for field in ('batch_id', 'kind', 'max_credits', 'person_key'):
            require(old.get(field) == new.get(field), 'historical operation scope changed')
        if old['status'] in ('settled', 'cancelled'):
            require(old['status'] == new['status'] and old['actual_credits'] == new['actual_credits'], 'historical settlement erased or changed')


REPORT_SECTIONS = {
    'organization': ['元信息', '公司主体', '检索日志', '全量人员台账', '职能分布', '自动选择', '来源'],
    'email': ['元信息', '执行摘要', '邮箱总表', '人员详情', '验收'],
}


def check_batch(batch: Path) -> dict:
    result = {'errors': [], 'warnings': [], 'counts': {}, 'company_budgets': {},
              'all_completed': False, 'next_step': None, 'exit_code': 1}
    batch = Path(batch).resolve()

    def path(value, base=batch):
        require(text(value), 'path required')
        p = Path(value)
        return p.resolve() if p.is_absolute() else (base / p).resolve()

    def file_ref(ref, base=batch):
        require(isinstance(ref, dict) and isinstance(ref.get('sha256'), str)
                and re.fullmatch('[0-9a-f]{64}', ref['sha256']), 'valid file fingerprint required')
        p = path(ref.get('path'), base)
        require(p.is_file(), f'file missing: {p}')
        require(digest(p) == ref['sha256'], f'file fingerprint changed: {p}')
        return p

    try:
        state = load_json(batch / 'logs/checkpoint.json')
        require(isinstance(state, dict) and state.get('schema') == 1, 'checkpoint schema must be 1')
        require(text(state.get('batch_id')) and text(state.get('next_step')), 'batch identity/next_step required')
        require(state.get('phase') in ('research', 'enrichment', 'closed'), 'invalid phase')
        for field in ('items', 'approvals', 'source_changes'):
            require(isinstance(state.get(field), list), f'{field} must be list')
        for field in ('sources', 'skill_sources'):
            require(isinstance(state.get(field), list) and state[field], f'{field} required')
            for ref in state[field]:
                require(isinstance(ref, dict) and isinstance(ref.get('sha256'), str) and re.fullmatch('[0-9a-f]{64}', ref['sha256']), 'source SHA-256 required')
                p = path(ref.get('path'))
                observed = digest(p) if p.is_file() else None
                if observed != ref['sha256']:
                    acknowledged = any(isinstance(c, dict) and c.get('path') == ref['path'] and
                                       c.get('observed_sha256') == observed and text(c.get('resolution')) for c in state['source_changes'])
                    if not acknowledged:
                        result['warnings'].append(f'{field} changed: {p}; reconcile frozen scope/version')
        for name in ('01_批次进度.md', '02_批次总结.md'):
            require((batch / name).is_file() and text((batch / name).read_text(encoding='utf-8-sig')), f'batch report missing/empty: {name}')
        ledgers, selections, ops, seen_ids, seen_paths = {}, {}, {}, set(), set()
        statuses = ('queued', 'in_progress', 'waiting_confirmation', 'completed', 'blocked')
        counts = {status: 0 for status in statuses}
        predecessor_queued = False
        for item in state['items']:
            require(isinstance(item, dict), 'invalid item')
            for field in ('customer_id', 'country', 'company_key', 'stage', 'next_step'):
                require(text(item.get(field)), f'item {field} required')
            key, cid = item['company_key'], item['customer_id']
            require((item['country'], cid) not in seen_ids and key not in ledgers, 'duplicate company/customer in frozen queue')
            seen_ids.add((item['country'], cid))
            status = item.get('status')
            require(status in statuses, 'invalid item status')
            require(not (predecessor_queued and status == 'in_progress'), 'cannot skip queued predecessor')
            predecessor_queued |= status == 'queued'
            counts[status] += 1
            require(counts['in_progress'] <= 1, 'multiple active companies')
            ledger_path = path(item.get('ledger_path'))
            require(ledger_path not in seen_paths, 'one ledger shared by different company identities')
            seen_paths.add(ledger_path)
            ledger = load_json(ledger_path)
            summary = validate_ledger(ledger)
            result['errors'].extend(f'{key}: {e}' for e in summary['errors'])
            result['warnings'].extend(f'{key}: {w}' for w in summary['warnings'])
            result['company_budgets'][key] = summary
            require(not summary['errors'], f'invalid ledger: {key}')
            require(ledger['company_key'] == key and cid in ledger['customer_ids'], 'ledger company/customer mismatch')
            anchor = file_ref(item.get('ledger_anchor'))
            require(not anchor.samefile(ledger_path), 'anchor cannot be live ledger or hardlink')
            preserve_history(ledger, load_json(anchor))
            for ref in ledger['history']:
                oldpath = file_ref(ref, ledger_path.parent)
                require(not oldpath.samefile(ledger_path), 'history cannot be live ledger or hardlink')
                preserve_history(ledger, load_json(oldpath))
            selection = item.get('selection')
            checked = validate_selection(ledger, selection)
            result['errors'].extend(f'{key}: {e}' for e in checked['errors'])
            if not checked['errors']:
                for person in selection['people']:
                    evidence_path = file_ref(person['email_evidence'])
                    matches = [p for p in search_people(load_json(evidence_path))
                               if p.get('id') == person['apollo_id']]
                    require(matches and all(p.get('has_email') is True for p in matches),
                            f"{key}/{person['candidate_id']}: search evidence must confirm has_email=true for selected ID")
            ledgers[key], selections[key] = ledger, selection
            ops[key] = {op['operation_id']: op for op in ledger['operations']}
            reports = item.get('reports')
            require(isinstance(reports, dict), 'reports mapping required')
            if status in ('waiting_confirmation', 'completed'):
                require(set(REPORT_SECTIONS).issubset(reports), 'two company reports required')
            for kind, ref in reports.items():
                require(kind in REPORT_SECTIONS, 'unknown report kind')
                report_path = file_ref(ref)
                content = report_path.read_text(encoding='utf-8-sig')
                require(re.search(r'(?<![\w-])' + re.escape(cid) + r'(?![\w-])', content), 'report customer identity missing')
                headings = '\n'.join(re.findall(r'^#{1,6}\s+(.+)$', content, re.M))
                require(all(token in headings for token in REPORT_SECTIONS[kind]), f'{kind} report sections incomplete')
            if status == 'completed':
                require(text(item.get('completion_basis')), 'completed requires result/limitations basis')
                for person in selection['people']:
                    op = ops[key].get(person.get('operation_id'))
                    require(op is not None and op['status'] in ('settled', 'cancelled'), 'selected person not resolved')
            if status == 'blocked':
                require(text(item.get('block_reason')), 'blocked reason required')
        result['counts'] = counts
        approvals = {}
        for approval in state['approvals']:
            require(isinstance(approval, dict) and text(approval.get('approval_id')), 'approval ID required')
            aid = approval['approval_id']
            require(aid not in approvals, 'duplicate approval ID')
            require(isinstance(approval.get('allocations'), list), 'approval scope required')
            scope = {}
            for alloc in approval['allocations']:
                require(isinstance(alloc, dict) and alloc.get('company_key') in ledgers, 'approval company not in batch')
                k = (alloc['company_key'], alloc.get('person_key'), alloc.get('apollo_id'))
                require(k not in scope, 'duplicate approval scope')
                scope[k] = money(alloc.get('max_credits'))
            require(sum(scope.values(), Decimal(0)) == money(approval.get('max_credits')), 'approval total mismatch')
            approvals[aid] = (approval, scope, {})

        begins, outcomes, used_ops = {}, {}, set()
        logpath = batch / 'logs/actions.jsonl'
        require(logpath.is_file(), 'actions log required')
        for line in logpath.read_text(encoding='utf-8-sig').splitlines():
            require(text(line), 'blank log event')
            event = json.loads(line)
            require(isinstance(event, dict) and text(event.get('action_id')) and text(event.get('recorded_at')), 'invalid log event')
            action_id, kind = event['action_id'], event.get('event')
            if kind == 'begin':
                require(action_id not in begins, 'duplicate begin')
                for field in ('tool', 'kind', 'target'):
                    require(text(event.get(field)), f'begin {field} required')
                allocations = event.get('allocations')
                require(isinstance(allocations, list), 'begin allocations required')
                if event['kind'] in ('organization_search', 'organization_enrichment', 'people_enrichment'):
                    require(bool(allocations), 'paid-capable action requires company budget allocations')
                if event['kind'] == 'people_enrichment':
                    require(0 < len(allocations) <= 10, 'people bulk request must contain 1..10 people')
                    params = event.get('params')
                    require(isinstance(params, dict) and params.get('reveal_personal_emails') is False
                            and params.get('reveal_phone_number') is False, 'work email only; disable personal email and phone')
                for allocation in allocations:
                    require(isinstance(allocation, dict), 'invalid allocation')
                    key, opid = allocation.get('company_key'), allocation.get('operation_id')
                    require(key in ops and opid in ops[key] and (key, opid) not in used_ops, 'allocation missing or duplicate operation')
                    used_ops.add((key, opid))
                    op = ops[key][opid]
                    maximum = money(allocation.get('max_credits'))
                    require(op['batch_id'] == state['batch_id'] and op['kind'] == event['kind']
                            and money(op['max_credits']) == maximum and op.get('person_key') == allocation.get('person_key'), 'operation scope mismatch')
                    if event['kind'] == 'people_enrichment':
                        people = selections[key]['people']
                        require(any(p['person_key'] == allocation.get('person_key') and p['apollo_id'] == allocation.get('apollo_id')
                                    and (p.get('operation_id') == opid or
                                         (op['status'] == 'cancelled' and op.get('executed') is False))
                                    for p in people), 'request not in fixed selection')
                    require(event.get('approval_id') in approvals, 'fee confirmation required')
                    approval, scope, used = approvals[event['approval_id']]
                    require(approval.get('confirmed') is True and approval.get('kind') == event['kind'], 'approval not confirmed or wrong kind')
                    for field in ('user_confirmation_ref', 'confirmation_text', 'balance_snapshot'):
                        require(text(approval.get(field)), f'approval {field} required')
                    scoped = (key, allocation.get('person_key'), allocation.get('apollo_id'))
                    if scoped not in scope:
                        for mapping in state.get('id_mappings', []):
                            if (mapping.get('person_key') == allocation.get('person_key') and mapping.get('new_id') == allocation.get('apollo_id')
                                    and text(mapping.get('evidence_ref'))):
                                scoped = (key, allocation.get('person_key'), mapping.get('old_id'))
                                break
                    require(scoped in scope, 'request outside approved people/company scope')
                    used[scoped] = used.get(scoped, Decimal(0)) + maximum
                    require(used[scoped] <= scope[scoped], 'approval reused beyond maximum')
                begins[action_id] = event
            elif kind in ('end', 'reconcile'):
                require(action_id in begins, 'result without begin')
                old = outcomes.get(action_id)
                require((kind == 'end' and old is None) or (kind == 'reconcile' and text(event.get('reason'))), 'duplicate end or invalid reconciliation')
                require(event.get('executed') is None or type(event.get('executed')) is bool, 'execution certainty must be boolean/null')
                require(text(event.get('outcome')), 'result outcome required')
                require(event.get('request_id') is None or text(event['request_id']), 'request_id must be string/null')
                require(path(event.get('evidence_path')).is_file(), 'result evidence missing')
                if event['executed'] is not True or event['outcome'] != 'success':
                    require(text(event.get('error')), 'failure/unknown explanation required')
                if old and old['executed'] is True:
                    require(event['executed'] is True, 'cannot erase confirmed execution')
                outcomes[action_id] = event
            else:
                raise ValueError('unknown log event')
        for action_id, begin in begins.items():
            outcome = outcomes.get(action_id)
            if outcome is None or outcome['executed'] is None:
                result['warnings'].append(f'{action_id}: unclosed/unknown execution')
            for allocation in begin['allocations']:
                op = ops[allocation['company_key']][allocation['operation_id']]
                if outcome is None or outcome['executed'] is None:
                    require(op['status'] in ('reserved', 'unknown'), 'unknown execution must hold credits')
                elif outcome['executed'] is False:
                    require(op['status'] == 'cancelled', 'nonexecution must have cancellation evidence')
                else:
                    require(op['status'] in ('settled', 'unknown'), 'executed action must settle or retain unknown charge')
        for key, ledger in ledgers.items():
            for op in ledger['operations']:
                if op['batch_id'] == state['batch_id']:
                    require((key, op['operation_id']) in used_ops, 'batch operation missing logged begin')
        result['next_step'] = state['next_step']
        result['all_completed'] = state['phase'] == 'closed' and bool(state['items']) and counts['completed'] == len(state['items']) and not result['errors'] and not result['warnings']
    except (ValueError, TypeError, KeyError, OSError, InvalidOperation, AttributeError) as exc:
        result['errors'].append(str(exc))
    result['exit_code'] = 1 if result['errors'] else 2 if result['warnings'] else 0
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    result = check_batch(Path(args.batch))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
