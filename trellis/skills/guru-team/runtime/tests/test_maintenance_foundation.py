"""Checkout isolation and public transport behavior, without business migration logic."""
from __future__ import annotations
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from runtime import bootstrap, base_selection, maintenance_transport as transport
from runtime.io import CommandError


class CheckoutIsolationTests(unittest.TestCase):
    def test_primary_and_linked_local_pointer_preserve_common_and_peer(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            peer = Path(temporary) / "peer"
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL, text=True).strip()
            root.mkdir()
            git("init", "-b", "main")
            git("-c", "user.name=Test", "-c", "user.email=t@example.invalid", "commit", "--allow-empty", "-m", "initial")
            git("worktree", "add", "-b", "dev", str(peer))
            common = bootstrap.active_pointer_path(root, for_write=True)
            common.parent.mkdir(parents=True)
            common.write_text("common-original")
            peer_gitdir = bootstrap.repository_git_dirs(peer)[0]
            peer_pointer = peer_gitdir / "guru-team/python/active.json"
            peer_pointer.parent.mkdir(parents=True)
            peer_pointer.write_text("peer-original")
            self.assertEqual(bootstrap.active_pointer_path(peer), peer_pointer)
            bootstrap.write_active(root, "a" * 24, checkout_local=True)
            self.assertEqual(common.read_text(), "common-original")
            self.assertEqual(bootstrap.active_pointer_path(root), root / ".trellis/.runtime/guru-team/python/active.json")
            self.assertEqual(bootstrap.active_pointer_path(peer), peer_pointer)
            bootstrap.write_active(peer, "b" * 24, checkout_local=True)
            self.assertEqual(peer_pointer.read_text(), "peer-original")
            self.assertEqual(common.read_text(), "common-original")
            self.assertEqual(json.loads(bootstrap.active_pointer_path(root).read_text())["runtime_id"], "a" * 24)
            self.assertEqual(json.loads(bootstrap.active_pointer_path(peer).read_text())["runtime_id"], "b" * 24)
            # Ordinary activation updates the effective checkout-local override.
            self.assertEqual(bootstrap.active_pointer_path(root, for_write=True), bootstrap.active_pointer_path(root))
            self.assertEqual(bootstrap.active_pointer_path(peer, for_write=True), bootstrap.active_pointer_path(peer))
            bootstrap.write_active(root, "c" * 24)
            self.assertEqual(json.loads(bootstrap.active_pointer_path(root).read_text())["runtime_id"], "c" * 24)
            self.assertEqual(json.loads(bootstrap.active_pointer_path(peer).read_text())["runtime_id"], "b" * 24)
            bootstrap.write_active(peer, "d" * 24)
            self.assertEqual(json.loads(bootstrap.active_pointer_path(peer).read_text())["runtime_id"], "d" * 24)
            self.assertEqual(common.read_text(), "common-original")
            self.assertEqual(peer_pointer.read_text(), "peer-original")
            # Dirty business work is not a readonly target-selection prohibition.
            (peer / "business.txt").write_text("uncommitted")
            selected = base_selection.select_base(root)
            self.assertEqual(selected["selected_base"], "dev")
            self.assertEqual(base_selection.authority_checkout(root, "dev"), peer.resolve())
            with self.assertRaises(CommandError):
                base_selection.authority_checkout(root, "dev", require_clean=True)
            git("worktree", "remove", "--force", str(peer))
            # Missing preferred checkout is a diagnostic, never downgrade to main.
            self.assertEqual(base_selection.select_base(root)["selected_base"], "dev")
            with self.assertRaises(CommandError):
                base_selection.authority_checkout(root, "dev")


class TransportTests(unittest.TestCase):
    def test_candidate_mismatch_prevents_operation(self):
        source = {"cli_package_root": ".", "dependency_mode": "local_candidate", "expected_candidate": {}}
        contract = {"maintenance_api": "1.0", "cli_version": "v", "core_version": "v", "operation_kinds": ["tools_install", "task_conversion", "legacy_closeout"]}
        with mock.patch.object(transport, "_invoke", return_value={"contract": contract, "core_package_root": "."}) as invoke, mock.patch.object(transport, "package_digest", return_value="bytes"):
            with self.assertRaises(CommandError) as error:
                transport.call(source, "applyMaintenance", {"plan": {}, "state_dir": "unused"})
            self.assertEqual(error.exception.code, "candidate_mismatch")
            self.assertEqual(invoke.call_count, 1)

    def test_apply_preserves_frozen_plan_and_recovery_arguments(self):
        source = {"cli_package_root": "."}
        payload = {"plan": {"operation_id": "original"}, "state_dir": "/tmp/owner-state"}
        with mock.patch.object(transport, "inspect_source", return_value={"cli_package_root": "."}), mock.patch.object(transport, "_invoke", return_value={"status": "applied"}) as invoke:
            self.assertEqual(transport.call(source, "applyMaintenance", payload), {"status": "applied"})
            invoke.assert_called_once_with(".", "applyMaintenance", payload)

if __name__ == "__main__":
    unittest.main()
