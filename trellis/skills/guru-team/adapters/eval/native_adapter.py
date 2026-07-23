#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


ADAPTERS = ("shared", "codex", "claude", "cursor")

OWNER_INPUT = ".trellis/.runtime/guru-team/evals/public-input.json"
OWNER_RESULT = ".trellis/.runtime/guru-team/evals/owner-result.json"
OWNER_PLAN = ".trellis/.runtime/guru-team/evals/owner-plan.json"
PRODUCTION_SKILLS = {
    "guru-approve-task-plan",
    "guru-check-task",
    "guru-create-task-commit",
    "guru-review-branch",
}

TRACE_HELPER = r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stdout_digest(value: str) -> str:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        normalized = value.strip()
    else:
        normalized = json.dumps(payload, separators=(",", ":"))
    return digest(normalized.encode("utf-8"))


def append_event(
    trace_path: Path,
    request_sha256: str,
    projection_root: str,
    skill_sha256: str,
    wrapper_sha256: str,
    event: dict[str, object],
) -> None:
    if trace_path.exists():
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    else:
        payload = {
            "schema_version": "1.0",
            "request_sha256": request_sha256,
            "projection_root": projection_root,
            "skill_sha256": skill_sha256,
            "wrapper_sha256": wrapper_sha256,
            "events": [],
        }
    if (
        payload.get("request_sha256") != request_sha256
        or payload.get("projection_root") != projection_root
        or payload.get("skill_sha256") != skill_sha256
        or payload.get("wrapper_sha256") != wrapper_sha256
        or not isinstance(payload.get("events"), list)
    ):
        raise ValueError("native trace request binding mismatch")
    event["request_sha256"] = request_sha256
    payload["events"].append(event)
    trace_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--projection-root", required=True)
    parser.add_argument("--skill-sha256", required=True)
    parser.add_argument("--wrapper-sha256", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("--kind", required=True, choices=("skill_contract", "case_file"))
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--wrapper", required=True)
    invoke_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    trace_path = Path(args.trace).resolve()
    if args.operation == "read":
        target = Path(args.path).resolve()
        content = target.read_bytes()
        append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
            "kind": "read", "target_kind": args.kind, "path": str(target), "sha256": digest(content),
        })
        sys.stdout.buffer.write(content)
        return 0
    wrapper = Path(args.wrapper).resolve()
    forwarded = list(args.arguments)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]
    process = subprocess.run(
        [str(wrapper), *forwarded], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
        "kind": "invoke", "wrapper_path": str(wrapper), "argv": [str(wrapper), *forwarded],
        "returncode": process.returncode, "stdout_sha256": stdout_digest(process.stdout),
        "stderr_sha256": digest(process.stderr.encode("utf-8")),
    })
    sys.stdout.write(process.stdout)
    sys.stderr.write(process.stderr)
    return process.returncode


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
'''


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, separators=(",", ":")))
    return 0


def response(
    request: dict[str, Any],
    status: str,
    transcript: Path,
    *,
    stdout: str = "",
    stderr: str = "",
    trace_events: list[str] | None = None,
    timing_ms: int = 0,
    native_trace: Path | None = None,
) -> dict[str, Any]:
    try:
        corpus_sha256 = hashlib.sha256(Path(request["corpus_path"]).read_bytes()).hexdigest()
    except (KeyError, OSError, TypeError):
        corpus_sha256 = str(request.get("corpus_sha256") or "0" * 64)
    return {
        "schema_version": "1.0",
        "capability_status": status,
        "corpus_sha256": corpus_sha256,
        "public_stdout": stdout,
        "public_stderr": stderr,
        "trace_events": trace_events or [],
        "transcript_locator": str(transcript),
        "native_trace_locator": str(native_trace or transcript.with_name("native-trace.json")),
        "timing_ms": timing_ms,
    }


def public_projection_assets(interface: dict[str, Any]) -> set[Path]:
    assets = {Path("SKILL.md"), Path("interface.json")}
    contracts = interface.get("public_contracts")
    if not isinstance(contracts, dict):
        raise ValueError("public Interface contracts are unavailable")

    def add_reference(reference: Any) -> None:
        if not isinstance(reference, dict):
            return
        value = reference.get("path")
        if not isinstance(value, str):
            return
        relative = Path(value)
        if relative.is_absolute() or not relative.parts or ".." in relative.parts:
            raise ValueError("public Interface contains an unsafe asset path")
        assets.add(relative)

    public_input = contracts.get("input")
    if isinstance(public_input, dict):
        add_reference(public_input.get("aggregate_schema"))
        for profile in public_input.get("profiles", []):
            if isinstance(profile, dict):
                add_reference(profile.get("schema"))
                add_reference(profile.get("example"))
    invocation = contracts.get("invocation")
    if not isinstance(invocation, dict):
        raise ValueError("public invocation contract is unavailable")
    wrapper = invocation.get("wrapper")
    if not isinstance(wrapper, str):
        raise ValueError("public wrapper locator is unavailable")
    wrapper_path = Path(wrapper)
    if wrapper_path.is_absolute() or not wrapper_path.parts or ".." in wrapper_path.parts:
        raise ValueError("public wrapper locator is unsafe")
    assets.add(wrapper_path)
    add_reference(invocation.get("error_schema"))
    add_reference(invocation.get("error_example"))
    for output in contracts.get("outputs", []):
        if isinstance(output, dict):
            add_reference(output.get("schema"))
            add_reference(output.get("example"))
    return assets


def stage_public_projection(request: dict[str, Any], execution_root: Path) -> tuple[Path, Path, Path, str, str]:
    canonical_root = Path(request["package_root"]).resolve()
    interface = json.loads((canonical_root / "interface.json").read_text(encoding="utf-8"))
    if not isinstance(interface, dict) or interface.get("id") != request.get("skill_id"):
        raise ValueError("exact public Interface identity is unavailable")
    projection_root = execution_root / "public-packages" / str(request["skill_id"])
    projection_root.mkdir(parents=True, exist_ok=False)
    for relative in sorted(public_projection_assets(interface), key=lambda item: item.as_posix()):
        source = canonical_root / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"public projection asset is unavailable: {relative.as_posix()}")
        destination = projection_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    if (projection_root / "evals").exists() or any(path.name == "guru_team_trellis.py" for path in projection_root.rglob("*")):
        raise ValueError("public projection contains eval or private runtime assets")
    local_invocation = interface.get("public_contracts", {}).get("invocation")
    request_interface = request.get("interface")
    request_invocation = request_interface.get("public_invocation") if isinstance(request_interface, dict) else None
    if not isinstance(local_invocation, dict) or request_invocation != local_invocation:
        raise ValueError("side-local public invocation contract does not match exact package Interface")
    wrapper_relative = local_invocation["wrapper"]
    wrapper_path = projection_root / wrapper_relative
    skill_path = projection_root / "SKILL.md"
    skill_sha256 = hashlib.sha256(skill_path.read_bytes()).hexdigest()
    wrapper_sha256 = hashlib.sha256(wrapper_path.read_bytes()).hexdigest()
    if skill_sha256 != hashlib.sha256((canonical_root / "SKILL.md").read_bytes()).hexdigest():
        raise ValueError("public projection Skill bytes differ from canonical bytes")
    if wrapper_sha256 != hashlib.sha256((canonical_root / wrapper_relative).read_bytes()).hexdigest():
        raise ValueError("public projection wrapper bytes differ from canonical bytes")
    return projection_root, skill_path, wrapper_path, skill_sha256, wrapper_sha256


def public_runtime_target(request: dict[str, Any]) -> Path:
    target = request.get("runtime_target")
    if not isinstance(target, str) or not target:
        raise ValueError("public invocation runtime boundary is unavailable")
    candidate = Path(target)
    if not candidate.is_absolute() or candidate.is_symlink():
        raise ValueError("public invocation runtime boundary target is unsafe")
    resolved = Path(os.path.abspath(candidate))
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise ValueError("public invocation runtime boundary target is unavailable")
    return resolved


def load_owner_runtime(runtime_target: Path) -> Any:
    runtime_path = runtime_target.parent.parent / "python" / "guru_team_trellis.py"
    if runtime_path.is_symlink() or not runtime_path.is_file():
        raise ValueError("owner staging runtime is unavailable")
    spec = importlib.util.spec_from_file_location("guru_team_eval_owner_runtime", runtime_path)
    if spec is None or spec.loader is None:
        raise ValueError("owner staging runtime cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def run_git(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=root, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        raise ValueError(f"owner staging git command failed: {' '.join(arguments)}")
    return process.stdout.strip()


def owner_recipe(request: dict[str, Any]) -> tuple[str, Path]:
    workdir = Path(request["workdir"]).resolve()
    recipe: str | None = None
    public_input: Path | None = None
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        staging = payload.get("owner_staging")
        if isinstance(staging, dict):
            candidate = staging.get("recipe")
            if not isinstance(candidate, str) or not candidate:
                raise ValueError("owner staging recipe is invalid")
            if recipe is not None:
                raise ValueError("multiple case files declare owner staging recipes")
            recipe = candidate
        if payload.get("profile") and payload.get("mode"):
            if public_input is not None:
                raise ValueError("multiple case files declare public inputs")
            public_input = path
    if recipe is None or public_input is None:
        raise ValueError("semantic case does not declare one owner staging recipe and public input")
    return recipe, public_input


def stage_clean_installed_owner_repo(
    execution_root: Path, runtime_target: Path, request_package: Path,
) -> tuple[Path, Path]:
    fixture = execution_root / "owner-repo"
    source_repo = runtime_target.parents[4]
    source_scripts = source_repo / ".trellis/scripts"
    source_workflow = source_repo / ".trellis/workflow.md"
    apply_script = source_repo / "trellis/presets/guru-team/scripts/bash/apply.sh"
    if (
        source_scripts.is_symlink() or not source_scripts.is_dir()
        or source_workflow.is_symlink() or not source_workflow.is_file()
    ):
        raise ValueError("installed Trellis inputs are unavailable for owner staging")
    (fixture / ".trellis").mkdir(parents=True)
    shutil.copytree(
        source_scripts, fixture / ".trellis/scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copy2(source_workflow, fixture / ".trellis/workflow.md")
    (fixture / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
    run_git(fixture, "init", "-q", "-b", "main")
    run_git(fixture, "config", "user.email", "stage0-eval@example.invalid")
    run_git(fixture, "config", "user.name", "Stage0 Eval")
    canonical_packages = source_repo / "trellis/skills/guru-team/packages"
    try:
        request_package.relative_to(canonical_packages)
        source_mode = True
    except ValueError:
        source_mode = False
    if source_mode:
        if apply_script.is_symlink() or not os.access(apply_script, os.X_OK):
            raise ValueError("canonical preset inputs are unavailable for owner staging")
        canonical_workflow = source_repo / "trellis/workflows/guru-team/workflow.md"
        if canonical_workflow.is_symlink() or not canonical_workflow.is_file():
            raise ValueError("canonical workflow input is unavailable for owner staging")
        shutil.copy2(canonical_workflow, fixture / ".trellis/workflow.md")
        applied = subprocess.run(
            [str(apply_script), "--repo", str(fixture), "--all-platforms"],
            cwd=source_repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if applied.returncode != 0:
            raise ValueError("canonical preset apply failed during owner staging")
    else:
        installed_root = source_repo / ".trellis/guru-team"
        extension_path = installed_root / "extension.json"
        try:
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            skill_packages = extension["skill_packages"]
            files = skill_packages["files"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("installed Skill package provenance is unavailable") from exc
        if (
            not isinstance(skill_packages, dict)
            or skill_packages.get("status") != "ok"
            or skill_packages.get("conflicts") != []
            or skill_packages.get("sidecars") != []
            or not isinstance(files, list)
            or installed_root.is_symlink() or not installed_root.is_dir()
        ):
            raise ValueError("installed Skill package provenance is not reusable")
        shutil.copytree(
            installed_root, fixture / ".trellis/guru-team", dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        for row in files:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                raise ValueError("installed Skill file provenance is invalid")
            relative = Path(row["path"])
            if relative.is_absolute() or not relative.parts or ".." in relative.parts:
                raise ValueError("installed Skill file provenance path is unsafe")
            source = source_repo / relative
            target = fixture / relative
            expected_sha256 = row.get("sha256")
            if (
                source.is_symlink() or not source.is_file()
                or not isinstance(expected_sha256, str)
                or hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha256
            ):
                raise ValueError("installed Skill file provenance does not match live bytes")
            if relative.parts[:3] == (".trellis", "guru-team", "skills"):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return fixture, source_repo


def write_fake_gh(execution_root: Path, recipe: str) -> Path:
    binary = execution_root / "owner-bin"
    binary.mkdir(parents=True, exist_ok=True)
    target = binary / "gh"
    issue_145_state = "CLOSED" if recipe == "clarity-new-task" else "OPEN"
    workspace_recipe = recipe.startswith("workspace-")
    issue_title = (
        "Stage 0 workspace owner staging"
        if workspace_recipe else "Issue 145 owner staging"
    )
    issue_body = (
        "The Stage 0 migration is one independently deliverable unit."
        if workspace_recipe else "Issue 145 owner staging body"
    )
    issue_assignees = [{"login": "stage0-eval"}] if workspace_recipe else []
    target.write_text(
        "#!/usr/bin/env python3\n"
        "import json,sys\n"
        f"states={{145:{issue_145_state!r},146:'OPEN'}}\n"
        f"titles={{145:{issue_title!r},146:'Issue 146 owner staging'}}\n"
        f"bodies={{145:{issue_body!r},146:'Issue 146 owner staging body'}}\n"
        f"assignees={{145:{issue_assignees!r},146:[]}}\n"
        "args=sys.argv[1:]\n"
        "if args[:2]==['auth','status']:\n"
        " raise SystemExit(0)\n"
        "if args[:2]==['api','user']:\n"
        " print(json.dumps({'login':'stage0-eval'})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " number=int(args[2]); state=states.get(number,'OPEN')\n"
        " title=titles.get(number,f'Issue {number} owner staging'); body=bodies.get(number,f'Issue {number} owner staging body')\n"
        " print(json.dumps({'number':number,'url':f'https://github.com/example/guru-extension/issues/{number}',"
        "'state':state,'updatedAt':'2026-01-01T00:00:00Z','title':title,'body':body,"
        "'comments':[],'assignees':assignees.get(number,[]),'labels':[]}))\n"
        " raise SystemExit(0)\n"
        "print('unsupported fake gh invocation',file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    target.chmod(0o755)
    real_git = shutil.which("git")
    if real_git is None:
        raise ValueError("git is unavailable for owner staging")
    git_target = binary / "git"
    git_target.write_text(
        "#!/usr/bin/env python3\n"
        "import os,sys\n"
        f"real_git={real_git!r}\n"
        "args=sys.argv[1:]\n"
        "if args and args[0]=='fetch': raise SystemExit(0)\n"
        "os.execv(real_git,[real_git,*args])\n",
        encoding="utf-8",
    )
    git_target.chmod(0o755)
    return binary


def clarity_target(
    runtime: Any,
    payload: dict[str, Any],
    *,
    state: str = "open",
    body: str = "Issue 145 owner staging body",
) -> dict[str, Any]:
    target = {
        "kind": "issue", "repo": "example/guru-extension", "issue_number": 145,
        "url": "https://github.com/example/guru-extension/issues/145", "state": state,
        "updated_at": "2026-01-01T00:00:00Z",
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    target["facts_sha256"] = runtime.context_digest(target)
    payload["invocation_context"] = {
        "kind": "initial_issue", "caller": "stage0 eval owner staging",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    payload["review_target"] = target
    return payload


def clarity_disposition(
    runtime: Any,
    payload: dict[str, Any],
    disposition: str,
    *,
    candidates: list[dict[str, Any]] | None = None,
    selected_issue: dict[str, Any] | None = None,
    role: str = "primary",
    confirmation_ref: str | None = None,
) -> dict[str, Any]:
    payload["target_disposition"] = {
        "disposition": disposition,
        "duplicate_query": "repo:example/guru-extension is:issue is:open stage0 eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z",
        "duplicate_candidates": candidates or [], "duplicate_facts_sha256": "0" * 64,
        "selected_issue": selected_issue, "original_target_role": role,
        "decision_summary": f"The reviewed owner staging selected {disposition}.",
        "confirmation_ref": confirmation_ref, "disposition_digest": "0" * 64,
    }
    return runtime.derive_requirements_clarification_result(payload)


def clarity_confirm(runtime: Any, payload: dict[str, Any], action_ids: list[str]) -> dict[str, Any]:
    payload = runtime.derive_requirements_clarification_result(payload)
    actions = {item["action_id"]: item for item in payload["source_actions"]}
    payload["human_confirmation"] = {
        "status": "confirmed",
        "confirmation_kind": "exact_source_action_and_target" if action_ids else "exact_target_disposition",
        "action_digest": runtime.context_digest([actions[item]["action_digest"] for item in action_ids]) if action_ids else None,
        "target_disposition_digest": payload["target_disposition"]["disposition_digest"],
        "proposal_digests": [], "confirmed_actions": action_ids, "confirmer": "user",
        "confirmed_at": "2026-01-01T00:00:01Z",
        "evidence_summary": "The exact reviewed owner staging action was confirmed.",
    }
    return runtime.derive_requirements_clarification_result(payload)


def build_clarity_owner(runtime: Any, package_root: Path, recipe: str) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    if recipe == "clarity-clear":
        return runtime.derive_requirements_clarification_result(payload)

    payload["mode"] = "workflow"
    if recipe == "clarity-needs-context":
        payload["typed_exit"] = "needs_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
        payload["context_evidence"] = {
            "status": "missing", "schema_id": None, "snapshot_sha256": None,
            "evidence_refs": ["repository.current_owner"],
            "missing_reason": "The current repository owner evidence is unavailable.",
        }
        payload["reason"] = "A named repository fact is required before clarification can continue."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-refresh-context":
        payload["mode"] = "standalone"
        payload["typed_exit"] = "refresh_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["context_evidence"]["status"] = "stale"
        payload["context_evidence"]["missing_reason"] = "The reviewed source binding changed."
        payload["reason"] = "The context snapshot must be refreshed from current authority."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-blocked":
        payload = clarity_target(runtime, payload)
        payload = clarity_disposition(runtime, payload, "keep_current_open_issue")
        payload["typed_exit"] = "blocked"
        payload["consumer"] = {"kind": "stop", "id": "requirements-clarification-blocked"}
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["user_refused"],
            "summary": "A load-bearing requirement decision was refused.",
        }
        payload["reason"] = "The refused load-bearing decision blocks the clarification loop."
        return runtime.derive_requirements_clarification_result(payload)
    if recipe == "clarity-retarget":
        payload = clarity_target(runtime, payload)
        projection = {
            "repo": "example/guru-extension", "number": 146, "identity": "#146",
            "url": "https://github.com/example/guru-extension/issues/146", "state": "open",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        candidate = {
            **projection, "facts_sha256": runtime.context_digest(projection),
            "decision": "selected", "reason": "The current duplicate is the confirmed target.",
        }
        selected = {
            "repo": candidate["repo"], "issue_number": candidate["number"],
            "url": candidate["url"], "state": candidate["state"],
            "updated_at": candidate["updated_at"], "facts_sha256": candidate["facts_sha256"],
        }
        payload["typed_exit"] = "retarget_context"
        payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
        payload["source_actions"] = [{
            "action_id": "select_existing", "kind": "select_existing_issue",
            "target": {"repo": candidate["repo"], "issue_number": candidate["number"]},
            "payload": selected, "preimage_sha256": payload["review_target"]["facts_sha256"],
            "payload_sha256": None, "action_digest": "0" * 64, "status": "validated",
            "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "retarget_existing_issue", candidates=[candidate],
            selected_issue=selected, role="related", confirmation_ref="selected_target_confirmation",
        )
        return clarity_confirm(runtime, payload, ["select_existing"])
    if recipe == "clarity-new-task":
        payload = clarity_target(runtime, payload, state="closed")
        payload["typed_exit"] = "new_task"
        payload["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
        payload["source_actions"] = [{
            "action_id": "new_issue", "kind": "new_issue_draft",
            "target": {"repo": "example/guru-extension"},
            "payload": {"title": "Independent Stage 0 follow-up", "body": "Reviewed independent delivery scope."},
            "preimage_sha256": None, "payload_sha256": None, "action_digest": "0" * 64,
            "status": "draft_ready", "mutation_evidence": None,
        }]
        payload = clarity_disposition(
            runtime, payload, "create_followup_draft", role="related",
            confirmation_ref="followup_target_confirmation",
        )
        return clarity_confirm(runtime, payload, ["new_issue"])
    raise ValueError(f"unsupported clarification owner staging recipe: {recipe}")


def context_sync_result(runtime: Any, head: str) -> dict[str, Any]:
    identity = runtime.resolution_identity(
        source="explicit", selected_base="main", remote="origin", candidates=["main"],
        decision_branch="main", decision_head=head, decision_clean=True,
    )
    resolution_sha256 = runtime.canonical_json_sha256(identity)
    result = {
        "schema_version": "1.0", "skill_id": "guru-sync-base", "status": "synced",
        "resolution": {
            "source": "explicit", "selected_base": "main", "remote": "origin",
            "candidates": ["main"], "resolution_sha256": resolution_sha256,
        },
        "post_sync_resolution": identity,
        "post_sync_resolution_sha256": resolution_sha256,
        "decision_checkout": {
            "branch": "main", "head_before": head, "head_after": head,
            "clean_before": True, "clean_after": True,
        },
        "git": {
            "local_ref": "refs/heads/main", "remote_ref": "refs/remotes/origin/main",
            "local_head_before": head, "local_head_after": head, "remote_head_after": head,
            "fetch_performed": True, "fast_forwarded": False,
        },
        "fresh": True,
    }
    result["facts_sha256"] = runtime.canonical_json_sha256(result)
    return result


def build_context_owner(
    runtime: Any,
    fixture: Path,
    package_root: Path,
    recipe: str,
    task_dir: Path | None = None,
) -> dict[str, Any]:
    payload = json.loads(
        (package_root / "examples/context-discovery.json").read_text(encoding="utf-8")
    )
    old_head = run_git(fixture, "rev-parse", "HEAD")
    sync = context_sync_result(runtime, old_head)
    payload["repository"] = {
        "repo": "example/guru-extension", "selected_base": "main", "decision_branch": "main",
    }
    payload["base_evidence"] = {
        "schema_id": "guru-base-sync-result-1.0", "sync_result": sync, "remote": "origin",
        "base_head": old_head, "decision_head": old_head, "local_head": old_head,
        "remote_head": old_head, "post_sync_resolution_sha256": sync["post_sync_resolution_sha256"],
        "clean": True,
    }
    payload["change_input"]["issue_refs"] = []
    payload["change_input"]["paths"] = ["docs/requirements.md"]
    payload["live_change"]["issue_binding"] = None
    body_sha256 = hashlib.sha256(b"Stage 0 context owner staging draft").hexdigest()
    live_unsigned = {
        "kind": "draft", "identity": f"draft:{body_sha256}", "state": "draft",
        "updated_at": "2026-01-01T00:00:00Z", "body_sha256": body_sha256,
    }
    payload["live_change"] = {
        **live_unsigned, "facts_sha256": runtime.context_digest(live_unsigned), "issue_binding": None,
    }
    evidence_paths = {
        "docs": "docs/requirements.md",
        "code_contracts": "trellis/runtime.py",
        "tests": "trellis/test_runtime.py",
    }
    for group, path in evidence_paths.items():
        rows = payload["current_state"][group]
        rows[0]["path"] = path
        rows[0]["blob_or_content_sha256"] = run_git(fixture, "rev-parse", f"HEAD:{path}")
    query = runtime.canonicalize_context_query(fixture, payload["change_input"])
    payload["canonical_query"] = query
    payload["history_preview"] = runtime.build_context_history_preview(fixture, query)
    payload["history_review"] = {
        "selected_candidates": [], "excluded_candidates": [], "deep_reads": [],
    }
    payload["refresh_history"] = []
    payload["error"] = None
    payload["typed_exit"] = "context_ready"
    payload["ai_review_gate"]["status"] = "passed"
    if task_dir is not None:
        payload["task_worktree_state"] = runtime.context_task_worktree_state(
            fixture, task_dir,
        )
    payload["snapshot_identity"] = runtime.context_snapshot_identity(payload)
    if recipe == "context-ready":
        return payload
    if recipe == "context-blocked":
        payload["typed_exit"] = "blocked"
        payload["ai_review_gate"]["status"] = "blocked"
        payload["error"] = {
            "codes": ["semantic_review_blocked"],
            "summary": "A named load-bearing repository source could not be reviewed.",
        }
        payload["snapshot_identity"] = runtime.context_snapshot_identity(payload)
        return payload
    if recipe == "context-refresh-base":
        ready_snapshot = payload["snapshot_identity"]["snapshot_sha256"]
        run_git(fixture, "commit", "--allow-empty", "-q", "-m", "advance context fixture")
        if task_dir is not None:
            payload["task_worktree_state"] = runtime.context_task_worktree_state(
                fixture, task_dir,
            )
        payload["typed_exit"] = "refresh_base"
        payload["refresh_history"] = [{
            "reason": "The decision checkout advanced after context review.",
            "error_codes": (
                runtime.context_live_base_errors(fixture, payload, task_dir)
                if task_dir is not None
                else ["base_head_stale", "local_base_stale"]
            ),
            "superseded_query_sha256": query["query_sha256"],
            "superseded_snapshot_sha256": ready_snapshot,
            "detected_at": "2026-01-01T00:01:00Z",
        }]
        payload["snapshot_identity"] = runtime.context_snapshot_identity(payload)
        return payload
    raise ValueError(f"unsupported context owner staging recipe: {recipe}")


def wording_review(
    runtime: Any,
    profile: str,
    mode: str,
    scope: dict[str, Any],
    scan: dict[str, Any],
    typed_exit: str,
) -> dict[str, Any]:
    passed = typed_exit != "blocked"
    revisions: list[dict[str, Any]] = []
    if typed_exit == "content_changed":
        item = scope["items"][0]
        revisions = [{
            "revision_id": "stage0-eval-revision", "locator": item["path"],
            "before_sha256": "0" * 64, "after_sha256": item["content_sha256"],
            "reason": "The authorized planning wording revision is present in the current rescan.",
            "mutation_authority": "The reviewed workflow authorized the exact planning wording revision.",
            "rescan_sha256": scan["scan_sha256"],
        }]
    gate: dict[str, Any] = {
        "status": "passed" if passed else "blocked", "reviewer": "stage0-eval-reviewer",
        "summary": "The complete fixed wording scope and current rescan were semantically reviewed.",
        "reviewed_scan_sha256": scan["scan_sha256"],
        "checked_dimensions": {
            key: passed for key in runtime.CONTRACT_WORDING_REVIEW_DIMENSIONS
        },
    }
    if profile == "planning_artifacts":
        gate["planning_checked_dimensions"] = {
            key: passed for key in runtime.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
        }
    authored = {
        "generated_at": "2026-01-01T00:00:00Z",
        "semantic_review": {
            "revisions": revisions,
            "classifications": [{
                "hit_id": hit["hit_id"], "classification": "term_definition",
                "reason": "The semantic review retained this explicit contract term.",
            } for hit in scan["hits"]] if passed else [],
            "ai_review_gate": gate,
        },
        "human_confirmation": {
            "status": "not_required" if passed else "refused", "confirmed_by": None,
            "confirmed_at": None,
            "reason": "The current route records the completed wording review decision.",
        },
        "typed_exit": typed_exit,
    }
    return runtime.contract_wording_derive_result(profile, mode, scope, scan, authored)


def build_wording_owner(
    runtime: Any, fixture: Path, package_root: Path, recipe: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    change_request = {
        "kind": "draft", "draft_id": "stage0-wording-eval",
        "title": "Review Stage 0 wording",
        "body": "The current change request defines one bounded delivery unit.",
        "selected_comments": [],
    }
    change_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    change_path.write_text(json.dumps(change_request) + "\n", encoding="utf-8")
    if recipe == "wording-pass":
        profile, mode = "change_request", "workflow"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            change_request_input=change_path.relative_to(fixture).as_posix(),
        )
        typed_exit = "pass"
    elif recipe == "wording-content-changed":
        profile, mode = "planning_artifacts", "workflow"
        task = fixture / ".trellis/tasks/current"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode, task_dir=task,
        )
        typed_exit = "content_changed"
    elif recipe == "wording-blocked":
        profile, mode = "explicit_paths", "standalone"
        scope, contents = runtime.contract_wording_build_scope(
            fixture, profile, mode,
            explicit_paths=["docs/requirements/requirement-main.md"],
        )
        typed_exit = "blocked"
    else:
        raise ValueError(f"unsupported wording owner staging recipe: {recipe}")
    scan = runtime.scan_contract_wording(scope, contents)
    return wording_review(runtime, profile, mode, scope, scan, typed_exit), change_request


def readiness_prerequisites(
    runtime: Any, fixture: Path, source: dict[str, Any], source_path: Path,
) -> dict[str, dict[str, Any]]:
    context_package = fixture / ".trellis/guru-team/skills/packages/guru-discover-change-context"
    context = build_context_owner(runtime, fixture, context_package, "context-ready")
    body_sha256 = hashlib.sha256(source["body"].encode("utf-8")).hexdigest()
    live = {
        "kind": "draft", "identity": f"draft:{body_sha256}", "state": "draft",
        "updated_at": "2026-01-01T00:00:00Z", "body_sha256": body_sha256,
    }
    context["live_change"] = {
        **live, "facts_sha256": runtime.context_digest(live), "issue_binding": None,
    }
    context["snapshot_identity"] = runtime.context_snapshot_identity(context)

    clarity_package = fixture / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
    clarity = json.loads(
        (clarity_package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    clarity["mode"] = "standalone"
    clarity["invocation_context"] = {
        "kind": "proposed_draft", "caller": "stage0 readiness eval",
        "task_locator": None, "resume_target": "guru-review-contract-wording",
    }
    authority = {
        "kind": "draft", "repo": "example/guru-extension", "issue_number": None,
        "url": None, "state": "draft", "updated_at": None, "body_sha256": body_sha256,
    }
    clarity["review_target"] = {**authority, "facts_sha256": runtime.context_digest(authority)}
    clarity["target_disposition"] = {
        "disposition": "keep_current_draft",
        "duplicate_query": "repo:example/guru-extension is:issue is:open readiness eval",
        "duplicate_checked_at": "2026-01-01T00:00:00Z", "duplicate_candidates": [],
        "duplicate_facts_sha256": "0" * 64, "selected_issue": None,
        "original_target_role": "primary",
        "decision_summary": "No current duplicate replaces the reviewed draft.",
        "confirmation_ref": None, "disposition_digest": "0" * 64,
    }
    snapshot_sha256 = context["snapshot_identity"]["snapshot_sha256"]
    clarity["context_evidence"] = {
        "status": "current", "schema_id": "guru-context-discovery-1.0",
        "snapshot_sha256": snapshot_sha256,
        "evidence_refs": [f"guru-context-discovery-1.0:{snapshot_sha256}"],
        "missing_reason": None,
    }
    clarity = runtime.derive_requirements_clarification_result(clarity)

    scope, contents = runtime.contract_wording_build_scope(
        fixture, "change_request", "standalone",
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    scan = runtime.scan_contract_wording(scope, contents)
    wording = wording_review(runtime, "change_request", "standalone", scope, scan, "pass")
    return {"context": context, "clarity": clarity, "wording": wording}


def readiness_semantic_review(
    runtime: Any, target: dict[str, Any], linkage: dict[str, Any], typed_exit: str,
) -> dict[str, Any]:
    non_ready = typed_exit != "ready"
    finding_id = "stage0-readiness-finding"
    category = {
        "clarify_requirements": "requirement_gap",
        "review_wording": "wording_gap",
        "refresh_context": "context_stale",
        "blocked": "target_complete",
    }.get(typed_exit, "requirement_gap")
    finding = {
        "finding_id": finding_id, "category": category,
        "summary": "The reviewed evidence requires the declared prerequisite route.",
        "blocking": True, "evidence_refs": ["target"],
        "affected_hashes": [target["content_sha256"]],
        "route_basis": "The semantic review selected the owner of the identified gap.",
    }
    dimensions = [{
        "id": dimension_id, "status": "failed" if non_ready and index == 0 else "passed",
        "summary": "This readiness dimension was reviewed against current linked evidence.",
        "evidence_refs": ["target"], "affected_hashes": [target["content_sha256"]],
        "finding_ids": [finding_id] if non_ready and index == 0 else [],
    } for index, dimension_id in enumerate(runtime.CHANGE_REQUEST_REVIEW_DIMENSIONS)]
    scope_conclusion = {
        "requirement_scope_basis": "The reviewed draft and current prerequisites define the scope.",
        "delivery_unit_id": "stage0-readiness-eval", "close_issues": [],
        "related_issues": [], "followup_issues": [],
        "duplicate_reuse_decision": "No duplicate replaces this delivery unit.",
        "implementation_target": "The Stage 0 minimal handoff package graph.",
        "current_gap": "The selected route identifies the next readiness owner.",
        "archived_constraints": [], "risk_boundary": ["Normal honest workflow operation only."],
        "excluded_scope": ["Workspace mutation remains downstream."],
    }
    return {
        "dimensions": dimensions, "findings": [finding] if non_ready else [],
        "scope_conclusion": scope_conclusion,
        "ai_review_gate": {
            "status": runtime.CHANGE_REQUEST_REVIEW_GATE_BY_EXIT[typed_exit],
            "reviewer": "stage0-eval-reviewer",
            "reviewed_linkage_sha256": linkage["linkage_sha256"],
            "summary": "The complete readiness evidence was reviewed for one declared route.",
            "findings_count": 1 if non_ready else 0,
            "scope_conclusion_sha256": runtime.context_digest(scope_conclusion),
        },
    }


def build_readiness_owner(
    runtime: Any, fixture: Path, package_root: Path, recipe: str, mode: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    route_by_recipe = {
        "readiness-ready": "ready",
        "readiness-clarify": "clarify_requirements",
        "readiness-wording": "review_wording",
        "readiness-refresh": "refresh_context",
        "readiness-blocked": "blocked",
    }
    typed_exit = route_by_recipe.get(recipe)
    if typed_exit is None:
        raise ValueError(f"unsupported readiness owner staging recipe: {recipe}")
    source = {
        "kind": "draft", "draft_id": "stage0-readiness-eval",
        "title": "Review Stage 0 readiness",
        "body": "The Stage 0 migration is one independently deliverable unit.",
        "selected_comments": [],
    }
    source_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    prerequisites = readiness_prerequisites(runtime, fixture, source, source_path)
    scope, _ = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    title_sha256, body_sha256, _ = runtime.change_request_review_scope_hashes(scope)
    raw_target = {
        "kind": "proposed_draft", "repo": "example/guru-extension",
        "draft_id": source["draft_id"],
        "source_request_sha256": runtime.context_digest(
            runtime.change_request_review_request_authority_projection(
                "example/guru-extension", source, body_sha256
            )
        ),
        "title_sha256": title_sha256, "body_sha256": body_sha256,
        "side_effect_free": True,
    }
    target, scope, contents = runtime.change_request_review_normalize_target(
        fixture, raw_target, source_path.relative_to(fixture).as_posix(), mode,
    )
    projections = runtime.change_request_review_prerequisite_projections(
        fixture, prerequisites, target, scope, contents,
    )
    linkage = runtime.change_request_review_linkage(target, projections)
    authored = {
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "target": raw_target, "prerequisite_payloads": prerequisites,
        "semantic_review": readiness_semantic_review(runtime, target, linkage, typed_exit),
        "human_confirmation": {
            "status": "required" if typed_exit == "clarify_requirements" else "not_required",
            "reason": "A product decision returns to requirements clarification."
            if typed_exit == "clarify_requirements" else "No new product decision is required.",
            "proposal_sha256": "f" * 64 if typed_exit == "clarify_requirements" else None,
        },
        "typed_exit": typed_exit,
        "reason": "The semantic readiness review selected exactly one declared route.",
        "affected_evidence": [{
            "ref": "target", "sha256": target["content_sha256"],
            "summary": "The current reviewed change-request title and body.",
        }],
        "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS[typed_exit],
    }
    result = runtime.change_request_review_derive_result(target, projections, linkage, authored)
    return result, prerequisites, source


def workspace_prerequisites(
    runtime: Any, fixture: Path, mode: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    repo = "example/guru-extension"
    issue_number = 145
    issue_url = f"https://github.com/{repo}/issues/{issue_number}"
    updated_at = "2026-01-01T00:00:00Z"
    title = "Stage 0 workspace owner staging"
    body = "The Stage 0 migration is one independently deliverable unit."
    title_sha256 = hashlib.sha256(title.encode("utf-8")).hexdigest()
    body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()

    context_package = fixture / ".trellis/guru-team/skills/packages/guru-discover-change-context"
    context = build_context_owner(runtime, fixture, context_package, "context-ready")
    issue_facts = {
        "repo": repo, "number": issue_number, "url": issue_url, "state": "open",
        "updated_at": updated_at, "body_sha256": body_sha256,
    }
    context["live_change"] = {
        "kind": "issue", "identity": issue_url, "state": "open",
        "updated_at": updated_at, "body_sha256": body_sha256,
        "facts_sha256": runtime.context_digest(issue_facts), "issue_binding": None,
    }
    context["snapshot_identity"] = runtime.context_snapshot_identity(context)

    clarity_package = fixture / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
    clarity = json.loads(
        (clarity_package / "examples/requirements-clarification.json").read_text(encoding="utf-8")
    )
    clarity["mode"] = mode
    clarity["context_evidence"] = {
        "status": "current", "schema_id": "guru-context-discovery-1.0",
        "snapshot_sha256": context["snapshot_identity"]["snapshot_sha256"],
        "evidence_refs": [
            f"guru-context-discovery-1.0:{context['snapshot_identity']['snapshot_sha256']}"
        ],
        "missing_reason": None,
    }
    clarity = clarity_target(runtime, clarity, body=body)
    clarity = clarity_disposition(runtime, clarity, "keep_current_open_issue")

    source = {
        "kind": "issue", "repo": repo, "number": issue_number,
        "selected_comments": [],
    }
    source_path = fixture / ".trellis/.runtime/guru-team/evals/change-request.json"
    source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    scope, contents = runtime.contract_wording_build_scope(
        fixture, "change_request", mode,
        change_request_input=source_path.relative_to(fixture).as_posix(),
    )
    scan = runtime.scan_contract_wording(scope, contents)
    wording = wording_review(runtime, "change_request", mode, scope, scan, "pass")

    raw_target = {
        "kind": "existing_issue", "repo": repo, "issue_number": issue_number,
        "url": issue_url, "updated_at": updated_at,
        "title_sha256": title_sha256, "body_sha256": body_sha256,
    }
    prerequisite_payloads = {"context": context, "clarity": clarity, "wording": wording}
    target, normalized_scope, normalized_contents = runtime.change_request_review_normalize_target(
        fixture, raw_target, source_path.relative_to(fixture).as_posix(), mode,
    )
    projections = runtime.change_request_review_prerequisite_projections(
        fixture, prerequisite_payloads, target, normalized_scope, normalized_contents,
    )
    linkage = runtime.change_request_review_linkage(target, projections)
    semantic_review = readiness_semantic_review(runtime, target, linkage, "ready")
    semantic_review["scope_conclusion"]["close_issues"] = [issue_number]
    semantic_review["ai_review_gate"]["scope_conclusion_sha256"] = runtime.context_digest(
        semantic_review["scope_conclusion"]
    )
    authored = {
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "target": raw_target, "prerequisite_payloads": prerequisite_payloads,
        "semantic_review": semantic_review,
        "human_confirmation": {
            "status": "not_required",
            "reason": "The current reviewed issue requires no additional product decision.",
            "proposal_sha256": None,
        },
        "typed_exit": "ready",
        "reason": "The complete existing-issue delivery unit passed semantic readiness review.",
        "affected_evidence": [{
            "ref": "target", "sha256": target["content_sha256"],
            "summary": "The current reviewed issue title and body.",
        }],
        "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS["ready"],
    }
    readiness = runtime.change_request_review_derive_result(
        target, projections, linkage, authored
    )
    return {
        "base": context["base_evidence"]["sync_result"],
        "context": context,
        "clarity": clarity,
        "wording": wording,
        "readiness": readiness,
    }, {
        "repo": repo, "issue_number": issue_number, "url": issue_url,
        "updated_at": updated_at, "title": title, "body": body,
        "title_sha256": title_sha256, "body_sha256": body_sha256,
    }


def workspace_plan(
    runtime: Any,
    fixture: Path,
    recipe: str,
    mode: str,
    prerequisites: dict[str, dict[str, Any]],
    issue: dict[str, Any],
) -> tuple[dict[str, Any], Path]:
    prerequisite_root = fixture / ".trellis/.runtime/guru-team/evals/workspace-prerequisites"
    prerequisite_root.mkdir(parents=True, exist_ok=True)
    projections: dict[str, dict[str, Any]] = {}
    for key, payload in prerequisites.items():
        relative = f".trellis/.runtime/guru-team/evals/workspace-prerequisites/{key}.json"
        path = fixture / relative
        path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        projections[key] = runtime.task_workspace_prerequisite_projection(
            key, relative, payload, hashlib.sha256(path.read_bytes()).hexdigest()
        )

    route = {
        "workspace-created": ("passed", "confirmed"),
        "workspace-cancelled": ("passed", "refused"),
        "workspace-refresh-review": ("reroute", "not_in_current_invocation"),
        "workspace-blocked": ("blocked", "not_in_current_invocation"),
    }.get(recipe)
    if route is None:
        raise ValueError(f"unsupported task workspace owner staging recipe: {recipe}")
    gate_status, confirmation_status = route
    task_slug = "145-stage0-owner-eval"
    task_dir = f".trellis/tasks/{time.strftime('%m-%d')}-{task_slug}"
    scope_item = {
        "number": issue["issue_number"], "url": issue["url"],
        "title": issue["title"],
        "reason": "The reviewed Stage 0 delivery unit closes this exact issue.",
    }
    base_result = prerequisites["base"]
    naming_disposition = "conflict_blocked" if gate_status == "blocked" else "create_new"
    plan: dict[str, Any] = {
        "schema_version": "1.0", "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-01-01T00:00:00Z", "mode": mode,
        "invocation": {
            "caller": "guru-review-change-request:ready", "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": "stage0-workspace-eval",
        },
        "prerequisites": projections,
        "target": {
            "kind": "existing_issue", "repo": issue["repo"],
            "issue_number": issue["issue_number"], "url": issue["url"],
            "state": "open", "updated_at": issue["updated_at"],
            "title_sha256": issue["title_sha256"], "body_sha256": issue["body_sha256"],
            "draft": None,
            "disposition_sha256": prerequisites["clarity"]["target_disposition"]["disposition_digest"],
            "duplicate_decision_sha256": prerequisites["clarity"]["target_disposition"]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None, "created_issue_result": None,
        },
        "scope": {
            "primary": scope_item, "close": [scope_item], "related": [], "followup": [],
            "scope_sha256": "0" * 64,
        },
        "base": {
            "selected_base": base_result["resolution"]["selected_base"],
            "remote": base_result["resolution"]["remote"],
            "base_ref": base_result["git"]["remote_ref"],
            "decision_head": base_result["decision_checkout"]["head_after"],
            "local_head": base_result["git"]["local_head_after"],
            "remote_head": base_result["git"]["remote_head_after"],
            "post_sync_resolution_sha256": base_result["post_sync_resolution_sha256"],
            "sync_facts_sha256": base_result["facts_sha256"],
        },
        "naming": {
            "branch_name": f"feat/{task_slug}", "workspace_slug": task_slug,
            "task_slug": task_slug, "task_title": "#145 Stage 0 owner eval",
            "reason": "Names bind the reviewed issue and isolated eval workspace.",
            "branch_disposition": naming_disposition,
            "workspace_disposition": naming_disposition,
            "task_disposition": naming_disposition,
        },
        "assignee": {
            "login": "stage0-eval", "source": "single_issue_assignee",
            "candidates": ["stage0-eval"],
            "resolution_evidence": "The live source issue has one exact assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch", "create_worktree", "create_task",
                "write_task_artifacts", "write_runtime_mappings",
            ],
            "task_artifacts": [
                f"{task_dir}/{name}" for name in runtime.TASK_WORKSPACE_ARTIFACT_NAMES
            ],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
            "command_argv": ["create-task-workspace", "--input", OWNER_PLAN],
            "stop_after": "created_workspace",
        },
        "confirmations": {
            "github_issue_mutation": {
                "status": "not_in_current_invocation", "source": None,
                "reviewed_plan_sha256": None, "evidence": None,
                "confirmation_sha256": None,
            },
            "workspace_and_task_mutation": {
                "status": confirmation_status,
                "source": "explicit_user_confirmation" if confirmation_status != "not_in_current_invocation" else None,
                "reviewed_plan_sha256": "0" * 64 if confirmation_status != "not_in_current_invocation" else None,
                "evidence": (
                    "The exact reviewed workspace mutation was confirmed."
                    if confirmation_status == "confirmed"
                    else "The exact reviewed workspace mutation was refused."
                    if confirmation_status == "refused" else None
                ),
                "confirmation_sha256": "0" * 64 if confirmation_status != "not_in_current_invocation" else None,
            },
        },
        "ai_review_gate": {
            "status": gate_status, "reviewer": "stage0-eval-reviewer",
            "reviewed_plan_sha256": "0" * 64,
            "summary": "The exact target, names, assignee, scope and mutation boundary were reviewed.",
            "evidence": [
                "The invocation owns one isolated workspace and task.",
                "All durable artifacts are task-local and all runtime mappings are ignored.",
            ],
        },
        "freshness": {
            "captured_at": "2026-01-01T00:00:00Z",
            "reviewable_plan_sha256": "0" * 64, "plan_sha256": "0" * 64,
        },
    }
    plan["scope"]["scope_sha256"] = runtime.task_workspace_scope_digest(plan["scope"])
    reviewable = runtime.context_digest(runtime.task_workspace_reviewable_projection(plan))
    confirmation = plan["confirmations"]["workspace_and_task_mutation"]
    if confirmation_status != "not_in_current_invocation":
        confirmation["reviewed_plan_sha256"] = reviewable
        confirmation["confirmation_sha256"] = runtime.task_workspace_confirmation_digest(confirmation)
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable
    plan["freshness"]["reviewable_plan_sha256"] = reviewable
    plan["freshness"]["plan_sha256"] = runtime.task_workspace_plan_digest(plan)
    plan_path = fixture / OWNER_PLAN
    plan_path.write_text(json.dumps(plan) + "\n", encoding="utf-8")
    return plan, plan_path


def build_workspace_owner(
    runtime: Any, fixture: Path, recipe: str, mode: str,
) -> dict[str, Any]:
    prerequisites, issue = workspace_prerequisites(runtime, fixture, mode)
    plan, plan_path = workspace_plan(
        runtime, fixture, recipe, mode, prerequisites, issue
    )
    relative_plan = plan_path.relative_to(fixture).as_posix()
    runtime.cmd_record_task_workspace_plan(argparse.Namespace(
        root=str(fixture), input=relative_plan,
    ))

    real_prepare_workspace = runtime.prepare_workspace

    def prepare_and_copy_inputs(*arguments: Any, **kwargs: Any) -> tuple[str, Path, bool]:
        workspace_mode, workspace, ready = real_prepare_workspace(*arguments, **kwargs)
        if ready and workspace.resolve() != fixture.resolve():
            source = fixture / ".trellis/.runtime/guru-team/evals/workspace-prerequisites"
            target = workspace / ".trellis/.runtime/guru-team/evals/workspace-prerequisites"
            shutil.copytree(source, target, dirs_exist_ok=True)
        return workspace_mode, workspace, ready

    runtime.prepare_workspace = prepare_and_copy_inputs
    try:
        result = runtime.cmd_create_task_workspace(argparse.Namespace(
            root=str(fixture), input=relative_plan,
            cancelled=recipe == "workspace-cancelled",
            refresh_review=recipe == "workspace-refresh-review",
            reason=None,
            reason_code=(
                "disposition_changed" if recipe == "workspace-refresh-review"
                else "object_conflict" if recipe == "workspace-blocked" else None
            ),
        ))
    finally:
        runtime.prepare_workspace = real_prepare_workspace
    result_path = fixture / OWNER_RESULT
    result_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
    return runtime.cmd_check_task_workspace_result(argparse.Namespace(
        root=str(fixture), input=result_path.relative_to(fixture).as_posix(),
        plan_input=relative_plan,
    ))


def production_wording_evidence(runtime: Any, fixture: Path, task: Path) -> None:
    scope, contents = runtime.contract_wording_build_scope(
        fixture, "planning_artifacts", "workflow", task_dir=task,
    )
    scan = runtime.scan_contract_wording(scope, contents)
    gate = {
        "status": "passed",
        "reviewer": "production-eval-owner",
        "summary": "The fixed planning scope passed the complete wording review.",
        "reviewed_scan_sha256": scan["scan_sha256"],
        "checked_dimensions": {
            key: True for key in runtime.CONTRACT_WORDING_REVIEW_DIMENSIONS
        },
        "planning_checked_dimensions": {
            key: True for key in runtime.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
        },
    }
    evidence = runtime.contract_wording_derive_result(
        "planning_artifacts",
        "workflow",
        scope,
        scan,
        {
            "generated_at": "2026-07-23T00:00:00Z",
            "semantic_review": {
                "revisions": [],
                "classifications": [],
                "ai_review_gate": gate,
            },
            "human_confirmation": {
                "status": "not_required",
                "confirmed_by": None,
                "confirmed_at": None,
                "reason": "The production eval wording review does not mutate content.",
            },
            "typed_exit": "pass",
        },
    )
    runtime.write_json(task / runtime.CONTRACT_WORDING_EVIDENCE_ARTIFACT, evidence)


def production_task_fixture(runtime: Any, fixture: Path) -> tuple[Path, str]:
    (fixture / ".trellis/guru-team/config.yml").write_text(
        "workspace_mode: current\n", encoding="utf-8",
    )
    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    runtime.write_json(task / "task.json", {
        "id": "current",
        "name": "current",
        "title": "Production minimal handoff eval",
        "status": "planning",
        "scope": "issue #146",
        "branch": "eval/current",
        "base_branch": "main",
    })
    for name, content in {
        "prd.md": (
            "# PRD\n\n## R1. Production eval\n\n"
            "The production eval uses the public package boundary.\n"
        ),
        "design.md": (
            "# Design\n\n## Docs SSOT Plan\n\n"
            "Strategy: ssot_first. Durable requirements own the contract.\n"
        ),
        "implement.md": (
            "# Implement\n\nExecute the recorder, checker, and public wrapper.\n"
        ),
    }.items():
        (task / name).write_text(content, encoding="utf-8")
    runtime.write_json(task / "issue-scope-ledger.json", {
        "schema_version": "1.0",
        "primary_issue": {"number": 146},
        "close_issues": [{"number": 146}],
        "related_issues": [],
        "followup_issues": [],
    })
    runtime.write_json(task / "task-start-context.json", {
        "schema_version": "1.0",
        "task_artifact_dir": ".trellis/tasks/current",
        "task_slug": "current",
        "workspace_slug": "current",
        "task_title": "Production minimal handoff eval",
        "task_workspace_id": "current",
        "branch_name": "eval/current",
        "base_branch": "main",
        "base_ref": "refs/remotes/origin/main",
        "base_head_sha": "0" * 40,
        "remote_head_sha": "0" * 40,
        "source_issue": {"number": 146},
        "source_repo": {"repo": "example/guru-extension", "url": ""},
        "assignee": "production-eval",
        "actor": {"login": "production-eval"},
        "issue_scope_ledger_seed": {},
        "intake_summary": {
            "duplicate_decision": {}, "naming_quality": {}, "confirmation": {},
        },
    })
    durable = fixture / "docs/requirements.md"
    durable.parent.mkdir(parents=True, exist_ok=True)
    durable.write_text(
        "# Requirements\n\nThe public wrapper owns the production eval boundary.\n",
        encoding="utf-8",
    )
    source = fixture / "src/production-eval.txt"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("baseline\n", encoding="utf-8")
    production_wording_evidence(runtime, fixture, task)
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage production owner fixture")
    base_head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", base_head)
    run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
    run_git(fixture, "checkout", "-q", "-b", "eval/current")
    context_path = task / "task-start-context.json"
    context = json.loads(context_path.read_text(encoding="utf-8"))
    context["base_head_sha"] = base_head
    context["remote_head_sha"] = base_head
    runtime.write_json(context_path, context)
    run_git(fixture, "add", context_path.relative_to(fixture).as_posix())
    run_git(fixture, "commit", "-q", "-m", "bind production task base")
    return task, base_head


def production_planning_input(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> Path:
    statuses = {
        "approved": "passed",
        "revision_required": "revision_required",
        "clarify_scope": "clarify_scope",
        "blocked": "blocked",
    }
    consumers = {
        "approved": {"kind": "workflow", "id": "phase-1-task-activation"},
        "revision_required": {"kind": "skill", "id": "guru-approve-task-plan"},
        "clarify_scope": {
            "kind": "workflow", "id": "guru-task-plan-clarify-scope-router",
        },
        "blocked": {"kind": "stop", "id": "task-plan-approval-blocked"},
    }
    status = statuses[exit_id]
    gate = {
        "status": status,
        "reviewer": "production-eval-owner",
        "summary": "The exact production planning case completed semantic review.",
        "reviewed_at": "2026-07-23T00:01:00Z",
        "findings": [],
        "revision_actions": (
            ["Revise the task-local planning contract."]
            if exit_id == "revision_required" else []
        ),
        "scope_proposals": (
            ["scope-proposal:R13"] if exit_id == "clarify_scope" else []
        ),
        "blocking_reasons": (
            ["The required planning authority is unavailable."]
            if exit_id == "blocked" else []
        ),
    }
    confirmation = {
        "kind": "post-planning-approval" if exit_id == "approved" else "not-required",
        "status": "confirmed" if exit_id == "approved" else "not_required",
        "prompt_presented_at": "2026-07-23T00:02:00Z" if exit_id == "approved" else None,
        "confirmed_at": "2026-07-23T00:03:00Z" if exit_id == "approved" else None,
        "evidence_summary": (
            "The user confirmed after reviewing all planning links."
            if exit_id == "approved"
            else "This route does not activate the task."
        ),
    }
    payload = {
        "mode": "workflow",
        "requirement_authorities": [{
            "id": "task-prd",
            "kind": "task_artifact",
            "locator": ".trellis/tasks/current/prd.md",
            "sha256": "0" * 64,
            "updated_at": None,
        }],
        "docs_ssot_plan": {
            "strategy": "ssot_first",
            "artifact_path": "design.md",
            "locator": "Docs SSOT Plan",
            "statement_sha256": "0" * 64,
            "durable_paths": ["docs/requirements.md"],
        },
        "provenance_review": {
            "entries": [{
                "id": "R1",
                "artifact_path": "prd.md",
                "locator": "R1. Production eval",
                "statement_sha256": "0" * 64,
                "classification": "explicit_requirement",
                "authority_refs": ["task-prd"],
                "reason": "The task PRD explicitly owns the public eval boundary.",
                "implementation_choice": None,
                "scope_expansion": None,
                "out_of_scope_proposal": None,
            }],
            "coverage": {
                "reviewer": "production-eval-owner",
                "summary": "Every load-bearing item is covered.",
                "reviewed_entry_ids": ["R1"],
                "all_load_bearing_items_covered": True,
                "review_sha256": "0" * 64,
            },
        },
        "unusual_scenario_review": {
            "reviewer": "production-eval-owner",
            "summary": "No unusual scenario expands this eval scope.",
            "candidates": [],
            "unresolved_count": 0,
            "review_sha256": "0" * 64,
        },
        "semantic_review": {"ai_review_gate": gate},
        "user_confirmation": confirmation,
        "typed_exit": exit_id,
        "consumer": consumers[exit_id],
        "reason": f"Production planning eval selected {exit_id}.",
        "supersedes_facts_sha256": None,
    }
    path = fixture / ".trellis/.runtime/guru-team/evals/planning-owner-input.json"
    runtime.write_json(path, payload)
    return path


def production_record_planning(
    runtime: Any, fixture: Path, task: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_planning_input(runtime, fixture, task, exit_id)
    runtime.cmd_record_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_planning_approval(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        allow_committed_head=False,
        require_exit=None,
        expected_artifact_sha256=None,
    ))


def production_agent_assignment(runtime: Any, fixture: Path, task: Path) -> None:
    head = run_git(fixture, "rev-parse", "HEAD")
    roles = (("实现代理", "implement-1"), ("阶段二检查代理", "check-1"))
    agents = [{
        "logical_role": role,
        "agent_id": agent_id,
        "platform_nickname": agent_id,
        "assigned_at": "2026-07-23T00:04:00Z",
        "assigned_head": head,
        "reason": f"Assign {role} for the complete eval round.",
        "event_id": f"evt-{agent_id}-assigned",
    } for role, agent_id in roles]
    events = [{
        "event_id": f"evt-{agent_id}-completed",
        "event": "completed",
        "agent_id": agent_id,
        "logical_role": role,
        "platform_nickname": agent_id,
        "observed_at": "2026-07-23T00:05:00Z",
        "recorded_at": "2026-07-23T00:05:00Z",
        "head": head,
        "source": "main-session",
        "evidence": f"{role} completed the production eval round.",
        "predecessor_agent_id": "",
        "predecessor_event_id": "",
        "termination_reason": "",
        "termination_source_event_id": "",
        "replacement_reason": "",
        "handoff_summary": "",
    } for role, agent_id in roles]
    runtime.write_json(task / "agent-assignment.json", {
        "schema_version": runtime.AGENT_ASSIGNMENT_SCHEMA_VERSION,
        "generated_at": "2026-07-23T00:04:00Z",
        "updated_at": "2026-07-23T00:05:00Z",
        "task": ".trellis/tasks/current",
        "head": head,
        "agents": agents,
        "liveness": {},
        "review_rounds": [],
        "reuse_decisions": [],
        "status_events": events,
        "event_corrections": [],
        "recovery_links": [],
    })


def production_phase2_input(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> Path:
    payload = json.loads(
        (package / "examples/phase2-check.json").read_text(encoding="utf-8")
    )
    payload["mode"] = "workflow"
    payload["requirement_provenance"] = {
        "summary": "The approved requirement authority was reviewed.",
        "artifacts": [{"path": "docs/requirements.md"}],
        "facts_sha256": "0" * 64,
    }
    payload["docs_ssot_plan"] = {
        "strategy": "ssot_first",
        "durable_paths": [{"path": "docs/requirements.md"}],
        "sync_result": "The durable requirement was the implementation input.",
        "task_delta_merged": True,
        "task_history_only": ["Eval owner staging evidence"],
        "no_update_reason": None,
        "followup_or_pr_limit": None,
        "facts_sha256": "0" * 64,
    }
    payload["implementation_handoff"] = {
        "summary": "The production eval implementation and checks completed.",
        "artifacts": [{"path": ".trellis/tasks/current/implement.md"}],
        "facts_sha256": "0" * 64,
    }
    payload["agent_assignment"] = {
        "implementation_agent_ids": ["implement-1"],
        "check_agent_ids": ["check-1"],
    }
    payload["repository_snapshot"] = {
        "reviewed_paths": [
            {"path": "src/production-eval.txt"},
            {"path": ".trellis/tasks/current/agent-assignment.json"},
        ],
    }
    payload["check_execution"]["worker_evidence"] = [{
        "source": "official_trellis_check",
        "agent_id": "check-1",
        "summary": "The checker supplied evidence for the completed semantic round.",
        "evidence_only": True,
        "facts_sha256": "f" * 64,
    }]
    payload["check_execution"]["unverified_items"] = []
    payload["scope_qualification"]["candidates"] = []
    payload["semantic_review"]["findings"] = []
    for dimension in payload["semantic_review"]["adequacy_dimensions"]:
        dimension["status"] = "passed"
        dimension["finding_ids"] = []
        dimension["unverified_ids"] = []
    route = None
    consumer = {
        "passed": {"kind": "skill", "id": "guru-create-task-commit"},
        "implementation_required": {"kind": "workflow", "id": "guru-resume-implementation"},
        "planning_stale": {"kind": "workflow", "id": "guru-task-check-planning-router"},
        "blocked": {"kind": "stop", "id": "task-check-blocked"},
    }[exit_id]
    if exit_id == "implementation_required":
        payload["scope_qualification"]["candidates"] = [{
            "id": "C1", "summary": "A current-scope implementation defect remains.",
            "trigger_refs": ["PRD R1"],
            "normal_path_reproduction": "The supported eval path reproduces the defect.",
            "disposition": "current_scope", "route_basis": "Return to implementation.",
            "severity": "P2", "finding_id": "F1",
        }]
        payload["semantic_review"]["findings"] = [{
            "id": "F1", "candidate_id": "C1", "severity": "P2",
            "summary": "The current implementation requires a fix.",
            "path": "src/production-eval.txt", "blocking": True, "status": "open",
        }]
        payload["semantic_review"]["adequacy_dimensions"][2]["finding_ids"] = ["F1"]
    elif exit_id == "planning_stale":
        route = "reapprove_plan"
        payload["scope_qualification"]["candidates"] = [{
            "id": "scope-proposal:R13",
            "summary": "The approved scope requires a current authority decision.",
            "trigger_refs": ["PRD R1"],
            "normal_path_reproduction": "The supported eval path requires a scope change.",
            "disposition": "scope_change_required",
            "route_basis": "Return to the planning owner.",
            "severity": None, "finding_id": None,
        }]
    elif exit_id == "blocked":
        payload["check_execution"]["unverified_items"] = [{
            "id": "U1", "command_or_area": "integration verification",
            "reason": "The required dependency is unavailable.",
            "impact": "A complete reliable check cannot be claimed.",
            "blocking": True,
        }]
        payload["semantic_review"]["adequacy_dimensions"][9]["unverified_ids"] = ["U1"]
    payload["typed_exit"] = exit_id
    payload["route"] = route
    payload["reason"] = f"Production Phase 2 eval selected {exit_id}."
    payload["consumer"] = consumer
    payload["semantic_review"]["ai_review_gate"]["status"] = exit_id
    payload["semantic_review"]["ai_review_gate"]["full_rerun"] = True
    path = fixture / ".trellis/.runtime/guru-team/evals/phase2-owner-input.json"
    runtime.write_json(path, payload)
    return path


def production_record_phase2(
    runtime: Any, fixture: Path, task: Path, package: Path, exit_id: str,
) -> dict[str, Any]:
    input_path = production_phase2_input(runtime, fixture, task, package, exit_id)
    runtime.cmd_record_phase2_check(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        input=input_path.relative_to(fixture).as_posix(),
        dry_run=False,
    ))
    return runtime.cmd_check_phase2_check(argparse.Namespace(
        root=str(fixture), task=task.relative_to(fixture).as_posix(),
    ))


def production_commit_for_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    checked: dict[str, Any],
) -> tuple[str, str]:
    public_input = {
        "profile": "initial_commit",
        "mode": "workflow",
        "task_ref": task.relative_to(fixture).as_posix(),
        "message_intent": {
            "subject": "feat(workflow): #146 添加分支审查评测",
            "body": (
                "背景：\n"
                "把 production Branch Review eval 绑定到真实 task commit。\n\n"
                "变更：\n"
                "提交精确的已检查 fixture 路径。\n\n"
                "边界：\n"
                "不执行真实发布或外部仓库写入。\n\n"
                "验证：\n"
                "运行 shared public Skill wrapper corpus。\n\n"
                "Refs #146"
            ),
        },
        "path_authorizations": runtime.git_status_paths(fixture),
        "semantic_review": {
            "status": "passed",
            "summary": "The exact production review fixture paths passed semantic review.",
        },
        "human_authorization": {
            "status": "confirmed",
            "summary": "The production eval authorizes this isolated fixture commit.",
        },
        "exit_intent": "committed",
        "source_exit": "passed",
        "checked_head": checked["checked_head"],
        "check_ref": runtime.task_commit_public_check_ref(
            checked["artifact_sha256"]
        ),
    }
    try:
        candidate, plan, _ = runtime.build_task_commit_candidate_from_public_input(
            fixture, task, public_input,
        )
        executed = runtime.execute_task_commit_candidate(fixture, candidate, task)
    except runtime.WorkflowError as exc:
        raise ValueError(
            "production Branch Review fixture task commit failed: "
            + json.dumps(exc.payload, ensure_ascii=False, sort_keys=True)
        ) from exc
    return str(executed["commit_sha"]), str(plan["git"]["base_ref"])


def production_review_candidate(
    exit_id: str,
    head: str,
    *,
    resolved: bool = False,
) -> list[dict[str, Any]]:
    common = {
        "candidate_ref": "candidate-001",
        "affected_behavior": "The public Branch Review route must preserve the reviewed task behavior.",
        "path": "src/production-eval.txt",
        "evidence_refs": ["reviews/round-001-problem.md"],
        "requirement_refs": ["PRD R1"],
        "scope_basis": "The approved production eval requirement owns this behavior.",
        "qualification_reason": "The candidate was classified before any severity was assigned.",
    }
    current_scope_rejections = [
        {
            "candidate_ref": f"candidate-rejected-{scenario}",
            "disposition": "rejected_candidate",
            "scenario_class": scenario,
            "affected_behavior": (
                "The reviewer candidate was evaluated against current scope "
                "and disproved by implementation evidence."
            ),
            "path": "src/production-eval.txt",
            "evidence_refs": ["src/production-eval.txt"],
            "requirement_refs": ["PRD R5"],
            "scope_basis": (
                "The production eval preserves the current approved scenario "
                "without inventing a finding."
            ),
            "qualification_reason": (
                "The current implementation satisfies the bound contract, so "
                "the candidate is rejected without severity or finding fields."
            ),
        }
        for scenario in (
            "normal_required_behavior",
            "explicit_nonstandard_requirement",
            "approved_nonstandard_expansion",
        )
    ]
    if exit_id == "implementation_required" or resolved:
        findings = [{
            **common,
            "disposition": "qualified_finding",
            "scenario_class": "normal_required_behavior",
            "finding_ref": "F-001",
            "severity": "P2",
            "owner_round": 1,
            "reviewed_head": head,
            "status": "resolved" if resolved else "open",
            "closure_evidence": (
                ["reviews/round-002-closure.md"]
                if resolved else []
            ),
        }]
        return findings + (current_scope_rejections if resolved else [])
    if exit_id == "scope_confirmation_required":
        return [{
            **common,
            "disposition": "scope_proposal",
            "scenario_class": "unconfirmed_nonstandard_proposal",
            "proposal_ref": "scope-proposal:R2",
            "proposal": "Expand the eval beyond the approved public wrapper boundary.",
            "trigger_evidence": ["The reviewer identified an unapproved optional expansion."],
            "clarification_route": "guru-clarify-requirements",
        }]
    return current_scope_rejections


def production_review_rounds(
    exit_id: str,
    head: str,
    *,
    resolved: bool,
) -> list[dict[str, Any]]:
    if resolved:
        return [
            {
                "round": 1,
                "logical_role": "问题发现审查代理",
                "agent_id": "review-finding-1",
                "platform_nickname": "review-finding-1",
                "reviewed_head": head,
                "findings_count": 1,
                "reuse_policy": "Finding owners may return only for closure review.",
                "reuse_decision": "new-agent",
                "report_name": "round-001-problem.md",
            },
            {
                "round": 2,
                "logical_role": "问题闭环审查代理",
                "agent_id": "review-closure-replacement-1",
                "platform_nickname": "review-closure-replacement-1",
                "reviewed_head": head,
                "findings_count": 0,
                "reuse_policy": "A replacement reviewer closes the failed finding owner through the complete recovery chain.",
                "reuse_decision": "replace",
                "report_name": "round-002-closure.md",
            },
            {
                "round": 3,
                "logical_role": "最终放行审查代理",
                "agent_id": "review-final-1",
                "platform_nickname": "review-final-1",
                "reviewed_head": head,
                "findings_count": 0,
                "reuse_policy": "Final review uses a fresh agent across the complete range.",
                "reuse_decision": "new-agent",
                "report_name": "round-003-final.md",
            },
        ]
    if exit_id == "passed":
        role = "最终放行审查代理"
        findings_count = 0
        report_name = "round-001-final.md"
        agent_id = "review-final-1"
    else:
        role = "问题发现审查代理"
        findings_count = 1 if exit_id == "implementation_required" else 0
        report_name = "round-001-problem.md"
        agent_id = "review-finding-1"
    return [{
        "round": 1,
        "logical_role": role,
        "agent_id": agent_id,
        "platform_nickname": agent_id,
        "reviewed_head": head,
        "findings_count": findings_count,
        "reuse_policy": (
            "Final review uses a fresh agent across the complete range."
            if exit_id == "passed"
            else "The owner records only the current qualification-first review round."
        ),
        "reuse_decision": "new-agent",
        "report_name": report_name,
    }]


def production_record_review(
    runtime: Any,
    fixture: Path,
    task: Path,
    public_input: dict[str, Any],
    recipe: str,
) -> dict[str, Any]:
    exit_id = recipe.removeprefix("review-")
    resolved = exit_id == "finding-fix-passed"
    if resolved:
        exit_id = "passed"
    elif exit_id == "fresh-final-passed":
        exit_id = "passed"
    head = runtime.current_head(fixture)
    rounds = production_review_rounds(exit_id, head, resolved=resolved)
    assignment_path = task / "agent-assignment.json"
    assignment = runtime.read_json(assignment_path)
    assignment["head"] = head
    assignment["updated_at"] = "2026-07-23T00:12:00Z"
    reports: list[str] = []
    known_agents = {
        str(item.get("agent_id") or "")
        for item in assignment.get("agents", [])
        if isinstance(item, dict)
    }
    for index, round_item in enumerate(rounds, start=1):
        report_name = str(round_item.pop("report_name"))
        report = task / "reviews" / report_name
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            "# 分支审查原始报告\n\n"
            f"第 {index} 轮对完整当前范围完成语义审查；"
            f"findings_count={round_item['findings_count']}。\n",
            encoding="utf-8",
        )
        digest = runtime.file_digest(fixture, report)
        round_item.update({
            "recorded_at": f"2026-07-23T00:{12 + index:02d}:00Z",
            "review_report_path": digest["path"],
            "review_report_sha256": digest["sha256"],
            "review_report_size_bytes": digest["size_bytes"],
            "review_report_modified_at": digest["modified_at"],
        })
        assignment.setdefault("review_rounds", []).append(round_item)
        reports.append(digest["path"])
        agent_id = str(round_item["agent_id"])
        if agent_id not in known_agents:
            assignment.setdefault("agents", []).append({
                "logical_role": round_item["logical_role"],
                "agent_id": agent_id,
                "platform_nickname": round_item["platform_nickname"],
                "assigned_at": f"2026-07-23T00:{10 + index:02d}:00Z",
                "assigned_head": head,
                "reason": "Assign the exact production Branch Review eval role.",
                "event_id": f"evt-{agent_id}-assigned",
            })
            known_agents.add(agent_id)
        if not resolved:
            assignment.setdefault("status_events", []).append({
                "event_id": f"evt-{agent_id}-round-{index}-completed",
                "event": "completed",
                "agent_id": agent_id,
                "logical_role": round_item["logical_role"],
                "platform_nickname": round_item["platform_nickname"],
                "observed_at": f"2026-07-23T00:{20 + index:02d}:00Z",
                "recorded_at": f"2026-07-23T00:{20 + index:02d}:00Z",
                "head": head,
                "source": "main-session",
                "evidence": "The production Branch Review eval round completed.",
                "predecessor_agent_id": "",
                "predecessor_event_id": "",
                "termination_reason": "",
                "termination_source_event_id": "",
                "replacement_reason": "",
                "handoff_summary": "",
            })
    if resolved:
        failed = runtime.build_liveness_event(
            payload=assignment,
            root=fixture,
            logical_role="问题发现审查代理",
            agent_id="review-finding-1",
            platform_nickname="review-finding-1",
            event_name="failed",
            observed_at="2026-07-23T00:21:00Z",
            evidence=(
                "The finding report is retained, but the original owner "
                "cannot continue the closure round."
            ),
            source="main-session",
        )
        assignment.setdefault("status_events", []).append(failed)
        replacement = runtime.build_liveness_event(
            payload=assignment,
            root=fixture,
            logical_role="问题闭环审查代理",
            agent_id="review-closure-replacement-1",
            platform_nickname="review-closure-replacement-1",
            event_name="replacement-started",
            observed_at="2026-07-23T00:22:00Z",
            evidence="The replacement closure reviewer accepted the exact finding handoff.",
            source="main-session",
            predecessor_agent_id="review-finding-1",
            predecessor_event_id=failed["event_id"],
            replacement_reason="terminal_failed_incomplete",
            handoff_summary="Close F-001 against the current committed review range.",
        )
        assignment["status_events"].append(replacement)
        for event_index, (logical_role, agent_id, observed_at) in enumerate(
            (
                (
                    "问题闭环审查代理",
                    "review-closure-replacement-1",
                    "2026-07-23T00:23:00Z",
                ),
                (
                    "最终放行审查代理",
                    "review-final-1",
                    "2026-07-23T00:24:00Z",
                ),
            ),
            start=1,
        ):
            assignment["status_events"].append(
                runtime.build_liveness_event(
                    payload=assignment,
                    root=fixture,
                    logical_role=logical_role,
                    agent_id=agent_id,
                    platform_nickname=agent_id,
                    event_name="completed",
                    observed_at=observed_at,
                    evidence=(
                        "The replacement closure completed."
                        if event_index == 1
                        else "The fresh final review completed."
                    ),
                    source="main-session",
                )
            )
        assignment.setdefault("reuse_decisions", []).append({
            "logical_role": "问题闭环审查代理",
            "agent_id": "review-closure-replacement-1",
            "decision": "replace",
            "reason": "The original finding owner failed before closure.",
            "head": head,
            "recorded_at": "2026-07-23T00:22:00Z",
            "from_round": 1,
            "to_round": 2,
        })
    runtime.write_json(assignment_path, assignment)
    (task / "review.md").write_text(
        "# 分支审查汇总\n\n"
        "当前公开 Skill eval 已完成 qualification-first 语义审查。\n\n"
        "## 原始报告链接\n\n"
        + "".join(f"- {path}\n" for path in reports),
        encoding="utf-8",
    )
    semantic = {
        "candidates": production_review_candidate(
            exit_id, head, resolved=resolved,
        ),
        "ai_review_gate": {
            "status": exit_id,
            "summary": "The production Branch Review semantic Gate selected the actual route.",
        },
    }
    semantic_path = fixture / ".trellis/.runtime/guru-team/evals/review-owner-input.json"
    runtime.write_json(semantic_path, semantic)
    public_input.update({
        "task_ref": task.relative_to(fixture).as_posix(),
        "base_ref": runtime.diff_base_ref(fixture, "main"),
        "committed_head": head,
    })
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    direct_recorder_inputs = {runtime_input, semantic_path}
    for runtime_artifact in runtime_dir.rglob("*"):
        if (
            runtime_artifact.is_file()
            and runtime_artifact not in direct_recorder_inputs
        ):
            runtime_artifact.unlink()
    runtime.cmd_review_branch(argparse.Namespace(
        root=str(fixture),
        json=True,
        task=task.relative_to(fixture).as_posix(),
        base_branch="main",
        pass_gate=exit_id == "passed",
        summary="Branch Review eval 已完成当前语义路由。",
        evidence=["已审查运行时、CI/CD、Docker、K8s、migration 与 Makefile 部署影响。"],
        reviewer=str(rounds[-1]["agent_id"]),
        review_source=runtime.INDEPENDENT_REVIEW_SOURCE,
        review_report=(task / "review.md").relative_to(fixture).as_posix(),
        agent_assignment=assignment_path.relative_to(fixture).as_posix(),
        finding=[],
        findings_file=None,
        observation=[],
        observations_file=None,
        followup_candidate=[],
        followup_candidates_file=None,
        skill_input=runtime_input.relative_to(fixture).as_posix(),
        semantic_review_file=semantic_path.relative_to(fixture).as_posix(),
        typed_exit=exit_id,
        dry_run=False,
    ))
    return runtime.cmd_check_review_gate(argparse.Namespace(
        root=str(fixture),
        task=task.relative_to(fixture).as_posix(),
        allow_metadata_after_gate=False,
        allow_nonpass=True,
        expected_exit=exit_id,
    ))


def stage_production_owner_execution(
    request: dict[str, Any],
    fixture: Path,
    runtime_target: Path,
    request_package: Path,
    recipe: str,
    public_input_path: Path,
) -> tuple[Path, Path, dict[str, str]]:
    skill_id = str(request["skill_id"])
    fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if fixture_runtime_target.is_symlink() or not os.access(fixture_runtime_target, os.X_OK):
        raise ValueError("fixture public invocation runtime is unavailable")
    runtime = load_owner_runtime(fixture_runtime_target)
    task, _ = production_task_fixture(runtime, fixture)
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("owner staging package does not match the evaluated package contract")
    public_input = json.loads(public_input_path.read_text(encoding="utf-8"))
    expected_prefix = {
        "guru-approve-task-plan": "planning-",
        "guru-check-task": "check-",
        "guru-create-task-commit": "commit-",
        "guru-review-branch": "review-",
    }[skill_id]
    if not recipe.startswith(expected_prefix):
        raise ValueError("production owner staging recipe does not match the evaluated package")
    if skill_id == "guru-approve-task-plan":
        production_record_planning(
            runtime, fixture, task, str(public_input["exit_intent"]),
        )
    else:
        production_record_planning(runtime, fixture, task, "approved")
        task_payload = json.loads((task / "task.json").read_text(encoding="utf-8"))
        task_payload["status"] = "in_progress"
        runtime.write_json(task / "task.json", task_payload)
        run_git(fixture, "add", task.relative_to(fixture).as_posix())
        run_git(fixture, "commit", "-q", "-m", "activate production eval task")
        production_agent_assignment(runtime, fixture, task)
        (fixture / "src/production-eval.txt").write_text(
            f"{recipe}\n", encoding="utf-8",
        )
        phase2_package = fixture / ".trellis/guru-team/skills/packages/guru-check-task"
        checked = production_record_phase2(
            runtime,
            fixture,
            task,
            phase2_package,
            (
                "passed"
                if skill_id in {"guru-create-task-commit", "guru-review-branch"}
                else str(public_input["exit_intent"])
            ),
        )
        if skill_id == "guru-create-task-commit":
            public_input["checked_head"] = checked["checked_head"]
            public_input["check_ref"] = runtime.task_commit_public_check_ref(
                checked["artifact_sha256"]
            )
        elif skill_id == "guru-review-branch":
            production_commit_for_review(runtime, fixture, task, checked)
            production_record_review(
                runtime,
                fixture,
                task,
                public_input,
                (
                    "review-finding-fix-passed"
                    if recipe == "review-blocked"
                    else recipe
                ),
            )
            if recipe == "review-blocked":
                with (
                    task / "reviews/round-002-closure.md"
                ).open("a", encoding="utf-8") as handle:
                    handle.write(
                        "\n## 普通审查证据修订\n\n"
                        "该正常路径修订使已登记的 closure raw report digest 过期。\n"
                    )
            runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
            for runtime_artifact in runtime_dir.rglob("*"):
                if (
                    runtime_artifact.is_file()
                    and runtime_artifact != fixture / OWNER_INPUT
                ):
                    runtime_artifact.unlink()
    runtime_input = fixture / OWNER_INPUT
    runtime.write_json(runtime_input, public_input)
    return package, fixture_runtime_target, {}


def stage_owner_execution(
    request: dict[str, Any], execution_root: Path, runtime_target: Path,
) -> tuple[Path, Path, dict[str, str]]:
    skill_id = str(request["skill_id"])
    request_package = Path(request["package_root"]).resolve()
    fixture, _ = stage_clean_installed_owner_repo(
        execution_root, runtime_target, request_package,
    )
    if skill_id == "guru-sync-base":
        package = fixture / ".trellis/guru-team/skills/packages" / skill_id
        if (
            hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
            or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
            != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
        ):
            raise ValueError("owner staging package does not match the evaluated package contract")
        run_git(fixture, "add", ".")
        run_git(fixture, "commit", "-q", "-m", "stage owner fixture")
        head = run_git(fixture, "rev-parse", "HEAD")
        run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
        run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
        fake_bin = write_fake_gh(execution_root, "sync-base")
        fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        return package, fixture_runtime_target, {
            "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        }
    recipe, public_input = owner_recipe(request)
    if skill_id in PRODUCTION_SKILLS:
        return stage_production_owner_execution(
            request,
            fixture,
            runtime_target,
            request_package,
            recipe,
            public_input,
        )
    worktree_root = execution_root / "owner-worktrees"
    (fixture / ".trellis/guru-team/config.yml").write_text(
        f"workspace_mode: worktree\nworktree_root: {worktree_root}\n",
        encoding="utf-8",
    )
    evidence_files = {
        "docs/requirements.md": "# Requirements\n\nCurrent Stage 0 context evidence.\n",
        "docs/requirements/requirement-main.md": "# Contract\n\n本合同必须保持完整的语义审查。\n",
        "trellis/runtime.py": "STAGE0_CONTEXT_OWNER = 'runtime'\n",
        "trellis/test_runtime.py": "def test_stage0_context_owner():\n    assert True\n",
    }
    for relative, content in evidence_files.items():
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    task = fixture / ".trellis/tasks/current"
    task.mkdir(parents=True, exist_ok=True)
    (task / "task.json").write_text(json.dumps({
        "id": "current", "name": "current", "title": "Stage 0 wording fixture",
        "status": "planning", "scope": "issue #145", "branch": "main", "base_branch": "main",
    }) + "\n", encoding="utf-8")
    for name, content in {
        "prd.md": "# PRD\n\n## Requirement\n\nThe exact Stage 0 public contract is required.\n",
        "design.md": "# Design\n\n## Docs SSOT Plan\n\nStrategy: ssot_first.\n",
        "implement.md": "# Implement\n\nRun the production wrapper and owner checker.\n",
    }.items():
        (task / name).write_text(content, encoding="utf-8")
    (task / "task-start-context.json").write_text(json.dumps({
        "schema_version": "1.0", "task_artifact_dir": ".trellis/tasks/current",
        "task_slug": "current", "workspace_slug": "current",
        "task_title": "Stage 0 wording fixture", "task_workspace_id": "current",
        "branch_name": "main", "base_branch": "main", "base_ref": "main",
        "base_head_sha": "", "remote_head_sha": "", "source_issue": {"number": 145},
        "source_repo": {"repo": "example/guru-extension", "url": ""},
        "assignee": "stage0-eval", "actor": {"login": "stage0-eval"},
        "issue_scope_ledger_seed": {},
        "intake_summary": {"duplicate_decision": {}, "naming_quality": {}, "confirmation": {}},
    }) + "\n", encoding="utf-8")
    fixture_runtime_target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if fixture_runtime_target.is_symlink() or not os.access(fixture_runtime_target, os.X_OK):
        raise ValueError("fixture public invocation runtime is unavailable")
    package = fixture / ".trellis/guru-team/skills/packages" / skill_id
    if (
        hashlib.sha256((package / "interface.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "interface.json").read_bytes()).hexdigest()
        or hashlib.sha256((package / "evals/evals.json").read_bytes()).hexdigest()
        != hashlib.sha256((request_package / "evals/evals.json").read_bytes()).hexdigest()
    ):
        raise ValueError("owner staging package does not match the evaluated package contract")
    runtime_dir = fixture / ".trellis/.runtime/guru-team/evals"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    (fixture / OWNER_INPUT).write_bytes(public_input.read_bytes())
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage owner fixture")
    head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
    run_git(fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
    runtime = load_owner_runtime(runtime_target)
    public_payload = json.loads(public_input.read_text(encoding="utf-8"))
    public_mode = str(public_payload.get("mode") or "")
    fake_bin = write_fake_gh(execution_root, recipe)
    environment = {"PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}"}
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = environment["PATH"]
    try:
        if skill_id == "guru-clarify-requirements":
            owner = build_clarity_owner(runtime, package, recipe)
        elif skill_id == "guru-discover-change-context":
            context_task_dir = (
                fixture / str(public_payload["task_locator"])
                if public_payload.get("profile") == "task_local_reentry"
                else None
            )
            owner = build_context_owner(
                runtime, fixture, package, recipe, context_task_dir,
            )
        elif skill_id == "guru-review-contract-wording":
            owner, _ = build_wording_owner(runtime, fixture, package, recipe)
        elif skill_id == "guru-review-change-request":
            owner, prerequisites, _ = build_readiness_owner(
                runtime, fixture, package, recipe, public_mode
            )
            (fixture / ".trellis/.runtime/guru-team/evals/prerequisites.json").write_text(
                json.dumps(prerequisites) + "\n", encoding="utf-8"
            )
        elif skill_id == "guru-create-task-workspace":
            owner = build_workspace_owner(runtime, fixture, recipe, public_mode)
        else:
            raise ValueError(f"owner staging is not implemented for {skill_id}")
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    owner_path = fixture / OWNER_RESULT
    if (
        skill_id == "guru-discover-change-context"
        and public_payload.get("profile") == "task_local_reentry"
    ):
        owner_path = (
            fixture
            / str(public_payload["task_locator"])
            / str(public_payload["prior_snapshot_locator"])
        )
    owner_path.parent.mkdir(parents=True, exist_ok=True)
    owner_path.write_text(json.dumps(owner) + "\n", encoding="utf-8")
    return package, fixture_runtime_target, environment


def start_public_runtime_boundary(
    execution_root: Path,
    target: Path,
    package_root: Path,
    projection_root: Path,
    runtime_environment: dict[str, str],
) -> tuple[Path, threading.Thread, threading.Event]:
    request_path = execution_root / "public-invocation-request.json"
    response_path = execution_root / "public-invocation-response.json"
    request_path.unlink(missing_ok=True)
    response_path.unlink(missing_ok=True)
    stop = threading.Event()

    def serve() -> None:
        try:
            while not request_path.is_file():
                if stop.wait(0.01):
                    return
            try:
                request = json.loads(request_path.read_text(encoding="utf-8"))
                arguments = request["arguments"]
                if not isinstance(arguments, list) or any(not isinstance(item, str) for item in arguments):
                    raise ValueError("invalid public invocation arguments")
                if arguments[:2] != ["--package-root", str(projection_root)]:
                    raise ValueError("public invocation package projection binding is invalid")
                arguments = ["--package-root", str(package_root), *arguments[2:]]
                process = subprocess.run(
                    [str(target), *arguments],
                    cwd=target.parents[4],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    env={**os.environ, **runtime_environment},
                )
                response_payload = {
                    "returncode": process.returncode,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                }
            except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
                response_payload = {"returncode": 2, "stdout": "", "stderr": str(exc)}
            response_path.write_text(
                json.dumps(response_payload, separators=(",", ":")), encoding="utf-8",
            )
            while request_path.exists() or response_path.exists():
                if stop.wait(0.01):
                    return
        finally:
            if stop.is_set():
                try:
                    request_path.unlink(missing_ok=True)
                    response_path.unlink(missing_ok=True)
                except OSError:
                    pass

    thread = threading.Thread(target=serve, name="guru-eval-public-invocation", daemon=True)
    thread.start()
    boundary = execution_root / "public-invocation-boundary.sh"
    boundary.write_text(
        "#!/usr/bin/env python3\n"
        "import json,sys,time\n"
        "from pathlib import Path\n"
        f"request_path=Path({str(request_path)!r}); response_path=Path({str(response_path)!r})\n"
        "request_path.write_text(json.dumps({'arguments':sys.argv[1:]},separators=(',',':')),encoding='utf-8')\n"
        "for _ in range(3000):\n"
        " if response_path.is_file(): break\n"
        " time.sleep(0.01)\n"
        "else: raise SystemExit('public invocation response timed out')\n"
        "result=json.loads(response_path.read_text(encoding='utf-8')); request_path.unlink(missing_ok=True); response_path.unlink(missing_ok=True)\n"
        "sys.stdout.write(result['stdout']); sys.stderr.write(result['stderr'])\n"
        "raise SystemExit(result['returncode'])\n",
        encoding="utf-8",
    )
    boundary.chmod(0o755)
    return boundary, thread, stop


def build_context(
    request: dict[str, Any],
) -> tuple[str, Path, Path, Path, Path, Path, str, Path, threading.Thread, threading.Event]:
    workdir = Path(request["workdir"]).resolve()
    execution_root = workdir.parent
    projection_root, skill_path, wrapper_path, skill_sha256, wrapper_sha256 = stage_public_projection(request, execution_root)
    runtime_target = public_runtime_target(request)
    runtime_package_root, execution_runtime_target, runtime_environment = stage_owner_execution(
        request, execution_root, runtime_target
    )
    trace_path = execution_root / "native-trace.json"
    helper_path = execution_root / "native-trace-helper.py"
    helper_path.write_text(TRACE_HELPER, encoding="utf-8")
    helper_path.chmod(0o755)
    file_sections: list[str] = []
    for relative in request["files"]:
        staged = workdir / relative
        if not staged.is_file():
            raise ValueError("staged case file is unavailable")
        try:
            content = staged.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = f"<binary sha256={hashlib.sha256(staged.read_bytes()).hexdigest()}>"
        file_sections.append(f"### {relative}\n{content}")
    context = "\n".join([
        "Execute exactly one Guru Team Skill behavior eval.",
        f"Skill id: {request['skill_id']}",
        f"Exact public Skill projection: {projection_root}",
        f"Public wrapper: {wrapper_path}",
        f"Isolated workdir: {workdir}",
        f"Native trace helper: {helper_path}",
        f"Native trace receipt: {trace_path}",
        "The projection is the complete execution-visible package. Paths absent from it are outside the native execution contract.",
        "All Skill/runtime file reads and the public invocation must use the trace helper. Direct reads or direct wrapper execution are unsupported.",
        "First read the exact Skill contract with the helper's read operation, then invoke the exact public wrapper with its invoke operation.",
        "Return only the wrapper's single typed-exit JSON object, with no Markdown fence or explanation.",
        f"Case prompt:\n{request['prompt']}",
        f"Public invocation contract:\n{json.dumps(request['interface']['public_invocation'], separators=(',', ':'))}",
        "Staged case files:\n" + ("\n".join(file_sections) if file_sections else "<none>"),
        "The adapter has already completed any declared owner staging and checker validation in the installed fixture.",
        "Use the exact public_invocation.arguments from the staged case facts; do not recreate or rewrite public input, owner result, or owner plan files.",
        "For this post-owner invocation boundary, run only the exact Skill read command above and then the exact wrapper invocation command above. Do not read linked references, Interface assets, examples, wrapper source, or any other file.",
    ])
    native_request = {
        "schema_version": "1.0",
        "skill_id": request["skill_id"],
        "case_id": request["case_id"],
        "prompt": request["prompt"],
        "files": request["files"],
        "workdir": str(workdir),
        "public_package_root": str(projection_root),
        "public_invocation": request["interface"]["public_invocation"],
    }
    native_request_path = execution_root / "native-request.json"
    native_request_path.write_text(json.dumps(native_request, separators=(",", ":")), encoding="utf-8")
    request_sha256 = hashlib.sha256(native_request_path.read_bytes()).hexdigest()
    helper_arguments = (
        f"--trace {trace_path} --request-sha256 {request_sha256} --projection-root {projection_root} "
        f"--skill-sha256 {skill_sha256} --wrapper-sha256 {wrapper_sha256}"
    )
    context = context.replace(
        "First read the exact Skill contract with the helper's read operation, then invoke the exact public wrapper with its invoke operation.",
        f"First read the exact Skill contract with: {helper_path} {helper_arguments} read --kind skill_contract --path {skill_path}\n"
        f"Then invoke the exact public wrapper with: {helper_path} {helper_arguments} invoke --wrapper {wrapper_path} -- <declared wrapper arguments>",
    )
    context_path = execution_root / "native-context.txt"
    context_path.write_text(context, encoding="utf-8")
    protocol_path = execution_root / "native-protocol.json"
    protocol_path.write_text(json.dumps({
        "schema_version": "1.0", "native_request_path": str(native_request_path),
        "request_sha256": request_sha256, "helper_path": str(helper_path),
        "trace_path": str(trace_path), "skill_path": str(skill_path),
        "wrapper_path": str(wrapper_path), "projection_root": str(projection_root),
        "skill_sha256": skill_sha256, "wrapper_sha256": wrapper_sha256,
    }, separators=(",", ":")), encoding="utf-8")
    boundary_path, boundary_thread, boundary_stop = start_public_runtime_boundary(
        execution_root, execution_runtime_target, runtime_package_root, projection_root,
        runtime_environment,
    )
    return (
        context, context_path, wrapper_path, trace_path, protocol_path,
        native_request_path, request_sha256, boundary_path, boundary_thread,
        boundary_stop,
    )


def validate_native_trace(
    trace_path: Path,
    request_sha256: str,
    request: dict[str, Any],
    wrapper_path: Path,
    public_stdout: str,
    protocol_path: Path,
) -> list[str]:
    try:
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise ValueError("native trace receipt is missing or malformed")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    expected_top = {"schema_version", "request_sha256", "projection_root", "skill_sha256", "wrapper_sha256", "events"}
    if set(payload) != expected_top or payload.get("schema_version") != "1.0" or payload.get("request_sha256") != request_sha256:
        raise ValueError("native trace receipt request binding is invalid")
    events = payload.get("events")
    if not isinstance(events, list) or len(events) < 2:
        raise ValueError("native trace receipt is incomplete")
    projection_root = Path(protocol["projection_root"]).resolve()
    skill_path = Path(protocol["skill_path"]).resolve()
    if (
        payload.get("projection_root") != str(projection_root)
        or payload.get("skill_sha256") != protocol.get("skill_sha256")
        or payload.get("wrapper_sha256") != protocol.get("wrapper_sha256")
        or (projection_root / "evals").exists()
        or any(path.name == "guru_team_trellis.py" for path in projection_root.rglob("*"))
    ):
        raise ValueError("native trace public projection binding is invalid")
    workdir = Path(request["workdir"]).resolve()
    allowed_reads = {skill_path, *(workdir / relative for relative in request["files"])}
    skill_reads = []
    invocations = []
    for event in events:
        if not isinstance(event, dict) or event.get("request_sha256") != request_sha256:
            raise ValueError("native trace event binding is invalid")
        if event.get("kind") == "read":
            if set(event) != {"kind", "target_kind", "path", "sha256", "request_sha256"}:
                raise ValueError("native read trace shape is invalid")
            target = Path(str(event.get("path"))).resolve()
            if target not in allowed_reads:
                raise ValueError("native trace contains an undeclared file read")
            try:
                expected_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
            except OSError:
                raise ValueError("native trace read target is unavailable")
            if event.get("sha256") != expected_sha256:
                raise ValueError("native trace read digest mismatch")
            if target == skill_path and event.get("target_kind") == "skill_contract":
                skill_reads.append(event)
        elif event.get("kind") == "invoke":
            if set(event) != {"kind", "wrapper_path", "argv", "returncode", "stdout_sha256", "stderr_sha256", "request_sha256"}:
                raise ValueError("native invocation trace shape is invalid")
            invocations.append(event)
        else:
            raise ValueError("native trace event kind is invalid")
    if len(skill_reads) != 1 or events.index(skill_reads[0]) != 0:
        raise ValueError("native trace must begin with one exact Skill read")
    if len(invocations) != 1 or events.index(invocations[0]) != len(events) - 1:
        raise ValueError("native trace must end with one public wrapper invocation")
    invocation = invocations[0]
    argv = invocation.get("argv")
    if (
        Path(str(invocation.get("wrapper_path"))).resolve() != wrapper_path.resolve()
        or not isinstance(argv, list) or not argv
        or Path(str(argv[0])).resolve() != wrapper_path.resolve()
        or any(not isinstance(item, str) for item in argv)
        or invocation.get("returncode") != 0
        or invocation.get("stdout_sha256") != hashlib.sha256(public_stdout.encode("utf-8")).hexdigest()
        or not isinstance(invocation.get("stderr_sha256"), str)
        or len(invocation["stderr_sha256"]) != 64
    ):
        raise ValueError("native public wrapper invocation receipt is invalid")
    return ["public_invocation", "evals_not_loaded", "private_runtime_not_read"]


def native_argv(
    adapter: str,
    command: str,
    request: dict[str, Any],
    context: str,
    context_path: Path,
    native_request_path: Path,
    projection_root: Path,
) -> tuple[list[str], Path | None]:
    workdir = str(Path(request["workdir"]).resolve())
    if adapter == "shared":
        return [command, "--request", str(native_request_path), "--context", str(context_path), "--workdir", workdir], None
    if adapter == "codex":
        output_path = native_request_path.with_name("native-last-message.txt")
        trusted_root = str(Path(request["runtime_target"]).resolve().parents[4])
        return [
            command, "exec", "--ephemeral", "--ignore-user-config", "--sandbox", "workspace-write",
            "--cd", trusted_root, "--add-dir", workdir, "--add-dir", str(projection_root),
            "--output-last-message", str(output_path), context,
        ], output_path
    if adapter == "claude":
        return [
            command, "--print", "--safe-mode", "--output-format", "json", "--no-session-persistence",
            "--permission-mode", "dontAsk", "--add-dir", str(projection_root),
        ], None
    return [command, "--print", "--output-format", "json", context], None


def unwrap_native_output(adapter: str, stdout: str, output_path: Path | None) -> str:
    value = output_path.read_text(encoding="utf-8") if output_path and output_path.is_file() else stdout
    if adapter in {"claude", "cursor"}:
        try:
            payload = json.loads(value)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict) and isinstance(payload.get("result"), str):
            value = payload["result"]
    value = value.strip()
    if value.startswith("```") and value.endswith("```"):
        lines = value.splitlines()
        value = "\n".join(lines[1:-1]).strip()
    payload = json.loads(value)
    if not isinstance(payload, dict):
        raise ValueError("native output is not one typed JSON object")
    return json.dumps(payload, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, choices=ADAPTERS)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--request", required=True)
    args = parser.parse_args()
    request_path = Path(args.request).resolve()
    transcript = request_path.parent / "adapter-transcript.json"
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        fallback = {"corpus_sha256": "0" * 64}
        transcript.write_text(json.dumps({"adapter": args.adapter, "error": str(exc)}), encoding="utf-8")
        return emit(response(fallback, "execution_error", transcript, stderr="adapter request/context invalid"))
    packaged_native = Path(__file__).resolve().parent / args.native_command
    native = (
        str(packaged_native)
        if args.adapter == "shared" and packaged_native.is_file() and os.access(packaged_native, os.X_OK)
        else shutil.which(args.native_command)
    )
    if native is None:
        transcript.write_text(json.dumps({"adapter": args.adapter, "native_command": args.native_command, "status": "unsupported"}), encoding="utf-8")
        return emit(response(request, "unsupported", transcript, native_trace=Path(request["workdir"]).resolve().parent / "native-trace.json"))
    if args.adapter == "cursor":
        status = subprocess.run(
            [native, "status"], text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        status_text = f"{status.stdout}\n{status.stderr}".lower()
        if status.returncode != 0 or any(
            marker in status_text
            for marker in ("not logged in", "not authenticated", "unauthenticated", "login required")
        ):
            transcript.write_text(json.dumps({
                "adapter": args.adapter, "native_command": args.native_command,
                "status": "unsupported", "reason": "authentication unavailable",
            }), encoding="utf-8")
            return emit(response(
                request, "unsupported", transcript,
                native_trace=Path(request["workdir"]).resolve().parent / "native-trace.json",
            ))
    try:
        (
            context, context_path, wrapper_path, trace_path, protocol_path,
            native_request_path, request_sha256, boundary_path,
            boundary_thread, boundary_stop,
        ) = build_context(request)
    except Exception as exc:
        transcript.write_text(json.dumps({"adapter": args.adapter, "error": str(exc)}), encoding="utf-8")
        return emit(response(request, "execution_error", transcript, stderr="adapter request/context invalid"))
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    projection_root = Path(protocol["projection_root"])
    argv, output_path = native_argv(args.adapter, native, request, context, context_path, native_request_path, projection_root)
    native_environment = dict(os.environ)
    native_environment.pop("GURU_TEAM_FAKE_NATIVE_DISPATCHER", None)
    native_environment.pop("OLDPWD", None)
    native_environment["PWD"] = str(Path(request["workdir"]).resolve().parent)
    native_environment["GURU_TEAM_DISPATCHER"] = str(boundary_path)
    native_environment["GURU_TEAM_NATIVE_REQUEST"] = str(native_request_path)
    native_environment["GURU_TEAM_NATIVE_PROTOCOL"] = str(protocol_path)
    started = time.monotonic_ns()
    process = subprocess.run(
        argv,
        cwd=Path(request["workdir"]).resolve().parent,
        input=context if args.adapter == "claude" else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=native_environment,
    )
    boundary_stop.set()
    boundary_thread.join(timeout=1)
    timing_ms = max(0, (time.monotonic_ns() - started) // 1_000_000)
    transcript.write_text(json.dumps({
        "adapter": args.adapter,
        "native_command": args.native_command,
        "argv": argv,
        "context_path": str(context_path),
        "protocol_path": str(protocol_path),
        "native_trace_path": str(trace_path),
        "native_request_path": str(native_request_path),
        "projection_root": str(projection_root),
        "wrapper_path": str(wrapper_path),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }, indent=2), encoding="utf-8")
    if process.returncode != 0:
        return emit(response(request, "execution_error", transcript, stderr=process.stderr, timing_ms=timing_ms, native_trace=trace_path))
    try:
        public_stdout = unwrap_native_output(args.adapter, process.stdout, output_path)
        trace_events = validate_native_trace(trace_path, request_sha256, request, wrapper_path, public_stdout, protocol_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return emit(response(request, "execution_error", transcript, stderr=str(exc), timing_ms=timing_ms, native_trace=trace_path))
    return emit(response(
        request,
        "executed",
        transcript,
        stdout=public_stdout,
        stderr=process.stderr,
        trace_events=trace_events,
        timing_ms=timing_ms,
        native_trace=trace_path,
    ))


if __name__ == "__main__":
    raise SystemExit(main())
