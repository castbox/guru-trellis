"""Real wrappers and installed Delivery API; fixture judgments prove transport only."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
KERNEL = PACKAGE.parents[1]
sys.path.insert(0, str(KERNEL))
support_spec = importlib.util.spec_from_file_location(
    'check_delivery_fixture_support', KERNEL / 'packages/guru-create-delivery/tests/support.py')
support = importlib.util.module_from_spec(support_spec)
support_spec.loader.exec_module(support)
installed_fixture, owner_module = support.installed_fixture, support.owner_module
from runtime.delivery_projection.gates import record_gate, rework
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository


class CandidateCheckTests(unittest.TestCase):
    def setUp(self):
        self.fixture = f = installed_fixture(self)
        self.root = f.root
        self.git('config', 'user.name', 'Check Test')
        self.git('config', 'user.email', 'check@example.invalid')
        (self.root / '.gitignore').write_text('.trellis/.runtime/\n')
        (self.root / 'current.md').write_text('Existing complete current\n')
        (self.root / 'implementation.txt').write_text('Initial implementation\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixed content baseline')
        self.base = self.git('rev-parse', 'HEAD')
        BranchBindingStore(inspect_repository(self.root)).establish(TaskLifecycleKey('projection-task', 0), 'task')
        self.key = f.create()
        self.plan = f.planning(self.key)
        directory = f.projection.planning_directory(self.key)
        (directory / 'prd.md').write_text('Accepted slice\n')
        (directory / 'implement.md').write_text('Candidate Check then actual final integration\n')
        (self.root / 'implementation.txt').write_text('Complete implementation\n')
        (self.root / 'proposed.md').write_text('Complete proposed definition\n')
        self.common = owner_module(PACKAGE, 'common.py')
        self.public = {'profile': 'delivery_candidate_check', 'mode': 'workflow',
                       'task_ref': f.task_ref, 'delivery_key': self.key,
                       'planning_accepted_result_id': self.plan['result_id'],
                       'source_exit': 'implementation_complete'}

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout.strip()

    def begin(self):
        p = self.fixture.projection
        candidate = p.candidate(['current.md', 'implementation.txt', 'proposed.md'],
                                base_ref=self.base, head_ref=self.git('rev-parse', 'HEAD'))
        p.begin_check(self.key, candidate)
        return candidate

    def owner(self, exit_id='candidate_checked'):
        value = json.loads((PACKAGE / 'examples/phase2-authoring.json').read_text())
        value.update(reviewed_paths=['current.md', 'implementation.txt', 'proposed.md'], typed_exit=exit_id)
        value['consumer'] = ({'kind': 'workflow', 'id': 'guru-knowledge-final-integration-router'}
                             if exit_id == 'candidate_checked' else {'kind': 'skill', 'id': 'guru-create-task-commit'})
        return value

    def recorded_owner(self, owner):
        directory = self.root / '.trellis/.runtime/check-input'
        directory.mkdir(parents=True, exist_ok=True)
        authoring = directory / 'semantic.json'
        authoring.write_text(json.dumps(owner))
        args = ['--root', str(self.root), '--task', self.fixture.task_ref]
        record = subprocess.run([str(PACKAGE / 'scripts/record-phase2-check.sh'), *args,
                                 '--input', str(authoring)], text=True, capture_output=True)
        self.assertEqual(record.returncode, 0, record.stdout + record.stderr)
        receipt = json.loads(record.stdout)
        self.assertFalse(receipt['formal_exit'])
        path = Path(receipt['result']['artifact_path'])
        checker = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), *args],
                                  text=True, capture_output=True)
        self.assertEqual(checker.returncode, 0, checker.stdout + checker.stderr)
        self.assertFalse(json.loads(checker.stdout)['formal_exit'])
        self.assertEqual(path, Path(json.loads(checker.stdout)['result']['artifact_path']))
        return path

    def invoke(self, public, owner, expected=0):
        directory = self.root / '.trellis/.runtime/check-input'
        directory.mkdir(parents=True, exist_ok=True)
        inp, result = directory / 'input.json', directory / 'owner.json'
        inp.write_text(json.dumps(public))
        if isinstance(owner, Path):
            result = owner
        elif 'schema_version' not in owner:
            result = self.recorded_owner(owner)
        else:
            result.write_text(json.dumps(owner))
        invocation = subprocess.run([str(PACKAGE / 'scripts/invoke.sh'), '--root', str(self.root),
                                     '--input', str(inp), '--owner-result', str(result)],
                                    text=True, capture_output=True)
        self.assertEqual(invocation.returncode, expected, invocation.stdout + invocation.stderr)
        return json.loads(invocation.stdout)

    def test_candidate_write_rebind_and_final_gate_use_real_public_phases(self):
        p = self.fixture.projection
        phases = [p.resolve(self.key)['phase']]
        before = self.begin(); phases.append(p.resolve(self.key)['phase'])
        owner = self.recorded_owner(self.owner())
        checked = self.invoke(self.public, owner)
        phases.append(p.resolve(self.key)['phase'])
        self.assertEqual(checked['exit_id'], 'candidate_checked')
        self.assertEqual(set(checked), {'exit_id', 'task_ref', 'delivery_key', 'candidate'})
        self.assertEqual(p.resolve(self.key)['results']['check'], None)
        self.assertEqual(p.resolve(self.key)['results']['planning']['result_id'], self.plan['result_id'])
        self.assertEqual(self.common.content_identity(self.root), json.loads(owner.read_text())['reviewed_content_sha256'])
        self.assertEqual((self.root / 'current.md').read_text(), 'Existing complete current\n')
        # The original maintenance owner performs the actual reviewed write.
        (self.root / 'current.md').write_text((self.root / 'proposed.md').read_text())
        with self.assertRaises(p.api.delivery_schema.DeliveryError) as stale:
            p.api.delivery_store.verify_candidate(self.root, before)
        self.assertEqual(stale.exception.code, "candidate_mismatch")
        after = self.begin(); phases.append(p.resolve(self.key)['phase'])
        self.assertNotEqual(before['content_ref'], after['content_ref'])
        final = dict(self.public, profile='delivery_initial_check')
        recorded_final = self.recorded_owner(self.owner('passed'))
        result = self.invoke(final, recorded_final)
        phases.append(p.resolve(self.key)['phase'])
        self.assertEqual(phases, ['implementing', 'checking', 'implementing', 'checking', 'reviewing'])
        self.assertEqual(p.resolve(self.key)['results']['check']['candidate'], after)
        # Real final gate output recovery is allowed and creates no new commit.
        self.assertEqual(result, self.invoke(final, recorded_final))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(p.content_base(self.key), self.base)

    def test_lost_candidate_output_requires_begin_check_and_new_judgment_even_no_change(self):
        p = self.fixture.projection
        before = self.begin(); owner = self.recorded_owner(self.owner())
        first = self.invoke(self.public, owner)
        self.invoke(self.public, owner, expected=3)
        self.assertEqual(p.resolve(self.key)['phase'], 'implementing')
        after = self.begin()
        self.assertEqual(before, after)
        second = self.invoke(self.public, self.owner())
        self.assertEqual(first, second)
        self.assertEqual(p.resolve(self.key)['results']['check'], None)
        self.assertEqual((self.root / 'current.md').read_text(), 'Existing complete current\n')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_retained_real_gates_are_history_after_final_write(self):
        p = self.fixture.projection
        self.begin()
        record_gate(p, self.key, 'check', 'actual-prior-check', 'passed', [self.fixture.scope], [])
        record_gate(p, self.key, 'full_review', 'actual-prior-review', 'passed', [self.fixture.scope], [])
        rework(p, self.key, 'full_review', 'implementation', self.fixture.scope, ['readiness'])
        self.begin()
        self.invoke(self.public, self.owner())
        self.assertEqual(p.resolve(self.key)['results']['check']['result_id'], 'actual-prior-check')
        self.assertEqual(p.resolve(self.key)['results']['full_review']['result_id'], 'actual-prior-review')
        (self.root / 'current.md').write_text('Actual changed complete body\n')
        self.begin()
        self.assertEqual(p.gate_applicability(self.key)['check']['kind'], 'not_applicable')
        self.assertEqual(p.gate_applicability(self.key)['full_review']['kind'], 'not_applicable')

    def test_candidate_and_final_profiles_cannot_confuse_success_results(self):
        self.begin()
        self.invoke(self.public, self.owner('passed'), expected=2)
        self.invoke(dict(self.public, profile='delivery_initial_check'), self.owner(), expected=2)
        self.assertEqual(self.fixture.projection.resolve(self.key)['results']['check'], None)

    def test_recorded_candidate_content_change_rejects_without_rewriting_result(self):
        self.begin()
        artifact = self.recorded_owner(self.owner())
        original = artifact.read_bytes()
        (self.root / 'implementation.txt').write_text('Ordinary later implementation change\n')
        checked = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), '--root', str(self.root),
                                  '--task', self.fixture.task_ref], text=True, capture_output=True)
        self.assertEqual(checked.returncode, 3, checked.stdout + checked.stderr)
        self.assertEqual(json.loads(checked.stdout)['field_path'], 'reviewed_content_sha256')
        self.assertEqual(original, artifact.read_bytes())
        self.invoke(self.public, artifact, expected=3)

    def test_complete_recorder_output_is_consumer_only_not_new_record_input(self):
        self.begin()
        artifact = self.recorded_owner(self.owner())
        original = artifact.read_bytes()
        result = subprocess.run([str(PACKAGE / 'scripts/record-phase2-check.sh'), '--root', str(self.root),
            '--task', self.fixture.task_ref, '--input', str(artifact)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        error = json.loads(result.stdout)
        self.assertEqual(('schema_mismatch', 'input'), (error['code'], error['field_path']))
        self.assertIn('MIGRATION-710', error['remediation'])
        self.assertEqual(original, artifact.read_bytes())
        self.assertEqual('candidate_checked', self.invoke(self.public, artifact)['exit_id'])

    def test_checker_identifies_task_locator_after_normal_archive_move(self):
        self.begin()
        artifact = self.recorded_owner(self.owner())
        previous = self.root / self.fixture.task_ref
        archived = self.root / '.trellis/tasks/archive/2026-10' / previous.name
        archived.parent.mkdir(parents=True)
        previous.rename(archived)
        checked = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), '--root', str(self.root),
            '--task', archived.relative_to(self.root).as_posix()], text=True, capture_output=True)
        self.assertEqual(checked.returncode, 3, checked.stdout + checked.stderr)
        error = json.loads(checked.stdout)
        self.assertEqual(('stale_identity', 'task_ref'), (error['code'], error['field_path']))
        self.assertTrue(artifact.is_file())

    def test_checker_preserves_capture_ancestry_after_normal_history_replacement(self):
        self.begin()
        artifact = self.recorded_owner(self.owner())
        original = artifact.read_bytes()
        # A new root history can contain the same business bytes. It still
        # cannot consume a Check captured on the unrelated old history.
        self.git('checkout', '--orphan', 'replacement-history')
        self.git('add', '.')
        self.git('commit', '-qm', 'Replacement root with the same business content')
        checked = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), '--root', str(self.root),
                                  '--task', self.fixture.task_ref], text=True, capture_output=True)
        self.assertEqual(checked.returncode, 3, checked.stdout + checked.stderr)
        error = json.loads(checked.stdout)
        self.assertEqual(('stale_identity', 'phase2_capture_commit'), (error['code'], error['field_path']))
        self.assertEqual(original, artifact.read_bytes())

    def test_checker_identifies_coverage_after_normal_index_change(self):
        self.begin()
        artifact = self.recorded_owner(self.owner())
        original = artifact.read_bytes()
        # Removing a file only from the index leaves its worktree bytes and
        # content token unchanged, but adds a real dirty path to review.
        self.git('rm', '--cached', '.gitignore')
        checked = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), '--root', str(self.root),
                                  '--task', self.fixture.task_ref], text=True, capture_output=True)
        self.assertEqual(checked.returncode, 3, checked.stdout + checked.stderr)
        error = json.loads(checked.stdout)
        self.assertEqual(('stale_identity', 'reviewed_paths'), (error['code'], error['field_path']))
        self.assertEqual(original, artifact.read_bytes())

    def test_metadata_is_not_content_but_actual_mode_changes_are(self):
        candidate = self.begin(); before = self.common.content_identity(self.root)
        directory = self.fixture.projection.planning_directory(self.key)
        (directory / 'test-result.md').write_text('Current validation facts\n')
        self.assertEqual(before, self.common.content_identity(self.root))
        (self.root / 'implementation.txt').chmod(0o755)
        self.assertNotEqual(before, self.common.content_identity(self.root))
        with self.assertRaises(self.fixture.projection.api.delivery_schema.DeliveryError) as stale:
            self.fixture.projection.api.delivery_store.verify_candidate(self.root, candidate)
        self.assertEqual(stale.exception.code, "candidate_mismatch")


if __name__ == '__main__':
    unittest.main()
