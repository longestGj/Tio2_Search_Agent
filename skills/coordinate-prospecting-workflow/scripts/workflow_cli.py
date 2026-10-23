"""Local workflow record CLI. Never dispatches agents or reads report semantics."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

from workflow_model import fingerprint, summarize
from workflow_store import (RecoveryRequired, atomic_bytes, atomic_json, commit_command, check_workflow,
                            load_state, project_path, read_json, recover_workflow, validate_workflow)

def validate_artifacts(project, artifacts):
    issues=[]
    for a in artifacts:
        try:
            p=project_path(project,a['path'])
            if not p.is_file():raise ValueError('missing file')
            expected=a['sha256']
            if not isinstance(expected,str) or len(expected)!=64:raise ValueError('sha256 required')
            if hashlib.sha256(p.read_bytes()).hexdigest()!=expected.lower():raise ValueError('source version mismatch')
        except (OSError,ValueError,KeyError,TypeError) as e:
            issues.append(dict(path=a.get('path') if isinstance(a,dict) else None,issue=str(e)))
    return issues

def render_progress(workflow,state):
    summary=summarize(state)
    def cell(v):return str(v).replace('|','\\|').replace('\n','<br>')
    lines=['# 任务与进度','',f"工作流：{state['task']['workflow_id']}；状态：{state['status']}；终点：{state['task']['target_stage']}",
           '',f"授权数量：{summary['requested']}；已选公司：{summary['selected']}；数量缺口：{summary['scope_shortfall']}。",
           f"草稿完成公司：{summary['outcomes']['draft_done']}；草稿文件：{summary['draft_files']}；全部草稿完成：{'是' if summary['all_drafts_done'] else '否'}。",
           '', '| 客户 ID | 当前阶段 | 执行状态 | 流程结果 | 阻塞原因 |','| --- | --- | --- | --- | --- |']
    for cid,c in state['companies'].items():lines.append('| '+' | '.join(cell(v) for v in (cid,c['stage'],c['status'],c['outcome'],c.get('blocked_reason',''))) +' |')
    lines+=['','统计仅反映进度和交接，不代表调度层进行了业务质量评估。','', '预算（未知消耗保留）：', '```json',json.dumps(state['task']['budgets'],ensure_ascii=False,indent=2),'```']
    todo=['# 交接与待办','',f"下一步：{summary['next_action']}；当前派发：{state['active_assignment']}；回执：{state['dispatch']}",'',
          '原始任务单位于 assignments/，专业交接单位于 handoffs/；历史位于 history/。','']
    for cid,c in state['companies'].items():
        todo += [f'## {cid}',f"恢复条件：{cell(c.get('resume_condition',''))}"]
        for h in c['history']:
            todo += [f"- {h['handoff_id']} / {h['stage']} / {h['execution_status']} → {h['route']} / {h['next_stage']}",
                     f"  专业原文：{cell(h['business_conclusion'])}；引用：{cell(h['conclusion_ref'])}；理由：{cell(h['route_reason'])}"]
            for a in h['artifacts']:todo.append(f"  成果：{cell(a['path'])}；SHA256：{a['sha256']}")
    files={'01_任务与进度.md':'\n'.join(lines)+'\n','02_交接与待办.md':'\n'.join(todo)+'\n'}
    hashes={}
    for name,body in files.items():
        data=body.encode('utf8');atomic_bytes(Path(workflow)/name,data);hashes[name]=hashlib.sha256(data).hexdigest()
    atomic_json(Path(workflow)/'projection.json',dict(state_sha256=fingerprint(state),files=hashes))

def execute(project,workflow,command):
    command=deepcopy(command)
    if command['op']=='receive':command['artifact_check']={'checked':True,'issues':[]}
    def validate(c):
        op=c['op'];artifacts=[]
        if op=='init':artifacts=c['task']['scope']['source_artifacts']
        elif op=='prepare':artifacts=c['assignment']['input_artifacts']
        elif op=='receive':artifacts=[a for i in c['handoff']['items'] for a in i['artifacts']]
        issues=validate_artifacts(project,artifacts)
        if issues:raise ValueError(json.dumps(issues,ensure_ascii=False))
    try:
        return commit_command(project,workflow,command,render=render_progress,validate=validate)
    except OSError as e:
        # A journal or claim may already be durable; never label this safe to retry.
        raise RecoveryRequired('persistence interrupted; inspect and recover before retry: '+str(e)) from e

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True);parser.add_argument('--workflow',required=True)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input');group.add_argument('--check',action='store_true');group.add_argument('--recover',action='store_true')
    args=parser.parse_args(argv)
    try:
        project=Path(args.project).resolve();workflow=validate_workflow(project,args.workflow)
        if args.input:state=execute(project,workflow,read_json(args.input))
        elif args.recover:state=recover_workflow(project,workflow,render=render_progress)
        else:state=check_workflow(project,workflow)
        result=summarize(state);result['workflow']=str(workflow)
        result['technical_issues']=list(result['technical_issues'])
        if state['dispatch']=='unknown':result['technical_issues'].append('dispatch_unknown: inspect original executor; never auto retry')
        if any(c.get('source_changed') or c.get('blocked_reason')=='source_changed' for c in state['companies'].values()):result['technical_issues'].append('source_changed')
        print(json.dumps(result,ensure_ascii=False));return 2 if result['technical_issues'] else 0
    except RecoveryRequired as e:
        print(json.dumps(dict(scope='progress_and_handoff_only',technical_issues=[str(e)],next_action='recover'),ensure_ascii=False));return 2
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(json.dumps(dict(scope='progress_and_handoff_only',error=str(e)),ensure_ascii=False));return 1

if __name__=='__main__':sys.exit(main())
