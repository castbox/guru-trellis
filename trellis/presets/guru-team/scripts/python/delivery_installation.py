"""Read-only Delivery support diagnosis before any preset or upgrade mutation."""
from __future__ import annotations

import json
import importlib
import importlib.util
import sys
import uuid
import hashlib
import subprocess
from pathlib import Path


def installed_capabilities(common: Path, workflow: Path, records: list[tuple[str, dict]]) -> list[str]:
    """Read actual target modules and the public declaration without file writes."""
    required = {"delivery_schema": ("parse_task_v2",),
                "delivery_operations": ("parse_operation", "apply_operation", "get_gate_applicability"),
                "delivery_store": ("apply_to_store", "candidate_content_ref", "verify_authority", "verify_candidate"),
                "delivery_session": ("get_current_delivery", "select_delivery", "release_delivery", "planning_directory"),
                "runtime_contract": ("read_runtime_contract", "validate_runtime_contract")}
    namespace = "guru_install_delivery_" + uuid.uuid4().hex
    original_bytecode = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location(namespace, common / "__init__.py", submodule_search_locations=[str(common)])
        if spec is None or spec.loader is None:
            return ["common.__init__"]
        module = importlib.util.module_from_spec(spec); sys.modules[namespace] = module; spec.loader.exec_module(module)
        modules = {name: importlib.import_module(namespace + "." + name) for name in required}
        missing = [name + "." + function for name, functions in required.items()
                   for function in functions if not callable(getattr(modules[name], function, None))]
        if missing:
            return missing
        declaration = modules["runtime_contract"].read_runtime_contract(workflow)
        if declaration["delivery_api"] != "1.0" or declaration["task_schema"] != "2.0":
            return ["runtime_contract.delivery_api"]
        for locator, record in records:
            modules["delivery_schema"].parse_task_v2(record)
        return []
    except (ImportError, AttributeError, OSError, ValueError, SyntaxError, RuntimeError) as exc:
        return ["installed_public_api:" + type(exc).__name__]
    finally:
        sys.dont_write_bytecode = original_bytecode
        for name in list(sys.modules):
            if name == namespace or name.startswith(namespace + "."):
                del sys.modules[name]


def retained_migration_records(target: Path) -> dict[str, dict]:
    """Consume only an original Plan2 checkpoint, never infer a legacy phase.

    The backup remains private for rollback and this installation diagnostic;
    these rows grant no task/session/gate authority.
    """
    result = subprocess.run(["git", "rev-parse", "--git-common-dir", "--absolute-git-dir"], cwd=target,
                            text=True, capture_output=True)
    if result.returncode:
        return {}
    receipts = []
    for line in result.stdout.splitlines():
        directory = Path(line)
        if not directory.is_absolute():
            directory = target / directory
        receipts.extend((directory / "guru-team/install-upgrade").glob("*/checkpoint.json"))
    retained = {}
    for path in set(receipts):
        try:
            value = json.loads(path.read_text())
            if value.get("schema_version") != "2.0" or value.get("core_completed") is not True:
                continue
            if value.get("phase") not in ("owners", "guru", "preset", "complete"):
                continue
            plan = value["plan"]["core_plan"]
            if plan["target"]["task_schema"] != "2.0" or plan["target"]["delivery_api"] != "1.0":
                continue
            workspaces = {row["id"]: Path(row["root"]).resolve()
                          for row in plan["workspaces"]}
            for row in plan["tasks"]:
                if workspaces.get(row["workspace"]) != target.resolve() or row["disposition"] not in ("defer", "history_only"):
                    continue
                if row["source"] is None:
                    continue
                ref = row["task_ref"] + "/task.json"
                file = target / ref
                actual = {"sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "mode": file.stat().st_mode & 0o777}
                if actual == {key: row["source"][key] for key in ("sha256", "mode")}:
                    retained[ref] = actual
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return retained


def diagnose_delivery_installation(source: Path, target: Path) -> dict:
    workflow = source / "trellis/workflows/guru-team/workflow.md"
    if "[trellis-runtime-contract]" not in workflow.read_text(encoding="utf-8"):
        return {"status": "not_applicable"}
    required = ("delivery_schema.py", "delivery_operations.py", "delivery_store.py", "delivery_session.py", "runtime_contract.py")
    common = target / ".trellis/scripts/common"
    missing = [".trellis/scripts/common/" + name for name in required if not (common / name).is_file()]
    version_file = target / ".trellis/.version"
    version = version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else None
    legacy, invalid, records = [], [], []
    retained = retained_migration_records(target)
    for path in sorted((target / ".trellis/tasks").glob("**/task.json")):
        locator = path.relative_to(target).as_posix()
        if locator in retained:
            continue  # exact history disposition, never passed to current parser
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            invalid.append(locator)
            continue
        if not isinstance(record, dict):
            invalid.append(locator)
        elif record.get("schema_version") != "2.0":
            legacy.append(locator)
        else:
            records.append((locator, record))
    if legacy:
        return {"status": "blocked", "code": "upstream_delivery_migration_required", "task_refs": legacy,
                "remediation": "Keep the complete pinned existing Guru installation. Run the source-loaded delivery_upgrade with reviewed upstream Plan2 and original-owner private migrations before applying this Delivery candidate."}
    if invalid:
        return {"status": "blocked", "code": "invalid_task_inventory", "task_refs": invalid,
                "remediation": "Resolve the actual Task records with their existing owner before installation."}
    if missing or version != "0.7.0-castbox.3":
        return {"status": "blocked", "code": "unsupported_delivery_api", "installed_core": version, "missing_modules": missing,
                "remediation": "Install the explicitly reviewed Core/CLI Delivery API 1.0 candidate as a complete package before Guru projection. Matching version text alone is not candidate qualification."}
    missing_capabilities = installed_capabilities(common, workflow, records)
    if missing_capabilities:
        return {"status": "blocked", "code": "unsupported_delivery_api", "installed_core": version,
                "missing_capabilities": missing_capabilities,
                "remediation": "Restore the complete reviewed candidate's public Python API and valid Task schema 2 records before any Guru installation writes."}
    return {"status": "supported_candidate", "installed_core": version, "delivery_api": "1.0", "task_schema": "2.0"}


def require_delivery_installation(source: Path, target: Path) -> dict:
    result = diagnose_delivery_installation(source, target)
    if result["status"] == "blocked":
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    return result
