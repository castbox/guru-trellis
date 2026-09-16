"""Fact-only Phase 2 fixtures and transport to the existing installed owners."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from adapters.eval.fixture_io import public_input_path, run_git
from adapters.eval.eval_support import qualification_planning_identity

SKILL = "guru-check-task"
FACTS = "docs/phase2-evidence/public-authoring-facts.json"
ARCHITECTURE = "guru-maintain-architecture-baseline"
QUALIFIERS = ("guru-qualify-normal-scenario", "guru-qualify-solution-mechanism")
PUBLIC_READS = (
    "SKILL.md", "references/contract.md", "interface.json",
    "schemas/phase2-check.schema.json", "schemas/public-input.schema.json",
    "schemas/public-initial-check-input.schema.json",
)
ARCHITECTURE_READS = (
    "SKILL.md", "references/contract.md", "interface.json",
    "schemas/semantic-result.schema.json", "schemas/public-input-impact.schema.json",
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    public = json.loads(public_input_path(request).read_text(encoding="utf-8"))
    task_ref = public["task_ref"]
    task = Path(task_ref)
    if task.is_absolute() or ".." in task.parts:
        raise ValueError("Phase 2 task locator is unsafe")
    sources = [
        Path(request["workdir"]) / relative for relative in request["files"]
        if relative.endswith(".py")
    ]
    if len(sources) != 1:
        raise ValueError("Phase 2 authoring requires one implementation source")
    spec_paths = [
        ".trellis/spec/workflow/semantic-retrieval.md",
        ".trellis/spec/workflow/subtraction-first-compatibility.md",
    ]
    for relative in spec_paths:
        source = source_repo / relative
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Phase 2 required spec is unavailable: {relative}")
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    files = {
        f"{task_ref}/task.json": json.dumps({
            "id": task.name, "name": task.name, "status": "in_progress",
            "title": "Inclusive integer range", "branch": "main", "base_branch": "main",
        }) + "\n",
        f"{task_ref}/prd.md": "# Approved PRD\n\nR1: contains(value, lower, upper) returns whether lower <= value <= upper for integers with lower <= upper. Both endpoints are included. No I/O or state.\n",
        f"{task_ref}/design.md": "# Approved Design\n\nOne pure function in interval.py; preserve the existing signature. No new owner, storage, integration, compatibility layer, or deployment change. Docs SSOT: docs/range.md remains current. Architecture: no boundary changes.\n",
        f"{task_ref}/implement.md": "# Approved Implementation\n\nImplement the inclusive comparison and run test_interval.py. Review lower, interior, upper, outside, singleton and negative bounds.\n",
        "docs/range.md": "# Integer Range\n\ncontains(value, lower, upper) includes both endpoints, including singleton ranges. Inputs are integers and lower <= upper.\n",
        "docs/architecture/README.md": "# Architecture Baseline\n\nIdentity: range-v1. Active. interval.py owns a pure predicate; test_interval.py is its only caller. No external dependencies, state, deployment, or persistence.\n",
        "docs/architecture/00-foundation/design-constitution.md": "# Design Constitution\n\nIdentity: range-constitution-v1. Keep mature direct comparisons, complete interval semantics, one cohesive pure owner, minimum complexity, and no new debt.\n",
        "docs/architecture/06-governance/change-contract.md": "# Change Contract\n\nIdentity: range-contract-v1. Concerns: range-concerns-v1. A predicate correction within the existing pure function changes no architecture boundary. No project Architecture checks apply; functional tests are Phase 2 evidence.\n",
        "interval.py": "def contains(value, lower, upper):\n    raise NotImplementedError\n",
        "test_interval.py": (
            "import unittest\nfrom interval import contains\n\n"
            "class IntervalTests(unittest.TestCase):\n"
            "    def test_endpoints_and_interior(self):\n"
            "        for value in (2, 3, 4):\n"
            "            with self.subTest(value=value):\n"
            "                self.assertTrue(contains(value, 2, 4))\n"
            "    def test_outside(self):\n"
            "        for value in (1, 5):\n"
            "            self.assertFalse(contains(value, 2, 4))\n"
            "    def test_singleton(self):\n"
            "        self.assertTrue(contains(2, 2, 2))\n"
            "    def test_negative(self):\n"
            "        self.assertTrue(contains(-2, -4, -2))\n"
            "\nif __name__ == '__main__':\n    unittest.main()\n"
        ),
    }
    for relative, content in files.items():
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-qm", "stage inclusive range requirements and test fixture")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", run_git(fixture, "rev-parse", "HEAD"))
    (fixture / "interval.py").write_bytes(sources[0].read_bytes())
    validation = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "-v", "test_interval"],
        cwd=fixture, capture_output=True, text=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    evidence = fixture / "docs/phase2-evidence"
    write_json(evidence / "validation.json", {
        "argv": [sys.executable, "-B", "-m", "unittest", "-v", "test_interval"],
        "returncode": validation.returncode, "stdout": validation.stdout, "stderr": validation.stderr,
    })
    (evidence / "diff.patch").write_text(run_git(fixture, "diff", "HEAD") + "\n")
    # Only upstream call identity is prepared. Its semantic result is AI-authored.
    architecture_schema = json.loads((
        package.parent / ARCHITECTURE / "schemas/public-input-impact.schema.json"
    ).read_text(encoding="utf-8"))
    architecture_input = {
        "schema_version": "2.0", "profile": "task_impact_sync",
        "source_exit": "implementation_complete", "mode": "workflow",
        "continuation_id": "range-phase2", "stage": "phase2", "task_locator": task_ref,
        "baseline": {"locator": "docs/architecture/README.md", "identity": "range-v1", "status": "active"},
        "constitution": {
            "authority_locator": "docs/architecture/00-foundation/design-constitution.md",
            "authority_status": "current", "identity_kind": "version", "identity": "range-constitution-v1",
            "principles": [
                {key: value["const"] for key, value in architecture_schema["$defs"][f"p{index}"]["properties"].items()}
                for index in range(1, 6)
            ],
        },
        "project_contract": {
            "guru_contract_identity": f"{ARCHITECTURE}:2.0",
            "change_contract_locator": "docs/architecture/06-governance/change-contract.md",
            "change_contract_identity": "range-contract-v1",
            "required_concern_set_identity": "range-concerns-v1",
        },
        "freshness_identity": hashlib.sha256((fixture / "interval.py").read_bytes()).hexdigest(),
        "requirement_authority": f"{task_ref}/prd.md", "behavior_authority": f"{task_ref}/design.md",
    }
    write_json(evidence / "architecture-input.json", architecture_input)
    required = sorted([
        *files, *spec_paths, "docs/phase2-evidence/validation.json", "docs/phase2-evidence/diff.patch",
        "docs/phase2-evidence/architecture-input.json",
        *(f".trellis/guru-team/skills/packages/{ARCHITECTURE}/{path}" for path in ARCHITECTURE_READS),
        *(f".trellis/guru-team/skills/packages/{skill}/{path}" for skill in QUALIFIERS for path in (
            "SKILL.md", "references/contract.md", "schemas/semantic-result.schema.json",
            "schemas/public-phase2-candidate-set-input.schema.json",
        )),
        ".trellis/guru-team/skills/consumers/workflow/production/normal-scenario-qualification-invocation.schema.json",
        ".trellis/guru-team/skills/consumers/workflow/production/solution-mechanism-qualification-invocation.schema.json",
    ])
    write_json(fixture / FACTS, {
        "schema_version": "1.0", "required_reads": required,
        "architecture_input_sha256": hashlib.sha256(json.dumps(
            architecture_input, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest(),
        "reviewed_paths": sorted([*files, *(
            str(path.relative_to(fixture)) for path in evidence.iterdir()
        ), FACTS]),
        "current_head": run_git(fixture, "rev-parse", "HEAD"),
        "qualification_target": {
            "repo_locator": ".", "task_ref": task_ref,
            "checkout_head": run_git(fixture, "rev-parse", "HEAD"),
            "planning_identity": qualification_planning_identity(fixture, [
                f"{task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")
            ]),
            "diff_locator": "docs/phase2-evidence/diff.patch",
        },
    })


def execute(package: Path, repo: Path, envelope: dict, environment: dict) -> subprocess.CompletedProcess:
    """Record AI fields unchanged, then check and invoke the installed package."""
    runtime = repo / ".trellis/.runtime/guru-team/evals"
    authoring = runtime / "phase2-authoring.json"
    public_path = runtime / "phase2-public-input.json"
    public = envelope["public_input"]
    write_json(authoring, envelope["owner_result"])
    write_json(public_path, public)
    commands = [
        [str(package / "scripts/record-phase2-check.sh"), "--root", str(repo),
         "--task", public["task_ref"], "--input", str(authoring)],
        [str(package / "scripts/check-phase2-check.sh"), "--root", str(repo),
         "--task", public["task_ref"]],
    ]
    receipts = []
    try:
        for command in commands:
            result = subprocess.run(command, cwd=repo, env=environment, capture_output=True, text=True)
            receipts.append({"argv": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
            if result.returncode:
                return result
        artifact = json.loads(receipts[0]["stdout"])["artifact_path"]
        command = [str(package / "scripts/invoke.sh"),
                   "--input", str(public_path), "--owner-result", artifact]
        result = subprocess.run(command, cwd=repo, env=environment, capture_output=True, text=True)
        receipts.append({"argv": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        return result
    finally:
        write_json(repo.parent / "phase2-command-receipts.json", receipts)
        authoring.unlink(missing_ok=True)
        public_path.unlink(missing_ok=True)
