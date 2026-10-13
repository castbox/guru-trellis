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
