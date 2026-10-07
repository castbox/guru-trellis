"""Explicit legacy installation executor. Semantic decisions are supplied by AI."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from files import MigrationError, business_state, control_token, current_baseline, git, relative_file, restore, run as command, snapshot, state, task_token, write_json
from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.task_lifecycle.identity import task_inventory

TARGET_CORE = "0.7.0-castbox.3"
TARGET_GURU = "0.7.0-guru.3"


def formal_guru_source(source: Path, requested_ref: str) -> None:
    head = git(source, "rev-parse", "HEAD")
    if git(source, "rev-parse", requested_ref + "^{commit}") != head:
        raise MigrationError("The formal Guru source ref does not resolve to HEAD")
    if git(source, "status", "--porcelain=v1", "--untracked-files=all", "--", "trellis"):
        raise MigrationError("Formal Guru canonical source has ordinary uncommitted or untracked changes")
    manifest = json.loads(command(["git", "show", head + ":trellis/guru-team-extension.json"], source))
    if manifest["version"] != TARGET_GURU:
        raise MigrationError("The requested Guru commit does not contain the migration candidate version")
    command(["git", "cat-file", "-e", head + ":trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md"], source)


def source_root(package: Path) -> Path:
    # Migration must come from target source, never bootstrap through old target.
    for parent in package.parents:
        if (parent / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py").is_file():
            return parent
    raise MigrationError("Load this Skill from the complete target canonical source checkout")


def installer(source: Path):
    path = source / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
    spec = importlib.util.spec_from_file_location("migration_preset", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def source_profile(version: str) -> str:
    if re.fullmatch(r"0\.6\.\d+-guru\.\d+", version):
        return "guru0.6-family"
    if re.fullmatch(r"0\.7\.0-guru\.\d+", version):
        return "guru0.7.0-family"
    raise MigrationError("Source is outside the supported Guru 0.6.x / 0.7.0 families")


def old_manifest(root: Path) -> dict:
    value = json.loads(relative_file(root, ".trellis/guru-team/extension.json").read_text(encoding="utf-8"))
    if value.get("schema_version") not in {"1.0", "2.0"}:
        raise MigrationError("Unknown installation manifest schema")
    extension = value.get("extension", {})
    source_profile(extension.get("version", ""))
    core = extension.get("target_trellis_cli", "")
    if not re.fullmatch(r"0\.6\.\d+|0\.7\.0-castbox\.\d+", core):
        raise MigrationError("Missing or unsupported actual installed core contract")
    provenance = value.get("source", {})
    repo = "castbox/guru-trellis"
    # Same bounded GitHub transport identities used by current origin_matches.
    source_repos = {prefix + repo + suffix for prefix in
                    ("https://github.com/", "git@github.com:", "ssh://git@github.com/")
                    for suffix in ("", ".git")}
    if provenance.get("repo") not in source_repos or not provenance.get("commit"):
        raise MigrationError("Missing legacy Guru source provenance")
    return value


def legacy_source_commits(manifest: dict, source: Path) -> list[str]:
    # Early receipts describe the observed working tree, sometimes a release
    # predecessor. Formal tags supply exact canonical bytes, never target hashes.
    candidates = [manifest["source"]["commit"]]
    ref = manifest["source"].get("ref", "")
    if re.fullmatch(r"v0\.(?:6\.\d+|7\.0)-guru\.\d+", ref):
        candidates.append(ref)
    candidates += git(source, "tag", "--list", "v0.6.*-guru.*", "v0.7.0-guru.*").splitlines()
    result = []
    expected = manifest.get("extension", {})
    for candidate in candidates:
        try:
            commit = git(source, "rev-parse", candidate + "^{commit}")
            extension = json.loads(command(["git", "show", commit + ":trellis/guru-team-extension.json"], source))
        except (MigrationError, ValueError):
            continue
        if expected and (extension.get("version") != expected.get("version")
                         or extension.get("target_trellis_cli") != expected.get("target_trellis_cli")):
            continue
        if commit not in result:
            result.append(commit)
    if not result:
        raise MigrationError("Acquire the exact installed release/source objects before preview")
    return result


def legacy_source_paths(path: str) -> list[str]:
    if path.startswith(".trellis/guru-team/"):
        return ["trellis/workflows/guru-team/" + path.removeprefix(".trellis/guru-team/")]
    # Package receipts normally own this mapping. Early installers projected
    # overlay bytes directly, including upstream-owned claims handed to Fork.
    paths = ["trellis/presets/guru-team/overlays/" + path]
    parts = Path(path).parts
    if len(parts) >= 4 and parts[1] == "skills" and parts[2].startswith("guru-"):
        paths.insert(0, "trellis/skills/guru-team/packages/" + "/".join(parts[2:]))
    if path.startswith(".trellis/spec/workflow/"):
        paths.insert(0, "trellis/workflows/guru-team/spec/" + path.removeprefix(".trellis/spec/workflow/"))
    return paths


def old_paths(manifest: dict, source: Path | None = None, root: Path | None = None) -> dict[str, str | None]:
    hashes = dict(manifest["install"].get("managed_asset_hashes", {}))
    for name in ("skill_packages", "overlays"):
        section = manifest.get(name)
        if section is None:
            continue
        if section.get("status") != "ok" or section.get("conflicts") or section.get("sidecars"):
            raise MigrationError("Resolve the old installation's recorded conflicts and sidecars first")
        for row in section["files"]:
            previous = hashes.get(row["path"])
            if previous is not None and previous != row["sha256"]:
                raise MigrationError(f"Conflicting old managed hash: {row['path']}")
            hashes[row["path"]] = row["sha256"]
    missing = set(manifest["install"].get("managed_assets", [])) - set(hashes) - {".trellis/guru-team/extension.json"}
    # No Guru retirement of upstream files: their source ownership belongs to
    # the Fork even when an early Guru receipt claimed them.
    missing = {p for p in missing if guru_owned(p)}
    if missing:
        if source is None:
            raise MigrationError("Read the exact legacy source to resolve missing managed hashes")
        commits = legacy_source_commits(manifest, source)
        for path in sorted(missing):
            candidates = set()
            for commit in commits:
                for source_path in legacy_source_paths(path):
                    original = subprocess.run(["git", "show", commit + ":" + source_path], cwd=source, capture_output=True)
                    if original.returncode == 0:
                        candidates.add(hashlib.sha256(original.stdout).hexdigest())
                        break
            current = state(relative_file(root, path))["sha256"] if root is not None else None
            if current in candidates:
                hashes[path] = current
            elif len(candidates) == 1:
                hashes[path] = next(iter(candidates))
            else:
                # Missing/ambiguous historical bytes never authorize deletion.
                # The AI must explicitly preserve or replace the actual preimage.
                hashes[path] = None
    for path, digest in hashes.items():
        if digest is not None and not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise MigrationError(f"Invalid exact managed hash: {path}")
    return hashes


def guru_owned(path: str) -> bool:
    if path == ".trellis/guru-team/config.yml":
        return False  # Materialized user configuration, never retired asset bytes.
    parts = Path(path).parts
    if len(parts) >= 3 and parts[:2] == (".trellis", "guru-team"):
        return True
    if path.startswith(".trellis/spec/workflow/"):
        return True
    if len(parts) >= 3 and parts[1] == "skills" and parts[2].startswith("guru-"):
        return True
    return path in {".codex/prompts/guru-finish-work.md", ".cursor/commands/guru-finish-work.md", ".claude/commands/guru/finish-work.md"}


def controls(root: Path, plan: dict) -> dict[str, Path]:
    common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    local = Path(git(root, "rev-parse", "--absolute-git-dir"))
    result = {"python_common": common / "guru-team/python/active.json", "python_checkout": local / "guru-team/python/active.json"}
    for row in plan.get("controls", []):
        base = {"common": common, "checkout": local}[row["location"]]
        if not row["path"].startswith(("trellis/", "guru-team/")):
            raise MigrationError("Control restoration is limited to Trellis/Guru Git-private state")
        result[row["location"] + ":" + row["path"]] = relative_file(base, row["path"])
    return result


def core_preview(root: Path, fork: Path, core_plan: dict, installed_core: str) -> dict:
    # Temporary plan remains outside the repository. No target runtime needed.
    from runtime.temporary_lifecycle import temporary_directory
    with temporary_directory("installation_upgrade_core_preview") as directory:
        path = Path(directory) / "core-plan.json"
        write_json(path, core_plan)
        return json.loads(command(["node", str(fork), "migrate", "--from", installed_core, "--plan", str(path), "--dry-run"], root))


def preview(package: Path, root: Path, public: dict, plan: dict | None, fork: Path | None) -> dict:
    source = source_root(package)
    if public["profile"] != "initial_upgrade":
        raise MigrationError("Preview an initial_upgrade; recovery reads its own private checkpoint")
    if git(source, "rev-parse", public["target_source_ref"] + "^{commit}") != git(source, "rev-parse", "HEAD"):
        raise MigrationError("Target source ref does not resolve to this checkout HEAD")
    manifest = old_manifest(root)
    installed_core = (root / ".trellis/.version").read_text().strip()
    if not re.fullmatch(r"0\.6\.\d+|0\.7\.0-castbox\.\d+", installed_core):
        raise MigrationError("Live core is outside the supported predecessor contracts")
    actual_profile = source_profile(manifest["extension"]["version"])
    if public["source_profile"] != actual_profile:
        raise MigrationError("Source family selector differs from actual installed version")
    if manifest["extension"]["version"] == TARGET_GURU:
        raise MigrationError("This target is already installed; use ordinary reapply")
    if actual_profile == "guru0.7.0-family" and int(manifest["extension"]["version"].rsplit(".", 1)[1]) >= int(TARGET_GURU.rsplit(".", 1)[1]):
        raise MigrationError("Upgrade requires a successor target version")
    hashes = old_paths(manifest, source, root)
    rows = []
    for p, expected in sorted(hashes.items()):
        current = state(relative_file(root, p))
        rows.append({"path": p, "previous_sha256": expected, **current,
                     "owner": "guru" if guru_owned(p) else "fork_or_user",
                     "state": "missing" if current["sha256"] is None else "managed" if current["sha256"] == expected else "local_edit"})
    tasks = []
    for path in sorted((root / ".trellis/tasks").glob("*/task.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        tasks.append({"task_ref": path.parent.relative_to(root).as_posix(), "sha256": state(path)["sha256"],
                      "id": record.get("id"), "status": record.get("status"), "fields": sorted(record),
                      "branch": record.get("branch"), "base_branch": record.get("base_branch"),
                      "worktree_path": record.get("worktree_path"), "pr_url": record.get("pr_url")})
    payload = {"status": "preview", "source_profile": actual_profile, "installed_core": installed_core, "installed_version": manifest["extension"]["version"],
               "recorded_core": manifest["extension"]["target_trellis_cli"], "managed": rows, "tasks": tasks,
               "git_status": git(root, "status", "--porcelain=v1", "-z"),
               "worktrees": git(root, "worktree", "list", "--porcelain"),
               "legacy_source": manifest["source"], "selected_platforms": manifest["install"]["selected_platforms"]}
    if plan is not None:
        if fork is None:
            raise MigrationError("Supply the fixed Fork CLI entrypoint for core preview")
        payload["core"] = core_preview(root, fork, plan["core_plan"], installed_core)
        module = installer(source)
        selected = set(plan["selected_platforms"])
        payload["preset_paths"] = sorted(p.as_posix() for p in module.managed_transaction_paths(root, root / ".trellis/guru-team", selected, None))
        projections = module.managed_source_projections(root, root / ".trellis/guru-team", selected)
        payload["preset_inventory"] = [
            {"path": p, **state(relative_file(root, p)),
             "target_sha256": state(projections[Path(p)])["sha256"] if Path(p) in projections else None}
            for p in payload["preset_paths"]
        ]
        payload["sidecars"] = [p + suffix for p in payload["preset_paths"] for suffix in (".new", ".bak")
                               if relative_file(root, p + suffix).exists()]
    return payload


def validate_plan(package: Path, plan: dict) -> None:
    validate_json(plan, package / "schemas/private-plan.schema.json", "plan")


def begin(package: Path, root: Path, public: dict, plan: dict, fork: Path) -> tuple[Path, dict]:
    facts = preview(package, root, public, plan, fork)
    if facts["core"]["conflicts"]:
        raise MigrationError("Core preview has unresolved file decisions")
    if facts["sidecars"]:
        raise MigrationError("Resolve existing managed .new/.bak files before initial migration")
    source = source_root(package)
    if json.loads((source / "trellis/guru-team-extension.json").read_text())["version"] != TARGET_GURU:
        raise MigrationError("Target Guru source does not contain the migration candidate")
    decisions = {x["path"]: x for x in plan["guru_decisions"]}
    if len(decisions) != len(plan["guru_decisions"]):
        raise MigrationError("Duplicate Guru path decision")
    for row in facts["managed"]:
        if row["owner"] != "guru" or row["sha256"] is None:
            continue
        chosen = decisions.get(row["path"])
        if row["state"] == "local_edit" and chosen is None:
            raise MigrationError(f"Review the local managed edit: {row['path']}")
        if chosen is not None and chosen["expected_sha256"] != row["sha256"]:
            raise MigrationError(f"Stale Guru decision: {row['path']}")
    wf = plan["workflow"]
    if wf["provider_ref"] != public["target_source_ref"] or state(root / ".trellis/workflow.md")["sha256"] != wf["expected_sha256"]:
        raise MigrationError("Workflow source or preimage changed; preview again")
    if plan["dependency_mode"] == "source_locked":
        formal_guru_source(source, public["target_source_ref"])
        lock = json.loads((source / "trellis/presets/guru-team/source/trellis-source.json").read_text())
        if lock["cli_version"] != TARGET_CORE:
            raise MigrationError("The formal migration-capable Fork source lock is not available")
        cli_root = fork.parents[3]
        verifier_root = source / "trellis/presets/guru-team/scripts/python"
        sys.path.insert(0, str(verifier_root))
        from verify_trellis_compatibility_matrix import validate_fork_source
        verified = validate_fork_source(source, cli_root)
        if verified["cli_version"] != TARGET_CORE:
            raise MigrationError("Formal fixed Fork source lock is not available")
    paths = set(facts["preset_paths"]) | {x["path"] for x in facts["core"]["actions"]}
    paths |= {x["path"] for x in facts["managed"] if x["owner"] == "guru"}
    paths |= {".trellis/guru-team/extension.json", ".trellis/workflow.md", ".trellis/workflow.md.new", ".trellis/workflow.md.bak"}
    # Preset sidecars are adjacent to its declared managed footprint.
    paths |= {p + suffix for p in list(paths) for suffix in (".new", ".bak")}
    ctrl = controls(root, plan)
    reference = str(uuid.uuid4())
    recovery = Path(git(root, "rev-parse", "--absolute-git-dir")) / "guru-team/install-upgrade" / reference
    checkpoint = {"schema_version": "1.0", "root": str(root), "source": str(source), "source_ref": git(source, "rev-parse", "HEAD"),
                  "fork": str(fork), "plan": plan, "phase": "core", "controls": {k: str(v) for k, v in ctrl.items()},
                  "old_installation": {"core": facts["installed_core"], "guru": facts["installed_version"], "source": facts["legacy_source"]},
                  "old_managed": facts["managed"], "preimages": snapshot(root, recovery, paths, ctrl),
                  "business_before": business_state(root, business_managed_paths(paths, plan))}
    checkpoint["control_before"] = control_token(checkpoint)
    write_json(recovery / "checkpoint.json", checkpoint)
    return recovery, checkpoint


def business_managed_paths(paths: set[str], plan: dict) -> set[str]:
    # Explicit preservation hands ownership to user content. Keep these bytes
    # and modes in the existing fixed business-before comparison on every phase.
    preserved = {row["path"] for row in plan.get("guru_decisions", []) if row["action"] == "preserve"}
    preserved.update(row["path"] for row in plan.get("core_plan", {}).get("file_decisions", [])
                     if row["action"] == "preserve")
    if plan.get("workflow", {}).get("action") == "preserve":
        preserved.add(".trellis/workflow.md")
    return paths - preserved


def save_baseline(root: Path, recovery: Path, checkpoint: dict) -> None:
    checkpoint["baseline"] = current_baseline(root, checkpoint)
    checkpoint["business_after"] = business_state(root, business_managed_paths({k[5:] for k in checkpoint["preimages"] if k.startswith("repo:")}, checkpoint["plan"]))
    write_json(recovery / "checkpoint.json", checkpoint)


def validate_task_dispositions(root: Path, plan: dict) -> None:
    deferred = plan["core_plan"].get("deferred_tasks", [])
    refs = {row["task_ref"] for row in deferred}
    if len(refs) != len(deferred):
        raise MigrationError("Duplicate deferred task disposition")
    for row in deferred:
        if state(relative_file(root, row["task_ref"] + "/task.json"))["sha256"] != row["expected_sha256"]:
            raise MigrationError("Deferred task bytes changed; review its disposition again")
    # Shared current classification diagnoses malformed records and excludes
    # known legacy from lifecycle authority. Only this migration consumes hashes.
    current = {row.task_ref for row in task_inventory(root) if row.lifecycle_state == "active"}
    task_root = root / ".trellis/tasks"
    active = {p.relative_to(root).as_posix() for p in task_root.iterdir()
              if p.name != "archive" and p.is_dir()} if task_root.exists() else set()
    if active - current != refs:
        raise MigrationError("Active legacy task inventory differs from reviewed deferred dispositions")


def preserved_companions(root: Path, module, plan: dict) -> set[str]:
    companion_paths = {".trellis/guru-team/" + p.as_posix() for p in module.MANAGED_ASSET_PATHS}
    return {row["path"] for row in plan["guru_decisions"]
            if row["action"] == "preserve" and row["path"] in companion_paths}


def preserve_customizations(root: Path, source: Path, module, plan: dict) -> None:
    projections = module.managed_source_projections(root, root / ".trellis/guru-team", set(plan["selected_platforms"]))
    for chosen in plan["guru_decisions"]:
        path = Path(chosen["path"])
        if chosen["action"] != "preserve" or path not in projections or chosen["path"] in preserved_companions(root, module, plan):
            continue
        target = relative_file(root, chosen["path"])
        canonical = projections[path]
        if target.exists() and target.read_bytes() != canonical.read_bytes():
            pending = relative_file(root, chosen["path"] + ".new")
            pending.parent.mkdir(parents=True, exist_ok=True)
            pending.write_bytes(canonical.read_bytes())
            raise MigrationError(f"Preserved customization requires reconciliation: {chosen['path']}")


def resume(package: Path, root: Path, recovery: Path, checkpoint: dict) -> dict:
    if checkpoint["root"] != str(root) or checkpoint["source"] != str(source_root(package)):
        raise MigrationError("Recovery belongs to another source or checkout")
    source = source_root(package)
    if git(source, "rev-parse", "HEAD") != checkpoint["source_ref"]:
        raise MigrationError("Recovery source HEAD changed")
    plan = checkpoint["plan"]
    fork = Path(checkpoint["fork"])
    if plan["dependency_mode"] == "source_locked":
        formal_guru_source(source, checkpoint["source_ref"])
    if checkpoint["phase"] == "complete" and (
            current_baseline(root, checkpoint) != checkpoint["baseline"]
            or business_state(root, business_managed_paths({k[5:] for k in checkpoint["preimages"] if k.startswith("repo:")}, checkpoint["plan"])) != checkpoint["business_after"]):
        return {"exit_id": "blocked", "reason": "work_since_completed_migration"}
    try:
        if checkpoint["phase"] != "core":
            validate_task_dispositions(root, plan)
        if checkpoint["phase"] == "core":
            core_path = recovery / "core-plan.json"
            write_json(core_path, plan["core_plan"])
            result = json.loads(command(["node", str(fork), "migrate", "--from", checkpoint["old_installation"]["core"], "--plan", str(core_path)], root))
            if result["status"] != "migrated":
                raise MigrationError("Core migration did not complete")
            checkpoint["task_after_core"] = task_token(root, checkpoint)
            checkpoint["phase"] = "guru"
            save_baseline(root, recovery, checkpoint)
            validate_task_dispositions(root, plan)
        if checkpoint["phase"] == "guru":
            decisions = {x["path"]: x for x in plan["guru_decisions"]}
            for row in checkpoint["old_managed"]:
                if row["owner"] != "guru":
                    continue
                path = relative_file(root, row["path"])
                current = state(path)["sha256"]
                chosen = decisions.get(row["path"])
                if chosen and chosen["action"] == "preserve":
                    continue
                expected = chosen["expected_sha256"] if chosen else row["previous_sha256"]
                if current is None:
                    continue
                if current != expected:
                    raise MigrationError(f"Managed bytes changed: {row['path']}")
                path.unlink()
            # Explicit ownership transition, not a fabricated current manifest.
            relative_file(root, ".trellis/guru-team/extension.json").unlink(missing_ok=True)
            checkpoint["phase"] = "preset"
            save_baseline(root, recovery, checkpoint)
        if checkpoint["phase"] == "preset":
            module = installer(source)
            # File retirement leaves directories outside the preset's staged
            # file inventory. Prune only parents of reviewed retired paths;
            # retained or unknown content makes rmdir stop without deleting it.
            decisions = {x["path"]: x for x in plan["guru_decisions"]}
            for row in sorted(checkpoint["old_managed"], key=lambda row: len(Path(row["path"]).parts), reverse=True):
                if row["owner"] != "guru" or decisions.get(row["path"], {}).get("action") == "preserve":
                    continue
                path = relative_file(root, row["path"])
                if not path.exists():
                    module.prune_empty_managed_skill_parents(root, path)
            wf = plan["workflow"]
            if wf["action"] == "replace":
                pending = relative_file(root, ".trellis/workflow.md.new")
                canonical = source / "trellis/workflows/guru-team/workflow.md"
                current_hash = state(relative_file(root, ".trellis/workflow.md"))["sha256"]
                if current_hash not in {wf["expected_sha256"], state(canonical)["sha256"]}:
                    raise MigrationError("Workflow changed since preview; review its local edits before resume")
                if plan["dependency_mode"] == "source_locked":
                    provider = "gh:castbox/guru-trellis/trellis#" + checkpoint["source_ref"]
                    base = ["node", str(fork), "workflow", "--marketplace", provider, "--template", "guru-team"]
                    command(base + ["--create-new"], root)
                else:
                    # Local isolated rehearsal is a canonical projection, never
                    # remote marketplace or exact-release evidence.
                    pending.write_bytes(canonical.read_bytes())
                if pending.read_bytes() != canonical.read_bytes():
                    raise MigrationError("Marketplace preview differs from reviewed canonical workflow")
                if plan["dependency_mode"] == "source_locked":
                    command(base + ["--force"], root)
                else:
                    relative_file(root, ".trellis/workflow.md").write_bytes(pending.read_bytes())
                pending.unlink(missing_ok=True)
                # Workflow provider backup is preserved in migration preimages.
                relative_file(root, ".trellis/workflow.md.bak").unlink(missing_ok=True)
            preserve_customizations(root, source, module, plan)
            result = module.install_assets(source / "trellis/workflows/guru-team", root / ".trellis/guru-team", root, set(plan["selected_platforms"]),
                                           migration_preserved_paths=preserved_companions(root, module, plan))
            if (result["skill_packages"]["status"] != "ok" or result["overlays"]["status"] != "ok"
                    or result["skill_installed_validation"].get("returncode") != 0):
                raise MigrationError("Current preset has unresolved managed edits or sidecars")
            validate_task_dispositions(root, plan)
        # Validate the activated target, not merely the staged file projection.
        runtime_assets = root / ".trellis/guru-team/runtime"
        live_validation = json.loads(command([
            "env", "PYTHONPATH=" + str(root / ".trellis/guru-team"),
            "bash", str(runtime_assets / "resolve-python.sh"), str(root), str(runtime_assets),
            "-m", "runtime.validate", "--root", str(root), "--mode", "installed", "--json",
        ], root))
        if live_validation.get("status") != "passed":
            raise MigrationError("Actual target installed validation failed; review retained local content")
        if checkpoint["phase"] == "preset":
            checkpoint["phase"] = "complete"
            save_baseline(root, recovery, checkpoint)
        return {"exit_id": "upgraded", "installed_version": TARGET_GURU,
                "recovery_ref": recovery.name, "unverified": [] if plan["dependency_mode"] == "source_locked" else ["formal_fork_source_lock"]}
    except (MigrationError, SystemExit, OSError, ValueError, KeyError) as exc:
        checkpoint["failure"] = {"phase": checkpoint["phase"], "detail": str(exc)[:500]}
        save_baseline(root, recovery, checkpoint)
        return {"exit_id": "resume_required", "profile": "resume", "recovery_ref": recovery.name}


def rollback(root: Path, recovery: Path, checkpoint: dict) -> dict:
    paths = {k[5:] for k in checkpoint["preimages"] if k.startswith("repo:")}
    if "control_before" not in checkpoint or (checkpoint["phase"] != "core" and "task_after_core" not in checkpoint):
        return {"exit_id": "blocked", "reason": "recovery_missing_stable_rollback_anchors"}
    if control_token(checkpoint) != checkpoint["control_before"]:
        return {"exit_id": "blocked", "reason": "control_work_since_migration"}
    if "task_after_core" in checkpoint and task_token(root, checkpoint) != checkpoint["task_after_core"]:
        return {"exit_id": "blocked", "reason": "task_work_since_core_migration"}
    if "baseline" not in checkpoint or current_baseline(root, checkpoint) != checkpoint["baseline"]:
        return {"exit_id": "blocked", "reason": "managed_or_control_work_since_migration"}
    if business_state(root, business_managed_paths(paths, checkpoint["plan"])) != checkpoint["business_after"] or checkpoint["business_after"] != checkpoint["business_before"]:
        return {"exit_id": "blocked", "reason": "business_work_since_migration"}
    restore(root, recovery, checkpoint)
    if current_baseline(root, checkpoint) != {k: {"sha256": v["sha256"], "mode": v["mode"]} for k, v in checkpoint["preimages"].items()}:
        raise MigrationError("Restored bytes or modes do not match the preimage")
    shutil.rmtree(recovery)
    return {"exit_id": "rolled_back", "installed_version": checkpoint["old_installation"]["guru"]}


def run(package_root: Path, metadata: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--plan")
    parser.add_argument("--fork")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    public = read_json(args.input, "input")
    profile = public.get("profile")
    if profile not in ("initial_upgrade", "resume", "rollback"):
        raise CommandError("schema_mismatch", "input.profile", "Use a declared upgrade input profile")
    validate_json(public, package_root / f"schemas/public-{profile}-input.schema.json", "input")
    plan = read_json(args.plan, "plan") if args.plan else None
    if plan is not None:
        validate_plan(package_root, plan)
    fork = Path(args.fork).resolve() if args.fork else None
    try:
        if metadata["runtime_role"] == "preview":
            return preview(package_root, root, public, plan, fork)
        if profile == "initial_upgrade":
            if plan is None or fork is None:
                raise MigrationError("Initial execution requires the reviewed private plan and fixed Fork CLI")
            recovery, checkpoint = begin(package_root, root, public, plan, fork)
            result = resume(package_root, root, recovery, checkpoint)
        else:
            recovery = Path(git(root, "rev-parse", "--absolute-git-dir")) / "guru-team/install-upgrade" / public["recovery_ref"]
            checkpoint = json.loads((recovery / "checkpoint.json").read_text())
            validate_json(checkpoint, package_root / "schemas/private-recovery.schema.json", "recovery")
            if checkpoint["root"] != str(root):
                raise MigrationError("Recovery checkout mismatch")
            result = rollback(root, recovery, checkpoint) if profile == "rollback" else resume(package_root, root, recovery, checkpoint)
        validate_json(result, package_root / f"schemas/public-{result['exit_id']}-output.schema.json", "output")
        return result
    except MigrationError as exc:
        return {"exit_id": "blocked", "reason": str(exc)}
    except (OSError, ValueError, KeyError):
        return {"exit_id": "blocked", "reason": "refresh_inventory_or_recovery_facts"}
