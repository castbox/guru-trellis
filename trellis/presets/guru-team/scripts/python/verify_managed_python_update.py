"""One real current-CLI clean/reapply sample; no platform or Python-minor matrix."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(SOURCE / "trellis/skills/guru-team"))
from runtime.bootstrap import active_pointer_path, runtime_identity
from runtime.temporary_lifecycle import temporary_directory


def run(arguments, *, cwd, environment):
    result = subprocess.run([str(item) for item in arguments], cwd=cwd, env=environment,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        # No provider/pip raw output is projected into reusable verification evidence.
        raise RuntimeError(f"{Path(str(arguments[0])).name} command failed (exit {result.returncode})")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trellis-cli", type=Path, required=True, help="Verified matching current CLI entry; used read-only.")
    parser.add_argument("--python", default="python3", help="Real Python 3 used to create a PATH venv without pip/jsonschema.")
    args = parser.parse_args()
    cli = args.trellis_cli.resolve(strict=True)
    seed = shutil.which(args.python)
    if seed is None:
        parser.error("--python must select an executable Python 3")
    node = shutil.which("node")
    if node is None:
        parser.error("node is required for the selected CLI")
    caller_pointer = active_pointer_path(SOURCE)
    caller_before = caller_pointer.read_bytes() if caller_pointer.is_file() else None
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    assets = SOURCE / "trellis/skills/guru-team/runtime"
    # Workflow is unchanged by #556, so the task base is its immutable marketplace source.
    workflow_ref = run(["git", "rev-parse", "origin/main"], cwd=SOURCE, environment=environment).strip()
    with temporary_directory("throwaway_install") as temporary:
        repo = temporary / "repo"
        repo.mkdir()
        path_venv = temporary / "path-python"
        run([seed, "-m", "venv", "--without-pip", path_venv], cwd=repo, environment=environment)
        path_python = path_venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python3")
        environment["PATH"] = str(path_python.parent) + os.pathsep + environment["PATH"]
        environment["GURU_TEAM_PYTHON_CACHE_ROOT"] = str(temporary / "cache")
        run([path_python, "-c", "import importlib.util; assert importlib.util.find_spec('jsonschema') is None; assert importlib.util.find_spec('pip') is None"],
            cwd=repo, environment=environment)
        run(["git", "init", "-q", "-b", "main"], cwd=repo, environment=environment)
        run([node, cli, "init", "--yes", "--codex", "--workflow", "guru-team", "--workflow-source",
             "gh:castbox/guru-trellis/trellis#" + workflow_ref], cwd=repo, environment=environment)
        if (repo / ".trellis/workflow.md").read_bytes() != (SOURCE / "trellis/workflows/guru-team/workflow.md").read_bytes():
            raise RuntimeError("pinned marketplace workflow differs from current canonical")
        command = ["bash", SOURCE / "trellis/presets/guru-team/scripts/bash/apply.sh", "--repo", repo, "--platform", "codex", "--json"]
        fresh = json.loads(run(command, cwd=SOURCE, environment=environment))
        if fresh["status"] != "ok" or fresh["python_runtime"]["action"] != "installed":
            raise RuntimeError("clean preset install failed")
        expected_id, identity = runtime_identity(assets, path_python)
        if fresh["python_runtime"]["runtime_identity"] != expected_id:
            raise RuntimeError("clean install did not select current PATH Python")
        pointer = active_pointer_path(repo)
        before = pointer.read_bytes()
        target = Path(fresh["python_runtime"]["interpreter"]).parents[2]
        metadata_before = (target / "metadata.json").read_bytes()
        # Direct installer runner is managed; its default target remains PATH python3.
        reapply = json.loads(run([fresh["python_runtime"]["interpreter"],
                                 SOURCE / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py",
                                 "--repo", repo, "--platform", "codex", "--json"], cwd=SOURCE, environment=environment))
        if reapply["status"] != "ok" or reapply["python_runtime"]["action"] != "reused":
            raise RuntimeError("explicit reapply did not reuse valid identity")
        if pointer.read_bytes() != before or (target / "metadata.json").read_bytes() != metadata_before:
            raise RuntimeError("same-identity reapply changed runtime metadata/pointer")
        resolver = repo / ".trellis/guru-team/runtime/resolve-python.sh"
        validation = json.loads(run([resolver, repo, repo / ".trellis/guru-team/runtime", "-m", "runtime.validate",
                                     "--mode", "installed", "--root", repo, "--json"], cwd=repo,
                                    environment={**environment, "PYTHONPATH": str(repo / ".trellis/guru-team")}))
        if validation.get("status") != "passed":
            raise RuntimeError("complete installed graph validation failed")
        for section in ("skill_packages", "overlays"):
            if reapply[section]["sidecars"] or reapply[section]["conflicts"]:
                raise RuntimeError("reapply has unresolved sidecars/conflicts")
        if list(repo.rglob("*.new")) or list(repo.rglob("*.bak")):
            raise RuntimeError("clean/reapply left sidecars")
        for source in (SOURCE / "trellis/presets/guru-team/spec/workflow").glob("*.md"):
            if source.read_bytes() != (repo / ".trellis/spec/workflow" / source.name).read_bytes():
                raise RuntimeError("canonical managed spec projection differs")
        for historical in (".trellis/.developer", ".trellis/workspace"):
            if (repo / historical).exists():
                raise RuntimeError("clean sample unexpectedly created historical workspace identity")
        summary = {"status": "passed", "sample": "one-current-clean-and-reapply", "platform": "codex",
                   "path_python_has_pip_or_jsonschema": False, "runtime_identity": expected_id,
                   "python_minor": identity["python_minor"], "clean_action": fresh["python_runtime"]["action"],
                   "reapply_action": reapply["python_runtime"]["action"],
                   "source_validation": fresh["skill_source_validation"]["returncode"],
                   "installed_validation": validation["status"], "sidecars": [],
                   "wrapper_evidence": "real-wrapper-capability-fixture-only",
                   "matrix": "not-executed", "cli_evidence": "verified-local-candidate"}
    caller_after = caller_pointer.read_bytes() if caller_pointer.is_file() else None
    if caller_before != caller_after:
        raise RuntimeError("caller active pointer changed")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
