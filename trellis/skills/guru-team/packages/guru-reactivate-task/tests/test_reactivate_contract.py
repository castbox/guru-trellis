"""Executable unittest coverage of current contracts and ordinary missing facts."""
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from test_delivery_reactivate import Fixture, owner, shared, PACKAGE
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.errors import LifecycleContractError


def _record_contract_receipt(receipt):
    destination = os.environ.get('GURU_TERMINAL_ERROR_RECEIPTS')
    if destination:
        with Path(destination).open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(receipt, ensure_ascii=False) + '\n')


def _contract_command(argv):
    result = subprocess.run(argv, capture_output=True, text=True)
    _record_contract_receipt({
        'boundary': 'public_command', 'argv': argv, 'cwd': str(Path.cwd()),
        'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
    })
    return result


class TerminalInvocationErrorContractTests(unittest.TestCase):
    def test_reactivate_invocation_errors_follow_declared_error_contract(self):
        public = str(PACKAGE / 'examples/public-input.json')
        semantic = str(PACKAGE / 'examples/semantic-result.json')
        for case, expected_code, expected_field in [
            ('duplicate_input', 'conflicting_arguments', 'arguments.--input'),
            ('help_with_arguments', 'conflicting_arguments', 'arguments'),
            ('missing_semantic', 'invalid_arguments', 'arguments'),
        ]:
            with self.subTest(case=case):
                arguments = {
                    'duplicate_input': ['--input', public, '--input', public, '--semantic-result', semantic],
                    'help_with_arguments': ['--help', '--input', public],
                    'missing_semantic': ['--input', public],
                }[case]
                result = _contract_command(['bash', str(PACKAGE / 'scripts/invoke.sh'), *arguments])
                self.assertEqual(result.returncode, 2, (result.stdout, result.stderr))
                error = json.loads(result.stdout)
                self.assertEqual((error['code'], error['field_path']), (expected_code, expected_field))
                if case != 'missing_semantic':
                    self.assertEqual(result.stderr, '')
                interface = json.loads((PACKAGE / 'interface.json').read_text())
                invocation = interface['public_contracts']['invocation']
                validate_json(error, PACKAGE / invocation['error_schema']['path'], 'invocation_error')
                error_example = json.loads((PACKAGE / invocation['error_example']['path']).read_text())
                validate_json(error_example, PACKAGE / invocation['error_schema']['path'], 'error_example')
                self.assertTrue(any(row['path'] == invocation['error_schema']['path'] for row in interface['schemas']))
                self.assertTrue(any(row['path'] == invocation['error_example']['path'] for row in interface['artifacts']))
                self.assertEqual(json.loads((PACKAGE / invocation['error_schema']['path']).read_text())['$id'],
                                 invocation['error_schema']['schema_id'])
                validate_json(interface, PACKAGE.parents[1] / 'schemas/skill-interface-1.6.schema.json', 'interface')

    def test_terminal_duplicate_input_matches_command_help_and_catalog(self):
        for package_id, script, command_id in [
            ('guru-complete-task-closure', 'invoke.sh', 'invoke-guru-complete-task-closure'),
            ('guru-finish-task', 'invoke.sh', 'invoke-guru-finish-task'),
            ('guru-reactivate-task', 'invoke.sh', 'invoke-guru-reactivate-task'),
            ('guru-reactivate-task', 'observe.sh', 'observe-task-reactivation-implementation'),
            ('guru-cleanup-task-resources', 'invoke.sh', 'invoke-guru-cleanup-task-resources'),
        ]:
            with self.subTest(package_id=package_id, command_id=command_id):
                package = PACKAGE.parent / package_id
                metadata = json.loads((package / 'commands.json').read_text())
                command = next(row for row in metadata['commands'] if row['id'] == command_id)
                public = str(package / 'examples/public-input.json')
                arguments = ['--input', public, '--input', public]
                if any(row['flag'] == '--semantic-result' for row in command['arguments']):
                    arguments.extend(['--semantic-result', str(package / 'examples/semantic-result.json')])
                wrapper = ['bash', str(package / 'scripts' / script)]
                result = _contract_command([*wrapper, *arguments])
                help_result = _contract_command([*wrapper, '--help'])
                self.assertEqual(result.returncode, 2, (result.stdout, result.stderr))
                self.assertEqual(result.stderr, '')
                error = json.loads(result.stdout)
                self.assertEqual((error['code'], error['field_path']), ('conflicting_arguments', 'arguments.--input'))
                self.assertEqual(help_result.returncode, 0, help_result.stderr)
                self.assertEqual(help_result.stderr, '')
                self.assertIn(error['code'], command['errors'])
                catalog = json.loads((package / 'errors/catalog.json').read_text())
                declared = next(row for row in catalog['errors'] if row['code'] == error['code'])
                self.assertEqual(declared['exit_status'], result.returncode)
                interface = json.loads((package / 'interface.json').read_text())
                validate_json(error, package / interface['public_contracts']['invocation']['error_schema']['path'], 'error')
                self.assertIn(f"  {error['code']}\n", help_result.stdout)

    def test_reactivate_blocked_exit_keeps_normal_output_contract(self):
        interface = json.loads((PACKAGE / 'interface.json').read_text())
        output = next(row for row in interface['public_contracts']['outputs'] if row['exit_id'] == 'reactivate_blocked')
        blocked = json.loads((PACKAGE / output['example']['path']).read_text())
        validate_json(blocked, PACKAGE / output['schema']['path'], 'typed_exit')
        validate_json(blocked, PACKAGE / 'schemas/public-output.schema.json', 'normal_stdout')
        with self.assertRaises(CommandError) as caught:
            validate_json(blocked, PACKAGE / interface['public_contracts']['invocation']['error_schema']['path'], 'invocation_error')
        self.assertEqual(caught.exception.code, 'schema_mismatch')

    def test_finish_missing_reader_error_is_declared(self):
        package = PACKAGE.parent / 'guru-finish-task'
        spec = importlib.util.spec_from_file_location('finish_error_declaration_owner', package / 'runtime/invoke.py')
        finish = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(finish)
        with mock.patch.dict(sys.modules, {'runtime.task_lifecycle.closure_result': None}):
            with self.assertRaises(CommandError) as caught:
                finish.read_closure_snapshot(Path.cwd(), package, {})
        error = caught.exception
        _record_contract_receipt({
            'boundary': 'unit_before_repository_read', 'call': 'guru-finish-task.read_closure_snapshot',
            'error': {'code': error.code, 'field_path': error.field_path, 'remediation': error.remediation},
            'exit_status': error.exit_status,
        })
        help_result = _contract_command(['bash', str(package / 'scripts/invoke.sh'), '--help'])
        self.assertEqual((error.code, error.field_path, error.exit_status), ('closure_result_reader_missing', 'closure_result', 3))
        command = next(row for row in json.loads((package / 'commands.json').read_text())['commands']
                       if row['id'] == 'invoke-guru-finish-task')
        self.assertIn(error.code, command['errors'])
        catalog = json.loads((package / 'errors/catalog.json').read_text())
        self.assertEqual(next(row for row in catalog['errors'] if row['code'] == error.code)['exit_status'], error.exit_status)
        validate_json({'code': error.code, 'field_path': error.field_path, 'remediation': error.remediation},
                      package / 'schemas/public-invocation-error.schema.json', 'error')
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertEqual(help_result.stderr, '')
        self.assertIn(f'  {error.code}\n', help_result.stdout)


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
