"""Executable unittest coverage of current contracts and ordinary missing facts."""
import json
import subprocess
from pathlib import Path
from unittest import mock

from test_delivery_reactivate import Fixture, owner, shared, PACKAGE
from runtime.schema import validate_json
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.errors import LifecycleContractError


class ReactivateContractTests(Fixture):
    def test_current_interface_examples_and_unique_consumers(self):
        interface = json.loads((PACKAGE / 'interface.json').read_text())
        for output in interface['public_contracts']['outputs']:
            value = json.loads((PACKAGE / output['example']['path']).read_text())
            validate_json(value, PACKAGE / output['schema']['path'], output['exit_id'])
        self.assertEqual({row['id'] for row in interface['external_exits']},
                         {'reactivated_to_planning', 'session_binding_recovery_required', 'resume_reactivation', 'reactivate_blocked'})
        for projection in interface['public_contracts']['projections']:
            output = next(row for row in interface['public_contracts']['outputs'] if row['exit_id'] == projection['exit_id'])
            source = json.loads((PACKAGE / output['example']['path']).read_text())
            consumer = next(row for row in interface['public_contracts']['consumer_inputs'] if row['id'] == projection['consumer_input_id'])
            payload = source if projection['operation'] == 'direct' else {row['target']: source[row['source']] for row in projection['mappings']}
            validate_json(payload, PACKAGE / consumer['contract']['path'], projection['id'])

    def test_old_profile_and_source_correction_do_not_enter_current_executor(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        for profile, route in [('delivery_reactivate_completed_task', semantic['route']), (public['profile'], 'source_correction_required')]:
            with self.subTest(profile=profile, route=route), self.assertRaises(Exception):
                owner.execute(self.root, {**public, 'profile': profile}, {**semantic, 'profile': profile, 'route': route})
        self.assertFalse((self.root / '.trellis/tasks/current').exists())

    def test_unmerged_or_missing_archive_facts_block_before_acquisition(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        self.prs.clear()
        with self.assertRaisesRegex(LifecycleContractError, 'shared_archive_mismatch'):
            owner.execute(self.root, public, semantic)
        self.assertFalse((self.root / '.trellis/tasks/current').exists())

    def test_same_pending_resource_blocks(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        repository = inspect_repository(self.root); key = TaskLifecycleKey('stable-id', 0)
        branch = BranchBindingStore(repository).establish(key, 'task-next')
        ResourceLedgerStore(repository).establish_current(key, binding_revision=branch.binding_revision,
            branch_name='task-next', branch_ownership='guru_owned', worktree_ownership='not_applicable')
        with self.assertRaisesRegex(LifecycleContractError, 'branch_responsibility_pending'):
            owner.execute(self.root, public, semantic)

    def test_unrelated_old_pending_branch_does_not_block_new_generation(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        repository = inspect_repository(self.root); key = TaskLifecycleKey('stable-id', 0)
        self.git(self.root, 'branch', 'task-old')
        bindings = BranchBindingStore(repository)
        branch = bindings.establish(key, 'task-old')
        resources = ResourceLedgerStore(repository)
        resources.establish_current(key, binding_revision=branch.binding_revision,
            branch_name='task-old', branch_ownership='guru_owned', worktree_ownership='not_applicable')
        resources.seal_for_finish(key, finish_result_id='finish:old',
            finish_head=self.git(self.root, 'rev-parse', 'task-old'))
        before = resources.snapshot(key)
        self.assertEqual({row.state for row in resources.read(key).resources}, {'cleanup_pending'})

        result = owner.execute(self.root, public, semantic)

        self.assertEqual(result['exit_id'], 'session_binding_recovery_required')
        self.assertEqual(result['lifecycle_generation'], 1)
        self.assertEqual(resources.snapshot(key), before)
        self.assertEqual(bindings.read(key), branch)
        self.assertEqual(bindings.read(TaskLifecycleKey('stable-id', 1)).branch_name, 'task-next')
        self.assertEqual(self.git(self.root, 'branch', '--list', 'task-old').strip(), 'task-old')

    def test_other_task_branch_association_remains_a_conflict(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        BranchBindingStore(inspect_repository(self.root)).establish(TaskLifecycleKey('peer', 0), 'task-next')
        with self.assertRaisesRegex(LifecycleContractError, 'branch_responsibility_pending'):
            owner.execute(self.root, public, semantic)

    def test_github_failures_keep_stable_redacted_error_facts(self):
        # Exercise the actual adapter, separate from controlled PR-domain fixtures.
        self.provider.stop()
        for stderr, code in [('HTTP 401 authentication', 'github_auth_failed'), ('HTTP 403 forbidden', 'github_permission_denied'),
                             ('HTTP 404', 'github_repo_access_denied'), ('network unavailable', 'github_api_unavailable')]:
            with self.subTest(code=code), mock.patch.object(shared.shutil, 'which', return_value='/tool/gh'), mock.patch.object(shared.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', stderr)):
                with self.assertRaises(LifecycleContractError) as error:
                    shared.github_json('example/repository', 'commits/head/pulls')
                self.assertEqual(error.exception.code, code)
        with mock.patch.object(shared.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(LifecycleContractError, 'github_cli_missing'):
                shared.github_json('example/repository', 'commits/head/pulls')
        for payload in ['invalid JSON', '{}', '[{}]']:
            with self.subTest(payload=payload), mock.patch.object(shared.shutil, 'which', return_value='/tool/gh'), mock.patch.object(shared.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, payload, '')):
                with self.assertRaisesRegex(LifecycleContractError, 'github_response_incomplete'):
                    shared.github_json('example/repository', 'commits/head/pulls')

    def test_inconsistent_session_route_is_zero_write(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        output = owner.execute(self.root, public, {**semantic, 'session_outcome': 'explicit_task_mode'})
        self.assertEqual(output['reason_code'], 'session_route_mismatch')
        self.assertFalse((self.root / '.trellis/tasks/current').exists())
