from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError, fail, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.checkout_acquisition import CheckoutAcquisitionPlan, acquire_checkout
from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import commit_path_bytes, discover_worktree_facts, inspect_repository, local_branch_head
from runtime.task_lifecycle.identity import resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from runtime.task_lifecycle.results import reason, task_artifact, transaction_ref
from runtime.task_lifecycle.schema import validate_dto
from runtime.task_lifecycle.session_adapter import resolve_session


def blocked(package: Path, code: str, refs: str | list[str]) -> dict[str, Any]:
    output = {"exit_id": "reactivate_blocked", **reason(code, [refs] if isinstance(refs, str) else refs)}
    validate_json(output, package / "schemas/public-blocked-output.schema.json", "stdout")
    return output


def transaction_path(repository: Any, key: TaskLifecycleKey) -> Path:
    return repository.common_dir / "guru-team" / "reactivate" / key.task_id / f"{key.lifecycle_generation}.json"


def source_transaction_path(repository: Any, key: TaskLifecycleKey) -> Path:
    return repository.common_dir / "guru-team" / "reactivate" / key.task_id / f"{key.lifecycle_generation}-source.json"


def session_outcome(root: Path, key: TaskLifecycleKey, task_ref: str) -> str:
    init = root / ".trellis/scripts/common/__init__.py"
    if not init.is_file():
        raise LifecycleContractError("official_session_unavailable", "session", "Install the Fixed Fork schema-2 session API.")
    spec = importlib.util.spec_from_file_location(
        "guru_reactivate_target_common", init, submodule_search_locations=[str(init.parent)]
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


def archived_identity(root: Path, key: TaskLifecycleKey) -> str:
    identity = resolve_task_id(root, key.task_id)
    if identity.lifecycle_state != "archived" or identity.lifecycle_generation != key.lifecycle_generation:
        raise LifecycleContractError("archived_lifecycle_stale", "archived_lifecycle", "Resolve the exact finished archived generation.")
    metadata = json.loads((root / identity.task_ref / "task.json").read_text(encoding="utf-8"))
    if metadata.get("status") != "completed":
        raise LifecycleContractError("archived_lifecycle_stale", "task.status", "Reactivate only a normally finished task.")
    summary_path = root / identity.task_ref / "finish-summary.json"
    if not summary_path.is_file():
        raise LifecycleContractError("finish_result_unsealed", "finish-summary", "Finish must persist the terminal archive before Reactivate.")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if (summary.get("schema_version") != 2 or summary.get("task", {}).get("archive_dir") != identity.task_ref
            or summary.get("task", {}).get("status") != "completed"):
        raise LifecycleContractError("finish_result_unsealed", "finish-summary", "Use the exact normally finished archive.")
    verify_finish_seal(inspect_repository(root), key, identity.task_ref)
    return identity.task_ref


def verify_finish_seal(repository: Any, key: TaskLifecycleKey, archive_ref: str) -> None:
    ledger = ResourceLedgerStore(repository).read(key)
    if ledger is None or ledger.finish_result_id is None or ledger.finish_head is None:
        raise LifecycleContractError("finish_result_unsealed", "resource_ledger", "Recover and seal Finish for the archived generation first.")
    committed_task = commit_path_bytes(repository, ledger.finish_head, f"{archive_ref}/task.json")
    committed_summary = commit_path_bytes(repository, ledger.finish_head, f"{archive_ref}/finish-summary.json")
    if committed_task is None or committed_summary is None:
        raise LifecycleContractError("finish_result_unsealed", "finish_head", "The sealed Finish HEAD must contain the terminal task archive.")
    terminal_task = json.loads(committed_task)
    terminal_summary = json.loads(committed_summary)
    if (terminal_task.get("id") != key.task_id or terminal_task.get("lifecycle_generation", 0) != key.lifecycle_generation
            or terminal_task.get("status") != "completed" or terminal_summary.get("schema_version") != 2
            or terminal_summary.get("task", {}).get("archive_dir") != archive_ref):
        raise LifecycleContractError("finish_result_unsealed", "finish_head", "Use a Finish seal for the exact archived TaskLifecycleKey.")
    finish_schema = Path(__file__).resolve().parents[2] / "guru-finish-task/schemas/finish-transaction.schema.json"
    for checkout in discover_worktree_facts(repository):
        directory = checkout.path / ".trellis/.runtime/guru-team/finish"
        if not directory.is_dir():
            continue
        for path in directory.glob("*.json"):
            transaction = json.loads(path.read_text(encoding="utf-8"))
            if transaction.get("task_id") != key.task_id or transaction.get("lifecycle_generation") != key.lifecycle_generation:
                continue
            validate_json(transaction, finish_schema, "finish_transaction")
            if (transaction["stage"] != "success" or transaction["finish_ref"] != ledger.finish_result_id
                    or transaction["target_head"] != ledger.finish_head or transaction["archive_ref"] != archive_ref):
                raise LifecycleContractError("finish_transaction_unfinished", "finish_transaction", "Resume the exact Finish transaction before Reactivate.")


def correct_source(root: Path, key: TaskLifecycleKey, archive_ref: str, correction: dict[str, Any]) -> None:
    from runtime.task_lifecycle.source import normalize_source

    repository = inspect_repository(root)
    if transaction_path(repository, key).exists():
        raise LifecycleContractError("source_correction_stale", "transaction", "Do not correct an archive after its next generation exists.")
    path = source_transaction_path(repository, key)
    metadata_path = root / archive_ref / "task.json"
    original = metadata_path.read_bytes()
    metadata = json.loads(original)
    current = normalize_source(metadata.get("source"))
    receipt = {"schema_version": "1.0", **correction}
    schema = Path(__file__).resolve().parents[1] / "schemas/source-correction-transaction.schema.json"
    validate_json(receipt, schema, "source_correction_transaction")
    if path.exists():
        stored = json.loads(path.read_text(encoding="utf-8"))
        validate_json(stored, schema, "source_correction_transaction")
        if stored != receipt or current != correction["reviewed_source"]:
            raise LifecycleContractError("source_correction_stale", "source_correction", "Resume only the exact applied source correction.")
        return
    if current != correction["current_source"]:
        raise LifecycleContractError("source_correction_stale", "current_source", "Review the current archived source relation.")
    if current == correction["reviewed_source"]:
        raise LifecycleContractError("source_correction_stale", "reviewed_source", "No source correction is needed.")
    metadata["source"] = correction["reviewed_source"]
    try:
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            json.dump(receipt, stream, sort_keys=True)
            stream.write("\n")
    except Exception:
        metadata_path.write_bytes(original)
        raise


def release_resolved_prior_binding(branches: BranchBindingStore, resources: ResourceLedgerStore,
                                   key: TaskLifecycleKey, branch_name: str) -> Any:
    owner = branches.branch_owner(branch_name)
    if resources.branch_has_unresolved_incarnation(branch_name, key=key, allowed_current_epoch=None,
                                                   allowed_current_revision=None):
        raise LifecycleContractError("branch_responsibility_pending", "branch_name", "Resolve prior resource responsibility before reusing the branch.")
    if owner is not None and owner.key != key:
        raise LifecycleContractError("branch_already_bound", "branch_name", "Choose a branch without another task's active association.")
    old = branches.read(key)
    if old is None:
        return None
    previous = resources.read(key)
    if previous is None or previous.finish_result_id is None:
        raise LifecycleContractError("finish_result_unsealed", "resource_ledger", "Do not release a binding without the exact sealed old generation.")
    snapshot = branches.snapshot(key)
    branches.retire_generation(
        key,
        expected_epoch=old.binding_epoch,
        expected_revision=old.binding_revision,
        expected_branch_name=old.branch_name,
    )
    return snapshot


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
        branch_ref=data["branch_ref"], expected_status="planning",
        decision_head=data["decision_head"], transaction_id=data["transaction_id"],
        result_id=data["result_id"], provision_disposition=data.get("provision_disposition"),
        invocation_checkout=Path(data["invocation_checkout"]) if "invocation_checkout" in data else None,
        target_path=Path(data["target_path"]) if "target_path" in data else None,
        forbidden_branch_refs=(base_ref,), task_artifact_expectation="absent",
    )


def recover(root: Path, key: TaskLifecycleKey, plan: CheckoutAcquisitionPlan, semantic: dict[str, Any]) -> tuple[str, int] | None:
    repository = inspect_repository(root)
    path = transaction_path(repository, key)
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version": "1.0", "task_id": key.task_id, "archived_generation": key.lifecycle_generation,
        "transaction_id": plan.transaction_id, "result_id": plan.result_id,
        "branch_ref": canonical_head_ref(plan.branch_ref),
        "base_ref": canonical_head_ref(semantic["selected_base_ref"]),
        "base_head": plan.decision_head, "task_ref": plan.task_ref,
    }
    correction = semantic.get("source_correction")
    if correction is not None:
        expected["source_correction_result_id"] = validate_dto("SourceCorrectionReadyDTO", correction)["result_id"]
    if (not isinstance(record, dict) or set(record) != {*expected, "archive_ref", "binding_epoch"}
            or any(record[k] != value for k, value in expected.items())):
        raise LifecycleContractError("reactivation_transaction_conflict", "transaction", "Resume only the exact Reactivate transaction.")
    validate_json(record, Path(__file__).resolve().parents[1] / "schemas/reactivation-transaction.schema.json", "transaction")
    verify_finish_seal(repository, key, record["archive_ref"])
    next_key = TaskLifecycleKey(key.task_id, key.lifecycle_generation + 1)
    binding = BranchBindingStore(repository).read(next_key)
    ledger = ResourceLedgerStore(repository)
    ownership = ledger.read_current(next_key)
    if binding is None or ownership is None or (
        binding.binding_epoch, binding.binding_revision, binding.branch_ref
    ) != (record["binding_epoch"], 0, expected["branch_ref"]) or (
        ownership.binding_epoch, ownership.binding_revision, ownership.branch_name
    ) != (binding.binding_epoch, 0, binding.branch_name):
        raise LifecycleContractError("reactivation_transaction_conflict", "control_state", "Recover the exact branch and ownership state.")
    rows = [row for row in discover_worktree_facts(repository) if row.branch_ref == binding.branch_ref and row.head == plan.decision_head]
    target = plan.invocation_checkout if plan.route == "adopt_invocation_checkout" else plan.target_path
    if len(rows) != 1 or target is None or rows[0].path != target.resolve():
        raise LifecycleContractError("reactivation_transaction_conflict", "checkout", "Recover the exact live checkout target.")
    stored = ledger.read(next_key)
    expected_branch_owner = "guru_owned" if plan.provision_disposition == "new_branch" else "caller_owned"
    expected_worktree_owner = (
        "not_applicable" if rows[0].topology == "primary" else
        "caller_owned" if plan.route == "adopt_invocation_checkout" or plan.provision_disposition == "existing_checkout" else
        "guru_owned"
    )
    expected_resources = {"current_branch": expected_branch_owner}
    if expected_worktree_owner != "not_applicable":
        expected_resources["current_worktree"] = expected_worktree_owner
    if stored is None or stored.ledger_revision != 1 or {
        row.responsibility_role: row.ownership for row in stored.resources
    } != expected_resources or any(row.state != "current" or row.binding_epoch != binding.binding_epoch
                     or row.binding_revision != 0 or row.branch_ref != binding.branch_ref for row in stored.resources):
        raise LifecycleContractError("reactivation_transaction_conflict", "resource_ledger", "Recover the exact acquired resource ownership.")
    identity = resolve_task_id(rows[0].path, key.task_id)
    metadata = json.loads((rows[0].path / identity.task_ref / "task.json").read_text(encoding="utf-8"))
    if identity.task_ref != plan.task_ref or identity.lifecycle_generation != next_key.lifecycle_generation or metadata.get("status") != "planning":
        raise LifecycleContractError("reactivation_transaction_conflict", "task", "Recover the exact planning incarnation.")
    if correction is not None and metadata.get("source") != correction["reviewed_source"]:
        raise LifecycleContractError("reactivation_transaction_conflict", "source", "Recover the reviewed source correction in the planning artifact.")
    return identity.task_ref, binding.binding_epoch


def reactivate(root: Path, key: TaskLifecycleKey, plan: CheckoutAcquisitionPlan, semantic: dict[str, Any], archive_ref: str) -> tuple[str, int]:
    repository = inspect_repository(root)
    next_key = TaskLifecycleKey(key.task_id, key.lifecycle_generation + 1)
    branches = BranchBindingStore(repository)
    resources = ResourceLedgerStore(repository)
    if branches.read(next_key) is not None or resources.read(next_key) is not None or transaction_path(repository, key).exists():
        raise LifecycleContractError("reactivation_transaction_conflict", "control_state", "Resolve the partial transaction before creating another incarnation.")
    branch_name = canonical_head_ref(plan.branch_ref).removeprefix("refs/heads/")
    owner = branches.branch_owner(branch_name)
    if (owner is not None and owner.key != key) or resources.branch_has_unresolved_incarnation(
            branch_name, key=key, allowed_current_epoch=None, allowed_current_revision=None):
        raise LifecycleContractError("branch_responsibility_pending", "branch_name", "Resolve prior branch association and resource responsibility first.")
    completed: list[tuple[str, int]] = []

    def after_acquisition(result: Any) -> None:
        checkout = result.checkout.path
        if archived_identity(checkout, key) != archive_ref:
            raise LifecycleContractError("archived_lifecycle_stale", "archive", "Use the same archive on the reviewed base.")
        source = checkout / archive_ref
        target = checkout / plan.task_ref
        if target.exists():
            raise LifecycleContractError("reactivation_target_conflict", "task_ref", "Do not replace an active task.")
        original = (source / "task.json").read_bytes()
        correction = semantic.get("source_correction")
        if correction is not None:
            from runtime.task_lifecycle.source import normalize_source

            correction = validate_dto("SourceCorrectionReadyDTO", correction)
            if (correction["task_id"], correction["lifecycle_generation"], correction["task_ref"]) != (
                    key.task_id, key.lifecycle_generation, archive_ref):
                raise LifecycleContractError("source_correction_stale", "source_correction", "Apply only a correction for the exact archived incarnation.")
            actual_source = normalize_source(json.loads(original).get("source"))
            if actual_source not in (correction["current_source"], correction["reviewed_source"]):
                raise LifecycleContractError("source_correction_stale", "current_source", "Review the actual source in the acquired checkout.")
        elif source_transaction_path(repository, key).exists():
            receipt = json.loads(source_transaction_path(repository, key).read_text(encoding="utf-8"))
            if json.loads(original).get("source") != receipt.get("reviewed_source"):
                raise LifecycleContractError("source_correction_stale", "source", "Carry the reviewed source correction into the acquired checkout.")
        branch_snapshot = branches.snapshot(next_key)
        resource_snapshot = resources.snapshot(next_key)
        old_snapshot = None
        moved = False
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
            moved = True
            metadata = json.loads(original)
            metadata.update(status="planning", completedAt=None, lifecycle_generation=next_key.lifecycle_generation,
                            base_branch=canonical_head_ref(semantic["selected_base_ref"]).removeprefix("refs/heads/"))
            metadata.pop("archive_dir", None)
            if correction is not None:
                metadata["source"] = correction["reviewed_source"]
            for field in ("worktree_path", "branch", "base_head"):
                metadata.pop(field, None)
            (target / "task.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            old_snapshot = release_resolved_prior_binding(branches, resources, key, branch_name)
            binding = branches.establish(next_key, branch_name)
            resources.establish_current(
                next_key, binding_epoch=binding.binding_epoch, binding_revision=0,
                branch_name=binding.branch_name, branch_ownership=result.branch_ownership,
                worktree_ownership=result.worktree_ownership,
            )
            record = {
                "schema_version": "1.0", "task_id": key.task_id, "archived_generation": key.lifecycle_generation,
                "transaction_id": plan.transaction_id, "result_id": plan.result_id,
                "branch_ref": binding.branch_ref, "base_ref": canonical_head_ref(semantic["selected_base_ref"]),
                "base_head": plan.decision_head, "archive_ref": archive_ref,
                "task_ref": plan.task_ref, "binding_epoch": binding.binding_epoch,
            }
            if correction is not None:
                record["source_correction_result_id"] = correction["result_id"]
            validate_json(record, Path(__file__).resolve().parents[1] / "schemas/reactivation-transaction.schema.json", "transaction")
            path = transaction_path(repository, key)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as stream:
                json.dump(record, stream, sort_keys=True)
                stream.write("\n")
            completed.append((plan.task_ref, binding.binding_epoch))
        except Exception:
            resources.restore(next_key, resource_snapshot)
            branches.restore(branch_snapshot)
            if old_snapshot is not None:
                branches.restore(old_snapshot)
            if moved:
                (target / "task.json").write_bytes(original)
                target.rename(source)
            raise

    acquire_checkout(plan, post_acquire=after_acquisition)
    return completed[0]


def execute(root: Path, public: dict[str, Any], semantic: dict[str, Any], *, confirmed: bool) -> dict[str, Any]:
    package = Path(__file__).resolve().parents[1]
    validate_json(public, package / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package / "schemas/semantic-result.schema.json", "semantic_result")
    if any(public[field] != semantic[field] for field in ("profile", "mode", "archived_lifecycle")):
        return blocked(package, "stale_semantic_result", "archived_lifecycle")
    key = TaskLifecycleKey(**validate_dto("TaskLifecycleDTO", public["archived_lifecycle"]))
    route = semantic["route"]
    if route == "reactivate_blocked":
        return blocked(package, semantic["reason_code"], semantic["reason_refs"])
    if route == "source_correction_required":
        archive_ref = archived_identity(root, key)
        correction = validate_dto("SourceCorrectionReadyDTO", semantic["source_correction"])
        if (correction["task_id"], correction["lifecycle_generation"], correction["task_ref"]) != (key.task_id, key.lifecycle_generation, archive_ref):
            return blocked(package, "source_correction_stale", "source_correction")
        if not confirmed:
            raise CommandError("confirmation_required", "confirmed_reactivation", "Confirm the reviewed archived source correction.", 4)
        correct_source(root, key, archive_ref, correction)
        output = {"exit_id": route, **correction}
    else:
        if route == "reactivated_to_planning" and semantic["session_outcome"] not in {"session_bound", "explicit_task_mode"}:
            return blocked(package, "session_route_mismatch", "session_outcome")
        if route == "session_binding_recovery_required" and semantic["session_outcome"] != "recovery_required":
            return blocked(package, "session_route_mismatch", "session_outcome")
        if not confirmed and route != "resume_reactivation":
            raise CommandError("confirmation_required", "confirmed_reactivation", "Confirm the exact archive, base and acquisition plan.", 4)
        repository = inspect_repository(root)
        existing = transaction_path(repository, key).exists()
        archive_ref = None if existing else archived_identity(root, key)
        plan = acquisition_plan(root, key, semantic, archive_ref)
        prior = recover(root, key, plan, semantic) if existing else None
        if prior is None:
            if route == "resume_reactivation":
                return blocked(package, "reactivation_transaction_missing", "transaction")
            assert archive_ref is not None
            prior = reactivate(root, key, plan, semantic, archive_ref)
        task_ref, epoch = prior
        if route == "resume_reactivation":
            output = {"exit_id": route, **transaction_ref(key.task_id, key.lifecycle_generation + 1, plan.transaction_id, plan.result_id)}
        elif route == "session_binding_recovery_required":
            output = {"exit_id": route, "task_id": key.task_id, "lifecycle_generation": key.lifecycle_generation + 1}
        else:
            actual = session_outcome(root, TaskLifecycleKey(key.task_id, key.lifecycle_generation + 1), task_ref)
            if actual != semantic["session_outcome"]:
                return blocked(package, "session_outcome_stale", "session")
            output = {"exit_id": route, **task_artifact(key.task_id, task_ref, key.lifecycle_generation + 1),
                      "binding_epoch": epoch, "binding_revision": 0, "session_outcome": semantic["session_outcome"]}
    validate_json(output, package / "schemas/public-output.schema.json", "stdout")
    exit_schema = {
        "reactivated_to_planning": "public-planning-output.schema.json",
        "session_binding_recovery_required": "public-session-output.schema.json",
        "resume_reactivation": "public-resume-output.schema.json",
        "source_correction_required": "public-source-output.schema.json",
    }[route]
    validate_json(output, package / "schemas" / exit_schema, "stdout")
    return output


def run(package_root: Path, command: dict, argv: list[str]) -> dict[str, Any]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-reactivation", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the Reactivate command contract.") from exc
    try:
        return execute(Path(args.root).resolve(), read_json(args.input, "input"), read_json(args.semantic_result, "semantic_result"), confirmed=args.confirmed_reactivation)
    except (LifecycleContractError, OSError, ValueError, RuntimeError, ImportError, AttributeError) as exc:
        if isinstance(exc, LifecycleContractError):
            return blocked(package_root, exc.code, exc.field_path)
        return blocked(package_root, "reactivation_state_invalid", "task")


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).resolve().parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        raise SystemExit(fail(exc))
