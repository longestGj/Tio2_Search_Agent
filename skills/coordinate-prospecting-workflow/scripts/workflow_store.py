"""Single writer journal and conservative project resource claims. No network."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import hashlib
import os
from pathlib import Path
import tempfile

from workflow_model import apply_command, fingerprint, identifier, new_state, require, timestamp

class RecoveryRequired(ValueError):
    pass

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def project_path(project, value):
    project=Path(project).resolve();p=Path(value)
    if not p.is_absolute():p=project/p
    p=p.resolve()
    require(p.is_relative_to(project),'path outside project')
    return p

def validate_workflow(project, workflow):
    p=project_path(project,workflow);rel=p.relative_to(Path(project).resolve())
    require(len(rel.parts)==4 and rel.parts[0]=='markets' and rel.parts[2]=='workflows','workflow path must be markets/ISO2/workflows/ID')
    require(len(rel.parts[1])==2 and rel.parts[1].isupper(),'workflow country')
    identifier(rel.parts[3]);return p

def canonical_resource(project, kind, value):
    require(kind in ('pool','batch','company'),'resource kind')
    if kind=='pool':
        require(len(value)==2 and value.isalpha(),'pool country');return 'pool:'+value.upper()
    if kind=='company':
        country,cid=value.split(':',1);identifier(cid);require(len(country)==2 and country.isalpha(),'company country')
        return 'company:'+country.upper()+':'+cid
    return 'batch:'+os.path.normcase(str(project_path(project,value))).casefold()

def normalize_resources(project, resources):
    result=[]
    for r in resources:
        kind,value=r.split(':',1);result.append(canonical_resource(project,kind,value))
    return sorted(set(result))

def atomic_json(path, data):
    atomic_bytes(path,(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf8'))

def atomic_bytes(path, data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.wf-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if Path(tmp).exists():Path(tmp).unlink()

@contextmanager
def lock(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    try: fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    except FileExistsError: raise ValueError('lock exists; verify writer before manual recovery: '+str(path)) from None
    try:
        with os.fdopen(fd,'w',encoding='utf8') as f:
            json.dump({'pid':os.getpid(),'created_at':datetime.now(timezone.utc).isoformat()},f);f.flush();os.fsync(f.fileno())
        yield
    finally:path.unlink()

def runtime(project):return Path(project).resolve()/'.codex/workflow-runtime'

def _claim(project,workflow,assignment_id,resources):
    path=runtime(project)/'resource-owners.json';registry=read_json(path) if path.exists() else {}
    owner=os.path.normcase(str(Path(workflow).resolve()))
    keys=normalize_resources(project,resources)
    for key in keys:
        existing=registry.get(key)
        require(not existing or (existing['workflow']==owner and existing['assignment_id']==assignment_id),'resource already owned: '+key)
    for key in keys:
        registry.setdefault(key,dict(workflow=owner,assignment_id=assignment_id,owner=owner,claimed_at=datetime.now(timezone.utc).isoformat()))
    atomic_json(path,registry)

def claim_resources(project,workflow,assignment_id,resources):
    project_path(project,workflow);identifier(assignment_id)
    with lock(runtime(project)/'.registry.lock'):_claim(project,workflow,assignment_id,resources)

def _release(project,workflow,assignment_id,release_ref,state):
    require(state['release_evidence'].get(assignment_id)==release_ref,'release needs recorded evidence')
    path=runtime(project)/'resource-owners.json';registry=read_json(path) if path.exists() else {}
    owner=os.path.normcase(str(Path(workflow).resolve()))
    registry={k:v for k,v in registry.items() if not (v['workflow']==owner and v['assignment_id']==assignment_id)}
    atomic_json(path,registry)

def release_resources(project,workflow,assignment_id,release_ref):
    workflow=validate_workflow(project,workflow)
    with lock(runtime(project)/'.registry.lock'),lock(workflow/'.writer.lock'):
        _release(project,workflow,assignment_id,release_ref,load_state(workflow))

def append_event(path,event):
    with Path(path).open('ab') as f:
        f.write((json.dumps(event,ensure_ascii=False,sort_keys=True,allow_nan=False)+'\n').encode('utf8'));f.flush();os.fsync(f.fileno())

def journal(workflow):
    path=Path(workflow)/'events.jsonl'
    if not path.exists():raise RecoveryRequired('missing journal')
    raw=path.read_bytes()
    if not raw or not raw.endswith(b'\n'):raise RecoveryRequired('truncated journal; bytes preserved')
    rows=[];state=None
    try:
        for line in raw.splitlines():
            row=json.loads(line);require(row['seq']==len(rows)+1 and row['schema']==1,'journal sequence')
            c=row['command'];require(row['event_id']==c['command_id'] and row['recorded_at']==c['recorded_at'],'event identity')
            if state is None:
                require(c['op']=='init','journal init');state=new_state(c['task']);state['commands'][c['command_id']]=fingerprint(c)
            else: state=apply_command(state,c)
            require(state==row['state_after'],'journal replay mismatch');rows.append(row)
    except (ValueError,KeyError,TypeError) as e:raise RecoveryRequired('invalid journal; bytes preserved: '+str(e)) from e
    return rows

def immutable_records(rows):
    for row in rows:
        c=row['command']
        if c['op']=='prepare':
            a=c['assignment'];yield 'assignments/'+a['assignment_id']+'-r'+str(a['revision'])+'.json',a
        elif c['op']=='receive':
            h=c['handoff'];yield 'handoffs/'+h['handoff_id']+'-r'+str(h['revision'])+'.json',h

def check_records(workflow,rows,repair=False):
    for relative,record in immutable_records(rows):
        path=Path(workflow)/relative
        if path.exists():
            try: same=read_json(path)==record
            except ValueError:same=False
            if not same:raise RecoveryRequired('immutable record conflict: '+relative)
        elif repair:atomic_json(path,record)
        else:raise RecoveryRequired('missing record: '+relative)

def load_state(workflow):
    workflow=Path(workflow);rows=journal(workflow);expected=rows[-1]['state_after']
    try:actual=read_json(workflow/'state.json')
    except (OSError,ValueError) as e:raise RecoveryRequired('missing/invalid state snapshot') from e
    if actual!=expected:raise RecoveryRequired('snapshot behind journal')
    check_records(workflow,rows)
    # CLI adds a projection receipt; a stale receipt is never silently ignored.
    receipt=workflow/'projection.json'
    if (workflow/'projection-required.json').exists():
        if not receipt.exists() or read_json(receipt).get('state_sha256')!=fingerprint(expected):
            raise RecoveryRequired('progress reports behind journal')
        for name,digest in read_json(receipt)['files'].items():
            p=workflow/name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
                raise RecoveryRequired('progress report missing or modified')
    return actual

def assignment_resources(state,a):
    country=state['task']['country']
    required=['company:'+country+':'+cid for cid in a['customer_ids']]
    if a['stage']=='market':required+=['pool:'+country]
    return a['resources']+required

def check_active_claims(project,workflow,state):
    aid=state['active_assignment']
    if not aid:return
    path=runtime(project)/'resource-owners.json'
    registry=read_json(path) if path.exists() else {}
    owner=os.path.normcase(str(Path(workflow).resolve()))
    for key in normalize_resources(project,assignment_resources(state,state['assignments'][aid])):
        r=registry.get(key,{})
        if r.get('workflow')!=owner or r.get('assignment_id')!=aid:
            raise RecoveryRequired('active resource ownership missing/conflicting: '+key)

def save_snapshot(workflow,state,seq):
    path=workflow/'state.json'
    if path.exists():
        raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        backup=workflow/'history'/f'{seq-1:06d}-{digest[:24]}.json'
        if backup.exists():
            if backup.read_bytes()!=raw:raise RecoveryRequired('history snapshot conflict')
        else:atomic_bytes(backup,raw)
    atomic_json(path,state)

def commit_command(project,workflow,command,render=None,validate=None):
    workflow=validate_workflow(project,workflow)
    with lock(runtime(project)/'.registry.lock'),lock(workflow/'.writer.lock'):
        if command['op']=='init':
            if (workflow/'events.jsonl').exists():
                state=load_state(workflow);check_active_claims(project,workflow,state)
                require(state['commands'].get(command['command_id'])==fingerprint(command),'workflow exists; init content mismatch')
                return state
            require(not (workflow/'events.jsonl').exists() and not (workflow/'state.json').exists(),'workflow exists')
            identifier(command['command_id']);timestamp(command['recorded_at'])
            state=new_state(command['task']);require(state['task']['country']==workflow.parent.parent.name and state['task']['workflow_id']==workflow.name,'workflow/task identity')
            state['commands'][command['command_id']]=fingerprint(command);rows=[];before=None
        else:
            before=load_state(workflow);check_active_claims(project,workflow,before);state=apply_command(before,command)
            if state==before:return state
            rows=journal(workflow)
        historical=False
        if before and command['op']=='receive':
            h=command['handoff'];a=before['assignments'][h['assignment_id']]
            historical=h['handoff_id'] in before['handoffs'] or h['revision']<a['revision']
        if validate and not historical:validate(command)
        if command['op']=='prepare':
            a=command['assignment']
            _claim(project,workflow,a['assignment_id'],assignment_resources(state,a))
        if render:atomic_json(workflow/'projection-required.json',{'required':True})
        row=dict(schema=1,seq=len(rows)+1,event_id=command['command_id'],recorded_at=command['recorded_at'],command=command,state_after=state)
        append_event(workflow/'events.jsonl',row);rows.append(row)
        save_snapshot(workflow,state,len(rows));check_records(workflow,rows,repair=True)
        for aid,ref in state['release_evidence'].items():_release(project,workflow,aid,ref,state)
        if render:
            try:render(workflow,state)
            except OSError as e:raise RecoveryRequired('progress save failed; recover required') from e
        return state

def check_workflow(project,workflow):
    workflow=validate_workflow(project,workflow)
    if not (workflow/'events.jsonl').exists():raise RecoveryRequired('missing workflow journal')
    with lock(runtime(project)/'.registry.lock'),lock(workflow/'.writer.lock'):
        state=load_state(workflow);check_active_claims(project,workflow,state);return state

def recover_workflow(project,workflow,render=None):
    workflow=validate_workflow(project,workflow)
    with lock(runtime(project)/'.registry.lock'),lock(workflow/'.writer.lock'):
        rows=journal(workflow);state=rows[-1]['state_after'];check_active_claims(project,workflow,state)
        # Detect immutable conflicts before changing any derived state.
        for relative,record in immutable_records(rows):
            p=workflow/relative
            if p.exists() and read_json(p)!=record:raise RecoveryRequired('immutable record conflict: '+relative)
        save_snapshot(workflow,state,len(rows));check_records(workflow,rows,repair=True)
        for aid,ref in state['release_evidence'].items():_release(project,workflow,aid,ref,state)
        if render:render(workflow,state)
        return state
