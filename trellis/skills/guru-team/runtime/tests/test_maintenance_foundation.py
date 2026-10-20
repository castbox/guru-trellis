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
    def source_and_contract(self):
        source = {"cli_package_root": ".", "dependency_mode": "local_candidate",
                  "expected_candidate": {"cli_version": "v", "core_version": "v",
                                         "cli_digest": "bytes", "core_digest": "bytes"}}
        contract = {"maintenance_api": "1.0", "cli_version": "v", "core_version": "v",
                    "operation_kinds": ["tools_install", "task_conversion", "legacy_closeout",
                                        "task_resume", "formal_archive_reactivation"],
                    "formal_archive_reactivation": {"task_families": ["schema1"],
                                                    "generation": "increment_once",
                                                    "original_archive": "read_only"}}
        return source, contract

    def test_candidate_mismatch_prevents_operation(self):
        source = {"cli_package_root": ".", "dependency_mode": "local_candidate", "expected_candidate": {}}
        contract = {"maintenance_api": "1.0", "cli_version": "v", "core_version": "v", "operation_kinds": ["tools_install", "task_conversion", "legacy_closeout"]}
        for method in ("applyMaintenance", "inspectFormalArchiveReactivation", "prepareFormalArchiveReactivation"):
            with self.subTest(method=method), mock.patch.object(transport, "_invoke", return_value={"contract": contract, "core_package_root": "."}) as invoke, mock.patch.object(transport, "package_digest", return_value="bytes"):
                with self.assertRaises(CommandError) as error:
                    transport.call(source, method, {"plan": {}, "state_dir": "unused"})
                self.assertEqual(error.exception.code, "candidate_mismatch")
                invoke.assert_called_once_with(Path(".").resolve(), "source")

    def test_formal_archive_methods_forward_original_input_and_result(self):
        source, contract = self.source_and_contract()
        payload = {"root": "/target", "key": {"task_id": "original", "lifecycle_generation": 0},
                   "task_ref": ".trellis/tasks/archive/original",
                   "archive": {"commit": "original-archive", "evidence": []}}
        for method, result in (("inspectFormalArchiveReactivation", {"successor": {"kind": "absent"}}),
                               ("prepareFormalArchiveReactivation", {"kind": "formal_archive_reactivation", "operation_id": "original"})):
            with self.subTest(method=method), mock.patch.object(transport, "_invoke", side_effect=[{"contract": contract, "core_package_root": "."}, result]) as invoke, mock.patch.object(transport, "package_digest", return_value="bytes"):
                self.assertIs(transport.call(source, method, payload), result)
                self.assertEqual(invoke.call_count, 2)
                self.assertEqual(invoke.call_args.args[:2], (str(Path(".").resolve()), method))
                self.assertIs(invoke.call_args.args[2], payload)

    def test_missing_formal_capability_prevents_sdk_call(self):
        for missing in ("operation", "capability", "task_families", "generation", "original_archive"):
            for method in ("inspectFormalArchiveReactivation", "prepareFormalArchiveReactivation"):
                source, contract = self.source_and_contract()
                if missing == "operation":
                    contract["operation_kinds"].remove("formal_archive_reactivation")
                elif missing == "capability":
                    del contract["formal_archive_reactivation"]
                else:
                    del contract["formal_archive_reactivation"][missing]
                with self.subTest(method=method, missing=missing), mock.patch.object(transport, "_invoke", return_value={"contract": contract, "core_package_root": "."}) as invoke, mock.patch.object(transport, "package_digest", return_value="bytes"):
                    with self.assertRaises(CommandError) as error:
                        transport.call(source, method, {"root": "/target"})
                    self.assertEqual(error.exception.code, "maintenance_prerequisite_missing")
                    invoke.assert_called_once_with(Path(".").resolve(), "source")

    def test_archive_resume_does_not_require_formal_reactivation_capability(self):
        source, contract = self.source_and_contract()
        contract["operation_kinds"].remove("formal_archive_reactivation")
        del contract["formal_archive_reactivation"]
        payload = {"key": {"task_id": "original", "lifecycle_generation": 0}}
        result = {"kind": "task_resume", "generation": 0}
        with mock.patch.object(transport, "_invoke", side_effect=[{"contract": contract, "core_package_root": "."}, result]) as invoke, mock.patch.object(transport, "package_digest", return_value="bytes"):
            self.assertIs(transport.call(source, "prepareArchivedTaskResume", payload), result)
            invoke.assert_called_with(str(Path(".").resolve()), "prepareArchivedTaskResume", payload)

    def test_apply_preserves_frozen_plan_and_recovery_arguments(self):
        source = {"cli_package_root": "."}
        payload = {"plan": {"operation_id": "original"}, "state_dir": "/tmp/owner-state"}
        with mock.patch.object(transport, "inspect_source", return_value={"cli_package_root": "."}), mock.patch.object(transport, "_invoke", return_value={"status": "applied"}) as invoke:
            self.assertEqual(transport.call(source, "applyMaintenance", payload), {"status": "applied"})
            invoke.assert_called_once_with(".", "applyMaintenance", payload)

if __name__ == "__main__":
    unittest.main()
