"""Cross-source recovery engine tests with a normal schema1.0 owner checkpoint.

Git, source identities, preimages and owner transitions are real. The public SDK,
preset asset writer and target native checks are isolated external boundaries;
these module tests do not claim complete installed/native recovery evidence.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[4]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / 'runtime'))
import tools_owner as owner
from test_peer_growth import git, repository


class FrozenSourceRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix='guru-frozen-assets-')
        cls.source = Path(cls.directory.name) / 'original-source'
        cls.source.mkdir()
        # A complete committed source is a normal old asset package, not patched
        # target code or a manufactured checkpoint. HEAD need not be latest main.
        archive = subprocess.check_output(['git', 'archive', 'HEAD', 'trellis'], cwd=SOURCE)
        with tarfile.open(fileobj=io.BytesIO(archive)) as files:
            files.extractall(cls.source, filter='data')
        (cls.source / '.gitignore').write_text('__pycache__/\n*.pyc\n')
        git(cls.source, 'init', '-q', '-b', 'main')
        git(cls.source, 'config', 'user.email', 'fixture@example.invalid')
        git(cls.source, 'config', 'user.name', 'Fixture')
        git(cls.source, 'add', '.')
        git(cls.source, 'commit', '-qm', 'Original complete asset source')
        cls.asset_package = cls.source / 'trellis/skills/guru-team/packages/guru-upgrade-tools'
        spec = importlib.util.spec_from_file_location('original_frozen_tools_engine', cls.asset_package / 'runtime/tools_owner.py')
        cls.original = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.original)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def fixture(self, base, *, pending=False, initial=False):
        root = repository(base)
        asset = root / 'asset'
        asset.write_text('original tool')
        manifest = root / '.trellis/guru-team/extension.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text('{"extension":{"version":"old-guru"}}')
        old = owner.legacy_owner(self.asset_package)
        plan = {'upstream_source': {'dependency_mode': 'local_candidate'},
                'upstream_plan': {'operation_id': 'original-public-operation', 'actions': []},
                'selected_platforms': ['codex'], 'guru_decisions': []}
        public = {'profile': 'install', 'source_ref': git(self.source, 'rev-parse', 'HEAD'),
                  'dependency_mode': 'local_candidate', 'checkout': str(root)}
        facts = {'installed_version': 'old-guru', 'managed': [],
                 'guru_paths': ['asset', '.trellis/guru-team/extension.json'],
                 'peer_pointers': self.original.peer_pointers(root, old)}
        writes = []

        def install(workflow, destination, selected_root, platforms, **kwargs):
            self.assertEqual(workflow, self.source / 'trellis/workflows/guru-team')
            self.assertEqual(selected_root, root)
            writes.append(kwargs['tools_maintenance'])
            asset.write_text('installed original asset')
            manifest.write_text('{"extension":{"version":"original-guru"}}')
            return {'skill_packages': {'status': 'ok'}, 'overlays': {'status': 'ok'},
                    'skill_installed_validation': {'returncode': 0}}

        installer = SimpleNamespace(install_assets=install)
        with patch.object(self.original, 'legacy_owner', return_value=old), \
                patch.object(self.original, 'inventory', return_value=facts):
            recovery, cp = self.original.begin(self.asset_package, root, public, plan)
        before = {key: cp[key] for key in ('source', 'source_ref', 'source_token', 'public', 'plan', 'preimages', 'peer_pointers', 'upstream_ref')}
        if initial:
            return root, recovery, cp, old, installer, writes, before
        # The original public owner response and asset writer are external to
        # the recovery engine under test. Its ordinary target-check error leaves
        # the original owner at its real pending preset stage.
        def apply(descriptor, method, payload):
            self.assertEqual(method, 'applyMaintenance')
            Path(cp['upstream_ref']).parent.mkdir(parents=True, exist_ok=True)
            Path(cp['upstream_ref']).write_text('{"phase":"applied"}')
            return {'status': 'applied', 'recovery_ref': cp['upstream_ref']}

        with patch.object(self.original, 'legacy_owner', return_value=old), \
                patch.object(self.original, 'upstream_source'), \
                patch.object(self.original, 'call', side_effect=apply), \
                patch.object(old, 'installer', return_value=installer), \
                patch.object(self.original, 'validate_actual_target', side_effect=OSError('target check unavailable') if pending else None):
            result = self.original.resume(self.asset_package, root, recovery, cp)
        self.assertEqual(result['exit_id'], 'resume_required' if pending else 'tools_upgraded')
        self.assertEqual(cp['phase'], 'preset' if pending else 'complete')
        self.assertEqual({key: cp[key] for key in before}, before)
        return root, recovery, cp, old, installer, writes, before

    def invoke(self, root, ref, action, old, installer, *, native_error=None, target_error=None, public_result=None):
        public = {'profile': 'recover_frozen_source', 'action': action, 'recovery_ref': ref}
        current = owner.legacy_owner(PACKAGE)
        def helper(package):
            return old if package == self.asset_package else current
        def public_call(descriptor, method, payload):
            result = public_result or {'status': 'rolled_back'}
            if result['status'] == 'applied':
                record = Path(result['recovery_ref'])
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text('{"phase":"applied"}')
            return result
        with patch.object(owner, 'legacy_owner', side_effect=helper), \
                patch.object(owner, 'upstream_source'), \
                patch.object(old, 'installer', return_value=installer), \
                patch.object(owner, 'validate_actual_target', side_effect=target_error), \
                patch.object(owner, 'old_native_smoke', side_effect=native_error), \
                patch.object(owner, 'call', side_effect=public_call):
            return owner.run(PACKAGE, {'runtime_role': 'invoke'}, ['--root', str(root), '--input', json.dumps(public)])

    def test_pending_preset_uses_original_assets_and_preserves_frozen_operation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory), pending=True)
            source_bytes = (self.source / 'trellis/guru-team-extension.json').read_bytes()
            peer = Path(directory) / 'later-peer'
            git(root, 'worktree', 'add', '-q', '-b', 'peer', str(peer))
            result = self.invoke(root, recovery.name, 'resume', old, installer)
            self.assertEqual(result, {'exit_id': 'tools_upgraded', 'installed_version': 'original-guru',
                                     'recovery_ref': recovery.name, 'unverified': ['formal_fork_source_lock']})
            self.assertEqual(len(writes), 2)  # original pending action, then same-action continuation
            after = json.loads((recovery / 'checkpoint.json').read_text())
            self.assertEqual({key: after[key] for key in before}, before)
            self.assertEqual(after['phase'], 'complete')
            self.assertEqual((self.source / 'trellis/guru-team-extension.json').read_bytes(), source_bytes)
            for call in writes:
                self.assertEqual(call, {'source': cp['plan']['upstream_source'], 'plan': cp['plan']['upstream_plan'],
                                        'recovery_ref': cp['upstream_ref']})

    def test_public_pending_checkpoint_uses_the_same_original_operation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory), initial=True)
            self.assertEqual(cp['phase'], 'public')
            result = self.invoke(root, recovery.name, 'resume', old, installer,
                                 public_result={'status': 'applied', 'recovery_ref': cp['upstream_ref']})
            self.assertEqual(result['exit_id'], 'tools_upgraded')
            after = json.loads((recovery / 'checkpoint.json').read_text())
            self.assertEqual({key: after[key] for key in before}, before)
            self.assertEqual(after['phase'], 'complete')
            self.assertEqual(len(writes), 1)

    def test_resume_retry_preserves_pending_stage_and_original_action(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory), pending=True)
            result = self.invoke(root, recovery.name, 'resume', old, installer,
                                 target_error=OSError('target check unavailable'))
            self.assertEqual(result, {'exit_id': 'frozen_recovery_required', 'profile': 'recover_frozen_source',
                                     'action': 'resume', 'recovery_ref': recovery.name})
            after = json.loads((recovery / 'checkpoint.json').read_text())
            self.assertEqual(after['phase'], 'preset')
            self.assertEqual({key: after[key] for key in before}, before)
            self.assertEqual(self.invoke(root, recovery.name, 'resume', old, installer)['exit_id'], 'tools_upgraded')

    def test_complete_recovery_validates_without_running_the_installer_again(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory))
            result = self.invoke(root, recovery.name, 'resume', old, installer)
            self.assertEqual(result['exit_id'], 'tools_upgraded')
            self.assertEqual(len(writes), 1)
            self.assertEqual(json.loads((recovery / 'checkpoint.json').read_text())['preimages'], before['preimages'])

    def test_rollback_retry_keeps_rollback_action_and_restores_only_original_preimages(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory))
            result = self.invoke(root, recovery.name, 'rollback', old, installer, native_error=ValueError('native temporarily unavailable'))
            self.assertEqual(result, {'exit_id': 'frozen_recovery_required', 'profile': 'recover_frozen_source',
                                     'action': 'rollback', 'recovery_ref': recovery.name})
            self.assertEqual((root / 'asset').read_text(), 'original tool')
            result = self.invoke(root, recovery.name, 'rollback', old, installer)
            self.assertEqual(result, {'exit_id': 'rolled_back', 'installed_version': 'old-guru'})
            after = json.loads((recovery / 'checkpoint.json').read_text())
            self.assertEqual({key: after[key] for key in before}, before)
            self.assertEqual(after['phase'], 'rolled_back')
            self.assertEqual(len(writes), 1)

    def test_owned_edit_still_blocks_without_refreshing_preimages(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory))
            (root / 'asset').write_text('later legitimate edit')
            result = self.invoke(root, recovery.name, 'resume', old, installer)
            self.assertEqual(result, {'exit_id': 'blocked', 'reason': 'owned_tools_changed_since_operation'})
            after = json.loads((recovery / 'checkpoint.json').read_text())
            self.assertEqual(after['preimages'], before['preimages'])
            self.assertEqual((root / 'asset').read_text(), 'later legitimate edit')

    def test_public_wrapper_rejects_a_changed_original_asset_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root, recovery, cp, old, installer, writes, before = self.fixture(Path(directory))
            path = self.source / 'trellis/guru-team-extension.json'
            original = path.read_bytes()
            try:
                path.write_bytes(original + b'\n')
                public = {'profile': 'recover_frozen_source', 'action': 'resume', 'recovery_ref': recovery.name}
                proc = subprocess.run(['bash', str(PACKAGE / 'scripts/invoke.sh'), '--root', str(root),
                                       '--input', json.dumps(public)], cwd=SOURCE, capture_output=True, text=True,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(json.loads(proc.stdout), {'exit_id': 'blocked',
                    'reason': 'Tools recovery source identity or canonical content changed'})
            finally:
                path.write_bytes(original)
            self.assertEqual(json.loads((recovery / 'checkpoint.json').read_text())['preimages'], before['preimages'])

    def test_legacy_helper_dependencies_come_from_the_selected_asset_source(self):
        current = owner.legacy_owner(PACKAGE)
        original = owner.legacy_owner(self.asset_package)
        self.assertEqual(Path(original.state.__code__.co_filename).resolve(),
                         (self.source / 'trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/files.py').resolve())
        self.assertNotEqual(original.state.__code__.co_filename, current.state.__code__.co_filename)
