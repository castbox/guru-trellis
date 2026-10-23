"""Actual Clarify wrappers separate source judgment and public scope acceptance."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parent / 'guru-create-delivery/tests'))
from support import installed_fixture
from runtime.delivery_projection.adapter import authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


class DeliveryScopeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = installed_fixture(self)
        self.key = self.fixture.create()
        self.selection = [{'locator':'docs/source.md','section':'Requirements','authority_kind':'requirement'}]

    def public(self, profile):
        value=json.loads((PACKAGE/('examples/public-'+profile.replace('_','-')+'-input.json')).read_text())
        value['task_ref']=self.fixture.task_ref
        if profile=='delivery_active_task_scope_change':value['delivery_key']=self.key
        elif profile=='delivery_task_scope_revision':value['task_key']={k:self.key[k] for k in ('task_id','lifecycle_generation')}
        else:
            value.update(requirements_locator=self.fixture.task_ref+'/prd.md',source_selection=self.selection,revision_refs=['docs/source.md#Requirements'])
        return value

    def invoke(self, public, action='revised', expected=0, authority=None):
        owner={'public_input':public,'typed_exit':'scope_ready','reason':'Actual current requirements judgment.',
               'ai_review_gate':{'status':'passed','summary':'Fixture scope comparison; native review separately owned.'},
               'source_selection':self.selection,'revision_refs':['docs/source.md#Requirements'],'scope_action':action}
        if authority is not None:owner['authority']=authority
        result=subprocess.run([sys.executable,'-m','runtime.command',str(PACKAGE),'invoke-guru-clarify-requirements','--invocation','-'],
            cwd=self.fixture.root,env={**os.environ,'PYTHONPATH':str(PACKAGE.parents[1])},input=json.dumps({'public_input':public,'owner_result':owner}),text=True,capture_output=True)
        self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
        return json.loads(result.stdout)

    def test_source_judgment_does_not_publish_before_scope_only_author(self):
        before=self.fixture.projection.read_record()
        output=self.invoke(self.public('delivery_active_task_scope_change'))
        self.assertEqual(output['exit_id'],'scope_ready')
        self.assertEqual(output['source_selection'],self.selection)
        self.assertEqual(self.fixture.projection.read_record(),before)
        self.assertNotIn('task_key',output)

    def test_post_author_acceptance_publishes_current_requirements_and_recovers(self):
        plan=self.fixture.projection.planning_directory(self.key)/'design.md'
        before=plan.read_bytes()
        (self.fixture.task/'prd.md').write_text('Revised whole Task scope\n')
        authority=authority_ref(self.fixture.task/'prd.md',self.fixture.root)
        public=self.public('task_scope_requirements_acceptance')
        output=self.invoke(public,authority=authority)
        self.assertEqual(output['task_key'],{k:self.key[k] for k in ('task_id','lifecycle_generation')})
        self.assertEqual(self.fixture.projection.read_record()['accepted_scope'],authority)
        self.assertEqual(self.invoke(public,authority=authority),output)
        self.assertEqual(plan.read_bytes(),before)
        self.assertEqual(self.fixture.projection.resolve(self.key)['phase'],'planning')

    def test_whole_task_scope_acceptance_requires_no_current_delivery(self):
        self.fixture.stop(self.key)
        public=self.public('task_scope_requirements_acceptance')
        output=self.invoke(public,action='no_change',authority=self.fixture.scope)
        self.assertEqual(output['exit_id'],'scope_ready')
        self.assertEqual(self.fixture.projection.current()['kind'],'no_current_delivery')

    def test_normal_edit_between_author_and_scope_acceptance_is_stale(self):
        public=self.public('task_scope_requirements_acceptance')
        old=self.fixture.scope
        (self.fixture.task/'prd.md').write_text('New normal requirement edit\n')
        output=self.invoke(public,authority=old,expected=3)
        self.assertEqual(output['code'],'stale_identity')
        self.assertEqual(self.fixture.projection.read_record()['accepted_scope'],old)

    def test_withdrawal_intent_never_impersonates_stage_stop(self):
        output=self.invoke(self.public('delivery_active_task_scope_change'),action='withdrawal_required')
        self.assertEqual(output['scope_action'],'withdrawal_required')
        self.assertEqual(self.fixture.projection.current()['key'],self.key)
        self.fixture.stop(self.key)
        self.assertEqual(self.fixture.projection.resolve(self.key)['phase'],'stopped')

    def command(self, skill, command, arguments, value):
        result = subprocess.run([sys.executable, '-m', 'runtime.command',
            str(PACKAGE.parent / skill), command, *arguments], cwd=self.fixture.root,
            env={**os.environ, 'PYTHONPATH': str(PACKAGE.parents[1]), 'PYTHONDONTWRITEBYTECODE': '1'},
            input=json.dumps(value), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        return output.get('result', output)

    def test_scope_dispositions_cross_author_acceptance_and_original_consumer(self):
        """Public wrapper integration; fixture judgments are not native AI proof."""
        for current_delivery in (True, False):
            for action in ('revised', 'no_change', 'withdrawal_required'):
                with self.subTest(current_delivery=current_delivery, action=action):
                    self.setUp()
                    fixture = self.fixture
                    projection = fixture.projection
                    if not current_delivery:
                        fixture.stop(self.key)
                    subprocess.run(['git', 'add', '.'], cwd=fixture.root, check=True, capture_output=True)
                    subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '-qm', 'Current scope fixture'], cwd=fixture.root, check=True, capture_output=True)
                    repository = inspect_repository(fixture.root)
                    task_key = TaskLifecycleKey(self.key['task_id'], self.key['lifecycle_generation'])
                    BranchBindingStore(repository).establish(task_key, 'task')
                    ResourceLedgerStore(repository).establish_current(task_key, binding_revision=0,
                        branch_name='task', branch_ownership='caller_owned', worktree_ownership='not_applicable')
                    before = projection.read_record()
                    profile = 'delivery_active_task_scope_change' if current_delivery else 'delivery_task_scope_revision'
                    intent = self.invoke(self.public(profile), action=action)
                    self.assertNotIn('task_key', intent)
                    self.assertEqual(projection.read_record(), before)

                    if action != 'no_change':
                        (fixture.task / 'prd.md').write_text('Current whole requirements: ' + action + '\n')
                    public = {name: intent[name] for name in ('mode', 'task_ref', 'source_selection', 'revision_refs')}
                    public['profile'] = 'task_scope_requirements'
                    public_file = fixture.root / 'author-input.json'
                    public_file.write_text(json.dumps(public))
                    ready = self.command('guru-author-task-plan', 'invoke-guru-author-task-plan',
                        ['--input', str(public_file), '--owner-result', '-'],
                        {'public_input': public, 'output': {'exit_id': 'scope_requirements_ready',
                         'task_ref': fixture.task_ref, 'requirements_locator': fixture.task_ref + '/prd.md'},
                         'ai_review_gate': {'status': 'passed', 'summary': 'Controlled scope-only Author transport.'}})
                    self.assertEqual(projection.read_record(), before)
                    acceptance = {name: intent[name] for name in ('mode', 'source_selection', 'revision_refs')}
                    acceptance.update(profile='task_scope_requirements_acceptance',
                        task_ref=ready['task_ref'], requirements_locator=ready['requirements_locator'])
                    scope = authority_ref(fixture.task / 'prd.md', fixture.root)
                    accepted = self.invoke(acceptance, action=action, authority=scope)
                    self.assertEqual(projection.read_record()['accepted_scope'], scope)
                    self.assertIn('task_key', accepted)
                    accepted_prd = (fixture.task / 'prd.md').read_bytes()

                    if not current_delivery:
                        public = {'profile': 'delivery_completion', 'mode': 'workflow',
                            'task_ref': fixture.task_ref, 'task_key': accepted['task_key']}
                        public_file.write_text(json.dumps(public))
                        route = {'typed_exit': 'completed'} if action == 'withdrawal_required' else {
                            'typed_exit': 'additional_delivery_required', 'reason': {
                                'reason_code': 'accepted_work_remains', 'reason_refs': [fixture.task_ref + '/prd.md']}}
                        owner = {'profile': public['profile'], 'mode': public['mode'],
                            'reviewed_task_key': accepted['task_key'], 'reviewed_scope': scope,
                            'reviewed_delivery_result_ids': [], 'evidence': [scope],
                            'remaining_work_refs': [] if action == 'withdrawal_required' else ['Current accepted work'],
                            'result_id': 'completion:scope-consumer', 'route': route}
                        owner_file = fixture.root / 'completion-owner.json'
                        owner_file.write_text(json.dumps(owner))
                        result = self.command('guru-review-task-completion', 'invoke-guru-review-task-completion',
                            ['--input', str(public_file), '--semantic-result', str(owner_file)], owner)
                        self.assertEqual(result['exit_id'], route['typed_exit'])
                        self.assertEqual(projection.current()['kind'], 'no_current_delivery')
                    elif action == 'withdrawal_required':
                        public = {'profile': 'delivery_scope_withdrawal', 'mode': accepted['mode'],
                            'task_ref': fixture.task_ref, 'delivery_key': self.key}
                        public_file.write_text(json.dumps(public))
                        result = self.command('guru-activate-delivery', 'invoke-guru-activate-delivery',
                            ['--input', str(public_file), '--owner-result', '-'],
                            {'reviewed_delivery_key': self.key, 'result_id': 'stop:scope-consumer',
                             'reason': scope, 'scope_decision': scope, 'evidence': [scope]})
                        self.assertEqual(result['exit_id'], 'delivery_stopped')
                        self.assertEqual(projection.current()['kind'], 'no_current_delivery')
                    elif action == 'revised':
                        public = {name: accepted[name] for name in ('mode', 'task_ref', 'source_selection', 'revision_refs')}
                        public.update(profile='delivery_scope_revision', delivery_key=self.key,
                            scope_ref={'authority': scope, 'anchors': ['Current revised acceptance']})
                        public_file.write_text(json.dumps(public))
                        result = self.command('guru-activate-delivery', 'invoke-guru-activate-delivery',
                            ['--input', str(public_file), '--owner-result', '-'],
                            {'public_input': public, 'ai_review_gate': {'status': 'passed',
                             'summary': 'Current Planning owner reviewed the retained slice.'}})
                        self.assertEqual(result['exit_id'], 'delivery_scope_revised')
                        self.assertEqual(projection.resolve(self.key)['scope_ref'], public['scope_ref'])
                    else:
                        self.assertEqual(projection.resolve(self.key), before['deliveries'][0])
                    self.assertEqual((fixture.task / 'prd.md').read_bytes(), accepted_prd)
                    self.assertEqual(len(projection.read_record()['deliveries']), 1)
