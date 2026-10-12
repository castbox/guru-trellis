from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import branch_checked_out_paths, inspect_repository
from runtime.task_lifecycle.identity import normalize_task_ref, resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


PROFILES = {
    "initial_review", "active_task_scope_change", "wording_reentry",
    "approval_revision", "delivery_plan_revision", "requirements_revision",
    "solution_planning", "architecture_conflict_resolution",
}


def _task(root: Path, task_ref: str) -> Path:
    try:
        normalize_task_ref(task_ref)
        path = root / task_ref
        metadata = read_json(str(path / "task.json"), "task_ref")
        identity = resolve_task_id(root, metadata["id"])
        if identity.task_ref != task_ref or metadata["status"] not in {"planning", "in_progress"}:
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
    except (LifecycleContractError, KeyError, OSError) as exc:
        raise CommandError("stale_identity", "task_ref", "Resolve the current TaskId and checkout through their original owners.", 3) from exc


def _regular_content(path: Path, label: str) -> None:
    if not path.is_file() or path.is_symlink() or not path.read_text(encoding="utf-8").strip():
        raise CommandError("stale_identity", label, "Complete the current regular planning file before invoking its handoff.", 3)


def execute(package_root: Path, root: Path, public: dict, owner: dict) -> dict:
    profile = public.get("profile")
    if profile not in PROFILES:
        raise CommandError("schema_mismatch", "input.profile", "Use one of the eight closed Author profiles.")
    validate_json(public, package_root / "schemas" / f"public-{profile.replace('_', '-')}-input.schema.json", "input")
    validate_json(owner, package_root / "schemas/semantic-result.schema.json", "owner_result")
    if owner["public_input"] != public or owner["output"]["task_ref"] != public["task_ref"]:
        raise CommandError("stale_identity", "owner_result", "Repeat this owner review against the exact current input.", 3)
    output = owner["output"]
    exit_id = output["exit_id"]
    if (exit_id == "blocked") != (owner["ai_review_gate"]["status"] == "blocked"):
        raise CommandError("schema_mismatch", "owner_result.ai_review_gate", "Bind the gate status to the selected exit.")
    if profile == "solution_planning" and exit_id == "requirements_ready":
        raise CommandError("schema_mismatch", "owner_result.output", "A changed candidate re-enters its requirements owner before solution writing.")
    if profile in {"initial_review", "active_task_scope_change", "requirements_revision", "architecture_conflict_resolution"} and exit_id == "plan_ready":
        raise CommandError("schema_mismatch", "owner_result.output", "This requirements profile hands a real candidate to Architecture before solution writing.")
    task = _task(root.resolve(), public["task_ref"])
    if exit_id == "requirements_ready":
        _regular_content(task / "prd.md", "prd.md")
        candidate = output["candidate"]
        if "design_locator" in candidate:
            if candidate["design_locator"] != f"{public['task_ref']}/design.md":
                raise CommandError("stale_identity", "candidate.design_locator", "Use this task's current design locator.", 3)
            _regular_content(task / "design.md", "design.md")
    elif exit_id == "plan_ready":
        for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
            _regular_content(task / name, name)
            if name.endswith(".jsonl"):
                for line in (task / name).read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        entry = json.loads(line)
                        if not isinstance(entry, dict) or not entry.get("file") or not entry.get("reason"):
                            raise CommandError("schema_mismatch", name, "Use official task.py add-context entries.")
    validate_json(output, package_root / "schemas" / f"public-{exit_id.replace('_', '-')}-output.schema.json", "stdout")
    return output


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    args = parser.parse_args(argv)
    return execute(package_root, Path(args.root), read_json(args.input, "input"), read_json(args.owner_result, "owner_result"))
