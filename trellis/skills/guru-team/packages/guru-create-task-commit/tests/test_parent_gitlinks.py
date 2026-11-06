from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
for source in (PACKAGE.parents[1], PACKAGE / 'runtime'):
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))

from common import capture_snapshot, validate
from execute import _materialize_exact_index
from runtime.io import CommandError


class ParentGitlinkCommitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'parent'
        self.repo.mkdir()
        self.git('init', '-q', '-b', 'feature/atomic')
        self.git('config', 'user.name', 'Atomic Test')
        self.git('config', 'user.email', 'atomic@example.test')
        (self.repo / 'ordinary.txt').write_text('before\n')
        self.git('add', 'ordinary.txt')
        self.git('update-index', '--add', '--cacheinfo', '160000', '1' * 40, 'module')
        self.git('commit', '-qm', 'base')
        self.pre = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args, env=None):
        return subprocess.check_output(['git', *args], cwd=self.repo,
                                       env={**os.environ, **(env or {})}, text=True)

    def candidate(self):
        snapshot = capture_snapshot(self.repo)
        return {'git': {'pre_commit_head': self.pre}, 'dirty_snapshot': snapshot,
                'exact_stage_paths': [row['path'] for row in snapshot['entries']]}

    def materialize(self, candidate):
        live = self.git('ls-files', '--stage', '-z')
        env = {'GIT_INDEX_FILE': str(self.root / 'transaction-index')}
        tree = _materialize_exact_index(self.repo, candidate, env)
        self.assertEqual(live, self.git('ls-files', '--stage', '-z'))
        return self.git('ls-tree', '-r', tree)

    def test_parent_oid_is_used_despite_different_dirty_child_head(self):
        child = self.repo / 'module'
        child.mkdir()
        subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=child, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Child Test'], cwd=child, check=True)
        subprocess.run(['git', 'config', 'user.email', 'child@example.test'], cwd=child, check=True)
        (child / 'child.txt').write_text('committed\n')
        subprocess.run(['git', 'add', '.'], cwd=child, check=True)
        subprocess.run(['git', 'commit', '-qm', 'child'], cwd=child, check=True)
        (child / 'child.txt').write_text('dirty child\n')
        self.git('update-index', '--cacheinfo', '160000', '2' * 40, 'module')
        before = self.candidate()
        row = next(row for row in before['dirty_snapshot']['entries'] if row['path'] == 'module')
        self.assertEqual('2' * 40, row['index_blob'])
        self.assertIsNone(row['worktree_sha256'])
        self.assertNotIn('gitlink_head', row)
        (child / 'untracked.txt').write_text('unrelated\n')
        self.assertEqual(before, self.candidate())
        self.assertIn('160000 commit ' + '2' * 40 + '\tmodule', self.materialize(before))

    def test_staged_delete_removes_parent_entry_while_child_directory_remains(self):
        child = self.repo / 'module'
        child.mkdir()
        (child / 'retained.txt').write_text('keep child data\n')
        self.git('update-index', '--force-remove', '--', 'module')
        candidate = self.candidate()
        rows = candidate['dirty_snapshot']['entries']
        self.assertEqual(['module'], [row['path'] for row in rows])
        self.assertEqual(('160000', None, True), (rows[0]['mode'], rows[0]['index_blob'], rows[0]['deleted']))
        self.assertNotIn('\tmodule', self.materialize(candidate))
        self.assertEqual('keep child data\n', (child / 'retained.txt').read_text())

    def test_added_absent_gitlink_and_blob_replacement_use_parent_types(self):
        self.git('update-index', '--add', '--cacheinfo', '160000', '3' * 40, 'added')
        self.git('update-index', '--force-remove', '--', 'module')
        (self.repo / 'module').write_text('replacement\n')
        self.git('add', 'module')
        self.git('update-index', '--cacheinfo', '160000', '4' * 40, 'ordinary.txt')
        tree = self.materialize(self.candidate())
        self.assertIn('160000 commit ' + '3' * 40 + '\tadded', tree)
        self.assertIn('160000 commit ' + '4' * 40 + '\tordinary.txt', tree)
        blob = self.git('hash-object', 'module').strip()
        self.assertIn('100644 blob ' + blob + '\tmodule', tree)

    def test_changed_parent_index_is_stale_before_transaction_index_write(self):
        self.git('update-index', '--cacheinfo', '160000', '2' * 40, 'module')
        candidate = self.candidate()
        self.git('update-index', '--cacheinfo', '160000', '3' * 40, 'module')
        with self.assertRaises(CommandError) as caught:
            self.materialize(candidate)
        self.assertEqual('stale_identity', caught.exception.code)
        self.assertFalse((self.root / 'transaction-index').exists())

    def test_ordinary_rename_still_removes_source_and_stages_destination(self):
        (self.repo / 'ordinary.txt').rename(self.repo / 'renamed.txt')
        self.git('add', '-A', '--', 'ordinary.txt', 'renamed.txt')
        candidate = self.candidate()
        row = next(row for row in candidate['dirty_snapshot']['entries'] if row['path'] == 'renamed.txt')
        self.assertEqual('ordinary.txt', row['renamed_from'])
        candidate['exact_stage_paths'].append('ordinary.txt')
        tree = self.materialize(candidate)
        self.assertIn('\trenamed.txt', tree)
        self.assertNotIn('\tordinary.txt', tree)

    def test_new_private_schema_rejects_old_unexecuted_delivery_candidate(self):
        with self.assertRaises(CommandError) as caught:
            validate(PACKAGE, {'delivery_key': {}, 'schema_version': 'delivery-2.0'})
        self.assertEqual('stale_identity', caught.exception.code)
        schema = json.loads((PACKAGE / 'schemas/delivery-commit-candidate-3.0.schema.json').read_text())
        validator = Draft202012Validator({'$ref': '#/$defs/snapshotEntry', '$defs': schema['$defs']})
        self.git('update-index', '--cacheinfo', '160000', '2' * 40, 'module')
        row = self.candidate()['dirty_snapshot']['entries'][0]
        validator.validate(row)


if __name__ == '__main__':
    unittest.main()
