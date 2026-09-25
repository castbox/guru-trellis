import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
sys.path.insert(0, str(PACKAGE / "runtime"))
from invoke import execute, source_transaction_path, transaction_path
import invoke


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, text=True, capture_output=True).stdout.strip()


def repository(tmp_path, *, old_branch="codex/demo-old", old_owner="caller_owned"):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / ".gitignore").write_text(".trellis/.runtime/\n")
    git(repo, "add", ".gitignore")
    git(repo, "commit", "-qm", "initial")
    archive = repo / ".trellis/tasks/archive/2026-09/09-19-demo"
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "lifecycle_generation": 2,
                                                  "source": {"kind": "no_issue"},
                                                  "completedAt": "2026-09-19", "worktree_path": "/old/machine/path"}))
    archive_ref = ".trellis/tasks/archive/2026-09/09-19-demo"
    (archive / "finish-summary.json").write_text(json.dumps({"schema_version": 2, "task": {
        "archive_dir": archive_ref, "status": "completed"}}))
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "archive")
    head = git(repo, "rev-parse", "HEAD")
    facts = inspect_repository(repo)
    key = TaskLifecycleKey("demo", 2)
    binding = BranchBindingStore(facts).establish(key, old_branch)
    ledger = ResourceLedgerStore(facts)
    ledger.establish_current(key, binding_epoch=binding.binding_epoch, binding_revision=0,
                             branch_name=old_branch, branch_ownership=old_owner, worktree_ownership="not_applicable")
    ledger.seal_for_finish(key, finish_result_id="finish:v1:1234567890abcdef", finish_head=head)
    finish_dir = repo / ".trellis/.runtime/guru-team/finish"
    finish_dir.mkdir(parents=True)
    (finish_dir / "1234567890abcdef.json").write_text(json.dumps({
        "schema_version": "2.0", "stage": "success", "task_ref": ".trellis/tasks/09-19-demo",
        "task_id": "demo", "closure_result_id": "closure:demo", "finish_ref": "finish:v1:1234567890abcdef",
        "lifecycle_generation": 2, "repo_ref": "castbox/guru-trellis", "base_branch": "main",
        "head_branch": old_branch, "expected_base_head": head, "archive_ref": archive_ref,
        "parent_head": head, "commit": head, "pr_number": 1,
        "pr_url": "https://github.com/castbox/guru-trellis/pull/1", "target_head": head,
    }))
    return repo, head


def inputs(repo, head, path, *, adopt=False, route="session_binding_recovery_required"):
    public = {"profile": "reactivate_completed_task", "mode": "standalone",
              "archived_lifecycle": {"task_id": "demo", "lifecycle_generation": 2}}
    acquisition = {"task_id": "demo", "task_ref": ".trellis/tasks/09-19-demo", "lifecycle_generation": 3,
                   "route": "adopt_invocation_checkout" if adopt else "provision_linked_worktree",
                   "branch_ref": "refs/heads/codex/demo-next", "decision_head": head,
                   "task_artifact_expectation": "absent", "transaction_id": "reactivate:demo:3", "result_id": "result:demo:3"}
    if adopt:
        acquisition["invocation_checkout"] = str(path)
    else:
        acquisition.update(target_path=str(path), provision_disposition="new_branch")
    semantic = {**public, "route": route, "reason_refs": ["new work"],
                "selected_base_ref": "refs/heads/main", "reviewed_base_head": head,
                "session_outcome": "recovery_required" if route == "session_binding_recovery_required" else "explicit_task_mode",
                "acquisition": acquisition}
    return public, semantic


def correction():
    return {
        "task_id": "demo", "task_ref": ".trellis/tasks/archive/2026-09/09-19-demo",
        "lifecycle_generation": 2, "current_source": {"kind": "no_issue"},
        "reviewed_source": {"kind": "issue", "repo_ref": "castbox/guru-trellis", "number": 454},
        "accepted_scope_identity": "scope:demo", "target_relation_id": "source:demo", "result_id": "correction:demo",
    }


def test_interface_and_examples_are_closed():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    exits = {row["id"] for row in interface["external_exits"]}
    assert exits == {"reactivated_to_planning", "session_binding_recovery_required", "resume_reactivation",
                     "source_correction_required", "reactivate_blocked"}
    for output in interface["public_contracts"]["outputs"]:
        payload = json.loads((PACKAGE / output["example"]["path"]).read_text())
        validate_json(payload, PACKAGE / output["schema"]["path"], output["exit_id"])
    for projection in interface["public_contracts"]["projections"]:
        output = next(row for row in interface["public_contracts"]["outputs"] if row["exit_id"] == projection["exit_id"])
        source = json.loads((PACKAGE / output["example"]["path"]).read_text())
        consumer = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
        payload = source if projection["operation"] == "direct" else {
            row["target"]: source[row["source"]] for row in projection["mappings"]
        }
        validate_json(payload, PACKAGE / consumer["contract"]["path"], projection["id"])


@pytest.mark.parametrize("adopt", [False, True])
def test_reactivate_acquires_checkout_and_recovers_exact_transaction(tmp_path, adopt):
    repo, head = repository(tmp_path)
    checkout = repo if adopt else tmp_path / "worktrees" / "new"
    if adopt:
        git(repo, "switch", "-qc", "codex/demo-next")
    public, semantic = inputs(repo, head, checkout, adopt=adopt)
    first = execute(repo, public, semantic, confirmed=True)
    assert first["exit_id"] == "session_binding_recovery_required"
    assert first["task_id"] == "demo" and first["lifecycle_generation"] == 3
    metadata_path = checkout / ".trellis/tasks/09-19-demo/task.json"
    before = metadata_path.read_bytes()
    metadata = json.loads(before)
    assert metadata["status"] == "planning" and "worktree_path" not in metadata
    repository_facts = inspect_repository(repo)
    key = TaskLifecycleKey("demo", 3)
    binding = BranchBindingStore(repository_facts).read(key)
    ledger = ResourceLedgerStore(repository_facts).read(key)
    assert binding is not None and binding.binding_revision == 0
    assert BranchBindingStore(repository_facts).read(TaskLifecycleKey("demo", 2)) is None
    assert ledger is not None and ledger.resources[0].ownership == ("caller_owned" if adopt else "guru_owned")
    transaction = transaction_path(repository_facts, TaskLifecycleKey("demo", 2))
    transaction_before = transaction.read_bytes()
    assert str(checkout) not in transaction_before.decode()
    assert execute(repo, public, semantic, confirmed=True) == first
    assert metadata_path.read_bytes() == before and transaction.read_bytes() == transaction_before
    semantic["route"] = "resume_reactivation"
    assert execute(repo, public, semantic, confirmed=False)["exit_id"] == "resume_reactivation"


def test_source_correction_applies_once_and_stale_generation_is_zero_write(tmp_path):
    repo, head = repository(tmp_path)
    public, semantic = inputs(repo, head, tmp_path / "worktrees" / "new")
    semantic.pop("acquisition")
    semantic.pop("session_outcome")
    semantic.pop("selected_base_ref")
    semantic.pop("reviewed_base_head")
    semantic["route"] = "source_correction_required"
    semantic["source_correction"] = correction()
    from runtime.io import CommandError
    with pytest.raises(CommandError, match="confirmation_required"):
        execute(repo, public, semantic, confirmed=False)
    metadata_path = repo / ".trellis/tasks/archive/2026-09/09-19-demo/task.json"
    assert json.loads(metadata_path.read_text())["source"] == {"kind": "no_issue"}
    result = execute(repo, public, semantic, confirmed=True)
    assert result["exit_id"] == "source_correction_required"
    corrected = metadata_path.read_bytes()
    assert json.loads(corrected)["source"] == semantic["source_correction"]["reviewed_source"]
    receipt = source_transaction_path(inspect_repository(repo), TaskLifecycleKey("demo", 2))
    assert receipt.is_file()
    assert execute(repo, public, semantic, confirmed=True) == result
    assert metadata_path.read_bytes() == corrected
    altered = json.loads(json.dumps(semantic))
    altered["source_correction"]["result_id"] = "correction:other"
    with pytest.raises(Exception, match="source_correction_stale"):
        execute(repo, public, altered, confirmed=True)
    assert (repo / ".trellis/tasks/archive/2026-09/09-19-demo").exists()
    public["archived_lifecycle"]["lifecycle_generation"] = 1
    semantic["archived_lifecycle"]["lifecycle_generation"] = 1
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="archived_lifecycle_stale"):
        execute(repo, public, semantic, confirmed=False)
    assert not transaction_path(inspect_repository(repo), TaskLifecycleKey("demo", 2)).exists()


def test_ready_source_correction_applied_in_activation_and_recovered(tmp_path):
    repo, head = repository(tmp_path)
    checkout = tmp_path / "worktrees" / "new"
    public, semantic = inputs(repo, head, checkout)
    semantic["source_correction"] = correction()
    first = execute(repo, public, semantic, confirmed=True)
    assert first["exit_id"] == "session_binding_recovery_required"
    task_path = checkout / ".trellis/tasks/09-19-demo/task.json"
    assert json.loads(task_path.read_text())["source"] == correction()["reviewed_source"]
    assert json.loads(transaction_path(inspect_repository(repo), TaskLifecycleKey("demo", 2)).read_text())[
        "source_correction_result_id"] == "correction:demo"
    assert execute(repo, public, semantic, confirmed=True) == first
    changed = json.loads(json.dumps(semantic))
    changed["source_correction"]["result_id"] = "correction:other"
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="reactivation_transaction_conflict"):
        execute(repo, public, changed, confirmed=True)


def test_invalid_session_route_does_not_acquire_checkout(tmp_path):
    repo, head = repository(tmp_path)
    target = tmp_path / "worktrees" / "new"
    public, semantic = inputs(repo, head, target, route="reactivated_to_planning")
    semantic["session_outcome"] = "recovery_required"
    result = execute(repo, public, semantic, confirmed=True)
    assert result["exit_id"] == "reactivate_blocked" and result["reason_code"] == "session_route_mismatch"
    assert not target.exists() and (repo / ".trellis/tasks/archive/2026-09/09-19-demo").is_dir()


def test_pending_guru_owned_old_branch_blocks_before_acquisition(tmp_path):
    repo, head = repository(tmp_path, old_branch="codex/demo-next", old_owner="guru_owned")
    target = tmp_path / "worktrees" / "new"
    public, semantic = inputs(repo, head, target)
    repository_facts = inspect_repository(repo)
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="branch_responsibility_pending"):
        execute(repo, public, semantic, confirmed=True)
    assert not target.exists()
    assert (repo / ".trellis/tasks/archive/2026-09/09-19-demo/task.json").is_file()
    assert BranchBindingStore(repository_facts).read(TaskLifecycleKey("demo", 3)) is None
    assert ResourceLedgerStore(repository_facts).read(TaskLifecycleKey("demo", 3)) is None


def test_resolved_old_branch_reuse_releases_only_old_binding(tmp_path):
    repo, head = repository(tmp_path, old_branch="codex/demo-next", old_owner="guru_owned")
    git(repo, "branch", "codex/demo-next", head)
    facts = inspect_repository(repo)
    key = TaskLifecycleKey("demo", 2)
    ledger_store = ResourceLedgerStore(facts)
    prior = ledger_store.read(key)
    assert prior is not None
    resolved = replace(prior, ledger_revision=prior.ledger_revision + 1,
                       resources=tuple(replace(row, state="resolved", responsibility_role="superseded")
                                       for row in prior.resources))
    ledger_store._write(resolved)
    public, semantic = inputs(repo, head, tmp_path / "worktrees" / "new")
    semantic["acquisition"]["provision_disposition"] = "existing_branch"
    result = execute(repo, public, semantic, confirmed=True)
    assert result["exit_id"] == "session_binding_recovery_required"
    bindings = BranchBindingStore(facts)
    assert bindings.read(key) is None
    assert bindings.read(TaskLifecycleKey("demo", 3)).branch_name == "codex/demo-next"
    assert ledger_store.read(key) == resolved
    assert ResourceLedgerStore(facts).read(TaskLifecycleKey("demo", 3)).resources[0].ownership == "caller_owned"


def test_caller_retained_old_branch_requires_resolved_incarnation(tmp_path):
    repo, head = repository(tmp_path, old_branch="codex/demo-next")
    git(repo, "branch", "codex/demo-next", head)
    key = TaskLifecycleKey("demo", 2)
    prior = ResourceLedgerStore(inspect_repository(repo)).read(key)
    assert prior is not None and prior.resources[0].state == "retained"
    public, semantic = inputs(repo, head, tmp_path / "worktrees" / "new")
    semantic["acquisition"]["provision_disposition"] = "existing_branch"
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="branch_responsibility_pending"):
        execute(repo, public, semantic, confirmed=True)
    assert ResourceLedgerStore(inspect_repository(repo)).read(key) == prior


def test_other_task_binding_still_blocks_branch_reuse(tmp_path):
    repo, head = repository(tmp_path)
    facts = inspect_repository(repo)
    BranchBindingStore(facts).establish(TaskLifecycleKey("another-task", 0), "codex/demo-next")
    target = tmp_path / "worktrees" / "new"
    public, semantic = inputs(repo, head, target)
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="branch_responsibility_pending"):
        execute(repo, public, semantic, confirmed=True)
    assert not target.exists()


@pytest.mark.parametrize("condition", ["missing_seal", "missing_summary", "unfinished_transaction", "wrong_finish_head"])
def test_unfinished_archive_cannot_reactivate(tmp_path, condition):
    repo, head = repository(tmp_path)
    facts = inspect_repository(repo)
    if condition == "missing_seal":
        ResourceLedgerStore(facts).path_for(TaskLifecycleKey("demo", 2)).unlink()
    elif condition == "missing_summary":
        (repo / ".trellis/tasks/archive/2026-09/09-19-demo/finish-summary.json").unlink()
    elif condition == "wrong_finish_head":
        old_commit = git(repo, "rev-parse", "HEAD^")
        prior = ResourceLedgerStore(facts).read(TaskLifecycleKey("demo", 2))
        assert prior is not None
        ResourceLedgerStore(facts)._write(replace(prior, finish_head=old_commit))
    else:
        path = repo / ".trellis/.runtime/guru-team/finish/1234567890abcdef.json"
        record = json.loads(path.read_text())
        record["stage"] = "pr_open"
        record.pop("target_head")
        path.write_text(json.dumps(record))
    public, semantic = inputs(repo, head, tmp_path / "worktrees" / "new")
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="finish_result_unsealed|finish_transaction_unfinished"):
        execute(repo, public, semantic, confirmed=True)
    assert not (tmp_path / "worktrees/new").exists()


@pytest.mark.parametrize("condition", ["missing_seal", "unfinished_transaction"])
def test_resume_rechecks_original_finish_generation(tmp_path, condition):
    repo, head = repository(tmp_path)
    public, semantic = inputs(repo, head, tmp_path / "worktrees" / "new")
    assert execute(repo, public, semantic, confirmed=True)["exit_id"] == "session_binding_recovery_required"
    assert transaction_path(inspect_repository(repo), TaskLifecycleKey("demo", 2)).is_file()
    if condition == "missing_seal":
        ResourceLedgerStore(inspect_repository(repo)).path_for(TaskLifecycleKey("demo", 2)).unlink()
    else:
        path = repo / ".trellis/.runtime/guru-team/finish/1234567890abcdef.json"
        record = json.loads(path.read_text())
        record["stage"] = "pr_open"
        record.pop("target_head")
        path.write_text(json.dumps(record))
    semantic["route"] = "resume_reactivation"
    from runtime.task_lifecycle.errors import LifecycleContractError
    with pytest.raises(LifecycleContractError, match="finish_result_unsealed|finish_transaction_unfinished"):
        execute(repo, public, semantic, confirmed=False)


def test_session_recovery_then_planning_on_same_incarnation(tmp_path, monkeypatch):
    repo, head = repository(tmp_path)
    checkout = tmp_path / "worktrees" / "new"
    public, semantic = inputs(repo, head, checkout)
    assert execute(repo, public, semantic, confirmed=True)["exit_id"] == "session_binding_recovery_required"
    observed = []
    def resolved_session(root, key, task_ref):
        observed.append((root, key, task_ref))
        return "session_bound"
    monkeypatch.setattr(invoke, "session_outcome", resolved_session)
    before = (checkout / ".trellis/tasks/09-19-demo/task.json").read_bytes()
    semantic["route"] = "reactivated_to_planning"
    semantic["session_outcome"] = "session_bound"
    result = execute(repo, public, semantic, confirmed=True)
    assert result["exit_id"] == "reactivated_to_planning"
    assert (result["task_id"], result["task_ref"], result["lifecycle_generation"]) == (
        "demo", ".trellis/tasks/09-19-demo", 3
    )
    assert result["session_outcome"] == "session_bound"
    assert observed == [(repo, TaskLifecycleKey("demo", 3), ".trellis/tasks/09-19-demo")]
    assert (checkout / ".trellis/tasks/09-19-demo/task.json").read_bytes() == before
