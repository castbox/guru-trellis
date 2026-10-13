"""Normal scope publication and original owner re-entry against installed API.

Fixture judgments exercise projections, not semantic review or remote success.
"""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

KERNEL = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KERNEL / 'packages/guru-create-delivery/tests'))
from support import installed_fixture
from runtime.delivery_projection.adapter import authority_ref
from runtime.delivery_projection.gates import record_gate

OWNERS = {
    'planning': 'guru-activate-delivery', 'check': 'guru-check-task',
    'full_review': 'guru-review-branch', 'readiness': 'guru-review-task-delivery',
    'publication': 'guru-publish-task-delivery', 'delivery': 'guru-merge-task-delivery',
}


class ScopeRevisionTests(unittest.TestCase):
    def prepare(self, role):
        fixture = installed_fixture(self)
        key = fixture.create()
        other = fixture.create()
        fixture.projection.select(key)
        if role != 'planning':
            fixture.planning(key)
        if role not in ('planning', 'implementation'):
            (fixture.root / 'candidate.txt').write_text('Existing candidate\n')
            candidate = fixture.projection.candidate(['candidate.txt'], kind='git_free')
            fixture.projection.begin_check(key, candidate)
        if role in ('full_review', 'readiness', 'publication', 'delivery'):
            record_gate(fixture.projection, key, 'check', 'check:existing', 'passed', [fixture.scope], [])
        if role in ('readiness', 'publication', 'delivery'):
            record_gate(fixture.projection, key, 'full_review', 'review:existing', 'passed', [fixture.scope], [])
        if role in ('publication', 'delivery'):
            record_gate(fixture.projection, key, 'readiness', 'ready:existing', 'ready', [fixture.scope], [])
        before = copy.deepcopy(fixture.projection.resolve(key))
        other_before = copy.deepcopy(fixture.projection.resolve(other))
        # Ordinary source edit followed by the actual original scope API.
        (fixture.task / 'prd.md').write_text('整体scope增加必要基础验收\n')
        scope = authority_ref(fixture.task / 'prd.md', fixture.root)
        fixture.projection.scope(scope)
        public = {'profile': 'delivery_scope_revision', 'mode': 'workflow', 'task_ref': fixture.task_ref,
                  'delivery_key': key, 'scope_ref': {'authority': scope, 'anchors': ['验收', '基础']},
                  'source_selection': [], 'revision_refs': ['基础']}
        semantic = {'public_input': public, 'ai_review_gate': {'status': 'passed',
                     'summary': 'Retained current slice covers the actual accepted scope revision.'}}
        return fixture, key, other, before, other_before, public, semantic

    def wrapper(self, fixture, role, public, semantic):
        directory = fixture.root / '.trellis/.runtime/scope-test'
        directory.mkdir(parents=True, exist_ok=True)
        inp, sem = directory / 'input.json', directory / 'semantic.json'
        inp.write_text(json.dumps(public)); sem.write_text(json.dumps(semantic))
        flag = '--semantic-result' if role == 'readiness' else '--review-input' if role in ('publication', 'delivery') else '--owner-result'
        cmd = ['bash', str(KERNEL / 'packages' / OWNERS[role] / 'scripts/invoke.sh'),
               '--root', str(fixture.root), '--input', str(inp), flag, str(sem)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        value = json.loads(result.stdout)
        return value.get('result', value)

    def test_each_original_stage_owner_revises_same_delivery_and_recovers_output(self):
        for role in OWNERS:
            with self.subTest(role=role):
                fixture, key, other, before, other_before, public, semantic = self.prepare(role)
                first = self.wrapper(fixture, role, public, semantic)
                after = copy.deepcopy(fixture.projection.resolve(key))
                recovered = self.wrapper(fixture, role, public, semantic)
                self.assertEqual(first, recovered)
                self.assertEqual(first['exit_id'], 'delivery_scope_revised')
                self.assertEqual(first['delivery_key'], key)
                self.assertEqual(after['phase'], 'planning')
                self.assertEqual(after['scope_ref'], public['scope_ref'])
                self.assertTrue(all(result is None for result in after['results'].values()))
                for name in ('candidate', 'publication_result', 'delivery_result', 'planning_root'):
                    self.assertEqual(after[name], before[name])
                self.assertEqual(fixture.projection.resolve(key), after)
                self.assertEqual(fixture.projection.resolve(other), other_before)
                self.assertNotIn('scope_ref', first)

    def test_real_apply_clean_and_reapply_install_scope_module_and_original_wrapper(self):
        fixture, key, other, before, other_before, public, semantic = self.prepare('planning')
        source_root = KERNEL.parents[2]
        (fixture.root / '.trellis/workflow.md').write_bytes(
            (source_root / 'trellis/workflows/guru-team/workflow.md').read_bytes())
        apply_script = source_root / 'trellis/presets/guru-team/scripts/bash/apply.sh'
        # The source-loaded installer resolves its temporary lifecycle from
        # the caller source checkout; use a fresh source copy as that caller.
        import shutil
        caller = fixture.root / 'installer-source'
        shutil.copytree(KERNEL / 'runtime', caller / 'trellis/skills/guru-team/runtime',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        outputs = []
        for turn in range(2):
            applied = subprocess.run(['bash', str(apply_script), '--repo', str(fixture.root)],
                                     cwd=caller, capture_output=True, text=True)
            self.assertEqual(applied.returncode, 0, applied.stdout[-2000:] + applied.stderr)
            result = json.loads(applied.stdout)
            self.assertEqual(result['skill_installed_validation']['returncode'], 0)
            installed_root = fixture.root / '.trellis/guru-team'
            module = installed_root / 'runtime/delivery_projection/scope_revision.py'
            self.assertEqual(module.read_bytes(), (KERNEL / 'runtime/delivery_projection/scope_revision.py').read_bytes())
            import os
            imported = subprocess.run([sys.executable, '-c', 'from runtime.delivery_projection.scope_revision import revise; assert callable(revise)'],
                                      cwd=fixture.root, env={**os.environ, 'PYTHONPATH': str(installed_root)},
                                      capture_output=True, text=True)
            self.assertEqual(imported.returncode, 0, imported.stderr)
            directory = fixture.root / '.trellis/.runtime/scope-installed-test'
            directory.mkdir(parents=True, exist_ok=True)
            inp, sem = directory / 'input.json', directory / 'semantic.json'
            inp.write_text(json.dumps(public)); sem.write_text(json.dumps(semantic))
            wrapper = installed_root / 'skills/packages/guru-activate-delivery/scripts/invoke.sh'
            completed = subprocess.run(['bash', str(wrapper), '--root', str(fixture.root),
                                        '--input', str(inp), '--owner-result', str(sem)],
                                       cwd=fixture.root, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            output = json.loads(completed.stdout)
            outputs.append(output.get('result', output))
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0]['exit_id'], 'delivery_scope_revised')
        self.assertEqual(fixture.projection.resolve(other), other_before)

    def test_implementation_owner_keeps_candidate_and_same_key(self):
        fixture, key, other, before, other_before, public, semantic = self.prepare('implementation')
        self.assertEqual(fixture.projection.revise_implementation_scope(key, public['scope_ref']), key)
        self.assertEqual(fixture.projection.revise_implementation_scope(key, public['scope_ref']), key)
        after = fixture.projection.resolve(key)
        self.assertEqual(after['scope_ref'], public['scope_ref'])
        self.assertEqual(after['candidate'], before['candidate'])
        self.assertEqual(fixture.projection.resolve(other), other_before)


if __name__ == '__main__':
    unittest.main()
