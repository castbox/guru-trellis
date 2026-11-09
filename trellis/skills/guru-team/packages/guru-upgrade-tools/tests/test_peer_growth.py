"""Real Git topology for observation preservation, not a synthetic key set."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / 'runtime'))
import tools_owner as owner


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def repository(base):
    root = base / 'target'
    root.mkdir()
    git(root, 'init', '-q', '-b', 'main')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'user.name', 'Fixture')
    (root / 'business').write_text('business')
    git(root, 'add', '.')
    git(root, 'commit', '-qm', 'fixture')
    return root.resolve()


class PeerGrowthTests(unittest.TestCase):
    def fixture(self, base, *, absent=False):
        root = repository(base)
        old = owner.legacy_owner(PACKAGE)
        asset = root / '.trellis/guru-team/asset'
        asset.parent.mkdir(parents=True)
        asset.write_text('target tool')
        if absent:
            asset.unlink()
        cp = {'peer_pointers': owner.peer_pointers(root, old),
              'preimages': old.snapshot(root, base / 'recovery', {'.trellis/guru-team/asset'}, {}),
              'plan': {'upstream_plan': {'actions': []}}}
        return root, old, cp

    def test_new_independent_registered_peer_does_not_refresh_original_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root, old, cp = self.fixture(base)
            original = json.dumps(cp, sort_keys=True)
            peer = base / 'normal peer'
            git(root, 'worktree', 'add', '-q', '-b', 'peer', str(peer))
            tool = peer / '.trellis/guru-team/asset'
            tool.parent.mkdir(parents=True)
            tool.write_bytes(b'peer tool')
            tool.chmod(0o640)
            pointer = peer / '.trellis/.runtime/guru-team/python/active.json'
            pointer.parent.mkdir(parents=True)
            pointer.write_text('{"schema_version":"2.0","runtime_id":"existing-peer"}\n')
            before = {path: (path.read_bytes(), path.stat().st_mode & 0o777)
                      for path in (tool, pointer, peer / 'business')}
            self.assertTrue(set(owner.peer_pointers(root, old)) - set(cp['peer_pointers']))
            owner.unchanged_peers(root, cp, old)
            self.assertEqual(json.dumps(cp, sort_keys=True), original)
            for path, expected in before.items():
                self.assertEqual((path.read_bytes(), path.stat().st_mode & 0o777), expected)

    def test_changed_existing_peer_pointer_remains_a_preservation_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root, old, cp = self.fixture(base)
            peer = base / 'peer'
            git(root, 'worktree', 'add', '-q', '-b', 'peer', str(peer))
            pointer = peer / '.trellis/.runtime/guru-team/python/active.json'
            pointer.parent.mkdir(parents=True)
            old.write_json(pointer, {'schema_version': '2.0', 'runtime_id': 'before'})
            cp['peer_pointers'] = owner.peer_pointers(root, old)
            original = json.dumps(cp, sort_keys=True)
            # Ordinary environment selection change after this operation froze.
            old.write_json(pointer, {'schema_version': '2.0', 'runtime_id': 'after'})
            with self.assertRaisesRegex(ValueError, 'peer/common Python pointer changed'):
                owner.unchanged_peers(root, cp, old)
            self.assertEqual(json.dumps(cp, sort_keys=True), original)
            self.assertEqual(json.loads(pointer.read_text())['runtime_id'], 'after')

    def test_new_peer_tool_alias_is_not_accepted_as_isolated_growth(self):
        for sharing in ('parent_alias', 'missing_leaf_parent_alias', 'leaf_symlink', 'hardlink'):
            with self.subTest(sharing=sharing), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                root, old, cp = self.fixture(base, absent=sharing == 'missing_leaf_parent_alias')
                peer = base / 'peer'
                git(root, 'worktree', 'add', '-q', '-b', 'peer', str(peer))
                target = root / '.trellis/guru-team/asset'
                if sharing in ('parent_alias', 'missing_leaf_parent_alias'):
                    (peer / '.trellis').mkdir()
                    (peer / '.trellis/guru-team').symlink_to(target.parent, target_is_directory=True)
                else:
                    peer_asset = peer / '.trellis/guru-team/asset'
                    peer_asset.parent.mkdir(parents=True)
                    if sharing == 'leaf_symlink':
                        peer_asset.symlink_to(target)
                    else:
                        os.link(target, peer_asset)
                with self.assertRaisesRegex(ValueError, 'write set physically overlaps'):
                    owner.unchanged_peers(root, cp, old)
                if sharing == 'missing_leaf_parent_alias':
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual(target.read_text(), 'target tool')
