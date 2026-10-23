"""Pure progress state machine. Business conclusions are opaque producer data."""
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import math
import re

STAGES = ('market', 'research', 'contacts', 'draft')
ROUTES = {'advance', 'revisit', 'hold', 'end', 'finish'}

def require(ok, field):
    if not ok:
        raise ValueError(field)

def fields(obj, names):
    require(isinstance(obj, dict), 'object required')
    for name in names.split():
        require(name in obj, 'missing ' + name)

def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest()

def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]+', value), 'unsafe identifier')

def timestamp(value):
    require(isinstance(value, str) and datetime.fromisoformat(value).utcoffset() is not None, 'timezone required')

def unique(values):
    require(isinstance(values, list) and len(values) == len(set(values)), 'unique list required')
    for v in values: identifier(v)

def number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0

def validate_task(task):
    fields(task, 'schema workflow_id country request_ref entry_stage scope order capabilities budgets overall_budgets')
    require(task['schema'] == 1, 'schema')
    identifier(task['workflow_id'])
    require(re.fullmatch('[A-Z]{2}', task['country']) and task['request_ref'], 'country/request_ref')
    start, end = task['entry_stage'], task.get('target_stage', 'draft')
    require(start in STAGES and end in STAGES and STAGES.index(start) <= STAGES.index(end), 'stage range')
    scope = task['scope']
    fields(scope, 'mode requested_count baseline_ids selected_ids source_artifacts')
    require(scope['mode'] in ('explicit_ids','discovery_new'), 'scope.mode')
    require(isinstance(scope['requested_count'], int) and scope['requested_count'] >= 0, 'requested_count')
    unique(scope['baseline_ids']); unique(scope['selected_ids']); unique(task['order'])
    require(set(task['order']) <= set(scope['selected_ids']), 'order outside scope')
    require(len(scope['selected_ids']) <= scope['requested_count'], 'scope count')
    if scope['mode'] == 'discovery_new':
        require(start == 'market' and not set(scope['selected_ids']) & set(scope['baseline_ids']), 'new scope')
    for stage, cap in task['capabilities'].items():
        require(stage in STAGES, 'capability stage'); fields(cap, 'available role_path role_version')
        require(type(cap['available']) is bool, 'available')
        require(not cap['available'] or (cap['role_path'] and cap['role_version']), 'capability version')
    seen = set()
    for b in task['budgets']:
        fields(b, 'budget_id stage unit limit used unknown authorization_ref')
        require(b['budget_id'] not in seen and b['stage'] in STAGES and b['unit'], 'budget identity')
        seen.add(b['budget_id'])
        require(number(b['used']) and (b['limit'] is None or number(b['limit'])) and type(b['unknown']) is bool, 'budget values')
    for cap in task['overall_budgets']:
        fields(cap, 'unit limit'); require(number(cap['limit']), 'overall limit')

def available(state, stage):
    return state['task']['capabilities'].get(stage, {}).get('available', False)

def queue(state, company, stage):
    company.update(stage=stage, status='queued' if available(state,stage) else 'blocked',
                   blocked_reason='' if available(state,stage) else 'dependency_unavailable')

def add_companies(state, ids):
    for cid in ids:
        c = dict(outcome='active', history=[], draft_ids=[], draft_files={}, stop_requested=False, recovery_refs=[])
        queue(state,c,state['task']['entry_stage'])
        state['companies'][cid] = c

def new_state(task):
    task = deepcopy(task); task.setdefault('target_stage','draft'); validate_task(task)
    state = dict(schema=1, task=task, status='running', companies={}, assignments={}, handoffs={}, commands={},
                 active_assignment=None, dispatch=None, scope_frozen=task['scope']['mode']=='explicit_ids' or bool(task['scope']['selected_ids']),
                 technical_issues=[], source_changes=[], progress=[], release_evidence={},
                 budget_uncertainties={b['budget_id']:['baseline'] if b['unknown'] else [] for b in task['budgets']})
    add_companies(state,task['scope']['selected_ids'])
    return state

def check_budget(state, assignment):
    reservations=assignment['budget_reservations']
    budgets={b['budget_id']:b for b in state['task']['budgets']}
    require(set(reservations) <= set(budgets), 'unknown budget')
    for bid,b in budgets.items():
        r=reservations.get(bid,0); require(number(r), 'reservation')
        require(not r or b['stage']==assignment['stage'], 'budget stage')
        bounded=b['limit'] is not None or any(c['unit']==b['unit'] for c in state['task']['overall_budgets'])
        if b['stage']==assignment['stage']:
            require(not (bounded and b['unknown']), 'unknown budget consumption')
            if b['limit'] is not None: require(b['used']+r<=b['limit'], 'stage budget exceeded')
    for cap in state['task']['overall_budgets']:
        group=[b for b in budgets.values() if b['unit']==cap['unit']]
        require(not any(b['unknown'] for b in group), 'unknown overall consumption')
        require(sum(b['used']+reservations.get(b['budget_id'],0) for b in group)<=cap['limit'], 'overall budget exceeded')

def active(state, assignment_id=None):
    aid=state['active_assignment']; require(aid is not None, 'no active assignment')
    require(assignment_id is None or aid==assignment_id, 'assignment mismatch')
    return state['assignments'][aid]

def discovery_remaining(state):
    return state['task']['scope']['mode']=='discovery_new' and len(state['companies'])<state['task']['scope']['requested_count']

def release(state, evidence):
    aid=state['active_assignment']; state['release_evidence'][aid]=evidence
    state['active_assignment']=None;state['dispatch']=None

def apply_command(state, command):
    fields(command,'command_id op recorded_at'); identifier(command['command_id']); timestamp(command['recorded_at'])
    digest=fingerprint(command)
    if command['command_id'] in state['commands']:
        require(state['commands'][command['command_id']]==digest, 'command_id content conflict')
        return deepcopy(state)
    s=deepcopy(state); op=command['op']; task=s['task']
    require(s['status']!='closed' or op=='receive', 'closed workflow')
    if op=='init_scope':
        ids=command['selected_ids']; unique(ids)
        require(not s['scope_frozen'] and not s['active_assignment'] and command.get('evidence_ref'), 'scope already frozen or active')
        require(len(ids)<=task['scope']['requested_count'] and not set(ids)&set(task['scope']['baseline_ids']), 'scope exceeds request')
        task['scope']['selected_ids']=ids;task['order']=ids; s['scope_frozen']=True;add_companies(s,ids)
    elif op=='prepare':
        require(s['status']=='running' and not s['active_assignment'] and not s['technical_issues'], 'dispatch blocked')
        a=deepcopy(command['assignment']); fields(a,'assignment_id revision stage customer_ids input_artifacts owner allowed_routes budget_reservations resources')
        identifier(a['assignment_id']);unique(a['customer_ids'])
        require(a['assignment_id'] not in s['assignments'] and isinstance(a['revision'],int) and a['revision']>=1, 'assignment identity')
        stage=a['stage'];require(stage in STAGES and available(s,stage), 'dependency_unavailable')
        require(STAGES.index(task['entry_stage'])<=STAGES.index(stage)<=STAGES.index(task['target_stage']), 'stage scope')
        require(a['owner'] and set(a['allowed_routes'])<=ROUTES, 'owner/routes')
        require(a['customer_ids'] or (stage=='market' and discovery_remaining(s)), 'empty assignment')
        for cid in a['customer_ids']:
            require(cid in s['companies'], 'customer outside scope'); c=s['companies'][cid]
            require(c['outcome']=='active' and c['stage']==stage and c['status']=='queued', 'customer not ready')
            c['status']='running'
        check_budget(s,a)
        s['assignments'][a['assignment_id']]=a;s['active_assignment']=a['assignment_id'];s['dispatch']='unknown'
    elif op=='dispatched':
        a=active(s,command['assignment_id']);require(command.get('executor_ref'), 'executor_ref')
        if a.get('executor_ref'): require(a['executor_ref']==command['executor_ref'],'executor mismatch')
        a['executor_ref']=command['executor_ref'];s['dispatch']='confirmed'
    elif op=='reconcile_dispatch':
        a=active(s);require(command.get('evidence_ref'),'reconciliation evidence')
        require(s['dispatch']=='unknown','dispatch is already known')
        if command['resolution']=='existing_executor':
            require(command.get('executor_ref'),'executor_ref');a['executor_ref']=command['executor_ref'];s['dispatch']='confirmed'
        elif command['resolution']=='not_dispatched':
            for cid in a['customer_ids']: queue(s,s['companies'][cid],a['stage'])
            release(s,command['evidence_ref'])
        else: raise ValueError('resolution')
    elif op=='progress':
        active(s,command['assignment_id']);fields(command,'progress_ref');s['progress'].append(command)
    elif op=='receive':
        h=deepcopy(command['handoff']);fields(h,'handoff_id assignment_id revision producer stage issued_at batch_status released items budget_used uncertainty')
        identifier(h['handoff_id']);timestamp(h['issued_at']); require(type(h['released']) is bool,'released')
        if h['handoff_id'] in s['handoffs']:
            require(s['handoffs'][h['handoff_id']]==h,'handoff_id content conflict')
        else:
            require(h['assignment_id'] in s['assignments'],'unknown assignment');a=s['assignments'][h['assignment_id']]
            require(h['producer']==a['owner'] and h['stage']==a['stage'],'producer/stage mismatch')
            require(isinstance(h['revision'],int) and 0<=h['revision']<=a['revision'],'revision mismatch')
            # An older task revision is historical only, never reapplied.
            if h['revision']<a['revision']:
                s['handoffs'][h['handoff_id']]=h
            else:
                active(s,h['assignment_id'])
                require(command.get('artifact_check',{}).get('checked') is True,'artifact check required')
                require(not command['artifact_check'].get('issues'),'artifact check failed')
                ids=[i['customer_id'] for i in h['items']];unique(ids)
                discovery=a['stage']=='market' and not a['customer_ids'] and discovery_remaining(s)
                if discovery:
                    require(len(ids)+len(s['companies'])<=task['scope']['requested_count'] and not set(ids)&(set(task['scope']['baseline_ids'])|set(s['companies'])),'discovery scope')
                else: require(set(ids)==set(a['customer_ids']),'handoff must cover exact assignment scope')
                for i in h['items']:
                    fields(i,'customer_id execution_status business_conclusion conclusion_ref route next_stage route_reason resume_condition artifacts')
                    require(i['route'] in a['allowed_routes'] and i['route'] in ROUTES,'route')
                    require(i['execution_status'] in ('completed','blocked','cancelled'),'execution_status')
                    require(i['execution_status']!='completed' or bool(i['artifacts']),'completed requires artifact references')
                    require(i['conclusion_ref'] and i['route_reason'],'conclusion/route reference')
                    route=i['route'];stage=a['stage'];nxt=i['next_stage']
                    if route=='advance':
                        require(i['execution_status']=='completed' and stage!=task['target_stage'] and STAGES.index(stage)+1<len(STAGES) and nxt==STAGES[STAGES.index(stage)+1], 'invalid advance')
                    elif route=='finish':
                        require(stage==task['target_stage'] and i['execution_status']=='completed' and nxt is None,'finish before target')
                        if stage=='draft':
                            fields(i,'draft_ids draft_files');unique(i['draft_ids'])
                            require(i['draft_ids'] and set(i['draft_ids'])==set(i['draft_files']) and set(i['draft_files'].values())<=set(x['path'] for x in i['artifacts']),'draft mapping')
                    elif route=='revisit':
                        require(nxt in STAGES and STAGES.index(task['entry_stage'])<=STAGES.index(nxt)<=STAGES.index(stage) and i['resume_condition'],'revisit scope/condition')
                    else: require(nxt is None,'terminal route next_stage')
                # budget_used is cumulative for this assignment, preventing repeated interim charges.
                for bid,used in h['budget_used'].items():
                    budgets={b['budget_id']:b for b in task['budgets']};require(bid in budgets and budgets[bid]['stage']==a['stage'],'budget identity')
                    prev=a.setdefault('reported_used',{}).get(bid,0);require(number(used) and used>=prev,'nonmonotonic consumption')
                    budgets[bid]['used']+=used-prev;a['reported_used'][bid]=used
                for bid in h['uncertainty']:
                    bs=[b for b in task['budgets'] if b['budget_id']==bid];require(len(bs)==1 and bs[0]['stage']==a['stage'],'unknown uncertainty budget')
                    if a['assignment_id'] not in s['budget_uncertainties'][bid]:s['budget_uncertainties'][bid].append(a['assignment_id'])
                    bs[0]['unknown']=True
                s['handoffs'][h['handoff_id']]=h
                if h['released']:
                    for b in task['budgets']:
                        if b['stage']!=a['stage']:continue
                        bid=b['budget_id'];pending=s['budget_uncertainties'][bid]
                        if bid not in h['budget_used'] or bid in h['uncertainty']:
                            if a['assignment_id'] not in pending:pending.append(a['assignment_id'])
                        elif a['assignment_id'] in pending:pending.remove(a['assignment_id'])
                        b['unknown']=bool(pending)
                    if discovery:
                        task['scope']['selected_ids']+=ids;task['order']+=ids;s['scope_frozen']=True;add_companies(s,ids)
                    for i in h['items']:
                        c=s['companies'][i['customer_id']]; c['history'].append(dict(stage=a['stage'],handoff_id=h['handoff_id'],**i));c['status']=i['execution_status']
                        if c['stop_requested'] or i['execution_status']=='cancelled': c.update(outcome='cancelled',status='cancelled')
                        elif i['route']=='advance': queue(s,c,i['next_stage'])
                        elif i['route']=='revisit': c.update(stage=i['next_stage'],status='blocked',blocked_reason='revisit',resume_condition=i['resume_condition'])
                        elif i['route']=='hold': c.update(outcome='on_hold',status='blocked',blocked_reason='professional_hold',resume_condition=i['resume_condition'])
                        elif i['route']=='end': c.update(outcome='ended')
                        elif i['route']=='finish': c.update(outcome='draft_done' if a['stage']=='draft' else 'target_done',draft_ids=i.get('draft_ids',[]),draft_files=i.get('draft_files',{}))
                        if c.get('source_changed'):c.update(status='blocked',blocked_reason='source_changed')
                    release(s,h['handoff_id'])
    elif op=='reconcile_budget':
        require(not s['active_assignment'] and command.get('evidence_ref'),'budget reconciliation requires evidence and released executor')
        bs=[b for b in task['budgets'] if b['budget_id']==command['budget_id']];require(len(bs)==1,'budget identity')
        b=bs[0];pending=s['budget_uncertainties'][b['budget_id']];resolved=command['resolved_assignments']
        require(isinstance(resolved,list) and resolved and len(resolved)==len(set(resolved)) and set(resolved)<=set(pending),'unresolved budget references required')
        require(number(command['used']) and command['used']>=b['used'],'cannot erase known spending')
        b['used']=command['used'];s['budget_uncertainties'][b['budget_id']]=[x for x in pending if x not in resolved]
        b['unknown']=bool(s['budget_uncertainties'][b['budget_id']])
    elif op=='reopen':
        c=s['companies'][command['customer_id']];ref=command.get('evidence_ref')
        require(c['status']=='blocked' and ref and ref not in c['recovery_refs'] and not s['active_assignment'],'new recovery evidence required')
        c['recovery_refs'].append(ref);c['outcome']='active';c['source_changed']=False;queue(s,c,c['stage'])
    elif op=='source_change':
        require(command.get('evidence_ref'),'source evidence');s['source_changes'].append(command)
        for cid in command['customer_ids']:
            require(cid in s['companies'],'source change outside scope');c=s['companies'][cid]
            if c['status']!='running': c.update(status='blocked',blocked_reason='source_changed')
            else: c['source_changed']=True
    elif op in ('pause','resume'):
        s['status']='paused' if op=='pause' else 'running'
    elif op=='cancel':
        require(command.get('request_ref'),'cancel authorization')
        for cid in command['customer_ids']:
            c=s['companies'][cid]
            if c['status']=='running': c['stop_requested']=True
            elif c['outcome']=='active': c.update(status='cancelled',outcome='cancelled')
    elif op=='close':
        require(not s['active_assignment'],'active executor cannot close')
        closed=all(c['outcome']!='active' and not c.get('source_changed') for c in s['companies'].values()) and s['scope_frozen'] and len(s['companies'])==task['scope']['requested_count']
        require(closed or command.get('request_ref'),'unfinished scope requires user closure')
        s['status']='closed'
    else: raise ValueError('unknown operation')
    s['commands'][command['command_id']]=digest
    return s

def summarize(state):
    outcomes={k:0 for k in ('active','draft_done','target_done','on_hold','ended','cancelled')}
    stages={k:{x:0 for x in ('waiting','queued','running','completed','blocked','cancelled')} for k in STAGES}
    for c in state['companies'].values():
        outcomes[c['outcome']]+=1;stages[c['stage']][c['status']]+=1
    requested=state['task']['scope']['requested_count'];selected=len(state['companies'])
    ready=[cid for cid in state['task']['order']+list(state['companies']) if cid in state['companies'] and state['companies'][cid]['status']=='queued' and state['companies'][cid]['outcome']=='active']
    next_action='reconcile_dispatch' if state['dispatch']=='unknown' else 'wait_executor' if state['active_assignment'] else 'paused' if state['status']!='running' else 'prepare' if ready or discovery_remaining(state) else 'review_blockers_or_close'
    return dict(scope='progress_and_handoff_only',status=state['status'],outcomes=outcomes,stages=stages,selected=selected,requested=requested,
                scope_shortfall=max(0,requested-selected),draft_files=sum(len(c['draft_ids']) for c in state['companies'].values()),
                all_drafts_done=requested>0 and selected==requested and outcomes['draft_done']==requested,
                next_action=next_action,next_customer_ids=list(dict.fromkeys(ready)),
                blocked_reasons={cid:c.get('blocked_reason') for cid,c in state['companies'].items() if c['status']=='blocked'},
                budgets=state['task']['budgets'],budget_uncertainties=state['budget_uncertainties'],technical_issues=state['technical_issues'])
