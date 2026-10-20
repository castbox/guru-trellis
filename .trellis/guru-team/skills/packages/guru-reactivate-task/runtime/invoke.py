"""Original Reactivate executor; Markdown owns qualification and route decisions."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from runtime.io import CommandError, fail, read_json
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.maintenance_transport import call
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.checkout_acquisition import CheckoutAcquisitionPlan, acquire_checkout
from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import discover_worktree_facts, inspect_repository, local_branch_head
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.results import reason, task_artifact, transaction_ref
from runtime.task_lifecycle.schema import validate_dto
from runtime.task_lifecycle.session_adapter import resolve_session
from shared_finish import read_shared_archive, find_successor, formal_inspection, require


def blocked(package, code, refs):
    output = {"exit_id": "reactivate_blocked", **reason(code, [refs] if isinstance(refs, str) else refs)}
    validate_json(output, package / "schemas/public-blocked-output.schema.json", "stdout")
    return output


def transaction_path(repository, key):
    return repository.common_dir / "guru-team/reactivate" / key.task_id / f"{key.lifecycle_generation}.json"


def session_outcome(root: Path, key: TaskLifecycleKey, task_ref: str) -> str:
    init = root / ".trellis/scripts/common/__init__.py"
    if not init.is_file():
        raise LifecycleContractError("official_session_unavailable", "session", "Install the reviewed Fixed Fork schema-3 session API.")
    spec = importlib.util.spec_from_file_location(
        "guru_reactivate_target_common_"+hashlib.sha256(str(init.resolve()).encode()).hexdigest()[:16], init, submodule_search_locations=[str(init.parent)]
    )
    if spec is None or spec.loader is None:
        raise LifecycleContractError("official_session_unavailable", "session", "Load the Fixed Fork session API.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    store = module.session_storage
    names = ("repository_facts", "session_path", "record_exists", "read_record", "write_record", "resolve_task_identity")
    official = SimpleNamespace(resolve_context_key=module.resolve_context_key, **{
        name: getattr(store, name) for name in names
    })
    result = resolve_session(official, root)
    if result.status == "explicit_task_mode" and result.reason_code == "context_key_unavailable":
        return "explicit_task_mode"
    if result.status == "session_resolved" and result.lifecycle == key and result.task_ref == task_ref:
        return "session_bound"
    return "recovery_required"


def acquisition_plan(root: Path, key: TaskLifecycleKey, semantic: dict[str, Any], archive_ref: str | None) -> CheckoutAcquisitionPlan:
    data = semantic["acquisition"]
    active_ref = data["task_ref"]
    if (data["task_id"], data["lifecycle_generation"], data["task_artifact_expectation"]) != (
        key.task_id, key.lifecycle_generation + 1, "absent"
    ) or (archive_ref is not None and active_ref != f".trellis/tasks/{Path(archive_ref).name}"):
        raise LifecycleContractError("reactivation_acquisition_mismatch", "acquisition", "Acquire the next planning incarnation of the archived TaskId.")
    base_ref = canonical_head_ref(semantic["selected_base_ref"])
    if canonical_head_ref(data["branch_ref"]) == base_ref:
        raise LifecycleContractError("reactivation_branch_invalid", "acquisition.branch_ref", "Select a task branch distinct from the base.")
    repository = inspect_repository(root)
    if (local_branch_head(repository, base_ref) != semantic["reviewed_base_head"]
            or data["decision_head"] != semantic["reviewed_base_head"]):
        raise LifecycleContractError("reactivation_base_stale", "reviewed_base_head", "Review the current target base before reactivation.")
    return CheckoutAcquisitionPlan(
        route=data["route"], repository_context=root, task_id=key.task_id,
        task_ref=active_ref, lifecycle_generation=key.lifecycle_generation + 1,
        branch_ref=data["branch_ref"], expected_status="active",
        decision_head=data["decision_head"], transaction_id=data["transaction_id"],
        result_id=data["result_id"], provision_disposition=data.get("provision_disposition"),
        invocation_checkout=Path(data["invocation_checkout"]) if "invocation_checkout" in data else None,
        target_path=Path(data["target_path"]) if "target_path" in data else None,
        forbidden_branch_refs=(base_ref,), task_artifact_expectation="absent",
    )



def release_resolved_prior_binding(branches, resources, key, branch_name):
    owner = branches.branch_owner(branch_name)
    if owner is not None and owner.key != key:
        raise LifecycleContractError("branch_already_bound", "branch_name", "Keep the other Task's active resource association.")
    if resources.branch_has_unresolved_incarnation(branch_name, key=key, allowed_current_revision=None):
        raise LifecycleContractError("branch_responsibility_pending", "branch_name", "Resolve the same resource's pending responsibility before reuse.")
    old = branches.read(key)
    if old is None or old.branch_name != branch_name:
        return
    previous = resources.read(key)
    if previous is None or previous.finish_result_id is None:
        raise LifecycleContractError("branch_responsibility_pending", "resource_ledger", "Resolve the exact old binding before reusing its branch.")
    branches.retire_generation(key, expected_revision=old.binding_revision, expected_branch_name=old.branch_name)


def save_transaction(path, value):
    validate_json(value, Path(__file__).resolve().parents[1] / "schemas/reactivation-transaction.schema.json", "transaction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def finish_public_operation(path, record, source):
    if record["public_recovery_ref"] and Path(record["public_recovery_ref"]).is_file():
        result = call(source, "recoverMaintenance", {"recovery_ref": record["public_recovery_ref"]})
        if result["status"] != "applied":
            result = call(source, "resumeMaintenance", {"recovery_ref": record["public_recovery_ref"]})
    else:
        result = call(source, "applyMaintenance", {"plan": record["public_plan"], "state_dir": record["public_state_dir"]})
    record["public_recovery_ref"] = result["recovery_ref"]
    if result.get("status") == "applied":
        require("reactivated_task" in result, "maintenance", "Read the original operation's actual active key and locator.")
        record["reactivated_task"] = result["reactivated_task"]
        record["stage"] = "public_applied"
    save_transaction(path, record)
    return record["reactivated_task"]


def pending_output(record):
    guard = record["public_plan"]["guard"]
    require(guard["task_id"] == record["task_id"] and guard["generation"] == record["archived_generation"]
            and guard["output_generation"] == record["archived_generation"] + 1,
            "public_plan", "Locate the same public plan's validated target generation, without claiming it is active.")
    return {"exit_id": "resume_reactivation", **transaction_ref(guard["task_id"], guard["output_generation"], record["transaction_id"], record["result_id"])}


def finish_local_binding(working, record):
    repository = inspect_repository(working)
    branches, resources = BranchBindingStore(repository), ResourceLedgerStore(repository)
    original_key = TaskLifecycleKey(record["task_id"], record["archived_generation"])
    key = TaskLifecycleKey(**record["reactivated_task"]["key"])
    branch = record["branch_ref"].removeprefix("refs/heads/")
    binding = branches.read(key)
    if binding is None:
        release_resolved_prior_binding(branches, resources, original_key, branch)
        binding = branches.establish(key, branch)
    require(binding.branch_ref == record["branch_ref"], "branch_binding", "Recover this operation's exact local binding.")
    current = resources.read_current(key)
    if current is None:
        require(resources.read(key) is None, "resource_ledger", "Preserve existing later resource responsibility.")
        ownership = record["resource_ownership"]
        resources.establish_current(key, binding_revision=binding.binding_revision, branch_name=binding.branch_name,
            branch_ownership=ownership["branch"], worktree_ownership=ownership["worktree"])
    else:
        require((current.binding_revision, current.branch_name) == (binding.binding_revision, binding.branch_name),
                "resource_ledger", "Recover matching original local controls.")
    record["stage"] = "bound"
    for field in ("public_plan", "public_state_dir", "resource_ownership"):
        record.pop(field, None)
    return binding


def acquire_incarnation(root, key, public, semantic, facts):
    package = Path(__file__).resolve().parents[1]
    plan = acquisition_plan(root, key, semantic, None)
    repository = inspect_repository(root)
    branches, resources = BranchBindingStore(repository), ResourceLedgerStore(repository)
    branch = canonical_head_ref(plan.branch_ref).removeprefix("refs/heads/")
    # Only the selected resource is checked. Unrelated old-generation resources stay owned.
    owner = branches.branch_owner(branch)
    if (owner is not None and owner.key != key) or resources.branch_has_unresolved_incarnation(branch, key=key, allowed_current_revision=None):
        raise LifecycleContractError("branch_responsibility_pending", "branch_name", "Choose independent resources or resolve this resource's original responsibility.")
    completed = []

    def after_acquisition(acquired):
        checkout = acquired.checkout.path
        current = read_shared_archive(checkout, key, public["archive_anchor"])
        require(current["archive_commit"] == facts["archive_commit"], "archive_anchor", "Use the exact reviewed predecessor.")
        target = checkout / plan.task_ref
        if facts["family"] == "schema1":
            source = semantic["source_ref"]
            selected = formal_inspection(checkout, key, public["archive_anchor"], current, source)
            upstream = semantic["formal_input"]
            require(Path(upstream["root"]).resolve() == checkout.resolve()
                    and all(upstream.get(k) == v for k, v in selected.items() if k != "root") and upstream.get("active_ref") == plan.task_ref,
                    "formal_input", "Forward the exact AI-reviewed original SDK selection and projection.")
            prepared = call(source, "prepareFormalArchiveReactivation", upstream)
            path = transaction_path(repository, key)
            record = {"schema_version": "2.0", "stage": "public_prepared", "task_id": key.task_id,
                      "archived_generation": key.lifecycle_generation, "transaction_id": plan.transaction_id,
                      "result_id": plan.result_id, "branch_ref": canonical_head_ref(plan.branch_ref),
                      "base_ref": canonical_head_ref(semantic["selected_base_ref"]), "base_head": plan.decision_head,
                      "archive_anchor": public["archive_anchor"], "reactivated_task": None,
                      "public_recovery_ref": str(checkout / ".trellis/.runtime/guru-team/reactivate-public" / (prepared["operation_id"] + ".json")), "public_plan": prepared,
                      "public_state_dir": str(checkout / ".trellis/.runtime/guru-team/reactivate-public"),
                      "resource_ownership": {"branch": acquired.branch_ownership, "worktree": acquired.worktree_ownership}}
            save_transaction(path, record)
            try:
                actual = finish_public_operation(path, record, source)
            except CommandError as exc:
                # Preserve a clean acquired checkout carrying an ignored public
                # operation as well as an already-dirty applied incarnation.
                completed.append((checkout, exc))
                return
            if actual is None:
                completed.append((checkout, None))
                return
            recovery_ref = record["public_recovery_ref"]
        else:
            archive = checkout / facts["archive_ref"]
            require(not target.exists(), "task_ref", "Do not overwrite an existing active Task.")
            require(json.loads((archive / "task.json").read_text()) == facts["task"], "archive", "Use the exact shared predecessor bytes in the acquired checkout.")
            target.parent.mkdir(parents=True, exist_ok=True)
            archive.rename(target)
            try:
                receipt = DeliveryProjection(checkout, plan.task_ref).scope(semantic["authority"], reopen=True)
            except Exception:
                target.rename(archive)
                raise
            actual = {"key": receipt["key"], "task_ref": plan.task_ref}
            recovery_ref = None
        next_key = TaskLifecycleKey(**actual["key"])
        require(next_key == TaskLifecycleKey(key.task_id, key.lifecycle_generation + 1) and actual["task_ref"] == plan.task_ref,
                "reactivated_task", "Read the public writer's exact new key and active locator.")
        # Public work is retained if a subsequent local binding step needs recovery.
        if facts["family"] == "schema1":
            binding = finish_local_binding(checkout, record)
        else:
            release_resolved_prior_binding(branches, resources, key, branch)
            binding = branches.establish(next_key, branch)
            resources.establish_current(next_key, binding_revision=binding.binding_revision, branch_name=binding.branch_name,
                                        branch_ownership=acquired.branch_ownership, worktree_ownership=acquired.worktree_ownership)
        record = {"schema_version": "2.0", "stage": "bound", "task_id": key.task_id, "archived_generation": key.lifecycle_generation,
                  "transaction_id": plan.transaction_id, "result_id": plan.result_id,
                  "branch_ref": binding.branch_ref, "base_ref": canonical_head_ref(semantic["selected_base_ref"]),
                  "base_head": plan.decision_head, "archive_anchor": public["archive_anchor"],
                  "reactivated_task": actual, "public_recovery_ref": recovery_ref}
        validate_json(record, package / "schemas/reactivation-transaction.schema.json", "transaction")
        path = transaction_path(repository, key)
        save_transaction(path, record)
        completed.append((checkout, actual))
    acquire_checkout(plan, post_acquire=after_acquisition)
    return completed[0]


def execute(root, public, semantic):
    package = Path(__file__).resolve().parents[1]
    validate_json(public, package / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package / "schemas/semantic-result.schema.json", "semantic_result")
    if any(public[field] != semantic[field] for field in ("profile", "mode", "archived_lifecycle", "archive_anchor")):
        return blocked(package, "stale_semantic_result", "archive_anchor")
    key = TaskLifecycleKey(**validate_dto("TaskLifecycleDTO", public["archived_lifecycle"]))
    route = semantic["route"]
    if route == "reactivate_blocked":
        return blocked(package, semantic["reason_code"], semantic["reason_refs"])
    if route == "session_binding_recovery_required" and semantic.get("session_outcome") != "recovery_required":
        return blocked(package, "session_route_mismatch", "session_outcome")
    if route == "reactivated_to_planning" and semantic.get("session_outcome") not in {"session_bound", "explicit_task_mode"}:
        return blocked(package, "session_route_mismatch", "session_outcome")
    repository = inspect_repository(root)
    path = transaction_path(repository, key)
    stored = json.loads(path.read_text()) if path.is_file() else None
    working = root
    if stored is not None:
        validate_json(stored, package / "schemas/reactivation-transaction.schema.json", "transaction")
        require(stored["archive_anchor"] == public["archive_anchor"] and stored["task_id"] == key.task_id
                and stored["archived_generation"] == key.lifecycle_generation, "transaction", "Recover only the same predecessor and archive anchor.")
        if "acquisition" in semantic:
            require((stored["transaction_id"], stored["result_id"], stored["branch_ref"]) == (
                semantic["acquisition"]["transaction_id"], semantic["acquisition"]["result_id"], canonical_head_ref(semantic["acquisition"]["branch_ref"])),
                "transaction", "Resume the exact acquisition transaction.")
        selected_ref = stored["branch_ref"]
        if stored["stage"] == "bound":
            current_binding = BranchBindingStore(repository).read(TaskLifecycleKey(**stored["reactivated_task"]["key"]))
            if current_binding is not None:
                selected_ref = current_binding.branch_ref
        rows = [row for row in discover_worktree_facts(repository) if row.branch_ref == selected_ref]
        require(len(rows) == 1, "checkout", "Resolve the original acquired checkout through live Git registration.")
        working = rows[0].path
    facts = read_shared_archive(working, key, public["archive_anchor"])
    if stored is not None and stored["stage"] in {"public_prepared", "public_applied"}:
        require("source_ref" in semantic, "source_ref", "Recover the original public operation with its matching source.")
        if finish_public_operation(path, stored, semantic["source_ref"]) is None:
            return pending_output(stored)
        finish_local_binding(working, stored)
        save_transaction(path, stored)
    working, successor = find_successor(working, key, public["archive_anchor"], facts, semantic.get("source_ref"), with_checkout=True)
    if successor is None:
        require(stored is None and route != "resume_reactivation", "transaction", "Recover the original public incarnation; do not create another one.")
        require("acquisition" in semantic and "authority" in semantic, "acquisition", "Review the exact new-generation checkout and scope before acquisition.")
        working, successor = acquire_incarnation(root, key, public, semantic, facts)
        stored = json.loads(path.read_text())
        if isinstance(successor, CommandError):
            raise successor
        if successor is None:
            return pending_output(stored)
    else:
        if successor["task_ref"].startswith(".trellis/tasks/archive/"):
            return blocked(package, "successor_archive_review_required", [successor["task_ref"],
                "task_id=" + successor["key"]["task_id"], "lifecycle_generation=" + str(successor["key"]["lifecycle_generation"])])
    actual_key = TaskLifecycleKey(**successor["key"])
    if route == "resume_reactivation":
        require(stored is not None, "transaction", "No private operation exists; continue the verified public successor through the original environment owners.")
        original_key = stored["reactivated_task"]["key"]
        output = {"exit_id": route, **transaction_ref(original_key["task_id"], original_key["lifecycle_generation"], stored["transaction_id"], stored["result_id"])}
    elif route == "session_binding_recovery_required":
        require(semantic.get("session_outcome") == "recovery_required", "session_outcome", "Use the actual Bind recovery route.")
        output = {"exit_id": route, "task_id": actual_key.task_id, "lifecycle_generation": actual_key.lifecycle_generation}
    else:
        local_repository = inspect_repository(working)
        binding = BranchBindingStore(local_repository).read(actual_key)
        ownership = ResourceLedgerStore(local_repository).read_current(actual_key)
        require(binding is not None and ownership is not None
                and (binding.binding_revision, binding.branch_name) == (ownership.binding_revision, ownership.branch_name),
                "branch_binding", "Establish/Ensure/Bind matching actual public successor controls before Planning.")
        outcome = session_outcome(working, actual_key, successor["task_ref"])
        require(outcome == semantic.get("session_outcome") and outcome in {"session_bound", "explicit_task_mode"}, "session_outcome", "Read the actual current session outcome.")
        output = {"exit_id": route, **task_artifact(actual_key.task_id, successor["task_ref"], actual_key.lifecycle_generation),
                  "binding_revision": binding.binding_revision, "session_outcome": outcome}
    validate_json(output, package / "schemas/public-output.schema.json", "stdout")
    return output


def run(package_root, command, argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the Reactivate command contract.") from exc
    try:
        return execute(Path(args.root).resolve(), read_json(args.input, "input"), read_json(args.semantic_result, "semantic_result"))
    except (CommandError, LifecycleContractError, OSError, ValueError, RuntimeError, ImportError, AttributeError) as exc:
        known = isinstance(exc, (CommandError, LifecycleContractError))
        return blocked(package_root, exc.code if known else "reactivation_state_invalid", exc.field_path if known else "task")


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).resolve().parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        raise SystemExit(fail(exc))
