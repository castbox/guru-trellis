from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
