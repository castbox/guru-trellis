import sys
import unittest
from unittest.mock import patch
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parent / "guru-create-delivery/tests"))
from support import installed_fixture, owner_module


class ActivationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = installed_fixture(self)
        self.key = self.fixture.create()
        self.directory = self.fixture.projection.planning_directory(self.key)
        for filename in ("prd.md", "design.md", "implement.md"):
            (self.directory / filename).write_text("Reviewed " + filename + "\n")
        self.module = owner_module(PACKAGE)
        self.public = {"profile": "delivery_activation", "mode": "workflow", "task_ref": self.fixture.task_ref,
                       "delivery_key": self.key, "planning_result_id": self.module.planning_identity(self.fixture.root, self.directory), "action": "activate"}
        self.owner = {"typed_exit": "delivery_started", "reason": "Current reviewed plan ready for its legal accepted Planning transition."}

    def invoke(self, public=None):
        return self.module.invoke(PACKAGE, self.fixture.root, public or self.public, self.owner)

    def test_activation_and_output_recovery_keep_public_result_distinct_from_token(self):
        first = self.invoke()
        self.assertEqual(first["exit_id"], "delivery_started")
        recovered = self.invoke({**self.public, "action": "recover_activation"})
        self.assertEqual(first, recovered)
        self.assertNotEqual(first["planning_accepted_result_id"], self.public["planning_result_id"])
        delivery = self.fixture.projection.resolve(self.key)
        self.assertEqual(delivery["phase"], "implementing")
        self.assertEqual(delivery["results"]["planning"]["result_id"], first["planning_accepted_result_id"])
        self.assertNotIn(self.public["planning_result_id"], str(delivery))

    def test_plan_change_returns_approval_without_mutation(self):
        (self.directory / "implement.md").write_text("Changed validation plan\n")
        output = self.invoke()
        self.assertEqual(output["exit_id"], "planning_refresh_required")
        self.assertEqual(self.fixture.projection.resolve(self.key)["phase"], "planning")
        self.assertIsNone(self.fixture.projection.resolve(self.key)["results"]["planning"])

    def test_output_loss_recovery_retires_original_pending_operation(self):
        from runtime.task_lifecycle.errors import LifecycleContractError
        original = self.module.DeliveryProjection.apply

        def lost_stdout(projection, operation):
            original(projection, operation)
            raise LifecycleContractError("output_lost", "stdout", "Recover the actual public result.")

        with patch.object(self.module.DeliveryProjection, "apply", lost_stdout):
            self.assertEqual(self.invoke()["exit_id"], "blocked")
        pending = self.fixture.root / ".trellis/.runtime/guru-team/delivery-activation" / (self.key["delivery_id"] + ".json")
        self.assertTrue(pending.is_file())
        actual = self.fixture.projection.resolve(self.key)["results"]["planning"]["result_id"]
        recovered = self.invoke({**self.public, "action": "recover_activation"})
        self.assertEqual(recovered["planning_accepted_result_id"], actual)
        self.assertFalse(pending.exists())

    def test_unapplied_pending_operation_does_not_block_fresh_replanning(self):
        from runtime.task_lifecycle.errors import LifecycleContractError
        with patch.object(self.module.DeliveryProjection, "apply", side_effect=LifecycleContractError(
                "upstream_temporarily_unavailable", "operation", "Retry the same operation.")):
            self.assertEqual(self.invoke()["exit_id"], "blocked")
        pending = self.fixture.root / ".trellis/.runtime/guru-team/delivery-activation" / (self.key["delivery_id"] + ".json")
        self.assertTrue(pending.is_file())
        (self.directory / "design.md").write_text("Freshly reviewed revised plan\n")
        fresh = {**self.public, "planning_result_id": self.module.planning_identity(self.fixture.root, self.directory)}
        self.assertEqual(self.invoke(fresh)["exit_id"], "planning_refresh_required")
        self.assertFalse(pending.exists())
        self.assertEqual(self.invoke(fresh)["exit_id"], "delivery_started")

    def test_same_delivery_rework_preserves_candidate_then_records_new_planning_result(self):
        first = self.invoke()
        (self.fixture.root / "candidate.txt").write_text("existing candidate\n")
        candidate = self.fixture.projection.candidate(["candidate.txt"], kind="git_free")
        self.fixture.projection.begin_check(self.key, candidate)
        self.fixture.projection.apply({"api_version": "1.0", "operation": "rework", "key": self.key,
            "owner_role": "check", "owner_id": "guru-check-task", "expected_phase": "checking", "target_role": "planning",
            "reason": self.fixture.scope, "affected_results": ["planning", "check", "full_review", "readiness"]})
        (self.directory / "design.md").write_text("Revised same Delivery design\n")
        fresh = {**self.public, "planning_result_id": self.module.planning_identity(self.fixture.root, self.directory)}
        second = self.invoke(fresh)
        self.assertEqual(second["delivery_key"], self.key)
        self.assertNotEqual(second["planning_accepted_result_id"], first["planning_accepted_result_id"])
        self.assertEqual(self.fixture.projection.resolve(self.key)["candidate"], candidate)

    def test_planning_scope_withdrawal_releases_selection_and_recovers_same_result(self):
        public = {"profile": "delivery_scope_withdrawal", "mode": "workflow",
                  "task_ref": self.fixture.task_ref, "delivery_key": self.key}
        semantic = {"reviewed_delivery_key": self.key, "result_id": "planning-withdrawal:one",
                    "reason": self.fixture.scope, "scope_decision": self.fixture.scope,
                    "evidence": [self.fixture.scope]}
        first = self.module.invoke(PACKAGE, self.fixture.root, public, semantic)
        recovered = self.module.invoke(PACKAGE, self.fixture.root, public, semantic)
        self.assertEqual(first, recovered)
        self.assertEqual(first["exit_id"], "delivery_stopped")
        delivery = self.fixture.projection.resolve(self.key)
        self.assertEqual(delivery["phase"], "stopped")
        self.assertEqual(delivery["stop_result"]["result_id"], semantic["result_id"])
        self.assertIsNone(delivery["results"]["planning"])
        self.assertIsNone(delivery["results"]["readiness"])
        self.assertNotEqual(self.fixture.projection.current().get("status"), "selected")
        self.assertTrue((self.directory / "design.md").is_file())


if __name__ == "__main__":
    unittest.main()
