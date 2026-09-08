from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import copy
import importlib.util
import json
import subprocess
import sys

from adapters.eval.fixture_io import (
    run_git,
)


def load_package_owner_runtime(runtime_target: Path, skill_id: str) -> Any:
    runtime_path = (
        runtime_target.parent.parent.parent
        / "skills/packages"
        / skill_id
        / "runtime/owner.py"
    )
    if not runtime_path.is_file():
        module = load_package_runtime_module(runtime_target, skill_id, "common")
        if skill_id == "guru-clarify-requirements":
            module.context_digest = module.digest
            module.derive_requirements_clarification_result = (
                lambda payload: derive_clarification_eval_result(module, payload)
            )
        elif skill_id == "guru-review-change-request":
            compose_change_request_eval_runtime(runtime_target, module)
        elif skill_id == "guru-create-task-workspace":
            compose_task_workspace_eval_runtime(runtime_target, module)
        elif skill_id == "guru-review-branch":
            compose_review_branch_eval_runtime(runtime_target, module)
        return module
    if runtime_path.is_symlink():
        raise ValueError("package owner staging runtime is unavailable")
    spec = importlib.util.spec_from_file_location(
        f"guru_team_eval_{skill_id.replace('-', '_')}_owner", runtime_path
    )
    if spec is None or spec.loader is None:
        raise ValueError("package owner staging runtime cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module

def compose_change_request_eval_runtime(runtime_target: Path, module: Any) -> None:
    review = load_package_runtime_module(
        runtime_target, "guru-review-change-request", "common"
    )
    clarity = load_package_runtime_module(
        runtime_target, "guru-clarify-requirements", "common"
    )
    wording = load_package_runtime_module(
        runtime_target, "guru-review-contract-wording", "common"
    )
    module.context_digest = review.digest
    module.CHANGE_REQUEST_REVIEW_DIMENSIONS = review.DIMENSIONS
    module.CHANGE_REQUEST_REVIEW_CONSUMERS = review.CONSUMERS
    module.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT = review.GATES
    module.CONTRACT_WORDING_REVIEW_DIMENSIONS = wording.CONTRACT_WORDING_REVIEW_DIMENSIONS
    module.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS = (
        wording.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
    )
    module.derive_requirements_clarification_result = (
        lambda payload: derive_clarification_eval_result(clarity, payload)
    )
    module.contract_wording_build_scope = wording.contract_wording_build_scope
    module.scan_contract_wording = wording.scan_contract_wording
    module.contract_wording_derive_result = wording.contract_wording_derive_result

    def issue_view(repo: str, number: int, root: Path) -> dict[str, Any]:
        process = subprocess.run(
            ["gh", "issue", "view", str(number), "--repo", repo, "--json",
             "number,url,state,title,body,updatedAt"],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode != 0:
            raise ValueError("change-request eval issue authority is unavailable")
        value = json.loads(process.stdout)
        if not isinstance(value, dict):
            raise ValueError("change-request eval issue authority is invalid")
        return value

    def scope_hashes(scope: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
        values = {
            item.get("field"): item.get("content_sha256")
            for item in scope.get("items", []) if isinstance(item, dict)
        }
        title, body = values.get("title"), values.get("body")
        return title, body, review.digest({"title_sha256": title, "body_sha256": body}) if title and body else None

    def authority_projection(repo: Any, source: Any, body_sha256: Any) -> dict[str, Any] | None:
        if not isinstance(repo, str) or not isinstance(source, dict) or source.get("kind") != "draft":
            return None
        return {"kind": "draft", "repo": repo, "issue_number": None, "url": None,
                "state": "draft", "updated_at": None, "body_sha256": body_sha256}

    def normalize_target(root: Path, raw: Any, source_path: str, mode: str):
        source = review.load(root, root, source_path, "change_request")
        if source.get("kind") == "issue":
            live = issue_view(
                str(source.get("repo") or ""), int(source.get("number") or 0), root
            )
            source = {
                **source,
                "title": live.get("title"),
                "body": live.get("body"),
                "updated_at": live.get("updatedAt"),
            }
        scope, contents = wording.contract_wording_build_scope(
            root, "change_request", mode, change_request_input=source_path
        )
        return review.normalize_target(source, raw), scope, contents

    module.issue_view = issue_view
    module.change_request_review_scope_hashes = scope_hashes
    module.change_request_review_request_authority_projection = authority_projection
    module.change_request_review_normalize_target = normalize_target
    module.readiness_runtime = review

def compose_review_branch_eval_runtime(runtime_target: Path, module: Any) -> None:
    publication = load_package_owner_runtime(
        runtime_target, "guru-review-task-publication"
    )
    module.load_config = publication.load_config
    module.WorkflowError = publication.WorkflowError
    module.read_json = publication.read_json
    module.write_json = publication.write_json
    module.write_runtime_mappings = publication.write_runtime_mappings
    module.current_head = publication.current_head
    module.git_status_paths = publication.git_status_paths
    module.diff_base_ref = publication.diff_base_ref
    module.INDEPENDENT_REVIEW_SOURCE = "independent-agent"

    def changed_files(root: Path, diff_range: str) -> list[str]:
        output = subprocess.run(
            ["git", "diff", "--name-only", "-z", diff_range],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.decode("utf-8")
        return [path for path in output.split("\0") if path]

    module.changed_files = changed_files

    def commit_review_fixture(
        fixture: Path, task: Path, checked: dict[str, Any]
    ) -> tuple[str, str]:
        del checked
        run_git(fixture, "add", "-A")
        run_git(fixture, "commit", "-q", "-m", "commit reviewed production fixture")
        phase2 = (
            fixture
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / task.name
            / "phase2-check.json"
        )
        phase2.unlink(missing_ok=True)
        return run_git(fixture, "rev-parse", "HEAD"), "origin/main"

    module.commit_review_fixture = commit_review_fixture
    compose_production_owner_command_runtime(runtime_target, module)

def compose_production_owner_command_runtime(
    runtime_target: Path, module: Any,
) -> None:
    package_root = runtime_target.parent.parent.parent / "skills/packages"

    def run_component(skill_id: str, script: str, argv: list[str]) -> dict[str, Any]:
        process = subprocess.run(
            [str(package_root / skill_id / "scripts" / script), *argv, "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode != 0:
            raise ValueError(process.stderr.strip() or process.stdout.strip())
        value = json.loads(process.stdout)
        if not isinstance(value, dict):
            raise ValueError("package wrapper did not return one JSON object")
        return value

    bindings = {
        "cmd_record_planning_approval": lambda args: run_component(
            "guru-approve-task-plan",
            "record-planning-approval.sh",
            ["--root", str(args.root), "--task", str(args.task), "--input", str(args.input)],
        ),
        "cmd_check_planning_approval": lambda args: run_component(
            "guru-approve-task-plan",
            "check-planning-approval.sh",
            ["--root", str(args.root), "--task", str(args.task)],
        ),
        "cmd_record_phase2_check": lambda args: run_component(
            "guru-check-task",
            "record-phase2-check.sh",
            ["--root", str(args.root), "--task", str(args.task), "--input", str(args.input)],
        ),
        "cmd_check_phase2_check": lambda args: run_component(
            "guru-check-task",
            "check-phase2-check.sh",
            ["--root", str(args.root), "--task", str(args.task)],
        ),
        "cmd_review_branch": lambda args: run_component(
            "guru-review-branch",
            "review-branch.sh",
            [
                "--root", str(args.root), "--task", str(args.task),
                "--skill-input", str(args.skill_input),
                "--semantic-review-file", str(args.semantic_review_file),
                "--typed-exit", str(args.typed_exit),
            ],
        ),
        "cmd_check_review_gate": lambda args: run_component(
            "guru-review-branch",
            "check-review-gate.sh",
            [
                "--root", str(args.root), "--task", str(args.task),
                "--expected-exit", str(args.expected_exit),
            ],
        ),
    }
    for name, binding in bindings.items():
        if not hasattr(module, name):
            setattr(module, name, binding)

def compose_production_fixture_runtime(runtime_target: Path, module: Any) -> None:
    helper_names = ("load_config", "write_json", "write_runtime_mappings")
    missing = [name for name in helper_names if not hasattr(module, name)]
    if not missing:
        return
    publication = load_package_owner_runtime(
        runtime_target, "guru-review-task-publication"
    )
    for name in missing:
        setattr(module, name, getattr(publication, name))

def compose_task_workspace_eval_runtime(runtime_target: Path, module: Any) -> None:
    compose_change_request_eval_runtime(runtime_target, module)
    record = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "record"
    )
    execute = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "execute"
    )
    check = load_package_runtime_module(
        runtime_target, "guru-create-task-workspace", "check"
    )
    package_root = (
        runtime_target.parent.parent.parent
        / "skills/packages/guru-create-task-workspace"
    )
    module.context_digest = module.digest
    module.TASK_WORKSPACE_ARTIFACT_NAMES = ("issue-scope-ledger.json",)
    module.task_workspace_reviewable_projection = module.reviewable
    module.task_workspace_plan_digest = module.plan_digest

    def scope_digest(value: dict[str, Any]) -> str:
        projection = copy.deepcopy(value)
        projection.pop("scope_sha256", None)
        return module.digest(projection)

    def prerequisite_projection(
        key: str, artifact: str, payload: dict[str, Any], payload_sha256: str
    ) -> dict[str, Any]:
        identities = {
            "base": ("guru-sync-base", "guru-base-sync-result-1.0", "synced"),
            "clarity": ("guru-clarify-requirements", "guru-requirements-clarification-2.0", "clear"),
            "wording": ("guru-review-contract-wording", "guru-contract-wording-review-1.0", "pass"),
            "readiness": ("guru-review-change-request", "guru-change-request-review-2.0", "ready"),
        }
        skill_id, schema_id, typed_exit = identities[key]
        if key == "base":
            facts, content, linkage = payload.get("facts_sha256"), None, None
        elif key == "clarity":
            identity = payload.get("content_identity", {})
            facts, content, linkage = identity.get("result_sha256"), identity.get("content_sha256"), identity.get("context_sha256")
        elif key == "wording":
            facts = payload.get("facts_sha256")
            content = payload.get("scope", {}).get("scope_sha256")
            linkage = payload.get("scan", {}).get("scan_sha256")
        else:
            facts = payload.get("facts_sha256")
            content = payload.get("target", {}).get("content_sha256")
            linkage = payload.get("evidence_linkage", {}).get("linkage_sha256")
        return {"skill_id": skill_id, "schema_id": schema_id, "typed_exit": typed_exit,
                "artifact": artifact, "payload_sha256": payload_sha256,
                "facts_sha256": facts, "content_sha256": content,
                "linkage_sha256": linkage}

    def invoke(component: Any, args: argparse.Namespace) -> dict[str, Any]:
        argv = ["--root", str(args.root), "--invocation", "-"]
        return component.run(package_root, {}, argv)

    module.task_workspace_scope_digest = scope_digest
    module.task_workspace_prerequisite_projection = prerequisite_projection
    module.cmd_record_task_workspace_plan = lambda args: invoke(record, args)
    module.cmd_create_task_workspace = lambda args: invoke(execute, args)
    module.cmd_check_task_workspace_result = lambda args: invoke(check, args)

def derive_clarification_eval_result(runtime: Any, payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["schema_version"] = "2.0"
    result["skill_id"] = "guru-clarify-requirements"
    actions = result.get("source_actions")
    actions = actions if isinstance(actions, list) else []
    for action in actions:
        if not isinstance(action, dict):
            continue
        action["payload_sha256"] = (
            runtime.digest(action["payload"])
            if isinstance(action.get("payload"), dict)
            else None
        )
        action["action_digest"] = runtime.digest({
            key: copy.deepcopy(action.get(key))
            for key in (
                "action_id", "kind", "target", "payload", "preimage_sha256",
                "payload_sha256",
            )
        })
    unsigned = copy.deepcopy(result)
    unsigned.pop("content_identity", None)
    content = {
        "confirmed_facts": result.get("confirmed_facts"),
        "repository_answerable_questions": result.get("repository_answerable_questions"),
        "clarification_rounds": result.get("clarification_rounds"),
        "open_questions": result.get("open_questions"),
        "affected_contracts": result.get("affected_contracts"),
        "reason": result.get("reason"),
    }
    result["content_identity"] = {
        "target_sha256": runtime.digest(result.get("review_target")),
        "disposition_sha256": runtime.digest(result.get("target_disposition")),
        "content_sha256": runtime.digest(content),
        "context_sha256": runtime.digest(result.get("context_evidence")),
        "scope_sha256": runtime.digest(result.get("scope_proposals")),
        "action_sha256": runtime.digest(actions),
        "payload_sha256": runtime.digest([
            action.get("payload") if isinstance(action, dict) else None
            for action in actions
        ]),
        "result_sha256": runtime.digest(unsigned),
    }
    return result

def load_package_runtime_module(
    runtime_target: Path, skill_id: str, module_name: str,
) -> Any:
    runtime_path = (
        runtime_target.parent.parent.parent
        / "skills/packages"
        / skill_id
        / "runtime"
        / f"{module_name}.py"
    )
    if runtime_path.is_symlink() or not runtime_path.is_file():
        raise ValueError(f"package {module_name} runtime is unavailable")
    spec = importlib.util.spec_from_file_location(
        f"guru_team_eval_{skill_id.replace('-', '_')}_{module_name}", runtime_path
    )
    if spec is None or spec.loader is None:
        raise ValueError(f"package {module_name} runtime cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    previous_path = list(sys.path)
    previous = sys.dont_write_bytecode
    sys.path.insert(0, str(runtime_path.parent))
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous_path
        sys.dont_write_bytecode = previous
    return module
