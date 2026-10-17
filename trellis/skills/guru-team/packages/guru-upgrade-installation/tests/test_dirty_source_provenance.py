"""Dirty receipts retain exact historical per-path evidence, never implicit HEAD."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE/'runtime'))
from owner import MigrationError, legacy_source_commits, old_paths


class DirtySourceProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)/'source'; self.source.mkdir()
        self.target = Path(self.temp.name)/'target'; self.target.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Fixture'); self.git('config', 'user.email', 'fixture@example.invalid')
        self.extension = self.source/'trellis/guru-team-extension.json'; self.extension.parent.mkdir()
        self.extension.write_text(json.dumps({'version':'0.7.0-guru.3','target_trellis_cli':'0.7.0-castbox.3'}))
        self.ref = '.trellis/guru-team/scripts/bash/check-env.sh'
        self.canonical = self.source/'trellis/workflows/guru-team/scripts/bash/check-env.sh'
        self.canonical.parent.mkdir(parents=True); self.canonical.write_bytes(b'original source bytes\n')
        self.git('add','.'); self.git('commit','-qm','recorded source')
        self.recorded = self.git('rev-parse','HEAD')
        selected = self.target/self.ref; selected.parent.mkdir(parents=True)
        selected.write_bytes(self.canonical.read_bytes())
        self.digest = hashlib.sha256(selected.read_bytes()).hexdigest()
        # HEAD has the desired metadata but different asset bytes. It must not
        # replace the receipt's selected historical source.
        self.extension.write_text(json.dumps({'version':'0.7.0-guru.4','target_trellis_cli':'0.7.0-castbox.4'}))
        self.canonical.write_bytes(b'later source bytes\n')
        self.git('add','.'); self.git('commit','-qm','later source')
        self.manifest = {'source':{'commit':self.recorded,'tree_state':'dirty'},
                         'extension':{'version':'0.7.0-guru.4','target_trellis_cli':'0.7.0-castbox.4'},
                         'install':{'managed_assets':[self.ref],'managed_asset_hashes':{}}}

    def git(self, *args):
        return subprocess.check_output(['git',*args], cwd=self.source, text=True, stderr=subprocess.DEVNULL).strip()

    def test_dirty_recorded_source_supplies_only_matching_per_path_bytes(self):
        self.assertEqual(legacy_source_commits(self.manifest,self.source),[self.recorded])
        self.assertEqual(old_paths(self.manifest,self.source,self.target),{self.ref:self.digest})
        selected=self.target/self.ref; selected.write_bytes(b'ordinary later local change\n')
        self.assertEqual(old_paths(self.manifest,self.source,self.target),{self.ref:self.digest})
        self.assertEqual(selected.read_bytes(),b'ordinary later local change\n')
        # The original inventory still sees a different current preimage and
        # requires an explicit preserve/replace decision before retirement.
        self.assertNotEqual(hashlib.sha256(selected.read_bytes()).hexdigest(),self.digest)

    def test_clean_metadata_mismatch_does_not_use_later_head(self):
        self.manifest['source']['tree_state']='clean'
        with self.assertRaisesRegex(MigrationError,'exact installed release/source objects'):
            old_paths(self.manifest,self.source,self.target)

    def test_missing_recorded_object_remains_a_concrete_source_prerequisite(self):
        self.manifest['source']['commit']='f'*40
        with self.assertRaisesRegex(MigrationError,'exact installed release/source objects'):
            old_paths(self.manifest,self.source,self.target)


if __name__ == '__main__': unittest.main()
