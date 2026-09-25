import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
SPEC = importlib.util.spec_from_file_location("guru_cleanup_invoke", PACKAGE / "runtime/invoke.py")
assert SPEC and SPEC.loader
CLEANUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLEANUP)


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def fixture(tmp_path: Path, ownership: str = "guru_owned") -> tuple[Path, ResourceLedgerStore, dict, str]:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    (root / "tracked").write_text("base\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    head = git(root, "rev-parse", "HEAD")
    git(root, "branch", "codex/demo")
    store = ResourceLedgerStore(inspect_repository(root))
    key = TaskLifecycleKey("demo", 0)
    store.establish_current(key, binding_epoch=0, binding_revision=0, branch_name="codex/demo", branch_ownership=ownership, worktree_ownership="not_applicable")
    seal = store.seal_for_finish(key, finish_result_id="finish:demo", finish_head=head)
    public = {"profile": "normal", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0, "finish_result_id": "finish:demo", "inventory_id": seal["inventory_id"]}
    return root, store, public, head


def invoke(tmp_path: Path, root: Path, public: dict, confirmed: bool = False, route: str | None = None) -> dict:
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps({"profile": public["profile"], "mode": public["mode"], "route": {"typed_exit": route or ("handoff_cleanup_complete" if public["profile"] == "machine_handoff" else "cleaned")}}))
    argv = ["--root", str(root), "--input", str(input_path), "--semantic-result", str(semantic_path)]
    if confirmed:
        argv.append("--confirmed-cleanup")
    return CLEANUP.run(PACKAGE, {}, argv)


def test_contract_assets():
    validate_json(json.loads((PACKAGE / "interface.json").read_text()), ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    for name in ("public-input", "public-manual-input", "public-handoff-input"):
        validate_json(json.loads((PACKAGE / "examples" / (name + ".json")).read_text()), PACKAGE / "schemas/public-input.schema.json", name)


def test_cleanup_reentry_projections_validate_target_owned_profiles():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    for exit_id, example, authoring in (
        ("remaining_resources", "public-remaining-resources-output.json", "self-authoring.json"),
        ("manual_selection_required", "public-manual-selection-output.json", "manual-authoring.json"),
    ):
        output = json.loads((PACKAGE / "examples" / example).read_text())
        projection = next(row for row in interface["public_contracts"]["projections"] if row["exit_id"] == exit_id)
        consumer = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
        authored = json.loads((PACKAGE / "examples" / authoring).read_text())
        projected = {row["target"]: output[row["source"]] for row in projection["mappings"]}
        assert set(projected) == set(consumer["contract"]["seed_fields"])
        assert set(authored) == set(consumer["contract"]["authoring_fields"])
        validate_json({**authored, **projected}, PACKAGE / "schemas/public-input.schema.json", exit_id)


def test_normal_cleanup_deletes_sealed_guru_owned_branch_and_resolves_ledger(tmp_path):
    root, store, public, _head = fixture(tmp_path)
    assert invoke(tmp_path, root, public)["exit_id"] == "remaining_resources"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    result = invoke(tmp_path, root, public, confirmed=True)
    assert result["exit_id"] == "cleaned"
    assert subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/codex/demo"], cwd=root).returncode != 0
    ledger = store.read(TaskLifecycleKey("demo", 0))
    assert ledger.finish_result_id == "finish:demo"
    assert [(row.state, row.responsibility_role) for row in ledger.resources] == [("resolved", "superseded")]
    fresh = store.seal_for_finish(TaskLifecycleKey("demo", 0), finish_result_id="finish:demo", finish_head=_head)
    assert invoke(tmp_path, root, {**public, "inventory_id": fresh["inventory_id"]}) == result


def test_caller_owned_is_retained_and_manual_selection_requires_confirmation(tmp_path):
    root, store, public, head = fixture(tmp_path, ownership="caller_owned")
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    row = store.read(TaskLifecycleKey("demo", 0)).resources[0]
    assert row.state == "retained" and row.ownership == "caller_owned"
    manual = {"profile": "manual", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0, "finish_result_id": "finish:demo", "cleanup_state": "manual_cleanup_required", "selected_targets": [{"resource_id": row.resource_id, "kind": "local_branch", "portable_ref": row.portable_ref, "expected_cleanup_head": head}]}
    assert invoke(tmp_path, root, manual)["exit_id"] == "manual_selection_required"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    mismatch = {**manual, "selected_targets": [{**manual["selected_targets"][0], "expected_cleanup_head": "0" * 40}]}
    assert invoke(tmp_path, root, mismatch, confirmed=True)["reason_code"] == "branch_head_changed"
    result = invoke(tmp_path, root, manual, confirmed=True)
    assert result["exit_id"] == "cleaned"
    assert invoke(tmp_path, root, manual, confirmed=True) == result
    assert subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/codex/demo"], cwd=root).returncode != 0
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"


def test_manual_selection_refuses_a_current_resource(tmp_path):
    root, store, public, head = fixture(tmp_path, ownership="caller_owned")
    active = TaskLifecycleKey("other", 0)
    store.establish_current(active, binding_epoch=1, binding_revision=0, branch_name="codex/demo",
                            branch_ownership="caller_owned", worktree_ownership="not_applicable")
    row = store.read(TaskLifecycleKey("demo", 0)).resources[0]
    manual = {"profile": "manual", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0,
              "finish_result_id": "finish:demo", "cleanup_state": "manual_cleanup_required",
              "selected_targets": [{"resource_id": row.resource_id, "kind": row.kind,
                                    "portable_ref": row.portable_ref, "expected_cleanup_head": head}]}
    assert invoke(tmp_path, root, manual, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_already_absent_guru_resource_converges_and_resolves_ledger(tmp_path):
    root, store, public, head = fixture(tmp_path)
    git(root, "update-ref", "-d", "refs/heads/codex/demo", head)
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"


def test_failed_deletion_keeps_ledger_pending_until_retry(tmp_path, monkeypatch):
    root, store, public, _head = fixture(tmp_path)
    original = CLEANUP.remove_resource
    calls = 0

    def fail_once(root, item):
        nonlocal calls
        calls += 1
        return False if calls == 1 else original(root, item)

    monkeypatch.setattr(CLEANUP, "remove_resource", fail_once)
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "deletion_incomplete"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "cleanup_pending"

    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert calls == 2
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"


def test_normal_cleanup_deletes_worktree_branch_and_remote_in_order(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    (root / "tracked").write_text("base\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    head = git(root, "rev-parse", "HEAD")
    git(root, "branch", "codex/demo")
    remote = tmp_path / "github.com/example/repo.git"
    remote.parent.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(root, "remote", "add", "origin", str(remote))
    git(root, "push", "-q", "origin", "refs/heads/codex/demo:refs/heads/codex/demo")
    checkout = tmp_path / "linked"
    git(root, "worktree", "add", "-q", str(checkout), "codex/demo")
    store = ResourceLedgerStore(inspect_repository(root))
    key = TaskLifecycleKey("demo", 0)
    store.establish_current(key, binding_epoch=0, binding_revision=0, branch_name="codex/demo", branch_ownership="guru_owned", worktree_ownership="guru_owned")
    store.record_remote_delivery(key, expected_epoch=0, expected_revision=0, remote_name="origin", repository_ref="example/repo", branch_ref="refs/heads/codex/demo", ownership="guru_owned", expected_cleanup_head=head)
    seal = store.seal_for_finish(key, finish_result_id="finish:demo", finish_head=head)
    public = {"profile": "normal", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0, "finish_result_id": "finish:demo", "inventory_id": seal["inventory_id"]}
    removed = []
    original = CLEANUP.remove_resource
    def observed(root, item):
        removed.append(item["kind"])
        return original(root, item)
    monkeypatch.setattr(CLEANUP, "remove_resource", observed)

    assert invoke(tmp_path, root, public)["exit_id"] == "remaining_resources"
    assert checkout.is_dir()
    (checkout / "tracked").write_text("dirty\n")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "worktree_dirty"
    assert removed == []
    assert {row.state for row in store.read(key).resources} == {"cleanup_pending"}
    assert checkout.is_dir()
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    assert git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/demo")
    (checkout / "tracked").write_text("base\n")
    result = invoke(tmp_path, root, public, confirmed=True)
    assert result["exit_id"] == "cleaned"
    assert removed == ["linked_worktree", "local_branch", "remote_branch"]
    assert not checkout.exists()
    assert subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/codex/demo"], cwd=root).returncode != 0
    assert git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/demo") == ""
    assert {row.state for row in store.read(key).resources} == {"resolved"}


def test_checked_out_and_dirty_worktree_block_before_result_api(tmp_path):
    root, _store, public, _head = fixture(tmp_path)
    git(root, "switch", "-q", "codex/demo")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "branch_checked_out"
    git(root, "switch", "-q", "main")
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_stale_seal_and_moved_target_fail_closed(tmp_path):
    root, _store, public, _head = fixture(tmp_path)
    wrong = {**public, "inventory_id": "resource-inventory:stale"}
    assert invoke(tmp_path, root, wrong, confirmed=True)["reason_code"] == "resource_inventory_stale"
    git(root, "switch", "-q", "codex/demo")
    (root / "tracked").write_text("moved\n")
    git(root, "commit", "-qam", "move")
    git(root, "switch", "-q", "main")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "branch_head_changed"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_missing_terminal_ledger_and_handoff_require_explicit_route(tmp_path):
    root, store, public, _head = fixture(tmp_path)
    store.path_for(TaskLifecycleKey("demo", 0)).unlink()
    assert invoke(tmp_path, root, public)["exit_id"] == "manual_selection_required"
    handoff = {"profile": "machine_handoff", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0, "handoff_inventory": {"task_id": "demo", "lifecycle_generation": 0, "handoff_id": "handoff:demo", "inventory_id": "inventory:demo"}}
    assert invoke(tmp_path, root, handoff)["reason_code"] == "handoff_inventory_missing"


def handoff_fixture(tmp_path: Path) -> tuple[Path, ResourceLedgerStore, dict, str]:
    root, store, _normal, head = fixture(tmp_path)
    row = store.read(TaskLifecycleKey("demo", 0)).resources[0]
    ref = {"task_id": "demo", "lifecycle_generation": 0, "handoff_id": "handoff:demo", "inventory_id": "inventory:demo"}
    handoff = {"task_id": "demo", "lifecycle_generation": 0, "handoff_id": "handoff:demo",
               "receipt_ref": "refs/heads/guru-task-lifecycle/demo", "result_id": "handoff-result:demo"}
    path = store.repository.common_dir / "guru-team/handoff-cleanup/demo/0/handoff:demo.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"schema_version": "1.0", "inventory_ref": ref, "handoff_ref": handoff,
                                "resource_ids": [row.resource_id], "state": "released"}))
    public = {"profile": "machine_handoff", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0,
              "handoff_inventory": ref}
    return root, store, public, head


def test_handoff_requires_confirmation_resolves_exact_resource_and_recovers_result(tmp_path):
    root, store, public, _head = handoff_fixture(tmp_path)
    pending = invoke(tmp_path, root, public)
    assert pending["exit_id"] == "handoff_cleanup_remaining"
    assert pending["handoff_inventory"] == public["handoff_inventory"]
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "cleanup_pending"
    assert invoke(tmp_path, root, public, confirmed=True, route="handoff_cleanup_remaining") == pending
    complete = invoke(tmp_path, root, public, confirmed=True)
    assert complete["exit_id"] == "handoff_cleanup_complete"
    assert complete["handoff_ref"]["receipt_ref"] == "refs/heads/guru-task-lifecycle/demo"
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"
    assert not git(root, "branch", "--list", "codex/demo")
    assert invoke(tmp_path, root, public, confirmed=True) == complete


def test_handoff_already_absent_and_retry_after_deletion_failure(tmp_path, monkeypatch):
    root, store, public, head = handoff_fixture(tmp_path)
    original = CLEANUP.remove_resource
    monkeypatch.setattr(CLEANUP, "remove_resource", lambda *_args: False)
    assert invoke(tmp_path, root, public, confirmed=True)["reason"]["reason_code"] == "deletion_incomplete"
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "cleanup_pending"
    monkeypatch.setattr(CLEANUP, "remove_resource", original)
    git(root, "update-ref", "-d", "refs/heads/codex/demo", head)
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "handoff_cleanup_complete"
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"


def test_handoff_stale_inventory_generation_and_moved_head_do_not_delete(tmp_path):
    root, store, public, head = handoff_fixture(tmp_path)
    assert invoke(tmp_path, root, {**public, "lifecycle_generation": 1}, confirmed=True)["reason_code"] == "handoff_inventory_stale"
    wrong = {**public, "handoff_inventory": {**public["handoff_inventory"], "inventory_id": "inventory:other"}}
    assert invoke(tmp_path, root, wrong, confirmed=True)["reason_code"] == "handoff_inventory_stale"
    git(root, "switch", "-q", "codex/demo")
    (root / "tracked").write_text("moved\n")
    git(root, "commit", "-qam", "moved")
    git(root, "switch", "-q", "main")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "branch_head_changed"
    assert git(root, "rev-parse", "codex/demo") != head
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "cleanup_pending"
