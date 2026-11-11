from __future__ import annotations

import argparse
from pathlib import Path

from check import checked_gate
from common import (
    RETIRED_EXITS,
    load,
    parse,
    rel,
    retire_checkpoint,
    root,
    review_input_schema,
    task,
    validate_public_binding,
)
from runtime.io import CommandError
from runtime.schema import validate_json


def _scope_phase(repo, public):
    from runtime.delivery_projection.adapter import DeliveryProjection
    projection = DeliveryProjection(repo, public["task_ref"])
    owners = projection.declaration()["owners"]
    if owners["check"] != "guru-review-branch" or owners["full_review"] != "guru-review-branch":
        raise CommandError("stale_identity", "owners", "Install the matching post-commit Review workflow and package together.", 3)
    phase = projection.resolve(public["delivery_key"])["phase"]
    return "checking" if phase == "checking" else "reviewing"


def _scope_role(repo, public):
    # Both declared roles belong to this same semantic owner. The phase only
    # selects its legal API role, not a semantic owner or a scope decision.
    return "check" if _scope_phase(repo, public) == "checking" else "full_review"


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--task")
    parser.add_argument("--invocation")
    parser.add_argument("--input")
    parser.add_argument("--owner-result")
    args = parse(parser, argv)
    repo = root(package_root, args.root)
    if bool(args.invocation) == bool(args.input):
        raise CommandError(
            "invalid_arguments",
            "invocation",
            "Provide exactly one public input locator or invocation envelope.",
        )
    if args.invocation:
        envelope = load(repo, package_root, args.invocation, "invocation")
        if set(envelope) != {"public_input"} or not isinstance(
            envelope["public_input"], dict
        ):
            raise CommandError(
                "invalid_arguments",
                "invocation",
                "Provide only the public_input invocation member.",
            )
        public = envelope["public_input"]
    else:
        public = load(repo, package_root, args.input, "input")
    if public.get("profile") == "delivery_draft_content_review":
        raise CommandError("schema_mismatch", "profile", "Early Draft content analysis is retired; use the matching current committed Review.")
    if public.get("profile") == "delivery_promotion_reference_alignment":
        from alignment import facts
        facts(package_root, repo, public)
    if public.get("profile") == "legacy_control_retirement":
        from legacy_maintenance import invoke_retirement
        return invoke_retirement(package_root, public, repo)
    if public.get("profile") == "delivery_scope_revision":
        from runtime.delivery_projection.scope_revision import revise
        return revise(repo, package_root, public, load(repo, package_root, args.owner_result, "owner_result"), owner_role=_scope_role(repo, public), expected_phase=_scope_phase(repo, public), output_version="2.0")
    if public.get("profile") == "delivery_scope_withdrawal":
        from runtime.delivery_projection.withdrawal import stop
        semantic = load(repo,package_root,args.owner_result,"owner_result")
        return stop(repo,package_root,public,semantic,owner_role=_scope_role(repo, public),expected_phase=_scope_phase(repo, public), output_version="2.0")
    if public.get("profile") == "delivery_planning_stale_recovery":
        validate_json(public, package_root / "schemas/public-delivery-planning-stale-recovery-input-1.0.schema.json", "input")
    else:
        validate_json(public, package_root / "schemas" / review_input_schema(public), "input")
    task_dir = task(repo, args.task or public.get("task_ref"))
    if public.get("task_ref") != rel(repo, task_dir):
        raise CommandError(
            "stale_identity", "task", "Invoke the exact task-owned checkpoint.", 3
        )
    if str(public.get("profile", "")).startswith("delivery_"):
        from common import checkpoint, load_checkpoint, validate_gate, git, dirty_paths
        from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
        from runtime.delivery_projection.gates import record_gate, rework
        import hashlib, json
        projection = DeliveryProjection(repo, public["task_ref"])
        delivery = projection.resolve(public["delivery_key"])
        if public["profile"] == "delivery_archived_review":
            _path, owner = load_checkpoint(repo, task_dir, public["delivery_key"])
            validate_gate(package_root, repo, owner)
            validate_public_binding(package_root, repo, public, owner)
            if owner["typed_exit"] == "blocked":
                retire_checkpoint(repo, task_dir, public["delivery_key"])
                return {"exit_id": "blocked"}
            if owner["typed_exit"] != "archived_review_passed":
                raise CommandError("stale_identity", "archived_review", "Complete the independent archived content review.", 3)
            output = {"exit_id": "archived_review_passed", "task_ref": owner["task_dir"],
                      "delivery_key": public["delivery_key"], "branch_review_commit": owner["review_commit"],
                      "pr_payload_snapshot_sha256": owner["pr_payload_snapshot_sha256"], "reviewed_base_head": owner["base_head"]}
            validate_json(output, package_root / "schemas/public-output-delivery-archived-review-passed-1.0.schema.json", "stdout")
            retire_checkpoint(repo, task_dir, public["delivery_key"])
            return output
        from runtime.task_lifecycle.active_checkout import resolve_active_task_checkout
        from runtime.task_lifecycle.errors import LifecycleContractError
        try:
            resolve_active_task_checkout(repo, public["task_ref"])
        except LifecycleContractError as exc:
            raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
        from delivery_review import candidate, recover_pass
        recovering_rollback = public.get("profile") == "delivery_planning_stale_recovery"
        if recovering_rollback:
            validate_json(public, package_root / "schemas/public-delivery-planning-stale-recovery-input-1.0.schema.json", "input")
            public = public["original_review_input"]
        if delivery["phase"] != "implementing":
            candidate(projection, public, recovery=recovering_rollback)
        if not checkpoint(repo, task_dir, public["delivery_key"]).exists():
            if public["profile"] not in {"delivery_branch_review", "delivery_promotion_reference_alignment"}:
                raise CommandError("stale_identity", "review_result", "Recover the original owner checkpoint.", 3)
            result_id = recover_pass(projection, public)
            output = {"exit_id": "passed", "task_ref": public["task_ref"], "delivery_key": public["delivery_key"],
                      "branch_review_commit": public["branch_review_commit"], "full_review_result_id": result_id}
            validate_json(output, package_root / "schemas/public-output-delivery-passed-2.0.schema.json", "stdout")
            return output
        _path, owner = load_checkpoint(repo, task_dir, public["delivery_key"])
        validate_gate(package_root, repo, owner)
        validate_public_binding(package_root, repo, public, owner)
        exit_id = owner["typed_exit"]
        output = {"exit_id": exit_id}
        if exit_id != "blocked":
            output.update(task_ref=public["task_ref"], delivery_key=public["delivery_key"])
        if exit_id == "passed":
            from delivery_review import passed
            result_id = passed(projection, public, owner)
            output.update(branch_review_commit=owner["review_commit"], full_review_result_id=result_id)
        elif exit_id == "planning_stale":
            from delivery_review import planning_stale
            output = planning_stale(projection, public, owner)
        elif exit_id == "implementation_required":
            output.update(branch_review_commit=owner["review_commit"], finding_refs=[row["finding_ref"] for row in owner["semantic_review"]["qualified_findings"] if row["status"] == "open"])
            current = projection.resolve(public["delivery_key"])
            if current["phase"] != "implementing":
                role = "check" if current["phase"] == "checking" else "full_review"
                rework(projection, public["delivery_key"], role, "implementation", authority_ref(projection.planning_directory(public["delivery_key"]) / "implement.md", repo), ["check", "full_review", "readiness"])
        elif exit_id == "scope_confirmation_required":
            output["proposal_refs"] = [row["proposal_ref"] for row in owner["semantic_review"]["scope_proposals"]]
        elif exit_id == "continuity_passed":
            output.update(branch_review_commit=owner["review_commit"], **{key: owner["integration_pair"][key] for key in ("task_head", "old_base_head", "new_base_head", "candidate_tree_sha256", "resume_target")})
        elif exit_id == "blocked":
            pass
        else:
            raise CommandError("schema_mismatch", "typed_exit", "Archived legacy review does not produce a Delivery gate.")
        validate_json(output, package_root / "schemas" / ("public-output-delivery-" + exit_id.replace("_", "-") + ("-2.0.schema.json" if exit_id in {"passed", "implementation_required", "scope_confirmation_required", "planning_stale"} else "-1.0.schema.json")), "stdout")
        if exit_id in RETIRED_EXITS:
            retire_checkpoint(repo, task_dir, public["delivery_key"])
        return output
    owner = checked_gate(package_root, repo, task_dir)
    validate_public_binding(package_root, repo, public, owner)
    exit_id = owner["typed_exit"]
    if exit_id == "archived_review_passed":
        output = {
            "exit_id": exit_id,
            "task_ref": owner["task_dir"],
            "branch_review_commit": owner["review_commit"],
            "pr_payload_snapshot_sha256": owner["pr_payload_snapshot_sha256"],
            "reviewed_base_head": owner["base_head"],
        }
        schema = "public-archived-review-passed-output.schema.json"
    elif exit_id == "blocked":
        output = {"exit_id": "blocked"}
        schema = "public-blocked-output.schema.json"
    else:
        raise CommandError(
            "schema_mismatch", "typed_exit", "Return one declared typed exit."
        )
    validate_json(output, package_root / "schemas" / schema, "stdout")
    if exit_id in RETIRED_EXITS:
        retire_checkpoint(repo, task_dir)
    return output
