import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.task_lifecycle.closure_result import read_terminal_closure_result
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import inspect_repository


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def fixture():
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    semantic = json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    return public, semantic


def fake_gh(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    script = bin_dir / "gh"
    script.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "log = pathlib.Path(os.environ['GH_LOG'])\n"
        "with log.open('a') as stream: stream.write(' '.join(args) + '\\n')\n"
        "state = pathlib.Path(os.environ['GH_STATE'])\n"
        "states = json.loads(state.read_text())\n"
        "key = args[args.index('--repo') + 1] + '#' + args[2]\n"
        "if args[1] == 'view': print(states[key])\n"
        "elif args[1] == 'close':\n"
        "    if key == os.environ.get('GH_FAIL_ISSUE'): sys.exit(1)\n"
        "    states[key] = 'CLOSED'; state.write_text(json.dumps(states))\n"
    )
    script.chmod(0o755)
    state = tmp_path / "states.json"
    state.write_text(json.dumps({"castbox/guru-trellis#436": "OPEN", "castbox/guru-trellis#437": "OPEN"}))
    env = {**os.environ, "PYTHONPATH": str(ROOT), "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
           "GH_LOG": str(tmp_path / "gh.log"), "GH_STATE": str(state)}
    return env, state, tmp_path / "gh.log"


def invoke(tmp_path, public, semantic, env, confirmed=False):
    if not (tmp_path / ".git").exists():
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    inp = tmp_path / "input.json"
    review = tmp_path / "semantic.json"
    inp.write_text(json.dumps(public))
    review.write_text(json.dumps(semantic))
    argv = [sys.executable, str(PACKAGE / "runtime/invoke.py"), "--root", str(tmp_path),
            "--input", str(inp), "--semantic-result", str(review)]
    if confirmed:
        argv.append("--confirmed-close")
    return subprocess.run(argv, text=True, capture_output=True, env=env)


def test_contract_assets():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    assert [item["id"] for item in interface["external_exits"]] == [
        "no_mutation", "closed", "resume_closure", "external_change_conflict", "blocked",
    ]
    for group in ("artifacts", "schemas"):
        for item in interface[group]:
            assert (PACKAGE / item["path"]).is_file()
    for output in interface["public_contracts"]["outputs"]:
        value = json.loads((PACKAGE / output["example"]["path"]).read_text())
        validate_json(value, PACKAGE / output["schema"]["path"], output["exit_id"])
        validate_json(value, PACKAGE / "schemas/public-output.schema.json", output["exit_id"])
    finish = next(item for item in interface["public_contracts"]["consumer_inputs"] if item["id"] == "finish")
    assert finish["contract"]["seed_fields"] == ["closure_result"]


def test_no_issue_no_mutation_never_calls_provider(tmp_path):
    public, semantic = fixture()
    public["source"] = {"kind": "no_issue"}
    public["action_set"] = []
    semantic["reviewed_action_set"] = []
    env, _, log = fake_gh(tmp_path)
    result = invoke(tmp_path, public, semantic, env)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["exit_id"] == "no_mutation"
    assert not log.exists()

    result_ref = json.loads(result.stdout)["result_ref"]
    snapshot = read_terminal_closure_result(inspect_repository(tmp_path), result_ref)
    assert snapshot == {"result_ref": result_ref, "terminal": "no_mutation", "action_set": []}
    with pytest.raises(LifecycleContractError, match="closure_result_stale"):
        read_terminal_closure_result(inspect_repository(tmp_path), {**result_ref, "result_id": "closure:other"})


def test_close_and_same_owner_output_loss_recovery(tmp_path):
    public, semantic = fixture()
    env, state, log = fake_gh(tmp_path)
    pending = invoke(tmp_path, public, semantic, env)
    assert pending.returncode == 0, pending.stderr
    pending_ref = json.loads(pending.stdout)["transaction_ref"]
    assert not log.exists()
    public["source_exit"] = "resume_closure"
    public["transaction_ref"] = pending_ref
    closed = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert closed.returncode == 0, closed.stderr
    assert json.loads(closed.stdout)["result_ref"]["result_id"] == pending_ref["result_id"]
    retry = invoke(tmp_path, public, semantic, env)
    assert retry.returncode == 0, retry.stderr
    assert json.loads(retry.stdout) == json.loads(closed.stdout)
    assert log.read_text().count("issue close 436") == 1
    assert json.loads(state.read_text())["castbox/guru-trellis#436"] == "CLOSED"


def test_partial_transaction_conflict_can_be_semantically_reentered(tmp_path):
    public, semantic = fixture()
    public["action_set"].append({"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 437}, "disposition": "close"})
    semantic["reviewed_action_set"] = copy.deepcopy(public["action_set"])
    env, state, log = fake_gh(tmp_path)
    pending = invoke(tmp_path, public, semantic, {**env, "GH_FAIL_ISSUE": "castbox/guru-trellis#437"}, confirmed=True)
    assert json.loads(pending.stdout)["exit_id"] == "resume_closure"
    state.write_text(json.dumps({"castbox/guru-trellis#436": "OPEN", "castbox/guru-trellis#437": "OPEN"}))
    public["source_exit"] = "resume_closure"
    public["transaction_ref"] = json.loads(pending.stdout)["transaction_ref"]
    conflict = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert json.loads(conflict.stdout)["exit_id"] == "external_change_conflict"
    public["source_exit"] = "external_change_conflict"
    public["transaction_ref"] = json.loads(conflict.stdout)["transaction_ref"]
    reviewed = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert reviewed.returncode == 0, reviewed.stderr
    assert json.loads(reviewed.stdout)["exit_id"] == "closed"
    assert log.read_text().count("issue close 436") == 2


def test_frozen_scope_binding_action_and_generation_conflict(tmp_path):
    public, semantic = fixture()
    env, _, log = fake_gh(tmp_path)
    assert invoke(tmp_path, public, semantic, env, confirmed=True).returncode == 0
    for field, value in [
        ("accepted_scope_identity", "scope:changed"),
        ("binding_ref", {**public["binding_ref"], "binding_revision": 1}),
        ("action_set", [{"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 436}, "disposition": "already_closed_at_review"}]),
        ("completion_result", {**public["completion_result"], "result_id": "completion:new"}),
        ("content_head", "b" * 40),
    ]:
        changed = copy.deepcopy(public)
        review = copy.deepcopy(semantic)
        changed[field] = value
        if field == "action_set":
            review["reviewed_action_set"] = value
        if field == "completion_result":
            changed["evidence_slots"]["completion"] = value["result_id"]
        conflict = invoke(tmp_path, changed, review, env, confirmed=True)
        assert conflict.returncode == 0, conflict.stderr
        assert json.loads(conflict.stdout)["exit_id"] == "external_change_conflict"
    assert log.read_text().count("issue close 436") == 1


def test_reopened_required_issue_semantic_reentry(tmp_path):
    public, semantic = fixture()
    env, state, log = fake_gh(tmp_path)
    assert invoke(tmp_path, public, semantic, env, confirmed=True).returncode == 0
    state.write_text(json.dumps({"castbox/guru-trellis#436": "OPEN"}))
    changed = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert changed.returncode == 0, changed.stderr
    output = json.loads(changed.stdout)
    assert output["exit_id"] == "external_change_conflict"
    assert output["reason"]["reason_code"] == "required_closed_issue_reopened"
    assert log.read_text().count("issue close 436") == 1
    public["source_exit"] = "external_change_conflict"
    public["transaction_ref"] = output["transaction_ref"]
    retried = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert retried.returncode == 0, retried.stderr
    assert json.loads(retried.stdout)["exit_id"] == "closed"
    assert json.loads(retried.stdout)["result_ref"]["result_id"] != output["transaction_ref"]["result_id"]
    assert log.read_text().count("issue close 436") == 2


def test_multi_issue_action_set_and_no_authority_item(tmp_path):
    public, semantic = fixture()
    public["action_set"].append({"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 437}, "disposition": "no_close_authority"})
    semantic["reviewed_action_set"] = copy.deepcopy(public["action_set"])
    env, _, log = fake_gh(tmp_path)
    result = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["exit_id"] == "closed"
    assert "437" not in log.read_text()


def test_partial_action_set_recovers_only_unfinished_issue(tmp_path):
    public, semantic = fixture()
    public["action_set"].append({"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 437}, "disposition": "close"})
    semantic["reviewed_action_set"] = copy.deepcopy(public["action_set"])
    env, _, log = fake_gh(tmp_path)
    first = invoke(tmp_path, public, semantic, {**env, "GH_FAIL_ISSUE": "castbox/guru-trellis#437"}, confirmed=True)
    assert first.returncode == 0, first.stderr
    pending = json.loads(first.stdout)
    assert pending["exit_id"] == "resume_closure"
    public["source_exit"] = "resume_closure"
    public["transaction_ref"] = pending["transaction_ref"]
    resumed = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert resumed.returncode == 0, resumed.stderr
    assert json.loads(resumed.stdout)["exit_id"] == "closed"
    assert log.read_text().count("issue close 436") == 1
    assert log.read_text().count("issue close 437") == 2


@pytest.mark.parametrize("field", ["source", "completion_result", "binding_ref", "action_set"])
def test_invalid_input_zero_mutation(tmp_path, field):
    public, semantic = fixture()
    public[field] = None
    env, _, log = fake_gh(tmp_path)
    failed = invoke(tmp_path, public, semantic, env, confirmed=True)
    assert failed.returncode != 0
    assert not log.exists()
