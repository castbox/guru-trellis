"""Fixed-source creation through public owners; fixtures supply AI judgments only."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

import test_contract as creation
from runtime.schema import validate_json
from runtime.delivery_projection.tests.upstream_fixture import scripts_source

SKILLS = creation.PACKAGE.parents[1]
path = SKILLS / 'packages/guru-sync-base/tests/test_read_baseline_chain.py'
spec = importlib.util.spec_from_file_location('fixed_base_intake_fixture', path)
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class FixedBaseTests(unittest.TestCase):
    def fixture(self):
        case = creation.CreateTaskTests('test_adopt_no_issue_create_and_read_only_recovery')
        case.setUp()
        self.addCleanup(case.doCleanups)
        case.payload['creation']['reviewed_base_source']['kind'] = 'git_object'
        return case

    def test_versioned_contracts_validate_both_generations_and_reject_substitution(self):
        current = json.loads((creation.PACKAGE / 'examples/public-create-input.json').read_text())
        legacy = copy.deepcopy(current)
        legacy['creation']['reviewed_base_head'] = legacy['creation'].pop('reviewed_base_source')['commit']
        for payload, version, shared in ((current, 'public-input-2.0.schema.json', 'task-creation-input-3.0.schema.json'),
                                         (legacy, 'public-input.schema.json', 'task-creation-input.schema.json')):
            validate_json(payload, creation.PACKAGE / 'schemas' / version, 'input')
            validate_json(payload['creation'], SKILLS / 'contracts/task-lifecycle' / shared, 'creation')
        for payload, wrong in ((current, 'public-input.schema.json'), (legacy, 'public-input-2.0.schema.json')):
            with self.assertRaises(creation.MODULE.CommandError):
                validate_json(payload, creation.PACKAGE / 'schemas' / wrong, 'input')
        case = self.fixture()
        old = copy.deepcopy(case.payload)
        old['creation']['reviewed_base_head'] = old['creation'].pop('reviewed_base_source')['commit']
        with self.assertRaises(creation.MODULE.CommandError):
            case.invoke(old)
        self.assertFalse((case.root / case.ref).exists())

    def test_fixed_object_and_acquisition_errors_are_field_specific_in_create_and_recovery(self):
        case = self.fixture()
        before = case.git('worktree', 'list', '--porcelain')
        blob = case.git('rev-parse', 'HEAD:README.md')
        for commit in ('a' * 40, blob):
            request = copy.deepcopy(case.payload)
            request['creation']['reviewed_base_source']['commit'] = commit
            for action in ('create_task', 'recover_created_task_result'):
                result = case.invoke({**request, 'action': action})
                self.assertEqual(result['reason_code'], 'creation_base_object_unavailable')
                self.assertEqual(result['diagnostic']['field_path'], 'reviewed_base_source.commit')
        request = copy.deepcopy(case.payload)
        request['acquisition']['decision_head'] = 'b' * 40
        for action in ('create_task', 'recover_created_task_result'):
            result = case.invoke({**request, 'action': action})
            self.assertEqual(result['reason_code'], 'creation_acquisition_mismatch')
            self.assertEqual(result['diagnostic']['field_path'], 'acquisition.decision_head')
        self.assertEqual(case.git('worktree', 'list', '--porcelain'), before)
        self.assertFalse((case.root / case.ref).exists())

    def test_foreign_checkout_common_directory_is_rejected_by_both_paths(self):
        case = self.fixture()
        foreign = Path(case.temporary.name) / 'foreign'
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(foreign)], check=True)
        wrong = copy.deepcopy(case.payload)
        wrong['acquisition']['invocation_checkout'] = str(foreign)
        for action in ('create_task', 'recover_created_task_result'):
            result = case.invoke({**wrong, 'action': action})
            self.assertEqual(result['reason_code'], 'creation_repository_mismatch')
            self.assertEqual(result['diagnostic']['field_path'], 'acquisition.invocation_checkout')
        self.assertFalse((case.root / case.ref).exists())

    def test_synchronized_creation_stale_and_recovery_after_ref_advance(self):
        case = self.fixture()
        source = case.payload['creation']['reviewed_base_source']
        source.update(kind='synced_branch', selected_ref='refs/heads/main')
        wrong = copy.deepcopy(case.payload)
        wrong['creation']['reviewed_base_source']['selected_ref'] = 'other-branch'
        rejected = case.invoke(wrong)
        self.assertEqual(rejected['diagnostic']['field_path'], 'reviewed_base_source.selected_ref')
        created = case.invoke(case.payload)
        self.assertEqual(created['exit_id'], 'created')
        subprocess.run(['git', 'commit', '--allow-empty', '-qm', 'normal later main work'], cwd=case.primary, check=True)
        # Same completed result survives ordinary synchronized branch advancement.
        self.assertEqual(case.invoke({**case.payload, 'action': 'recover_created_task_result'}), created)
        fresh = copy.deepcopy(case.payload)
        fresh['creation'].update(task_id='another-task', task_ref=case.ref.replace('example-task', 'another-task'))
        fresh['acquisition'].update(branch_ref='codex/another-task')
        self.assertEqual(case.invoke(fresh), {'exit_id': 'refresh_review', 'reason_code': 'creation_base_stale'})

    def test_full_read_intake_creation_with_old_dirty_primary_and_lost_output(self):
        chain = intake.ReadBaselineChainTests('test_actual_sync_still_rejects_dirty_authority')
        chain.setUp()
        self.addCleanup(chain.doCleanups)
        chain.environment = {k: v for k, v in chain.environment.items()
                             if not k.startswith(('TRELLIS_', 'CODEX_', 'CLAUDE_', 'CURSOR_', 'GIT_'))}
        # Install upstream public Task assets before the tested producer boundary.
        scripts = scripts_source()
        shutil.copytree(scripts, chain.worktree / '.trellis/scripts')
        (chain.worktree / '.trellis/.version').write_bytes((scripts.parent / '.version').read_bytes())
        (chain.worktree / '.trellis/workflow.md').write_bytes((creation.SOURCE / 'trellis/workflows/guru-team/workflow.md').read_bytes())
        (chain.worktree / 'docs/requirements.md').write_text(chain.files['docs/requirements.md'])
        chain.git('add', '.trellis', 'docs/requirements.md', cwd=chain.worktree)
        chain.git('commit', '-m', 'new reviewed source', cwd=chain.worktree)
        chain.commit = chain.git('rev-parse', 'HEAD', cwd=chain.worktree)
        chain.git('update-ref', 'refs/remotes/origin/main', chain.commit)
        old_main = chain.git('rev-parse', 'main')
        self.assertNotEqual(old_main, chain.commit)
        # Ordinary staged and unstaged work in primary stays outside Task creation.
        staged = chain.root / 'docs/requirements.md'
        staged.write_text('unrelated staged work\n')
        chain.git('add', 'docs/requirements.md')
        unstaged = chain.root / 'src/runtime.py'
        unstaged.write_text('VALUE = 99\n')
        primary = (chain.git('symbolic-ref', 'HEAD'), old_main,
                   (chain.root / '.git/index').read_bytes(), staged.read_bytes(), unstaged.read_bytes(),
                   chain.git('status', '--porcelain'))
        baseline = chain.baseline('origin/main', chain.commit)
        context, _ = chain.context(baseline)
        clear = chain.clarify(context)
        wording = chain.wording(clear)
        ready, _ = chain.readiness(wording, target_kind='standalone_request')
        self.assertEqual(ready['exit_id'], 'ready')
        self.assertEqual(ready['transition']['target']['kind'], 'standalone_request')
        base = ready['transition']['base']
        self.assertEqual(base, baseline['transition']['base'])
        prefix = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%m-%d')
        ref = f'.trellis/tasks/{prefix}-fixed-source'
        target = Path(chain.tmp.name) / 'created-checkout'
        request = {'profile': 'delivery_task_creation', 'action': 'create_task',
            'creation': {'task_id': 'fixed-source', 'task_ref': ref,
                'source_profile': 'standalone_request', 'reviewed_source': {'kind': 'no_issue'},
                'accepted_scope_identity': ready['transition']['target']['identity_sha256'],
                'delivery_target': {'repo_ref': ready['transition']['target']['repo'], 'branch_ref': 'main'},
                'selected_base_ref': 'main',
                'reviewed_base_source': {key: base[key] for key in ('kind', 'selected_ref', 'commit')}},
            'acquisition': {'route': 'provision_linked_worktree', 'branch_ref': 'codex/fixed-source',
                'decision_head': base['commit'], 'transaction_id': 'acquisition:fixed-source',
                'result_id': 'checkout:fixed-source', 'provision_disposition': 'new_branch',
                'path_source': 'explicit', 'checkout_root': str(target)},
            'task': {'title': 'Fixed source task', 'description': 'Reviewed fixed source request', 'scope': chain.body}}
        def call(wrapper, payload):
            if wrapper == 'invoke.sh':
                return chain.call('guru-create-task', wrapper, payload,
                                  ('--root', str(chain.worktree), '--input', '-'))
            # Creation's component commands use the declared shared launcher,
            # rather than separate package-local shell wrappers.
            result = subprocess.run([str(SKILLS / 'runtime/launch.sh'), str(creation.PACKAGE),
                                     wrapper.removesuffix('.sh'), '--root', str(chain.worktree), '--input', '-'],
                                    input=json.dumps(payload), text=True, capture_output=True, env=chain.environment)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            from runtime.io import project_intermediate_receipt
            return project_intermediate_receipt(json.loads(result.stdout), SKILLS / 'schemas')
        self.assertEqual(call('record-task-plan.sh', request)['status'], 'ready')
        created = call('invoke.sh', request)
        self.assertEqual(created, {'exit_id': 'created', 'task_id': 'fixed-source', 'task_ref': ref, 'lifecycle_generation': 0})
        self.assertEqual(chain.git('rev-parse', 'HEAD', cwd=target), chain.commit)
        task = json.loads((target / ref / 'task.json').read_text())
        self.assertEqual((task['id'], task['lifecycle_generation'], task['base_branch']), ('fixed-source', 0, 'main'))
        before = ((target / ref / 'task.json').read_bytes(), chain.git('show-ref'), chain.git('worktree', 'list', '--porcelain'))
        # Discarded first stdout is recovered through both original public readers.
        recovered_request = {**request, 'action': 'recover_created_task_result'}
        self.assertEqual(call('check-task-creation-result.sh', recovered_request), created)
        self.assertEqual(call('recover-created-task-result.sh', recovered_request), created)
        self.assertEqual(((target / ref / 'task.json').read_bytes(), chain.git('show-ref'), chain.git('worktree', 'list', '--porcelain')), before)
        self.assertEqual((chain.git('symbolic-ref', 'HEAD'), chain.git('rev-parse', 'main'),
                          (chain.root / '.git/index').read_bytes(), staged.read_bytes(), unstaged.read_bytes(),
                          chain.git('status', '--porcelain')), primary)
        self.assertEqual(chain.git('rev-parse', 'origin/main'), chain.commit)


if __name__ == '__main__':
    unittest.main()
