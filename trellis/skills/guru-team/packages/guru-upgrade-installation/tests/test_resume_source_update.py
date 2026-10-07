from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / 'runtime'))
from owner import MigrationError, TARGET_CORE, TARGET_GURU, resume, update_resume_source, run, rollback


class ResumeSourceUpdateTests(unittest.TestCase):
    def fixture(self, directory):
        base = Path(directory).resolve()
        source, root, recovery = base / 'source', base / 'target', base / 'recovery'
        for path in (source, root, recovery):
            path.mkdir()
        for argv in (['init', '-q'], ['config', 'user.name', 'Fixture'], ['config', 'user.email', 'fixture@example.invalid']):
            self.git(source, *argv)
        for name, content in {
            'trellis/guru-team-extension.json': json.dumps({'version': TARGET_GURU, 'target_trellis_cli': TARGET_CORE}),
            'trellis/presets/guru-team/source/trellis-source.json': json.dumps({'cli_version': TARGET_CORE}),
            'trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md': '# fixture',
            'trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py': '# fixture',
            'trellis/pending.txt': 'original',
        }.items():
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.git(source, 'add', '.')
        self.git(source, 'commit', '-qm', 'original source')
        previous = self.git(source, 'rev-parse', 'HEAD')
        plan = {'dependency_mode': 'source_locked', 'selected_platforms': ['codex'], 'core_plan': {'tasks': []},
                'guru_decisions': [], 'controls': [],
                'workflow': {'provider_ref': previous, 'action': 'replace', 'expected_sha256': 'a' * 64}}
        paths = {'.trellis/guru-team/extension.json', '.trellis/workflow.md', '.trellis/workflow.md.new', '.trellis/workflow.md.bak', 'managed.txt'}
        paths |= {p + suffix for p in list(paths) for suffix in ('.new', '.bak')}
        checkpoint = {'schema_version': '1.0', 'controls': {}, 'root': str(root), 'source': str(source), 'source_ref': previous, 'phase': 'guru', 'fork': str(base / 'fork.js'),
                      'plan': plan, 'preimages': {'repo:' + p: {'sha256': None, 'mode': None} for p in paths},
                      'business_before': 'initial business', 'control_before': 'b' * 64, 'task_after_core': 'c' * 64,
                      'old_installation': {'core': '0.6.0', 'guru': '0.6.5-guru.41', 'source': {}}, 'old_managed': [],
                      'baseline': {'initial': True}, 'business_after': 'paused business'}
        (recovery / 'checkpoint.json').write_text(json.dumps(checkpoint))
        (source / 'trellis/pending.txt').write_text('successor runtime fix')
        self.git(source, 'commit', '-qam', 'runtime fix')
        proposed = copy.deepcopy(plan)
        proposed['workflow']['provider_ref'] = self.git(source, 'rev-parse', 'HEAD')
        return source, root, recovery, checkpoint, proposed

    def git(self, root, *args):
        return subprocess.check_output(['git', *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()

    def contexts(self, source, paths=None):
        module = SimpleNamespace(managed_transaction_paths=lambda *args: {Path(p) for p in (paths or ['managed.txt'])})
        verifier = SimpleNamespace(validate_fork_source=lambda *args: {'cli_version': TARGET_CORE})
        return (patch('owner.source_root', return_value=source), patch('owner.installer', return_value=module),
                patch('owner.fork_checkout_root', return_value=source),
                patch.dict(sys.modules, {'verify_trellis_compatibility_matrix': verifier}),
                patch('owner.validate_task_dispositions'))

    def invoke(self, source, root, recovery, checkpoint, plan, paths=None):
        from contextlib import ExitStack
        with ExitStack() as stack:
            for context in self.contexts(source, paths):
                stack.enter_context(context)
            update_resume_source(PACKAGE, root, recovery, checkpoint, plan)

    def test_successor_updates_only_source_pointer_and_workflow_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            source, root, recovery, checkpoint, proposed = self.fixture(directory)
            expected = copy.deepcopy(checkpoint)
            expected['source_ref'] = proposed['workflow']['provider_ref']
            expected['plan'] = proposed
            self.invoke(source, root, recovery, checkpoint, proposed)
            self.assertEqual(checkpoint, expected)
            self.assertEqual(json.loads((recovery / 'checkpoint.json').read_text()), expected)
            self.assertEqual(list(root.iterdir()), [])

    def test_initial_immutable_tag_provider_resolves_to_original_source(self):
        for annotated in (False, True):
            with self.subTest(annotated=annotated), tempfile.TemporaryDirectory() as directory:
                source, root, recovery, checkpoint, proposed = self.fixture(directory)
                argv = ['tag'] + (['-a', '-m', 'original source'] if annotated else [])
                self.git(source, *argv, 'migration-source', checkpoint['source_ref'])
                checkpoint['plan']['workflow']['provider_ref'] = 'migration-source'
                self.invoke(source, root, recovery, checkpoint, proposed)
                self.assertEqual(checkpoint['source_ref'], proposed['workflow']['provider_ref'])

    def test_normal_incompatible_successors_leave_checkpoint_unchanged(self):
        for case in ('core', 'preset', 'complete', 'plan', 'lock', 'manifest', 'footprint', 'dirty', 'provider', 'source_path', 'unrelated'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                source, root, recovery, checkpoint, proposed = self.fixture(directory)
                paths = None
                if case in ('core', 'preset', 'complete'):
                    checkpoint['phase'] = case
                elif case == 'plan':
                    proposed['selected_platforms'] = ['claude']
                elif case in ('lock', 'manifest'):
                    name = 'trellis/presets/guru-team/source/trellis-source.json' if case == 'lock' else 'trellis/guru-team-extension.json'
                    (source / name).write_text('{}')
                    self.git(source, 'commit', '-qam', 'changed target')
                    proposed['workflow']['provider_ref'] = self.git(source, 'rev-parse', 'HEAD')
                elif case == 'footprint':
                    paths = ['new-managed.txt']
                elif case == 'dirty':
                    (source / 'trellis/pending.txt').write_text('pending fix')
                elif case == 'provider':
                    proposed['workflow']['provider_ref'] = checkpoint['source_ref']
                elif case == 'source_path':
                    checkpoint['source'] = str(source.parent / 'other-source')
                elif case == 'unrelated':
                    self.git(source, 'checkout', '--orphan', 'unrelated')
                    self.git(source, 'commit', '-qm', 'unrelated source')
                    proposed['workflow']['provider_ref'] = self.git(source, 'rev-parse', 'HEAD')
                before = copy.deepcopy(checkpoint)
                saved = (recovery / 'checkpoint.json').read_bytes()
                with self.assertRaises(MigrationError):
                    self.invoke(source, root, recovery, checkpoint, proposed, paths)
                self.assertEqual(checkpoint, before)
                self.assertEqual((recovery / 'checkpoint.json').read_bytes(), saved)
                self.assertEqual(list(root.iterdir()), [])

    def test_omitted_plan_keeps_strict_source_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            source, root, recovery, checkpoint, proposed = self.fixture(directory)
            with patch('owner.source_root', return_value=source), self.assertRaisesRegex(MigrationError, 'HEAD changed'):
                resume(PACKAGE, root, recovery, checkpoint)

    def test_same_source_plan_is_only_noop(self):
        with tempfile.TemporaryDirectory() as directory:
            source, root, recovery, checkpoint, proposed = self.fixture(directory)
            self.git(source, 'checkout', '-q', checkpoint['source_ref'])
            before = (recovery / 'checkpoint.json').read_bytes()
            self.invoke(source, root, recovery, checkpoint, copy.deepcopy(checkpoint['plan']))
            self.assertEqual((recovery / 'checkpoint.json').read_bytes(), before)
            with self.assertRaisesRegex(MigrationError, 'unchanged migration plan'):
                self.invoke(source, root, recovery, checkpoint, proposed)

    def test_successor_resume_runs_remaining_phases_without_core_and_keeps_anchors(self):
        from contextlib import ExitStack
        import owner
        with tempfile.TemporaryDirectory() as directory:
            source, root, recovery, checkpoint, proposed = self.fixture(directory)
            self.git(root, 'init', '-q')
            self.git(root, 'config', 'user.name', 'Fixture')
            self.git(root, 'config', 'user.email', 'fixture@example.invalid')
            self.git(root, 'commit', '--allow-empty', '-qm', 'initial target')
            checkpoint['controls'] = {}
            checkpoint['plan']['workflow']['action'] = 'preserve'
            proposed['workflow']['action'] = 'preserve'
            checkpoint['plan']['workflow']['expected_sha256'] = None
            proposed['workflow']['expected_sha256'] = None
            from files import business_state, control_token, task_token
            checkpoint['business_before'] = business_state(root, {key[5:] for key in checkpoint['preimages']})
            checkpoint['control_before'] = control_token(checkpoint)
            checkpoint['task_after_core'] = task_token(root, checkpoint)
            anchors = {key: copy.deepcopy(checkpoint[key]) for key in
                       ('preimages', 'business_before', 'control_before', 'task_after_core', 'old_installation', 'old_managed', 'fork')}
            module = SimpleNamespace(
                MANAGED_ASSET_PATHS=[],
                managed_transaction_paths=lambda *args: {Path('managed.txt')},
                managed_source_projections=lambda *args: {},
                install_assets=lambda *args, **kwargs: {'skill_packages': {'status': 'ok'}, 'overlays': {'status': 'ok'},
                                                       'skill_installed_validation': {'returncode': 0}},
            )
            real_command = owner.command
            commands = []
            def command(argv, cwd):
                commands.append(argv)
                if argv[0] == 'env':
                    return '{"status":"passed"}'
                return real_command(argv, cwd)
            with ExitStack() as stack:
                for context in self.contexts(source):
                    stack.enter_context(context)
                stack.enter_context(patch('owner.installer', return_value=module))
                stack.enter_context(patch('owner.command', side_effect=command))
                self.assertEqual(resume(PACKAGE, root, recovery, checkpoint, proposed)['exit_id'], 'upgraded')
            self.assertFalse(any('migrate' in argv for argv in commands))
            self.assertEqual(checkpoint['phase'], 'complete')
            for key, value in anchors.items():
                self.assertEqual(checkpoint[key], value)
            self.assertEqual(rollback(root, recovery, checkpoint)['exit_id'], 'rolled_back')
            self.assertFalse(recovery.exists())

    def test_run_dispatch_passes_resume_plan_without_initial_begin(self):
        with tempfile.TemporaryDirectory() as directory:
            source, root, recovery, checkpoint, proposed = self.fixture(directory)
            reference = '83139db2-e826-42aa-9161-c4b46ae7e62e'
            git_dir = root / '.git'
            stored = git_dir / 'guru-team/install-upgrade' / reference
            stored.mkdir(parents=True)
            (stored / 'checkpoint.json').write_text(json.dumps(checkpoint))
            input_path, plan_path = Path(directory) / 'input.json', Path(directory) / 'plan.json'
            input_path.write_text(json.dumps({'profile': 'resume', 'recovery_ref': reference}))
            plan_path.write_text(json.dumps(proposed))
            result = {'exit_id': 'resume_required', 'profile': 'resume', 'recovery_ref': reference}
            with patch('owner.git', return_value=str(git_dir)), patch('owner.begin') as begin, patch('owner.resume', return_value=result) as writer:
                self.assertEqual(run(PACKAGE, {'runtime_role': 'invoke'}, ['--root', str(root), '--input', str(input_path), '--plan', str(plan_path)]), result)
                begin.assert_not_called()
                self.assertEqual(writer.call_args.args[-1], proposed)


if __name__ == '__main__':
    unittest.main()
