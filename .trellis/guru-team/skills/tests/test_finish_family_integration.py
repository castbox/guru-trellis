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
    def delivery_fixture(self):
        import importlib.util
        path=SKILLS/'packages/guru-check-task/tests/test_delivery_flow.py'
        # Test tooling may be taken from canonical while every package call below
        # is redirected to the selected installed runtime.
        if not path.is_file(): path=SOURCE/'trellis/skills/guru-team/packages/guru-check-task/tests/test_delivery_flow.py'
        spec=importlib.util.spec_from_file_location('finish_public_delivery_fixture',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.SKILLS=SKILLS;module.PACKAGE=SKILLS/'packages/guru-check-task'
        fixture=module.DeliveryFlow();fixture.setUp();self.addCleanup(fixture.doCleanups)
        return fixture

    def test_reactivated_validation_only_completion_to_closure_and_finish(self) -> None:
        fixture=self.delivery_fixture()
        fixture.test_no_mutation_closure_records_public_result_and_recovers()
        projection=fixture.projection;scope=projection.read_record()['accepted_scope']
        projection.apply({'api_version':'1.0','operation':'reopen_task','key':{'task_id':'flow-task','lifecycle_generation':0},'owner_role':'task_scope','owner_id':'guru-test-task_scope','authority':scope})
        self.assertEqual(1,projection.read_record()['lifecycle_generation'])
        self.assertFalse(any(row['lifecycle_generation']==1 for row in projection.read_record()['deliveries']))
        public={'profile':'delivery_reactivation_validation','mode':'workflow','task_ref':fixture.task_ref,'task_key':{'task_id':'flow-task','lifecycle_generation':1},'reactivation_anchor':{'task_id':'flow-task','archived_generation':0,'archive_ref':'.trellis/tasks/archive/2026-10/flow-task','archive_head':fixture.head}}
        semantic={'profile':public['profile'],'mode':public['mode'],'reviewed_task_key':public['task_key'],'reviewed_scope':scope,'reviewed_delivery_result_ids':['delivery:flow'],'evidence':[scope],'remaining_work_refs':[],'result_id':'completion:revalidated','route':{'typed_exit':'completed'}}
        completed=fixture.wrapper('guru-review-task-completion','invoke.sh','--input',fixture.write('revalidated.json',public),'--semantic-result',fixture.write('revalidated-owner.json',semantic))
        self.assertEqual('completed',completed['exit_id']);self.assertEqual(1,completed['result_ref']['lifecycle_generation'])
        closure_input=read_json(SKILLS/'packages/guru-review-task-completion/examples/closure-authoring.json')
        closure_input.update(source_exit='completed',completion_result=completed['result_ref'],source={'kind':'no_issue'},action_set=[],binding_ref={'task_id':'flow-task','lifecycle_generation':1,'binding_revision':0},evidence_slots={'completion':completed['result_ref']['result_id']},content_head=fixture.head)
        closure_review=read_json(SKILLS/'packages/guru-complete-task-closure/examples/semantic-result.json');closure_review['reviewed_action_set']=[]
        closed=fixture.wrapper('guru-complete-task-closure','invoke.sh','--input',fixture.write('revalidated-closure.json',closure_input),'--semantic-result',fixture.write('revalidated-closure-owner.json',closure_review))
        self.assertEqual('no_mutation',closed['exit_id']);self.assertEqual(1,closed['result_ref']['lifecycle_generation'])
        sys.path.insert(0,str(RUNTIME_ROOT))
        from runtime.schema import validate_json
        validate_json({'profile':'closure_completed','mode':'workflow','closure_result':closed['result_ref']},SKILLS/'packages/guru-finish-task/schemas/public-input.schema.json','finish')
        self.assertNotIn('status',projection.read_record())

    def test_old_generation_cannot_enter_reactivated_completion_chain(self) -> None:
        fixture=self.delivery_fixture()
        fixture.test_no_mutation_closure_records_public_result_and_recovers()
        projection=fixture.projection;scope=projection.read_record()['accepted_scope']
        projection.apply({'api_version':'1.0','operation':'reopen_task','key':{'task_id':'flow-task','lifecycle_generation':0},'owner_role':'task_scope','owner_id':'guru-test-task_scope','authority':scope})
        public={'profile':'delivery_completion','mode':'workflow','task_ref':fixture.task_ref,'task_key':{'task_id':'flow-task','lifecycle_generation':0}}
        semantic={'profile':public['profile'],'mode':'workflow','reviewed_task_key':public['task_key'],'reviewed_scope':scope,'reviewed_delivery_result_ids':['delivery:flow'],'evidence':[scope],'remaining_work_refs':[],'result_id':'completion:old','route':{'typed_exit':'completed'}}
        result=fixture.wrapper('guru-review-task-completion','invoke.sh','--input',fixture.write('old.json',public),'--semantic-result',fixture.write('old-owner.json',semantic),success=False)
        self.assertEqual('stale_identity',result['code'])
        self.assertEqual(1,len(projection.read_record()['completion_results']))

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
            "Every change-intent request first resolves task identity",
            "Unrelated active tasks",
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
