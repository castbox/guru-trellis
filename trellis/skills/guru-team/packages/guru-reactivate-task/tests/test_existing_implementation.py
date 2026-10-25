"""Real Git/public writers; controlled PR facts are not native Agent proof."""
import copy
import json
import os
from pathlib import Path
from unittest import mock

from test_delivery_reactivate import Fixture, owner, shared, PACKAGE
from runtime.task_lifecycle.git_facts import capture_implementation_state, capture_checkout_state
from runtime.task_lifecycle import TaskLifecycleKey, inspect_repository, BranchBindingStore
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.delivery_projection import DeliveryProjection
from runtime.schema import validate_json
from existing_implementation import observe, PROFILE


class ExistingFixture(Fixture):
    def pr_rows(self, repo, endpoint):
        return self.implementation_pr if endpoint.startswith('pulls/') else self.prs

    def prepare_existing(self, formal=False):
        if formal:
            import test_formal_archive_reactivate as formal_fixture
            public, semantic, scope = formal_fixture.FormalArchiveReactivateTests.prepare_formal(self)
        else:
            public, scope = self.task2_archive()
            semantic = self.semantic(public, scope)
        # A real implementation commit, followed by real tool/source differences.
        (self.root / 'implementation.txt').write_text('existing implementation\n')
        (self.root / 'tool.sh').write_text('tool before upgrade\n')
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'existing implementation')
        head = self.git(self.root, 'rev-parse', 'HEAD')
        (self.root / 'implementation.txt').write_text('staged implementation\n')
        self.git(self.root, 'add', 'implementation.txt')
        (self.root / 'implementation.txt').write_text('unstaged implementation\n')
        (self.root / 'tool.sh').write_text('local source locked tool upgrade\n')
        (self.root / 'scratch.txt').write_text('untracked working content\n')
        (self.root / '.trellis/local-tool-state').write_text('reviewed tool difference\n')
        public.update(profile=PROFILE, implementation_pr={'repo_ref': 'example/repository', 'number': 838})
        self.implementation_pr = {'number': 838, 'state': 'open', 'draft': True,
                                  'base': {'ref': 'main', 'repo': {'full_name': 'example/repository'}},
                                  'head': {'ref': 'task-next', 'sha': head, 'repo': {'full_name': 'example/repository'}}}
        semantic.update(public)
        semantic['acquisition']['decision_head'] = head
        semantic['implementation_state'] = capture_implementation_state(self.root)
        return public, semantic


class ExistingImplementationTests(ExistingFixture):
    def test_reopen_preserves_index_working_bytes_head_pr_and_caller_ownership(self):
        public, semantic = self.prepare_existing()
        index = self.git(self.root, 'ls-files', '--stage')
        files = {name: (self.root / name).read_bytes() for name in
                 ('implementation.txt', 'tool.sh', 'scratch.txt', '.trellis/local-tool-state')}
        pr = copy.deepcopy(self.implementation_pr)
        head = self.git(self.root, 'rev-parse', 'HEAD')
        refs = self.git(self.root, 'show-ref')
        before = DeliveryProjection(self.root, public['archive_anchor']['archive_ref']).read_record()
        result = owner.execute(self.root, public, semantic)
        self.assertEqual(result, {'exit_id': 'session_binding_recovery_required', 'task_id': 'stable-id', 'lifecycle_generation': 1})
        self.assertEqual(self.git(self.root, 'ls-files', '--stage'), index)
        self.assertEqual(self.git(self.root, 'rev-parse', 'HEAD'), head)
        self.assertEqual(self.git(self.root, 'show-ref'), refs)
        self.assertEqual(self.implementation_pr, pr)
        for name, content in files.items(): self.assertEqual((self.root / name).read_bytes(), content)
        task = DeliveryProjection(self.root, '.trellis/tasks/current').read_record()
        self.assertEqual(task['completion_results'], before['completion_results'])
        self.assertEqual(task['closure_results'], before['closure_results'])
        self.assertEqual(task['deliveries'], [])
        ledger = ResourceLedgerStore(inspect_repository(self.root)).read(TaskLifecycleKey('stable-id', 1))
        self.assertEqual([(row.kind, row.ownership) for row in ledger.resources], [('local_branch', 'caller_owned')])
        record = json.loads(owner.transaction_path(inspect_repository(self.root), TaskLifecycleKey('stable-id', 0)).read_text())
        self.assertEqual(record['schema_version'], '3.0')
        self.assertNotEqual(record['base_head'], record['implementation_state']['head'])
        self.assertEqual(record['implementation_state'], capture_implementation_state(self.root))
        # The generated Task metadata has an exact after-state; replay uses it.
        self.assertNotEqual(record['implementation_state'], semantic['implementation_state'])
        self.assertEqual(owner.execute(self.root, public, semantic), result)
        self.assertEqual(owner.execute(self.root, public, {**semantic, 'route': 'resume_reactivation'})['lifecycle_generation'], 1)

    def test_index_stat_refresh_is_same_logical_state(self):
        public, semantic = self.prepare_existing()
        os.utime(self.root / 'scope.md', None)
        # --refresh normally exits 1 when unrelated tracked files need update.
        import subprocess
        subprocess.run(['git', 'update-index', '--refresh'], cwd=self.root, capture_output=True)
        self.assertEqual(capture_implementation_state(self.root), semantic['implementation_state'])
        self.assertEqual(owner.execute(self.root, public, semantic)['lifecycle_generation'], 1)

    def test_file_mode_type_bytes_and_index_are_observable(self):
        public, semantic = self.prepare_existing()
        expected = semantic['implementation_state']
        file = self.root / 'tool.sh'; original = file.read_bytes(); mode = file.stat().st_mode
        file.chmod(mode | 0o111)
        self.assertNotEqual(capture_implementation_state(self.root), expected)
        file.chmod(mode)
        file.unlink(); file.symlink_to('implementation.txt')
        self.assertNotEqual(capture_implementation_state(self.root), expected)
        file.unlink(); file.write_bytes(original)
        self.assertEqual(capture_implementation_state(self.root), expected)
        self.git(self.root, 'add', 'implementation.txt')
        self.assertNotEqual(capture_implementation_state(self.root), expected)
        with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
            owner.execute(self.root, public, semantic)
        self.assertFalse((self.root / '.trellis/tasks/current').exists())

    def test_reviewed_local_bytes_changed_stops_without_writes(self):
        public, semantic = self.prepare_existing()
        (self.root / '.trellis/local-tool-state').write_text('later upgrade result\n')
        before = capture_implementation_state(self.root)
        with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
            owner.execute(self.root, public, semantic)
        self.assertEqual(capture_implementation_state(self.root), before)

    def test_head_branch_base_and_pr_mismatches_are_zero_write(self):
        public, semantic = self.prepare_existing()
        original_pr = copy.deepcopy(self.implementation_pr)
        changes = [('state', 'closed'), ('draft', False), ('head.ref', 'other'), ('head.sha', '1' * 40),
                   ('head.repo.full_name', 'other/repository'), ('base.ref', 'other'), ('base.repo.full_name', 'other/repository')]
        for field, value in changes:
            self.implementation_pr = copy.deepcopy(original_pr)
            selected = self.implementation_pr
            parts = field.split('.')
            for part in parts[:-1]: selected = selected[part]
            selected[parts[-1]] = value
            with self.subTest(field=field), self.assertRaises(LifecycleContractError):
                owner.execute(self.root, public, semantic)
            self.assertFalse((self.root / '.trellis/tasks/current').exists())
        self.implementation_pr = original_pr
        self.git(self.root, 'branch', '-m', 'renamed')
        with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
            owner.execute(self.root, public, semantic)
        self.git(self.root, 'branch', '-m', 'task-next')
        self.git(self.root, 'commit', '--allow-empty', '-qm', 'implementation advanced')
        with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
            owner.execute(self.root, public, semantic)

    def test_base_advance_and_other_repository_stop(self):
        public, semantic = self.prepare_existing()
        self.git(self.root, 'update-ref', 'refs/heads/main', self.git(self.root, 'rev-parse', 'HEAD'))
        with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
            owner.execute(self.root, public, semantic)
        self.git(self.root, 'update-ref', 'refs/heads/main', semantic['reviewed_base_head'])
        self.git(self.root, 'remote', 'set-url', 'origin', 'https://github.com/other/repository.git')
        with self.assertRaises(LifecycleContractError): owner.execute(self.root, public, semantic)
        self.assertFalse((self.root / '.trellis/tasks/current').exists())

    def test_output_loss_and_missing_receipt_continue_public_successor(self):
        public, semantic = self.prepare_existing()
        result = owner.execute(self.root, public, semantic)
        task = (self.root / '.trellis/tasks/current/task.json').read_bytes()
        owner.transaction_path(inspect_repository(self.root), TaskLifecycleKey('stable-id', 0)).unlink()
        with mock.patch.object(owner, 'acquire_checkout', wraps=owner.acquire_checkout) as acquire:
            self.assertEqual(owner.execute(self.root, public, semantic), result)
        acquire.assert_not_called()
        self.assertEqual((self.root / '.trellis/tasks/current/task.json').read_bytes(), task)

    def test_public_writer_success_then_local_failure_recovers_same_generation(self):
        public, semantic = self.prepare_existing()
        with mock.patch.object(owner.ResourceLedgerStore, 'establish_current', side_effect=LifecycleContractError('local_control_unavailable', 'resource_ledger', 'Retry original owner.')):
            with self.assertRaisesRegex(LifecycleContractError, 'local_control_unavailable'):
                owner.execute(self.root, public, semantic)
        before = (self.root / '.trellis/tasks/current/task.json').read_bytes()
        with mock.patch.object(owner.DeliveryProjection, 'scope', wraps=owner.DeliveryProjection.scope) as reopen:
            result = owner.execute(self.root, public, semantic)
        reopen.assert_not_called()
        self.assertEqual(result['lifecycle_generation'], 1)
        self.assertEqual((self.root / '.trellis/tasks/current/task.json').read_bytes(), before)

    def test_new_profile_retains_resource_conflicts_and_old_clean_contract(self):
        public, semantic = self.prepare_existing()
        old_public = {k: v for k, v in public.items() if k != 'implementation_pr'}
        old_public['profile'] = 'delivery_reactivate_shared_archive'
        old_semantic = {k: v for k, v in semantic.items() if k not in {'implementation_state', 'implementation_pr'}}
        old_semantic.update(old_public)
        with self.assertRaisesRegex(LifecycleContractError, 'reactivation_base_stale'):
            owner.execute(self.root, old_public, old_semantic)
        BranchBindingStore(inspect_repository(self.root)).establish(TaskLifecycleKey('peer', 0), 'task-next')
        with self.assertRaisesRegex(LifecycleContractError, 'branch_responsibility_pending'):
            owner.execute(self.root, public, semantic)

    def test_observer_only_facts_and_independent_contracts(self):
        public, semantic = self.prepare_existing()
        before = capture_implementation_state(self.root)
        facts = observe(self.root, public)
        self.assertEqual(facts['implementation_state'], before)
        self.assertEqual(capture_implementation_state(self.root), before)
        self.assertNotIn('exit_id', facts)
        validate_json(public, PACKAGE / 'schemas/public-existing-implementation-input-1.0.schema.json', 'input')
        validate_json(semantic, PACKAGE / 'schemas/semantic-existing-implementation-1.0.schema.json', 'semantic')
        with self.assertRaises(Exception): validate_json(public, PACKAGE / 'schemas/public-input.schema.json', 'legacy')
        with self.assertRaises(Exception): validate_json(semantic, PACKAGE / 'schemas/semantic-result.schema.json', 'legacy')


class ExistingFormalImplementationTests(ExistingFixture):
    def test_new_profile_keeps_original_formal_operation_and_archive(self):
        public, semantic = self.prepare_existing(formal=True)
        archive = self.root / public['archive_anchor']['archive_ref']
        before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
        output = owner.execute(self.root, public, semantic)
        self.assertEqual(output['lifecycle_generation'], public['archived_lifecycle']['lifecycle_generation'] + 1)
        for path, content in before.items(): self.assertEqual((archive / path).read_bytes(), content)
        self.assertEqual(owner.execute(self.root, public, semantic), output)


    def test_applied_formal_pending_and_lost_output_resume_exact_public_operation(self):
        from runtime.io import CommandError
        for output in ("pending", "lost_output"):
            with self.subTest(output=output):
                fixture = ExistingFixture(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
                public, semantic = fixture.prepare_existing(formal=True)
                real = owner.call
                def caller_response(source, method, payload):
                    result = real(source, method, payload)
                    if method == 'applyMaintenance':
                        if output == 'pending':
                            return {'status': 'pending', 'recovery_ref': result['recovery_ref']}
                        raise CommandError('maintenance_prerequisite_missing', 'maintenance_source',
                                           'Controlled ordinary stdout loss after the real public apply.')
                    return result
                with mock.patch.object(owner, 'call', side_effect=caller_response):
                    if output == 'pending':
                        self.assertEqual(owner.execute(fixture.root, public, semantic)['exit_id'], 'resume_reactivation')
                    else:
                        with self.assertRaises(CommandError): owner.execute(fixture.root, public, semantic)
                active = fixture.root / '.trellis/tasks/current/task.json'
                before = active.read_bytes()
                path = owner.transaction_path(inspect_repository(fixture.root), TaskLifecycleKey(public['archived_lifecycle']['task_id'], public['archived_lifecycle']['lifecycle_generation']))
                pending = json.loads(path.read_text())
                self.assertEqual(pending['stage'], 'public_prepared')
                self.assertNotEqual(pending['implementation_state'], capture_implementation_state(fixture.root))
                with mock.patch.object(owner, 'call', wraps=real) as calls:
                    recovered = owner.execute(fixture.root, public, semantic)
                methods = [row.args[1] for row in calls.call_args_list]
                self.assertLess(methods.index('previewMaintenance'), methods.index('recoverMaintenance'))
                self.assertNotIn('prepareFormalArchiveReactivation', methods)
                self.assertNotIn('applyMaintenance', methods)
                self.assertEqual(recovered['lifecycle_generation'], public['archived_lifecycle']['lifecycle_generation'] + 1)
                self.assertEqual(active.read_bytes(), before)
                complete = json.loads(path.read_text())
                self.assertEqual(complete['stage'], 'bound')
                self.assertNotIn('implementation_head', complete)
                self.assertEqual(complete['implementation_state'], capture_implementation_state(fixture.root))

    def test_pending_formal_keeps_business_difference_outside_public_write_set(self):
        public, semantic = self.prepare_existing(formal=True)
        real = owner.call
        def caller_response(source, method, payload):
            result = real(source, method, payload)
            return {'status': 'pending', 'recovery_ref': result['recovery_ref']} if method == 'applyMaintenance' else result
        with mock.patch.object(owner, 'call', side_effect=caller_response):
            self.assertEqual(owner.execute(self.root, public, semantic)['exit_id'], 'resume_reactivation')
        active = self.root / '.trellis/tasks/current/task.json'
        original = active.read_bytes()
        (self.root / 'implementation.txt').write_text('ordinary business edit while output was unavailable\n')
        before = capture_implementation_state(self.root)
        with mock.patch.object(owner, 'call', wraps=real) as calls:
            with self.assertRaisesRegex(LifecycleContractError, 'implementation_state_changed'):
                owner.execute(self.root, public, semantic)
        calls.assert_not_called()
        self.assertEqual(capture_implementation_state(self.root), before)
        self.assertEqual(active.read_bytes(), original)
