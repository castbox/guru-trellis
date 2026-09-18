from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publish_owner", PACKAGE / "runtime/owner.py")
assert SPEC and SPEC.loader
OWNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OWNER)


TASK = ".trellis/tasks/current"
HEAD = "b" * 40
CYCLE = "delivery-cycle:v1:" + "a" * 64
BODY = "## Summary\n\nRefs #435\n"


def source_input() -> dict:
    return {"profile":"review_ready","mode":"workflow","task_ref":TASK,"delivery_cycle_ref":CYCLE,"reviewed_head":HEAD,"pr_title":"Delivery title","pr_body":BODY,"remaining_work_state":"remaining"}


def pr(*, draft: bool = True, title: str = "Delivery title", body: str = BODY) -> dict:
    return {"number":435,"url":"https://github.com/castbox/guru-trellis/pull/435","state":"OPEN","is_draft":draft,"title":title,"body":body,"head_branch":"codex/435","head_sha":HEAD,"base_branch":"main","head_owner":"castbox"}


def transaction(stage: str = "bind_pr") -> dict:
    value = {"schema_version":"1.0","skill_id":OWNER.SKILL_ID,"transaction_ref":"c"*64,"stage":stage,"input":source_input(),"repo_ref":"castbox/guru-trellis","base_branch":"main","head_branch":"codex/435","reviewed_head":HEAD,"initial_remote_head":None,"candidate_pr":None,"bound_pr":None,"decisions":{"push_required":True,"create_pr_required":True,"metadata":None,"ready":None}}
    return value


class TransactionTests(unittest.TestCase):
    def test_closing_keyword_is_rejected_but_refs_is_allowed(self) -> None:
        OWNER.validate_public_input(source_input())
        invalid = source_input()
        invalid["pr_body"] = "Fixes #435"
        with self.assertRaises(OWNER.WorkflowError):
            OWNER.validate_public_input(invalid)

    def test_review_ready_rejects_values_outside_closed_schema(self) -> None:
        for field, value in (
            ("delivery_cycle_ref", "not-a-cycle"),
            ("remaining_work_state", "completed"),
        ):
            with self.subTest(field=field):
                invalid = source_input()
                invalid[field] = value
                with self.assertRaises(OWNER.WorkflowError) as raised:
                    OWNER.validate_public_input(invalid)
                self.assertEqual(raised.exception.code, "schema_mismatch")

    def test_equal_head_unbound_bind_recovery_does_not_create_pr(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = transaction()
            equal = pr(draft=True)
            with mock.patch.object(OWNER, "find_bindable_pr", return_value=equal), mock.patch.object(OWNER, "save_transaction") as save, mock.patch.object(OWNER, "_run") as run:
                OWNER.bind_pr(root, state)
            run.assert_not_called()
            self.assertEqual(state["bound_pr"]["number"], 435)
            self.assertEqual(state["stage"], "converge_metadata")
            self.assertTrue(state["decisions"]["ready"]["mutation_required"])
            save.assert_called_once()

    def test_first_pr_is_created_once_then_bound_before_later_mutation(self) -> None:
        state = transaction()
        created = pr(draft=True)
        completed = mock.Mock(returncode=0, stdout=created["url"], stderr="")
        with mock.patch.object(OWNER, "find_bindable_pr", side_effect=[None, created]), mock.patch.object(OWNER, "save_transaction") as save, mock.patch.object(OWNER, "_run", return_value=completed) as run:
            OWNER.bind_pr(Path("/repo"), state)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[1][0:3], ["gh", "pr", "create"])
        self.assertEqual(state["bound_pr"]["number"], 435)
        self.assertEqual(state["stage"], "converge_metadata")
        self.assertGreaterEqual(save.call_count, 2)

    def test_metadata_output_loss_accepts_exact_postimage_without_second_edit(self) -> None:
        state = transaction("converge_metadata")
        state["bound_pr"] = {"number":435,"url":"https://github.com/castbox/guru-trellis/pull/435","head_sha":HEAD}
        state["decisions"]["metadata"] = {"original_title":"Old","original_body_sha256":OWNER.hashlib.sha256(b"Old").hexdigest(),"title_matches":False,"body_matches":False,"mutation_required":True}
        with mock.patch.object(OWNER, "read_pr", side_effect=[pr(title="Old", body="Old"), pr()]), mock.patch.object(OWNER, "_run") as run, mock.patch.object(OWNER, "save_transaction"):
            OWNER.converge_metadata(Path("/repo"), state)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(state["stage"], "mark_ready")
        with mock.patch.object(OWNER, "read_pr", return_value=pr()), mock.patch.object(OWNER, "_run") as retry_run, mock.patch.object(OWNER, "save_transaction"):
            state["stage"] = "converge_metadata"
            OWNER.converge_metadata(Path("/repo"), state)
        retry_run.assert_not_called()

    def test_ready_output_loss_rematerializes_without_mutation(self) -> None:
        state = transaction("ready")
        state["bound_pr"] = {"number":435,"url":"https://github.com/castbox/guru-trellis/pull/435","head_sha":HEAD}
        with mock.patch.object(OWNER, "read_pr", return_value=pr(draft=False)), mock.patch.object(OWNER, "_run") as run:
            first = OWNER.ready_output(Path("/repo"), state)
            second = OWNER.ready_output(Path("/repo"), state)
        run.assert_not_called()
        self.assertEqual(first, second)
        self.assertEqual(first["exit_id"], "ready_for_merge")
        self.assertEqual(set(first), {"exit_id","task_ref","delivery_cycle_ref","repo_ref","pr_number","expected_head_sha","publication_body_sha256"})

    def test_ready_retry_does_not_repeat_mutation(self) -> None:
        state = transaction("mark_ready")
        state["bound_pr"] = {"number":435,"url":"https://github.com/castbox/guru-trellis/pull/435","head_sha":HEAD}
        state["decisions"]["ready"] = {"original_is_draft":True,"mutation_required":True}
        with mock.patch.object(OWNER, "read_pr", return_value=pr(draft=False)), mock.patch.object(OWNER, "_run") as run, mock.patch.object(OWNER, "save_transaction"):
            OWNER.mark_ready(Path("/repo"), state)
        run.assert_not_called()
        self.assertEqual(state["stage"], "ready")

    def test_reprepare_selects_only_active_cycle_when_old_cycle_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old = transaction("ready")
            old["transaction_ref"] = "d" * 64
            old["input"]["delivery_cycle_ref"] = "delivery-cycle:v1:" + "d" * 64
            current = transaction("bind_pr")
            OWNER.save_transaction(root, old)
            OWNER.save_transaction(root, current)
            reprepare = {
                "profile": "reprepare_publication",
                "mode": "workflow",
                "task_ref": TASK,
                "reason_code": "private_state_invalid",
            }
            with mock.patch.object(
                OWNER,
                "task_context",
                return_value=(root / TASK, {"branch":"codex/435","base_branch":"main"}),
            ), mock.patch.object(
                OWNER, "git_text", return_value=HEAD
            ), mock.patch.object(
                OWNER, "repository_identity", return_value="castbox/guru-trellis"
            ), mock.patch.object(
                OWNER, "remote_head", return_value=None
            ), mock.patch.object(
                OWNER, "list_open_prs", return_value=[]
            ):
                plan = OWNER.plan_from_input(root, reprepare)
        self.assertEqual(plan["typed_exit"], "preview")
        self.assertEqual(plan["transaction_ref"], current["transaction_ref"])
        self.assertEqual(plan["input"]["delivery_cycle_ref"], CYCLE)

    def test_invoke_maps_plan_stage_recovery_errors_to_progressing_exits(self) -> None:
        review = {
            "schema_version": "1.0",
            "skill_id": OWNER.SKILL_ID,
            "review": {"status": "passed", "summary": "Current publication plan is reviewed."},
            "route": {"typed_exit": "ready_for_merge"},
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review_path = root / "review.json"
            review_path.write_text(json.dumps(review))
            profiles = (
                {"profile":"same_plan_resume","mode":"workflow","task_ref":TASK,"transaction_ref":"c"*64},
                {"profile":"reprepare_publication","mode":"workflow","task_ref":TASK,"reason_code":"private_state_invalid"},
            )
            for public_input in profiles:
                input_path = root / f"{public_input['profile']}.json"
                input_path.write_text(json.dumps(public_input))
                for code in OWNER.REPREPARE_REQUIRED_CODES:
                    with self.subTest(profile=public_input["profile"], code=code), mock.patch.object(
                        OWNER,
                        "plan_from_input",
                        side_effect=OWNER.WorkflowError("plan failed", code=code),
                    ):
                        output = OWNER.invoke(root, str(input_path), str(review_path), None)
                    if code in {"private_state_invalid", "private_state_missing"}:
                        self.assertEqual(
                            output,
                            {"exit_id": "review_stale", "task_ref": TASK, "stale_reason": code},
                        )
                    else:
                        self.assertEqual(
                            output,
                            {"exit_id": "reprepare_required", "task_ref": TASK, "reason_code": code},
                        )

    def test_missing_transaction_returns_to_delivery_review(self) -> None:
        review = {
            "schema_version": "1.0",
            "skill_id": OWNER.SKILL_ID,
            "review": {"status": "passed", "summary": "Current publication plan is reviewed."},
            "route": {"typed_exit": "ready_for_merge"},
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "reprepare.json"
            review_path = root / "review.json"
            input_path.write_text(json.dumps({
                "profile": "reprepare_publication",
                "mode": "workflow",
                "task_ref": TASK,
                "reason_code": "private_state_missing",
            }))
            review_path.write_text(json.dumps(review))
            output = OWNER.invoke(root, str(input_path), str(review_path), None)
        self.assertEqual(
            output,
            {"exit_id": "review_stale", "task_ref": TASK, "stale_reason": "private_state_invalid"},
        )


if __name__ == "__main__":
    unittest.main()
