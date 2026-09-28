"""Current task Delivery-to-Finish graph and legacy terminal isolation."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[4]
MODE = os.environ.get("GURU_FINISH_INTEGRATION_MODE", "source")
if MODE not in {"source", "installed"}:
    raise RuntimeError("GURU_FINISH_INTEGRATION_MODE must be source or installed")
ROOT = Path(os.environ.get("GURU_FINISH_INTEGRATION_ROOT", str(SOURCE))).resolve()
SKILLS = ROOT / (".trellis/guru-team/skills" if MODE == "installed" else "trellis/skills/guru-team")
RUNTIME_ROOT = ROOT / (".trellis/guru-team" if MODE == "installed" else "trellis/skills/guru-team")
WORKFLOW = ROOT / (".trellis/workflow.md" if MODE == "installed" else "trellis/workflows/guru-team/workflow.md")
RETIRED = {
    "guru-create-task-workspace", "guru-review-task-publication", "guru-finalize-task",
    "guru-merge-task-pr", "guru-restore-archived-task",
}
ROUTES = {
    ("guru-review-branch", "passed"): ("skill", "guru-review-task-delivery"),
    ("guru-review-task-delivery", "ready"): ("skill", "guru-publish-task-delivery"),
    ("guru-publish-task-delivery", "ready_for_merge"): ("skill", "guru-merge-task-delivery"),
    ("guru-merge-task-delivery", "delivered"): ("skill", "guru-review-task-completion"),
    ("guru-review-task-completion", "remaining_work"): ("workflow", "active-task-continuation"),
    ("guru-review-task-completion", "additional_delivery_required"): ("workflow", "task-delivery-planning-router"),
    ("guru-review-task-completion", "completed"): ("skill", "guru-complete-task-closure"),
    ("guru-complete-task-closure", "closed"): ("skill", "guru-finish-task"),
    ("guru-complete-task-closure", "no_mutation"): ("skill", "guru-finish-task"),
    ("guru-finish-task", "success"): ("skill", "guru-cleanup-task-resources"),
    ("guru-cleanup-task-resources", "cleaned"): ("stop", "task-cleanup-complete"),
    ("guru-reactivate-task", "reactivated_to_planning"): ("workflow", "task-planning-router"),
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markers(kind: str) -> list[dict]:
    return [json.loads(value) for value in re.findall(
        rf"<!-- guru-{kind}: (\{{.*?\}}) -->", WORKFLOW.read_text(encoding="utf-8")
    )]


class CurrentFinishGraphTests(unittest.TestCase):
    def test_reactivated_validation_only_completion_to_closure_and_finish(self) -> None:
        completion = SKILLS / "packages/guru-review-task-completion"
        closure = SKILLS / "packages/guru-complete-task-closure"
        finish = SKILLS / "packages/guru-finish-task"
        public = read_json(completion / "examples/public-reactivation-validation-input.json")
        semantic = read_json(completion / "examples/reactivation-semantic-result.json")
        self.assertNotIn("merge_result", public)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            task = root / public["task_artifact"]["task_ref"]
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({
                "id": "example-task", "status": "in_progress", "lifecycle_generation": 1,
                "source": {"kind": "no_issue"},
            }))

            def run(package: Path, name: str, authored: dict, review: dict) -> dict:
                input_path = root / f"{name}-input.json"
                review_path = root / f"{name}-review.json"
                input_path.write_text(json.dumps(authored))
                review_path.write_text(json.dumps(review))
                result = subprocess.run([
                    sys.executable, str(package / "runtime/invoke.py"), "--root", str(root),
                    "--input", str(input_path), "--semantic-result", str(review_path),
                ], capture_output=True, text=True, check=False,
                    env={**os.environ, "PYTHONPATH": str(RUNTIME_ROOT), "PYTHONDONTWRITEBYTECODE": "1"})
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)

            completed = run(completion, "completion", public, semantic)
            self.assertEqual(completed["exit_id"], "completed")
            self.assertEqual(completed["result_ref"]["lifecycle_generation"], 1)
            closure_input = read_json(completion / "examples/closure-authoring.json")
            closure_input.update({"source_exit": completed["exit_id"], "completion_result": completed["result_ref"],
                                  "source": {"kind": "no_issue"}, "action_set": [],
                                  "binding_ref": {"task_id": "example-task", "lifecycle_generation": 1,
                                                  "binding_epoch": 0, "binding_revision": 0},
                                  "evidence_slots": {"completion": completed["result_ref"]["result_id"]}})
            closure_review = read_json(closure / "examples/semantic-result.json")
            closure_review["reviewed_action_set"] = []
            closed = run(closure, "closure", closure_input, closure_review)
            self.assertEqual(closed["exit_id"], "no_mutation")
            self.assertEqual(closed["result_ref"]["lifecycle_generation"], 1)
            sys.path.insert(0, str(RUNTIME_ROOT))
            from runtime.schema import validate_json
            validate_json({"profile": "closure_completed", "mode": "workflow", "closure_result": closed["result_ref"]},
                          finish / "schemas/public-input.schema.json", "finish")

    def test_old_generation_merge_cannot_enter_reactivated_completion_chain(self) -> None:
        completion = SKILLS / "packages/guru-review-task-completion"
        authored = read_json(completion / "examples/public-reactivation-validation-input.json")
        reviewed = read_json(completion / "examples/reactivation-semantic-result.json")
        authored.pop("reactivation_anchor")
        authored["merge_result"] = read_json(completion / "examples/public-input.json")["merge_result"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "completion-input.json"
            review_path = root / "completion-review.json"
            input_path.write_text(json.dumps(authored))
            review_path.write_text(json.dumps(reviewed))
            result = subprocess.run([
                sys.executable, str(completion / "runtime/invoke.py"), "--root", str(root),
                "--input", str(input_path), "--semantic-result", str(review_path),
            ], capture_output=True, text=True, check=False,
                env={**os.environ, "PYTHONPATH": str(RUNTIME_ROOT), "PYTHONDONTWRITEBYTECODE": "1"})
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stderr)["code"], "schema_mismatch")
            self.assertFalse((root / ".git").exists())

    def test_every_active_exit_has_one_matching_marker_and_consumer(self) -> None:
        active = {
            item["id"] for item in read_json(SKILLS / "registry.json")["skills"]
            if item["state"] == "active"
            and item.get("workflow_integration_state", "integrated") == "integrated"
            and item["id"] != "guru-verify-extension-installation"
        }
        self.assertFalse(active & RETIRED)
        invokes = markers("skill-invoke")
        exits = markers("skill-exit")
        self.assertEqual(len(invokes), len(active))
        self.assertEqual({item["skill"] for item in invokes}, active)
        expected = {}
        for skill_id in active:
            interface = read_json(SKILLS / "packages" / skill_id / "interface.json")
            for exit_contract in interface["external_exits"]:
                expected[(skill_id, exit_contract["id"])] = exit_contract["consumer"]
        self.assertEqual(len(exits), len(expected))
        self.assertEqual(
            {(item["skill"], item["exit"]): item["consumer"] for item in exits},
            expected,
        )
        targets = {
            (kind, item["id"])
            for kind in ("workflow", "stop") for item in markers(f"{kind}-target")
        }
        self.assertEqual(targets, {
            (consumer["kind"], consumer["id"])
            for consumer in expected.values() if consumer["kind"] in {"workflow", "stop"}
        })
        for key, (kind, target) in ROUTES.items():
            self.assertEqual(expected[key], {"kind": kind, "id": target})

    def test_current_public_wrappers_load_and_retired_packages_are_absent(self) -> None:
        for skill_id in {key[0] for key in ROUTES}:
            with self.subTest(skill=skill_id):
                interface = read_json(SKILLS / "packages" / skill_id / "interface.json")
                wrapper = SKILLS / "packages" / skill_id / interface["public_contracts"]["invocation"]["wrapper"]
                result = subprocess.run(
                    [str(wrapper), "--help"], cwd=ROOT, capture_output=True, text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
        for skill_id in RETIRED:
            self.assertFalse(any(
                path.is_file() and path.suffix not in {".pyc", ".pyo"} and "__pycache__" not in path.parts
                for path in (SKILLS / "packages" / skill_id).rglob("*")
            ))

    def test_legacy_terminal_state_cannot_enter_current_graph(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("archived_review_passed", text)
        self.assertIn("legacy-archived-review-disposition-required", text)
        self.assertIn("pinned compatible old version or per-case manual disposition", text)
        self.assertIn(
            "Prove one TaskId, source, accepted scope and terminal Git identity",
            " ".join(text.split()),
        )
        for item in markers("skill-exit"):
            self.assertNotIn(item["skill"], RETIRED)
            self.assertNotIn(item["consumer"].get("id"), RETIRED)

    def test_no_task_breadcrumb_preserves_identity_boundary(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        state = text.split("[workflow-state:no_task]", 1)[1].split("[/workflow-state:no_task]", 1)[0]
        for phrase in (
            "Every file-changing request first resolves task identity",
            "Unrelated `in_progress` tasks",
            "A checkout path alone does not bind its task identity",
            "current repository and TaskId must be validated",
            "An unfinished task for the same Issue must resolve to its existing identity",
            "no relevant active task, archived incomplete-closeout identity, or normally finished original-task Reactivate candidate",
            "discover relevant normally finished archives by source Issue or explicit original TaskId",
            "old Finalizer residue is not a normally completed archive",
        ):
            self.assertIn(phrase, " ".join(state.split()))


if __name__ == "__main__":
    unittest.main()
