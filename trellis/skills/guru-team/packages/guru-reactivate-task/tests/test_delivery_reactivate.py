"""Real Git/public writers with a controlled read-only PR provider; not native AI proof."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION
from runtime.delivery_projection.tests.upstream_fixture import scripts_source, public_task
from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.errors import LifecycleContractError

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shared_reactivate_test_owner', PACKAGE / 'runtime/invoke.py')
owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
shared = sys.modules['shared_finish']


class Fixture(unittest.TestCase):
    def setUp(self, fixture_directory=None, installed_repository=None):
        if fixture_directory is None:
            self.temporary = tempfile.TemporaryDirectory()
            self.addCleanup(self.temporary.cleanup)
        else:
            # Explicit native-fixture setup is retained for its real Agent owner.
            from types import SimpleNamespace
            fixture_directory.mkdir(parents=True, exist_ok=False)
            self.temporary = SimpleNamespace(name=str(fixture_directory))
        self.root = Path(installed_repository).resolve() if installed_repository else Path(self.temporary.name) / 'repo'
        if installed_repository:
            if not (self.root / '.trellis/scripts/common/delivery_schema.py').is_file():
                raise RuntimeError('Install the complete matching Fork and Guru preset before fixture setup.')
            if any((self.root / '.trellis/tasks').glob('*/task.json')):
                raise RuntimeError('Use an empty fixture repository without existing Tasks.')
            if self.git(self.root, 'symbolic-ref', '--short', 'HEAD') != 'main':
                raise RuntimeError('Use the empty fixture main branch.')
        else:
            self.root.mkdir()
            self.git(self.root, 'init', '-q', '-b', 'main')
            shutil.copytree(scripts_source(), self.root / '.trellis/scripts')
            (self.root / '.trellis/workflow.md').write_text('[trellis-runtime-contract]\n' + json.dumps(DECLARATION) + '\n[/trellis-runtime-contract]\n')
            (self.root / '.trellis/.developer').write_text('fixture\n')
        self.git(self.root, 'config', 'user.name', 'Fixture')
        self.git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        if 'origin' in self.git(self.root, 'remote').splitlines():
            self.git(self.root, 'remote', 'set-url', 'origin', 'https://github.com/example/repository.git')
        else:
            self.git(self.root, 'remote', 'add', 'origin', 'https://github.com/example/repository.git')
        ignore = self.root / '.gitignore'
        if not ignore.is_file() or '.trellis/.runtime/' not in ignore.read_text():
            with ignore.open('a') as stream: stream.write('\n.trellis/.runtime/\n')
        (self.root / 'scope.md').write_text('Reviewed fixture scope\n')
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'initial')
        self.provider = mock.patch.object(shared, 'github_json', side_effect=self.pr_rows)
        self.provider.start(); self.addCleanup(self.provider.stop)
        self.prs = []

    @staticmethod
    def git(root, *args):
        return subprocess.check_output(['git', *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()

    def pr_rows(self, repo, endpoint):
        return self.prs

    def record_merge(self, archive_ref, original_ref, task_id, generation):
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'archive result')
        archive_head = self.git(self.root, 'rev-parse', 'HEAD')
        self.git(self.root, 'switch', '-q', 'main')
        self.git(self.root, 'merge', '--no-ff', '-qm', 'Merge bookkeeping', 'finish')
        merge = self.git(self.root, 'rev-parse', 'HEAD')
        self.prs.append({'number': len(self.prs) + 1, 'merged_at': '2026-10-20T00:00:00Z',
                         'merge_commit_sha': merge, 'base': {'ref': 'main', 'repo': {'full_name': 'example/repository'}}})
        public = {'profile': 'delivery_reactivate_shared_archive', 'mode': 'standalone',
                  'archived_lifecycle': {'task_id': task_id, 'lifecycle_generation': generation},
                  'archive_anchor': {'repo_ref': 'example/repository', 'archive_ref': archive_ref,
                                     'archive_commit': archive_head, 'original_task_ref': original_ref,
                                     'target_ref': 'refs/heads/main'}}
        return public

    def task2_archive(self):
        self.git(self.root, 'switch', '-qc', 'finish')
        active_ref = '.trellis/tasks/current'
        task = self.root / active_ref; task.mkdir(parents=True)
        (task / 'task.json').write_text(json.dumps(public_task({'id': 'stable-id', 'name': 'current'})))
        projection = DeliveryProjection(self.root, active_ref)
        scope = authority_ref(self.root / 'scope.md', self.root)
        projection.scope(scope)
        key = {'task_id': 'stable-id', 'lifecycle_generation': 0}
        completion = {'result_id': 'completion:stable-id', 'owner_id': DECLARATION['owners']['completion'],
                      'evidence': [scope], 'lifecycle_generation': 0, 'accepted_scope': scope,
                      'delivery_result_ids': [], 'outcome': 'completed'}
        projection.apply({'api_version': '1.0', 'operation': 'complete_task', 'key': key,
                          'owner_role': 'completion', 'owner_id': completion['owner_id'], 'result': completion})
        closure = {'result_id': 'closure:stable-id', 'owner_id': DECLARATION['owners']['closure'],
                   'evidence': [scope], 'lifecycle_generation': 0, 'completion_result_id': completion['result_id'],
                   'disposition': 'no_mutation', 'source_result': None}
        projection.apply({'api_version': '1.0', 'operation': 'close_task', 'key': key,
                          'owner_role': 'closure', 'owner_id': closure['owner_id'], 'result': closure})
        spec = importlib.util.spec_from_file_location('shared_finish_fixture_owner', PACKAGE.parent / 'guru-finish-task/runtime/invoke.py')
        finish = importlib.util.module_from_spec(spec); spec.loader.exec_module(finish)
        archive_ref = '.trellis/tasks/archive/2026-10/current'
        finish.project_archive(self.root, {**key, 'task_ref': active_ref, 'closure_result': closure}, Path(active_ref), archive_ref, Path(archive_ref))
        public = self.record_merge(archive_ref, active_ref, 'stable-id', 0)
        return public, scope

    def semantic(self, public, scope, adopt=True):
        target = self.root if adopt else Path(self.temporary.name) / 'linked'
        head = self.git(self.root, 'rev-parse', 'main')
        if adopt:
            self.git(self.root, 'switch', '-qc', 'task-next')
        acquisition = {'task_id': public['archived_lifecycle']['task_id'], 'task_ref': '.trellis/tasks/current',
                       'lifecycle_generation': public['archived_lifecycle']['lifecycle_generation'] + 1,
                       'route': 'adopt_invocation_checkout' if adopt else 'provision_linked_worktree',
                       'branch_ref': 'refs/heads/task-next', 'decision_head': head,
                       'task_artifact_expectation': 'absent', 'transaction_id': 'reactivate:fixture', 'result_id': 'result:fixture'}
        if adopt:
            acquisition['invocation_checkout'] = str(target)
        else:
            acquisition.update(target_path=str(target), provision_disposition='new_branch')
        return {**public, 'route': 'session_binding_recovery_required', 'reason_refs': ['new reviewed work'],
                'selected_base_ref': 'refs/heads/main', 'reviewed_base_head': head,
                'session_outcome': 'recovery_required', 'acquisition': acquisition, 'authority': scope}


class DeliveryReactivateTests(Fixture):
    def test_public_reopen_in_adopted_and_linked_checkout_without_old_seal(self):
        # Independent temporary fixtures, not another installer profile.
        public, scope = self.task2_archive()
        semantic = self.semantic(public, scope, adopt=False)
        first = owner.execute(self.root, public, semantic)
        self.assertEqual(first, {'exit_id': 'session_binding_recovery_required', 'task_id': 'stable-id', 'lifecycle_generation': 1})
        target = Path(semantic['acquisition']['target_path'])
        before = (target / '.trellis/tasks/current/task.json').read_bytes()
        self.assertEqual(owner.execute(self.root, public, semantic), first)
        self.assertEqual((target / '.trellis/tasks/current/task.json').read_bytes(), before)
        resumed = owner.execute(self.root, public, {**semantic, 'route': 'resume_reactivation'})
        self.assertEqual(resumed['lifecycle_generation'], 1)

    def test_later_target_commit_and_new_active_do_not_invalidate_archive(self):
        public, scope = self.task2_archive()
        (self.root / 'unrelated.md').write_text('later target work\n')
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'target advance')
        semantic = self.semantic(public, scope)
        first = owner.execute(self.root, public, semantic)
        self.assertEqual(first['lifecycle_generation'], 1)
        self.assertEqual(owner.execute(self.root, public, semantic), first)

    def test_private_receipt_absent_continues_existing_public_successor(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        first = owner.execute(self.root, public, semantic)
        path = owner.transaction_path(inspect_repository(self.root), TaskLifecycleKey('stable-id', 0))
        path.unlink()  # Ordinary loss of a local recovery receipt, not forged authority.
        self.assertEqual(owner.execute(self.root, public, {k: v for k, v in semantic.items() if k != 'acquisition'}), first)
        record = DeliveryProjection(self.root, '.trellis/tasks/current').read_record()
        self.assertEqual(record['lifecycle_generation'], 1)

    def test_lost_receipt_from_retained_root_finds_registered_linked_successor(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope, adopt=False)
        first = owner.execute(self.root, public, semantic)
        target = Path(semantic['acquisition']['target_path'])
        key = TaskLifecycleKey('stable-id', 1)
        store = BranchBindingStore(inspect_repository(self.root))
        binding = store.read(key)
        before = (target / '.trellis/tasks/current/task.json').read_bytes()
        owner.transaction_path(inspect_repository(self.root), TaskLifecycleKey('stable-id', 0)).unlink()
        with mock.patch.object(owner, 'acquire_checkout', wraps=owner.acquire_checkout) as acquire, mock.patch.object(owner, 'call', wraps=owner.call) as sdk:
            resumed = owner.execute(self.root, public, {k: v for k, v in semantic.items() if k != 'acquisition'})
        self.assertEqual(resumed, first)
        acquire.assert_not_called()
        sdk.assert_not_called()
        self.assertEqual(store.read(key), binding)
        self.assertEqual((target / '.trellis/tasks/current/task.json').read_bytes(), before)
        self.assertEqual(DeliveryProjection(target, '.trellis/tasks/current').read_record()['lifecycle_generation'], 1)

    def test_merged_shared_snapshot_does_not_block_linked_owner_checkout(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope, adopt=False)
        first = owner.execute(self.root, public, semantic)
        target = Path(semantic['acquisition']['target_path'])
        self.git(target, 'add', '.'); self.git(target, 'commit', '-qm', 'publish linked successor')
        self.git(self.root, 'merge', '--ff-only', 'task-next')
        before = (target / '.trellis/tasks/current/task.json').read_bytes()
        store = BranchBindingStore(inspect_repository(self.root)); key = TaskLifecycleKey('stable-id', 1)
        binding = store.read(key)
        for receipt_present in (True, False):
            with self.subTest(receipt_present=receipt_present):
                if not receipt_present:
                    owner.transaction_path(inspect_repository(self.root), TaskLifecycleKey('stable-id', 0)).unlink()
                with mock.patch.object(owner, 'acquire_checkout', wraps=owner.acquire_checkout) as acquire, mock.patch.object(owner, 'call', wraps=owner.call) as sdk:
                    output = owner.execute(self.root, public, {k: v for k, v in semantic.items() if k != 'acquisition'})
                self.assertEqual(output, first)
                acquire.assert_not_called(); sdk.assert_not_called()
                self.assertEqual(store.read(key), binding)
                self.assertEqual((target / '.trellis/tasks/current/task.json').read_bytes(), before)

    def test_planning_reports_actual_binding_revision(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        owner.execute(self.root, public, semantic)
        store = BranchBindingStore(inspect_repository(self.root)); key = TaskLifecycleKey('stable-id', 1)
        # The original stores legitimately evolve current controls together.
        head = self.git(self.root, 'rev-parse', 'HEAD')
        self.git(self.root, 'switch', '-qc', 'task-later')
        current = store.advance(key, expected_revision=0, branch_name='task-later')
        ResourceLedgerStore(inspect_repository(self.root)).rebind_current(key, expected_revision=0,
            source_branch_name='task-next', target_branch_name='task-later', expected_cleanup_head=head,
            target_branch_ownership='caller_owned', target_worktree_ownership='not_applicable', worktree_reassociated=False)
        with mock.patch.object(owner, 'session_outcome', return_value='explicit_task_mode'):
            output = owner.execute(self.root, public, {k: v for k, v in {**semantic, 'route': 'reactivated_to_planning', 'session_outcome': 'explicit_task_mode'}.items() if k != 'acquisition'})
        self.assertEqual(output['binding_revision'], current.binding_revision)
        self.assertEqual(output['binding_revision'], 1)

    def test_independent_clone_uses_original_environment_consumers(self):
        public, scope = self.task2_archive(); semantic = self.semantic(public, scope)
        owner.execute(self.root, public, semantic)
        self.git(self.root, 'add', '.'); self.git(self.root, 'commit', '-qm', 'publish successor')
        clone = Path(self.temporary.name) / 'independent'
        self.git(Path(self.temporary.name), 'clone', '-q', '--branch', 'task-next', str(self.root), str(clone))
        self.git(clone, 'remote', 'set-url', 'origin', 'https://github.com/example/repository.git')
        self.git(clone, 'branch', 'main', self.git(self.root, 'rev-parse', 'main'))
        output = owner.execute(clone, public, {k: v for k, v in semantic.items() if k != 'acquisition'})
        self.assertEqual(output['lifecycle_generation'], 1)
        key = TaskLifecycleKey('stable-id', 1)
        self.assertIsNone(BranchBindingStore(inspect_repository(clone)).read(key))
        def original(name):
            spec = importlib.util.spec_from_file_location('consumer_' + name.replace('-', '_'), PACKAGE.parent / name / 'runtime/invoke.py')
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
            return module
        selected = {'profile': 'delivery_active_task', 'mode': 'standalone', 'task_id': key.task_id,
                    'lifecycle_generation': key.lifecycle_generation}
        established = original('guru-establish-task-branch-binding').invoke(clone, {**selected, 'task_ref': '.trellis/tasks/current', 'action': 'establish'})
        self.assertEqual(established['exit_id'], 'binding_established', established)
        ensured = original('guru-ensure-task-checkout').invoke(clone, selected)
        self.assertEqual(ensured['exit_id'], 'checkout_resolved', ensured)
        bind = original('guru-bind-task-session')
        bind_input = {'profile': 'delivery_rebind_missing_session', 'mode': 'standalone', 'task_id': key.task_id,
                      'lifecycle_generation': 1, 'continuation_id': 'clone-fixture'}
        reviewed = {**bind_input, 'route': 'rebind', 'resume_target': 'phase-2',
                    'ai_review_gate': {'status': 'passed', 'summary': 'Controlled integration fixture; not actual AI acceptance.'}}
        with mock.patch.dict(os.environ, {'TRELLIS_CONTEXT_ID': 'shared-clone-fixture'}):
            bound = bind.execute(clone, json.dumps(bind_input), json.dumps(reviewed))
        self.assertEqual(bound['exit_id'], 'session_rebound', bound)
        self.assertIsNotNone(ResourceLedgerStore(inspect_repository(clone)).read_current(key))
