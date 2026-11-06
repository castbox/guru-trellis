"""Finalize diagnoses caller omissions before repeating target commands."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / 'runtime'))
spec = importlib.util.spec_from_file_location('finalize_maintenance', PACKAGE / 'runtime/invoke.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
from runtime.io import CommandError


class FinalizeReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def fixture(self, profile, suffix=''):
        root = self.base / (profile + suffix)
        root.mkdir()
        active = '.trellis/tasks/selected'
        archive = '.trellis/tasks/archive/2026-11/selected'
        task = root / active / 'task.json'
        task.parent.mkdir(parents=True)
        task.write_text(json.dumps({'schema_version': '2.0', 'id': 'selected', 'lifecycle_generation': 0}))
        key = {'task_id': 'selected', 'lifecycle_generation': 0}
        state = {
            'phase': 'verification_required',
            'public_input': {'profile': profile, 'target_checkout': str(root), 'key': key,
                             'task_ref': archive if profile == 'archive_resume' else active},
            'public_plan': {'guard': {'archive_ref': archive}},
        }
        if profile == 'archive_resume':
            state['resumed_task'] = {'key': key, 'task_ref': active}
        checkpoint = root / 'checkpoint.json'
        checkpoint.write_text(json.dumps(state))
        public = root / 'resume.json'
        public.write_text(json.dumps({'profile': 'resume', 'recovery_ref': str(checkpoint)}))
        review = {'observations': {}, 'caller_note': 'An existing caller may retain extra fields.'}
        for name in ['native'] + ([] if profile == 'history_closeout' else ['next_owner']):
            script = root / '.trellis/scripts' / (name + '.py')
            script.parent.mkdir(parents=True, exist_ok=True)
            script.write_text(
                'from pathlib import Path\n'
                f'Path("{name}-called").write_text("executed")\n'
                f'print("{name} context")\n'
            )
            argv = [sys.executable, script.relative_to(root).as_posix()]
            review[name + '_argv'] = argv
            review['observations'][name] = {
                'argv': argv, 'returncode': 0, 'stdout': name + ' context\n', 'stderr': '',
            }
        review['output'] = ({'exit_id': 'history_archived', 'key': key, 'archive_ref': archive}
                            if profile == 'history_closeout' else
                            {'exit_id': 'task_resumed', **key, 'task_ref': active})
        return root, public, checkpoint, review

    def finalize(self, root, public, review):
        path = root / 'review.json'
        path.write_text(json.dumps(review))
        return owner.run(PACKAGE, {'stdout': 'single_typed_exit'}, [
            '--root', str(root), '--input', str(public), '--action', 'finalize',
            '--review-input', str(path),
        ])

    def assert_no_commands(self, root):
        self.assertFalse((root / 'native-called').exists())
        self.assertFalse((root / 'next_owner-called').exists())

    def test_missing_review_fields_stop_before_any_command_or_checkpoint_write(self):
        for field in ['native_argv', 'observations', 'output', 'next_owner_argv']:
            with self.subTest(field=field):
                root, public, checkpoint, review = self.fixture('archive_resume', '-' + field)
                del review[field]
                before = checkpoint.read_bytes()
                with self.assertRaises(CommandError) as raised:
                    self.finalize(root, public, review)
                self.assertEqual((raised.exception.code, raised.exception.field_path),
                                 ('schema_mismatch', 'review_input.' + field))
                self.assertIn('contract.md#finalize-review-input', raised.exception.remediation)
                self.assert_no_commands(root)
                self.assertEqual(checkpoint.read_bytes(), before)

    def test_missing_observation_member_stops_before_both_commands(self):
        root, public, checkpoint, review = self.fixture('archive_resume')
        del review['observations']['next_owner']['stdout']
        before = checkpoint.read_bytes()
        with self.assertRaises(CommandError) as raised:
            self.finalize(root, public, review)
        self.assertEqual(raised.exception.field_path, 'review_input.observations.next_owner.stdout')
        self.assert_no_commands(root)
        self.assertEqual(checkpoint.read_bytes(), before)

    def test_invalid_next_owner_entry_stops_before_native_execution(self):
        root, public, _, review = self.fixture('archive_resume')
        review['next_owner_argv'] = []
        with self.assertRaises(CommandError) as raised:
            self.finalize(root, public, review)
        self.assertEqual(raised.exception.field_path, 'review_input.next_owner_argv')
        self.assert_no_commands(root)

    def test_existing_success_shapes_keep_extra_caller_fields(self):
        for profile in ['convert', 'archive_resume', 'history_closeout']:
            with self.subTest(profile=profile):
                root, public, checkpoint, review = self.fixture(profile)
                result = self.finalize(root, public, review)
                self.assertEqual(result, review['output'])
                self.assertEqual(json.loads(checkpoint.read_text())['terminal_output'], result)
                self.assertEqual((root / 'native-called').read_text(), 'executed')
                self.assertEqual((root / 'next_owner-called').exists(), profile != 'history_closeout')

    def test_stale_observations_still_reexecute_and_block(self):
        root, public, checkpoint, review = self.fixture('history_closeout')
        review['observations']['native']['stdout'] = 'previous context\n'
        before = checkpoint.read_bytes()
        with self.assertRaises(CommandError) as raised:
            self.finalize(root, public, review)
        self.assertEqual(raised.exception.code, 'stale_native_observation')
        self.assertTrue((root / 'native-called').exists())
        self.assertEqual(checkpoint.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
