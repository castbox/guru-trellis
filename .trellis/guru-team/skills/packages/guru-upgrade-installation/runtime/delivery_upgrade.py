"""Plan2 installation executor and bounded private recovery.

Semantic projections are supplied by their owners. Public migration writes and
the entire occupied inventory are validated/executed only by installed upstream.
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import sys
import uuid
from pathlib import Path

from files import MigrationError, git, relative_file, state, write_json, business_state
from delivery_upstream import call, packages


OWNER_MIGRATIONS = {
    "guru-create-task-commit": ("migrate-task-commit-planning-source", "migrate-delivery-source.sh",
                               {"delivery_source_migration"}, {"source_bound", "direct_committed"}),
    "guru-publish-task-delivery": ("migrate-task-delivery-publication", "migrate-delivery-transaction.sh",
                                  {"historical_publication_migration", "inflight_publication_migration"}, {"transaction_bound", "already_bound"}),
    "guru-merge-task-delivery": ("migrate-task-delivery-merge", "migrate-delivery-transaction.sh",
                               {"historical_merge_migration"}, {"historical_delivery_recorded", "fresh_merge_review_required"}),
}

OWNER_SCHEMAS = {
    "guru-create-task-commit": ("delivery-source-migration-input-1.0.schema.json", "delivery-commit-review-1.0.schema.json"),
    "guru-publish-task-delivery": ("private-delivery-migration-input-1.0.schema.json", "private-delivery-migration-review-1.0.schema.json"),
    "guru-merge-task-delivery": ("private-delivery-migration-input-1.0.schema.json", "private-delivery-migration-review-1.0.schema.json"),
}


def inventory(directory: Path) -> dict:
    return {p.relative_to(directory).as_posix(): state(p) for p in sorted(directory.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def freeze_source(source: Path) -> dict:
    return {"head": git(source, "rev-parse", "HEAD"), "files": inventory(source / "trellis")}


def freeze_fork(fork: Path) -> dict:
    cli, core = packages(fork)
    return {"cli": inventory(cli), "core": inventory(core)}


def verify_sources(source: Path, fork: Path, plan: dict) -> None:
    if freeze_source(source) != plan["source_candidate"]:
        raise MigrationError("Guru frozen candidate bytes, modes or HEAD changed; retain the same recovery plan")
    if freeze_fork(fork) != plan["fork_candidate"]:
        raise MigrationError("Installed CLI/Core frozen candidate bytes or modes changed")
    if plan["dependency_mode"] == "source_locked":
        from owner import formal_guru_source
        formal_guru_source(source, plan["source_candidate"]["head"])
        lock = json.loads((source / "trellis/presets/guru-team/source/trellis-source.json").read_text())
        cli, core = packages(fork)
        if lock.get("cli_version") != "0.7.0-castbox.4":
            raise MigrationError("Formal source lock does not select the Delivery candidate")
        # Formal source mode cannot claim a dirty local tar or installed tree.
        # The installation must come from the lock's exact package integrity.
        checkout = plan.get("fork_source_root")
        if not checkout:
            raise MigrationError("Formal source mode requires the exact source-locked Fork checkout")
        import sys
        sys.path.insert(0, str(source / "trellis/presets/guru-team/scripts/python"))
        from verify_trellis_compatibility_matrix import validate_fork_source
        validate_fork_source(source, Path(checkout))
        for installed, name in ((cli, "cli"), (core, "core")):
            built = Path(checkout) / "packages" / name / "dist"
            if inventory(built) != inventory(installed / "dist"):
                raise MigrationError("Installed packages differ from the exact source-locked Fork build")


def roots(plan: dict) -> dict[str, Path]:
    # Plan2 root is already the project root; project_relative only locates
    # that project beneath its registered Git worktree top.
    return {row["id"]: Path(row["root"]).resolve()
            for row in plan["core_plan"]["workspaces"]}


def raw_snapshot(path: Path) -> dict | None:
    facts = state(path)
    if facts["sha256"] is None:
        return None
    return {"content_base64": base64.b64encode(path.read_bytes()).decode("ascii"), **facts}


def prepare_inventory(root: Path, fork: Path | None) -> dict:
    """Read original facts only; the owner chooses Plan2 dispositions.

    This is a call-local preview, not a second Task/copy model. Public Plan2
    validates the complete registrations, identities, groups and bindings.
    """
    import subprocess
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                           text=True, capture_output=True)
    common = None
    registrations = ""
    suffix = None
    targets = [root]
    if probe.returncode == 0:
        top = Path(probe.stdout.strip()).resolve()
        suffix = root.relative_to(top).as_posix() if root != top else None
        common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        registrations = git(root, "worktree", "list", "--porcelain", "-z")
        targets = []
        for record in registrations.split("\0\0"):
            fields = record.split("\0")
            if not fields[0].startswith("worktree "):
                continue
            registered = Path(fields[0][9:])
            prunable = any(field == "prunable" or field.startswith("prunable ") for field in fields[1:])
            if registered != top and prunable and not os.path.lexists(registered / ".git"):
                continue
            target = registered.resolve(strict=True) / (suffix or "")
            if (target / ".trellis").exists():
                targets.append(target)
    else:
        # Match the public Git-free boundary; a damaged Git checkout is not it.
        if "not a git repository" not in probe.stderr or any(os.path.lexists(p / ".git") for p in (root, *root.parents)):
            raise MigrationError("Registered checkout inventory is unavailable; reenter checkout resolution")
    bindings = {}
    workspaces = []
    for target in sorted(targets):
        task_root = target / ".trellis/tasks"
        tasks = []
        directories = [p for p in task_root.iterdir() if p.is_dir() and p.name != "archive"] if task_root.exists() else []
        archive = task_root / "archive"
        if archive.exists():
            for p in archive.iterdir():
                if p.is_dir():
                    directories.extend([p] if (p / "task.json").exists() else [child for child in p.iterdir() if child.is_dir()])
        for directory in sorted(directories):
            path = directory / "task.json"
            ref = directory.relative_to(target).as_posix()
            original = raw_snapshot(path)
            tasks.append({"task_ref": ref, "source": original,
                          "artifacts": {p.relative_to(target).as_posix(): raw_snapshot(p)
                                        for p in sorted(directory.rglob("*")) if p.is_file() and p != path}})
            if common is not None and original is not None and not ref.startswith(".trellis/tasks/archive/"):
                metadata = json.loads(base64.b64decode(original["content_base64"]))
                task_id = metadata["id"]
                generation = metadata.get("lifecycle_generation", 0)
                binding_path = relative_file(common, f"trellis/task-branches/{task_id}/{generation}.json")
                binding = raw_snapshot(binding_path)
                if binding is not None:
                    bindings[(task_id, generation)] = {"task_id": task_id, "lifecycle_generation": generation, "source": binding}
        row = {"root": str(target), "project_relative": suffix, "tasks": tasks,
               "branch_name": None if common is None else git(target, "branch", "--show-current"),
               "version_source": raw_snapshot(target / ".trellis/.version"),
               "receipt_source": raw_snapshot(target / ".trellis/.template-hashes.json"),
               "workflow_source": raw_snapshot(target / ".trellis/workflow.md"),
               "guru_source": raw_snapshot(target / ".trellis/guru-team/extension.json"),
               "local_sessions": {p.name: raw_snapshot(p) for p in sorted((target / ".trellis/.runtime/sessions").glob("*.json"))}}
        if fork is not None:
            row["prospective_templates"] = call(target, fork, "templates")
        workspaces.append(row)
    return {"registrations": registrations, "workspaces": workspaces,
            "branch_bindings": list(bindings.values()),
            "common_sessions": {} if common is None else {p.name: raw_snapshot(p) for p in sorted((common / "trellis/sessions").glob("*.json"))}}


def old_installation(root: Path, source: Path | None = None) -> dict:
    from owner import old_manifest, source_profile
    manifest = old_manifest(root, source)
    version = (root / ".trellis/.version").read_text().strip()
    if not version.startswith(("0.6.", "0.7.0-castbox.")):
        raise MigrationError("Unsupported live Core source contract")
    return {"core": version, "guru": manifest["extension"]["version"],
            "profile": source_profile(manifest["extension"]["version"]), "manifest": manifest}


def preview(package: Path, root: Path, public: dict, plan: dict | None, fork: Path | None) -> dict:
    from owner import source_root, installer, old_paths, guru_owned
    source = source_root(package)
    old = old_installation(root, source)
    if public["source_profile"] != old["profile"]:
        raise MigrationError("Source family differs from actual installed Guru")
    if public["target_source_ref"] != git(source, "rev-parse", "HEAD"):
        raise MigrationError("Target source ref must name the current exact Guru HEAD")
    result = {"status": "preview", "installed_core": old["core"], "installed_version": old["guru"],
              "source_candidate": freeze_source(source)}
    if plan is None:
        result["inventory"] = prepare_inventory(root, fork)
        result["worktrees"] = result["inventory"]["registrations"]
    if fork is not None:
        result["fork_candidate"] = freeze_fork(fork)
        result["prospective_templates"] = (next(row for row in result["inventory"]["workspaces"] if row["root"] == str(root))["prospective_templates"]
                                           if plan is None else call(root, fork, "templates"))
    if plan is None:
        return result
    if fork is None:
        raise MigrationError("Plan2 preview requires the reviewed installed CLI/Core")
    if plan["core_plan"]["schema_version"] != "2.0":
        raise MigrationError("delivery_upgrade requires upstream Plan2, not historical Plan1")
    verify_sources(source, fork, plan)
    if root not in roots(plan).values():
        raise MigrationError("The target checkout is absent from Plan2 workspaces")
    result["core"] = call(root, fork, "preview", plan["core_plan"])
    if result["core"]["conflicts"]:
        raise MigrationError("Plan2 preview has stale preimages or unresolved decisions")
    module = installer(source)
    workspace_rows = {row["workspace"]: row for row in plan["guru_workspaces"]}
    if set(workspace_rows) != set(roots(plan)):
        raise MigrationError("Every Plan2 workspace requires its Guru installation disposition")
    target_paths = {str(Path(row["path"]).resolve()) for row in result["core"]["actions"]}
    managed = {}
    for workspace, target in roots(plan).items():
        selected = workspace_rows[workspace]
        previous = old_installation(target, source)
        hashes = old_paths(previous["manifest"], source, target)
        decisions = {row["path"]: row for row in selected["decisions"]}
        if len(decisions) != len(selected["decisions"]):
            raise MigrationError("Duplicate Guru managed decision")
        rows = []
        for path, digest in hashes.items():
            if not guru_owned(path):
                continue
            current = state(relative_file(target, path))
            decision = decisions.get(path)
            if current["sha256"] is not None and current["sha256"] != digest and decision is None:
                raise MigrationError("Review the current locally modified Guru asset: " + path)
            if decision and decision["expected_sha256"] != current["sha256"]:
                raise MigrationError("Guru asset decision became stale: " + path)
            rows.append({"path": path, "previous_sha256": digest, **current})
            target_paths.add(str(relative_file(target, path)))
        paths = module.managed_transaction_paths(target, target / ".trellis/guru-team",
                                                 set(selected["selected_platforms"]), previous["manifest"])
        target_paths.update(str(target / path) for path in paths)
        managed[workspace] = rows
    # The semantic owner supplies the bounded prospective private write set.
    # Its actual read-only preview is checked after Core creates the projection.
    for item in plan["owner_migrations"]:
        owner = OWNER_MIGRATIONS.get(item["skill_id"])
        if not owner or item["command_id"] != owner[0] or item["input"].get("profile") not in owner[2]:
            raise MigrationError("Use a declared original-owner private migration profile")
        if item["workspace"] not in roots(plan):
            raise MigrationError("Private migration workspace is absent from the reviewed plan")
        target = roots(plan)[item["workspace"]]
        # Private assets belong only to a projected Task. The public executor
        # has already judged group legality; a deferred peer is preserve-only.
        owner_input = item["input"]
        selected = owner_input.get("current_input", owner_input)
        task_ref = selected.get("task_ref")
        key = selected.get("delivery_key", {})
        projected = [row for row in plan["core_plan"]["tasks"]
                     if row["workspace"] == item["workspace"]
                     and row["disposition"] in {"convert_active", "convert_archive", "current"}]
        if task_ref is not None:
            belongs = any(row["task_ref"] == task_ref for row in projected)
        else:
            records = [row.get("record") or json.loads(base64.b64decode(row["source"]["content_base64"])) for row in projected]
            belongs = any(record["id"] == key.get("task_id") and record.get("lifecycle_generation", 0) == key.get("lifecycle_generation")
                          for record in records)
        if not belongs:
            raise MigrationError("Private migration requires the projected Task, never a deferred/history-only peer")
        from runtime.schema import validate_json
        owner_package = package.parent / item["skill_id"]
        schemas = OWNER_SCHEMAS[item["skill_id"]]
        validate_json(item["input"], owner_package / "schemas" / schemas[0], "owner_migration.input")
        review_path = Path(item["owner_result"])
        if not review_path.is_absolute():
            review_path = target / review_path
        review = json.loads(review_path.read_text())
        validate_json(review, owner_package / "schemas" / schemas[1], "owner_migration.owner_result")
        if review["status"] != "passed":
            raise MigrationError("Original private migration owner must review this exact conversion before writes")
        for path in item["paths"]:
            target_paths.add(str(relative_file(target, path)))
    for item in plan["controls"]:
        target = roots(plan)[item["workspace"]]
        directory = Path(git(target, "rev-parse", "--git-common-dir" if item["location"] == "common" else "--absolute-git-dir"))
        if not directory.is_absolute():
            directory = target / directory
        if not item["path"].startswith(("trellis/", "guru-team/")):
            raise MigrationError("Controls must be original Trellis/Guru private paths")
        target_paths.add(str(relative_file(directory, item["path"])))
    from runtime.bootstrap import active_pointer_path
    for target in roots(plan).values():
        target_paths.add(str(active_pointer_path(target, for_write=True)))
        for argument in ("--git-common-dir", "--absolute-git-dir"):
            directory = Path(git(target, "rev-parse", argument))
            if not directory.is_absolute():
                directory = target / directory
            target_paths.add(str(directory / "guru-team/python/active.json"))
    target_paths |= {path + suffix for path in list(target_paths) for suffix in (".new", ".bak")}
    if any(Path(path).exists() for path in target_paths if path.endswith((".new", ".bak"))):
        raise MigrationError("Resolve existing managed sidecars before the initial migration")
    result.update(target_paths=sorted(target_paths), old_managed=managed)
    return result


def current(checkpoint: dict) -> dict:
    return {path: state(Path(path)) for path in checkpoint["preimages"]}


def business(checkpoint: dict) -> dict:
    result = {}
    for workspace, target in roots(checkpoint["plan"]).items():
        paths = {str(Path(path).relative_to(target)) for path in checkpoint["preimages"]
                 if Path(path).is_relative_to(target)}
        preserved = {row["path"] for row in next(row for row in checkpoint["plan"]["guru_workspaces"]
                                                 if row["workspace"] == workspace)["decisions"]
                     if row["action"] == "preserve"}
        result[workspace] = business_state(target, paths - preserved)
        # Original helper's historical exclusions are inappropriate for Plan2:
        # archives, journals and newly occupied roots are part of this rollback.
        extra = {}
        for directory in (target / ".trellis/tasks", target / ".trellis/workspace", target / ".trellis/.runtime/sessions"):
            if directory.exists():
                extra.update({str(p): state(p) for p in directory.rglob("*") if p.is_file() and str(p) not in checkpoint["preimages"]})
        common = Path(git(target, "rev-parse", "--git-common-dir"))
        if not common.is_absolute():
            common = target / common
        common = common.resolve()
        sessions = common / "trellis/sessions"
        if sessions.exists():
            extra.update({str(p): state(p) for p in sessions.rglob("*") if p.is_file() and str(p) not in checkpoint["preimages"]})
        # Core preserves Git routing. Bind it once with the original business
        # snapshot so post-Core resume/rollback cannot skip its freshness check.
        # Lock/prunable descriptions do not change checkout routing.
        registrations = sorted(
            [field for field in record.split("\0")
             if field.startswith(("worktree ", "branch ")) or field in {"detached", "bare"}]
            for record in git(target, "worktree", "list", "--porcelain", "-z").split("\0\0")
            if record.startswith("worktree ")
        )
        result[workspace] = {"git_business": result[workspace], "historical_and_session_files": extra,
                             "git_routing": {"branch": git(target, "branch", "--show-current"),
                                             "registrations": registrations}}
    return result


def save(recovery: Path, checkpoint: dict) -> None:
    checkpoint["baseline"] = current(checkpoint)
    write_json(recovery / "checkpoint.json", checkpoint)


def begin(package: Path, root: Path, public: dict, plan: dict, fork: Path) -> tuple[Path, dict]:
    from owner import source_root
    source = source_root(package)
    facts = preview(package, root, public, plan, fork)
    recovery = Path(git(root, "rev-parse", "--absolute-git-dir")) / "guru-team/install-upgrade" / str(uuid.uuid4())
    checkpoint = {"schema_version": "2.0", "root": str(root), "source": str(source),
                  "fork": str(fork), "plan": plan, "phase": "core", "core_completed": False,
                  "owner_index": 0, "preset_index": 0, "old_managed": facts["old_managed"],
                  "old_installation": old_installation(root, source), "preimages": {}}
    for index, path in enumerate(facts["target_paths"]):
        row = state(Path(path))
        row["backup"] = "preimages/" + str(index)
        if row["sha256"] is not None:
            backup = recovery / row["backup"]
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(Path(path).read_bytes())
        checkpoint["preimages"][path] = row
    checkpoint["business_before"] = business(checkpoint)
    save(recovery, checkpoint)
    return recovery, checkpoint


def owners(package: Path, recovery: Path, checkpoint: dict) -> None:
    for index, item in enumerate(checkpoint["plan"]["owner_migrations"]):
        if index < checkpoint["owner_index"]:
            continue
        target = roots(checkpoint["plan"])[item["workspace"]]
        # These original-owner migration commands are intermediate receipts;
        # they do not claim a new workflow exit or current gate.
        owner = OWNER_MIGRATIONS[item["skill_id"]]
        owner_package = package.parent / item["skill_id"]
        commands = json.loads((owner_package / "commands.json").read_text())["commands"]
        if not any(row["id"] == item["command_id"] for row in commands):
            raise MigrationError("Original-owner migration command is not registered")
        wrapper = owner_package / "scripts" / owner[1]
        import subprocess
        input_file = recovery / "owner-input.json"
        write_json(input_file, item["input"])
        argv = ["bash", str(wrapper), "--root", str(target), "--input", str(input_file), "--owner-result", item["owner_result"]]
        def invoke(extra: list[str]) -> dict:
            result = subprocess.run(argv + extra, cwd=target, text=True, capture_output=True)
            if result.returncode:
                try:
                    error_code = json.loads(result.stdout).get("code", "owner_command_failed")
                except (ValueError, AttributeError):
                    error_code = "owner_command_failed"
                raise MigrationError("Original private migration owner " + item["skill_id"] + ": " + str(error_code))
            return json.loads(result.stdout).get("result", {})

        try:
            prospective = invoke(["--preview"])
            if (item["skill_id"] == "guru-merge-task-delivery"
                    and prospective.get("status") == "fresh_merge_review_required"):
                # No historical write applies. The original Merge owner still
                # requires its fresh current review; Upgrade creates no pass.
                checkpoint["owner_index"] = index + 1
                continue
            paths = prospective.get("write_paths")
            if prospective.get("status") != "preview" or not isinstance(paths, list):
                raise MigrationError("Original private migration owner requires reentry: " + item["skill_id"])
            for path in paths:
                absolute = str(relative_file(target, path))
                if path not in item["paths"] or absolute not in checkpoint["preimages"]:
                    raise MigrationError("Original private migration write lacks its frozen initial backup: " + item["skill_id"])
            value = invoke([])
        finally:
            input_file.unlink(missing_ok=True)
        if value.get("status") not in owner[3]:
            raise MigrationError("Original private migration owner requires reentry: " + item["skill_id"])
        checkpoint["owner_index"] = index + 1


def resume(package: Path, root: Path, recovery: Path, checkpoint: dict, plan: dict | None = None) -> dict:
    from owner import source_root, installer, preserve_customizations, preserved_companions
    source = source_root(package)
    if checkpoint["root"] != str(root) or checkpoint["source"] != str(source):
        raise MigrationError("Recovery belongs to a different source/target checkout")
    if plan is not None and plan != checkpoint["plan"]:
        raise MigrationError("Plan2 resume requires the same frozen plan; no refreshed rollback anchors")
    plan = checkpoint["plan"]
    verify_sources(source, Path(checkpoint["fork"]), plan)
    if current(checkpoint) != checkpoint["baseline"] or business(checkpoint) != checkpoint["business_before"]:
        raise MigrationError("Ordinary work changed since the migration pause; preserve it and reenter the original owner")
    if checkpoint["phase"] == "complete":
        return upgraded(checkpoint, recovery)
    try:
        if checkpoint["phase"] == "core":
            result = call(root, Path(checkpoint["fork"]), "migrate", plan["core_plan"])
            if result["status"] != "migrated":
                raise MigrationError("Actual upstream Plan2 did not finish")
            checkpoint["core_completed"] = True
            checkpoint["phase"] = "owners"
            save(recovery, checkpoint)
        if checkpoint["phase"] == "owners":
            owners(package, recovery, checkpoint)
            checkpoint["phase"] = "guru"
            save(recovery, checkpoint)
        module = installer(source)
        if checkpoint["phase"] == "guru":
            for workspace, target in roots(plan).items():
                selected = next(row for row in plan["guru_workspaces"] if row["workspace"] == workspace)
                decisions = {row["path"]: row for row in selected["decisions"]}
                for row in checkpoint["old_managed"][workspace]:
                    chosen = decisions.get(row["path"])
                    if chosen and chosen["action"] == "preserve":
                        continue
                    path = relative_file(target, row["path"])
                    expected = chosen["expected_sha256"] if chosen else row["previous_sha256"]
                    if state(path)["sha256"] not in (None, expected):
                        raise MigrationError("Old Guru asset changed during migration")
                    path.unlink(missing_ok=True)
                    module.prune_empty_managed_skill_parents(target, path)
                (target / ".trellis/guru-team/extension.json").unlink(missing_ok=True)
            checkpoint["phase"] = "preset"
            save(recovery, checkpoint)
        if checkpoint["phase"] == "preset":
            for index, (workspace, target) in enumerate(roots(plan).items()):
                if index < checkpoint["preset_index"]:
                    continue
                selected = next(row for row in plan["guru_workspaces"] if row["workspace"] == workspace)
                adapter = {"selected_platforms": selected["selected_platforms"], "guru_decisions": selected["decisions"]}
                preserve_customizations(target, source, module, adapter)
                result = module.install_assets(source / "trellis/workflows/guru-team", target / ".trellis/guru-team",
                                               target, set(selected["selected_platforms"]),
                                               migration_preserved_paths=preserved_companions(target, module, adapter), python=sys.executable)
                if (result["skill_packages"]["status"] != "ok" or result["overlays"]["status"] != "ok"
                        or result["skill_installed_validation"].get("returncode") != 0):
                    raise MigrationError("Current preset has unresolved managed edits or sidecars")
                checkpoint["preset_index"] = index + 1
                save(recovery, checkpoint)
            from files import run
            for target in roots(plan).values():
                assets = target / ".trellis/guru-team/runtime"
                value = json.loads(run(["env", "PYTHONPATH=" + str(target / ".trellis/guru-team"), "bash",
                                        str(assets / "resolve-python.sh"), str(target), str(assets),
                                        "-m", "runtime.validate", "--root", str(target), "--mode", "installed", "--json"], target))
                if value.get("status") != "passed":
                    raise MigrationError("Actual activated target failed installed validation")
            checkpoint["phase"] = "complete"
            save(recovery, checkpoint)
        return upgraded(checkpoint, recovery)
    except (MigrationError, SystemExit, OSError, ValueError, KeyError) as exc:
        checkpoint["failure"] = {"phase": checkpoint["phase"], "detail": str(exc) if isinstance(exc, MigrationError) else type(exc).__name__}
        save(recovery, checkpoint)
        return {"exit_id": "delivery_resume_required", "profile": "delivery_resume", "recovery_ref": recovery.name}


def upgraded(checkpoint: dict, recovery: Path) -> dict:
    from owner import TARGET_GURU
    return {"exit_id": "upgraded", "installed_version": TARGET_GURU, "recovery_ref": recovery.name,
            "unverified": [] if checkpoint["plan"]["dependency_mode"] == "source_locked" else ["formal_fork_source_lock"]}


def rollback(root: Path, recovery: Path, checkpoint: dict) -> dict:
    if checkpoint["root"] != str(root):
        raise MigrationError("Rollback checkout mismatch")
    if current(checkpoint) != checkpoint["baseline"] or business(checkpoint) != checkpoint["business_before"]:
        return {"exit_id": "blocked", "reason": "work_since_delivery_migration"}
    for path, row in checkpoint["preimages"].items():
        target = Path(path)
        if row["sha256"] is None:
            target.unlink(missing_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((recovery / row["backup"]).read_bytes())
            os.chmod(target, row["mode"])
    if current(checkpoint) != {path: {key: row[key] for key in ("sha256", "mode")}
                               for path, row in checkpoint["preimages"].items()}:
        raise MigrationError("Plan2 rollback bytes/modes differ from their original preimages")
    version = checkpoint["old_installation"]["guru"]
    shutil.rmtree(recovery)
    return {"exit_id": "rolled_back", "installed_version": version}
