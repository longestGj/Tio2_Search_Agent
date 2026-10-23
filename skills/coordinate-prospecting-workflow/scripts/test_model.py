import unittest
from copy import deepcopy
from test_support import *
from workflow_model import new_state, apply_command, summarize

class ModelTests(unittest.TestCase):
    def test_scope_new_five_not_sixty_five(self):
        t = make_task(entry_stage='market', order=[], scope=dict(mode='discovery_new', requested_count=5, baseline_ids=[f'B{i}' for i in range(65)], selected_ids=[], source_artifacts=[]))
        s = new_state(t)
        ids = [f'N{i}' for i in range(5)]
        s = apply_command(s, cmd('init_scope', selected_ids=ids, evidence_ref='market:handoff'))
        self.assertEqual(list(s['companies']), ids)
        for bad in [['B1'], ids+['N5']]:
            with self.assertRaises(ValueError): apply_command(new_state(t), cmd('init_scope', selected_ids=bad, evidence_ref='x'))
        with self.assertRaises(ValueError): apply_command(s, cmd('init_scope', command_id='expand', selected_ids=['N9'], evidence_ref='x'))

    def test_unknown_dispatch_blocks_duplicate(self):
        s = apply_command(new_state(make_task()), cmd('prepare', assignment=make_assignment()))
        self.assertEqual(s['dispatch'], 'unknown')
        with self.assertRaises(ValueError): apply_command(s, cmd('prepare', command_id='again', assignment=make_assignment(assignment_id='A2')))
        s = apply_command(s, cmd('reconcile_dispatch', resolution='not_dispatched', evidence_ref='lookup:none'))
        self.assertIsNone(s['active_assignment'])

    def test_idempotence_and_old_revision(self):
        s = started(); c = cmd('receive', handoff=make_handoff(), artifact_check={'checked':True,'issues':[]})
        out = apply_command(s,c)
        self.assertEqual(apply_command(out,c),out)
        self.assertEqual(s['companies']['C1']['stage'],'research')
        with self.assertRaises(ValueError): apply_command(out,cmd('receive',handoff=make_handoff(released=False),artifact_check={'checked':True,'issues':[]}))
        old = receive(out,make_handoff(handoff_id='old',revision=0),command_id='old')
        self.assertEqual(old['companies'],out['companies'])

    def test_release_and_technical_gate(self):
        s = receive(started(),make_handoff(released=False))
        self.assertEqual(s['companies']['C1']['stage'],'research')
        self.assertIsNotNone(s['active_assignment'])
        with self.assertRaises(ValueError): apply_command(started(),cmd('receive',handoff=make_handoff()))

    def test_revisit_needs_new_condition(self):
        s = receive(started(),make_handoff(items=[item(route='revisit',stage='research')]))
        self.assertEqual(s['companies']['C1']['stage'],'research')
        self.assertEqual(s['companies']['C1']['status'],'blocked')
        with self.assertRaises(ValueError): apply_command(s,cmd('reopen',customer_id='C1',evidence_ref=''))
        s = apply_command(s,cmd('reopen',customer_id='C1',evidence_ref='new:1'))
        self.assertEqual(s['companies']['C1']['status'],'queued')

    def test_missing_capability_retains_target(self):
        t=make_task();t['capabilities']['contacts']['available']=False
        s=receive(started(t))
        self.assertEqual(s['companies']['C1']['blocked_reason'],'dependency_unavailable')
        self.assertEqual(s['task']['target_stage'],'draft')

    def test_hold_and_stage_only_finish(self):
        s=receive(started(),make_handoff(items=[item(route='hold',stage=None)]))
        s=apply_command(s,cmd('close'))
        self.assertEqual(s['status'],'closed')
        self.assertFalse(summarize(s)['all_drafts_done'])
        s=receive(started(make_task(target_stage='research')),make_handoff(items=[item(route='finish',stage=None)]))
        self.assertEqual(s['companies']['C1']['outcome'],'target_done')
        self.assertEqual(summarize(s)['draft_files'],0)

    def test_drafts_count_companies_separately(self):
        t=make_task(entry_stage='draft')
        a=make_assignment(stage='draft')
        i=item(route='finish',stage=None,draft_ids=['D1','D2','D3'],draft_files={x:'report' for x in ['D1','D2','D3']},artifacts=[{'path':'report','sha256':'0'*64}])
        s=receive(started(t,a),make_handoff(stage='draft',items=[i]))
        self.assertEqual(summarize(s)['outcomes']['draft_done'],1)
        self.assertEqual(summarize(s)['draft_files'],3)

    def test_zero_and_cancel_running(self):
        t=make_task(order=[],scope=dict(mode='explicit_ids',requested_count=0,baseline_ids=[],selected_ids=[],source_artifacts=[]))
        self.assertFalse(summarize(new_state(t))['all_drafts_done'])
        s=apply_command(started(),cmd('cancel',customer_ids=['C1'],request_ref='user:stop'))
        self.assertEqual(s['companies']['C1']['status'],'running')
        self.assertTrue(s['companies']['C1']['stop_requested'])

    def test_scope_and_route_rejected(self):
        with self.assertRaises(ValueError): receive(started(),make_handoff(items=[item('OUT')]))
        with self.assertRaises(ValueError): receive(started(),make_handoff(items=[item(stage='draft')]))
        with self.assertRaises(ValueError): receive(started(),make_handoff(items=[item(route='finish',stage=None)]))

    def test_budget_reservations_and_unknown(self):
        b=dict(budget_id='b',stage='research',unit='queries',limit=10,used=2,unknown=False,authorization_ref='user:cap')
        t=make_task(budgets=[b],overall_budgets=[dict(unit='queries',limit=5)])
        with self.assertRaises(ValueError): started(t,make_assignment(budget_reservations={'b':4}))
        b['unknown']=True
        with self.assertRaises(ValueError): started(make_task(budgets=[b]),make_assignment(budget_reservations={'b':1}))
        s=started(make_task(budgets=[dict(b,unknown=False)]),make_assignment(budget_reservations={'b':3}))
        s=receive(s,make_handoff(budget_used={'b':2}))
        self.assertEqual(s['task']['budgets'][0]['used'],4)

    def test_source_change_does_not_expand(self):
        s=apply_command(new_state(make_task()),cmd('source_change',customer_ids=['C1'],evidence_ref='v2'))
        self.assertEqual(list(s['companies']),['C1'])
        self.assertEqual(s['companies']['C1']['blocked_reason'],'source_changed')

    def test_running_source_change_blocks_downstream(self):
        s=apply_command(started(),cmd('source_change',customer_ids=['C1'],evidence_ref='v2'))
        s=receive(s)
        self.assertEqual(s['companies']['C1']['status'],'blocked')
        with self.assertRaises(ValueError):apply_command(s,cmd('prepare',command_id='next',assignment=make_assignment(assignment_id='A2',stage='contacts')))

    def test_omitted_final_budget_is_unknown_not_zero(self):
        b=dict(budget_id='b',stage='research',unit='queries',limit=10,used=2,unknown=False,authorization_ref='user:cap')
        s=receive(started(make_task(budgets=[b]),make_assignment(budget_reservations={'b':3})))
        self.assertTrue(s['task']['budgets'][0]['unknown'])

    def test_empty_discovery_cannot_silently_close_shortfall(self):
        t=make_task(entry_stage='market',order=[],scope=dict(mode='discovery_new',requested_count=5,baseline_ids=[],selected_ids=[],source_artifacts=[]))
        s=apply_command(new_state(t),cmd('init_scope',selected_ids=[],evidence_ref='market:none'))
        with self.assertRaises(ValueError):apply_command(s,cmd('close'))

if __name__=='__main__': unittest.main()
