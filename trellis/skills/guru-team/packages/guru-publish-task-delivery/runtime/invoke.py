from __future__ import annotations

from pathlib import Path
from typing import Any

from owner import _public_command, invoke, parser, repo_root
from runtime.io import read_json


@_public_command
def run(package_root: Path, command: dict[str, Any], argv: list[str]) -> dict[str, Any]:
    # Inspect only the profile before loading the separate legacy owner. Normal
    # current calls keep their original runtime dependencies and preconditions.
    import argparse as _argparse
    _selector=_argparse.ArgumentParser(add_help=False);_selector.add_argument('--input')
    _selected,_rest=_selector.parse_known_args(argv)
    if _selected.input is not None:
        _public=read_json(_selected.input,'input')
        if _public.get('profile') in {'legacy_control_retirement','legacy_history_verification'}:
            import importlib.util as _util
            _spec=_util.spec_from_file_location('legacy_'+package_root.name.replace('-','_'),package_root/'runtime/legacy_maintenance.py')
            _owner=_util.module_from_spec(_spec);_spec.loader.exec_module(_owner)
            return _owner.maybe_run(package_root,argv,public=_public)
    del command
    args = parser("invoke").parse_args(argv)
    public = _public
    from current import EXECUTE, PREPARE, execute, prepare, recover
    from owner import WorkflowError
    from runtime.delivery_projection.adapter import DeliveryProjection
    from runtime.task_lifecycle import LifecycleContractError

    root = repo_root(Path(args.root or "."))
    profile = public.get("profile")
    try:
        if profile in {PREPARE, EXECUTE} and not args.review_input:
            raise WorkflowError("Supply the AI-authored review for this invocation.", code="schema_mismatch")
        if profile == PREPARE:
            return prepare(package_root, root, public, read_json(args.review_input, "review_input"))
        if profile == EXECUTE:
            return execute(package_root, root, public, read_json(args.review_input, "review_input"),
                           args.confirmed_preview_sha256)
        if profile in {"delivery_same_plan_resume", "delivery_reprepare_publication"}:
            from owner import validate_public_input
            return recover(root, validate_public_input(public))
        if profile in {"delivery_scope_revision", "delivery_scope_withdrawal"}:
            phase = DeliveryProjection(root, public["task_ref"]).resolve(public["delivery_key"])["phase"]
            expected_phase = "reviewing" if phase == "reviewing" else "publishing"
            role = "readiness" if expected_phase == "reviewing" else "publication"
            # Each projector checks its exact terminal result before returning
            # it. A terminal phase alone never authorizes another transition.
            recovery_phase = "planning" if profile == "delivery_scope_revision" else "stopped"
            if phase not in {"reviewing", "publishing", recovery_phase}:
                raise WorkflowError("Resume the original current scope owner.", code="publication_stale")
            review = read_json(args.review_input, "review_input")
            if profile == "delivery_scope_revision":
                from runtime.delivery_projection.scope_revision import revise
                return revise(root, package_root, public, review, owner_role=role, expected_phase=expected_phase)
            from runtime.delivery_projection.withdrawal import stop
            return stop(root, package_root, public, review, owner_role=role, expected_phase=expected_phase)
        if profile in {"delivery_remote_draft_recovery", "delivery_remote_ready_recovery", "delivery_return_to_draft"}:
            if profile.startswith("delivery_remote_"):
                from owner import validate_public_input
                from current import _selection, merged
                validate_public_input(public)
                _, delivery, _ = _selection(root, public)
                output = merged(root, public, delivery, selected_pr=public["pr_ref"])
                if output:
                    return output
            return invoke(root, public, read_json(args.review_input, "review_input"), args.confirmed_preview_sha256)
    except LifecycleContractError as exc:
        raise WorkflowError(exc.remediation, code="task_identity_stale", field_path=exc.field_path) from exc
    raise WorkflowError("Use the current Publication preparation and execution profiles. See MIGRATION-900.",
                        code="schema_mismatch")
