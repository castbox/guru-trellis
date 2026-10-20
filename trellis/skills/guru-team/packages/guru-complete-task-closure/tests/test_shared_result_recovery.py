"""Public Closure production and recovery across independent Git common dirs."""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from .test_closure_contract import PACKAGE, ROOT, fake_gh, fixture, invoke
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.schema import validate_json
from runtime.task_lifecycle.closure_result import closure_carrier_path, read_terminal_closure_result
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository


def producer(tmp_path, variant="close"):
    root = tmp_path / "source"
    root.mkdir()
    public, semantic = fixture()
    if variant == "no_issue":
        public["source"], public["action_set"] = {"kind": "no_issue"}, []
    elif variant == "reference":
        public["source"]["disposition"] = "reference_only"
        public["action_set"][0]["disposition"] = "no_close_authority"
    else:
        public["action_set"][0]["disposition"] = "retain_open" if variant in {"retain", "mixed"} else variant
        if variant == "mixed":
            public["action_set"].append({"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 437}, "disposition": "close"})
    semantic["reviewed_action_set"] = copy.deepcopy(public["action_set"])
    env, states, log = fake_gh(root)
    if variant == "already_closed_at_review":
        states.write_text(json.dumps({"castbox/guru-trellis#436": "CLOSED", "castbox/guru-trellis#437": "OPEN"}))
    return root, public, semantic, env, states, log


def clone_public(root, target):
    subprocess.run(["git", "add", ".trellis"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.com", "commit", "-qm", "Persist public Closure input"], cwd=root, check=True)
    subprocess.run(["git", "clone", "-q", str(root), str(target)], check=True)
    assert inspect_repository(root).common_dir != inspect_repository(target).common_dir
    assert not (inspect_repository(target).common_dir / "guru-team/closure").exists()
    return next((target / ".trellis/tasks").glob("*/task.json")).parent


def recovery_input(root, task, result):
    from runtime.delivery_projection.adapter import authority_ref
    return {"profile": "closure_shared_result_recovery", "mode": "workflow",
            "task_ref": task.relative_to(root).as_posix(), "result_ref": result,
            "shared_result": authority_ref(task / closure_carrier_path(result), root)}


def recover(root, public, actions, env, *, blocked=None):
    inp, sem = root.parent / "recovery-input.json", root.parent / "recovery-semantic.json"
    inp.write_text(json.dumps(public))
    semantic = {"profile": public["profile"], "mode": public["mode"], "reviewed_action_set": actions,
                "route": {"typed_exit": "apply"}}
    if blocked:
        semantic["route"] = {"typed_exit": "blocked", "reason": blocked}
    sem.write_text(json.dumps(semantic))
    return subprocess.run(["bash", str(PACKAGE / "scripts/invoke.sh"), "--root", str(root),
                           "--input", str(inp), "--semantic-result", str(sem)], env=env, text=True, capture_output=True)


@pytest.mark.parametrize("variant", ["close", "already_closed_at_review", "retain", "mixed", "reference", "no_issue"])
def test_shared_public_result_survives_clone_without_private_state(tmp_path, variant):
    root, public, semantic, env, states, log = producer(tmp_path, variant)
    produced = invoke(root, public, semantic, env, confirmed=True, wrapper=True)
    assert produced.returncode == 0, produced.stdout + produced.stderr
    output = json.loads(produced.stdout)
    clone = tmp_path / "clone"
    task = clone_public(root, clone)
    snapshot = read_terminal_closure_result(inspect_repository(clone), output["result_ref"])
    assert snapshot["action_set"] == public["action_set"] and snapshot["source"] == public["source"]
    assert snapshot["terminal"] == output["exit_id"]
    validate_json(snapshot, ROOT / "packages/guru-finish-task/schemas/closure-result-snapshot.schema.json", "snapshot")
    before = log.read_text() if log.exists() else ""
    task_before = (task / "task.json").read_bytes()
    recovered = recover(clone, recovery_input(clone, task, output["result_ref"]), public["action_set"], env)
    assert recovered.returncode == 0, recovered.stdout + recovered.stderr
    assert json.loads(recovered.stdout) == output
    assert (task / "task.json").read_bytes() == task_before
    after = log.read_text() if log.exists() else ""
    assert after.count("issue close") == before.count("issue close")
    assert not (inspect_repository(clone).common_dir / "guru-team/closure").exists()
    if variant in {"no_issue", "reference"}:
        assert before == after == ""


def test_provider_success_with_missing_public_projection_restores_original_result_only(tmp_path, monkeypatch):
    root, public, semantic, env, _, log = producer(tmp_path)
    pending = invoke(root, public, semantic, env)
    assert json.loads(pending.stdout)["exit_id"] == "resume_closure"
    spec = importlib.util.spec_from_file_location("shared_closure_owner", PACKAGE / "runtime/invoke.py")
    owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
    original_apply = DeliveryProjection.apply
    original_state = owner._state
    def state_with_shared_input(checkout, issue):
        carrier = next((checkout / ".trellis/tasks").glob("*/closeout/closure/*.json"))
        payload = json.loads(carrier.read_text())
        assert payload["action_set"] == public["action_set"]
        assert set(payload) == {"schema_version", "result_ref", "completion_result_id", "source", "action_set"}
        return original_state(checkout, issue)
    def unavailable_projection(self, operation):
        if operation["operation"] == "close_task":
            raise LifecycleContractError("write_failed", "closure_result", "Public projection unavailable.")
        return original_apply(self, operation)
    with monkeypatch.context() as patch:
        for key, value in env.items():
            patch.setenv(key, value)
        patch.setattr(DeliveryProjection, "apply", unavailable_projection)
        patch.setattr(owner, "_state", state_with_shared_input)
        result = owner.run(PACKAGE, {}, ["--root", str(root), "--input", str(root / "input.json"),
                          "--semantic-result", str(root / "semantic.json"), "--confirmed-close"])
    assert result["exit_id"] == "resume_closure"
    result_ref = {key: result["transaction_ref"][key] for key in ("task_id", "lifecycle_generation", "result_id")}
    clone = tmp_path / "clone"; task = clone_public(root, clone)
    assert json.loads((task / "task.json").read_text())["closure_results"] == []
    with pytest.raises(LifecycleContractError, match="closure_result_stale"):
        read_terminal_closure_result(inspect_repository(clone), result_ref)
    restored = recover(clone, recovery_input(clone, task, result_ref), public["action_set"], env)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert json.loads(restored.stdout) == {"exit_id": "closed", "result_ref": result_ref}
    assert log.read_text().count("issue close") == 1
    assert read_terminal_closure_result(inspect_repository(clone), result_ref)["action_set"] == public["action_set"]
    assert not (inspect_repository(clone).common_dir / "guru-team/closure").exists()


@pytest.mark.parametrize("variant,required_state,reason", [
    ("close", "OPEN", "required_closed_issue_reopened"),
    ("retain", "CLOSED", "required_open_issue_closed"),
])
def test_recovery_returns_provider_drift_to_original_closure_without_close(tmp_path, variant, required_state, reason):
    root, public, semantic, env, states, log = producer(tmp_path, variant)
    produced = invoke(root, public, semantic, env, confirmed=True)
    output = json.loads(produced.stdout)
    clone = tmp_path / "clone"; task = clone_public(root, clone)
    observed = json.loads(states.read_text()); observed["castbox/guru-trellis#436"] = required_state
    states.write_text(json.dumps(observed))
    before = log.read_text().count("issue close")
    result = recover(clone, recovery_input(clone, task, output["result_ref"]), public["action_set"], env)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["reason"]["reason_code"] == reason
    assert log.read_text().count("issue close") == before


def test_blocked_shared_review_preserves_reason_without_provider_or_projection(tmp_path):
    root, public, semantic, env, _, log = producer(tmp_path, "retain")
    produced = invoke(root, public, semantic, env)
    output = json.loads(produced.stdout)
    clone = tmp_path / "clone"; task = clone_public(root, clone)
    before = log.read_bytes()
    reason = {"reason_code": "source_review_missing", "reason_refs": ["task:source"]}
    result = recover(clone, recovery_input(clone, task, output["result_ref"]), [], env, blocked=reason)
    assert json.loads(result.stdout) == {"exit_id": "blocked", "reason": reason}
    assert log.read_bytes() == before
