"""Formal Guru wrappers with a real installed schema2 Task and public Delivery.

Fixture semantic decisions are transport evidence, not native AI review proof.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
KERNEL = PACKAGE.parents[1]
sys.path.insert(0, str(PACKAGE.parent / 'guru-create-delivery/tests'))
from support import installed_fixture
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class PlanningChainTest(unittest.TestCase):
    def setUp(self):
        self.fixture = installed_fixture(self)
        self.root = self.fixture.root.resolve()
        self.ref = self.fixture.task_ref
        self.task = self.fixture.task
        self.key = self.fixture.create()
        self.directory = self.fixture.projection.planning_directory(self.key)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True, capture_output=True)
        subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Planning fixture'], cwd=self.root, check=True, capture_output=True)
        repo = inspect_repository(self.root)
        task_key = TaskLifecycleKey(self.key['task_id'], 0)
        BranchBindingStore(repo).establish(task_key, 'task')
        ResourceLedgerStore(repo).establish_current(task_key, binding_revision=0, branch_name='task', branch_ownership='caller_owned', worktree_ownership='not_applicable')

    def command(self, skill, command, args, value=None, expected=0):
        process = subprocess.run([sys.executable, '-m', 'runtime.command', str(PACKAGE.parent / skill), command, *args],
            cwd=self.root, text=True, input=json.dumps(value) if value is not None else None,
            capture_output=True, env={**os.environ, 'PYTHONPATH': str(KERNEL), 'PYTHONDONTWRITEBYTECODE': '1'})
        self.assertEqual(expected, process.returncode, process.stdout + process.stderr)
        response = json.loads(process.stdout)
        return response.get('result', response)

    def author(self, public, output, expected=0):
        path = self.root / 'author-public.json'
        path.write_text(json.dumps(public))
        return self.command(PACKAGE.name, 'invoke-guru-author-task-plan', ['--input', str(path), '--owner-result', '-'],
            {'public_input': public, 'output': output, 'ai_review_gate': {'status': 'passed', 'summary': 'Local fixture transport; semantic adequacy reviewed separately.'}}, expected=expected)

    def docs(self):
        for name in ('prd.md', 'design.md', 'implement.md'):
            (self.directory / name).write_text('Current independent Delivery plan.\n')
        for name in ('implement.jsonl', 'check.jsonl'):
            subprocess.run([sys.executable, str(self.root / '.trellis/scripts/task.py'), 'add-context', self.ref,
                name[:-6], '.trellis/workflow.md', 'Current workflow', '--delivery', self.key['delivery_id']],
                cwd=self.root, check=True, capture_output=True)

    def architecture_envelope(self, candidate=None):
        package = PACKAGE.parent / 'guru-maintain-architecture-baseline'
        public = json.loads((package / 'examples/public-input-candidate-assessment-3.0.json').read_text())
        public.update(schema_version='delivery-1.0', profile='delivery_task_impact_sync', task_locator=self.ref,
            delivery_key=self.key, planning_root=self.fixture.projection.resolve(self.key)['planning_root'])
        if candidate is not None:
            public['candidate'] = candidate
            current = digest(candidate) if 'design_locator' not in candidate else hashlib.sha256((self.root / candidate['design_locator']).read_bytes()).hexdigest()
        else:
            public.pop('candidate')
            public.update(planning_purpose='final_plan', design_locator=(self.directory / 'design.md').relative_to(self.root).as_posix())
            current = hashlib.sha256((self.directory / 'design.md').read_bytes()).hexdigest()
        public['freshness_identity'] = 'sha256:' + current
        constitution = self.root / public['constitution']['authority_locator']
        constitution.parent.mkdir(parents=True, exist_ok=True)
        constitution.write_text('Current fixture constitution.\n')
        owner = {k: copy.deepcopy(public[k]) for k in ('schema_version','profile','mode','continuation_id','stage','task_locator','baseline','constitution','project_contract','freshness_identity','planning_purpose','delivery_key','planning_root')}
        owner.update(input_sha256=digest(public), typed_exit='baseline_current', baseline_identity=public['baseline']['identity'],
            constitution_identity=public['constitution']['identity'], impact_kind='no_architecture_impact', impact_reason='Fixture uses the existing owner and transport.',
            consumer={'kind':'workflow','id':'guru-architecture-baseline-current-router'},
            ai_review_gate={'status':'passed','reviewed_scope':'Fixture current boundary','evidence_summary':'Fixture only','findings':[],'conclusion':'Existing responsibility retained.'})
        if candidate is None:
            owner['promotion_state'] = 'no_change'
        return {'public_input':public,'owner_result':owner}

    def architecture(self, candidate=None, expected=0):
        return self.command('guru-maintain-architecture-baseline', 'invoke-guru-maintain-architecture-baseline',
            ['--invocation','-'], self.architecture_envelope(candidate), expected=expected)

    def wording(self, changed=False):
        package = PACKAGE.parent / 'guru-review-contract-wording'
        selectors = ['--task',self.ref,'--delivery-key',json.dumps(self.key)]
        args = ['--mode','workflow','--profile','delivery_planning_artifacts',*selectors]
        path = self.directory / 'design.md'
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        if changed:
            path.write_text('Current equivalent independent Delivery plan.\n')
        scan = self.command(package.name,'record-contract-wording-review',[*args,'--scan-only'])
        gate = json.loads((package/'examples/contract-wording-review.json').read_text())['semantic_review']['ai_review_gate']
        gate.update(status='passed',checked_dimensions=dict.fromkeys(gate['checked_dimensions'],True),planning_checked_dimensions=dict.fromkeys((
            'no_requirement_weakening','source_issue_semantics_preserved','conditional_paths_have_conditions','no_parallel_implementation_paths',
            'gates_have_machine_verifiable_conditions','acceptance_criteria_are_deterministic','external_quotes_are_labeled_non_contract'),True))
        revisions = [] if not changed else [{'revision_id':'equivalent','locator':path.relative_to(self.root).as_posix(),'before_sha256':before,
            'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'reason':'Equivalent wording clarification.','rescan_sha256':scan['scan']['scan_sha256']}]
        record = self.command(package.name,'record-contract-wording-review',[*args,'--input','-'], {'typed_exit':'content_changed' if changed else 'pass',
            'classifications':[{'hit_id':row['hit_id'],'classification':'term_definition','reason':'Fixture definition.'} for row in scan['scan']['hits']],
            'ai_review_gate':gate,'revisions':revisions})
        checked = self.command(package.name,'check-contract-wording-review',[*selectors,'--input','-'],record)
        public = json.loads((package/'examples/public-delivery-planning-artifacts-input.json').read_text())
        public.update(task_ref=self.ref,delivery_key=self.key)
        return self.command(package.name,'invoke-guru-review-contract-wording',['--root',str(self.root),'--invocation','-'],
            {'public_input':public,'owner_result':record,'validation_receipt':checked['validation_receipt']})

    def approve(self, final, revision_actions=None):
        package=PACKAGE.parent/'guru-approve-task-plan'
        seed=json.loads((package/'examples/planning-approval-delivery.json').read_text())
        authored={k:seed[k] for k in ('mode','authority_refs','delivery_policy','docs_ssot_plan','semantic_review','typed_exit','consumer','reason')}
        if revision_actions:
            authored.update(typed_exit='revision_required',consumer={'kind':'workflow','id':'guru-task-plan-approval-revision-router'})
            authored['semantic_review'].update(status='revision_required',revision_actions=revision_actions)
        self.command(package.name,'record-planning-approval',['--task',self.ref,'--delivery-key',json.dumps(self.key),'--input','-'],authored)
        checked=self.command(package.name,'check-planning-approval',['--task',self.ref,'--delivery-key',json.dumps(self.key)])
        public=json.loads((package/'examples/public-delivery-initial-review-input-2.0.json').read_text())
        public.update(task_ref=self.ref,delivery_key=self.key,architecture_assessment={k:final[k] for k in ('planning_purpose','freshness_identity','baseline_identity','constitution_identity','constitution_status','impact_kind','promotion_state')})
        file=self.root/'approval-public.json';file.write_text(json.dumps(public))
        return self.command(package.name,'invoke-guru-approve-task-plan',['--input',str(file),'--owner-result',checked['artifact_path']])

    def test_first_schema2_task_scope_only_acceptance_then_creation(self):
        from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
        from runtime.task_lifecycle.identity import resolve_task_id
        # A real second independent fixture Task, never a rewritten aggregate.
        self.fixture.stop(self.key)
        subprocess.run(['git','checkout','-qb','scope-first'],cwd=self.root,check=True,capture_output=True)
        created=subprocess.run([sys.executable,str(self.root/'.trellis/scripts/task.py'),'create','Initial scope fixture',
            '--description','No accepted scope or Delivery yet','--slug','scope-first','--task-id','scope-first-task',
            '--schema-version','2.0','--source-json','{"kind":"no_issue"}','--base-branch','task','--no-start'],
            cwd=self.root,text=True,capture_output=True)
        self.assertEqual(created.returncode,0,created.stdout+created.stderr)
        self.ref=resolve_task_id(self.root,'scope-first-task').task_ref
        self.task=self.root/self.ref
        projection=DeliveryProjection(self.root,self.ref)
        self.assertIsNone(projection.read_record()['accepted_scope'])
        self.assertEqual(projection.read_record()['deliveries'],[])
        repo=inspect_repository(self.root)
        key=TaskLifecycleKey('scope-first-task',0)
        BranchBindingStore(repo).establish(key,'scope-first')
        ResourceLedgerStore(repo).establish_current(key,binding_revision=0,branch_name='scope-first',branch_ownership='caller_owned',worktree_ownership='not_applicable')
        # This fixture deliberately switches to a second Task. Establish that
        # official route before Creation; it must not overwrite the first route.
        projection._call(projection.api.delivery_session.set_active_task, str(self.task), self.root)
        (self.task/'prd.md').write_text('Whole Task requirements and overall acceptance.\n')
        selection=[{'locator':'docs/source.md','section':'Requirements','authority_kind':'requirement'}]
        public={'profile':'task_scope_requirements','mode':'workflow','task_ref':self.ref,'source_selection':selection,'revision_refs':['docs/source.md#Requirements']}
        ready=self.author(public,{'exit_id':'scope_requirements_ready','task_ref':self.ref,'requirements_locator':self.ref+'/prd.md'})
        self.assertIsNone(projection.read_record()['accepted_scope'])
        self.assertFalse((self.task/'design.md').exists())
        acceptance={'profile':'task_scope_requirements_acceptance','mode':'workflow',
            **{k:ready[k] for k in ('task_ref','requirements_locator')},'source_selection':selection,'revision_refs':public['revision_refs']}
        scope=self.command('guru-clarify-requirements','invoke-guru-clarify-requirements',['--invocation','-'],
            {'public_input':acceptance,'owner_result':{'public_input':acceptance,'typed_exit':'scope_ready','reason':'Whole requirements reviewed.',
             'ai_review_gate':{'status':'passed','summary':'Fixture scope-only positive behavior.'},'source_selection':selection,
             'revision_refs':public['revision_refs'],'scope_action':'revised','authority':authority_ref(self.task/'prd.md',self.root)}})
        creation={'profile':'delivery_creation','mode':'workflow','task_ref':self.ref,'task_key':scope['task_key'],
            'scope_ref':{'authority':projection.read_record()['accepted_scope'],'anchors':['Overall acceptance']},
            'delivery_profile':'pull_request','continuation_id':'scope-first-delivery','action':'create'}
        file=self.root/'creation-public.json';file.write_text(json.dumps(creation))
        delivered=self.command('guru-create-delivery','invoke-guru-create-delivery',['--input',str(file),'--owner-result','-'],
            {'typed_exit':'created','reason':'Explicit independent slice after actual scope acceptance.'})
        self.assertEqual(projection.current()['key'],delivered['delivery_key'])
        self.assertEqual(len(projection.read_record()['deliveries']),1)
        self.assertNotIn('status',projection.read_record())

    def test_real_chain_candidate_solution_wording_final_approval_revision_activation(self):
        original_seed=(self.directory/'design.md').read_bytes()
        (self.directory/'prd.md').write_text('Current Delivery requirements.\n')
        public={'profile':'delivery_initial_review','mode':'workflow','task_ref':self.ref,'delivery_key':self.key,'source_selection':[
            {'locator':'docs/source.md','section':'Design','authority_kind':'design_constraint'}]}
        ready=self.author(public,{'exit_id':'requirements_ready','task_ref':self.ref,'delivery_key':self.key,
            'candidate':{'design_facts':['One existing transport owner.'],'constraint_refs':['docs/source.md#Design']}})
        self.assertEqual((self.directory/'design.md').read_bytes(), original_seed)
        candidate=self.architecture(ready['candidate'])
        self.assertNotIn('promotion_state',candidate)
        self.docs()
        solution={'profile':'delivery_solution_planning','mode':'workflow','task_ref':self.ref,'delivery_key':self.key,
            'architecture_assessment':{k:candidate[k] for k in ('planning_purpose','baseline_identity','constitution_identity','impact_kind','impact_reason')}}
        planned=self.author(solution,{'exit_id':'plan_ready','task_ref':self.ref,'delivery_key':self.key})
        wording=self.wording(changed=True)
        self.author({'profile':'delivery_wording_reentry','mode':'workflow',**{k:wording[k] for k in ('task_ref','delivery_key','change_refs')}},planned)
        self.assertEqual(self.wording()['exit_id'],'pass')
        final=self.architecture()
        self.assertEqual(final['planning_purpose'],'final_plan')
        revision=self.approve(final, ['Specify actual current validation boundary.'])
        self.assertEqual(revision['revision_actions'],['Specify actual current validation boundary.'])
        self.author({'profile':'delivery_approval_revision','mode':'workflow',**{k:revision[k] for k in ('task_ref','delivery_key','revision_actions')}},planned)
        self.assertEqual(self.fixture.projection.resolve(self.key)['phase'],'planning')

    def test_all_eight_profiles_use_selected_public_planning_root(self):
        self.docs()
        interface=json.loads((PACKAGE/'interface.json').read_text())
        before=(self.task/'prd.md').read_bytes()
        for row in interface['public_contracts']['input']['profiles']:
            if row['id']=='task_scope_requirements':continue
            public=json.loads((PACKAGE/row['example']['path']).read_text());public.update(task_ref=self.ref,delivery_key=self.key)
            output={'exit_id':'plan_ready','task_ref':self.ref,'delivery_key':self.key}
            if row['id'] in {'delivery_initial_review','delivery_active_task_scope_change','delivery_requirements_revision','delivery_architecture_conflict_resolution'}:
                output.update(exit_id='requirements_ready',candidate={'design_locator':(self.directory/'design.md').relative_to(self.root).as_posix()})
            with self.subTest(profile=row['id']):self.assertEqual(output,self.author(public,output))
        self.assertEqual((self.task/'prd.md').read_bytes(),before)
        self.assertNotIn('status',self.fixture.projection.read_record())
