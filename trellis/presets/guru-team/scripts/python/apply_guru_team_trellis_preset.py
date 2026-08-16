#!/usr/bin/env python3
"""Apply Guru team Trellis companion assets to a project repository."""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import stat
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_MODULE_DIR = Path(__file__).resolve().parent
if str(SCRIPT_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_MODULE_DIR))

from validate_upstream_ownership import validate_repository as validate_upstream_ownership_repository


EXTENSION_MANIFEST = Path("trellis/guru-team-extension.json")
WORKFLOW_MARKETPLACE = "gh:castbox/guru-trellis/trellis"
WORKFLOW_TEMPLATE = "guru-team"
DEFAULT_PLATFORMS = ("codex", "cursor")
PLATFORM_OVERLAY_PREFIXES = {
    "codex": (Path(".codex"),),
    "cursor": (Path(".cursor"),),
    "claude": (Path(".claude"),),
}
ALL_PLATFORMS = tuple(PLATFORM_OVERLAY_PREFIXES)
GURU_OVERLAY_ENTRY_PATHS = {
    "codex": Path(".codex/prompts/guru-finish-work.md"),
    "cursor": Path(".cursor/commands/guru-finish-work.md"),
    "claude": Path(".claude/commands/guru/finish-work.md"),
}
GURU_OVERLAY_SCHEMA_VERSION = "1.0"
INSTALLED_EXTENSION_SCHEMA_VERSION = "2.0"
INSTALLED_EXTENSION_KEYS = {
    "schema_version",
    "extension",
    "installed_at",
    "source",
    "install",
    "skill_packages",
    "overlays",
    "notes",
}
GURU_OVERLAY_REMOVAL_SIDECAR = (
    "Guru Team platform selection no longer manages this entry. Review the "
    "preserved local file, remove it or migrate its content, then delete this "
    "sidecar and reapply the preset.\n"
).encode("utf-8")
SKILL_DESTINATION_PLATFORM_ORDER = ("shared", "codex", "claude", "cursor")
CURRENT_SKILL_SHARED_SCHEMAS = frozenset({
    "production-contract-manifest-4.0.schema.json",
    "production-contract-manifest-3.0.schema.json",
    "production-contract-manifest-2.0.schema.json",
    "production-contract-manifest.schema.json",
    "skill-eval-adapter-request-3.0.schema.json",
    "skill-eval-adapter-request-2.0.schema.json",
    "skill-eval-adapter-request.schema.json",
    "skill-eval-adapter-response-3.0.schema.json",
    "skill-eval-adapter-response-2.0.schema.json",
    "skill-eval-adapter-response.schema.json",
    "skill-eval-control-map-1.0.schema.json",
    "skill-eval-human-feedback.schema.json",
    "skill-eval-native-trace.schema.json",
    "skill-eval-run-4.0.schema.json",
    "skill-eval-run-3.0.schema.json",
    "skill-eval-run-2.0.schema.json",
    "skill-eval-run.schema.json",
    "skill-eval-semantic-grading.schema.json",
    "skill-evals-2.0.schema.json",
    "skill-evals.schema.json",
    "skill-interface-1.3.schema.json",
    "skill-interface-1.4.schema.json",
    "skill-interface-1.5.schema.json",
    "skill-interface-1.6.schema.json",
    "skill-registry-1.3.schema.json",
    "skill-registry-1.4.schema.json",
    "skill-registry.schema.json",
    "skill-commands.schema.json",
    "skill-error-catalog.schema.json",
})
SKILL_RUNTIME_KERNEL_PATHS = (
    Path("__init__.py"),
    Path("bootstrap.py"),
    Path("command.py"),
    Path("compat.py"),
    Path("discovery.py"),
    Path("eval_runner.py"),
    Path("installed.py"),
    Path("io.py"),
    Path("launch.sh"),
    Path("probe.py"),
    Path("python-runtime.json"),
    Path("requirements.lock"),
    Path("resolve-python.sh"),
    Path("schema.py"),
    Path("validate.py"),
)
ALWAYS_OVERLAY_PREFIXES = (Path(".agents"), Path(".trellis/agents"))
CODEX_DISPATCH_HEADER = """#-------------------------------------------------------------------------------
# Codex (dispatch behavior)
#-------------------------------------------------------------------------------
# Codex-only knob; other platforms ignore it. Default ("sub-agent") lets the
# main Codex session dispatch trellis-implement / trellis-check /
# trellis-research. Codex sub-agents run with `fork_turns="none"` isolation, so
# the main session must include `Active task: <task path>` in dispatch prompts
# and sub-agents fall back to `task.py current --source` if needed. Set
# "inline" only as an explicit downgrade/debug mode where the main Codex agent
# edits and checks directly.
"""
MANAGED_CONFIG = Path("config-template.yml")
MANAGED_SPEC_PATHS = (
    (
        Path("trellis/presets/guru-team/spec/workflow/semantic-retrieval.md"),
        Path(".trellis/spec/workflow/semantic-retrieval.md"),
    ),
    (
        Path("trellis/presets/guru-team/spec/workflow/workflow-contract.md"),
        Path(".trellis/spec/workflow/workflow-contract.md"),
    ),
    (
        Path("trellis/presets/guru-team/spec/workflow/skill-package-contract.md"),
        Path(".trellis/spec/workflow/skill-package-contract.md"),
    ),
    (
        Path("trellis/presets/guru-team/spec/workflow/data-contracts.md"),
        Path(".trellis/spec/workflow/data-contracts.md"),
    ),
    (
        Path("trellis/presets/guru-team/spec/workflow/companion-scripts.md"),
        Path(".trellis/spec/workflow/companion-scripts.md"),
    ),
    (
        Path("trellis/presets/guru-team/spec/workflow/quality-guidelines.md"),
        Path(".trellis/spec/workflow/quality-guidelines.md"),
    ),
)
MANAGED_ASSET_PATHS = [
    Path("config-template.yml"),
    Path("schemas/closeout-plan.schema.json"),
    Path("schemas/finish-summary.schema.json"),
    Path("schemas/marketplace-verification.schema.json"),
    Path("scripts/bash/check-env.sh"),
    Path("scripts/bash/version.sh"),
    Path("scripts/bash/prepare-task.sh"),
    Path("scripts/bash/check-workspace-boundary.sh"),
    Path("scripts/bash/check-skill-packages.sh"),
    Path("scripts/bash/discover-skill-contract.sh"),
    Path("scripts/bash/discover-skill-evals.sh"),
    Path("scripts/bash/run-skill-evals.sh"),
    Path("scripts/bash/run-skill-command.sh"),
    Path("scripts/bash/run-package-command.sh"),
    Path("scripts/bash/invoke-stage0-skill.sh"),
    Path("scripts/bash/sync-base.sh"),
    Path("scripts/bash/check-base-sync.sh"),
    Path("scripts/bash/preview-change-context-history.sh"),
    Path("scripts/bash/record-context-discovery.sh"),
    Path("scripts/bash/check-context-discovery.sh"),
    Path("scripts/bash/record-requirements-clarification.sh"),
    Path("scripts/bash/check-requirements-clarification.sh"),
    Path("scripts/bash/record-contract-wording-review.sh"),
    Path("scripts/bash/check-contract-wording-review.sh"),
    Path("scripts/bash/record-change-request-review.sh"),
    Path("scripts/bash/check-change-request-review.sh"),
    Path("scripts/bash/record-task-workspace-plan.sh"),
    Path("scripts/bash/create-task-workspace.sh"),
    Path("scripts/bash/check-task-workspace-result.sh"),
    Path("scripts/bash/resolve-human-artifacts.sh"),
    Path("scripts/bash/record-planning-approval.sh"),
    Path("scripts/bash/check-planning-approval.sh"),
    Path("scripts/bash/record-phase2-check.sh"),
    Path("scripts/bash/check-phase2-check.sh"),
    Path("scripts/bash/record-task-publication-review.sh"),
    Path("scripts/bash/check-task-publication-review.sh"),
    Path("scripts/bash/execute-extension-verification.sh"),
    Path("scripts/bash/record-extension-verification.sh"),
    Path("scripts/bash/check-extension-verification.sh"),
    Path("scripts/bash/invoke-extension-verification.sh"),
    Path("scripts/bash/preview-finalization.sh"),
    Path("scripts/bash/record-finalization-gate.sh"),
    Path("scripts/bash/check-finalization-gate.sh"),
    Path("scripts/bash/execute-finalization-transition.sh"),
    Path("scripts/bash/preview-task-pr-merge.sh"),
    Path("scripts/bash/record-task-pr-merge.sh"),
    Path("scripts/bash/check-task-pr-merge.sh"),
    Path("scripts/bash/execute-task-pr-merge.sh"),
    Path("scripts/bash/invoke-task-pr-merge.sh"),
    Path("scripts/bash/record-agent-recovery.sh"),
    Path("scripts/bash/check-agent-recovery.sh"),
    Path("scripts/bash/prepare-task-commit.sh"),
    Path("scripts/bash/check-commit-messages.sh"),
    Path("scripts/bash/create-task-commit.sh"),
    Path("scripts/bash/format-merge-commit.sh"),
    Path("scripts/bash/review-branch.sh"),
    Path("scripts/bash/check-review-gate.sh"),
    Path("scripts/bash/finish-work.sh"),
]
LEGACY_MANAGED_ASSET_HASHES = {
    Path("scripts/python/guru_team_trellis.py"): frozenset({
        # v0.6.5-guru.5, the required Issue #195 upgrade baseline.
        "c9ac793cbf02cbffa5b77e207a0c0de39fada462361d788388827798756ce9da",
        # The live main baseline from which the Issue #195 worktree was created.
        "78fb34e209c7b87eecdb515929b726dab160399001f3deed582eaaa9bcb90377",
    }),
}
LEGACY_MANAGED_ASSET_REMOVAL_SIDECAR = (
    "This former Guru Team managed runtime is obsolete after the package-local "
    "Skill runtime migration. The installed bytes do not match a known managed "
    "baseline. Review and preserve any local changes, remove the obsolete file, "
    "then delete this sidecar and reapply the preset.\n"
).encode("utf-8")
ENGLISH_LANGUAGE_RULES = (
    "**Language**: All documentation must be written in **English**.",
    "**Language**: All documentation should be written in **English**.",
)
CHINESE_LANGUAGE_RULE = (
    "**Language**: 业务项目人类可读文档默认使用**中文**；"
    "命令、路径、代码符号、配置键、GitHub keyword 等 literal token 可保留英文。"
)
RUNTIME_GITIGNORE_MARKER = "# Guru Team local runtime cache"
RUNTIME_GITIGNORE_RULE = ".trellis/.runtime/"
WORKSPACE_GITIGNORE_MARKER = "# Guru Team excludes upstream workspace journals"
WORKSPACE_GITIGNORE_RULE = ".trellis/workspace/"
AGENTS_AI_FIRST_START_MARKER = "<!-- guru-team-ai-first-principles:start -->"
AGENTS_AI_FIRST_END_MARKER = "<!-- guru-team-ai-first-principles:end -->"
AGENTS_AI_FIRST_BLOCK = f"""{AGENTS_AI_FIRST_START_MARKER}
## Guru Team AI-first 原则

- **AI-first，不模拟人类审批流**：AI 直接读取 live authority、规划、diff、测试和前序最终结果完成语义判断，不制造 assignment、handoff、签字或审批链。
- **只保留不可重新推导且有直接 consumer 的最小结果**：活动 checkpoint 默认 owner-private、短生命周期，consumer 完成后即删除。
- **任何阶段都不持久化用户授权信息或授权过程**：授权只存在于当前对话，不进入 tracked、ignored-runtime、gate、handoff、checkpoint、archive、schema 或 public DTO。
- **Digest 不是 workflow authority**：digest 只服务一个局部确定性 consumer，不绑定用户授权、semantic approval、跨 Skill handoff 或全链 freshness。
- **交互只服务真实选择和副作用**：只有真实选择、scope/authority 变化或 Git/GitHub 副作用才询问；mapped exit、stale/re-entry/reprepare/recovery 自动承接。
- **语义门禁与持久化解耦**：AI 语义门禁仍然必需；recorder/checker 不得替代判断，也不得为留下证明制造 tracked dirty。
{AGENTS_AI_FIRST_END_MARKER}
"""
SESSION_AUTO_COMMIT_HEADER = """# Guru Team owns archive and finish-summary metadata commits.
# Keep official task.py/add_session.py bookkeeping from committing implicitly.
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(["git", *args], 127, "", str(exc))


def repo_root_from_args(value: str | None) -> Path:
    root = Path(value or os.getcwd()).resolve()
    if not (root / ".trellis").is_dir():
        raise SystemExit(f"Target repo does not contain .trellis/: {root}")
    return root


def guru_root_from_script() -> Path:
    return Path(__file__).resolve().parents[5]


def load_extension_manifest(guru_root: Path) -> dict[str, Any]:
    manifest_path = guru_root / EXTENSION_MANIFEST
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing Guru Team extension manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid Guru Team extension manifest JSON: {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"Guru Team extension manifest must be a JSON object: {manifest_path}")
    for key in ["schema_version", "extension_id", "version", "workflow_template_id"]:
        if not str(payload.get(key) or "").strip():
            raise SystemExit(f"Guru Team extension manifest missing required field: {key}")
    return payload


def run_upstream_ownership_validator(guru_root: Path) -> dict[str, Any]:
    payload = validate_upstream_ownership_repository(guru_root)
    if payload.get("status") != "ok":
        first_error = next(iter(payload.get("errors") or []), {})
        code = str(first_error.get("code") or "ownership_validation_failed")
        path = str(first_error.get("path") or "unknown")
        raise SystemExit(
            "Canonical upstream ownership validation failed before preset mutation: "
            f"{code} {path}"
        )
    return payload


def ensure_managed_python_runtime(
    repo: Path,
    guru_root: Path,
    *,
    activate: bool = False,
) -> dict[str, Any]:
    runtime_assets = guru_root / "trellis/skills/guru-team/runtime"
    bootstrap = runtime_assets / "bootstrap.py"
    if not bootstrap.is_file() or bootstrap.is_symlink():
        raise_managed_runtime_error()
    command = [
            sys.executable,
            str(bootstrap),
            "--repo",
            str(repo),
            "--runtime-assets",
            str(runtime_assets),
            "--python",
            sys.executable,
            "--json",
        ]
    if not activate:
        command.append("--no-activate")
    proc = subprocess.run(
        command,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    raw = proc.stdout.strip() or proc.stderr.strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        payload = {
            "code": "runtime_dependency_missing",
            "field_path": "runtime",
            "dependency": "python-runtime",
            "runtime_identity": None,
            "remediation": "trellis/presets/guru-team/scripts/bash/apply.sh --repo .",
        }
        raise SystemExit(json.dumps(payload, sort_keys=True)) from None
    if proc.returncode != 0 or payload.get("status") != "ok":
        error = {
            "code": str(payload.get("code") or "runtime_dependency_missing"),
            "field_path": str(payload.get("field_path") or "runtime"),
            "dependency": str(payload.get("dependency") or "python-runtime"),
            "runtime_identity": payload.get("runtime_identity"),
            "remediation": str(payload.get("remediation") or "trellis/presets/guru-team/scripts/bash/apply.sh --repo ."),
        }
        raise SystemExit(json.dumps(error, sort_keys=True))
    return payload


def raise_managed_runtime_error(runtime_identity: str | None = None) -> None:
    payload = {
        "code": "runtime_dependency_missing",
        "field_path": "runtime",
        "dependency": "python-runtime",
        "runtime_identity": runtime_identity,
        "remediation": "trellis/presets/guru-team/scripts/bash/apply.sh --repo .",
    }
    raise SystemExit(json.dumps(payload, sort_keys=True))


def is_mutable_ref(ref: str | None, exact_tag: str | None) -> bool | None:
    if not ref:
        return None
    if exact_tag and ref == exact_tag:
        return False
    if ref == "HEAD":
        return True
    return not re_full_hex(ref)


def re_full_hex(value: str) -> bool:
    return len(value) == 40 and all(ch in "0123456789abcdefABCDEF" for ch in value)


def source_provenance(guru_root: Path) -> dict[str, Any]:
    top_proc = run_git(["rev-parse", "--show-toplevel"], guru_root)
    if top_proc.returncode != 0:
        return {
            "repo": None,
            "ref": None,
            "commit": None,
            "tree_state": "archive",
            "is_mutable_ref": None,
        }

    git_root = Path(top_proc.stdout.strip()).resolve()
    remote_proc = run_git(["remote", "get-url", "origin"], git_root)
    commit_proc = run_git(["rev-parse", "HEAD"], git_root)
    dirty_proc = run_git(["status", "--short"], git_root)

    commit = commit_proc.stdout.strip() if commit_proc.returncode == 0 else None
    ref = commit if isinstance(commit, str) and re_full_hex(commit) else None
    tree_state = "dirty" if dirty_proc.returncode == 0 and dirty_proc.stdout.strip() else "clean"
    if dirty_proc.returncode != 0:
        tree_state = "unknown"

    return {
        "repo": remote_proc.stdout.strip() if remote_proc.returncode == 0 and remote_proc.stdout.strip() else None,
        "ref": ref,
        "commit": commit,
        "tree_state": tree_state,
        "is_mutable_ref": is_mutable_ref(ref, None),
    }


def extension_summary(manifest: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    tested = manifest.get("tested") if isinstance(manifest.get("tested"), dict) else {}
    return {
        "extension_id": manifest.get("extension_id"),
        "version": manifest.get("version"),
        "workflow_template_id": manifest.get("workflow_template_id"),
        "target_trellis_cli": manifest.get("target_trellis_cli"),
        "tested_trellis_cli": tested.get("trellis_cli") if isinstance(tested.get("trellis_cli"), list) else [],
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref"),
        "source_commit": source.get("commit"),
        "source_tree_state": source.get("tree_state"),
        "source_is_mutable_ref": source.get("is_mutable_ref"),
    }


def build_installed_extension_manifest(
    manifest: dict[str, Any],
    source: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    managed_assets = sorted(
        (set(result["installed"]) - {".trellis/guru-team/config.yml"})
        | set(result["unchanged"])
        | set(result["updated_managed"])
        | set(result["replaced_overlays"])
        | {".trellis/guru-team/extension.json"}
    )
    return {
        "schema_version": INSTALLED_EXTENSION_SCHEMA_VERSION,
        "extension": manifest,
        "installed_at": now_iso(),
        "source": source,
        "install": {
            "selected_platforms": result["platforms"],
            "all_platforms": result["all_platforms"],
            "managed_assets": managed_assets,
            "managed_asset_hashes": result["managed_asset_hashes"],
            "new_copies": result["new_copies"],
            "managed_backups": result["managed_backups"],
            "workflow_marketplace": WORKFLOW_MARKETPLACE,
            "workflow_template": WORKFLOW_TEMPLATE,
        },
        "skill_packages": result["skill_packages"],
        "overlays": {
            key: result["overlays"][key]
            for key in (
                "schema_version",
                "status",
                "selected_platforms",
                "files",
                "removals",
                "conflicts",
                "sidecars",
            )
        },
        "notes": (
            "This file records deterministic install provenance for the Guru Team Trellis extension. "
            "source.commit and source.tree_state describe the extension source observed at apply time; "
            "they are not a claim that this installed manifest is contained in that commit. "
            "Upgrade and rollback judgment belongs to AI/human review."
        ),
    }


def write_installed_extension_manifest(dst: Path, payload: dict[str, Any]) -> str:
    path = dst / "extension.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path.name


def ensure_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | 0o755)


def load_previous_installed_manifest(dst: Path) -> dict[str, Any] | None:
    path = dst / "extension.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Installed extension manifest is not valid current JSON: {path}") from exc
    if (
        not isinstance(payload, dict)
        or set(payload) != INSTALLED_EXTENSION_KEYS
        or payload.get("schema_version") != INSTALLED_EXTENSION_SCHEMA_VERSION
    ):
        raise SystemExit(f"Installed extension manifest does not match the current contract: {path}")
    return payload


def previous_skill_hashes(
    manifest: dict[str, Any] | None,
) -> tuple[dict[str, str], set[str], bool, set[str]]:
    if manifest is None:
        return {}, set(), True, set()
    skill_packages = manifest.get("skill_packages")
    if skill_packages is None:
        return {}, set(), True, set()
    required_fields = {
        "schema_version", "status", "canonical_registry_sha256", "registry_schema_version",
        "active_ids", "selected_platforms", "packages", "files", "removals",
        "conflicts", "sidecars",
    }
    if (
        not isinstance(skill_packages, dict)
        or set(skill_packages) != required_fields
        or skill_packages.get("schema_version") != "1.0"
        or not isinstance(skill_packages.get("packages"), list)
        or not isinstance(skill_packages.get("removals"), list)
    ):
        return {}, set(), False, set()
    status = skill_packages.get("status")
    conflicts = skill_packages.get("conflicts")
    sidecars = skill_packages.get("sidecars")
    clean = status == "ok" and conflicts == [] and sidecars == []
    recovering_backups = (
        status == "conflict"
        and conflicts == []
        and isinstance(sidecars, list)
        and bool(sidecars)
    )
    if not clean and not recovering_backups:
        return {}, set(), False, set()
    files = skill_packages.get("files")
    if not isinstance(files, list):
        return {}, set(), False, set()
    hashes: dict[str, str] = {}
    paths: set[str] = set()
    valid = True
    for item in files:
        if not isinstance(item, dict):
            valid = False
            continue
        path = item.get("path")
        digest = item.get("sha256")
        if (
            not isinstance(path, str)
            or not path
            or path.startswith("/")
            or ".." in Path(path).parts
            or path in paths
        ):
            valid = False
            continue
        paths.add(path)
        if not isinstance(digest, str) or not re_full_hex_digest(digest):
            valid = False
            continue
        hashes[path] = digest
    recoverable_sidecars: set[str] = set()
    if recovering_backups:
        for sidecar in sidecars:
            relative = Path(sidecar) if isinstance(sidecar, str) else None
            if (
                relative is None
                or not sidecar.endswith(".bak")
                or sidecar.startswith("/")
                or ".." in relative.parts
                or relative.as_posix() != sidecar
                or sidecar in recoverable_sidecars
                or sidecar[:-4] not in paths
            ):
                valid = False
                continue
            recoverable_sidecars.add(sidecar)
    return hashes, paths, valid, recoverable_sidecars


def previous_overlay_hashes(
    manifest: dict[str, Any] | None,
    canonical_hashes: dict[str, str],
) -> tuple[dict[str, str], set[str], bool, set[str]]:
    """Read the exact current overlay provenance contract."""

    if manifest is None:
        return {}, set(), True, set()

    overlays = manifest.get("overlays")
    required_fields = {
        "schema_version",
        "status",
        "selected_platforms",
        "files",
        "removals",
        "conflicts",
        "sidecars",
    }
    valid = (
        isinstance(overlays, dict)
        and set(overlays) == required_fields
        and overlays.get("schema_version") == GURU_OVERLAY_SCHEMA_VERSION
        and isinstance(overlays.get("files"), list)
        and isinstance(overlays.get("removals"), list)
        and isinstance(overlays.get("conflicts"), list)
        and isinstance(overlays.get("sidecars"), list)
    )
    if not isinstance(overlays, dict):
        return {}, set(), False, set()

    selected = overlays.get("selected_platforms")
    if (
        not isinstance(selected, list)
        or any(not isinstance(item, str) or item not in ALL_PLATFORMS for item in selected)
        or selected != sorted(set(selected))
    ):
        valid = False

    hashes: dict[str, str] = {}
    paths: set[str] = set()
    files = overlays.get("files") if isinstance(overlays.get("files"), list) else []
    for item in files:
        if not isinstance(item, dict):
            valid = False
            continue
        path = item.get("path")
        digest = item.get("sha256")
        source = item.get("source")
        executable = item.get("executable")
        action = item.get("action")
        if (
            set(item) != {"path", "source", "sha256", "executable", "action"}
            or not isinstance(path, str)
            or path not in canonical_hashes
            or path in paths
            or not isinstance(source, str)
            or source != f"trellis/presets/guru-team/overlays/{path}"
            or not isinstance(digest, str)
            or not re_full_hex_digest(digest)
            or not isinstance(executable, bool)
            or action not in {"installed", "unchanged", "updated_managed"}
        ):
            valid = False
            continue
        paths.add(path)
        hashes[path] = digest

    status = overlays.get("status")
    conflicts = overlays.get("conflicts")
    sidecars = overlays.get("sidecars")
    clean = status == "ok" and conflicts == [] and sidecars == []
    recovering_backups = (
        status == "conflict"
        and conflicts == []
        and isinstance(sidecars, list)
        and bool(sidecars)
    )
    if not clean and not recovering_backups:
        valid = False

    recoverable_sidecars: set[str] = set()
    if recovering_backups:
        for sidecar in sidecars:
            relative = Path(sidecar) if isinstance(sidecar, str) else None
            if (
                relative is None
                or not sidecar.endswith(".bak")
                or sidecar.startswith("/")
                or ".." in relative.parts
                or relative.as_posix() != sidecar
                or sidecar in recoverable_sidecars
                or sidecar[:-4] not in paths
            ):
                valid = False
                continue
            recoverable_sidecars.add(sidecar)
    return hashes, paths, valid, recoverable_sidecars


def re_full_hex_digest(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def lexical_repo_relative(repo: Path, target: Path) -> Path:
    repo_abs = Path(os.path.abspath(repo))
    target_abs = Path(os.path.abspath(target))
    try:
        relative = target_abs.relative_to(repo_abs)
    except ValueError as exc:
        raise ValueError("target is outside the repository boundary") from exc
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("target has an unsafe repository-relative path")
    return relative


def lstat_repo_path(repo: Path, target: Path) -> tuple[Path, os.stat_result | None, str | None]:
    try:
        relative = lexical_repo_relative(repo, target)
    except ValueError as exc:
        return Path(), None, str(exc)
    current = Path(os.path.abspath(repo))
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            return relative, None, None
        except OSError:
            return relative, None, "path component cannot be inspected"
        if stat.S_ISLNK(current_stat.st_mode):
            return relative, current_stat, "path contains a symlink component"
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(current_stat.st_mode):
            return relative, current_stat, "path ancestor is not a directory"
    return relative, current_stat, None


def ensure_safe_repo_parents(repo: Path, target: Path) -> Path:
    relative = lexical_repo_relative(repo, target)
    current = Path(os.path.abspath(repo))
    for part in relative.parts[:-1]:
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            current.mkdir(mode=0o755)
            current_stat = current.lstat()
        if stat.S_ISLNK(current_stat.st_mode) or not stat.S_ISDIR(current_stat.st_mode):
            raise ValueError("target ancestor is not a real directory")
    return relative


def write_safe_repo_file(repo: Path, path: Path, content: bytes, mode: int) -> None:
    ensure_safe_repo_parents(repo, path)
    _, current_stat, error = lstat_repo_path(repo, path)
    if error:
        raise ValueError(error)
    if current_stat is not None and not stat.S_ISREG(current_stat.st_mode):
        raise ValueError("target is not a regular file")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, mode)
    with os.fdopen(fd, "wb") as handle:
        handle.write(content)
    path.chmod(mode)


def skill_conflict(
    path: str,
    reason: str,
    *,
    sidecar: str | None = None,
    previous_managed_sha256: str | None = None,
) -> dict[str, Any]:
    payload = {
        "path": path,
        "reason": reason,
        "remediation": "Review the preserved local path and sidecar, then remove the conflict before reapplying the preset.",
    }
    if sidecar:
        payload["sidecar"] = sidecar
    if previous_managed_sha256:
        payload["previous_managed_sha256"] = previous_managed_sha256
    return payload


def copy_provenance_managed(
    source: Path,
    target: Path,
    repo: Path,
    previous_hashes: dict[str, str],
    provenance_valid: bool,
) -> dict[str, Any]:
    try:
        relative_path = lexical_repo_relative(repo, target)
    except ValueError:
        return {"action": "conflict", "path": "<outside-repo>", "reason": "outside_repo_boundary"}
    relative = relative_path.as_posix()
    canonical = source.read_bytes()
    canonical_hash = hashlib.sha256(canonical).hexdigest()
    executable = bool(source.stat().st_mode & 0o100)
    target_mode = 0o755 if executable else 0o644

    def write_target(path: Path, content: bytes) -> None:
        write_safe_repo_file(repo, path, content, target_mode)

    _, target_stat, target_error = lstat_repo_path(repo, target)
    if target_error:
        return {"action": "conflict", "path": relative, "reason": "unsafe_path_boundary"}
    if target_stat is None:
        try:
            write_target(target, canonical)
        except ValueError:
            return {"action": "conflict", "path": relative, "reason": "unsafe_path_boundary"}
        return {"action": "installed", "path": relative, "sha256": canonical_hash, "executable": executable}
    if not stat.S_ISREG(target_stat.st_mode):
        sidecar = target.with_name(f"{target.name}.new")
        try:
            write_target(sidecar, canonical)
            sidecar_path = lexical_repo_relative(repo, sidecar).as_posix()
        except ValueError:
            sidecar_path = None
        return {
            "action": "conflict", "path": relative, "sha256": canonical_hash,
            "executable": executable, "sidecar": sidecar_path,
            "reason": "target_not_regular_file",
        }
    current = target.read_bytes()
    current_hash = hashlib.sha256(current).hexdigest()
    if current_hash == canonical_hash:
        if stat.S_IMODE(target_stat.st_mode) != target_mode:
            target.chmod(target_mode)
        return {"action": "unchanged", "path": relative, "sha256": canonical_hash, "executable": executable}
    previous_hash = previous_hashes.get(relative)
    if provenance_valid and previous_hash and current_hash == previous_hash:
        backup = target.with_name(f"{target.name}.bak")
        try:
            write_safe_repo_file(repo, backup, current, target_stat.st_mode & 0o777)
            write_target(target, canonical)
        except ValueError:
            return {"action": "conflict", "path": relative, "reason": "unsafe_sidecar_boundary"}
        return {
            "action": "updated_managed", "path": relative, "sha256": canonical_hash,
            "executable": executable, "sidecar": backup.relative_to(repo).as_posix(),
            "previous_managed_sha256": previous_hash,
        }
    sidecar = target.with_name(f"{target.name}.new")
    try:
        write_target(sidecar, canonical)
    except ValueError:
        return {"action": "conflict", "path": relative, "reason": "unsafe_sidecar_boundary"}
    return {
        "action": "conflict", "path": relative, "sha256": canonical_hash,
        "executable": executable, "sidecar": sidecar.relative_to(repo).as_posix(),
        "reason": "unknown_local_edit" if provenance_valid else "invalid_provenance",
        "previous_managed_sha256": previous_hash,
    }


def skill_registry_entries(skills_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        registry = json.loads((skills_root / "registry.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit("Canonical Guru Team skill registry is missing or invalid.") from exc
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        raise SystemExit("Canonical Guru Team skill registry has an invalid structure.")
    entries = [entry for entry in registry["skills"] if isinstance(entry, dict)]
    if len(entries) != len(registry["skills"]):
        raise SystemExit("Canonical Guru Team skill registry contains a non-object entry.")
    return registry, entries


SKILL_MANAGED_ROOTS = (
    Path(".trellis/guru-team/skills"),
    Path(".trellis/guru-team/runtime"),
    Path(".agents/skills"),
    Path(".codex/skills"),
    Path(".cursor/skills"),
    Path(".claude/skills"),
)


def skill_path_is_managed(relative: Path) -> bool:
    return any(relative == root or root in relative.parents for root in SKILL_MANAGED_ROOTS)


def prune_empty_managed_skill_parents(repo: Path, path: Path) -> None:
    relative = lexical_repo_relative(repo, path)
    managed_root = next((root for root in SKILL_MANAGED_ROOTS if root in relative.parents), None)
    if managed_root is None:
        return
    current = path.parent
    stop = Path(os.path.abspath(repo)) / managed_root
    while current != stop and stop in current.parents:
        _, current_stat, error = lstat_repo_path(repo, current)
        if error or current_stat is None or not stat.S_ISDIR(current_stat.st_mode):
            return
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def remove_stale_skill_path(
    repo: Path,
    relative_text: str,
    previous_hashes: dict[str, str],
    provenance_valid: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    relative = Path(relative_text)
    if not skill_path_is_managed(relative):
        return None, skill_conflict(relative_text, "previous_path_outside_skill_roots"), None
    target = Path(os.path.abspath(repo)) / relative
    checked_relative, target_stat, error = lstat_repo_path(repo, target)
    if error or checked_relative != relative:
        return None, skill_conflict(relative_text, "unsafe_stale_path_boundary"), None
    if target_stat is None:
        return {"path": relative_text, "action": "already_missing"}, None, None
    if not stat.S_ISREG(target_stat.st_mode):
        return None, skill_conflict(relative_text, "stale_target_not_regular_file"), None
    current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    previous_hash = previous_hashes.get(relative_text)
    if provenance_valid and previous_hash and current_hash == previous_hash:
        target.unlink()
        prune_empty_managed_skill_parents(repo, target)
        return {
            "path": relative_text,
            "action": "removed_managed",
            "previous_managed_sha256": previous_hash,
        }, None, None
    sidecar = target.with_name(f"{target.name}.new")
    removal_notice = (
        "Guru Team managed removal requested. Review the adjacent preserved local file, "
        "remove it or migrate its content, then delete this sidecar and reapply the preset.\n"
    ).encode("utf-8")
    try:
        write_safe_repo_file(repo, sidecar, removal_notice, 0o644)
        sidecar_relative = lexical_repo_relative(repo, sidecar).as_posix()
    except ValueError:
        sidecar_relative = None
    reason = "stale_unknown_local_edit" if provenance_valid else "stale_invalid_provenance"
    return None, skill_conflict(
        relative_text,
        reason,
        sidecar=sidecar_relative,
        previous_managed_sha256=previous_hash,
    ), sidecar_relative


def run_skill_package_validator(
    repo: Path,
    guru_root: Path,
    mode: str,
    python: Path | None = None,
) -> dict[str, Any]:
    runtime_root = (
        guru_root / "trellis/skills/guru-team"
        if mode == "source"
        else repo / ".trellis/guru-team"
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(runtime_root) + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH")
        else ""
    )
    proc = subprocess.run(
        [str(python or sys.executable), "-m", "runtime.validate", "--json", "--mode", mode, "--root", str(repo)],
        cwd=repo,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    raw = proc.stdout.strip() or proc.stderr.strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"status": "failed", "mode": mode, "facts": {}, "errors": ["skill package validator returned invalid JSON"]}
    if not isinstance(payload, dict):
        payload = {"status": "failed", "mode": mode, "facts": {}, "errors": ["skill package validator returned a non-object payload"]}
    payload["returncode"] = proc.returncode
    return payload


def skill_package_source_files(package_root: Path) -> list[Path]:
    return sorted(
        path
        for path in package_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in path.relative_to(package_root).parts
        and path.suffix not in {".pyc", ".pyo"}
    )


def skill_platform_public_files(package_root: Path) -> list[Path]:
    """Return the Agent-readable projection without package-private runtime assets."""
    interface = json.loads((package_root / "interface.json").read_text(encoding="utf-8"))
    private_paths = {
        str(item["schema"]["path"])
        for item in interface.get("public_contracts", {}).get("private_artifacts", [])
        if isinstance(item, dict)
        and isinstance(item.get("schema"), dict)
        and isinstance(item["schema"].get("path"), str)
    }
    private_artifact_paths = {
        str(item["path"])
        for item in interface.get("artifacts", [])
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and str(item["path"]) not in {
            str(ref.get("example", {}).get("path"))
            for ref in interface.get("public_contracts", {}).get("outputs", [])
            if isinstance(ref, dict) and isinstance(ref.get("example"), dict)
        }
    }
    public_wrapper = str(
        interface.get("public_contracts", {})
        .get("invocation", {})
        .get("wrapper", "")
    )
    excluded_roots = {"runtime", "tests", "errors"}
    return [
        path
        for path in skill_package_source_files(package_root)
        if path.relative_to(package_root).parts[0] not in excluded_roots
        and (
            path.relative_to(package_root).parts[0] != "scripts"
            or path.relative_to(package_root).as_posix() == public_wrapper
        )
        and path.relative_to(package_root).as_posix() not in private_paths
        and path.relative_to(package_root).as_posix() not in private_artifact_paths
    ]


def install_skill_packages(
    repo: Path,
    guru_root: Path,
    dst: Path,
    platforms: set[str],
    previous_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    canonical_root = guru_root / "trellis/skills/guru-team"
    registry, entries = skill_registry_entries(canonical_root)
    previous_hash_map, previous_paths, provenance_valid, recoverable_sidecars = previous_skill_hashes(
        previous_manifest
    )
    pending_recovery_sidecars: list[str] = []
    if provenance_valid:
        for sidecar_text in sorted(recoverable_sidecars):
            sidecar = Path(os.path.abspath(repo)) / Path(sidecar_text)
            checked_relative, sidecar_stat, sidecar_error = lstat_repo_path(repo, sidecar)
            if (
                sidecar_error
                or checked_relative.as_posix() != sidecar_text
                or (sidecar_stat is not None and not stat.S_ISREG(sidecar_stat.st_mode))
            ):
                provenance_valid = False
                pending_recovery_sidecars = []
                break
            if sidecar_stat is not None:
                pending_recovery_sidecars.append(sidecar_text)
    active_entries = [entry for entry in entries if entry.get("state") == "active"]
    active_ids = sorted(str(entry.get("id")) for entry in active_entries)
    source_files: list[tuple[Path, Path]] = [
        (canonical_root / "registry.json", Path("registry.json")),
    ]
    finish_integration_test = canonical_root / "tests/test_finish_family_integration.py"
    if not finish_integration_test.is_file() or finish_integration_test.is_symlink():
        raise SystemExit("Canonical Finish family integration test is missing or unsafe.")
    source_files.append(
        (
            finish_integration_test,
            finish_integration_test.relative_to(canonical_root),
        )
    )
    for shared_root_name in ("schemas", "adapters", "contracts"):
        shared_root = canonical_root / shared_root_name
        if shared_root.is_dir():
            for source in skill_package_source_files(shared_root):
                if (
                    shared_root_name == "schemas"
                    and source.name not in CURRENT_SKILL_SHARED_SCHEMAS
                ):
                    continue
                source_files.append((source, source.relative_to(canonical_root)))
    consumer_root = canonical_root / "consumers"
    if consumer_root.is_dir():
        for source in skill_package_source_files(consumer_root):
            source_files.append((source, source.relative_to(canonical_root)))
    packages: list[dict[str, Any]] = []
    for entry in active_entries:
        skill_id = str(entry["id"])
        package_root = canonical_root / str(entry["package"])
        package_files = skill_package_source_files(package_root)
        for source in package_files:
            source_files.append((source, source.relative_to(canonical_root)))
        interface_path = canonical_root / str(entry["interface"])
        tree_hash = hashlib.sha256()
        for source in package_files:
            rel = source.relative_to(package_root).as_posix()
            tree_hash.update(rel.encode("utf-8") + b"\0" + source.read_bytes() + b"\0")
        packages.append({
            "id": skill_id,
            "interface_sha256": hashlib.sha256(interface_path.read_bytes()).hexdigest(),
            "tree_sha256": tree_hash.hexdigest(),
        })

    records: list[dict[str, Any]] = []
    removals: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    sidecars: list[str] = list(pending_recovery_sidecars)

    if not provenance_valid:
        conflicts.append(skill_conflict(
            ".trellis/guru-team/extension.json",
            "invalid_previous_provenance",
        ))

    def install_one(source: Path, target: Path) -> None:
        result = copy_provenance_managed(source, target, repo, previous_hash_map, provenance_valid)
        if result["action"] == "conflict":
            sidecar = result.get("sidecar")
            conflict = skill_conflict(
                result["path"],
                str(result.get("reason") or "skill_install_conflict"),
                sidecar=str(sidecar) if sidecar else None,
                previous_managed_sha256=result.get("previous_managed_sha256"),
            )
            conflicts.append(conflict)
            if sidecar:
                sidecars.append(str(sidecar))
            return
        record = {
            "path": result["path"],
            "source": source.relative_to(guru_root).as_posix(),
            "sha256": result["sha256"],
            "executable": result["executable"],
            "action": result["action"],
        }
        records.append(record)
        if result.get("sidecar"):
            sidecars.append(str(result["sidecar"]))

    desired_files: list[tuple[Path, Path]] = []
    installed_root = dst / "skills"
    for source, relative in source_files:
        desired_files.append((source, installed_root / relative))
    runtime_root = canonical_root / "runtime"
    if runtime_root.is_dir():
        for relative in SKILL_RUNTIME_KERNEL_PATHS:
            source = runtime_root / relative
            if not source.is_file() or source.is_symlink():
                raise SystemExit(f"Missing canonical Skill runtime kernel file: {source}")
            desired_files.append((source, dst / "runtime" / relative))

    destination_roots = [
        (
            platform,
            Path(".agents/skills")
            if platform == "shared"
            else PLATFORM_OVERLAY_PREFIXES[platform][0] / "skills",
        )
        for platform in SKILL_DESTINATION_PLATFORM_ORDER
        if platform == "shared" or platform in platforms
    ]
    for entry in active_entries:
        skill_id = str(entry["id"])
        supported = set(entry.get("supported_platforms") or [])
        package_root = canonical_root / str(entry["package"])
        package_files = skill_platform_public_files(package_root)
        for platform, target_root in destination_roots:
            if platform not in supported:
                continue
            for source in package_files:
                desired_files.append((source, repo / target_root / skill_id / source.relative_to(package_root)))

    desired_paths = {
        lexical_repo_relative(repo, target).as_posix()
        for _, target in desired_files
    }
    for source, target in desired_files:
        install_one(source, target)
    for stale_path in sorted(previous_paths - desired_paths):
        removal, conflict, sidecar = remove_stale_skill_path(
            repo,
            stale_path,
            previous_hash_map,
            provenance_valid,
        )
        if removal:
            removals.append(removal)
        if conflict:
            conflicts.append(conflict)
        if sidecar:
            sidecars.append(sidecar)

    status = "ok" if provenance_valid and not conflicts and not sidecars else "conflict"
    return {
        "schema_version": "1.0",
        "status": status,
        "canonical_registry_sha256": hashlib.sha256((canonical_root / "registry.json").read_bytes()).hexdigest(),
        "registry_schema_version": registry.get("schema_version"),
        "active_ids": active_ids,
        "selected_platforms": sorted(platforms),
        "packages": packages,
        "files": records,
        "removals": removals,
        "conflicts": conflicts,
        "sidecars": sorted(sidecars),
    }


def ensure_runtime_gitignore(repo: Path) -> dict[str, str]:
    path = repo / ".gitignore"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines()
    if RUNTIME_GITIGNORE_RULE in {line.strip() for line in lines}:
        return {"action": "unchanged", "path": ".gitignore", "rule": RUNTIME_GITIGNORE_RULE}
    separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    path.write_text(f"{original}{separator}{RUNTIME_GITIGNORE_MARKER}\n{RUNTIME_GITIGNORE_RULE}\n", encoding="utf-8")
    return {"action": "updated" if original else "installed", "path": ".gitignore", "rule": RUNTIME_GITIGNORE_RULE}


def ensure_workspace_gitignore(repo: Path) -> dict[str, str]:
    path = repo / ".gitignore"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if WORKSPACE_GITIGNORE_RULE in {line.strip() for line in original.splitlines()}:
        return {"action": "unchanged", "path": ".gitignore", "rule": WORKSPACE_GITIGNORE_RULE}
    separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    path.write_text(
        f"{original}{separator}{WORKSPACE_GITIGNORE_MARKER}\n{WORKSPACE_GITIGNORE_RULE}\n",
        encoding="utf-8",
    )
    return {"action": "updated" if original else "installed", "path": ".gitignore", "rule": WORKSPACE_GITIGNORE_RULE}


def ensure_agents_ai_first_principles(repo: Path) -> dict[str, str]:
    path = repo / "AGENTS.md"
    exists = path.exists() or path.is_symlink()
    if exists:
        try:
            path_stat = path.lstat()
        except OSError as exc:
            raise SystemExit(f"Cannot inspect target AGENTS.md: {exc}") from exc
        if not stat.S_ISREG(path_stat.st_mode):
            raise SystemExit("Target AGENTS.md must be a regular file")
        try:
            original = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SystemExit("Target AGENTS.md must be valid UTF-8") from exc
    else:
        original = ""

    start_count = original.count(AGENTS_AI_FIRST_START_MARKER)
    end_count = original.count(AGENTS_AI_FIRST_END_MARKER)
    if start_count == 0 and end_count == 0:
        separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
        updated = f"{original}{separator}{AGENTS_AI_FIRST_BLOCK}"
        action = "updated" if exists else "installed"
    else:
        if start_count != 1 or end_count != 1:
            raise SystemExit("Target AGENTS.md contains malformed or duplicate Guru Team AI-first markers")
        lines = original.splitlines(keepends=True)
        start_indexes = [
            index
            for index, line in enumerate(lines)
            if line.rstrip("\r\n") == AGENTS_AI_FIRST_START_MARKER
        ]
        end_indexes = [
            index
            for index, line in enumerate(lines)
            if line.rstrip("\r\n") == AGENTS_AI_FIRST_END_MARKER
        ]
        if len(start_indexes) != 1 or len(end_indexes) != 1 or start_indexes[0] >= end_indexes[0]:
            raise SystemExit("Target AGENTS.md contains malformed or out-of-order Guru Team AI-first markers")
        start_index = start_indexes[0]
        end_index = end_indexes[0]
        current_block = "".join(lines[start_index : end_index + 1])
        if current_block == AGENTS_AI_FIRST_BLOCK:
            return {
                "action": "unchanged",
                "path": "AGENTS.md",
                "marker": AGENTS_AI_FIRST_START_MARKER,
            }
        updated = "".join(lines[:start_index]) + AGENTS_AI_FIRST_BLOCK + "".join(lines[end_index + 1 :])
        action = "updated"

    path.write_bytes(updated.encode("utf-8"))
    return {"action": action, "path": "AGENTS.md", "marker": AGENTS_AI_FIRST_START_MARKER}


def ensure_session_auto_commit_false(repo: Path) -> dict[str, str | None]:
    path = repo / ".trellis/config.yaml"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines()
    active_indexes: list[int] = []
    previous: str | None = None
    for index, line in enumerate(lines):
        if line.startswith("session_auto_commit:"):
            active_indexes.append(index)
            if previous is None:
                previous = strip_inline_comment(line.split(":", 1)[1]) or None
    if len(active_indexes) > 1:
        raise SystemExit(".trellis/config.yaml contains duplicate top-level session_auto_commit keys")
    if active_indexes and previous == "false":
        return {"action": "unchanged", "path": ".trellis/config.yaml", "previous": "false", "value": "false"}
    if active_indexes:
        lines[active_indexes[0]] = "session_auto_commit: false"
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": previous, "value": "false"}
    separator = "" if not original else ("\n" if original.endswith("\n") else "\n\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"{original}{separator}{SESSION_AUTO_COMMIT_HEADER}session_auto_commit: false\n",
        encoding="utf-8",
    )
    return {"action": "updated" if original else "installed", "path": ".trellis/config.yaml", "previous": None, "value": "false"}


def path_has_prefix(path: Path, prefix: Path) -> bool:
    return path == prefix or prefix in path.parents


def overlay_selected(relative: Path, platforms: set[str]) -> bool:
    if any(path_has_prefix(relative, prefix) for prefix in ALWAYS_OVERLAY_PREFIXES):
        return True
    selected_prefixes = [
        prefix
        for platform in sorted(platforms)
        for prefix in PLATFORM_OVERLAY_PREFIXES[platform]
    ]
    return any(path_has_prefix(relative, prefix) for prefix in selected_prefixes)


def selected_platforms(platforms: list[str] | None, all_platforms: bool) -> tuple[set[str], bool]:
    if all_platforms:
        return set(ALL_PLATFORMS), True
    if platforms:
        return set(platforms), False
    return set(DEFAULT_PLATFORMS), False


def leading_spaces(value: str) -> int:
    return len(value) - len(value.lstrip(" "))


def strip_inline_comment(value: str) -> str:
    return value.split("#", 1)[0].strip().strip("\"'")


def ensure_codex_dispatch_mode(repo: Path) -> dict[str, str | None]:
    """Materialize the Guru Team Codex default in project .trellis/config.yaml.

    Explicit `dispatch_mode: inline` is a user downgrade and is preserved.
    Missing, commented-out, or invalid values are updated to `sub-agent` so
    Codex can satisfy the independent Branch Review Gate path by default.
    """

    config_path = repo / ".trellis/config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(f"{CODEX_DISPATCH_HEADER}codex:\n  dispatch_mode: sub-agent\n", encoding="utf-8")
        return {"action": "installed", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}

    original = config_path.read_text(encoding="utf-8")
    lines = original.splitlines()
    codex_index: int | None = None
    codex_indent = 0
    dispatch_index: int | None = None
    dispatch_value: str | None = None

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "codex:":
            codex_index = index
            codex_indent = leading_spaces(line)
            continue
        if codex_index is not None:
            indent = leading_spaces(line)
            if indent <= codex_indent:
                break
            if stripped.startswith("dispatch_mode:"):
                dispatch_index = index
                dispatch_value = strip_inline_comment(stripped.split(":", 1)[1])
                break

    if dispatch_value in {"sub-agent", "inline"}:
        return {
            "action": "unchanged",
            "path": ".trellis/config.yaml",
            "previous": dispatch_value,
            "mode": dispatch_value,
        }

    if dispatch_index is not None:
        indent = " " * leading_spaces(lines[dispatch_index])
        previous = dispatch_value or None
        lines[dispatch_index] = f"{indent}dispatch_mode: sub-agent"
        updated = "\n".join(lines).rstrip() + "\n"
        config_path.write_text(updated, encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": previous, "mode": "sub-agent"}

    if codex_index is not None:
        insert_at = codex_index + 1
        child_indent = " " * (codex_indent + 2)
        while insert_at < len(lines):
            line = lines[insert_at]
            if line.strip() and not line.lstrip().startswith("#") and leading_spaces(line) <= codex_indent:
                break
            insert_at += 1
        lines.insert(insert_at, f"{child_indent}dispatch_mode: sub-agent")
        updated = "\n".join(lines).rstrip() + "\n"
        config_path.write_text(updated, encoding="utf-8")
        return {"action": "updated", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}

    separator = "" if original.endswith("\n") or not original else "\n"
    addition = f"{separator}\n{CODEX_DISPATCH_HEADER}codex:\n  dispatch_mode: sub-agent\n"
    config_path.write_text(original.rstrip() + addition, encoding="utf-8")
    return {"action": "updated", "path": ".trellis/config.yaml", "previous": None, "mode": "sub-agent"}


def copy_managed(source: Path, target: Path) -> dict[str, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(source, target)
        return {"path": str(target), "action": "installed"}
    if filecmp.cmp(source, target, shallow=False):
        return {"path": str(target), "action": "unchanged"}
    backup = target.with_name(f"{target.name}.bak")
    shutil.copyfile(target, backup)
    shutil.copyfile(source, target)
    return {"path": str(target), "action": "updated_managed", "backup": str(backup)}


def copy_managed_spec(
    source: Path,
    target: Path,
    repo: Path,
    previous_manifest: dict[str, Any] | None,
) -> dict[str, str]:
    relative = target.relative_to(repo).as_posix()
    previous_hashes = {}
    if isinstance(previous_manifest, dict):
        install = previous_manifest.get("install")
        if isinstance(install, dict) and isinstance(install.get("managed_asset_hashes"), dict):
            previous_hashes = install["managed_asset_hashes"]
    if not target.exists() or filecmp.cmp(source, target, shallow=False):
        return copy_managed(source, target)
    previous_hash = previous_hashes.get(relative)
    current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if isinstance(previous_hash, str) and re_full_hex_digest(previous_hash) and current_hash == previous_hash:
        return copy_managed(source, target)
    sidecar = target.with_name(f"{target.name}.new")
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, sidecar)
    return {"path": str(target), "action": "conflict", "sidecar": str(sidecar)}


def remove_legacy_managed_assets(
    repo: Path,
    dst: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    removals: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    sidecars: list[str] = []
    for relative, known_hashes in LEGACY_MANAGED_ASSET_HASHES.items():
        target = dst / relative
        relative_target = lexical_repo_relative(repo, target)
        checked_relative, target_stat, error = lstat_repo_path(repo, target)
        if error or checked_relative != relative_target:
            conflicts.append(skill_conflict(relative_target.as_posix(), "unsafe_legacy_path_boundary"))
            continue
        if target_stat is None:
            continue
        if not stat.S_ISREG(target_stat.st_mode):
            conflicts.append(skill_conflict(relative_target.as_posix(), "legacy_target_not_regular_file"))
            continue
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest in known_hashes:
            target.unlink()
            removals.append({
                "path": relative_target.as_posix(),
                "action": "removed_managed",
                "previous_managed_sha256": digest,
            })
            continue
        sidecar = target.with_name(f"{target.name}.new")
        try:
            write_safe_repo_file(repo, sidecar, LEGACY_MANAGED_ASSET_REMOVAL_SIDECAR, 0o644)
            sidecar_relative = lexical_repo_relative(repo, sidecar).as_posix()
        except ValueError:
            sidecar_relative = None
        conflicts.append(skill_conflict(
            relative_target.as_posix(),
            "legacy_unknown_local_edit",
            sidecar=sidecar_relative,
            previous_managed_sha256=digest,
        ))
        if sidecar_relative:
            sidecars.append(sidecar_relative)
    return removals, conflicts, sidecars


def prune_empty_overlay_parents(repo: Path, path: Path) -> None:
    relative = lexical_repo_relative(repo, path)
    platform_root = next(
        (
            prefix
            for prefixes in PLATFORM_OVERLAY_PREFIXES.values()
            for prefix in prefixes
            if prefix in relative.parents
        ),
        None,
    )
    if platform_root is None:
        return
    current = path.parent
    stop = Path(os.path.abspath(repo)) / platform_root
    while current != stop and stop in current.parents:
        _, current_stat, error = lstat_repo_path(repo, current)
        if error or current_stat is None or not stat.S_ISDIR(current_stat.st_mode):
            return
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def remove_stale_overlay_path(
    repo: Path,
    relative_text: str,
    previous_hashes: dict[str, str],
    provenance_valid: bool,
    canonical_hashes: dict[str, str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    if relative_text not in canonical_hashes:
        return None, skill_conflict(relative_text, "previous_path_outside_overlay_inventory"), None
    relative = Path(relative_text)
    target = Path(os.path.abspath(repo)) / relative
    checked_relative, target_stat, error = lstat_repo_path(repo, target)
    if error or checked_relative != relative:
        return None, skill_conflict(relative_text, "unsafe_stale_path_boundary"), None
    if target_stat is None:
        return {"path": relative_text, "action": "already_missing"}, None, None
    if not stat.S_ISREG(target_stat.st_mode):
        return None, skill_conflict(relative_text, "stale_target_not_regular_file"), None

    current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    previous_hash = previous_hashes.get(relative_text)
    if provenance_valid and previous_hash is not None and current_hash == previous_hash:
        target.unlink()
        prune_empty_overlay_parents(repo, target)
        return {
            "path": relative_text,
            "action": "removed_managed",
            "previous_managed_sha256": previous_hash,
        }, None, None

    sidecar = target.with_name(f"{target.name}.new")
    try:
        write_safe_repo_file(repo, sidecar, GURU_OVERLAY_REMOVAL_SIDECAR, 0o644)
        sidecar_relative = lexical_repo_relative(repo, sidecar).as_posix()
    except ValueError:
        sidecar_relative = None
    reason = "stale_unknown_local_edit" if provenance_valid else "stale_invalid_provenance"
    return None, skill_conflict(
        relative_text,
        reason,
        sidecar=sidecar_relative,
        previous_managed_sha256=previous_hash,
    ), sidecar_relative


def language_guidance_targets(repo: Path) -> list[Path]:
    targets: set[Path] = set()
    spec_root = repo / ".trellis/spec"
    if spec_root.is_dir():
        targets.update(path for path in spec_root.rglob("*.md") if path.is_file())

    bootstrap_root = repo / ".trellis/tasks/00-bootstrap-guidelines"
    if bootstrap_root.is_dir():
        targets.update(path for path in bootstrap_root.rglob("*.md") if path.is_file())

    return sorted(targets)


def normalize_business_doc_language_guidance(repo: Path) -> dict[str, Any]:
    checked_paths: list[str] = []
    updated_paths: list[dict[str, Any]] = []
    replacement_count = 0

    for path in language_guidance_targets(repo):
        rel_path = path.relative_to(repo).as_posix()
        checked_paths.append(rel_path)
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = original
        path_replacements = 0
        for english_rule in ENGLISH_LANGUAGE_RULES:
            occurrences = updated.count(english_rule)
            if occurrences:
                updated = updated.replace(english_rule, CHINESE_LANGUAGE_RULE)
                path_replacements += occurrences

        if path_replacements:
            path.write_text(updated, encoding="utf-8")
            replacement_count += path_replacements
            updated_paths.append({"path": rel_path, "replacements": path_replacements})

    return {
        "action": "updated" if replacement_count else "checked",
        "rule": "business-project-human-readable-docs-default-chinese",
        "replacement": CHINESE_LANGUAGE_RULE,
        "checked_paths": checked_paths,
        "updated_paths": updated_paths,
        "replacement_count": replacement_count,
        "scope": [
            ".trellis/spec/**/*.md",
            ".trellis/tasks/00-bootstrap-guidelines/**/*.md",
        ],
    }


TRANSACTION_IGNORED_ROOTS = (
    Path(".git"),
    Path(".trellis/.developer"),
    Path(".trellis/.runtime"),
    Path(".trellis/workspace"),
)


def transaction_path_ignored(relative: Path) -> bool:
    return (
        any(relative == root or root in relative.parents for root in TRANSACTION_IGNORED_ROOTS)
        or "__pycache__" in relative.parts
        or relative.suffix in {".pyc", ".pyo"}
    )


def copy_repo_to_staging(repo: Path, staging_repo: Path) -> None:
    repo = Path(os.path.abspath(repo))

    def ignored(directory: str, names: list[str]) -> set[str]:
        directory_path = Path(directory)
        relative_directory = directory_path.relative_to(repo)
        ignored_names: set[str] = set()
        for name in names:
            relative = relative_directory / name
            if transaction_path_ignored(relative):
                ignored_names.add(name)
        return ignored_names

    shutil.copytree(repo, staging_repo, symlinks=True, ignore=ignored)


def transaction_tree_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        relative_directory = directory_path.relative_to(root)
        directory_names[:] = [
            name
            for name in directory_names
            if not transaction_path_ignored(relative_directory / name)
        ]
        for name in file_names:
            relative = relative_directory / name
            if not transaction_path_ignored(relative):
                files.add(relative)
    return files


def staged_file_matches_target(staged: Path, target: Path) -> bool:
    try:
        staged_stat = staged.lstat()
        target_stat = target.lstat()
    except FileNotFoundError:
        return False
    if not stat.S_ISREG(staged_stat.st_mode) or not stat.S_ISREG(target_stat.st_mode):
        if stat.S_ISLNK(staged_stat.st_mode) and stat.S_ISLNK(target_stat.st_mode):
            return os.readlink(staged) == os.readlink(target)
        return False
    return (
        stat.S_IMODE(staged_stat.st_mode) == stat.S_IMODE(target_stat.st_mode)
        and filecmp.cmp(staged, target, shallow=False)
    )


def activate_staged_repository(staging_repo: Path, repo: Path) -> None:
    staged_files = transaction_tree_files(staging_repo)
    target_files = transaction_tree_files(repo)
    writes = sorted(
        (
            relative
            for relative in staged_files
            if relative not in target_files
            or not staged_file_matches_target(staging_repo / relative, repo / relative)
        ),
        key=lambda relative: (
            relative == Path(".trellis/guru-team/extension.json"),
            relative.as_posix(),
        ),
    )
    removals = sorted(target_files - staged_files, key=lambda relative: relative.as_posix())

    for relative in removals:
        _, target_stat, error = lstat_repo_path(repo, repo / relative)
        if error or target_stat is None or not stat.S_ISREG(target_stat.st_mode):
            raise SystemExit(f"Cannot activate staged removal for non-regular path: {relative.as_posix()}")
    for relative in writes:
        staged = staging_repo / relative
        staged_stat = staged.lstat()
        if not stat.S_ISREG(staged_stat.st_mode):
            raise SystemExit(f"Cannot activate staged non-regular path: {relative.as_posix()}")
        _, target_stat, error = lstat_repo_path(repo, repo / relative)
        if error or (target_stat is not None and not stat.S_ISREG(target_stat.st_mode)):
            raise SystemExit(f"Cannot activate staged path across an unsafe target: {relative.as_posix()}")

    for relative in removals:
        (repo / relative).unlink()
    for relative in writes:
        staged = staging_repo / relative
        mode = stat.S_IMODE(staged.stat().st_mode)
        write_safe_repo_file(repo, repo / relative, staged.read_bytes(), mode)

    staged_directories = {
        path.relative_to(staging_repo)
        for path in staging_repo.rglob("*")
        if path.is_dir() and not path.is_symlink() and not transaction_path_ignored(path.relative_to(staging_repo))
    }
    target_directories = sorted(
        (
            path
            for path in repo.rglob("*")
            if path.is_dir()
            and not path.is_symlink()
            and not transaction_path_ignored(path.relative_to(repo))
            and path.relative_to(repo) not in staged_directories
        ),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for path in target_directories:
        try:
            path.rmdir()
        except OSError:
            continue


def materialize_staged_conflict_sidecars(
    staging_repo: Path,
    repo: Path,
    result: dict[str, Any],
) -> None:
    sidecars = {
        str(path)
        for path in result.get("new_copies", [])
        if isinstance(path, str) and path.endswith(".new")
    }
    skill_packages = result.get("skill_packages")
    if isinstance(skill_packages, dict):
        sidecars.update(
            str(path)
            for path in skill_packages.get("sidecars", [])
            if isinstance(path, str) and path.endswith(".new")
        )
    overlays = result.get("overlays")
    if isinstance(overlays, dict):
        sidecars.update(
            str(path)
            for path in overlays.get("sidecars", [])
            if isinstance(path, str) and path.endswith(".new")
        )
    for sidecar_text in sorted(sidecars):
        relative = Path(sidecar_text)
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"Invalid staged conflict sidecar path: {sidecar_text}")
        staged = staging_repo / relative
        try:
            staged_stat = staged.lstat()
        except FileNotFoundError as exc:
            raise SystemExit(f"Missing staged conflict sidecar: {sidecar_text}") from exc
        if not stat.S_ISREG(staged_stat.st_mode):
            raise SystemExit(f"Staged conflict sidecar is not a regular file: {sidecar_text}")
        write_safe_repo_file(
            repo,
            repo / relative,
            staged.read_bytes(),
            stat.S_IMODE(staged_stat.st_mode),
        )
def managed_backup_recovery_candidate(result: dict[str, Any]) -> bool:
    sections = [result.get("skill_packages"), result.get("overlays")]
    if any(not isinstance(section, dict) for section in sections):
        return False
    sidecars: list[str] = []
    has_conflict_status = False
    for section in sections:
        assert isinstance(section, dict)
        section_sidecars = section.get("sidecars")
        if (
            section.get("status") not in {"ok", "conflict"}
            or section.get("conflicts") != []
            or not isinstance(section_sidecars, list)
        ):
            return False
        if section.get("status") == "conflict":
            has_conflict_status = True
        sidecars.extend(section_sidecars)
    return (
        has_conflict_status
        and bool(sidecars)
        and len(sidecars) == len(set(sidecars))
        and all(isinstance(path, str) and path.endswith(".bak") for path in sidecars)
    )


def validate_staged_graph_without_recovery_backups(
    staging_repo: Path,
    guru_root: Path,
    result: dict[str, Any],
    python: Path,
) -> dict[str, Any]:
    if not managed_backup_recovery_candidate(result):
        return result["skill_installed_validation"]
    manifest_path = staging_repo / ".trellis/guru-team/extension.json"
    original_manifest = manifest_path.read_bytes()
    manifest = json.loads(original_manifest)
    sections = [manifest["skill_packages"], manifest["overlays"]]
    sidecars = sorted({
        str(path)
        for section in sections
        for path in section["sidecars"]
    })
    recovery_root = staging_repo.parent / "recovery-sidecars"
    moved: list[tuple[Path, Path]] = []
    try:
        recovery_root.mkdir()
        for index, sidecar_text in enumerate(sidecars):
            sidecar = staging_repo / sidecar_text
            checked_relative, sidecar_stat, error = lstat_repo_path(staging_repo, sidecar)
            if (
                error
                or checked_relative.as_posix() != sidecar_text
                or sidecar_stat is None
                or not stat.S_ISREG(sidecar_stat.st_mode)
            ):
                return {
                    "status": "failed",
                    "mode": "installed",
                    "facts": {},
                    "errors": ["recoverable managed backup inventory is invalid"],
                    "returncode": 2,
                }
            parked = recovery_root / str(index)
            sidecar.replace(parked)
            moved.append((parked, sidecar))
        for section in sections:
            section["status"] = "ok"
            section["sidecars"] = []
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return run_skill_package_validator(staging_repo, guru_root, "installed", python)
    finally:
        manifest_path.write_bytes(original_manifest)
        for parked, sidecar in reversed(moved):
            sidecar.parent.mkdir(parents=True, exist_ok=True)
            parked.replace(sidecar)


def install_assets(
    src: Path,
    dst: Path,
    repo: Path,
    platforms: set[str] | None = None,
    all_platforms: bool = False,
) -> dict[str, Any]:
    if not src.is_dir():
        raise SystemExit(f"Missing source directory: {src}")

    guru_root = guru_root_from_script()
    upstream_ownership_validation = run_upstream_ownership_validator(guru_root)
    repo = Path(os.path.abspath(repo))
    python_runtime = ensure_managed_python_runtime(repo, guru_root, activate=False)
    managed_python = Path(str(python_runtime.get("interpreter") or ""))
    if not managed_python.is_file() or not os.access(managed_python, os.X_OK):
        raise_managed_runtime_error(str(python_runtime.get("runtime_identity") or "") or None)
    source_validation = run_skill_package_validator(guru_root, guru_root, "source", managed_python)
    if source_validation.get("returncode") != 0:
        raise SystemExit("Canonical Guru Team skill package validation failed before preset mutation.")
    dst_relative = lexical_repo_relative(repo, dst)
    with tempfile.TemporaryDirectory(prefix="guru-team-preset-stage-") as temporary:
        staging_repo = Path(temporary) / "repo"
        copy_repo_to_staging(repo, staging_repo)
        result = _install_assets_in_place(
            src,
            staging_repo / dst_relative,
            staging_repo,
            platforms,
            all_platforms=all_platforms,
            source_validation=source_validation,
            upstream_ownership_validation=upstream_ownership_validation,
            managed_python=managed_python,
        )
        result["python_runtime"] = python_runtime
        skill_packages = result["skill_packages"]
        overlays = result["overlays"]
        installed_validation = result["skill_installed_validation"]
        activation_ready = (
            skill_packages["status"] == "ok"
            and overlays["status"] == "ok"
            and installed_validation.get("returncode") == 0
        )
        activation_validation = (
            installed_validation
            if activation_ready
            else validate_staged_graph_without_recovery_backups(
                staging_repo,
                guru_root,
                result,
                managed_python,
            )
        )
        result["skill_activation_validation"] = activation_validation
        recoverable_activation_ready = (
            managed_backup_recovery_candidate(result)
            and activation_validation.get("returncode") == 0
        )
        if activation_ready or recoverable_activation_ready:
            activate_staged_repository(staging_repo, repo)
            activated_runtime = ensure_managed_python_runtime(repo, guru_root, activate=True)
            if activated_runtime.get("runtime_identity") != python_runtime.get("runtime_identity"):
                raise_managed_runtime_error(str(python_runtime.get("runtime_identity") or "") or None)
        else:
            materialize_staged_conflict_sidecars(staging_repo, repo, result)
        return result


def _install_assets_in_place(
    src: Path,
    dst: Path,
    repo: Path,
    platforms: set[str] | None = None,
    all_platforms: bool = False,
    *,
    source_validation: dict[str, Any],
    upstream_ownership_validation: dict[str, Any],
    managed_python: Path,
) -> dict[str, Any]:
    guru_root = guru_root_from_script()
    previous_manifest = load_previous_installed_manifest(dst)
    dst.mkdir(parents=True, exist_ok=True)

    legacy_removals, legacy_conflicts, legacy_sidecars = remove_legacy_managed_assets(
        repo, dst
    )

    installed: list[str] = []
    unchanged: list[str] = []
    new_copies: list[str] = []
    replaced_overlays: list[str] = []
    updated_managed: list[str] = []
    managed_backups: list[str] = []
    managed_spec_conflicts: list[dict[str, str]] = []
    managed_spec_sidecars: list[str] = []
    managed_asset_hashes: dict[str, str] = {}
    for source_relative, target_relative in MANAGED_SPEC_PATHS:
        result = copy_managed_spec(
            guru_root / source_relative,
            repo / target_relative,
            repo,
            previous_manifest,
        )
        rel_path = Path(result["path"]).relative_to(repo).as_posix()
        if result["action"] == "installed":
            installed.append(rel_path)
            managed_asset_hashes[rel_path] = hashlib.sha256((repo / target_relative).read_bytes()).hexdigest()
        elif result["action"] == "unchanged":
            unchanged.append(rel_path)
            managed_asset_hashes[rel_path] = hashlib.sha256((repo / target_relative).read_bytes()).hexdigest()
        elif result["action"] == "updated_managed":
            updated_managed.append(rel_path)
            managed_asset_hashes[rel_path] = hashlib.sha256((repo / target_relative).read_bytes()).hexdigest()
            backup = result.get("backup")
            if backup:
                managed_backups.append(Path(backup).relative_to(repo).as_posix())
        elif result["action"] == "conflict":
            sidecar = Path(result["sidecar"]).relative_to(repo).as_posix()
            new_copies.append(sidecar)
            managed_spec_sidecars.append(sidecar)
            managed_spec_conflicts.append({
                "path": rel_path,
                "reason": "unknown_local_spec_edit",
                "sidecar": sidecar,
            })
    for relative in MANAGED_ASSET_PATHS:
        result = copy_managed(src / relative, dst / relative)
        rel_path = Path(result["path"]).relative_to(repo).as_posix()
        if result["action"] == "installed":
            installed.append(rel_path)
        elif result["action"] == "unchanged":
            unchanged.append(rel_path)
        elif result["action"] == "updated_managed":
            updated_managed.append(rel_path)
            backup = result.get("backup")
            if backup:
                managed_backups.append(Path(backup).relative_to(repo).as_posix())

    target_config = dst / "config.yml"
    if not target_config.exists():
        shutil.copyfile(src / MANAGED_CONFIG, target_config)
        installed.append(target_config.relative_to(repo).as_posix())

    for script in [
        dst / "scripts/bash/check-env.sh",
        dst / "scripts/bash/version.sh",
        dst / "scripts/bash/prepare-task.sh",
        dst / "scripts/bash/check-workspace-boundary.sh",
        dst / "scripts/bash/check-skill-packages.sh",
        dst / "scripts/bash/discover-skill-contract.sh",
        dst / "scripts/bash/discover-skill-evals.sh",
        dst / "scripts/bash/run-skill-evals.sh",
        dst / "scripts/bash/run-skill-command.sh",
        dst / "scripts/bash/run-package-command.sh",
        dst / "scripts/bash/invoke-stage0-skill.sh",
        dst / "scripts/bash/sync-base.sh",
        dst / "scripts/bash/check-base-sync.sh",
        dst / "scripts/bash/preview-change-context-history.sh",
        dst / "scripts/bash/record-context-discovery.sh",
        dst / "scripts/bash/check-context-discovery.sh",
        dst / "scripts/bash/record-requirements-clarification.sh",
        dst / "scripts/bash/check-requirements-clarification.sh",
        dst / "scripts/bash/record-contract-wording-review.sh",
        dst / "scripts/bash/check-contract-wording-review.sh",
        dst / "scripts/bash/record-change-request-review.sh",
        dst / "scripts/bash/check-change-request-review.sh",
        dst / "scripts/bash/record-task-workspace-plan.sh",
        dst / "scripts/bash/create-task-workspace.sh",
        dst / "scripts/bash/check-task-workspace-result.sh",
        dst / "scripts/bash/resolve-human-artifacts.sh",
        dst / "scripts/bash/record-planning-approval.sh",
        dst / "scripts/bash/check-planning-approval.sh",
        dst / "scripts/bash/record-phase2-check.sh",
        dst / "scripts/bash/check-phase2-check.sh",
        dst / "scripts/bash/record-task-publication-review.sh",
        dst / "scripts/bash/check-task-publication-review.sh",
        dst / "scripts/bash/execute-extension-verification.sh",
        dst / "scripts/bash/record-extension-verification.sh",
        dst / "scripts/bash/check-extension-verification.sh",
        dst / "scripts/bash/invoke-extension-verification.sh",
        dst / "scripts/bash/preview-finalization.sh",
        dst / "scripts/bash/record-finalization-gate.sh",
        dst / "scripts/bash/check-finalization-gate.sh",
        dst / "scripts/bash/execute-finalization-transition.sh",
        dst / "scripts/bash/preview-task-pr-merge.sh",
        dst / "scripts/bash/record-task-pr-merge.sh",
        dst / "scripts/bash/check-task-pr-merge.sh",
        dst / "scripts/bash/execute-task-pr-merge.sh",
        dst / "scripts/bash/invoke-task-pr-merge.sh",
        dst / "scripts/bash/record-agent-recovery.sh",
        dst / "scripts/bash/check-agent-recovery.sh",
        dst / "scripts/bash/prepare-task-commit.sh",
        dst / "scripts/bash/check-commit-messages.sh",
        dst / "scripts/bash/create-task-commit.sh",
        dst / "scripts/bash/format-merge-commit.sh",
        dst / "scripts/bash/review-branch.sh",
        dst / "scripts/bash/check-review-gate.sh",
        dst / "scripts/bash/finish-work.sh",
    ]:
        if script.exists():
            ensure_executable(script)

    selected = platforms or set(DEFAULT_PLATFORMS)
    skill_packages = install_skill_packages(repo, guru_root, dst, selected, previous_manifest)
    skill_packages["conflicts"].extend(managed_spec_conflicts)
    skill_packages["sidecars"] = sorted(set(skill_packages["sidecars"] + managed_spec_sidecars))
    skill_packages["removals"].extend(legacy_removals)
    skill_packages["conflicts"].extend(legacy_conflicts)
    skill_packages["sidecars"] = sorted(set(skill_packages["sidecars"] + legacy_sidecars))
    if skill_packages["conflicts"] or skill_packages["sidecars"]:
        skill_packages["status"] = "conflict"
    overlays = install_overlays(repo, guru_root, selected, previous_manifest)
    installed.extend(overlays["installed"])
    unchanged.extend(overlays["unchanged"])
    new_copies.extend(overlays["new_copies"])
    replaced_overlays.extend(overlays["replaced_overlays"])
    updated_managed.extend(overlays["updated_managed"])
    managed_backups.extend(overlays["managed_backups"])
    agents_principles = ensure_agents_ai_first_principles(repo)
    codex_dispatch = ensure_codex_dispatch_mode(repo)
    session_auto_commit = ensure_session_auto_commit_false(repo)
    runtime_gitignore = ensure_runtime_gitignore(repo)
    workspace_gitignore = ensure_workspace_gitignore(repo)
    language_guidance = normalize_business_doc_language_guidance(repo)

    result = {
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
        "managed_asset_hashes": managed_asset_hashes,
        "agents_principles": agents_principles,
        "codex_dispatch": codex_dispatch,
        "session_auto_commit": session_auto_commit,
        "runtime_gitignore": runtime_gitignore,
        "workspace_gitignore": workspace_gitignore,
        "language_guidance": language_guidance,
        "platforms": sorted(selected),
        "all_platforms": all_platforms,
        "skill_packages": skill_packages,
        "overlays": overlays,
        "skill_source_validation": source_validation,
        "upstream_ownership_validation": upstream_ownership_validation,
    }
    manifest = load_extension_manifest(guru_root)
    source = source_provenance(guru_root)
    installed_manifest = build_installed_extension_manifest(manifest, source, result)
    write_installed_extension_manifest(dst, installed_manifest)
    rel_extension = (dst / "extension.json").relative_to(repo).as_posix()
    result["extension_manifest"] = rel_extension
    result["guru_team_extension"] = extension_summary(manifest, source)
    result["skill_installed_validation"] = run_skill_package_validator(
        repo,
        guru_root,
        "installed",
        managed_python,
    )
    return result


def install_overlays(
    repo: Path,
    guru_root: Path,
    platforms: set[str],
    previous_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    overlay_root = guru_root / "trellis/presets/guru-team/overlays"
    installed: list[str] = []
    unchanged: list[str] = []
    new_copies: list[str] = []
    replaced_overlays: list[str] = []
    updated_managed: list[str] = []
    managed_backups: list[str] = []
    if not overlay_root.is_dir():
        raise SystemExit("Canonical Guru Team overlay root is missing.")

    canonical_sources = sorted(
        path
        for path in overlay_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and "__pycache__" not in path.relative_to(overlay_root).parts
        and path.suffix not in {".pyc", ".pyo"}
    )
    canonical_by_path = {
        source.relative_to(overlay_root).as_posix(): source
        for source in canonical_sources
    }
    expected_paths = {
        path.as_posix() for path in GURU_OVERLAY_ENTRY_PATHS.values()
    }
    if set(canonical_by_path) != expected_paths:
        raise SystemExit(
            "Canonical Guru Team overlay inventory must contain exactly the three Guru finish entries."
        )
    canonical_hashes = {
        relative: hashlib.sha256(source.read_bytes()).hexdigest()
        for relative, source in canonical_by_path.items()
    }
    (
        previous_hashes,
        previous_paths,
        provenance_valid,
        recoverable_sidecars,
    ) = previous_overlay_hashes(previous_manifest, canonical_hashes)

    pending_recovery_sidecars: list[str] = []
    if provenance_valid:
        for sidecar_text in sorted(recoverable_sidecars):
            sidecar = Path(os.path.abspath(repo)) / Path(sidecar_text)
            checked_relative, sidecar_stat, sidecar_error = lstat_repo_path(repo, sidecar)
            if (
                sidecar_error
                or checked_relative.as_posix() != sidecar_text
                or (sidecar_stat is not None and not stat.S_ISREG(sidecar_stat.st_mode))
            ):
                provenance_valid = False
                pending_recovery_sidecars = []
                break
            if sidecar_stat is not None:
                pending_recovery_sidecars.append(sidecar_text)

    records: list[dict[str, Any]] = []
    removals: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    sidecars: list[str] = list(pending_recovery_sidecars)
    managed_backups.extend(pending_recovery_sidecars)
    if not provenance_valid:
        conflicts.append(
            skill_conflict(
                ".trellis/guru-team/extension.json",
                "invalid_previous_overlay_provenance",
            )
        )

    desired_paths = {
        relative
        for relative in canonical_by_path
        if overlay_selected(Path(relative), platforms)
    }
    for relative in sorted(desired_paths):
        source = canonical_by_path[relative]
        relative = source.relative_to(overlay_root)
        target = repo / relative
        result = copy_provenance_managed(
            source,
            target,
            repo,
            previous_hashes,
            provenance_valid,
        )
        rel_path = str(result["path"])
        if result["action"] == "conflict":
            sidecar = result.get("sidecar")
            conflicts.append(
                skill_conflict(
                    rel_path,
                    str(result.get("reason") or "overlay_install_conflict"),
                    sidecar=str(sidecar) if sidecar else None,
                    previous_managed_sha256=result.get("previous_managed_sha256"),
                )
            )
            if sidecar:
                sidecars.append(str(sidecar))
                if str(sidecar).endswith(".new"):
                    new_copies.append(str(sidecar))
            continue

        record = {
            "path": rel_path,
            "source": source.relative_to(guru_root).as_posix(),
            "sha256": result["sha256"],
            "executable": result["executable"],
            "action": result["action"],
        }
        records.append(record)
        if result["action"] == "installed":
            installed.append(rel_path)
        elif result["action"] == "unchanged":
            unchanged.append(rel_path)
        elif result["action"] == "updated_managed":
            updated_managed.append(rel_path)
        if result.get("sidecar"):
            sidecar = str(result["sidecar"])
            sidecars.append(sidecar)
            managed_backups.append(sidecar)

    for stale_path in sorted(previous_paths - desired_paths):
        removal, conflict, sidecar = remove_stale_overlay_path(
            repo,
            stale_path,
            previous_hashes,
            provenance_valid,
            canonical_hashes,
        )
        if removal:
            removals.append(removal)
        if conflict:
            conflicts.append(conflict)
        if sidecar:
            sidecars.append(sidecar)
            new_copies.append(sidecar)

    status = "ok" if provenance_valid and not conflicts and not sidecars else "conflict"
    return {
        "schema_version": GURU_OVERLAY_SCHEMA_VERSION,
        "status": status,
        "selected_platforms": sorted(platforms),
        "files": records,
        "removals": removals,
        "conflicts": conflicts,
        "sidecars": sorted(set(sidecars)),
        "installed": installed,
        "unchanged": unchanged,
        "new_copies": new_copies,
        "replaced_overlays": replaced_overlays,
        "updated_managed": updated_managed,
        "managed_backups": managed_backups,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Guru team Trellis preset")
    parser.add_argument("--repo", help="Target repository root. Defaults to current directory.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true", help="Print the Guru Team extension version from the canonical manifest and exit.")
    platform_group = parser.add_mutually_exclusive_group()
    platform_group.add_argument(
        "--platform",
        action="append",
        choices=ALL_PLATFORMS,
        help="Platform overlay to install. Repeat to select multiple platforms. Defaults to codex + cursor.",
    )
    platform_group.add_argument(
        "--all-platforms",
        action="store_true",
        help="Install every known platform overlay.",
    )
    args = parser.parse_args()

    guru_root = guru_root_from_script()
    if args.version:
        manifest = load_extension_manifest(guru_root)
        print(str(manifest["version"]))
        return 0

    repo = repo_root_from_args(args.repo)
    platforms, all_platforms = selected_platforms(args.platform, args.all_platforms)
    src = guru_root / "trellis/workflows/guru-team"
    dst = repo / ".trellis/guru-team"
    result = install_assets(src, dst, repo, platforms, all_platforms=all_platforms)

    payload: dict[str, Any] = {
        "status": (
            "ok"
            if result["skill_packages"]["status"] == "ok"
            and result["overlays"]["status"] == "ok"
            and result["skill_installed_validation"].get("returncode") == 0
            else "conflict"
        ),
        "repo": str(repo),
        "platforms": result["platforms"],
        "all_platforms": result["all_platforms"],
        "installed": result["installed"],
        "unchanged": result["unchanged"],
        "new_copies": result["new_copies"],
        "replaced_overlays": result["replaced_overlays"],
        "updated_managed": result["updated_managed"],
        "managed_backups": result["managed_backups"],
        "agents_principles": result["agents_principles"],
        "codex_dispatch": result["codex_dispatch"],
        "session_auto_commit": result["session_auto_commit"],
        "runtime_gitignore": result["runtime_gitignore"],
        "workspace_gitignore": result["workspace_gitignore"],
        "language_guidance": result["language_guidance"],
        "extension_manifest": result["extension_manifest"],
        "guru_team_extension": result["guru_team_extension"],
        "skill_packages": result["skill_packages"],
        "overlays": result["overlays"],
        "skill_source_validation": result["skill_source_validation"],
        "upstream_ownership_validation": result["upstream_ownership_validation"],
        "skill_installed_validation": result["skill_installed_validation"],
        "python_runtime": result["python_runtime"],
        "config": ".trellis/guru-team/config.yml",
        "workflow_marketplace": WORKFLOW_MARKETPLACE,
        "public_workflow_marketplace": WORKFLOW_MARKETPLACE,
        "workflow_template": WORKFLOW_TEMPLATE,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if (
        result["skill_packages"]["status"] != "ok"
        or result["overlays"]["status"] != "ok"
        or result["skill_installed_validation"].get("returncode") != 0
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
