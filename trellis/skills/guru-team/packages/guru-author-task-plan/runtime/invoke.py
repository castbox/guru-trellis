from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import branch_checked_out_paths, inspect_repository
from runtime.task_lifecycle.identity import normalize_task_ref, resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


DELIVERY_PROFILES = {"delivery_" + name for name in {
    "initial_review", "active_task_scope_change", "wording_reentry",
    "approval_revision", "delivery_plan_revision", "requirements_revision",
    "solution_planning", "architecture_conflict_resolution",
}}
PROFILES = DELIVERY_PROFILES | {"task_scope_requirements"}


def _task(root: Path, task_ref: str) -> Path:
    try:
        normalize_task_ref(task_ref)
        path = root / task_ref
        metadata = read_json(str(path / "task.json"), "task_ref")
        identity = resolve_task_id(root, metadata["id"])
        record = DeliveryProjection(root, task_ref).read_record()
        if identity.task_ref != task_ref or record["lifecycle_generation"] != identity.lifecycle_generation:
            raise CommandError("stale_identity", "task_ref", "Resolve the same active task lifecycle.", 3)
        repository = inspect_repository(root)
        key = TaskLifecycleKey(identity.task_id, identity.lifecycle_generation)
        binding = BranchBindingStore(repository).read(key)
        resources = ResourceLedgerStore(repository).read_current(key)
        if (binding is None or resources is None
                or branch_checked_out_paths(repository, binding.branch_ref) != (root,)
                or (binding.binding_revision, binding.branch_name)
                != (resources.binding_revision, resources.branch_name)):
            raise CommandError("stale_identity", "task_ref", "Resolve the current bound task checkout.", 3)
        return path
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, f"{exc.code}: {exc.remediation}", 3) from exc
    except (KeyError, OSError) as exc:
        raise CommandError("stale_identity", "task_ref", "Resolve the current TaskId and checkout through their original owners.", 3) from exc


def _regular_content(path: Path, label: str, *, allow_empty: bool = False) -> None:
    if not path.is_file() or path.is_symlink() or (not allow_empty and not path.read_text(encoding="utf-8").strip()):
        raise CommandError("stale_identity", label, "Complete the current regular planning file before invoking its handoff.", 3)


def execute(package_root: Path, root: Path, public: dict, owner: dict) -> dict:
    profile = public.get("profile")
    if profile not in PROFILES:
        raise CommandError("schema_mismatch", "input.profile", "Use Task scope requirements or one of the eight Delivery Author profiles.")
    validate_json(public, package_root / "schemas" / f"public-{profile.replace('_', '-')}-input.schema.json", "input")
    validate_json(owner, package_root / "schemas/semantic-result-2.0.schema.json", "owner_result")
    if owner["public_input"] != public or owner["output"]["task_ref"] != public["task_ref"]:
        raise CommandError("stale_identity", "owner_result", "Repeat this owner review against the exact current input.", 3)
    output = owner["output"]
    exit_id = output["exit_id"]
    if (exit_id == "blocked") != (owner["ai_review_gate"]["status"] == "blocked"):
        raise CommandError("schema_mismatch", "owner_result.ai_review_gate", "Bind the gate status to the selected exit.")
    scope_only = profile == "task_scope_requirements"
    if scope_only and exit_id not in {"scope_requirements_ready", "clarify_scope", "blocked"}:
        raise CommandError("schema_mismatch", "owner_result.output", "Task requirements cannot enter Delivery Planning or implementation.")
    if not scope_only and (output.get("delivery_key") != public["delivery_key"] or exit_id == "scope_requirements_ready"):
        raise CommandError("stale_identity", "delivery_key", "Return this exact Delivery's handoff.", 3)
    if profile == "delivery_solution_planning" and exit_id == "requirements_ready":
        raise CommandError("schema_mismatch", "owner_result.output", "A changed candidate re-enters its requirements owner before solution writing.")
    if profile in {"delivery_initial_review", "delivery_active_task_scope_change", "delivery_requirements_revision", "delivery_architecture_conflict_resolution"} and exit_id == "plan_ready":
        raise CommandError("schema_mismatch", "owner_result.output", "This requirements profile hands a real candidate to Architecture before solution writing.")
    task = _task(root.resolve(), public["task_ref"])
    directory = task
    if not scope_only:
        try:
            projection = DeliveryProjection(root, public["task_ref"])
            key = public["delivery_key"]
            delivery = projection.resolve(key)
            current = projection.current(key)
            kind = current.get("kind")
            if kind == "no_current_task":
                raise CommandError("stale_identity", "session.task", "This receiving session has no Task binding. Invoke guru-establish-task-identity, guru-ensure-task-checkout and guru-bind-task-session for the explicit Task, then reread current before Author.", 3)
            if kind == "no_current_delivery":
                raise CommandError("stale_identity", "session.delivery", "This receiving session has no Delivery selection. Invoke guru-create-delivery:delivery_selection for the explicit applicable key, then reread current before Author.", 3)
            if kind == "terminal_delivery":
                raise CommandError("stale_identity", "delivery.phase", "The receiving session selects a terminal Delivery. Return to its original terminal/release owner; do not reopen it through Author.", 3)
            if kind == "error":
                raise CommandError("stale_identity", "current.error", f"Current Delivery query failed ({current['code']}): {current['message']} Return to the original identity/session or installation owner; do not treat this as a missing binding.", 3)
            if kind != "current":
                raise CommandError("stale_identity", "current.kind", "Restore the supported public current query through the installation owner before Author.", 3)
            if current.get("key") != key:
                raise CommandError("stale_identity", "current.key", "The receiving session selects a different Task/Delivery. Resolve that selection through its original owner; do not overwrite it to enter Author.", 3)
            record = projection.read_record()
            if key["lifecycle_generation"] != record["lifecycle_generation"]:
                raise CommandError("stale_identity", "delivery_key.lifecycle_generation", "Resolve the current Task generation through guru-establish-task-identity before Author.", 3)
            if delivery["phase"] != "planning":
                raise CommandError("stale_identity", "delivery.phase", "Return to the actual stage owner for legal rework to planning before Author.", 3)
            if delivery["scope_ref"]["authority"] != record["accepted_scope"]:
                raise CommandError("stale_identity", "delivery.scope_ref.authority", "Refresh the changed whole-Task scope through original Clarify and the current stage's scope-revision owner before Author.", 3)
            projection._call(projection.api.delivery_store.verify_authority, root, delivery["scope_ref"]["authority"])
            directory = projection.planning_directory(key)
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    if exit_id == "scope_requirements_ready":
        if output["requirements_locator"] != f"{public['task_ref']}/prd.md":
            raise CommandError("stale_identity", "requirements_locator", "Use the whole-Task root requirements view.", 3)
        _regular_content(task / "prd.md", "prd.md")
    if exit_id == "requirements_ready":
        _regular_content(directory / "prd.md", "prd.md")
        candidate = output["candidate"]
        if "design_locator" in candidate:
            if candidate["design_locator"] != (directory / "design.md").relative_to(root.resolve()).as_posix():
                raise CommandError("stale_identity", "candidate.design_locator", "Use this Delivery's current design locator.", 3)
            _regular_content(directory / "design.md", "design.md")
    elif exit_id == "plan_ready":
        for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
            _regular_content(directory / name, name, allow_empty=name.endswith(".jsonl"))
            if name.endswith(".jsonl"):
                for line in (directory / name).read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        entry = json.loads(line)
                        if not isinstance(entry, dict) or not entry.get("file") or not entry.get("reason"):
                            raise CommandError("schema_mismatch", name, "Use official task.py add-context entries.")
    suffix = "" if exit_id == "scope_requirements_ready" else "-2.0"
    validate_json(output, package_root / "schemas" / f"public-{exit_id.replace('_', '-')}-output{suffix}.schema.json", "stdout")
    if profile == "delivery_initial_review" and exit_id == "requirements_ready":
        port = package_root.parent / "guru-create-delivery/runtime/creation_result.py"
        spec = importlib.util.spec_from_file_location("guru_author_creation_result_owner", port)
        if spec is None or spec.loader is None:
            raise CommandError("schema_mismatch", "creation_result_owner", "Restore the complete compatible Guru preset.")
        producer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(producer)
        producer.retire_creation_result(root, task_ref=public["task_ref"], delivery_key=public["delivery_key"])
    return output


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args(argv)
    return execute(package_root, Path(args.root), read_json(args.input, "input"), read_json(args.owner_result, "owner_result"))
