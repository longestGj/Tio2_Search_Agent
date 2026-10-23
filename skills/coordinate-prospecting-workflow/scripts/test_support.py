from copy import deepcopy

NOW = '2026-10-22T10:00:00+08:00'

def make_task(**overrides):
    task = dict(schema=1, workflow_id='XX-WF-20261022-01', country='XX', request_ref='user:fixture',
                entry_stage='research', target_stage='draft', order=['C1'],
                scope=dict(mode='explicit_ids', requested_count=1, baseline_ids=[], selected_ids=['C1'], source_artifacts=[]),
                capabilities={s: dict(available=True, role_path='fixture', role_version='simulation') for s in ['market','research','contacts','draft']},
                budgets=[], overall_budgets=[])
    task.update(deepcopy(overrides))
    return task

def make_assignment(**overrides):
    a = dict(assignment_id='A1', revision=1, stage='research', customer_ids=['C1'], input_artifacts=[],
             owner='researcher', allowed_routes=['advance','revisit','hold','end','finish'], budget_reservations={}, resources=['company:XX:C1'])
    a.update(deepcopy(overrides))
    return a

def item(cid='C1', route='advance', stage='contacts', **overrides):
    i = dict(customer_id=cid, execution_status='completed', business_conclusion='专业原文', conclusion_ref='fixture:report',
             route=route, next_stage=stage, route_reason='专业决定', resume_condition='新证据', artifacts=[dict(path='fixture-report.md',sha256='0'*64)])
    i.update(deepcopy(overrides))
    return i

def make_handoff(**overrides):
    h = dict(handoff_id='H1', assignment_id='A1', revision=1, producer='researcher', stage='research', issued_at=NOW,
             batch_status='completed', released=True, items=[item()], budget_used={}, uncertainty=[])
    h.update(deepcopy(overrides))
    return h

def cmd(op, **kwargs):
    return dict(command_id=kwargs.pop('command_id', op), op=op, recorded_at=NOW, **kwargs)

def started(task=None, assignment=None):
    from workflow_model import new_state, apply_command
    s = apply_command(new_state(task or make_task()), cmd('prepare', assignment=assignment or make_assignment()))
    return apply_command(s, cmd('dispatched', assignment_id='A1', executor_ref='agent:fixture'))

def receive(state, handoff=None, **kwargs):
    from workflow_model import apply_command
    return apply_command(state, cmd('receive', handoff=handoff or make_handoff(), artifact_check={'checked':True,'issues':[]}, **kwargs))
