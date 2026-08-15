from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from verify_throwaway_python_routing import runtime_checkpoint


SKILLS = (
    "guru-sync-base",
    "guru-discover-change-context",
    "guru-clarify-requirements",
    "guru-review-contract-wording",
    "guru-review-change-request",
    "guru-create-task-workspace",
)
HAPPY_CASES = {
    "guru-sync-base": "synced-route",
    "guru-discover-change-context": "context-ready-route",
    "guru-clarify-requirements": "clear-route",
    "guru-review-contract-wording": "pass-route",
    "guru-review-change-request": "ready-route",
    "guru-create-task-workspace": "created-route",
}
FORBIDDEN_RUNTIME_PARTS = {"evals", "phase0-transcript"}
FORBIDDEN_RUNTIME_NAMES = {
    "invocation.json",
    "owner-change-request.json",
    "owner-plan.json",
    "owner-prerequisites.json",
    "owner-result.json",
    "transition.json",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def operation_counts(env: dict[str, str]) -> dict[str, int]:
    path = Path(str(env.get("GURU_PHASE0_OPERATION_LOG") or ""))
    counts: dict[str, int] = {}
    if not path.is_file():
        return counts
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        operation = str(row["operation"])
        counts[operation] = counts.get(operation, 0) + 1
    return counts


def operation_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    return {
        operation: after.get(operation, 0) - before.get(operation, 0)
        for operation in sorted(set(before) | set(after))
        if after.get(operation, 0) != before.get(operation, 0)
    }


def empty_duplicate_snapshot(transition: dict[str, Any]) -> dict[str, Any]:
    value = {
        "query": "repo:example/guru-extension is:issue is:open phase0 transition",
        "checked_at": "2026-01-01T00:00:00Z",
        "target_locator": transition["target_locator"],
        "authority_content_sha256": transition["authority_content_sha256"],
        "candidates": [],
    }
    return {**value, "facts_sha256": digest(value)}


def context_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value) + b"\n").hexdigest()


def finalize_clarification_owner(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    actions = result.get("source_actions")
    actions = actions if isinstance(actions, list) else []
    for action in actions:
        if not isinstance(action, dict):
            continue
        action["payload_sha256"] = (
            digest(action["payload"])
            if isinstance(action.get("payload"), dict)
            else None
        )
        action["action_digest"] = digest({
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
        "repository_answerable_questions": result.get(
            "repository_answerable_questions"
        ),
        "clarification_rounds": result.get("clarification_rounds"),
        "open_questions": result.get("open_questions"),
        "affected_contracts": result.get("affected_contracts"),
        "reason": result.get("reason"),
    }
    result["content_identity"] = {
        "target_sha256": digest(result.get("review_target")),
        "disposition_sha256": digest(result.get("target_disposition")),
        "content_sha256": digest(content),
        "context_sha256": digest(result.get("context_evidence")),
        "scope_sha256": digest(result.get("scope_proposals")),
        "action_sha256": digest(actions),
        "payload_sha256": digest([
            action.get("payload") if isinstance(action, dict) else None
            for action in actions
        ]),
        "result_sha256": digest(unsigned),
    }
    return result


def clarification_typed_output(
    owner: dict[str, Any],
    public_input: dict[str, Any],
    transition: dict[str, Any],
) -> dict[str, Any]:
    exit_id = owner["typed_exit"]
    if exit_id == "clear":
        identity = owner["content_identity"]
        disposition = owner["target_disposition"]
        clarity_transition = {
            **copy.deepcopy(transition),
            "transition_id": f"clarity_current:{identity['result_sha256'][:24]}",
            "stage": "clarity_current",
            "clarity_result_sha256": identity["result_sha256"],
            "target_content_sha256": identity["content_sha256"],
            "clarity": {
                "facts_sha256": identity["result_sha256"],
                "target_sha256": identity["target_sha256"],
                "disposition_sha256": identity["disposition_sha256"],
                "content_sha256": identity["content_sha256"],
                "scope_sha256": identity["scope_sha256"],
            },
            "target_disposition": {
                "disposition_sha256": disposition["disposition_digest"],
                "duplicate_facts_sha256": disposition["duplicate_facts_sha256"],
            },
        }
        clarity_transition.pop("authority_content_sha256", None)
        return {
            "exit_id": "clear",
            "resume_target": owner["invocation_context"]["resume_target"],
            "target_disposition": "retained",
            "continuation_id": public_input["continuation_id"],
            "transition": clarity_transition,
        }
    if exit_id == "needs_context":
        base = copy.deepcopy(transition["base"])
        return {
            "exit_id": "needs_context",
            "handoff_profile": "pre_task",
            "handoff_mode": public_input["mode"],
            "handoff_repo_locator": transition["repo_locator"],
            "handoff_base_branch": base["selected_base"],
            "handoff_continuation_id": public_input["continuation_id"],
            "transition": {
                "schema_version": "1.0",
                "transition_id": (
                    "base_current:" + base["post_sync_resolution_sha256"][:24]
                ),
                "stage": "base_current",
                "mode": public_input["mode"],
                "repo_locator": transition["repo_locator"],
                "base": base,
            },
        }
    if exit_id == "refresh_context":
        output = {
            "exit_id": "refresh_context",
            "handoff_mode": public_input["mode"],
            "handoff_repo_root": transition["repo_locator"],
            "handoff_route": "repo_change",
        }
        if transition["base"].get("source") == "explicit":
            output["handoff_base_branch"] = transition["base"]["selected_base"]
        return output
    raise RuntimeError(f"unsupported transcript clarification output: {exit_id}")


def wording_change_request_source(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_kind": "issue",
        "identity": issue["url"],
        "title": issue["title"],
        "body": issue["body"],
        "updated_at": issue["updatedAt"],
    }


def readiness_reentry_transition(
    wording_transition: dict[str, Any], exit_id: str
) -> dict[str, Any]:
    transition = copy.deepcopy(wording_transition)
    transition.pop("wording_facts_sha256", None)
    transition.pop("wording", None)
    if exit_id == "review_wording":
        transition["stage"] = "clarity_current"
        transition["transition_id"] = (
            "clarity_current:" + transition["clarity_result_sha256"][:24]
        )
        return transition
    raise RuntimeError(f"unsupported readiness re-entry transition: {exit_id}")


def run(
    argv: list[str | Path],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    stdin: dict[str, Any] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        [str(item) for item in argv],
        cwd=cwd,
        env=env,
        input=json.dumps(stdin, ensure_ascii=False) if stdin is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and process.returncode != 0:
        diagnostics = "\n".join(
            value for value in (process.stderr.strip(), process.stdout.strip()) if value
        )
        raise RuntimeError(
            f"command failed ({process.returncode}): {' '.join(map(str, argv))}\n"
            f"{diagnostics}"
        )
    return process


def json_stdout(process: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{label} returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} returned a non-object JSON root")
    return payload


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected a JSON object at {path}")
    return payload


def assert_forbidden_runtime_absent(root: Path) -> None:
    runtime = root / ".trellis/.runtime/guru-team"
    if not runtime.exists():
        return
    forbidden = []
    for path in runtime.rglob("*"):
        relative = path.relative_to(runtime)
        if (
            FORBIDDEN_RUNTIME_PARTS.intersection(relative.parts)
            or (path.is_file() and path.name in FORBIDDEN_RUNTIME_NAMES)
            or (
                path.is_file()
                and any(token in path.name for token in ("owner-", "prerequisite", "transition"))
            )
        ):
            forbidden.append(relative.as_posix())
    if forbidden:
        raise RuntimeError(
            "six-step transcript found forbidden private runtime material: "
            + ", ".join(sorted(forbidden))
        )


def stage_transcript_owner_repo(
    installed_repo: Path,
    chain_root: Path,
) -> tuple[Path, dict[str, str]]:
    root = chain_root / "owner-repo"
    root.mkdir(parents=True)
    scripts = installed_repo / ".trellis/scripts"
    workflow = installed_repo / ".trellis/workflow.md"
    extension_path = installed_repo / ".trellis/guru-team/extension.json"
    if not scripts.is_dir() or scripts.is_symlink() or not workflow.is_file():
        raise RuntimeError("installed Trellis owner inputs are unavailable")
    extension = load_json(extension_path)
    managed_assets = (extension.get("install") or {}).get("managed_assets")
    skill_files = (extension.get("skill_packages") or {}).get("files")
    if (
        not isinstance(managed_assets, list)
        or not managed_assets
        or not isinstance(skill_files, list)
        or not skill_files
    ):
        raise RuntimeError("installed Guru Team asset inventory is unavailable")

    (root / ".trellis").mkdir()
    shutil.copytree(
        scripts,
        root / ".trellis/scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copy2(workflow, root / ".trellis/workflow.md")
    inventory: list[tuple[str, str | None]] = []
    for raw in managed_assets:
        inventory.append((raw, None))
    for row in skill_files:
        if not isinstance(row, dict):
            raise RuntimeError("installed Skill inventory contains a non-object")
        inventory.append((row.get("path"), row.get("sha256")))
    copied: set[str] = set()
    for raw, expected_sha256 in inventory:
        if not isinstance(raw, str):
            raise RuntimeError("installed Guru Team asset inventory contains a non-path")
        relative = Path(raw)
        if (
            relative.is_absolute()
            or not relative.parts
            or ".." in relative.parts
        ):
            raise RuntimeError("installed Guru Team asset inventory contains an unsafe path")
        if raw in copied:
            continue
        copied.add(raw)
        source = installed_repo / relative
        target = root / relative
        if (
            not source.is_file()
            or source.is_symlink()
            or (
                expected_sha256 is not None
                and (
                    not isinstance(expected_sha256, str)
                    or digest(source.read_bytes()) != expected_sha256
                )
            )
        ):
            raise RuntimeError(f"installed Guru Team asset is unavailable: {raw}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    worktrees = chain_root / "owner-worktrees"
    config = root / ".trellis/guru-team/config.yml"
    config.write_text(
        f"workspace_mode: worktree\nworktree_root: {worktrees}\n",
        encoding="utf-8",
    )
    (root / ".gitignore").write_text(
        ".trellis/.runtime/\n__pycache__/\n*.py[cod]\n",
        encoding="utf-8",
    )
    for relative, content in {
        "docs/requirements.md": "# Requirements\n\nCurrent Phase 0 public transition contract.\n",
        "trellis/runtime.py": "PHASE0_PUBLIC_TRANSITION = 'current'\n",
        "trellis/test_runtime.py": "def test_phase0_public_transition():\n    assert True\n",
    }.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    run(["git", "init", "-q", "-b", "main"], cwd=root)
    run(["git", "config", "user.email", "phase0-transcript@example.invalid"], cwd=root)
    run(["git", "config", "user.name", "Phase0 Transcript"], cwd=root)
    run(["git", "add", "."], cwd=root)
    run(["git", "commit", "-q", "-m", "install Phase 0 transcript owner"], cwd=root)
    head = run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    run(["git", "update-ref", "refs/remotes/origin/main", head], cwd=root)
    run(
        [
            "git", "symbolic-ref", "refs/remotes/origin/HEAD",
            "refs/remotes/origin/main",
        ],
        cwd=root,
    )
    run(
        ["git", "remote", "add", "origin", "https://github.com/example/guru-extension.git"],
        cwd=root,
    )

    runtime_assets = root / ".trellis/guru-team/runtime"
    bootstrap = runtime_assets / "bootstrap.py"
    if not bootstrap.is_file():
        raise RuntimeError("installed managed Python bootstrap is unavailable")
    runtime = json_stdout(
        run(
            [
                sys.executable,
                bootstrap,
                "--repo",
                root,
                "--runtime-assets",
                runtime_assets,
                "--python",
                sys.executable,
                "--json",
            ],
            cwd=root,
        ),
        "transcript owner managed runtime bootstrap",
    )
    if runtime.get("status") != "ok" or not runtime.get("runtime_identity"):
        raise RuntimeError("transcript owner managed runtime bootstrap failed")

    fake_bin = chain_root / "fake-bin"
    fake_bin.mkdir()
    managed_shebang = f"#!{sys.executable}\n"
    operation_log = chain_root / "operation-counts.jsonl"
    issue_body = chain_root / "issue-body.txt"
    issue_body.write_text(
        "The current Intake workflow must preserve one public transition chain.",
        encoding="utf-8",
    )
    fake_gh = fake_bin / "gh"
    fake_gh.write_text(
        managed_shebang
        +
        "import json,sys\n"
        "from pathlib import Path\n"
        f"issue_body_path={str(issue_body)!r}\n"
        f"operation_log_path={str(operation_log)!r}\n"
        "args=sys.argv[1:]\n"
        "def count(operation):\n"
        " with Path(operation_log_path).open('a',encoding='utf-8') as stream:\n"
        "  stream.write(json.dumps({'adapter':'gh','operation':operation},sort_keys=True)+'\\n')\n"
        "if args[:2]==['auth','status']: raise SystemExit(0)\n"
        "if args[:2]==['api','user']:\n"
        " count('prerequisite.project')\n"
        " print(json.dumps({'login':'stage0-transcript'})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " count('issue.get')\n"
        " number=int(args[2])\n"
        " if number != 145: raise SystemExit(2)\n"
        " body=Path(issue_body_path).read_text(encoding='utf-8')\n"
        " print(json.dumps({'number':145,'url':'https://github.com/example/guru-extension/issues/145',"
        "'state':'OPEN','updatedAt':'2026-01-01T00:00:00Z',"
        "'title':'Phase 0 public transition transcript',"
        "'body':body,"
        "'comments':[],'assignees':[{'login':'stage0-transcript'}],'labels':[]}))\n"
        " raise SystemExit(0)\n"
        "if len(args)>=2 and args[:2]==['issue','list']:\n"
        " count('issue.search')\n"
        " print('[]'); raise SystemExit(0)\n"
        "if len(args)>=2 and args[:2]==['api','repos/example/guru-extension/issues/145/comments']:\n"
        " count('issue.comments.list')\n"
        " print('[]'); raise SystemExit(0)\n"
        "print('unsupported transcript gh invocation',file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    fake_gh.chmod(0o755)
    real_git = shutil.which("git")
    if real_git is None:
        raise RuntimeError("git is unavailable for the transcript owner")
    fake_git = fake_bin / "git"
    fake_git.write_text(
        managed_shebang
        +
        "import json,os,subprocess,sys\n"
        "from pathlib import Path\n"
        f"real_git={real_git!r}\n"
        f"operation_log_path={str(operation_log)!r}\n"
        "args=sys.argv[1:]\n"
        "def count(operation):\n"
        " with Path(operation_log_path).open('a',encoding='utf-8') as stream:\n"
        "  stream.write(json.dumps({'adapter':'git','operation':operation},sort_keys=True)+'\\n')\n"
        "if args and args[0]=='fetch':\n"
        " rows=Path(operation_log_path).read_text(encoding='utf-8').splitlines() if Path(operation_log_path).is_file() else []\n"
        " previous=json.loads(rows[-1]).get('operation') if rows else None\n"
        " count('workspace.base.fetch' if previous=='workspace.mutation_boundary_recheck' else 'base.fetch')\n"
        " raise SystemExit(0)\n"
        "if args==['ls-remote','--symref','origin','HEAD']:\n"
        " count('base.resolve')\n"
        " result=subprocess.run([real_git,'rev-parse','--verify','refs/remotes/origin/main'],"
        "text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)\n"
        " if result.returncode: raise SystemExit(result.returncode)\n"
        " print('ref: refs/heads/main\\tHEAD')\n"
        " print(result.stdout.strip()+'\\tHEAD'); raise SystemExit(0)\n"
        "if args==['ls-remote','--heads','origin','main']:\n"
        " count('base.check')\n"
        " result=subprocess.run([real_git,'rev-parse','--verify','refs/remotes/origin/main'],"
        "text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)\n"
        " if result.returncode: raise SystemExit(result.returncode)\n"
        " print(result.stdout.strip()+'\\trefs/heads/main'); raise SystemExit(0)\n"
        "os.execv(real_git,[real_git,*args])\n",
        encoding="utf-8",
    )
    fake_git.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GURU_PHASE0_OPERATION_LOG": str(operation_log),
    }
    assert_forbidden_runtime_absent(root)
    return root, env


def installed_eval_runs(
    installed_repo: Path, work_root: Path, semantic_grading: Path
) -> tuple[dict[tuple[str, str], dict[str, Any]], list[dict[str, Any]]]:
    runner = installed_repo / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
    records: dict[tuple[str, str], dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for skill_id in SKILLS:
        run_root = work_root / "exit-families" / skill_id
        result = json_stdout(
            run(
                [
                    runner,
                    "--root",
                    installed_repo,
                    "--mode",
                    "installed",
                    "--skill",
                    skill_id,
                    "--adapter",
                    "shared",
                    "--run-root",
                    run_root,
                    "--semantic-grading",
                    semantic_grading,
                    "--json",
                ],
                cwd=installed_repo,
            ),
            f"installed eval {skill_id}",
        )
        if result.get("status") != "passed":
            raise RuntimeError(f"installed eval failed for {skill_id}: {result}")
        for case in result.get("cases", []):
            if not isinstance(case, dict) or case.get("status") != "passed":
                raise RuntimeError(f"installed eval case failed for {skill_id}: {case}")
            case_id = str(case.get("case_id") or "")
            transcript_path = Path(str(case.get("transcript_locator") or ""))
            transcript = load_json(transcript_path)
            trace = load_json(Path(str(transcript.get("native_trace_path") or "")))
            invokes = [
                event
                for event in trace.get("events", [])
                if isinstance(event, dict) and event.get("kind") == "invoke"
            ]
            if len(invokes) != 1:
                raise RuntimeError(f"{skill_id}/{case_id} did not invoke one public wrapper")
            invocation = invokes[0]
            argv = invocation.get("argv")
            if not isinstance(argv, list) or argv[-2:] != ["--invocation", "-"]:
                raise RuntimeError(f"{skill_id}/{case_id} did not use exact --invocation -")
            if any(
                item in argv
                for item in (
                    "--owner-result",
                    "--owner-prerequisites",
                    "--owner-change-request",
                    "--owner-plan",
                )
            ):
                raise RuntimeError(f"{skill_id}/{case_id} used a hidden owner locator")
            actual = json.loads(str(transcript.get("stdout") or ""))
            actual_exit = actual.get("exit_id") if isinstance(actual, dict) else None
            expected_exit = case.get("actual_exit")
            if actual_exit != expected_exit:
                raise RuntimeError(
                    f"{skill_id}/{case_id} expected-vs-actual assertion failed after stdout"
                )
            if not any(
                isinstance(check, dict)
                and check.get("id") == "actual-exit-output-schema"
                and check.get("passed") is True
                for check in case.get("deterministic_results", [])
            ):
                raise RuntimeError(f"{skill_id}/{case_id} output schema was not checked")
            owner_repo = transcript_path.parent / "execution/owner-repo"
            record = {
                "skill_id": skill_id,
                "case_id": case_id,
                "actual": actual,
                "actual_exit": actual_exit,
                "argv": argv[-2:],
                "stdout_sha256": digest(str(transcript.get("stdout") or "").encode()),
                "owner_repo": owner_repo,
                "transcript": str(transcript_path),
            }
            records[(skill_id, case_id)] = record
            rows.append({
                key: value
                for key, value in record.items()
                if key not in {"actual", "owner_repo"}
            })
    return records, rows


def invoke_public(
    root: Path,
    env: dict[str, str],
    skill_id: str,
    envelope: dict[str, Any],
    expected_exit: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    argv = [
        root / ".agents/skills" / skill_id / "scripts/invoke.sh",
        "--invocation",
        "-",
    ]
    input_sha256 = digest(envelope)
    operations_before = operation_counts(env)
    process = run(argv, cwd=root, env=env, stdin=envelope)
    operations_after = operation_counts(env)
    serializer_delta = operation_delta(operations_before, operations_after)
    if envelope.get("validation_receipt") is not None and serializer_delta:
        raise RuntimeError(f"{skill_id} public serializer made live calls: {serializer_delta}")
    actual = json_stdout(process, f"public wrapper {skill_id}")
    actual_exit = actual.get("exit_id")
    if actual_exit != expected_exit:
        raise RuntimeError(
            f"{skill_id} expected {expected_exit} only after stdout, got {actual_exit}"
        )
    return actual, {
        "skill_id": skill_id,
        "argv": ["--invocation", "-"],
        "input_sha256": input_sha256,
        "actual_exit": actual_exit,
        "stdout_sha256": digest(process.stdout.encode()),
        "public_serializer_operation_delta": serializer_delta,
    }


def project_installed_output(
    root: Path,
    skill_id: str,
    exit_id: str,
    actual: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    interface = load_json(
        root
        / ".trellis/guru-team/skills/packages"
        / skill_id
        / "interface.json"
    )
    projections = (interface.get("public_contracts") or {}).get("projections")
    matches = [
        row
        for row in projections or []
        if isinstance(row, dict) and row.get("exit_id") == exit_id
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"installed {skill_id}:{exit_id} does not declare one projection"
        )
    projection = matches[0]
    if projection.get("operation") != "rename":
        raise RuntimeError("installed transcript only supports declared rename projection")
    projected: dict[str, Any] = {}
    for mapping in projection.get("mappings", []):
        if not isinstance(mapping, dict):
            raise RuntimeError("installed projection contains a non-object mapping")
        source = mapping.get("source")
        target = mapping.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            raise RuntimeError("installed projection mapping is incomplete")
        if source in actual:
            projected[target] = copy.deepcopy(actual[source])
    return projected, str(projection.get("id") or "")


def record_semantic(
    root: Path,
    env: dict[str, str],
    skill_id: str,
    script: str,
    arguments: list[str | Path],
    payload: dict[str, Any],
) -> dict[str, Any]:
    path = (
        root
        / ".trellis/guru-team/skills/packages"
        / skill_id
        / "scripts"
        / script
    )
    return json_stdout(
        run([path, *arguments], cwd=root, env=env, stdin=payload),
        f"semantic recorder {skill_id}",
    )


def assert_owner_binding(
    skill_id: str,
    public_input: dict[str, Any],
    owner_result: dict[str, Any],
) -> None:
    mode = public_input.get("mode")
    if owner_result.get("mode") != mode:
        raise RuntimeError(
            f"{skill_id} owner mode does not match the current public invocation"
        )
    profile = public_input.get("profile")
    if skill_id == "guru-clarify-requirements":
        expected_kind = {
            "initial_change_request": "initial_issue",
            "standalone_review": "standalone_review",
        }.get(profile)
        invocation = owner_result.get("invocation_context")
        invocation = invocation if isinstance(invocation, dict) else {}
        target = owner_result.get("review_target")
        target = target if isinstance(target, dict) else {}
        if (
            expected_kind is None
            or invocation.get("kind") != expected_kind
            or (expected_kind == "initial_issue" and target.get("kind") != "issue")
            or target.get("url") != public_input.get("target_locator")
        ):
            raise RuntimeError(
                "guru-clarify-requirements owner profile does not match the current public invocation"
            )
    elif skill_id == "guru-review-contract-wording":
        scope = owner_result.get("scope")
        scope = scope if isinstance(scope, dict) else {}
        owner_target = str(scope.get("identity") or "").removeprefix(
            "change_request:"
        )
        if (
            owner_result.get("profile") != profile
            or owner_target != public_input.get("target_locator")
        ):
            raise RuntimeError(
                "guru-review-contract-wording owner profile does not match the current public invocation"
            )
    elif skill_id == "guru-review-change-request":
        target = owner_result.get("target")
        target = target if isinstance(target, dict) else {}
        expected_kind = {
            "current_issue": "existing_issue",
            "proposed_draft": "proposed_draft",
            "standalone_request": "standalone_request",
        }.get(profile)
        if (
            expected_kind is None
            or target.get("kind") != expected_kind
            or target.get("url") != public_input.get("target_locator")
        ):
            raise RuntimeError(
                "guru-review-change-request owner profile does not match the current public invocation"
            )


def live_issue(root: Path, env: dict[str, str]) -> dict[str, Any]:
    repo = "example/guru-extension"
    number = 145
    issue = json_stdout(
        run(
            [
                "gh", "issue", "view", str(number), "--repo", repo, "--json",
                "number,url,state,updatedAt,title,body",
            ],
            cwd=root,
            env=env,
        ),
        "live issue authority",
    )
    url = f"https://github.com/{repo}/issues/{number}"
    if issue.get("number") != number or issue.get("url") != url:
        raise RuntimeError("live issue authority returned a different identity")
    return issue


def live_issue_comments(root: Path, env: dict[str, str]) -> list[dict[str, Any]]:
    value = json.loads(
        run(
            ["gh", "api", "repos/example/guru-extension/issues/145/comments"],
            cwd=root,
            env=env,
        ).stdout
    )
    if not isinstance(value, list):
        raise RuntimeError("live issue comments did not return one array")
    return value


def context_owner_for_issue(
    root: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    repo = "example/guru-extension"
    number = 145
    live = live_issue(root, env)
    url = f"https://github.com/{repo}/issues/{number}"
    if live.get("number") != number or live.get("url") != url:
        raise RuntimeError("live issue authority returned a different identity")
    candidates = json.loads(
        run(
            ["gh", "issue", "list", "--repo", repo, "--state", "open", "--search", "phase0 transition", "--json", "number,url,state,updatedAt,title,body"],
            cwd=root,
            env=env,
        ).stdout
    )
    if not isinstance(candidates, list):
        raise RuntimeError("duplicate issue search returned a non-array JSON root")
    issue = {
        "repo": repo,
        "number": number,
        "url": url,
        "state": str(live.get("state") or "").casefold(),
        "updated_at": live.get("updatedAt"),
        "body_sha256": hashlib.sha256(
            str(live.get("body") or "").encode("utf-8")
        ).hexdigest(),
    }
    issue["facts_sha256"] = context_digest(issue)
    change_input = {
        "issue_refs": ["#145"],
        "pr_refs": [],
        "branches": [],
        "paths": ["docs/requirements.md"],
        "commands": ["guru-sync-base"],
        "config_keys": [],
        "schema_fields": [],
        "symbols": ["PHASE0_PUBLIC_TRANSITION"],
        "terms": ["public transition"],
        "queries": ["Phase 0 public transition chain"],
    }
    evidence = {
        "docs": "docs/requirements.md",
        "code_contracts": "trellis/runtime.py",
        "tests": "trellis/test_runtime.py",
    }
    current_rows = {
        "docs": [{
            "path": evidence["docs"],
            "blob_or_content_sha256": "",
            "purpose": "Review the durable Phase 0 behavior.",
            "observation": "The installed requirement declares one public transition chain.",
            "query_clues": ["public transition"],
        }],
        "code_contracts": [{
            "path": evidence["code_contracts"],
            "blob_or_content_sha256": "",
            "purpose": "Review the current runtime ownership boundary.",
            "observation": "The installed runtime owns deterministic transition validation.",
            "query_clues": ["PHASE0_PUBLIC_TRANSITION"],
        }],
        "tests": [{
            "path": evidence["tests"],
            "blob_or_content_sha256": "",
            "purpose": "Review the current public transcript test surface.",
            "observation": "The repository contains a current Phase 0 test contract.",
            "query_clues": ["test_phase0_public_transition"],
        }],
    }
    for group, path in evidence.items():
        blob = run(["git", "rev-parse", f"HEAD:{path}"], cwd=root, env=env).stdout.strip()
        current_rows[group][0]["blob_or_content_sha256"] = blob
    preview_args: list[str | Path] = [
        root
        / ".trellis/guru-team/skills/packages/guru-discover-change-context/scripts/preview-change-context-history.sh",
        "--root",
        root,
        "--query-json",
        json.dumps(change_input, ensure_ascii=False, sort_keys=True),
    ]
    preview = json_stdout(run(preview_args, cwd=root, env=env), "context history preview")
    return {
        "schema_version": "2.0",
        "skill_id": "guru-discover-change-context",
        "generated_at": "2026-01-01T00:00:00Z",
        "mode": "workflow",
        "typed_exit": "context_ready",
        "repository": {
            "repo": repo,
            "selected_base": "main",
            "decision_branch": "main",
        },
        "change_input": change_input,
        "live_change": {
            "kind": "issue",
            "identity": issue["url"],
            "state": issue["state"],
            "updated_at": issue["updated_at"],
            "body_sha256": issue["body_sha256"],
            "facts_sha256": issue["facts_sha256"],
            "issue_binding": None,
        },
        "duplicate_search": {
            "query": "repo:example/guru-extension is:issue is:open phase0 transition",
            "checked_at": "2026-01-01T00:00:00Z",
            "scope": "open_issues",
            "candidates": candidates,
        },
        "current_state": {
            "sequence_trace": [
                "fresh_base", "live_change", "duplicates", "docs",
                "code_contracts", "tests", "query_clues", "history_preview",
            ],
            **current_rows,
            "observations": [
                "Current installed docs, runtime and tests are sufficient before archived history."
            ],
        },
        "canonical_query": preview["canonical_query"],
        "history_preview": preview,
        "history_review": {
            "selected_candidates": [],
            "excluded_candidates": [],
            "deep_reads": [],
        },
        "mem_review": {
            "status": "not_needed",
            "reason": "Current installed and live authority evidence is sufficient.",
            "load_bearing_question": None,
            "exhausted_sources": {
                "task_artifacts": False,
                "current_docs_code_tests": False,
                "github": False,
                "git_history": False,
            },
            "summary": None,
        },
        "ai_review_gate": {
            "status": "passed",
            "reviewer": "phase0-transcript-reviewer",
            "reviewed_scope": [
                "live issue authority", "installed docs", "installed runtime",
                "installed tests", "current history preview",
            ],
            "excluded_scope": ["workspace mutation"],
            "relevance": "The current evidence directly describes the Phase 0 transition.",
            "sufficiency": "Live authority and current installed evidence are sufficient.",
            "conflicts": [],
            "reusable": ["installed public wrappers"],
            "not_reusable": ["private eval owner material"],
            "load_bearing_conclusions": [{
                "conclusion": "The public transition chain is the current implementation target.",
                "evidence_refs": ["docs/requirements.md", "trellis/runtime.py"],
            }],
            "findings": [],
            "reason": "All required semantic context dimensions passed.",
        },
        "error": None,
    }


def checked_context_owner_for_issue(
    root: Path,
    env: dict[str, str],
    transition: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    authored = context_owner_for_issue(root, env)
    base = transition["base"]
    authored["base_evidence"] = {
        "schema_id": "guru-base-sync-result-1.0",
        "sync_result": base_sync_payload(transition),
        "remote": base["remote"],
        "base_head": base["remote_base_head"],
        "decision_head": base["decision_head"],
        "local_head": base["local_base_head"],
        "remote_head": base["remote_base_head"],
        "post_sync_resolution_sha256": base["post_sync_resolution_sha256"],
        "clean": True,
    }
    recorded = record_semantic(
        root,
        env,
        "guru-discover-change-context",
        "record-context-discovery.sh",
        ["--mode", "workflow", "--input", "-"],
        authored,
    )
    checked = record_semantic(
        root,
        env,
        "guru-discover-change-context",
        "check-context-discovery.sh",
        [
            "--input", "-", "--expected-result-sha256",
            recorded["result_identity"]["result_sha256"],
        ],
        recorded,
    )
    if checked.get("status") != "passed" or checked.get("typed_exit") != "context_ready":
        raise RuntimeError("current context owner did not pass its production checker")
    return recorded, checked


def clarification_owner_for_issue(
    root: Path,
    env: dict[str, str],
    transition: dict[str, Any],
    duplicate_snapshot: dict[str, Any],
    typed_exit: str = "clear",
) -> tuple[dict[str, Any], dict[str, Any]]:
    issue = live_issue(root, env)
    if transition.get("target_locator") != issue.get("url"):
        raise RuntimeError("clarification transition does not target the current live issue")
    body_sha256 = hashlib.sha256(str(issue.get("body") or "").encode()).hexdigest()
    target = {
        "kind": "issue",
        "repo": "example/guru-extension",
        "issue_number": 145,
        "url": issue.get("url"),
        "state": str(issue.get("state") or "").casefold(),
        "updated_at": issue.get("updatedAt"),
        "body_sha256": body_sha256,
    }
    target["facts_sha256"] = context_digest(target)
    owner = {
        "schema_version": "2.0",
        "skill_id": "guru-clarify-requirements",
        "generated_at": "2026-01-01T00:00:00Z",
        "mode": "workflow",
        "typed_exit": "clear",
        "invocation_context": {
            "kind": "initial_issue",
            "caller": "guru-discover-change-context:context_ready",
            "task_locator": None,
            "resume_target": "guru-review-contract-wording",
        },
        "review_target": target,
        "target_disposition": {
            "disposition": "keep_current_open_issue",
            "duplicate_query": "repo:example/guru-extension is:issue is:open phase0 transition",
            "duplicate_checked_at": "2026-01-01T00:00:00Z",
            "duplicate_candidates": [],
            "duplicate_facts_sha256": duplicate_snapshot["facts_sha256"],
            "selected_issue": None,
            "original_target_role": "primary",
            "decision_summary": "The current open issue remains the primary delivery authority.",
            "disposition_digest": "0" * 64,
        },
        "context_evidence": {
            "status": "current",
            "evidence_refs": [transition["context_result_sha256"]],
            "missing_reason": None,
        },
        "confirmed_facts": [{
            "fact_id": "delivery_goal",
            "summary": "The live issue defines one bounded Phase 0 transition delivery.",
            "evidence_refs": ["review_target.body_sha256"],
            "affected_contracts": ["requirements", "workflow routing"],
        }],
        "repository_answerable_questions": [{
            "question_id": "current_owner",
            "question": "Which installed contract owns the transition chain?",
            "status": "answered",
            "evidence_refs": [transition["context_result_sha256"]],
            "answer_summary": "The installed Phase 0 package graph is the current owner.",
            "missing_reason": None,
        }],
        "clarification_rounds": [],
        "open_questions": [],
        "scope_proposals": [],
        "source_actions": [{
            "action_id": "no_source_change",
            "kind": "none",
            "target": None,
            "payload": None,
            "preimage_sha256": None,
            "payload_sha256": None,
            "action_digest": "0" * 64,
            "status": "not_required",
            "mutation_evidence": None,
        }],
        "mutation_results": [],
        "active_task_evidence": None,
        "ai_review_gate": {
            "status": "passed",
            "reviewed_scope": [
                "live issue authority", "actual context transition", "open questions",
            ],
            "excluded_scope": ["workspace mutation"],
            "load_bearing_conclusions": [
                "The current requirement is complete and ready for wording review."
            ],
            "findings": [],
            "summary": "Current authority and prior transition support a clear route.",
        },
        "affected_contracts": ["requirements", "workflow routing"],
        "content_identity": {},
        "reason": "All load-bearing requirements are confirmed by current evidence.",
        "consumer": {"kind": "workflow", "id": "guru-requirements-clear-router"},
        "error": None,
    }
    if typed_exit == "needs_context":
        owner.update({
            "typed_exit": "needs_context",
            "context_evidence": {
                "status": "missing",
                "evidence_refs": [transition["context_result_sha256"]],
                "missing_reason": (
                    "The current authoring pass requires a fresh repository context read."
                ),
            },
            "reason": "A current context read is required before wording review.",
            "consumer": {
                "kind": "skill",
                "id": "guru-discover-change-context",
            },
        })
    elif typed_exit == "refresh_context":
        owner.update({
            "typed_exit": "refresh_context",
            "context_evidence": {
                "status": "stale",
                "evidence_refs": [transition["context_result_sha256"]],
                "missing_reason": (
                    "Live issue authority changed after the context transition."
                ),
            },
            "reason": "Changed live authority requires a new base-bound context read.",
            "consumer": {"kind": "skill", "id": "guru-sync-base"},
        })
    elif typed_exit != "clear":
        raise RuntimeError(f"unsupported transcript clarification exit: {typed_exit}")
    owner["target_disposition"]["duplicate_query"] = duplicate_snapshot["query"]
    owner["target_disposition"]["duplicate_checked_at"] = duplicate_snapshot["checked_at"]
    owner["target_disposition"]["duplicate_candidates"] = [
        {**candidate, "identity": f"#{candidate['number']}", "state": "open", "decision": "rejected", "reason": "The candidate does not replace the current delivery authority."}
        for candidate in duplicate_snapshot["candidates"]
    ]
    owner = finalize_clarification_owner(owner)
    recorded = record_semantic(
        root,
        env,
        "guru-clarify-requirements",
        "record-requirements-clarification.sh",
        ["--mode", "workflow", "--input", "-"],
        owner,
    )
    checked = record_semantic(
        root,
        env,
        "guru-clarify-requirements",
        "check-requirements-clarification.sh",
        [
            "--input", "-", "--expected-result-sha256",
            recorded["content_identity"]["result_sha256"],
        ],
        recorded,
    )
    if checked.get("status") != "passed" or checked.get("typed_exit") != typed_exit:
        raise RuntimeError("current clarification owner did not pass its production checker")
    return recorded, checked


def wording_owner_for_issue(
    root: Path,
    env: dict[str, str],
    source_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    scanned = record_semantic(
        root,
        env,
        "guru-review-contract-wording",
        "record-contract-wording-review.sh",
        [
            "--mode", "workflow", "--profile", "change_request",
            "--change-request-input", source_path, "--scan-only",
        ],
        {},
    )
    scan = scanned["scan"]
    gate = {
        "status": "passed",
        "reviewer": "phase0-transcript-reviewer",
        "summary": "The complete fixed wording scope and current rescan were semantically reviewed.",
        "reviewed_scan_sha256": scan["scan_sha256"],
        "checked_dimensions": {
            "complete_profile_scope": True,
            "all_hits_classified": True,
            "zero_unchecked_hits": True,
            "product_semantics_preserved": True,
            "retained_reasons_sufficient": True,
            "zero_hits_not_requirement_review": True,
        },
    }
    authored = {
        "generated_at": "2026-01-01T00:00:00Z",
        "revisions": [],
        "classifications": [
            {
                "hit_id": hit["hit_id"],
                "classification": "term_definition",
                "reason": "The semantic review retained this explicit contract term.",
            }
            for hit in scan["hits"]
        ],
        "ai_review_gate": gate,
        "typed_exit": "pass",
    }
    recorded = record_semantic(
        root,
        env,
        "guru-review-contract-wording",
        "record-contract-wording-review.sh",
        [
            "--mode", "workflow", "--profile", "change_request",
            "--change-request-input", source_path, "--input", "-",
        ],
        authored,
    )
    checked = record_semantic(
        root,
        env,
        "guru-review-contract-wording",
        "check-contract-wording-review.sh",
        [
            "--change-request-input", source_path, "--input", "-",
            "--expected-facts-sha256", recorded["facts_sha256"],
        ],
        recorded,
    )
    if checked.get("status") != "passed" or checked.get("typed_exit") != "pass":
        raise RuntimeError("current wording owner did not pass its production checker")
    return recorded, checked


def readiness_owner_for_issue(
    root: Path,
    env: dict[str, str],
    transition: dict[str, Any],
    typed_exit: str = "ready",
) -> dict[str, Any]:
    issue = transition.get("readiness_source") or live_issue(root, env)
    title_sha256 = hashlib.sha256(str(issue.get("title") or "").encode()).hexdigest()
    body_sha256 = hashlib.sha256(str(issue.get("body") or "").encode()).hexdigest()
    raw_target = {
        "kind": "existing_issue",
        "repo": "example/guru-extension",
        "issue_number": 145,
        "url": issue.get("url"),
        "updated_at": issue.get("updatedAt") or issue.get("updated_at"),
        "title_sha256": title_sha256,
        "body_sha256": body_sha256,
    }
    target_identity_sha256 = digest(raw_target)
    target_content_sha256 = digest({
        "title_sha256": title_sha256,
        "body_sha256": body_sha256,
    })
    clarity = transition["clarity"]
    wording = transition["wording"]
    linkage = {
        "target_identity_sha256": target_identity_sha256,
        "target_content_sha256": target_content_sha256,
        "clarity_facts_sha256": clarity["facts_sha256"],
        "clarity_disposition_sha256": clarity["disposition_sha256"],
        "wording_facts_sha256": wording["facts_sha256"],
    }
    linkage["linkage_sha256"] = digest(linkage)
    dimension_ids = (
        "requirement_completeness",
        "delivery_unit_consistency",
        "implementation_target_evidence",
        "claimed_behavior_current",
        "current_implementation_gap",
        "docs_code_tests_consistency",
        "archived_history_constraints",
        "duplicate_reuse_validity",
        "target_authority_current",
        "prerequisite_hash_linkage",
    )
    scope = {
        "requirement_scope_basis": (
            "The reviewed draft and current prerequisites define the scope."
        ),
        "delivery_unit_id": "phase0-public-transcript",
        "close_issues": [145],
        "related_issues": [],
        "followup_issues": [],
        "duplicate_reuse_decision": "No duplicate replaces this delivery unit.",
        "implementation_target": "The Stage 0 minimal handoff package graph.",
        "current_gap": "The selected route identifies the next readiness owner.",
        "archived_constraints": [],
        "risk_boundary": ["Normal honest workflow operation only."],
        "excluded_scope": ["Workspace mutation remains downstream."],
    }
    owner = {
        "generated_at": "2026-01-01T00:00:00Z",
        "mode": "workflow",
        "target": raw_target,
        "semantic_review": {
            "dimensions": [
                {
                    "id": dimension_id,
                    "status": "passed",
                    "summary": (
                        "This readiness dimension was reviewed against current linked evidence."
                    ),
                    "evidence_refs": ["target"],
                    "affected_hashes": [target_content_sha256],
                    "finding_ids": [],
                }
                for dimension_id in dimension_ids
            ],
            "findings": [],
            "scope_conclusion": scope,
            "ai_review_gate": {
                "status": "passed",
                "reviewer": "phase0-transcript-reviewer",
                "reviewed_linkage_sha256": linkage["linkage_sha256"],
                "summary": "The complete readiness evidence was reviewed for one declared route.",
                "findings_count": 0,
                "scope_conclusion_sha256": digest(scope),
            },
        },
        "typed_exit": "ready",
        "reason": (
            "The complete existing-issue delivery unit passed semantic readiness review."
        ),
        "affected_evidence": [{
            "ref": "target",
            "sha256": target_content_sha256,
            "summary": "The current reviewed issue title and body.",
        }],
        "consumer": {"kind": "skill", "id": "guru-create-task-workspace"},
    }
    if typed_exit in {"clarify_requirements", "review_wording", "refresh_context"}:
        category = {
            "clarify_requirements": "requirement_gap",
            "review_wording": "wording_gap",
            "refresh_context": "context_stale",
        }[typed_exit]
        failed_dimension = {
            "clarify_requirements": "requirement_completeness",
            "review_wording": "claimed_behavior_current",
            "refresh_context": "target_authority_current",
        }[typed_exit]
        finding = {
            "finding_id": f"transcript-{typed_exit.replace('_', '-')}",
            "category": category,
            "summary": f"Current evidence requires the declared {typed_exit} route.",
            "blocking": True,
            "evidence_refs": ["target"],
            "affected_hashes": [target_content_sha256],
            "route_basis": "The current semantic review selected this declared consumer.",
        }
        for dimension in owner["semantic_review"]["dimensions"]:
            if dimension["id"] == failed_dimension:
                dimension.update({
                    "status": "failed",
                    "summary": finding["summary"],
                    "finding_ids": [finding["finding_id"]],
                })
        owner.update({
            "typed_exit": typed_exit,
            "reason": finding["summary"],
            "consumer": {
                "kind": "skill",
                "id": {
                    "clarify_requirements": "guru-clarify-requirements",
                    "review_wording": "guru-review-contract-wording",
                    "refresh_context": "guru-sync-base",
                }[typed_exit],
            },
        })
        owner["semantic_review"]["findings"] = [finding]
        owner["semantic_review"]["ai_review_gate"].update({
            "status": "reroute",
            "summary": finding["summary"],
            "findings_count": 1,
        })
    elif typed_exit != "ready":
        raise RuntimeError(f"unsupported transcript readiness exit: {typed_exit}")
    return owner


def checked_readiness_owner_for_issue(
    root: Path,
    env: dict[str, str],
    transition: dict[str, Any],
    source_path: Path,
    clarity_result: dict[str, Any],
    wording_result: dict[str, Any],
    typed_exit: str = "ready",
) -> tuple[dict[str, Any], dict[str, Any]]:
    transition = copy.deepcopy(transition)
    transition["readiness_source"] = load_json(source_path)
    authored = readiness_owner_for_issue(root, env, transition, typed_exit)
    clarity_identity = clarity_result["content_identity"]
    wording_content_hashes = {
        item.get("field"): item.get("content_sha256")
        for item in wording_result["scope"]["items"]
        if isinstance(item, dict)
    }
    target_content_sha256 = digest({
        "title_sha256": wording_content_hashes.get("title"),
        "body_sha256": wording_content_hashes.get("body"),
    })
    prerequisites = {
        "clarity": {
            "status": "current",
            "schema_id": "guru-requirements-clarification-2.0",
            "typed_exit": "clear",
            "payload_sha256": digest(clarity_result),
            "facts_sha256": clarity_identity["result_sha256"],
            "target_sha256": clarity_identity["target_sha256"],
            "disposition_sha256": clarity_identity["disposition_sha256"],
            "content_sha256": target_content_sha256,
            "scope_sha256": clarity_identity["scope_sha256"],
            "error_codes": [],
        },
        "wording": {
            "status": "current",
            "schema_id": "guru-contract-wording-review-1.0",
            "profile": "change_request",
            "typed_exit": "pass",
            "payload_sha256": digest(wording_result),
            "facts_sha256": wording_result["facts_sha256"],
            "scope_sha256": wording_result["scope"]["scope_sha256"],
            "scan_sha256": wording_result["scan"]["scan_sha256"],
            "target_content_sha256": target_content_sha256,
            "error_codes": [],
        },
    }
    authored["prerequisite_payloads"] = prerequisites
    recorded = record_semantic(
        root,
        env,
        "guru-review-change-request",
        "record-change-request-review.sh",
        [
            "--mode", "workflow", "--input", "-",
            "--change-request-input", source_path,
        ],
        authored,
    )
    prerequisites_path = source_path.with_name(
        f"readiness-prerequisites-{typed_exit}.json"
    )
    prerequisites_path.write_text(
        json.dumps(prerequisites, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checked = record_semantic(
        root,
        env,
        "guru-review-change-request",
        "check-change-request-review.sh",
        [
            "--input", "-", "--prerequisites-input", prerequisites_path,
            "--change-request-input", source_path,
            "--expected-facts-sha256", recorded["facts_sha256"],
        ],
        recorded,
    )
    if checked.get("status") != "passed" or checked.get("typed_exit") != typed_exit:
        raise RuntimeError("current readiness owner did not pass its production checker")
    return recorded, checked


def base_sync_payload(transition: dict[str, Any]) -> dict[str, Any]:
    base = transition["base"]
    identity = {
        "schema_version": "1.0",
        "skill_id": "guru-sync-base",
        "status": "resolved",
        "source": base["source"],
        "selected_base": base["selected_base"],
        "remote": base["remote"],
        "candidates": copy.deepcopy(base["ordered_candidates"]),
        "decision_checkout": {
            "branch": base["selected_base"],
            "head": base["decision_head"],
            "clean": True,
        },
    }
    if digest(identity) != base["post_sync_resolution_sha256"]:
        raise RuntimeError("readiness transition base provenance is inconsistent")
    payload = {
        "schema_version": "1.0",
        "skill_id": "guru-sync-base",
        "status": "synced",
        "resolution": {
            "source": base["source"],
            "selected_base": base["selected_base"],
            "remote": base["remote"],
            "candidates": copy.deepcopy(base["ordered_candidates"]),
            "resolution_sha256": base["post_sync_resolution_sha256"],
        },
        "post_sync_resolution": identity,
        "post_sync_resolution_sha256": base["post_sync_resolution_sha256"],
        "decision_checkout": {
            "branch": base["selected_base"],
            "head_before": base["decision_head"],
            "head_after": base["decision_head"],
            "clean_before": True,
            "clean_after": True,
        },
        "git": {
            "local_ref": f"refs/heads/{base['selected_base']}",
            "remote_ref": f"refs/remotes/{base['remote']}/{base['selected_base']}",
            "local_head_before": base["local_base_head"],
            "local_head_after": base["local_base_head"],
            "remote_head_after": base["remote_base_head"],
            "fetch_performed": True,
            "fast_forwarded": False,
        },
        "fresh": True,
    }
    payload["facts_sha256"] = digest(payload)
    return payload


def workspace_transition_payloads(
    transition: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    compact_target = transition["target"]
    target_kind = compact_target["kind"]
    target = {
        "kind": target_kind,
        "repo": compact_target.get("repo"),
        "issue_number": (
            compact_target.get("issue_number")
            if target_kind == "existing_issue" else None
        ),
        "url": compact_target.get("url") if target_kind == "existing_issue" else None,
        "updated_at": (
            compact_target.get("updated_at")
            if target_kind == "existing_issue" else None
        ),
        "draft_id": (
            compact_target.get("draft_id")
            if target_kind == "proposed_draft" else None
        ),
        "source_request_sha256": (
            compact_target.get("source_request_sha256")
            if target_kind in {"proposed_draft", "standalone_request"} else None
        ),
        "caller_locator": (
            compact_target.get("caller_locator")
            if target_kind == "standalone_request" else None
        ),
        "request_id": (
            compact_target.get("request_id")
            if target_kind == "standalone_request" else None
        ),
        "title_sha256": compact_target.get("title_sha256"),
        "body_sha256": compact_target.get("body_sha256"),
        "side_effect_free": target_kind != "existing_issue",
        "identity_sha256": compact_target.get("identity_sha256"),
        "content_sha256": compact_target.get("content_sha256"),
    }
    clarity_projection = transition["clarity"]
    wording_projection = transition["wording"]
    disposition = transition["target_disposition"]
    invocation_kind = {
        "existing_issue": "initial_issue",
        "proposed_draft": "proposed_draft",
        "standalone_request": "standalone_review",
    }[target_kind]
    clarity_payload = {
        "schema_version": "2.0",
        "skill_id": "guru-clarify-requirements",
        "mode": transition["mode"],
        "typed_exit": "clear",
        "invocation_context": {
            "kind": invocation_kind,
            "caller": target.get("caller_locator"),
            "task_locator": None,
            "resume_target": "guru-review-contract-wording",
        },
        "review_target": {
            "kind": "issue" if target_kind == "existing_issue" else "draft",
            "repo": target.get("repo"),
            "issue_number": target.get("issue_number"),
            "url": target.get("url"),
            "state": "open" if target_kind == "existing_issue" else "draft",
            "updated_at": target.get("updated_at"),
            "body_sha256": target.get("body_sha256"),
            "facts_sha256": clarity_projection.get("target_sha256"),
        },
        "target_disposition": {
            "disposition_digest": disposition.get("disposition_sha256"),
            "duplicate_facts_sha256": disposition.get("duplicate_facts_sha256"),
        },
        "content_identity": {
            "result_sha256": clarity_projection.get("facts_sha256"),
            "target_sha256": clarity_projection.get("target_sha256"),
            "disposition_sha256": clarity_projection.get("disposition_sha256"),
            "content_sha256": clarity_projection.get("content_sha256"),
            "context_sha256": clarity_projection.get("content_sha256"),
            "scope_sha256": clarity_projection.get("scope_sha256"),
        },
    }
    wording_payload = {
        "schema_version": "1.0",
        "skill_id": "guru-review-contract-wording",
        "profile": "change_request",
        "mode": transition["mode"],
        "typed_exit": "pass",
        "facts_sha256": wording_projection.get("facts_sha256"),
        "scope": {"scope_sha256": wording_projection.get("scope_sha256")},
        "scan": {"scan_sha256": wording_projection.get("scan_sha256")},
    }
    prerequisites = {
        "clarity": {
            "status": "current",
            "schema_id": "guru-requirements-clarification-2.0",
            "typed_exit": "clear",
            "payload_sha256": context_digest(clarity_payload),
            "facts_sha256": clarity_projection.get("facts_sha256"),
            "target_sha256": clarity_projection.get("target_sha256"),
            "disposition_sha256": clarity_projection.get("disposition_sha256"),
            "content_sha256": clarity_projection.get("content_sha256"),
            "scope_sha256": clarity_projection.get("scope_sha256"),
            "error_codes": [],
        },
        "wording": {
            "status": "current",
            "schema_id": "guru-contract-wording-review-1.0",
            "profile": "change_request",
            "typed_exit": "pass",
            "payload_sha256": context_digest(wording_payload),
            "facts_sha256": wording_projection.get("facts_sha256"),
            "scope_sha256": wording_projection.get("scope_sha256"),
            "scan_sha256": wording_projection.get("scan_sha256"),
            "target_content_sha256": wording_projection.get("target_content_sha256"),
            "error_codes": [],
        },
    }
    linkage = {
        "target_identity_sha256": target["identity_sha256"],
        "target_content_sha256": target["content_sha256"],
        "clarity_facts_sha256": prerequisites["clarity"]["facts_sha256"],
        "clarity_disposition_sha256": prerequisites["clarity"]["disposition_sha256"],
        "wording_facts_sha256": prerequisites["wording"]["facts_sha256"],
    }
    linkage["linkage_sha256"] = context_digest(linkage)
    scope = transition["scope"]
    readiness_scope = {
        "close_issues": copy.deepcopy(scope.get("close_issues")),
        "related_issues": copy.deepcopy(scope.get("related_issues")),
        "followup_issues": copy.deepcopy(scope.get("followup_issues")),
    }
    readiness = {
        "schema_version": "1.0",
        "skill_id": "guru-review-change-request",
        "mode": transition["mode"],
        "target": target,
        "prerequisites": prerequisites,
        "evidence_linkage": linkage,
        "semantic_review": {
            "scope_conclusion": readiness_scope,
            "ai_review_gate": {
                "status": "passed",
                "reviewed_linkage_sha256": linkage["linkage_sha256"],
                "scope_conclusion_sha256": context_digest(readiness_scope),
            },
        },
        "typed_exit": "ready",
        "consumer": {"kind": "skill", "id": "guru-create-task-workspace"},
        "facts_sha256": transition["readiness_facts_sha256"],
    }
    return {
        "base": base_sync_payload(transition),
        "clarity": clarity_payload,
        "wording": wording_payload,
        "readiness": readiness,
    }


def workspace_prerequisite(
    key: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    identities = {
        "base": ("guru-sync-base", "guru-base-sync-result-1.0", "synced"),
        "clarity": (
            "guru-clarify-requirements",
            "guru-requirements-clarification-2.0",
            "clear",
        ),
        "wording": (
            "guru-review-contract-wording",
            "guru-contract-wording-review-1.0",
            "pass",
        ),
        "readiness": (
            "guru-review-change-request",
            "guru-change-request-review-1.0",
            "ready",
        ),
    }
    skill_id, schema_id, typed_exit = identities[key]
    if key == "base":
        facts = payload["facts_sha256"]
        content = None
        linkage = None
    elif key == "clarity":
        identity = payload["content_identity"]
        facts = identity["result_sha256"]
        content = identity["content_sha256"]
        linkage = identity["context_sha256"]
    elif key == "wording":
        facts = payload["facts_sha256"]
        content = payload["scope"]["scope_sha256"]
        linkage = payload["scan"]["scan_sha256"]
    else:
        facts = payload["facts_sha256"]
        content = payload["target"]["content_sha256"]
        linkage = payload["evidence_linkage"]["linkage_sha256"]
    return {
        "skill_id": skill_id,
        "schema_id": schema_id,
        "typed_exit": typed_exit,
        "artifact": f"call-local:{key}",
        "payload_sha256": context_digest(payload),
        "facts_sha256": facts,
        "content_sha256": content,
        "linkage_sha256": linkage,
    }


def workspace_plan_for_transition(
    root: Path,
    env: dict[str, str],
    transition: dict[str, Any],
) -> dict[str, Any]:
    payloads = workspace_transition_payloads(transition)
    issue = live_issue(root, env)
    target = transition["target"]
    if (
        target.get("kind") != "existing_issue"
        or target.get("issue_number") != issue.get("number")
        or target.get("url") != issue.get("url")
    ):
        raise RuntimeError("workspace authoring target does not match live authority")
    title = str(issue.get("title") or "")
    scope_ref = {
        "number": 145,
        "url": str(issue["url"]),
        "title": title,
        "reason": "The current readiness scope identifies this delivery authority.",
    }
    scope = {
        "primary": copy.deepcopy(scope_ref),
        "close": [copy.deepcopy(scope_ref)],
        "related": [],
        "followup": [],
    }
    scope["scope_sha256"] = context_digest(scope)
    base_payload = payloads["base"]
    base_resolution = base_payload["resolution"]
    base_git = base_payload["git"]
    task_slug = "145-phase0-public-transcript"
    task_dir = (
        ".trellis/tasks/"
        + datetime.datetime.now().astimezone().strftime("%m-%d-")
        + task_slug
    )
    plan = {
        "schema_version": "2.0",
        "skill_id": "guru-create-task-workspace",
        "generated_at": "2026-01-01T00:00:00Z",
        "mode": transition["mode"],
        "invocation": {
            "caller": "guru-review-change-request:ready",
            "target_kind": "existing_issue",
            "action_scope": "workspace_and_task_mutation",
            "resume_identity": transition["continuation_id"],
        },
        "prerequisites": {
            key: workspace_prerequisite(key, payload)
            for key, payload in payloads.items()
        },
        "target": {
            "kind": "existing_issue",
            "repo": target["repo"],
            "issue_number": target["issue_number"],
            "url": target["url"],
            "state": "open",
            "updated_at": target["updated_at"],
            "title_sha256": target["title_sha256"],
            "body_sha256": target["body_sha256"],
            "draft": None,
            "disposition_sha256": transition["target_disposition"]["disposition_sha256"],
            "duplicate_decision_sha256": transition["target_disposition"]["duplicate_facts_sha256"],
            "created_issue_binding_sha256": None,
            "created_issue_result": None,
        },
        "scope": scope,
        "base": {
            "selected_base": base_resolution["selected_base"],
            "remote": base_resolution["remote"],
            "base_ref": base_git["remote_ref"],
            "decision_head": base_payload["decision_checkout"]["head_after"],
            "local_head": base_git["local_head_after"],
            "remote_head": base_git["remote_head_after"],
            "post_sync_resolution_sha256": base_payload["post_sync_resolution_sha256"],
            "sync_facts_sha256": base_payload["facts_sha256"],
        },
        "naming": {
            "branch_name": "feat/145-phase0-public-transcript",
            "workspace_slug": task_slug,
            "task_slug": task_slug,
            "task_title": "#145 Phase 0 public transcript",
            "reason": "Names bind the live issue to this independent transcript chain.",
            "branch_disposition": "create_new",
            "workspace_disposition": "create_new",
            "task_disposition": "create_new",
        },
        "assignee": {
            "login": "stage0-transcript",
            "source": "single_issue_assignee",
            "candidates": ["stage0-transcript"],
            "resolution_evidence": "The live issue has exactly one current assignee.",
        },
        "side_effects": {
            "operations": [
                "create_branch", "create_worktree", "create_task",
                "write_task_artifacts", "write_runtime_mappings",
            ],
            "task_artifacts": [f"{task_dir}/issue-scope-ledger.json"],
            "runtime_mappings": [
                f".trellis/.runtime/guru-team/workspaces/{task_slug}.json",
                f".trellis/.runtime/guru-team/tasks/{task_slug}.json",
            ],
            "command_argv": ["create-task-workspace", "--invocation", "-"],
            "stop_after": "created_workspace",
        },
        "ai_review_gate": {
            "status": "passed",
            "reviewer": "phase0-transcript-reviewer",
            "reviewed_plan_sha256": "0" * 64,
            "summary": "Live target, current transition, names and side effects were reviewed.",
            "evidence": [
                "The actual readiness transition is current.",
                "The live issue has one assignee and one close scope.",
            ],
        },
        "freshness": {
            "captured_at": "2026-01-01T00:00:00Z",
            "reviewable_plan_sha256": "0" * 64,
            "plan_sha256": "0" * 64,
        },
    }
    reviewable = {
        key: copy.deepcopy(plan.get(key))
        for key in (
            "schema_version", "skill_id", "mode", "invocation", "prerequisites",
            "target", "scope", "base", "naming", "assignee", "side_effects",
        )
    }
    reviewable_sha256 = digest(reviewable)
    plan["ai_review_gate"]["reviewed_plan_sha256"] = reviewable_sha256
    plan["freshness"]["reviewable_plan_sha256"] = reviewable_sha256
    projection = copy.deepcopy(plan)
    projection["freshness"].pop("plan_sha256", None)
    plan["freshness"]["plan_sha256"] = digest(projection)
    return plan


def reentry_transcripts(
    root: Path,
    env: dict[str, str],
    source: dict[str, Any],
    readiness_source_path: Path,
    wording_source_path: Path,
    clarity_result: dict[str, Any],
    wording_result: dict[str, Any],
    context_transition: dict[str, Any],
    context_duplicate_snapshot: dict[str, Any],
    wording_transition: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    needs_owner, needs_checked = clarification_owner_for_issue(
        root, env, context_transition, context_duplicate_snapshot, "needs_context"
    )
    needs_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "initial_change_request",
            "source_exit": "context_ready",
            "mode": "workflow",
            "target_locator": context_transition["target_locator"],
            "continuation_id": context_transition["continuation_id"],
            "duplicate_snapshot": context_duplicate_snapshot,
        },
        "transition": context_transition,
        "owner_context": {},
        "owner_result": needs_owner,
    }
    needs_envelope["typed_output"] = clarification_typed_output(
        needs_owner, needs_envelope["public_input"], context_transition
    )
    needs, needs_row = invoke_public(
        root, env, "guru-clarify-requirements", needs_envelope, "needs_context"
    )
    needs_input, needs_projection = project_installed_output(
        root, "guru-clarify-requirements", "needs_context", needs
    )
    discovery_owner, discovery_checked = checked_context_owner_for_issue(
        root, env, needs["transition"]
    )
    discovery_envelope = {
        "schema_version": "1.0",
        "public_input": needs_input,
        "transition": needs["transition"],
        "owner_context": {},
        "owner_result": discovery_owner,
    }
    discovery, discovery_row = invoke_public(
        root,
        env,
        "guru-discover-change-context",
        discovery_envelope,
        "context_ready",
    )
    if discovery.get("transition", {}).get("stage") != "context_current":
        raise RuntimeError("needs_context target did not parse and advance its transition")
    rows.append({
        "edge_id": "needs_context",
        "producer_skill": needs_row["skill_id"],
        "producer_actual_exit": needs_row["actual_exit"],
        "producer_stdout_sha256": needs_row["stdout_sha256"],
        "projection_id": needs_projection,
        "projected_input_sha256": digest(needs_input),
        "target_skill": discovery_row["skill_id"],
        "target_actual_exit": discovery_row["actual_exit"],
        "target_stdout_sha256": discovery_row["stdout_sha256"],
        "target_checker_status": discovery_checked.get("status"),
        "producer_checker_status": needs_checked.get("status"),
    })
    assert_forbidden_runtime_absent(root)

    for producer_exit, target_skill, target_exit in (
        ("clarify_requirements", "guru-clarify-requirements", "clear"),
        ("review_wording", "guru-review-contract-wording", "pass"),
    ):
        readiness_owner, readiness_checked = checked_readiness_owner_for_issue(
            root, env, wording_transition, readiness_source_path,
            clarity_result, wording_result, producer_exit
        )
        producer_transition = (
            context_transition
            if producer_exit == "clarify_requirements"
            else readiness_reentry_transition(wording_transition, producer_exit)
        )
        readiness_envelope = {
            "schema_version": "1.0",
            "public_input": {
                "profile": "current_issue",
                "source_exit": "pass",
                "mode": "workflow",
                "target_locator": wording_transition["target_locator"],
                "continuation_id": wording_transition["continuation_id"],
            },
            "transition": producer_transition,
            "owner_context": {"change_request": source},
            "owner_result": readiness_owner,
            "validation_receipt": readiness_checked["validation_receipt"],
        }
        producer, producer_row = invoke_public(
            root,
            env,
            "guru-review-change-request",
            readiness_envelope,
            producer_exit,
        )
        target_input, projection_id = project_installed_output(
            root, "guru-review-change-request", producer_exit, producer
        )
        if target_skill == "guru-clarify-requirements":
            target_owner, target_checked = clarification_owner_for_issue(
                root, env, producer["transition"], empty_duplicate_snapshot(producer["transition"]), "clear"
            )
            owner_context: dict[str, Any] = {}
        else:
            target_owner, target_checked = wording_owner_for_issue(
                root, env, wording_source_path
            )
            owner_context = {"change_request": source}
        target_envelope = {
            "schema_version": "1.0",
            "public_input": target_input,
            "transition": producer["transition"],
            "owner_context": owner_context,
            "owner_result": target_owner,
        }
        if target_skill == "guru-review-contract-wording":
            target_envelope["validation_receipt"] = target_checked["validation_receipt"]
        if target_skill == "guru-clarify-requirements":
            target_envelope["typed_output"] = clarification_typed_output(
                target_owner, target_input, producer["transition"]
            )
        assert_owner_binding(target_skill, target_input, target_owner)
        target, target_row = invoke_public(
            root, env, target_skill, target_envelope, target_exit
        )
        expected_stage = {
            "clarify_requirements": "clarity_current",
            "review_wording": "wording_current",
        }[producer_exit]
        if target.get("transition", {}).get("stage") != expected_stage:
            raise RuntimeError(
                f"{producer_exit} target did not parse and advance its transition"
            )
        rows.append({
            "edge_id": producer_exit,
            "producer_skill": producer_row["skill_id"],
            "producer_actual_exit": producer_row["actual_exit"],
            "producer_stdout_sha256": producer_row["stdout_sha256"],
            "producer_checker_status": readiness_checked.get("status"),
            "projection_id": projection_id,
            "projected_input_sha256": digest(target_input),
            "target_skill": target_row["skill_id"],
            "target_actual_exit": target_row["actual_exit"],
            "target_stdout_sha256": target_row["stdout_sha256"],
            "target_checker_status": target_checked.get("status"),
        })
        assert_forbidden_runtime_absent(root)
    return rows


def six_step_transcript(
    installed_repo: Path,
    chain_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    root, env = stage_transcript_owner_repo(installed_repo, chain_root)
    call_counts_before = operation_counts(env)
    before_status = run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, env=env
    ).stdout
    before_worktrees = run(["git", "worktree", "list", "--porcelain"], cwd=root, env=env).stdout
    rows: list[dict[str, Any]] = []

    sync, row = invoke_public(
        root,
        env,
        "guru-sync-base",
        {
            "schema_version": "1.0",
            "public_input": {
                "source_exit": "start",
                "mode": "workflow",
                "repo_root": ".",
                "base_branch": "main",
                "route": "repo_change",
            },
        },
        "synced",
    )
    rows.append(row)

    context_owner, context_checked = checked_context_owner_for_issue(
        root, env, sync["transition"]
    )
    context_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "pre_task",
            "source_exit": "synced",
            "mode": "workflow",
            "repo_locator": "example/guru-extension",
            "base_branch": "main",
            "continuation_id": "stage0-current",
        },
        "transition": sync["transition"],
        "owner_context": {},
        "owner_result": context_owner,
    }
    rows[-1]["next_input_sha256"] = digest(context_envelope)
    context, row = invoke_public(
        root, env, "guru-discover-change-context", context_envelope, "context_ready"
    )
    rows.append(row)

    clarity_owner, clarity_checked = clarification_owner_for_issue(
        root, env, context["transition"], context["duplicate_snapshot"]
    )
    clarity_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "initial_change_request",
            "source_exit": "context_ready",
            "mode": "workflow",
            "target_locator": context["transition"]["target_locator"],
            "continuation_id": context["transition"]["continuation_id"],
            "duplicate_snapshot": context["duplicate_snapshot"],
        },
        "transition": context["transition"],
        "owner_context": {},
        "owner_result": clarity_owner,
    }
    clarity_envelope["typed_output"] = clarification_typed_output(
        clarity_owner, clarity_envelope["public_input"], context["transition"]
    )
    assert_owner_binding(
        "guru-clarify-requirements",
        clarity_envelope["public_input"],
        clarity_owner,
    )
    rows[-1]["next_input_sha256"] = digest(clarity_envelope)
    clarity, row = invoke_public(
        root, env, "guru-clarify-requirements", clarity_envelope, "clear"
    )
    rows.append(row)
    discover_clarify_delta = operation_delta(call_counts_before, operation_counts(env))
    if discover_clarify_delta.get("issue.search", 0) != 1:
        raise RuntimeError(f"discover -> clarify duplicate search budget exceeded: {discover_clarify_delta}")

    source = {
        "kind": "issue",
        "repo": "example/guru-extension",
        "number": 145,
        "url": "https://github.com/example/guru-extension/issues/145",
        "selected_comments": [],
    }
    issue = live_issue(root, env)
    source.update({
        "title": issue["title"],
        "body": issue["body"],
        "updated_at": issue["updatedAt"],
    })
    readiness_source_path = chain_root / "inputs/readiness-change-request.json"
    readiness_source_path.parent.mkdir(parents=True)
    readiness_source_path.write_text(
        json.dumps(source, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    wording_source_path = chain_root / "inputs/wording-change-request.json"
    wording_source_path.write_text(
        json.dumps(wording_change_request_source(issue)) + "\n",
        encoding="utf-8",
    )
    wording_owner, wording_checked = wording_owner_for_issue(
        root, env, wording_source_path
    )
    wording_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "change_request",
            "source_exit": "clear",
            "mode": "workflow",
            "target_locator": clarity["transition"]["target_locator"],
            "continuation_id": clarity["transition"]["continuation_id"],
        },
        "transition": clarity["transition"],
        "owner_context": {"change_request": source},
        "owner_result": wording_owner,
        "validation_receipt": wording_checked["validation_receipt"],
    }
    assert_owner_binding(
        "guru-review-contract-wording",
        wording_envelope["public_input"],
        wording_owner,
    )
    rows[-1]["next_input_sha256"] = digest(wording_envelope)
    wording, row = invoke_public(
        root, env, "guru-review-contract-wording", wording_envelope, "pass"
    )
    rows.append(row)

    reentry = reentry_transcripts(
        root,
        env,
        source,
        readiness_source_path,
        wording_source_path,
        clarity_owner,
        wording_owner,
        context["transition"],
        context["duplicate_snapshot"],
        wording["transition"],
    )

    readiness_counts_before = operation_counts(env)
    source["selected_comments"] = live_issue_comments(root, env)
    readiness_source_path.write_text(
        json.dumps(source, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    readiness_owner, readiness_checked = checked_readiness_owner_for_issue(
        root, env, wording["transition"], readiness_source_path,
        clarity_owner, wording_owner,
    )
    readiness_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "current_issue",
            "source_exit": "pass",
            "mode": "workflow",
            "target_locator": wording["transition"]["target_locator"],
            "continuation_id": wording["transition"]["continuation_id"],
        },
        "transition": wording["transition"],
        "owner_context": {"change_request": source},
        "owner_result": readiness_owner,
        "validation_receipt": readiness_checked["validation_receipt"],
    }
    assert_owner_binding(
        "guru-review-change-request",
        readiness_envelope["public_input"],
        readiness_owner,
    )
    rows[-1]["next_input_sha256"] = digest(readiness_envelope)
    serializer_counts_before = operation_counts(env)
    readiness, row = invoke_public(
        root, env, "guru-review-change-request", readiness_envelope, "ready"
    )
    serializer_delta = operation_delta(serializer_counts_before, operation_counts(env))
    if serializer_delta:
        raise RuntimeError(f"readiness public serializer made live calls: {serializer_delta}")
    rows.append(row)
    readiness_delta = operation_delta(readiness_counts_before, operation_counts(env))
    if readiness_delta.get("issue.get", 0) > 1 or readiness_delta.get("issue.comments.list", 0) > 1:
        raise RuntimeError(f"readiness authority budget exceeded: {readiness_delta}")

    if (
        run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, env=env).stdout
        != before_status
        or run(["git", "worktree", "list", "--porcelain"], cwd=root, env=env).stdout
        != before_worktrees
    ):
        raise RuntimeError("pre-task five-step transcript wrote repository/worktree state")
    assert_forbidden_runtime_absent(root)

    workspace_plan = workspace_plan_for_transition(
        root, env, readiness["transition"]
    )
    workspace_plan = record_semantic(
        root,
        env,
        "guru-create-task-workspace",
        "record-task-workspace-plan.sh",
        ["--invocation", "-"],
        {
            "schema_version": "1.0",
            "plan": workspace_plan,
            "transition": readiness["transition"],
        },
    )

    mutation = {
        "schema_version": "1.0",
        "plan": workspace_plan,
        "transition": readiness["transition"],
    }
    workspace_package = (
        root
        / ".trellis/guru-team/skills/packages/guru-create-task-workspace/scripts"
    )
    result = json_stdout(
        run(
            [workspace_package / "create-task-workspace.sh", "--invocation", "-"],
            cwd=root,
            env=env,
            stdin=mutation,
        ),
        "workspace executor",
    )
    checked_result = json_stdout(
        run(
            [workspace_package / "check-task-workspace-result.sh", "--invocation", "-"],
            cwd=root,
            env=env,
            stdin={**mutation, "result": result},
        ),
        "workspace checker",
    )
    workspace_call = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "execute_reviewed_plan",
            "mode": "workflow",
        },
        "transition": readiness["transition"],
        "owner_plan": workspace_plan,
        "owner_result": checked_result,
    }
    rows[-1]["next_input_sha256"] = digest(workspace_call)
    workspace, row = invoke_public(
        root,
        env,
        "guru-create-task-workspace",
        workspace_call,
        "created",
    )
    rows.append(row)
    final_counts = operation_counts(env)
    expected_exact = {
        "base.fetch": 1,
        "workspace.base.fetch": 1,
        "workspace.mutation_boundary_recheck": 1,
    }
    if any(final_counts.get(operation, 0) != expected for operation, expected in expected_exact.items()) or final_counts.get("issue.comments.list", 0) > 1 or final_counts.get("issue.get", 0) > 15:
        raise RuntimeError(f"Phase 0 operation budget exceeded: {final_counts}")
    created = checked_result.get("created_workspace")
    if not isinstance(created, dict):
        raise RuntimeError("workspace checker did not return created workspace facts")
    branch = str(created.get("branch_name") or "")
    if run(
        ["git", "show-ref", "--verify", f"refs/heads/{branch}"],
        cwd=root,
        env=env,
        check=False,
    ).returncode:
        raise RuntimeError("six-step transcript did not create its reviewed branch")
    task_dir = root / str(created.get("task_artifact_dir") or "")
    if not task_dir.is_dir() or not (task_dir / "task.json").is_file():
        # The task belongs to the created worktree, not the decision checkout.
        worktrees = run(["git", "worktree", "list", "--porcelain"], cwd=root, env=env).stdout
        paths = [Path(line[9:]) for line in worktrees.splitlines() if line.startswith("worktree ")]
        if not any((path / str(created.get("task_artifact_dir") or "") / "task.json").is_file() for path in paths):
            raise RuntimeError("six-step transcript did not create its reviewed task")
    assert_forbidden_runtime_absent(root)
    return rows, reentry, {
        "actual_exit": workspace["exit_id"],
        "branch_name": branch,
        "workspace_slug": created.get("workspace_slug"),
        "task_slug": created.get("task_slug"),
        "task_artifact_dir": created.get("task_artifact_dir"),
        "checker_status": checked_result.get("checker", {}).get("status"),
        "clarification_checker_status": clarity_checked.get("status"),
        "wording_checker_status": wording_checked.get("status"),
        "context_checker_status": context_checked.get("status"),
        "forbidden_runtime_checks": 3,
        "owner_repo": str(root),
        "operation_counts": final_counts,
        "discover_clarify_operation_delta": discover_clarify_delta,
        "readiness_operation_delta": readiness_delta,
        "public_serializer_operation_delta": serializer_delta,
    }


def refresh_provenance_transcripts(
    installed_repo: Path,
    matrix_root: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for expected_source in ("explicit", "config-candidate", "remote-default"):
        chain_root = matrix_root / expected_source
        root, env = stage_transcript_owner_repo(installed_repo, chain_root)
        config = root / ".trellis/guru-team/config.yml"
        if expected_source != "explicit":
            candidate = "main" if expected_source == "config-candidate" else "missing"
            config.write_text(
                config.read_text(encoding="utf-8")
                + f"base_branch_candidates:\n  - {candidate}\n",
                encoding="utf-8",
            )
            run(["git", "add", config], cwd=root, env=env)
            run(
                ["git", "commit", "-q", "-m", f"configure {expected_source}"],
                cwd=root,
                env=env,
            )
            head = run(["git", "rev-parse", "HEAD"], cwd=root, env=env).stdout.strip()
            run(
                ["git", "update-ref", "refs/remotes/origin/main", head],
                cwd=root,
                env=env,
            )
        before_status = run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=root,
            env=env,
        ).stdout
        initial_input = {
            "source_exit": "start",
            "mode": "workflow",
            "repo_root": ".",
            "route": "repo_change",
        }
        if expected_source == "explicit":
            initial_input["base_branch"] = "main"
        sync, sync_row = invoke_public(
            root,
            env,
            "guru-sync-base",
            {"schema_version": "1.0", "public_input": initial_input},
            "synced",
        )
        initial_base = sync.get("transition", {}).get("base", {})
        if (
            initial_base.get("source") != expected_source
            or initial_base.get("selected_base") != "main"
        ):
            raise RuntimeError(
                f"initial sync did not resolve {expected_source} provenance"
            )
        context_input, sync_projection = project_installed_output(
            root, "guru-sync-base", "synced", sync
        )
        context_owner, context_checked = checked_context_owner_for_issue(
            root, env, sync["transition"]
        )
        context, context_row = invoke_public(
            root,
            env,
            "guru-discover-change-context",
            {
                "schema_version": "1.0",
                "public_input": context_input,
                "transition": sync["transition"],
                "owner_context": {},
                "owner_result": context_owner,
            },
            "context_ready",
        )
        (chain_root / "issue-body.txt").write_text(
            "The live issue authority changed and requires a fresh context read.",
            encoding="utf-8",
        )
        clarification_input, context_projection = project_installed_output(
            root, "guru-discover-change-context", "context_ready", context
        )
        refresh_owner, refresh_checked = clarification_owner_for_issue(
            root, env, context["transition"], context["duplicate_snapshot"], "refresh_context"
        )
        refresh_envelope = {
            "schema_version": "1.0",
            "public_input": clarification_input,
            "transition": context["transition"],
            "owner_context": {},
            "owner_result": refresh_owner,
        }
        refresh_envelope["typed_output"] = clarification_typed_output(
            refresh_owner, clarification_input, context["transition"]
        )
        refresh, refresh_row = invoke_public(
            root,
            env,
            "guru-clarify-requirements",
            refresh_envelope,
            "refresh_context",
        )
        projected_sync_input, refresh_projection = project_installed_output(
            root, "guru-clarify-requirements", "refresh_context", refresh
        )
        if expected_source == "explicit":
            if projected_sync_input.get("base_branch") != "main":
                raise RuntimeError("explicit refresh omitted its selected base")
        elif "base_branch" in projected_sync_input:
            raise RuntimeError(
                f"{expected_source} refresh forced an explicit base branch"
            )
        refreshed, refreshed_row = invoke_public(
            root,
            env,
            "guru-sync-base",
            {
                "schema_version": "1.0",
                "public_input": projected_sync_input,
            },
            "synced",
        )
        refreshed_base = refreshed.get("transition", {}).get("base", {})
        if (
            refreshed_base.get("source") != expected_source
            or refreshed_base.get("selected_base") != "main"
        ):
            raise RuntimeError(
                f"refresh sync did not preserve {expected_source} provenance"
            )
        if run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=root,
            env=env,
        ).stdout != before_status:
            raise RuntimeError("refresh provenance transcript wrote repository state")
        assert_forbidden_runtime_absent(root)
        rows.append({
            "source": expected_source,
            "selected_base": refreshed_base.get("selected_base"),
            "initial_sync_stdout_sha256": sync_row["stdout_sha256"],
            "sync_projection_id": sync_projection,
            "context_actual_exit": context_row["actual_exit"],
            "context_checker_status": context_checked.get("status"),
            "context_projection_id": context_projection,
            "refresh_actual_exit": refresh_row["actual_exit"],
            "refresh_checker_status": refresh_checked.get("status"),
            "refresh_projection_id": refresh_projection,
            "projected_base_branch": projected_sync_input.get("base_branch"),
            "refreshed_sync_actual_exit": refreshed_row["actual_exit"],
            "refreshed_sync_stdout_sha256": refreshed_row["stdout_sha256"],
        })
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--semantic-grading", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    installed_repo = Path(args.installed_repo).resolve()
    work_root = Path(args.work_root).resolve()
    semantic_grading_input = Path(args.semantic_grading)
    if semantic_grading_input.is_symlink():
        raise RuntimeError("semantic-grading must be a regular file, not a symlink")
    semantic_grading = semantic_grading_input.resolve()
    if not semantic_grading.is_file():
        raise RuntimeError("semantic-grading must be a regular file")
    if (
        work_root == installed_repo
        or installed_repo in work_root.parents
        or work_root == Path(work_root.anchor)
        or len(work_root.parts) < 4
    ):
        raise RuntimeError("work-root must be a dedicated path outside the installed repository")
    if work_root.exists():
        shutil.rmtree(work_root)
    work_root.mkdir(parents=True)
    records, exit_rows = installed_eval_runs(
        installed_repo, work_root, semantic_grading
    )
    expected_pairs = {
        (skill_id, exit_row["id"])
        for skill_id in SKILLS
        for exit_row in load_json(
            installed_repo
            / ".trellis/guru-team/skills/packages"
            / skill_id
            / "interface.json"
        ).get("external_exits", [])
        if isinstance(exit_row, dict)
    }
    actual_pairs = {(row["skill_id"], row["actual_exit"]) for row in exit_rows}
    if expected_pairs != actual_pairs or len(actual_pairs) != 23:
        raise RuntimeError(
            f"installed exit transcript coverage mismatch: expected={sorted(expected_pairs)} "
            f"actual={sorted(actual_pairs)}"
        )
    chain, reentry, workspace = six_step_transcript(
        installed_repo,
        work_root / "six-step",
    )
    refresh_provenance = refresh_provenance_transcripts(
        installed_repo,
        work_root / "refresh-provenance",
    )
    output = {
        "status": "ok",
        "checkpoint": args.checkpoint,
        "installed_repo": str(installed_repo),
        "exit_family_count": len(actual_pairs),
        "exit_transcripts": exit_rows,
        "six_step_transcript": chain,
        "reentry_transcripts": reentry,
        "refresh_provenance_transcripts": refresh_provenance,
        "workspace": workspace,
        "runtime_checkpoint": runtime_checkpoint(
            installed_repo,
            installed_repo / ".trellis/guru-team/runtime",
            f"phase0-{args.checkpoint}",
        ),
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
