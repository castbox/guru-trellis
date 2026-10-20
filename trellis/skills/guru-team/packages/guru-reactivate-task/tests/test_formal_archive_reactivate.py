"""Actual matching SDK over preserved #503 bytes, with a controlled PR provider."""
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from unittest import mock

from test_delivery_reactivate import Fixture, owner, shared, PACKAGE
from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.delivery_projection.tests.upstream_fixture import public_task
from runtime.maintenance_transport import call
from runtime.task_lifecycle import TaskLifecycleKey, inspect_repository, BranchBindingStore
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.identity import resolve_task_id


class FormalArchiveReactivateTests(Fixture):
    def prepare_formal(self, adopt=True):
        selected = os.environ.get('TRELLIS_MAINTENANCE_CANDIDATE')
        if not selected:
            self.fail('Matching reviewed TRELLIS_MAINTENANCE_CANDIDATE is required; no SKIP proof.')
        candidate = json.loads(Path(selected).read_text())
        self.source = {'cli_package_root': candidate['cli_package_root'], 'dependency_mode': 'local_candidate',
                       'expected_candidate': candidate['candidate']}
        self.git(self.root, 'switch', '-qc', 'finish')
        archive_ref = '.trellis/tasks/archive/2026-10/10-08-503-mixed-task-identity-reservation'
        original = PACKAGE.parents[4] / archive_ref
        shutil.copytree(original, self.root / archive_ref)
        raw = json.loads((self.root / archive_ref / 'task.json').read_text())
        summary = json.loads((self.root / archive_ref / 'finish-summary.json').read_text())
        public = self.record_merge(archive_ref, summary['task']['artifact_dir'], raw['id'], raw['lifecycle_generation'])
        scope = authority_ref(self.root / archive_ref / 'prd.md', self.root)
        semantic = self.semantic(public, scope, adopt=adopt)
        inspected = call(self.source, 'inspectTaskTarget', {'root': str(self.root), 'key': public['archived_lifecycle'], 'task_ref': archive_ref})
        projection = public_task(raw)
        projection['lifecycle_generation'] = raw['lifecycle_generation'] + 1
        projection['accepted_scope'] = scope
        facts = shared.read_shared_archive(self.root, TaskLifecycleKey(**public['archived_lifecycle']), public['archive_anchor'])
        upstream = shared.formal_inspection(self.root, TaskLifecycleKey(**public['archived_lifecycle']), public['archive_anchor'], facts, self.source)
        upstream['root'] = semantic['acquisition'].get('target_path', str(self.root))
        upstream.update(active_ref=semantic['acquisition']['task_ref'], projection=projection,
                        artifacts=[{'path': row['path'], 'action': 'preserve', 'source': row['source']}
                                   for row in inspected['artifacts'] if row['kind'] == 'file' and row['path'] != archive_ref + '/task.json'],
                        legacy_facts=[{'field': field, 'disposition': 'source_snapshot', 'owner_id': 'guru-reactivate-task', 'reason': scope}
                                      for field in ('completedAt', 'commit', 'pr_url') if raw.get(field) is not None])
        semantic.update(source_ref=self.source, formal_input=upstream)
        return public, semantic, scope

    def test_original_sdk_preserves_archive_and_returns_real_successor(self):
        public, semantic, scope = self.prepare_formal()
        archive = self.root / public['archive_anchor']['archive_ref']
        before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
        output = owner.execute(self.root, public, semantic)
        self.assertEqual(output['lifecycle_generation'], 1)
        self.assertEqual(resolve_task_id(self.root, public['archived_lifecycle']['task_id']).task_ref, '.trellis/tasks/current')
        for path, payload in before.items():
            self.assertEqual((archive / path).read_bytes(), payload)
        original_call = owner.call
        with mock.patch.object(owner, 'call', wraps=original_call) as calls:
            self.assertEqual(owner.execute(self.root, public, semantic), output)
            self.assertFalse(any(row.args[1] == 'prepareFormalArchiveReactivation' for row in calls.call_args_list))
        self.assertEqual(DeliveryProjection(self.root, '.trellis/tasks/current').read_record()['completion_results'], [])

    def test_pending_reuses_frozen_public_operation_without_another_prepare(self):
        public, semantic, scope = self.prepare_formal()
        original_call = owner.call
        first = True
        def port(source, method, payload):
            nonlocal first
            if method == 'applyMaintenance' and first:
                first = False
                return {'status': 'pending', 'recovery_ref': str(self.root / '.trellis/.runtime/pending.json')}
            return original_call(source, method, payload)
        with mock.patch.object(owner, 'call', side_effect=port) as calls:
            pending = owner.execute(self.root, public, semantic)
            self.assertEqual(pending['exit_id'], 'resume_reactivation')
            self.assertNotIn('task_ref', pending)
            self.assertFalse((self.root / '.trellis/tasks/current').exists())
            output = owner.execute(self.root, public, semantic)
            self.assertEqual(output['lifecycle_generation'], 1)
            self.assertEqual(sum(row.args[1] == 'prepareFormalArchiveReactivation' for row in calls.call_args_list), 1)
            self.assertEqual(owner.execute(self.root, public, {**semantic, 'route': 'resume_reactivation'})['lifecycle_generation'], 1)

    def test_public_apply_survives_local_control_failure_and_recovers_same_operation(self):
        public, semantic, scope = self.prepare_formal(adopt=False)
        with mock.patch.object(owner.ResourceLedgerStore, 'establish_current', side_effect=LifecycleContractError('local_control_unavailable', 'resource_ledger', 'Retry the original local owner.')):
            with self.assertRaisesRegex(LifecycleContractError, 'local_control_unavailable'):
                owner.execute(self.root, public, semantic)
        target = Path(semantic['acquisition']['target_path'])
        self.assertTrue((target / '.trellis/tasks/current/task.json').is_file())
        before = (target / '.trellis/tasks/current/task.json').read_bytes()
        with mock.patch.object(owner, 'call', wraps=owner.call) as calls:
            output = owner.execute(self.root, public, semantic)
        key = TaskLifecycleKey(public['archived_lifecycle']['task_id'], 1)
        self.assertEqual(output['lifecycle_generation'], 1)
        self.assertEqual((target / '.trellis/tasks/current/task.json').read_bytes(), before)
        self.assertIsNotNone(BranchBindingStore(inspect_repository(target)).read(key))
        self.assertIsNotNone(ResourceLedgerStore(inspect_repository(target)).read_current(key))
        self.assertFalse(any(row.args[1] == 'prepareFormalArchiveReactivation' for row in calls.call_args_list))

    def test_archived_successor_reenters_same_owner_on_new_exact_anchor(self):
        public, semantic, scope = self.prepare_formal()
        owner.execute(self.root, public, semantic)
        projection = DeliveryProjection(self.root, '.trellis/tasks/current')
        key = {'task_id': public['archived_lifecycle']['task_id'], 'lifecycle_generation': 1}
        completion = {'result_id': 'completion:second', 'owner_id': 'guru-review-task-completion', 'evidence': [scope],
                      'lifecycle_generation': 1, 'accepted_scope': scope, 'delivery_result_ids': [], 'outcome': 'completed'}
        projection.apply({'api_version': '1.0', 'operation': 'complete_task', 'key': key, 'owner_role': 'completion', 'owner_id': completion['owner_id'], 'result': completion})
        closure = {'result_id': 'closure:second', 'owner_id': 'guru-complete-task-closure', 'evidence': [scope],
                   'lifecycle_generation': 1, 'completion_result_id': completion['result_id'], 'disposition': 'no_mutation', 'source_result': None}
        projection.apply({'api_version': '1.0', 'operation': 'close_task', 'key': key, 'owner_role': 'closure', 'owner_id': closure['owner_id'], 'result': closure})
        spec = importlib.util.spec_from_file_location('formal_finish_again', PACKAGE.parent / 'guru-finish-task/runtime/invoke.py')
        finish = importlib.util.module_from_spec(spec); spec.loader.exec_module(finish)
        archive_ref = '.trellis/tasks/archive/2026-10/current'
        finish.project_archive(self.root, {**key, 'task_ref': '.trellis/tasks/current', 'closure_result': closure}, Path('.trellis/tasks/current'), archive_ref, Path(archive_ref))
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'second archive')
        archive_head = self.git(self.root, 'rev-parse', 'HEAD')
        self.git(self.root, 'switch', '-q', 'main'); self.git(self.root, 'merge', '--no-ff', '-qm', 'Merge second bookkeeping', 'task-next')
        merge = self.git(self.root, 'rev-parse', 'HEAD')
        self.prs.append({'number': 2, 'merged_at': '2026-10-21T00:00:00Z', 'merge_commit_sha': merge,
                         'base': {'ref': 'main', 'repo': {'full_name': 'example/repository'}}})
        self.assertEqual(resolve_task_id(self.root, key['task_id']).task_ref, archive_ref)
        # The original owner first inspects the actual successor and reviews its new anchor.
        facts = shared.read_shared_archive(self.root, TaskLifecycleKey(**public['archived_lifecycle']), public['archive_anchor'])
        successor = shared.find_successor(self.root, TaskLifecycleKey(**public['archived_lifecycle']), public['archive_anchor'], facts, self.source)
        self.assertEqual(successor, {'key': key, 'task_ref': archive_ref})
        new_public = {**public, 'archived_lifecycle': key, 'archive_anchor': {**public['archive_anchor'], 'archive_ref': archive_ref,
                         'archive_commit': archive_head, 'original_task_ref': '.trellis/tasks/current'}}
        new_semantic = {**new_public, 'route': 'session_binding_recovery_required', 'reason_refs': ['reviewed new generation'],
                        'selected_base_ref': 'refs/heads/main', 'reviewed_base_head': merge, 'session_outcome': 'recovery_required',
                        'authority': scope, 'acquisition': {**semantic['acquisition'], 'lifecycle_generation': 2,
                            'branch_ref': 'refs/heads/task-third', 'decision_head': merge, 'transaction_id': 'reactivate:second', 'result_id': 'result:second'}}
        self.git(self.root, 'switch', '-qc', 'task-third')
        with mock.patch.object(owner, 'call', wraps=owner.call) as calls:
            output = owner.execute(self.root, new_public, new_semantic)
            self.assertEqual(output['lifecycle_generation'], 2)
            self.assertFalse(any(row.args[1] == 'prepareFormalArchiveReactivation' for row in calls.call_args_list))
