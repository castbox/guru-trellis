#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


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


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def context_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value) + b"\n").hexdigest()


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
        raise RuntimeError(
            f"command failed ({process.returncode}): {' '.join(map(str, argv))}\n"
            f"{process.stderr.strip()}"
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


def installed_eval_runs(
    installed_repo: Path, work_root: Path
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
    process = run(argv, cwd=root, env=env, stdin=envelope)
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
    }


def record_semantic(
    root: Path,
    env: dict[str, str],
    skill_id: str,
    script: str,
    arguments: list[str | Path],
    payload: dict[str, Any],
) -> dict[str, Any]:
    path = root / ".agents/skills" / skill_id / "scripts" / script
    return json_stdout(
        run([path, *arguments], cwd=root, env=env, stdin=payload),
        f"semantic recorder {skill_id}",
    )


def context_owner_for_issue(
    root: Path,
    env: dict[str, str],
    seed: dict[str, Any],
) -> dict[str, Any]:
    owner = copy.deepcopy(seed)
    repo = "example/guru-extension"
    number = 145
    live = json_stdout(
        run(
            [
                "gh",
                "issue",
                "view",
                str(number),
                "--repo",
                repo,
                "--json",
                "number,url,state,updatedAt,body",
            ],
            cwd=root,
            env=env,
        ),
        "live issue authority",
    )
    url = f"https://github.com/{repo}/issues/{number}"
    if live.get("number") != number or live.get("url") != url:
        raise RuntimeError("live issue authority returned a different identity")
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
    owner["repository"] = {
        "repo": issue["repo"],
        "selected_base": "main",
        "decision_branch": "main",
    }
    owner["change_input"]["issue_refs"] = ["#145"]
    owner["change_input"]["paths"] = ["docs/requirements.md"]
    owner["live_change"] = {
        "kind": "issue",
        "identity": issue["url"],
        "state": issue["state"],
        "updated_at": issue["updated_at"],
        "body_sha256": issue["body_sha256"],
        "facts_sha256": issue["facts_sha256"],
        "issue_binding": None,
    }
    evidence = {
        "docs": "docs/requirements.md",
        "code_contracts": "trellis/runtime.py",
        "tests": "trellis/test_runtime.py",
    }
    for group, path in evidence.items():
        blob = run(["git", "rev-parse", f"HEAD:{path}"], cwd=root, env=env).stdout.strip()
        owner["current_state"][group][0]["path"] = path
        owner["current_state"][group][0]["blob_or_content_sha256"] = blob
    preview_args: list[str | Path] = [
        root
        / ".agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh",
        "--root",
        root,
        "--issue-ref",
        "#145",
        "--path",
        "docs/requirements.md",
    ]
    for command in owner["change_input"].get("commands", []):
        preview_args.extend(["--command", str(command)])
    for term in owner["change_input"].get("terms", []):
        preview_args.extend(["--term", str(term)])
    for query in owner["change_input"].get("queries", []):
        preview_args.extend(["--query", str(query)])
    preview = json_stdout(run(preview_args, cwd=root, env=env), "context history preview")
    owner["canonical_query"] = preview["canonical_query"]
    owner["history_preview"] = preview
    owner["history_review"] = {
        "selected_candidates": [],
        "excluded_candidates": [],
        "deep_reads": [],
    }
    owner["typed_exit"] = "context_ready"
    owner["error"] = None
    owner["ai_review_gate"]["status"] = "passed"
    owner.pop("result_identity", None)
    return owner


def cleanup_seed_workspace(root: Path, result: dict[str, Any]) -> None:
    created = result.get("created_workspace")
    if not isinstance(created, dict):
        raise RuntimeError("workspace seed did not create a workspace")
    branch = str(created.get("branch_name") or "")
    slug = str(created.get("workspace_slug") or "")
    listing = run(["git", "worktree", "list", "--porcelain"], cwd=root).stdout
    candidate: Path | None = None
    current: Path | None = None
    for line in listing.splitlines():
        if line.startswith("worktree "):
            current = Path(line.removeprefix("worktree "))
        elif line == f"branch refs/heads/{branch}" and current is not None:
            candidate = current
    if candidate is None or candidate.name != slug:
        raise RuntimeError("could not resolve the exact temporary seed worktree")
    run(["git", "worktree", "remove", "--force", candidate], cwd=root)
    run(["git", "branch", "-D", branch], cwd=root)
    for row in created.get("runtime_mappings", []):
        if isinstance(row, dict) and isinstance(row.get("path"), str):
            (root / row["path"]).unlink(missing_ok=True)
    if run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root).stdout:
        raise RuntimeError("workspace seed cleanup did not restore the temporary repo")


def six_step_transcript(
    records: dict[tuple[str, str], dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    workspace_record = records[(
        "guru-create-task-workspace",
        HAPPY_CASES["guru-create-task-workspace"],
    )]
    root = Path(workspace_record["owner_repo"])
    seed_result = load_json(root / ".trellis/.runtime/guru-team/evals/owner-result.json")
    workspace_envelope = load_json(
        root / ".trellis/.runtime/guru-team/evals/invocation.json"
    )
    cleanup_seed_workspace(root, seed_result)
    fake_bin = root.parent / "owner-bin"
    env = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
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

    context_seed_root = Path(records[(
        "guru-discover-change-context",
        HAPPY_CASES["guru-discover-change-context"],
    )]["owner_repo"])
    context_seed = load_json(
        context_seed_root / ".trellis/.runtime/guru-team/evals/owner-result.json"
    )
    context_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "pre_task",
            "source_exit": "synced",
            "mode": "workflow",
            "repo_locator": "example/guru-extension",
            "base_branch": "main",
            "continuation_id": "installed-phase0-transcript",
        },
        "transition": sync["transition"],
        "owner_context": {},
        "owner_result": context_owner_for_issue(root, env, context_seed),
    }
    rows[-1]["next_input_sha256"] = digest(context_envelope)
    context, row = invoke_public(
        root, env, "guru-discover-change-context", context_envelope, "context_ready"
    )
    rows.append(row)

    prerequisites = workspace_envelope["owner_prerequisites"]
    clarity_owner = copy.deepcopy(prerequisites["clarity"])
    clarity_envelope = {
        "schema_version": "1.0",
        "public_input": {
            "profile": "initial_change_request",
            "source_exit": "context_ready",
            "mode": "workflow",
            "target_locator": context["transition"]["target_locator"],
            "continuation_id": context["transition"]["continuation_id"],
        },
        "transition": context["transition"],
        "owner_context": {},
        "owner_result": clarity_owner,
    }
    rows[-1]["next_input_sha256"] = digest(clarity_envelope)
    clarity, row = invoke_public(
        root, env, "guru-clarify-requirements", clarity_envelope, "clear"
    )
    rows.append(row)

    source = {
        "kind": "issue",
        "repo": "example/guru-extension",
        "number": 145,
        "selected_comments": [],
    }
    wording_owner = copy.deepcopy(prerequisites["wording"])
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
    }
    rows[-1]["next_input_sha256"] = digest(wording_envelope)
    wording, row = invoke_public(
        root, env, "guru-review-contract-wording", wording_envelope, "pass"
    )
    rows.append(row)

    readiness_owner = copy.deepcopy(prerequisites["readiness"])
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
        "owner_context": {
            "change_request": source,
            "prerequisite_payloads": {
                "clarity": clarity_owner,
                "wording": wording_owner,
            },
        },
        "owner_result": readiness_owner,
    }
    rows[-1]["next_input_sha256"] = digest(readiness_envelope)
    readiness, row = invoke_public(
        root, env, "guru-review-change-request", readiness_envelope, "ready"
    )
    rows.append(row)

    if (
        run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, env=env).stdout
        != before_status
        or run(["git", "worktree", "list", "--porcelain"], cwd=root, env=env).stdout
        != before_worktrees
    ):
        raise RuntimeError("pre-task five-step transcript wrote repository/worktree state")

    mutation = {
        "schema_version": "1.0",
        "plan": workspace_envelope["owner_plan"],
        "prerequisite_payloads": prerequisites,
    }
    workspace_package = root / ".agents/skills/guru-create-task-workspace/scripts"
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
        "public_input": workspace_envelope["public_input"],
        "transition": readiness["transition"],
        "owner_prerequisites": prerequisites,
        "owner_plan": workspace_envelope["owner_plan"],
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
    return rows, {
        "actual_exit": workspace["exit_id"],
        "branch_name": branch,
        "workspace_slug": created.get("workspace_slug"),
        "task_slug": created.get("task_slug"),
        "task_artifact_dir": created.get("task_artifact_dir"),
        "checker_status": checked_result.get("checker", {}).get("status"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-repo", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--checkpoint", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    installed_repo = Path(args.installed_repo).resolve()
    work_root = Path(args.work_root).resolve()
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
    records, exit_rows = installed_eval_runs(installed_repo, work_root)
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
    chain, workspace = six_step_transcript(records)
    output = {
        "status": "ok",
        "checkpoint": args.checkpoint,
        "installed_repo": str(installed_repo),
        "exit_family_count": len(actual_pairs),
        "exit_transcripts": exit_rows,
        "six_step_transcript": chain,
        "workspace": workspace,
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
