from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


def load_runtime():
    runtime_path = PACKAGE / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location("finalize_task_package_runtime", runtime_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_transaction():
    spec = importlib.util.spec_from_file_location(
        "finalize_task_transaction_test",
        PACKAGE / "runtime/transaction.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


def git_fixture_commit(root: Path, *paths: str) -> None:
    subprocess.run(["git", "add", "--", *paths], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)


def workspace_boundary_fixture() -> tuple[Path, Path, dict[str, object]]:
    temp_root = Path(tempfile.mkdtemp(prefix="guru-workspace-boundary-"))
    source = temp_root / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
    subprocess.run(["git", "config", "user.name", "Guru Test"], cwd=source, check=True)
    subprocess.run(["git", "config", "user.email", "guru@example.com"], cwd=source, check=True)
    task_relative = ".trellis/tasks/08-27-312-workspace-boundary-merged-active-task"
    source_task = source / task_relative
    source_task.mkdir(parents=True)
    ordinary = (
        "task.json",
        "prd.md",
        "design.md",
        "implement.md",
        "implement.jsonl",
        "check.jsonl",
    )
    for name in ordinary:
        (source_task / name).write_text(f"{name}\n", encoding="utf-8")
    for name in GTT.WORKSPACE_BOUNDARY_REVIEW_METADATA:
        (source_task / name).write_text("review\n", encoding="utf-8")
    (source_task / "reviews").mkdir()
    git_fixture_commit(source, f"{task_relative}/")
    task_workspace = temp_root / "task-worktree"
    task_workspace.mkdir()
    context = {
        "workspace_mode": "worktree",
        "expected_workspace": task_workspace,
        "actual_repo_root": task_workspace,
        "source_checkout": source,
        "task_dir": task_workspace / task_relative,
        "task_dir_relative": task_relative,
        "task_context_present": True,
    }
    return temp_root, source, context


def shared_runtime_parent() -> Path:
    for parent in PACKAGE.parents:
        if (parent / "runtime/io.py").is_file():
            return parent
    raise AssertionError("shared Guru Team runtime is unavailable")


def provenance_manifest(
    source_repo: str,
    source_commit: str,
    *,
    installed_at: str = "before",
    tree_state: str = "clean",
    is_mutable_ref: bool = False,
    selected_platforms: list[str] | None = None,
    all_platforms: bool | None = None,
) -> dict:
    if selected_platforms is None:
        selected_platforms = ["claude", "codex", "cursor"]
    if all_platforms is None:
        all_platforms = selected_platforms == ["claude", "codex", "cursor"]
    return {
        "schema_version": "2.0",
        "extension": {"extension_id": "guru-team"},
        "installed_at": installed_at,
        "source": {
            "repo": f"https://github.com/{source_repo}.git",
            "ref": source_commit,
            "commit": source_commit,
            "tree_state": tree_state,
            "is_mutable_ref": is_mutable_ref,
        },
        "install": {
            "selected_platforms": selected_platforms,
            "all_platforms": all_platforms,
            "managed_assets": [
                ".trellis/spec/workflow/semantic-retrieval.md"
            ],
        },
        "skill_packages": {
            "selected_platforms": list(selected_platforms),
        },
        "overlays": {
            "selected_platforms": list(selected_platforms),
        },
    }


def provenance_file_action_sections(action: str) -> dict[str, dict[str, object]]:
    return {
        "skill_packages": {
            "files": [
                {
                    "path": ".trellis/guru-team/skills/registry.json",
                    "source": "trellis/skills/guru-team/registry.json",
                    "sha256": "1" * 64,
                    "executable": False,
                    "action": action,
                },
                {
                    "path": ".trellis/guru-team/skills/packages/guru-finalize-task/runtime/owner.py",
                    "source": "trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py",
                    "sha256": "2" * 64,
                    "executable": False,
                    "action": action,
                },
            ],
        },
        "overlays": {
            "files": [
                {
                    "path": ".claude/commands/guru/finish-work.md",
                    "source": "trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md",
                    "sha256": "3" * 64,
                    "executable": False,
                    "action": action,
                },
                {
                    "path": ".codex/prompts/guru-finish-work.md",
                    "source": "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md",
                    "sha256": "4" * 64,
                    "executable": False,
                    "action": action,
                },
            ],
        },
    }


def initialize_provenance_git_repo(root: Path, repo_ref: str) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Guru Test"], cwd=root, check=True)
    subprocess.run(
        ["git", "config", "user.email", "guru@example.com"],
        cwd=root,
        check=True,
    )
    subprocess.run(
        ["git", "remote", "add", "origin", f"https://github.com/{repo_ref}.git"],
        cwd=root,
        check=True,
    )


def commit_provenance_fixture(root: Path, message: str) -> str:
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", message], cwd=root, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def write_provenance_apply_fixture(root: Path, behavior: str = "normal") -> None:
    apply_script = (
        root
        / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
    )
    apply_script.parent.mkdir(parents=True)
    apply_script.write_text(
        f"""from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--repo", required=True)
parser.add_argument("--platform", action="append", choices=("claude", "codex", "cursor"))
parser.add_argument("--all-platforms", action="store_true")
parser.add_argument("--json", action="store_true")
args = parser.parse_args()
source_root = Path(__file__).resolve().parents[5]
target_root = Path(args.repo).resolve()
source_head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=source_root, check=True,
    text=True, stdout=subprocess.PIPE,
).stdout.strip()
target_head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=target_root, check=True,
    text=True, stdout=subprocess.PIPE,
).stdout.strip()
manifest_path = target_root / ".trellis/guru-team/extension.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
requested_platforms = (
    ["claude", "codex", "cursor"]
    if args.all_platforms
    else sorted(args.platform or [])
)
if requested_platforms != manifest["install"]["selected_platforms"]:
    raise SystemExit("preset apply platform selection did not match parent manifest")
if args.all_platforms is not manifest["install"]["all_platforms"]:
    raise SystemExit("preset apply all-platforms identity did not match parent manifest")
manifest["installed_at"] = "after"
manifest["source"]["ref"] = source_head
manifest["source"]["commit"] = source_head
manifest["source"]["tree_state"] = "clean"
manifest["source"]["is_mutable_ref"] = False
behavior = {behavior!r}
if behavior == "source_repo_drift":
    manifest["source"]["repo"] = "https://github.com/castbox/other-source.git"
if behavior == "business_head_as_source":
    manifest["source"]["ref"] = target_head
    manifest["source"]["commit"] = target_head
manifest_path.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
if behavior == "source_dirty":
    (source_root / "source-dirty.txt").write_text("dirty\\n", encoding="utf-8")
if behavior == "extra_target_path":
    (target_root / "unexpected.txt").write_text("unexpected\\n", encoding="utf-8")
if behavior == "managed_byte_drift":
    managed_path = target_root / ".trellis/spec/workflow/semantic-retrieval.md"
    managed_path.write_text("managed after apply\\n", encoding="utf-8")
if behavior in {{"managed_new_sidecar", "managed_backup_sidecar"}}:
    suffix = ".new" if behavior == "managed_new_sidecar" else ".bak"
    sidecar_path = target_root / f".trellis/spec/workflow/semantic-retrieval.md{{suffix}}"
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.write_text("managed sidecar\\n", encoding="utf-8")
print(json.dumps({{"status": "ok"}}))
""",
        encoding="utf-8",
    )


def local_source_fetch_runner(
    source_repo: Path,
    observed: list[tuple[list[str], Path | None]],
):
    original_run = GTT.run

    def routed(
        cmd: list[str],
        cwd: Path | None = None,
        check: bool = True,
        env: dict[str, str] | None = None,
    ):
        observed.append((list(cmd), cwd))
        if cmd[:4] == ["git", "fetch", "--depth=1", "origin"]:
            cmd = ["git", "fetch", "--depth=1", str(source_repo), cmd[4]]
        return original_run(cmd, cwd=cwd, check=check, env=env)

    return routed


def large_finish_summary() -> dict:
    paths = [f"changes/path-{index:04d}.txt" for index in range(2001)]
    title = "Large finish summary"
    index = {
        "problem": "Large diffs were rejected by an arbitrary path limit.",
        "outcome": "Complete large path sets are accepted.",
        "changed_behavior": ["Removed the arbitrary changed-path count limit."],
        "affected_surfaces": [{
            "kind": "schema",
            "name": "finish-summary",
            "paths": ["trellis/workflows/guru-team/schemas/finish-summary.schema.json"],
            "change": "Accept complete large path sets.",
        }],
        "contract_changes": [],
        "search_terms": {
            "issue_refs": [],
            "pr_refs": [],
            "branches": ["fix/227-finish-summary-large-path-set"],
            "paths": paths,
            "commands": [],
            "config_keys": [],
            "schema_fields": ["git.changed_paths", "index.search_terms.paths"],
            "symbols": ["finish_summary_errors"],
            "phrases": [
                "大型 diff 路径上限阻断",
                "finish_summary_errors 支持完整路径集",
                "已移除 finish summary limit",
            ],
        },
    }
    index["retrieval_text"] = GTT.current_finish_summary_retrieval_text(title, index)
    return {
        "schema_version": 2,
        "generated_at": "2026-08-14T00:00:00Z",
        "generator": "guru-team.finalize-task",
        "task": {
            "slug": "227-finish-summary-large-path-set",
            "title": title,
            "status": "completed",
            "artifact_dir": ".trellis/tasks/227-finish-summary-large-path-set",
            "archive_dir": ".trellis/tasks/archive/2026-08/227-finish-summary-large-path-set",
        },
        "git": {
            "base_branch": "main",
            "branch": "fix/227-finish-summary-large-path-set",
            "commits": ["a" * 40],
            "changed_paths": paths,
        },
        "github": {"pr_url": ""},
        "artifacts": {},
        "index": index,
    }


def eval_after_archive_hook_fixture(
    root: Path,
) -> tuple[dict[str, object], Path]:
    task_ref = ".trellis/tasks/current"
    task_dir = root / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(
        json.dumps(
            {
                "id": "current",
                "name": "current",
                "title": "Finalization hook preflight",
                "status": "in_progress",
                "branch": "main",
                "base_branch": "main",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    parser_source_dir = next(
        parent / ".trellis/scripts/common"
        for parent in PACKAGE.parents
        if (parent / ".trellis/scripts/common/config.py").is_file()
    )
    parser_target_dir = root / ".trellis/scripts/common"
    parser_target_dir.mkdir(parents=True)
    (parser_target_dir / "__init__.py").write_text("", encoding="utf-8")
    for name in ("config.py", "paths.py"):
        shutil.copy2(parser_source_dir / name, parser_target_dir / name)

    sentinel = root / "after-archive-hook-sentinel"
    (root / ".trellis/config.yaml").write_text(
        "hooks:\n"
        "  after_archive:\n"
        f'    - "touch {sentinel}"\n',
        encoding="utf-8",
    )
    public_input: dict[str, object] = {
        "profile": "publication_ready",
        "mode": "workflow",
        "task_ref": task_ref,
        "branch_review_commit": "a" * 40,
        "pr_title": "fix: reject official after_archive hooks",
        "pr_body": "Refs #267",
    }
    plan_digest = "b" * 64
    eval_dir = root / ".trellis/.runtime/guru-team/evals"
    eval_dir.mkdir(parents=True)
    (eval_dir / "finalization-context.json").write_text(
        json.dumps(
            {
                "schema_version": "2.0",
                "task_ref": task_ref,
                "plan_ref": f"finalization:{plan_digest}",
                "plan_digest": plan_digest,
                "branch_review_commit": "a" * 40,
                "publication_head": "a" * 40,
                "archive_locator": ".trellis/tasks/archive/2026-08/current",
                "repo_ref": "example/guru-extension",
                "remote": "origin",
                "head_branch": "main",
                "pr_title": public_input["pr_title"],
                "pr_body": public_input["pr_body"],
                "publication_status": "current",
                "publication_stale_reason": None,
                "transaction_state": "prepared",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return public_input, sentinel
