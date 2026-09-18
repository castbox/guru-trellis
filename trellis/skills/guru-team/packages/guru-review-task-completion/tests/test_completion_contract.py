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
CLOSURE_PACKAGE = PACKAGE.parent / "guru-complete-task-closure"

def _facts():
    public = {
        "profile": "completion",
        "mode": "standalone",
        "task_ref": ".trellis/tasks/demo",
        "authority_refs": ["requirements:current", "design:current"],
        "delivery_facts": [
            {"delivery_cycle_ref": "delivery:a", "merge_commit_sha": "a" * 40},
            {"delivery_cycle_ref": "delivery:b", "merge_commit_sha": "b" * 40},
        ],
        "evidence_refs": ["tests:ok", "deployment:ok"],
    }
    semantic = {
        "profile": "completion",
        "mode": "standalone",
        "authority_refs": list(public["authority_refs"]),
        "delivery_refs": [item["delivery_cycle_ref"] for item in public["delivery_facts"]],
        "evidence_refs": list(public["evidence_refs"]),
        "remaining_work_refs": [],
        "route": {"typed_exit": "completed"},
    }
    return public, semantic

def _invoke(tmp_path, public, semantic):
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    command = [
        sys.executable,
        str(PACKAGE / "runtime/invoke.py"),
        "--root",
        str(tmp_path),
        "--input",
        str(input_path),
        "--semantic-result",
        str(semantic_path),
    ]
    return subprocess.run(command, text=True, capture_output=True, env=env)

def test_contract_assets():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    assert [item["id"] for item in interface["external_exits"]] == ["remaining_work", "evidence_pending", "additional_delivery_required", "requirements_revision_required", "implementation_revision_required", "completed", "blocked"]
    for group in ("artifacts", "schemas"):
        for item in interface[group]: assert (PACKAGE / item["path"]).is_file()
    completed = next(item for item in interface["public_contracts"]["outputs"] if item["exit_id"] == "completed")
    assert completed["schema"]["path"] == "schemas/public-completed-output.schema.json"
    closure = next(item for item in interface["public_contracts"]["consumer_inputs"] if item["id"] == "closure")
    contract = closure["contract"]
    assert contract["kind"] == "skill_input_authoring_seed"
    assert contract["interface_path"] == "packages/guru-complete-task-closure/interface.json"
    assert contract["input_kind"] == "structured_json"
    assert contract["profile_id"] == "completion_approved"
    assert contract["seed_fields"] == ["source_exit", "task_ref", "completion_ref"]
    assert contract["authoring_fields"] == ["profile", "mode", "source_issue"]

    profiles = {item["id"]: item for item in interface["public_contracts"]["input"]["profiles"]}
    assert profiles["completion"]["example"]["path"] == "examples/public-input.json"
    assert profiles["evidence_refresh"]["example"]["path"] == "examples/public-evidence-refresh-input.json"

@pytest.mark.parametrize(
    "semantic_field",
    ["delivery_refs", "authority_refs", "evidence_refs"],
)
def test_completed_requires_every_declared_fact(tmp_path, semantic_field):
    public, semantic = _facts()
    semantic[semantic_field] = semantic[semantic_field][:-1]
    failed = _invoke(tmp_path, public, semantic)
    assert failed.returncode == 3
    assert json.loads(failed.stderr)["field_path"] == semantic_field

@pytest.mark.parametrize(
    ("public_field", "semantic_field"),
    [
        ("delivery_facts", "delivery_refs"),
        ("authority_refs", "authority_refs"),
        ("evidence_refs", "evidence_refs"),
    ],
)
def test_completed_rejects_empty_fact_groups(tmp_path, public_field, semantic_field):
    public, semantic = _facts()
    public[public_field] = []
    semantic[semantic_field] = []
    failed = _invoke(tmp_path, public, semantic)
    assert failed.returncode == 3
    assert json.loads(failed.stderr)["field_path"] == semantic_field

@pytest.mark.parametrize(
    "semantic_field",
    ["delivery_refs", "authority_refs", "evidence_refs"],
)
def test_completed_rejects_unbound_semantic_facts(tmp_path, semantic_field):
    public, semantic = _facts()
    semantic[semantic_field].append("unexpected:stale")
    failed = _invoke(tmp_path, public, semantic)
    assert failed.returncode == 3
    assert json.loads(failed.stderr)["field_path"] == semantic_field

def test_completed_projects_valid_closure_input(tmp_path):
    public, semantic = _facts()
    passed = _invoke(tmp_path, public, semantic)
    assert passed.returncode == 0, passed.stderr
    output = json.loads(passed.stdout)
    validate_json(output, PACKAGE / "schemas/public-completed-output.schema.json", "completed")
    interface = json.loads((PACKAGE / "interface.json").read_text())
    consumer = next(item for item in interface["public_contracts"]["consumer_inputs"] if item["id"] == "closure")
    projection = next(item for item in interface["public_contracts"]["projections"] if item["consumer_input_id"] == "closure")
    closure_input = json.loads((PACKAGE / consumer["contract"]["authoring_example"]["path"]).read_text())
    closure_input.update({mapping["target"]: output[mapping["source"]] for mapping in projection["mappings"]})
    assert set(mapping["target"] for mapping in projection["mappings"]) == set(consumer["contract"]["seed_fields"])
    validate_json(closure_input, CLOSURE_PACKAGE / "schemas/public-input.schema.json", "closure_input")
