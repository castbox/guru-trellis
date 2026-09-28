import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
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
    store.establish_current(key, binding_revision=0, branch_name="codex/demo", branch_ownership=ownership, worktree_ownership="not_applicable")
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


def selection(root: Path, *, task_id: str = "demo", finish_result_id: str = "finish:demo",
              kinds: tuple[str, ...] = ("local_branch",), branch_name: str = "codex/demo") -> dict:
    candidates = [dto for dto, _item in CLEANUP.discover_candidates(root).values()
                  if dto["kind"] in kinds and dto["branch_name"] == branch_name]
    assert len(candidates) == len(kinds)
    return {"profile": "select_explicit_cleanup_targets", "mode": "standalone", "task_id": task_id,
            "lifecycle_generation": 0, "finish_result_id": finish_result_id,
            "selected_candidate_ids": [dto["candidate_id"] for dto in candidates]}


def test_contract_assets():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    for item in interface["artifacts"] + interface["schemas"]:
        assert (PACKAGE / item["path"]).is_file()
    outputs = interface["public_contracts"]["outputs"]
    exits = [item["id"] for item in interface["external_exits"]]
    projections = [item["exit_id"] for item in interface["public_contracts"]["projections"]]
    assert sorted(exits) == sorted(item["exit_id"] for item in outputs) == sorted(projections)
    for item in outputs:
        schema = PACKAGE / item["schema"]["path"]
        assert json.loads(schema.read_text())["$id"] == item["schema"]["schema_id"]
        validate_json(json.loads((PACKAGE / item["example"]["path"]).read_text()), schema, item["exit_id"])
    for name in ("public-input", "public-selection-input", "public-handoff-input"):
        validate_json(json.loads((PACKAGE / "examples" / (name + ".json")).read_text()), PACKAGE / "schemas/public-input.schema.json", name)
    for name in ("public-output", "public-manual-cleanup-required-output", "public-remaining-resources-output",
                 "public-blocked-output", "public-handoff-complete-output", "public-handoff-remaining-output"):
        validate_json(json.loads((PACKAGE / "examples" / (name + ".json")).read_text()),
                      PACKAGE / "schemas/public-output.schema.json", name)
    retired = json.loads((PACKAGE / "examples/public-selection-input.json").read_text())
    retired["profile"] = "manual"
    with pytest.raises(CommandError):
        validate_json(retired, PACKAGE / "schemas/public-input.schema.json", "retired_profile")


def test_selection_rejects_wrong_profile_route_before_deletion(tmp_path):
    root, _store, public, _checkout = missing_ledger_fixture(tmp_path)
    with pytest.raises(CommandError) as exc:
        invoke(tmp_path, root, public, confirmed=True, route="handoff_cleanup_complete")
    assert exc.value.code == "schema_mismatch"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_cleanup_reentry_projections_validate_target_owned_profiles():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    for exit_id, example, authoring in (
        ("remaining_resources", "public-remaining-resources-output.json", "self-authoring.json"),
        ("manual_cleanup_required", "public-manual-cleanup-required-output.json", "selection-authoring.json"),
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


def test_normal_cleanup_same_seal_recovers_cleaned_after_output_loss(tmp_path):
    root, store, public, _head = fixture(tmp_path)
    first = invoke(tmp_path, root, public, confirmed=True)
    assert first["exit_id"] == "cleaned"
    assert not git(root, "branch", "--list", "codex/demo")
    assert invoke(tmp_path, root, public, confirmed=True) == first
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"
    wrong = {**public, "inventory_id": "resource-inventory:stale"}
    assert invoke(tmp_path, root, wrong, confirmed=True)["reason_code"] == "resource_inventory_stale"


def test_caller_owned_is_retained_and_manual_selection_requires_confirmation(tmp_path):
    root, store, public, _head = fixture(tmp_path, ownership="caller_owned")
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    row = store.read(TaskLifecycleKey("demo", 0)).resources[0]
    assert row.state == "retained" and row.ownership == "caller_owned"
    manual = selection(root)
    assert invoke(tmp_path, root, manual)["exit_id"] == "manual_cleanup_required"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    result = invoke(tmp_path, root, manual, confirmed=True)
    assert result["exit_id"] == "cleaned"
    assert invoke(tmp_path, root, manual, confirmed=True) == result
    assert subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/codex/demo"], cwd=root).returncode != 0
    assert store.read(TaskLifecycleKey("demo", 0)).resources[0].state == "resolved"


def test_manual_cleanup_removes_selected_linked_worktree_before_its_branch(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    (root / "tracked").write_text("base\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    head = git(root, "rev-parse", "HEAD")
    checkout = tmp_path / "linked"
    git(root, "worktree", "add", "-q", "-b", "codex/demo", str(checkout), head)
    store = ResourceLedgerStore(inspect_repository(root))
    key = TaskLifecycleKey("demo", 0)
    store.establish_current(key, binding_revision=0, branch_name="codex/demo",
                            branch_ownership="caller_owned", worktree_ownership="caller_owned")
    store.seal_for_finish(key, finish_result_id="finish:demo", finish_head=head)
    rows = store.read(key).resources
    assert {row.kind for row in rows} == {"linked_worktree", "local_branch"}
    manual = selection(root, kinds=("linked_worktree", "local_branch"))

    branch_only = selection(root)
    assert invoke(tmp_path, root, branch_only, confirmed=True)["reason_code"] == "branch_checked_out"
    assert checkout.is_dir() and git(root, "show-ref", "--verify", "refs/heads/codex/demo")

    assert invoke(tmp_path, root, manual, confirmed=True)["exit_id"] == "cleaned"
    assert not checkout.exists() and not git(root, "branch", "--list", "codex/demo")
    assert {row.state for row in store.read(key).resources} == {"resolved"}


def test_manual_selection_refuses_a_current_resource(tmp_path):
    root, store, public, head = fixture(tmp_path, ownership="caller_owned")
    active = TaskLifecycleKey("other", 0)
    store.establish_current(active, binding_revision=0, branch_name="codex/demo",
                            branch_ownership="caller_owned", worktree_ownership="not_applicable")
    manual = selection(root)
    assert invoke(tmp_path, root, manual, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_manual_selection_refuses_new_generation_binding_missing_from_invoking_checkout(tmp_path):
    root, store, public, head = fixture(tmp_path, ownership="caller_owned")
    archived = root / ".trellis/tasks/archive/2026-09/demo"
    archived.mkdir(parents=True)
    (archived / "task.json").write_text(json.dumps({"id": "demo", "lifecycle_generation": 0, "status": "completed"}))
    BranchBindingStore(store.repository).establish(TaskLifecycleKey("demo", 1), "codex/demo")
    manual = selection(root)

    assert invoke(tmp_path, root, manual, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_manual_selection_accepts_reviewed_caller_owned_head_after_finish(tmp_path):
    root, store, _public, old_head = fixture(tmp_path, ownership="caller_owned")
    (root / "tracked").write_text("updated\n")
    git(root, "add", "tracked")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "later")
    new_head = git(root, "rev-parse", "HEAD")
    git(root, "update-ref", "refs/heads/codex/demo", new_head, old_head)
    manual = selection(root)

    assert invoke(tmp_path, root, manual)["exit_id"] == "manual_cleanup_required"
    assert invoke(tmp_path, root, manual, confirmed=True)["exit_id"] == "cleaned"
    assert not git(root, "branch", "--list", "codex/demo")


def test_manual_selection_accepts_reviewed_caller_owned_remote_head_after_finish(tmp_path):
    root, store, public, old_head = fixture(tmp_path, ownership="caller_owned")
    remote = tmp_path / "github.com/example/repo.git"
    remote.parent.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(root, "remote", "add", "origin", str(remote))
    git(root, "push", "-q", "origin", "refs/heads/codex/demo:refs/heads/codex/demo")
    fresh = ResourceLedgerStore(inspect_repository(root))
    fresh_key = TaskLifecycleKey("remote-demo", 0)
    fresh.establish_current(fresh_key, binding_revision=0, branch_name="codex/demo",
                            branch_ownership="caller_owned", worktree_ownership="not_applicable")
    fresh.record_remote_delivery(fresh_key, expected_revision=0,
                                 remote_name="origin", repository_ref="example/repo",
                                 branch_ref="refs/heads/codex/demo", ownership="caller_owned",
                                 expected_cleanup_head=old_head)
    fresh.seal_for_finish(fresh_key, finish_result_id="finish:remote-demo", finish_head=old_head)
    (root / "tracked").write_text("updated\n")
    git(root, "add", "tracked")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "later")
    new_head = git(root, "rev-parse", "HEAD")
    git(root, "push", "-q", "origin", "HEAD:refs/heads/codex/demo")
    manual = selection(root, task_id="remote-demo", finish_result_id="finish:remote-demo",
                       kinds=("remote_branch",))

    assert invoke(tmp_path, root, manual)["exit_id"] == "manual_cleanup_required"
    assert invoke(tmp_path, root, manual, confirmed=True)["exit_id"] == "cleaned"
    assert not git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/demo")


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
    store.establish_current(key, binding_revision=0, branch_name="codex/demo", branch_ownership="guru_owned", worktree_ownership="guru_owned")
    store.record_remote_delivery(key, expected_revision=0, remote_name="origin", repository_ref="example/repo", branch_ref="refs/heads/codex/demo", ownership="guru_owned", expected_cleanup_head=head)
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


def test_finish_cleanup_handoff_uses_retained_checkout(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    (root / "tracked").write_text("base\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    head = git(root, "rev-parse", "HEAD")
    checkout = tmp_path / "task-worktree"
    git(root, "worktree", "add", "-q", "-b", "codex/demo", str(checkout), head)
    store = ResourceLedgerStore(inspect_repository(root))
    key = TaskLifecycleKey("demo", 0)
    store.establish_current(key, binding_revision=0, branch_name="codex/demo",
                            branch_ownership="guru_owned", worktree_ownership="guru_owned")
    seal = store.seal_for_finish(key, finish_result_id="finish:demo", finish_head=head)
    public = {"profile": "normal", "mode": "standalone", "task_id": "demo",
              "lifecycle_generation": 0, "finish_result_id": "finish:demo", "inventory_id": seal["inventory_id"]}

    assert invoke(tmp_path, checkout, public, confirmed=True)["reason_code"] == "worktree_identity_changed"
    assert checkout.is_dir()
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert not checkout.exists()


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
    root, _store, selected, _checkout = missing_ledger_fixture(tmp_path)
    public = {"profile": "normal", "mode": "standalone", "task_id": "demo",
              "lifecycle_generation": 0, "finish_result_id": selected["finish_result_id"],
              "inventory_id": "resource-inventory:missing"}
    output = invoke(tmp_path, root, public)
    assert output["exit_id"] == "manual_cleanup_required"
    assert {row["kind"] for row in output["candidates"]} >= {"local_branch", "linked_worktree"}
    assert all(row["candidate_id"] and row["live_head"] for row in output["candidates"])
    assert invoke(tmp_path, root, public)["candidates"] == output["candidates"]
    discovery = {"profile": "select_explicit_cleanup_targets", "mode": "standalone",
                 "task_id": "demo", "lifecycle_generation": 0,
                 "finish_result_id": selected["finish_result_id"], "selected_candidate_ids": []}
    assert invoke(tmp_path, root, discovery, confirmed=True) == output
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    handoff = {"profile": "machine_handoff", "mode": "standalone", "task_id": "demo", "lifecycle_generation": 0, "handoff_inventory": {"task_id": "demo", "lifecycle_generation": 0, "handoff_id": "handoff:demo", "inventory_id": "inventory:demo"}}
    assert invoke(tmp_path, root, handoff)["reason_code"] == "handoff_inventory_missing"


def test_missing_ledger_does_not_list_candidates_without_terminal_finish(tmp_path):
    root, store, public, _head = fixture(tmp_path)
    store.path_for(TaskLifecycleKey("demo", 0)).unlink()
    assert invoke(tmp_path, root, public)["exit_id"] == "blocked"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_missing_ledger_confirmed_empty_selection_seals_without_deleting_other_resources(tmp_path):
    root, store, selected, _checkout = missing_ledger_fixture(tmp_path)
    git(root, "update-ref", "-d", "refs/heads/codex/demo")
    public = {**selected, "selected_candidate_ids": []}
    listed = invoke(tmp_path, root, public)
    assert listed["exit_id"] == "manual_cleanup_required"
    assert any(row["branch_name"] == "main" for row in listed["candidates"])
    completed = invoke(tmp_path, root, public, confirmed=True)
    assert completed["exit_id"] == "cleaned"
    assert invoke(tmp_path, root, public, confirmed=True) == completed
    receipts = list((store.repository.common_dir / "guru-team/cleanup-results/demo").glob("selected-*.json"))
    assert len(receipts) == 1
    assert json.loads(receipts[0].read_text())["output"] == completed
    assert git(root, "show-ref", "--verify", "refs/heads/main")
    assert store.read(TaskLifecycleKey("demo", 0)) is None


def test_missing_ledger_manual_cleanup_requires_exact_finished_generation(tmp_path):
    root, store, public, head = fixture(tmp_path, ownership="caller_owned")
    key = TaskLifecycleKey("demo", 0)
    store.path_for(key).unlink()
    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    archive = root / archive_ref
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "lifecycle_generation": 0, "status": "completed"}))
    (archive / "finish-summary.json").write_text("{}\n")
    git(root, "switch", "-q", "codex/demo")
    git(root, "add", archive_ref)
    git(root, "commit", "-qm", "finish")
    head = git(root, "rev-parse", "HEAD")
    git(root, "switch", "-q", "main")
    result_id = "finish:v1:0123456789abcdef"
    manual = selection(root, finish_result_id=result_id)
    assert invoke(tmp_path, root, manual, confirmed=True)["reason_code"] == "manual_finish_result_missing"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")

    result_path = store.repository.common_dir / "guru-team/finish-results/demo/0-manual.json"
    result_path.parent.mkdir(parents=True)
    result = {"schema_version": "1.0", "task_id": "demo", "lifecycle_generation": 0,
              "finish_result_id": result_id, "finish_head": head, "target_head": head, "archive_ref": archive_ref}
    result_path.write_text(json.dumps(result))
    assert invoke(tmp_path, root, {**manual, "finish_result_id": "finish:v1:fedcba9876543210"}, confirmed=True)["reason_code"] == "manual_finish_result_stale"
    assert invoke(tmp_path, root, manual)["exit_id"] == "manual_cleanup_required"
    assert invoke(tmp_path, root, manual, confirmed=True)["exit_id"] == "cleaned"
    assert not git(root, "branch", "--list", "codex/demo")


def missing_ledger_fixture(tmp_path: Path, *, linked: bool = False) -> tuple[Path, ResourceLedgerStore, dict, Path | None]:
    root, store, _public, head = fixture(tmp_path, ownership="caller_owned")
    store.path_for(TaskLifecycleKey("demo", 0)).unlink()
    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    archive = root / archive_ref
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "lifecycle_generation": 0, "status": "completed"}))
    (archive / "finish-summary.json").write_text("{}\n")
    git(root, "switch", "-q", "codex/demo")
    git(root, "add", archive_ref)
    git(root, "commit", "-qm", "finish")
    head = git(root, "rev-parse", "HEAD")
    git(root, "switch", "-q", "main")
    checkout = tmp_path / "linked" if linked else None
    if checkout:
        git(root, "worktree", "add", "-q", str(checkout), "codex/demo")
    result_id = "finish:v1:0123456789abcdef"
    result_path = store.repository.common_dir / "guru-team/finish-results/demo/0-manual.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(json.dumps({"schema_version": "1.0", "task_id": "demo", "lifecycle_generation": 0,
                                       "finish_result_id": result_id, "finish_head": head,
                                       "target_head": head, "archive_ref": archive_ref,
                                       "head_branch": "codex/demo"}))
    return root, store, selection(root, finish_result_id=result_id), checkout


def test_missing_ledger_uses_finish_commit_when_retained_checkout_lags(tmp_path):
    root, _store, selected, checkout = missing_ledger_fixture(tmp_path, linked=True)
    assert checkout is not None
    assert not (root / ".trellis/tasks/archive/2026-09/demo/task.json").exists()
    assert (checkout / ".trellis/tasks/archive/2026-09/demo/task.json").is_file()
    listed = invoke(tmp_path, root, {**selected, "selected_candidate_ids": []})
    assert listed["exit_id"] == "manual_cleanup_required"
    targets = [row["candidate_id"] for row in listed["candidates"]
               if row["branch_name"] == "codex/demo" and row["kind"] in {"local_branch", "linked_worktree"}]
    assert len(targets) == 2
    assert invoke(tmp_path, root, {**selected, "selected_candidate_ids": targets})["exit_id"] == "manual_cleanup_required"


def test_missing_ledger_rejects_finish_target_without_archive(tmp_path):
    root, store, selected, _checkout = missing_ledger_fixture(tmp_path)
    result_path = store.repository.common_dir / "guru-team/finish-results/demo/0-manual.json"
    result = json.loads(result_path.read_text())
    result["target_head"] = git(root, "rev-parse", "main")
    result["finish_head"] = result["target_head"]
    result_path.write_text(json.dumps(result))
    discovery = {**selected, "selected_candidate_ids": []}
    assert invoke(tmp_path, root, discovery)["reason_code"] == "manual_finish_result_stale"
    assert invoke(tmp_path, root, selected)["reason_code"] == "manual_finish_result_stale"


def test_missing_ledger_stale_head_blocks_selected_candidate(tmp_path):
    root, store, public, _checkout = missing_ledger_fixture(tmp_path)
    git(root, "switch", "-q", "codex/demo")
    (root / "tracked").write_text("later\n")
    git(root, "commit", "-qam", "later")
    git(root, "switch", "-q", "main")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "cleanup_candidate_stale"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    assert store.read(TaskLifecycleKey("demo", 0)) is None


def test_missing_ledger_current_binding_blocks_selected_candidate(tmp_path):
    root, store, public, _checkout = missing_ledger_fixture(tmp_path)
    BranchBindingStore(store.repository).establish(TaskLifecycleKey("other", 0), "codex/demo")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_missing_other_task_control_state_keeps_its_active_checkout(tmp_path):
    root, _store, _public, checkout = missing_ledger_fixture(tmp_path, linked=True)
    assert checkout is not None
    task = checkout / ".trellis/tasks/09-28-other-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({
        "id": "other-task", "lifecycle_generation": 0, "status": "in_progress",
        "source": {"kind": "no_issue"},
    }))
    git(checkout, "add", ".trellis/tasks/09-28-other-task/task.json")
    git(checkout, "commit", "-qm", "start other task")
    selected = selection(root, finish_result_id="finish:v1:0123456789abcdef",
                         kinds=("linked_worktree", "local_branch"))
    assert invoke(tmp_path, root, selected, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert checkout.exists()
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_missing_other_task_control_state_keeps_its_remote_branch(tmp_path):
    root, _store, public, _checkout = missing_ledger_fixture(tmp_path)
    remote = tmp_path / "github.com/example/repo.git"
    remote.parent.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(root, "remote", "add", "origin", str(remote))
    git(root, "switch", "-q", "-c", "codex/other-task")
    task = root / ".trellis/tasks/09-28-other-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({
        "id": "other-task", "lifecycle_generation": 0, "status": "in_progress",
        "source": {"kind": "no_issue"},
    }))
    git(root, "add", ".trellis/tasks/09-28-other-task/task.json")
    git(root, "commit", "-qm", "start other task")
    git(root, "push", "-q", "origin", "HEAD:refs/heads/codex/other-task")
    git(root, "switch", "-q", "main")
    git(root, "branch", "-D", "codex/other-task")
    selected = selection(root, finish_result_id=public["finish_result_id"],
                         kinds=("remote_branch",), branch_name="codex/other-task")
    assert invoke(tmp_path, root, selected, confirmed=True)["reason_code"] == "resource_in_current_use"
    assert git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/other-task")


@pytest.mark.parametrize("retained_active_artifact", [True, False])
def test_manual_cleanup_requires_surviving_active_artifact(tmp_path, retained_active_artifact):
    root, _store, _public, _checkout = missing_ledger_fixture(tmp_path)
    git(root, "switch", "-q", "codex/demo")
    task = root / ".trellis/tasks/09-28-other-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({"id": "other-task", "status": "in_progress"}))
    git(root, "add", ".trellis/tasks/09-28-other-task/task.json")
    git(root, "commit", "-qm", "start other task")
    git(root, "switch", "-q", "main")
    git(root, "merge", "--ff-only", "codex/demo")
    if not retained_active_artifact:
        git(root, "rm", "-q", ".trellis/tasks/09-28-other-task/task.json")
        git(root, "commit", "-qm", "archive other task")
    selected = selection(root, finish_result_id="finish:v1:0123456789abcdef")
    result = invoke(tmp_path, root, selected, confirmed=True)
    if retained_active_artifact:
        assert result["exit_id"] == "cleaned"
        assert not git(root, "branch", "--list", "codex/demo")
    else:
        assert result["reason_code"] == "resource_in_current_use"
        assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")


def test_missing_ledger_dirty_worktree_blocks_selected_candidate(tmp_path):
    root, _store, _branch_only, checkout = missing_ledger_fixture(tmp_path, linked=True)
    assert checkout is not None
    public = selection(root, finish_result_id="finish:v1:0123456789abcdef", kinds=("linked_worktree",))
    (checkout / "tracked").write_text("dirty\n")
    assert invoke(tmp_path, root, public, confirmed=True)["reason_code"] == "worktree_dirty"
    assert checkout.exists()


def test_missing_ledger_partial_selection_preserves_unselected_resources(tmp_path):
    root, store, public, _checkout = missing_ledger_fixture(tmp_path)
    git(root, "branch", "codex/keep")
    listed = invoke(tmp_path, root, {"profile": "normal", "mode": "standalone", "task_id": "demo",
                                     "lifecycle_generation": 0, "finish_result_id": public["finish_result_id"],
                                     "inventory_id": "resource-inventory:missing"})
    assert listed["exit_id"] == "manual_cleanup_required"
    assert {row["branch_name"] for row in listed["candidates"]} >= {"codex/demo", "codex/keep"}
    assert invoke(tmp_path, root, public)["exit_id"] == "manual_cleanup_required"
    assert invoke(tmp_path, root, public, confirmed=True)["exit_id"] == "cleaned"
    assert not git(root, "branch", "--list", "codex/demo")
    assert git(root, "show-ref", "--verify", "refs/heads/codex/keep")
    assert store.read(TaskLifecycleKey("demo", 0)) is None


def test_missing_ledger_remote_identity_change_blocks_selection(tmp_path):
    root, _store, public, _checkout = missing_ledger_fixture(tmp_path)
    old_remote = tmp_path / "github.com/example/old.git"
    new_remote = tmp_path / "github.com/example/new.git"
    for remote in (old_remote, new_remote):
        remote.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(root, "remote", "add", "origin", str(old_remote))
    git(root, "push", "-q", "origin", "refs/heads/codex/demo:refs/heads/codex/demo")
    remote_dto = next(dto for dto, _item in CLEANUP.discover_candidates(root).values()
                      if dto["kind"] == "remote_branch" and dto["branch_name"] == "codex/demo")
    assert (remote_dto["remote_name"], remote_dto["remote_identity"]) == ("origin", "example/old")
    selected = selection(root, finish_result_id=public["finish_result_id"], kinds=("remote_branch",))
    git(root, "remote", "set-url", "origin", str(new_remote))
    git(root, "push", "-q", "origin", "refs/heads/codex/demo:refs/heads/codex/demo")
    assert invoke(tmp_path, root, selected, confirmed=True)["reason_code"] == "cleanup_candidate_stale"
    assert git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/demo")


def test_missing_ledger_remote_selection_deletes_only_exact_remote_ref(tmp_path):
    root, store, public, _checkout = missing_ledger_fixture(tmp_path)
    remote = tmp_path / "github.com/example/repo.git"
    remote.parent.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(root, "remote", "add", "origin", str(remote))
    git(root, "push", "-q", "origin", "refs/heads/codex/demo:refs/heads/codex/demo")
    selected = selection(root, finish_result_id=public["finish_result_id"], kinds=("remote_branch",))
    assert invoke(tmp_path, root, selected)["exit_id"] == "manual_cleanup_required"
    assert invoke(tmp_path, root, selected, confirmed=True)["exit_id"] == "cleaned"
    assert not git(root, "ls-remote", "--heads", "origin", "refs/heads/codex/demo")
    assert git(root, "show-ref", "--verify", "refs/heads/codex/demo")
    assert store.read(TaskLifecycleKey("demo", 0)) is None


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
