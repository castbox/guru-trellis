from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

PLATFORM_ROOTS = {
    "shared": Path(".agents/skills"),
    "codex": Path(".codex/skills"),
    "cursor": Path(".cursor/skills"),
    "claude": Path(".claude/skills"),
}
OVERLAY_PATHS = {
    "codex": Path(".codex/prompts/guru-finish-work.md"),
    "cursor": Path(".cursor/commands/guru-finish-work.md"),
    "claude": Path(".claude/commands/guru/finish-work.md"),
}
PRIVATE_PROJECTION_ROOTS = {"runtime", "tests", "errors"}
SIDECAR_SUFFIXES = (".new", ".bak")
MARKER_PATTERNS = {
    "invoke": re.compile(r"^\s*<!--\s*guru-skill-invoke:\s*(\{.*\})\s*-->\s*$"),
    "exit": re.compile(r"^\s*<!--\s*guru-skill-exit:\s*(\{.*\})\s*-->\s*$"),
    "target": re.compile(r"^\s*<!--\s*guru-(workflow|stop)-target:\s*(\{.*\})\s*-->\s*$"),
}


def safe_relative(value: Any) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/") or "//" in value:
        return None
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path


def lexical_relative(root: Path, path: Path) -> Path | None:
    try:
        return Path(os.path.abspath(path)).relative_to(Path(os.path.abspath(root)))
    except ValueError:
        return None


def lstat_path(root: Path, path: Path, label: str, errors: list[str], *, kind: str, required: bool = True):
    root = Path(os.path.abspath(root))
    path = Path(os.path.abspath(path))
    relative = lexical_relative(root, path)
    if relative is None:
        errors.append(f"{label} is outside the repository")
        return None
    current = root
    try:
        root_stat = root.lstat()
    except OSError:
        errors.append(f"{label} repository boundary is unreadable")
        return None
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        errors.append(f"{label} has a symlink component")
        return None
    for part in relative.parts:
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            if required:
                errors.append(f"{label} is missing")
            return None
        except OSError:
            errors.append(f"{label} is unreadable")
            return None
        if stat.S_ISLNK(current_stat.st_mode):
            errors.append(f"{label} has a symlink component")
            return None
    if kind == "file" and not stat.S_ISREG(current_stat.st_mode):
        errors.append(f"{label} is not a regular file")
        return None
    if kind == "directory" and not stat.S_ISDIR(current_stat.st_mode):
        errors.append(f"{label} is not a directory")
        return None
    return current_stat


def read_json(root: Path, path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    if lstat_path(root, path, label, errors, kind="file") is None:
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append(f"{label} is invalid JSON")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} JSON root is not an object")
        return None
    return value


def collect_files(root: Path, tree: Path, label: str, errors: list[str]) -> list[Path]:
    if lstat_path(root, tree, label, errors, kind="directory") is None:
        return []
    files: list[Path] = []
    for directory, names, filenames in os.walk(tree, followlinks=False):
        parent = Path(directory)
        for name in list(names):
            path = parent / name
            if lstat_path(root, path, label, errors, kind="directory") is None:
                names.remove(name)
        for name in filenames:
            path = parent / name
            if "__pycache__" in path.relative_to(tree).parts or path.suffix in {".pyc", ".pyo"}:
                continue
            if lstat_path(root, path, label, errors, kind="file") is not None:
                files.append(path)
    return sorted(files)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_files(package: Path, interface: dict[str, Any], files: list[Path]) -> list[Path]:
    private_paths = {
        str(item.get("schema", {}).get("path"))
        for item in interface.get("public_contracts", {}).get("private_artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("schema"), dict)
    }
    output_examples = {
        str(item.get("example", {}).get("path"))
        for item in interface.get("public_contracts", {}).get("outputs", [])
        if isinstance(item, dict) and isinstance(item.get("example"), dict)
    }
    private_artifacts = {
        str(item.get("path")) for item in interface.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str) and str(item.get("path")) not in output_examples
    }
    wrapper = str(interface.get("public_contracts", {}).get("invocation", {}).get("wrapper", ""))
    result = []
    for path in files:
        inner = path.relative_to(package)
        text = inner.as_posix()
        if inner.parts[0] in PRIVATE_PROJECTION_ROOTS or text in private_paths or text in private_artifacts:
            continue
        if inner.parts[0] == "scripts" and text != wrapper:
            continue
        result.append(path)
    return result


def workflow_facts(root: Path, workflow: Path, active: dict[str, dict[str, Any]], required: bool, errors: list[str]) -> dict[str, Any]:
    invokes: list[dict[str, Any]] = []
    exits: list[dict[str, Any]] = []
    targets: list[tuple[str, str]] = []
    if required and lstat_path(root, workflow, "installed workflow", errors, kind="file") is None:
        return {"invoke_markers": 0, "exit_markers": 0, "target_markers": 0}
    if not workflow.is_file() or workflow.is_symlink():
        return {"invoke_markers": 0, "exit_markers": 0, "target_markers": 0}
    for line in workflow.read_text(encoding="utf-8").splitlines():
        for kind, pattern in MARKER_PATTERNS.items():
            match = pattern.fullmatch(line)
            if not match:
                continue
            try:
                payload = json.loads(match.group(2 if kind == "target" else 1))
            except json.JSONDecodeError:
                errors.append(f"installed workflow has invalid {kind} marker JSON")
                continue
            if kind == "invoke": invokes.append(payload)
            elif kind == "exit": exits.append(payload)
            else: targets.append((match.group(1), str(payload.get("id") or "")))
    if required:
        integrated = {
            skill_id: entry for skill_id, entry in active.items()
            if entry.get("workflow_integration_state", "integrated") != "standalone_only"
        }
        for skill_id in integrated:
            count = sum(item.get("skill") == skill_id and item.get("required") is True for item in invokes)
            if count != 1:
                errors.append(f"active skill {skill_id} has {count} mandatory invoke markers")
        declared_consumers: set[tuple[str, str]] = set()
        for skill_id, entry in integrated.items():
            interface = entry["interface_data"]
            for declared in interface.get("external_exits", []):
                consumer = declared.get("consumer", {})
                if consumer.get("kind") in {"workflow", "stop"}:
                    declared_consumers.add((consumer["kind"], consumer["id"]))
                matching = [item for item in exits if item.get("skill") == skill_id and item.get("exit") == declared.get("id") and item.get("consumer") == consumer]
                if len(matching) != 1:
                    errors.append(f"active skill {skill_id} exit {declared.get('id')} has {len(matching)} matching exit markers")
        for consumer in declared_consumers:
            matches = [item for item in targets if item == consumer]
            other = [item for item in targets if item[1] == consumer[1] and item[0] != consumer[0]]
            if not matches:
                errors.append(f"{consumer[0]} consumer target {consumer[1]} has a kind mismatch" if other else f"{consumer[0]} consumer target {consumer[1]} is not declared")
            elif len(matches) != 1:
                errors.append(f"{consumer[0]} consumer target {consumer[1]} has multiple declarations")
        for target in targets:
            if target not in declared_consumers:
                errors.append(f"{target[0]} target {target[1]} is dangling")
    return {"invoke_markers": len(invokes), "exit_markers": len(exits), "target_markers": len(targets)}


def _validate(root: Path, skills_root: Path, workflow: Path, manifest_path: Path, require_workflow: bool | None) -> dict[str, Any]:
    errors: list[str] = []
    root = Path(os.path.abspath(root)); skills_root = Path(os.path.abspath(skills_root))
    registry = read_json(root, skills_root / "registry.json", "installed skill registry", errors) or {}
    entries = registry.get("skills") if isinstance(registry.get("skills"), list) else []
    active: dict[str, dict[str, Any]] = {}
    planned: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            errors.append("installed skill registry contains an invalid row")
            continue
        if entry.get("state") == "planned": planned.append(entry["id"]); continue
        if entry.get("state") != "active": errors.append(f"installed registry state is invalid for {entry['id']}"); continue
        package_rel = safe_relative(entry.get("package")); interface_rel = safe_relative(entry.get("interface"))
        if package_rel is None or interface_rel is None:
            errors.append(f"installed registry paths are invalid for {entry['id']}"); continue
        interface = read_json(root, skills_root / interface_rel, f"installed interface for {entry['id']}", errors)
        if interface is None: continue
        if interface.get("id") != entry["id"] or interface.get("state") != "active": errors.append(f"installed interface identity is invalid for {entry['id']}")
        active[entry["id"]] = {**entry, "package_rel": package_rel, "interface_rel": interface_rel, "interface_data": interface}
    marker_facts = workflow_facts(root, workflow, active, bool(active) if require_workflow is None else require_workflow, errors)
    facts: dict[str, Any] = {"schema_version": registry.get("schema_version"), "planned_ids": sorted(planned), "active_ids": sorted(active), **marker_facts}
    manifest = read_json(root, manifest_path, "installed extension manifest", errors) or {}
    provenance = manifest.get("skill_packages") if isinstance(manifest.get("skill_packages"), dict) else {}
    required = {"schema_version","status","canonical_registry_sha256","registry_schema_version","active_ids","selected_platforms","packages","files","removals","conflicts","sidecars"}
    if set(provenance) != required: errors.append("installed skill package provenance has invalid fields")
    if provenance.get("schema_version") != "1.0" or provenance.get("status") != "ok": errors.append("installed skill package provenance is invalid or conflicted")
    registry_path = skills_root / "registry.json"
    if registry_path.is_file() and provenance.get("canonical_registry_sha256") != sha256(registry_path): errors.append("installed registry digest does not match provenance")
    if provenance.get("registry_schema_version") != facts["schema_version"]: errors.append("installed registry schema version does not match provenance")
    if provenance.get("active_ids") != facts["active_ids"]: errors.append("installed registry lifecycle ids do not match provenance")
    selected = provenance.get("selected_platforms")
    if not isinstance(selected, list) or len(selected) != len(set(selected)) or any(item not in {"codex","cursor","claude"} for item in selected):
        errors.append("installed selected platform provenance is invalid"); selected = []
    expected: dict[str, tuple[str, Path]] = {}
    def expect(target: Path, source_relative: Path, source: Path):
        rel = lexical_relative(root, target)
        if rel is None: errors.append("derived installed skill path escapes the repository")
        else: expected[rel.as_posix()] = ((Path("trellis/skills/guru-team") / source_relative).as_posix(), source)
    expect(registry_path, Path("registry.json"), registry_path)
    finish = skills_root / "tests/test_finish_family_integration.py"
    if lstat_path(root, finish, "installed Finish family integration test", errors, kind="file", required=False): expect(finish, Path("tests/test_finish_family_integration.py"), finish)
    for name in ("schemas","adapters","contracts","consumers"):
        tree = skills_root / name
        if os.path.lexists(tree):
            for path in collect_files(root, tree, f"installed {name} root", errors): expect(path, path.relative_to(skills_root), path)
    kernel_root = skills_root.parent / "runtime"
    package_runtime_required = any(
        (skills_root / entry["package_rel"] / "commands.json").is_file()
        for entry in active.values()
    )
    if lstat_path(
        root,
        kernel_root,
        "installed shared runtime root",
        errors,
        kind="directory",
        required=package_runtime_required,
    ) is not None:
        for path in sorted(kernel_root.iterdir()):
            try:
                mode = path.lstat().st_mode
            except OSError:
                errors.append("installed shared runtime root contains an unreadable entry")
                continue
            if stat.S_ISLNK(mode):
                errors.append("installed shared runtime root contains a symlink entry")
                continue
            if stat.S_ISREG(mode) and path.suffix not in {".pyc", ".pyo"}:
                expect(
                    path,
                    Path("runtime") / path.name,
                    path,
                )
    expected_packages: dict[str, dict[str, str]] = {}
    expected_ids_by_platform: dict[str, set[str]] = {key:set() for key in PLATFORM_ROOTS}
    command_owners: dict[str, str] = {}
    for skill_id, entry in active.items():
        package = skills_root / entry["package_rel"]
        commands = read_json(root, package / "commands.json", f"installed commands for {skill_id}", errors) or {}
        if commands.get("package_id") != skill_id or not isinstance(commands.get("commands"), list):
            errors.append(f"installed command ownership is invalid for {skill_id}")
        else:
            validators = {
                item.get("id"): item.get("runtime_command")
                for item in entry["interface_data"].get("validators", [])
                if isinstance(item, dict)
            }
            seen_validators: set[str] = set()
            for command in commands["commands"]:
                if not isinstance(command, dict) or not isinstance(command.get("id"), str):
                    errors.append(f"installed command metadata is invalid for {skill_id}")
                    continue
                command_id = command["id"]
                previous = command_owners.get(command_id)
                if previous is not None:
                    errors.append(f"installed command id {command_id} has multiple owners: {previous}, {skill_id}")
                else:
                    command_owners[command_id] = skill_id
                validator_id = command.get("validator_id")
                seen_validators.add(str(validator_id))
                if command.get("owner") != skill_id or validators.get(validator_id) != command_id:
                    errors.append(f"installed command owner or interface binding is invalid for {skill_id}/{command_id}")
            if seen_validators != set(validators):
                errors.append(f"installed command validator coverage is incomplete for {skill_id}")
        files = collect_files(root, package, f"installed package {skill_id}", errors)
        tree_hash = hashlib.sha256()
        for path in files:
            inner = path.relative_to(package); expect(path, entry["package_rel"] / inner, path)
            tree_hash.update(inner.as_posix().encode()+b"\0"+path.read_bytes()+b"\0")
        interface = skills_root / entry["interface_rel"]
        expected_packages[skill_id] = {"id":skill_id,"interface_sha256":sha256(interface) if interface.is_file() else "","tree_sha256":tree_hash.hexdigest()}
        supported = set(entry.get("supported_platforms", [])); platforms = {"shared"}|(set(selected)&supported)
        public = public_files(package, entry["interface_data"], files)
        public_inner = {path.relative_to(package).as_posix() for path in public}
        for platform in platforms:
            expected_ids_by_platform[platform].add(skill_id)
            target_root = root / PLATFORM_ROOTS[platform] / skill_id
            actual = collect_files(root, target_root, f"{platform} public projection for {skill_id}", errors)
            actual_inner = {path.relative_to(target_root).as_posix() for path in actual}
            if actual_inner != public_inner: errors.append(f"{platform} public projection inventory for {skill_id} does not match allowlist")
            if any(Path(inner).parts[0] in PRIVATE_PROJECTION_ROOTS for inner in actual_inner): errors.append(f"{platform} public projection exposes private runtime/tests/errors for {skill_id}")
            for source in public:
                inner=source.relative_to(package); target=target_root/inner; expect(target,entry["package_rel"]/inner,source)
                target_stat=lstat_path(root,target,f"{platform} public file for {skill_id}",errors,kind="file")
                if target_stat and sha256(target)!=sha256(source): errors.append(f"{platform} runtime file content drift for {skill_id}/{inner.as_posix()}")
                if target_stat and bool(target_stat.st_mode&stat.S_IXUSR)!=bool(source.stat().st_mode&stat.S_IXUSR): errors.append(f"{platform} runtime file mode drift for {skill_id}/{inner.as_posix()}")
    package_records=provenance.get("packages") if isinstance(provenance.get("packages"),list) else []
    records={str(item.get("id")):item for item in package_records if isinstance(item,dict) and set(item)=={"id","interface_sha256","tree_sha256"}}
    if len(records)!=len(package_records) or set(records)!=set(expected_packages): errors.append("installed package provenance inventory is incomplete")
    for skill_id in set(records)&set(expected_packages):
        if records[skill_id]!=expected_packages[skill_id]: errors.append(f"installed package digest provenance drift for {skill_id}")
    files=provenance.get("files") if isinstance(provenance.get("files"),list) else []
    seen:set[str]=set()
    for index,item in enumerate(files):
        if not isinstance(item,dict) or set(item)!={"path","source","sha256","executable","action"}: errors.append(f"installed skill file record {index} is invalid"); continue
        rel=safe_relative(item.get("path")); source_rel=safe_relative(item.get("source"))
        if rel is None or source_rel is None or rel.as_posix() in seen: errors.append(f"installed skill file record {index} has invalid paths"); continue
        seen.add(rel.as_posix()); path=root/rel; path_stat=lstat_path(root,path,f"installed skill file {rel.as_posix()}",errors,kind="file")
        expected_record=expected.get(rel.as_posix())
        if expected_record is None: errors.append(f"installed manifest contains an unexpected file record: {rel.as_posix()}")
        elif source_rel.as_posix()!=expected_record[0]: errors.append(f"installed skill source provenance drift: {rel.as_posix()}")
        if path_stat and (not re.fullmatch(r"[0-9a-f]{64}",str(item.get("sha256") or "")) or sha256(path)!=item.get("sha256")): errors.append(f"installed skill file digest drift: {rel.as_posix()}")
        if path_stat and item.get("executable") is not bool(path_stat.st_mode&stat.S_IXUSR): errors.append(f"installed skill file mode drift: {rel.as_posix()}")
    if seen!=set(expected): errors.append("installed skill file provenance inventory is incomplete")
    removals=_validate_removals(root,provenance.get("removals"),"skill",None,errors)
    conflicts=provenance.get("conflicts") if isinstance(provenance.get("conflicts"),list) else []; sidecars=_validate_sidecars(root,provenance.get("sidecars"),errors,"skill")
    if conflicts: errors.append("installed skill package has unresolved conflicts")
    actual_sidecars=_scan_sidecars(root,[skills_root,*[root/path for path in PLATFORM_ROOTS.values()]],errors)
    if actual_sidecars!=sidecars: errors.append("installed skill sidecar inventory is incomplete")
    _validate_overlays(root,manifest.get("overlays"),selected,errors)
    for platform, relative in PLATFORM_ROOTS.items():
        platform_root=root/relative
        if lstat_path(root,platform_root,f"{platform} skill root",errors,kind="directory",required=False) is None: continue
        for child in platform_root.iterdir():
            try: mode=child.lstat().st_mode
            except OSError: errors.append(f"{platform} skill root contains an unreadable entry"); continue
            if child.name.startswith("guru-") and (stat.S_ISLNK(mode) or not stat.S_ISDIR(mode) or child.name not in expected_ids_by_platform[platform]): errors.append(f"unknown {platform} workflow skill copy: {child.name}")
    allowed={path.as_posix() for path in PLATFORM_ROOTS.values()}|{"trellis/skills"}
    for top in root.iterdir():
        try: mode=top.lstat().st_mode
        except OSError: continue
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode): continue
        candidate=top/"skills"
        if lstat_path(root,candidate,"platform skill discovery root",errors,kind="directory",required=False) is None: continue
        rel=lexical_relative(root,candidate)
        if rel and rel.as_posix() not in allowed and any(child.name.startswith("guru-") for child in candidate.iterdir()): errors.append(f"workflow skill copy exists in unknown platform root: {rel.as_posix()}")
    overlay=manifest.get("overlays") if isinstance(manifest.get("overlays"),dict) else {}
    return {"status":"passed" if not errors else "failed","mode":"installed","facts":{**facts,"selected_platforms":selected,"command_count":len(command_owners),"managed_file_count":len(files),"sidecar_count":len(sidecars),"removal_count":len(removals),"conflict_count":len(conflicts),"overlay_managed_file_count":len(overlay.get("files",[])) if isinstance(overlay.get("files"),list) else 0,"overlay_sidecar_count":len(overlay.get("sidecars",[])) if isinstance(overlay.get("sidecars"),list) else 0,"overlay_removal_count":len(overlay.get("removals",[])) if isinstance(overlay.get("removals"),list) else 0,"overlay_conflict_count":len(overlay.get("conflicts",[])) if isinstance(overlay.get("conflicts"),list) else 0},"errors":errors}


def _validate_removals(root:Path,value:Any,label:str,allowed_paths:set[str]|None,errors:list[str])->list[Any]:
    if not isinstance(value,list): errors.append(f"installed {label} removal provenance must be an array"); return []
    for index,item in enumerate(value):
        action=item.get("action") if isinstance(item,dict) else None; rel=safe_relative(item.get("path")) if isinstance(item,dict) else None
        fields={"path","action"}|({"previous_managed_sha256"} if action=="removed_managed" else set())
        if action not in {"removed_managed","already_missing"} or set(item)!=fields or rel is None or (allowed_paths is not None and rel.as_posix() not in allowed_paths): errors.append(f"installed {label} removal record {index} is invalid"); continue
        if lstat_path(root,root/rel,f"removed {label} path {rel.as_posix()}",errors,kind="file",required=False): errors.append(f"removed managed {label} path still exists: {rel.as_posix()}")
    return value


def _validate_sidecars(root:Path,value:Any,errors:list[str],label:str)->set[str]:
    if not isinstance(value,list): errors.append(f"installed {label} sidecar provenance must be an array"); return set()
    if value: errors.append(f"installed {label} package has unresolved sidecars" if label=="skill" else "installed overlays have unresolved sidecars")
    result:set[str]=set()
    for item in value:
        rel=safe_relative(item)
        if rel is None or rel.as_posix() in result or not rel.name.endswith(SIDECAR_SUFFIXES): errors.append(f"installed {label} sidecar provenance is invalid"); continue
        result.add(rel.as_posix()); lstat_path(root,root/rel,f"installed {label} sidecar {rel.as_posix()}",errors,kind="file")
    return result


def _scan_sidecars(root:Path,roots:list[Path],errors:list[str])->set[str]:
    result:set[str]=set()
    for tree in roots:
        if lstat_path(root,tree,"managed skill root",errors,kind="directory",required=False) is None: continue
        for path in collect_files(root,tree,"managed skill root",errors):
            if path.name.endswith(SIDECAR_SUFFIXES):
                rel=lexical_relative(root,path)
                if rel: result.add(rel.as_posix())
    return result


def _validate_overlays(root:Path,value:Any,selected:list[str],errors:list[str])->None:
    required={"schema_version","status","selected_platforms","files","removals","conflicts","sidecars"}; overlay=value if isinstance(value,dict) else {}
    if not isinstance(value,dict): errors.append("installed extension manifest has no overlay provenance")
    if set(overlay)!=required: errors.append("installed overlay provenance has invalid fields")
    if overlay.get("schema_version")!="1.0" or overlay.get("status")!="ok": errors.append("installed overlay provenance is invalid or conflicted")
    if overlay.get("selected_platforms")!=selected: errors.append("installed overlay platform selection does not match skill provenance")
    expected={path.as_posix() for platform,path in OVERLAY_PATHS.items() if platform in selected}; allowed={path.as_posix() for path in OVERLAY_PATHS.values()}; seen:set[str]=set()
    files=overlay.get("files") if isinstance(overlay.get("files"),list) else []
    for index,item in enumerate(files):
        if not isinstance(item,dict) or set(item)!={"path","source","sha256","executable","action"}: errors.append(f"installed overlay file record {index} is invalid"); continue
        rel=safe_relative(item.get("path"))
        if rel is None or rel.as_posix() not in allowed or rel.as_posix() in seen: errors.append(f"installed overlay file record {index} has an invalid path"); continue
        seen.add(rel.as_posix()); path=root/rel; path_stat=lstat_path(root,path,f"installed overlay file {rel.as_posix()}",errors,kind="file")
        if item.get("source")!=(Path("trellis/presets/guru-team/overlays")/rel).as_posix() or item.get("action") not in {"installed","unchanged","updated_managed"}: errors.append(f"installed overlay file record {index} has invalid provenance")
        if path_stat and sha256(path)!=item.get("sha256"): errors.append(f"installed overlay file digest drift: {rel.as_posix()}")
        if path_stat and item.get("executable") is not bool(path_stat.st_mode&stat.S_IXUSR): errors.append(f"installed overlay file mode drift: {rel.as_posix()}")
    if seen!=expected: errors.append("installed overlay file provenance inventory is incomplete")
    _validate_removals(root,overlay.get("removals"),"overlay",allowed,errors)
    conflicts=overlay.get("conflicts") if isinstance(overlay.get("conflicts"),list) else []
    if conflicts: errors.append("installed overlays have unresolved conflicts")
    declared=_validate_sidecars(root,overlay.get("sidecars"),errors,"overlay"); actual:set[str]=set()
    for path in OVERLAY_PATHS.values():
        target=root/path
        if path.as_posix() not in expected and lstat_path(root,target,f"unselected overlay path {path.as_posix()}",errors,kind="file",required=False): errors.append(f"Guru overlay exists for unselected platform: {path.as_posix()}")
        for suffix in SIDECAR_SUFFIXES:
            sidecar=target.with_name(target.name+suffix)
            if lstat_path(root,sidecar,f"overlay sidecar {sidecar.name}",errors,kind="file",required=False):
                rel=lexical_relative(root,sidecar)
                if rel: actual.add(rel.as_posix())
    if actual!=declared: errors.append("installed overlay sidecar inventory is incomplete")


def validate_skill_installed(root:Path,skills_root:Path,workflow:Path,manifest_path:Path,*,require_workflow:bool|None=None)->dict[str,Any]:
    try: return _validate(root,skills_root,workflow,manifest_path,require_workflow)
    except Exception:
        return {"status":"failed","mode":"installed","facts":{"schema_version":None,"planned_ids":[],"active_ids":[],"invoke_markers":0,"exit_markers":0,"target_markers":0,"selected_platforms":[],"managed_file_count":0,"sidecar_count":0,"removal_count":0,"conflict_count":0,"overlay_managed_file_count":0,"overlay_sidecar_count":0,"overlay_removal_count":0,"overlay_conflict_count":0},"errors":["installed skill validation failed safely on malformed input"]}
