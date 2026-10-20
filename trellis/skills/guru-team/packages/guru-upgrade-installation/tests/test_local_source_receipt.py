"""Recover normal local-clone receipts from caller-selected Git objects."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
from owner import MigrationError, installer, old_manifest, old_paths


class LocalSourceReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.origin = self.base / "old-origin"
        self.origin.mkdir()
        self.git(self.origin, "init", "-q", "-b", "main")
        self.git(self.origin, "config", "user.name", "Fixture")
        self.git(self.origin, "config", "user.email", "fixture@example.invalid")
        self.extension_path = "trellis/guru-team-extension.json"
        self.metadata = {"version": "0.7.0-guru.4", "target_trellis_cli": "0.7.0-castbox.4"}
        extension = self.origin / self.extension_path
        extension.parent.mkdir(parents=True)
        extension.write_text(json.dumps(self.metadata))
        self.source_path = "trellis/workflows/guru-team/scripts/bash/check-env.sh"
        original = self.origin / self.source_path
        original.parent.mkdir(parents=True)
        original.write_bytes(b"recorded original bytes\n")
        self.git(self.origin, "add", ".")
        self.git(self.origin, "commit", "-qm", "old installed source")
        self.source = self.base / "selected-source"
        self.git(self.base, "clone", "-q", str(self.origin), str(self.source))
        self.git(self.source, "config", "user.name", "Fixture")
        self.git(self.source, "config", "user.email", "fixture@example.invalid")
        canonical = next(parent for parent in PACKAGE.parents if (parent / "trellis/presets").is_dir())
        self.producer = installer(canonical)
        self.provenance = self.producer.source_provenance(self.source)
        self.target = self.base / "target"
        self.target.mkdir()
        self.asset = ".trellis/guru-team/scripts/bash/check-env.sh"
        path = self.target / self.asset
        path.parent.mkdir(parents=True)
        path.write_bytes(original.read_bytes())
        self.old_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        self.receipt = self.target / ".trellis/guru-team/extension.json"
        self.write_receipt()
        self.git(self.target, "init", "-q", "-b", "main")
        self.receipt_before = self.receipt.read_bytes()
        shutil.rmtree(self.origin)

    def git(self, root, *args):
        return subprocess.check_output(["git", *args], cwd=root, text=True,
                                       stderr=subprocess.DEVNULL).strip()

    def write_receipt(self, metadata=None, provenance=None):
        self.receipt.write_text(json.dumps({
            "schema_version": "2.0", "extension": metadata or self.metadata,
            "source": provenance or self.provenance,
            "install": {"managed_assets": [self.asset], "managed_asset_hashes": {}},
        }))

    def advance_source(self):
        (self.source / self.source_path).write_bytes(b"later source bytes\n")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "-qm", "later same-version source")
        self.git(self.source, "tag", "v0.7.0-guru.4")

    def test_deleted_origin_recovers_exact_old_bytes_not_head_or_tag(self):
        self.assertEqual(self.provenance["tree_state"], "clean")
        self.assertEqual(self.provenance["repo"], str(self.origin))
        self.advance_source()
        manifest = old_manifest(self.target, self.source)
        self.assertEqual(old_paths(manifest, self.source, self.target), {self.asset: self.old_hash})
        # A normal local edit matching later source is still not the old preimage.
        (self.target / self.asset).write_bytes(b"later source bytes\n")
        self.assertEqual(old_paths(manifest, self.source, self.target), {self.asset: self.old_hash})
        self.assertEqual(self.receipt.read_bytes(), self.receipt_before)

    def test_shallow_source_missing_recorded_object_stops_before_writes(self):
        self.advance_source()
        shallow = self.base / "shallow-source"
        self.git(self.base, "clone", "-q", "--depth", "1", self.source.as_uri(), str(shallow))
        self.assertEqual(self.git(shallow, "tag", "--list"), "v0.7.0-guru.4")
        before = (self.target / self.asset).read_bytes()
        with self.assertRaisesRegex(MigrationError, "exact installed release/source objects"):
            old_manifest(self.target, shallow)
        self.assertEqual((self.target / self.asset).read_bytes(), before)
        self.assertEqual(self.receipt.read_bytes(), self.receipt_before)

    def test_clean_metadata_mismatch_stops_before_writes(self):
        self.write_receipt({**self.metadata, "version": "0.7.0-guru.3"})
        before = self.receipt.read_bytes()
        with self.assertRaisesRegex(MigrationError, "exact installed release/source objects"):
            old_manifest(self.target, self.source)
        self.assertEqual(self.receipt.read_bytes(), before)
        self.assertEqual(hashlib.sha256((self.target / self.asset).read_bytes()).hexdigest(), self.old_hash)

    def test_dirty_local_receipt_retains_per_path_source_semantics(self):
        metadata = {**self.metadata, "version": "0.7.0-guru.5"}
        (self.source / self.extension_path).write_text(json.dumps(metadata))
        provenance = self.producer.source_provenance(self.source)
        self.assertEqual(provenance["tree_state"], "dirty")
        self.write_receipt(metadata, provenance)
        before = self.receipt.read_bytes()
        manifest = old_manifest(self.target, self.source)
        self.assertEqual(old_paths(manifest, self.source, self.target), {self.asset: self.old_hash})
        self.assertEqual(self.receipt.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
