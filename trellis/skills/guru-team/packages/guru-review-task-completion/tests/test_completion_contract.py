import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
CLOSURE = PACKAGE.parent / "guru-complete-task-closure"


def fixture():
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    semantic = json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    return public, semantic


def invoke(tmp_path, public, semantic):
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    return subprocess.run(
        [sys.executable, str(PACKAGE / "runtime/invoke.py"), "--root", str(tmp_path),
         "--input", str(input_path), "--semantic-result", str(semantic_path)],
        text=True, capture_output=True, env=env,
    )


def test_contract_assets_and_projection(tmp_path):
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    assert len(interface["external_exits"]) == 7
    for group in ("artifacts", "schemas"):
        for item in interface[group]:
            assert (PACKAGE / item["path"]).is_file()
    for output in interface["public_contracts"]["outputs"]:
        value = json.loads((PACKAGE / output["example"]["path"]).read_text())
        validate_json(value, PACKAGE / output["schema"]["path"], output["exit_id"])
        validate_json(value, PACKAGE / "schemas/public-output.schema.json", output["exit_id"])
    public, semantic = fixture()
    result = invoke(tmp_path, public, semantic)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert set(output) == {"exit_id", "result_ref"}
    assert output["result_ref"]["task_id"] == public["task_artifact"]["task_id"]
    contract = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == "closure")["contract"]
    projection = next(row for row in interface["public_contracts"]["projections"] if row["id"] == "closure")
    assert contract["seed_fields"] == ["source_exit", "completion_result"]
    authored = json.loads((PACKAGE / contract["authoring_example"]["path"]).read_text())
    authored.update({row["target"]: output[row["source"]] for row in projection["mappings"]})
    authored["evidence_slots"]["completion"] = output["result_ref"]["result_id"]
    validate_json(authored, CLOSURE / "schemas/public-input.schema.json", "closure")


@pytest.mark.parametrize("lineage,slots", [
    ("closeout", ["planning", "task_commit_pair", "phase2_check", "branch_review", "closeout_publication"]),
    ("pre_cutover_recovered", ["planning", "restore", "merge_recovery"]),
])
def test_exact_closeout_and_recovery_lineage(tmp_path, lineage, slots):
    public, semantic = fixture()
    public["merge_result"] = {
        "task_id": "example-task", "lifecycle_generation": 0, "repo_ref": "castbox/guru-trellis",
        "pr_number": 2, "merge_commit_sha": "c" * 40, "merge_lineage": lineage, "result_id": "merge:current",
    }
    public["evidence_slots"] = {name: name + ":current" for name in slots}
    semantic["reviewed_evidence_slots"] = copy.deepcopy(public["evidence_slots"])
    result = invoke(tmp_path, public, semantic)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["exit_id"] == "completed"
    public["evidence_slots"]["delivery_review"] = "old:review"
    assert invoke(tmp_path, public, semantic).returncode == 3


@pytest.mark.parametrize("change", ["generation", "task_id", "locator", "scope", "merge", "evidence", "remaining"])
def test_stale_and_incomplete_facts_do_not_complete(tmp_path, change):
    public, semantic = fixture()
    if change == "generation":
        public["merge_result"]["lifecycle_generation"] = 1
    elif change == "task_id":
        public["merge_result"]["task_id"] = "other-task"
    elif change == "locator":
        public["merge_result"]["task_ref"] = ".trellis/tasks/other-task"
    elif change == "scope":
        semantic["reviewed_scope_identity"] = "scope:stale"
    elif change == "merge":
        semantic["reviewed_merge_result_id"] = "merge:stale"
    elif change == "evidence":
        semantic["reviewed_evidence_slots"]["planning"] = "plan:stale"
    else:
        semantic["remaining_work_refs"] = ["scope:unfinished"]
    result = invoke(tmp_path, public, semantic)
    assert result.returncode == 3
    assert json.loads(result.stderr)["code"] == "stale_identity"


@pytest.mark.parametrize("route", [
    "remaining_work", "evidence_pending", "additional_delivery_required",
    "requirements_revision_required", "implementation_revision_required", "blocked",
])
def test_noncomplete_routes_use_artifact_and_reason(tmp_path, route):
    public, semantic = fixture()
    semantic["route"] = {"typed_exit": route, "reason": {"reason_code": "work_pending", "reason_refs": ["scope:current"]}}
    semantic["remaining_work_refs"] = ["scope:current"]
    result = invoke(tmp_path, public, semantic)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["exit_id"] == route
    assert output["reason"] == semantic["route"]["reason"]
    assert ("task_artifact" in output) == (route != "blocked")
    assert "resume_target" not in output and "completion_ref" not in output
