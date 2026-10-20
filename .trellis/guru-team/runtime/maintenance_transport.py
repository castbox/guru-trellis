"""Technical transport to the complete external Trellis public maintenance SDK.

This module validates source/package identity and forwards inputs unchanged. It
never chooses a Task, a migration projection, a route, or a semantic result.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

from runtime.io import CommandError

_METHODS = {
    "getMaintenanceContract", "inspectToolsTarget", "inspectTaskTarget",
    "prepareToolsInstallation", "prepareTaskConversion", "prepareLegacyCloseout",
    "prepareArchivedTaskResume",
    "inspectFormalArchiveReactivation", "prepareFormalArchiveReactivation",
    "previewMaintenance", "applyMaintenance", "recoverMaintenance",
    "resumeMaintenance", "rollbackMaintenance",
}
_BRIDGE = r'''
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const request=JSON.parse(fs.readFileSync(0,'utf8'));
try {
 const root=request.root;
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
 const require=createRequire(path.join(root,'package.json'));
 const core=path.dirname(require.resolve('@mindfoldhq/trellis-core/package.json'));
 const sdk=await import(pathToFileURL(path.resolve(root,manifest.main)).href);
 if(!sdk.maintenance || typeof sdk.maintenance.getMaintenanceContract!=='function')
   throw Object.assign(new Error('Matching source lacks public maintenance API 1.0'),{code:'maintenance_prerequisite_missing'});
 if(request.method==='source') {
  console.log(JSON.stringify({contract:sdk.maintenance.getMaintenanceContract(),core_package_root:core}));
 } else {
  const method=sdk.maintenance[request.method];
  if(typeof method!=='function') throw new Error('Public maintenance method unavailable');
  const result=request.method==='applyMaintenance'
    ? await method(request.payload.plan,{state_dir:request.payload.state_dir})
    : await method(request.payload);
  console.log(JSON.stringify(result));
 }
} catch(error) {
 console.log(JSON.stringify({error:{code:error.code||'maintenance_prerequisite_missing',message:error.message}}));
 process.exitCode=1;
}
'''


def _fail(code, message):
    raise CommandError(code, "maintenance_source", message)


def _invoke(root, method, payload=None):
    try:
        proc = subprocess.run(["node", "--input-type=module", "-e", _BRIDGE],
                              input=json.dumps({"root": str(root), "method": method, "payload": payload}),
                              text=True, capture_output=True)
        result = json.loads(proc.stdout)
    except (OSError, ValueError) as exc:
        _fail("maintenance_prerequisite_missing", "Complete matching CLI/Core public maintenance SDK is unavailable: " + str(exc))
    if proc.returncode or not isinstance(result, dict) or "error" in result:
        error = result.get("error", {}) if isinstance(result, dict) else {}
        _fail(error.get("code", "maintenance_failed"), error.get("message", "Public maintenance invocation failed"))
    return result


def package_digest(root):
    """Actual executable package bytes/modes, matching the public candidate identity."""
    digest = hashlib.sha256()
    def walk(path, ref):
        if not path.exists():
            return
        if path.is_dir():
            for child in sorted(path.iterdir()):
                walk(child, ref + "/" + child.name)
        elif path.is_file():
            digest.update(ref.encode())
            digest.update(str(path.stat().st_mode & 0o777).encode())
            digest.update(path.read_bytes())
    for ref in ("package.json", "bin", "dist", "src"):
        walk(root / ref, ref)
    return digest.hexdigest()


def _dist(root):
    return {p.relative_to(root).as_posix(): (p.stat().st_mode & 0o777, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob("*") if p.is_file()}


def inspect_source(source):
    root = Path(source["cli_package_root"]).resolve()
    mode = source.get("dependency_mode")
    if mode not in ("source_locked", "local_candidate"):
        _fail("invalid_arguments", "Select source_locked or isolated-development local_candidate explicitly")
    facts = _invoke(root, "source")
    contract = facts["contract"]
    if (contract.get("maintenance_api") != "1.0" or contract.get("cli_version") != contract.get("core_version")
            or not {"tools_install", "task_conversion", "legacy_closeout"}.issubset(contract.get("operation_kinds", []))):
        _fail("maintenance_prerequisite_missing", "Matching public CLI/Core maintenance API 1.0 is required before writes")
    core = Path(facts["core_package_root"])
    actual = {"cli_version": contract["cli_version"], "core_version": contract["core_version"],
              "cli_digest": package_digest(root), "core_digest": package_digest(core)}
    if actual != source.get("expected_candidate"):
        _fail("candidate_mismatch", "Actual CLI/Core package bytes differ from the selected fixed candidate")
    if mode == "source_locked":
        guru = Path(source.get("guru_source_root", ""))
        fork = Path(source.get("fork_source_root", ""))
        if not source.get("guru_source_root") or not source.get("fork_source_root"):
            _fail("maintenance_prerequisite_missing", "Source-locked execution requires complete Guru and exact source-locked Fork checkouts")
        validator = guru / "trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py"
        try:
            spec = importlib.util.spec_from_file_location("guru_maintenance_source_validator", validator)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.validate_fork_source(guru, fork)
        except Exception as exc:
            _fail("maintenance_prerequisite_missing", "Formal Fork source prerequisite is unavailable: " + str(exc))
        if _dist(root / "dist") != _dist(fork / "packages/cli/dist") or _dist(core / "dist") != _dist(fork / "packages/core/dist"):
            _fail("candidate_mismatch", "Executing public package build differs from the source-locked build")
    return {"contract": contract, "actual_candidate": actual,
            "cli_package_root": str(root), "core_package_root": str(core),
            "unverified": ["formal_fork_source_lock"] if mode == "local_candidate" else []}


def call(source, method, payload=None):
    if method not in _METHODS:
        _fail("invalid_arguments", "Use a declared public maintenance SDK method")
    facts = inspect_source(source)
    if method == "getMaintenanceContract":
        return facts["contract"]
    if method == "prepareArchivedTaskResume" and "task_resume" not in facts["contract"]["operation_kinds"]:
        _fail("maintenance_prerequisite_missing", "The selected CLI/Core pair lacks task_resume; use the original tools/source owner before archive-resume writes")
    if method in ("inspectFormalArchiveReactivation", "prepareFormalArchiveReactivation"):
        capability = facts["contract"].get("formal_archive_reactivation", {})
        if ("formal_archive_reactivation" not in facts["contract"]["operation_kinds"]
                or "schema1" not in capability.get("task_families", [])
                or capability.get("generation") != "increment_once"
                or capability.get("original_archive") != "read_only"):
            _fail("maintenance_prerequisite_missing", "The selected CLI/Core pair lacks formal_archive_reactivation for schema1 with increment_once and read_only archive; use the original tools/source owner before formal archive reactivation")
    return _invoke(facts["cli_package_root"], method, payload)
