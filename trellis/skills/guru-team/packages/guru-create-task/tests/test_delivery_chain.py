"""Real Guru creation and formal Planning transport, with installed upstream.

Synthetic contexts and semantic payloads prove this test layer only. Native
current-host observations and independent AI gates are recorded separately.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import test_contract as creation

PACKAGES = creation.PACKAGE.parent
sys.path.insert(0, str(PACKAGES / 'guru-author-task-plan/tests'))
import test_planning_chain as planning
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle.errors import LifecycleContractError


class CreateDeliveryChainTests(unittest.TestCase):
    def run_chain(self, context):
        environment = {k: v for k, v in os.environ.items()
                       if not k.startswith(('TRELLIS_', 'CODEX_', 'CLAUDE_', 'CURSOR_', 'GIT_'))}
        if context:
            environment['TRELLIS_CONTEXT_ID'] = context
        with patch.dict(os.environ, environment, clear=True):
            fixture = creation.CreateTaskTests('test_public_no_issue_creation_recovery_and_source_identity')
            fixture.setUp()
            self.addCleanup(fixture.doCleanups)
            root, ref = fixture.root.resolve(), fixture.ref
            (root / '.trellis/workflow.md').write_bytes((creation.SOURCE / 'trellis/workflows/guru-team/workflow.md').read_bytes())
            fixture.git('add', '.trellis/workflow.md')
            fixture.git('commit', '-qm', 'Current workflow fixture')
            head = fixture.git('rev-parse', 'HEAD')
            subprocess.run(['git', 'merge', '--ff-only', head], cwd=fixture.primary, check=True, capture_output=True)
            fixture.payload['creation']['reviewed_base_head'] = head
            fixture.payload['acquisition']['decision_head'] = head

            def create(payload):
                p = subprocess.run(['bash', str(creation.PACKAGE / 'scripts/invoke.sh'), '--root', str(root), '--input', '-'],
                    input=json.dumps(payload), text=True, capture_output=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
                return json.loads(p.stdout)

            created = create(fixture.payload)
            self.assertEqual(created['exit_id'], 'created', created)
            (root / 'README.md').write_text('Retained ordinary dirty content\n')
            note = root / 'user-note.txt'
            note.write_text('Retained untracked content\n')
            peer = subprocess.run([sys.executable, str(root / '.trellis/scripts/task.py'), 'create', 'Parallel Task',
                '--description', 'Independent untouched task', '--slug', 'parallel', '--task-id', 'parallel-task',
                '--schema-version', '2.0', '--source-json', '{"kind":"no_issue"}', '--base-branch', 'main', '--no-start'],
                cwd=root, text=True, capture_output=True)
            self.assertEqual(peer.returncode, 0, peer.stdout + peer.stderr)
            peer_path = next((root / '.trellis/tasks').glob('*parallel/task.json'))
            preserved = {p: p.read_bytes() for p in (peer_path, note, root / 'README.md')}
            refs, worktrees = fixture.git('show-ref'), fixture.git('worktree', 'list', '--porcelain')

            before = (root / ref / 'task.json').read_bytes()
            self.assertEqual(create({**fixture.payload, 'action': 'recover_created_task_result'}), created)
            self.assertEqual((root / ref / 'task.json').read_bytes(), before)
            projection = DeliveryProjection(root, ref)
            self.assertIsNone(projection.read_record()['accepted_scope'])
            self.assertEqual(projection.read_record()['deliveries'], [])

            chain = planning.PlanningChainTest()
            chain.root, chain.ref, chain.task = root, ref, root / ref
            chain.fixture = SimpleNamespace(projection=projection)
            (chain.task / 'prd.md').write_text('Whole Task requirements and observable overall acceptance.\n')
            overall = (chain.task / 'prd.md').read_bytes()
            source = [{'locator': 'README.md', 'section': 'Requirements', 'authority_kind': 'requirement'}]
            public = {'profile': 'task_scope_requirements', 'mode': 'workflow', 'task_ref': ref,
                      'source_selection': source, 'revision_refs': ['README.md#Requirements']}
            requirements = chain.author(public, {'exit_id': 'scope_requirements_ready', 'task_ref': ref, 'requirements_locator': ref + '/prd.md'})
            self.assertIsNone(projection.read_record()['accepted_scope'])
            scope_input = {'profile': 'task_scope_requirements_acceptance', 'mode': 'workflow',
                           **{k: requirements[k] for k in ('task_ref', 'requirements_locator')},
                           'source_selection': source, 'revision_refs': public['revision_refs']}
            scope = chain.command('guru-clarify-requirements', 'invoke-guru-clarify-requirements', ['--invocation', '-'],
                {'public_input': scope_input, 'owner_result': {'public_input': scope_input, 'typed_exit': 'scope_ready',
                 'reason': 'Fixture whole requirements reviewed.', 'ai_review_gate': {'status': 'passed', 'summary': 'Fixture transport only.'},
                 'source_selection': source, 'revision_refs': public['revision_refs'], 'scope_action': 'revised',
                 'authority': authority_ref(chain.task / 'prd.md', root)}})
            creation_input = {'profile': 'delivery_creation', 'mode': 'workflow', 'task_ref': ref, 'task_key': scope['task_key'],
                'scope_ref': {'authority': projection.read_record()['accepted_scope'], 'anchors': ['Overall acceptance']},
                'delivery_profile': 'pull_request', 'continuation_id': 'first-delivery', 'action': 'create'}

            def delivery(public):
                file = root / 'delivery-input.json'
                file.write_text(json.dumps(public))
                return chain.command('guru-create-delivery', 'invoke-guru-create-delivery', ['--input', str(file), '--owner-result', '-'],
                                     {'typed_exit': 'created', 'reason': 'Fixture exact independent slice.'})

            first = delivery(creation_input)
            self.assertEqual(first['exit_id'], 'created', first)
            self.assertEqual(delivery({**creation_input, 'action': 'recover_creation'}), first)
            chain.key = first['delivery_key']
            self.assertEqual({k: chain.key[k] for k in ('task_id', 'lifecycle_generation')}, scope['task_key'])
            self.assertEqual(len(projection.read_record()['deliveries']), 1)
            pending = list((root / '.trellis/.runtime/guru-team/delivery-creation').rglob('*.json'))
            self.assertEqual(len(pending), 0 if context else 1)
            if pending:
                self.assertEqual(json.loads(pending[0].read_text())['key'], chain.key)
                # A normal changed slice cannot consume or replace the original
                # no-context recovery input, even though the first output exists.
                wrong = {**creation_input, 'scope_ref': {**creation_input['scope_ref'], 'anchors': ['Different slice']}}
                prior = pending[0].read_bytes()
                self.assertEqual(delivery(wrong)['reason_code'], 'creation_input_changed')
                self.assertEqual(pending[0].read_bytes(), prior)
            else:
                record = (chain.task / 'task.json').read_bytes()
                self.assertEqual(delivery({**creation_input, 'continuation_id': 'another-slice'})['reason_code'], 'delivery_selection_conflict')
                self.assertEqual((chain.task / 'task.json').read_bytes(), record)

            chain.directory = projection.planning_directory(chain.key)
            (chain.directory / 'prd.md').write_text('Current independent Delivery requirements.\n')
            author_input = {'profile': 'delivery_initial_review', 'mode': 'workflow', 'task_ref': ref,
                            'delivery_key': chain.key, 'source_selection': source}
            ready_output = {'exit_id': 'requirements_ready', 'task_ref': ref, 'delivery_key': chain.key,
                            'candidate': {'design_facts': ['Existing official identity and transport owners.'], 'constraint_refs': ['README.md#Requirements']}}
            if context:
                with patch.dict(os.environ, {'TRELLIS_CONTEXT_ID': context + '-new-session'}):
                    unchanged = (chain.task / 'task.json').read_bytes()
                    rejected = chain.author(author_input, ready_output, expected=3)
                    self.assertEqual(rejected['code'], 'stale_identity')
                    # Available context without selection stays no-current;
                    # an explicit key must not turn it into implicit recovery.
                    self.assertEqual(projection.current(chain.key)['kind'], 'no_current_task')
                    self.assertEqual((chain.task / 'task.json').read_bytes(), unchanged)
            ready = chain.author(author_input, ready_output)
            self.assertFalse(list((root / '.trellis/.runtime/guru-team/delivery-creation').rglob('*.json')))
            candidate = chain.architecture(ready['candidate'])
            chain.docs()
            planned = chain.author({'profile': 'delivery_solution_planning', 'mode': 'workflow', 'task_ref': ref, 'delivery_key': chain.key,
                'architecture_assessment': {k: candidate[k] for k in ('planning_purpose','baseline_identity','constitution_identity','impact_kind','impact_reason')}},
                {'exit_id': 'plan_ready', 'task_ref': ref, 'delivery_key': chain.key})
            self.assertEqual(planned['exit_id'], 'plan_ready')
            self.assertEqual(chain.wording()['exit_id'], 'pass')
            final = chain.architecture()
            approved = chain.approve(final)
            self.assertEqual(approved['exit_id'], 'approved', approved)
            activation = {'profile': 'delivery_activation', 'mode': 'workflow', 'task_ref': ref, 'delivery_key': chain.key,
                          'planning_result_id': approved['planning_result_id'], 'action': 'activate'}
            file = root / 'activation-input.json'
            file.write_text(json.dumps(activation))
            activated = chain.command('guru-activate-delivery', 'invoke-guru-activate-delivery', ['--input', str(file), '--owner-result', '-'],
                                     {'typed_exit': 'delivery_started', 'reason': 'Fixture current approved plan transport.'})
            self.assertEqual(activated['exit_id'], 'delivery_started', activated)
            self.assertEqual(projection.current(chain.key)['delivery']['phase'], 'implementing')
            record = (chain.task / 'task.json').read_bytes()
            file.write_text(json.dumps({**activation, 'action': 'recover_activation'}))
            self.assertEqual(chain.command('guru-activate-delivery', 'invoke-guru-activate-delivery', ['--input', str(file), '--owner-result', '-'],
                {'typed_exit': 'delivery_started', 'reason': 'Fixture same-operation recovery.'}), activated)
            self.assertEqual((chain.task / 'task.json').read_bytes(), record)
            self.assertEqual((chain.task / 'prd.md').read_bytes(), overall)
            self.assertEqual(len(projection.read_record()['deliveries']), 1)
            planning_before = {path: path.read_bytes() for path in chain.directory.iterdir() if path.is_file()}
            self.assertEqual(create({**fixture.payload, 'action': 'recover_created_task_result'}), created)
            self.assertEqual((chain.task / 'task.json').read_bytes(), record)
            self.assertEqual({path: path.read_bytes() for path in planning_before}, planning_before)
            self.assertEqual(projection.current(chain.key)['delivery']['phase'], 'implementing')
            if not context:
                self.assertEqual(projection.current()['kind'], 'no_current_task')
                with self.assertRaises(LifecycleContractError):
                    projection.current({**chain.key, 'lifecycle_generation': 1})
                reason = {'result_id': 'fixture-stop', 'reason': projection.read_record()['accepted_scope'],
                          'scope_decision': projection.read_record()['accepted_scope'], 'evidence': [projection.read_record()['accepted_scope']]}
                projection.stop_implementation(chain.key, reason)
                self.assertEqual(projection.current(chain.key)['kind'], 'terminal_delivery')
                with self.assertRaisesRegex(LifecycleContractError, 'terminal_delivery'):
                    projection.select(chain.key)
            for path, content in preserved.items():
                self.assertEqual(path.read_bytes(), content)
            self.assertEqual(fixture.git('show-ref'), refs)
            self.assertEqual(fixture.git('worktree', 'list', '--porcelain'), worktrees)

    def test_real_guru_create_to_first_delivery_with_context(self):
        self.run_chain('guru548-chain')

    def test_real_guru_create_to_first_delivery_without_context(self):
        self.run_chain(None)


if __name__ == '__main__':
    unittest.main()
