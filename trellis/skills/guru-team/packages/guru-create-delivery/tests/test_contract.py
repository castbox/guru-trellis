import json
import unittest
from pathlib import Path
from unittest.mock import patch

from support import installed_fixture, owner_module
from runtime.delivery_projection.gates import record_gate


class CreationTests(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).resolve().parents[1]
        self.fixture = installed_fixture(self)
        self.module = owner_module(self.package)
        self.public = {"profile": "delivery_creation", "mode": "workflow", "task_ref": self.fixture.task_ref,
                       "task_key": {"task_id": "projection-task", "lifecycle_generation": 0},
                       "scope_ref": {"authority": self.fixture.scope, "anchors": ["验收"]},
                       "delivery_profile": "pull_request", "continuation_id": "d1", "action": "create"}
        self.owner = {"typed_exit": "created", "reason": "Reviewed independent slice with overall scope retained."}

    def invoke(self, public=None):
        return self.module.invoke(self.package, self.fixture.root, public or self.public, self.owner)

    def test_creation_and_lost_stdout_keep_identity(self):
        first = self.invoke()
        self.assertEqual(first["exit_id"], "created")
        recovered = self.invoke({**self.public, "action": "recover_creation"})
        self.assertEqual(first, recovered)
        self.assertEqual(len(self.fixture.projection.read_record()["deliveries"]), 1)
        self.assertFalse(self.module.checkpoint(self.fixture.root, self.fixture.task_ref, "d1").exists())

    def test_select_same_identity_then_new_delivery_preserves_original_plan(self):
        first = self.invoke()
        directory = self.fixture.projection.planning_directory(first["delivery_key"])
        (directory / "design.md").write_text("D1 unique plan\n")
        selected = self.invoke({"profile": "delivery_selection", "mode": "workflow", "task_ref": self.fixture.task_ref, "delivery_key": first["delivery_key"]})
        self.assertEqual(selected, first)
        self.fixture.stop(first["delivery_key"])
        second = self.invoke({**self.public, "continuation_id": "d2"})
        self.assertNotEqual(first["delivery_key"], second["delivery_key"])
        self.assertEqual((directory / "design.md").read_text(), "D1 unique plan\n")
        self.assertNotIn("status", self.fixture.projection.read_record())

    def test_selection_and_creation_recovery_preserve_each_active_phase(self):
        """Exercise real public transitions; semantic routing is native evidence."""
        created = self.invoke()
        key = created["delivery_key"]
        projection = self.fixture.projection
        implementation = self.fixture.root / "implementation.txt"
        implementation.write_text("Existing implementation survives selection.\n")

        def select_and_recover(phase):
            before = projection.resolve(key)
            selected = self.invoke({"profile": "delivery_selection", "mode": "workflow",
                                    "task_ref": self.fixture.task_ref, "delivery_key": key})
            recovered = self.invoke({**self.public, "action": "recover_creation"})
            self.assertEqual(selected, created)
            self.assertEqual(recovered, created)
            self.assertEqual(projection.current()["key"], key)
            self.assertEqual(projection.resolve(key), before)
            self.assertEqual(before["phase"], phase)
            self.assertEqual(len(projection.read_record()["deliveries"]), 1)
            self.assertEqual(implementation.read_text(), "Existing implementation survives selection.\n")

        select_and_recover("planning")
        self.fixture.planning(key)
        select_and_recover("implementing")
        projection.begin_check(key, projection.candidate(["implementation.txt"], kind="git_free"))
        select_and_recover("checking")
        record_gate(projection, key, "check", "check:selected", "passed", [self.fixture.scope], [])
        select_and_recover("reviewing")
        record_gate(projection, key, "full_review", "review:selected", "passed", [self.fixture.scope], [])
        record_gate(projection, key, "readiness", "ready:selected", "ready", [self.fixture.scope], [])
        select_and_recover("publishing")

    def test_unsupported_profile_is_rejected_before_pending_write(self):
        failed = self.invoke({**self.public, "delivery_profile": "local_commit"})
        self.assertEqual(failed, {"exit_id": "blocked", "reason_code": "unsupported_delivery_profile"})
        self.assertEqual(self.fixture.projection.read_record()["deliveries"], [])
        self.assertFalse(self.module.checkpoint(self.fixture.root, self.fixture.task_ref, "d1").exists())

    def test_original_unsupported_pending_is_retired_only_by_creation_owner(self):
        # Execute the exact previous owner against the real installed API;
        # never fabricate a checkpoint or public state to reproduce the failure.
        previous = owner_module(self.package, "../tests/fixtures/creation-before-profile-preflight.py")
        failed = previous.invoke(self.package, self.fixture.root,
                                 {**self.public, "delivery_profile": "local_commit"}, self.owner)
        self.assertEqual(failed["exit_id"], "blocked")
        pending = self.module.checkpoint(self.fixture.root, self.fixture.task_ref, "d1")
        self.assertTrue(pending.is_file())
        self.assertEqual(self.fixture.projection.read_record()["deliveries"], [])
        corrected = self.invoke()
        self.assertEqual(corrected["exit_id"], "created")
        self.assertEqual(len(self.fixture.projection.read_record()["deliveries"]), 1)
        self.assertFalse(pending.is_file())

    def test_existing_public_delivery_retains_original_pending_and_profile(self):
        # An ordinary official session write interruption leaves a real
        # created identity. Context absence now has its own valid explicit route.
        with patch.object(self.fixture.projection.api.delivery_session, 'select_delivery',
                          side_effect=OSError('ordinary session write interruption')):
            self.assertEqual(self.invoke()["exit_id"], "blocked")
        pending = self.module.checkpoint(self.fixture.root, self.fixture.task_ref, "d1")
        before = pending.read_bytes()
        rejected = self.invoke({**self.public, "delivery_profile": "local_commit"})
        self.assertEqual(rejected["exit_id"], "blocked")
        self.assertEqual(pending.read_bytes(), before)
        self.assertEqual(len(self.fixture.projection.read_record()["deliveries"]), 1)
        self.assertEqual(self.invoke({**self.public, "action": "recover_creation"})["exit_id"], "created")

    def test_selection_missing_after_create_recovers_original_uuid(self):
        with patch.object(self.fixture.projection.api.delivery_session, 'select_delivery',
                          side_effect=OSError('ordinary session write interruption')):
            failed = self.invoke()
        self.assertEqual(failed["exit_id"], "blocked")
        records = self.fixture.projection.read_record()["deliveries"]
        self.assertEqual(len(records), 1)
        recovered = self.invoke({**self.public, "action": "recover_creation"})
        self.assertEqual(recovered["delivery_key"]["delivery_id"], records[0]["id"])
        self.assertEqual(len(self.fixture.projection.read_record()["deliveries"]), 1)


if __name__ == "__main__":
    unittest.main()
