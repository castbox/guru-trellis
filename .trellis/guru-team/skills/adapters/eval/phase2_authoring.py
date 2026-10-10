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
        f"{task_ref}/design.md": "# Candidate Design\n\ninterval.py defines contains(value, lower, upper) using integer comparisons. test_interval.py calls it with endpoints, outside values, singleton ranges and negative bounds. docs/range.md specifies the inclusive predicate.\n",
        f"{task_ref}/implement.md": "# Approved Implementation\n\nImplement the inclusive comparison and run test_interval.py. Review lower, interior, upper, outside, singleton and negative bounds.\n",
        "docs/range.md": "# Integer Range\n\ncontains(value, lower, upper) includes both endpoints, including singleton ranges. Inputs are integers and lower <= upper.\n",
        "docs/architecture/README.md": "# Architecture Baseline\n\nIdentity: range-v1. Active. interval.py owns a pure predicate; range_filter.py is the production caller and test_interval.py verifies it. These modules have no external dependency, state, deployment or persistence.\n",
        "docs/architecture/00-foundation/design-constitution.md": "# Design Constitution\n\nIdentity: range-constitution-v1. The predicate module owns mathematical interval evaluation. The production filter composes it; neither module owns I/O or business rejection. Read project responsibilities and legal ranges from current authority.\n",
        "docs/architecture/06-governance/change-contract.md": "# Change Contract\n\nIdentity: range-contract-v1. Concerns: range-concerns-v1. Review actual predicate/filter ownership, state, dependencies and legal range contracts before classifying impact. No executable project Architecture check applies to this project; source and production caller are directly reviewable. Functional test results belong to the subsequent overall Phase 2 review.\n",
        "interval.py": "def contains(value, lower, upper):\n    raise NotImplementedError\n",
        "range_filter.py": "from interval import contains\ndef select(values, lower, upper):\n    return [value for value in values if contains(value, lower, upper)]\n",
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
    if "historical-red" in request["case_id"]:
        files.update({
            "legacy_report.py": "def format_legacy(value):\n    return str(value)\n",
            "test_legacy_report.py": "import unittest\nfrom legacy_report import format_legacy\nclass LegacyTests(unittest.TestCase):\n    def test_old_format(self):\n        self.assertEqual(format_legacy(2), '02')\n",
            "test_legacy_environment.py": "import os, unittest\nclass EnvironmentTests(unittest.TestCase):\n    def test_service_configuration(self):\n        self.assertTrue(os.environ['LEGACY_REPORT_SERVICE_AVAILABLE'])\n",
            "test_external_diagnostic.py": "import json, unittest\nfrom pathlib import Path\nclass ExternalDiagnostic(unittest.TestCase):\n    def test_observed_external_status(self):\n        observation = json.loads(Path('docs/phase2-evidence/external-observation.json').read_text())\n        self.assertEqual(observation['status'], 'ready')\n",
            "docs/legacy-report.md": "# Existing report\n\nLegacy report is a separate component, has no dependency on interval.py, and is not part of the range change. The historical reporting test, environment probe and external status diagnostic are optional diagnostics, not release gates. The external diagnostic has no before-result or verified cause; do not invent one.\n",
        })
    dependent = "required-dependency" in request["case_id"]
    test_layer = request["case_id"] in ("native-owner-test-boundary", "native-owner-test-support", "native-owner-selection-assertion")
    test_support = request["case_id"] == "native-owner-test-support"
    selection_assertion = request["case_id"] == "native-owner-selection-assertion"
    if test_layer:
        files.update({
            "interval.py": sources[0].read_text(encoding="utf-8"),
            f"{task_ref}/prd.md": "# Approved PRD\n\nR1: Complete verification of the existing inclusive integer predicate and production filtering: lower, interior, upper, outside, singleton and negative bounds. Inputs satisfy lower <= upper. Keep the pure production predicate and filter behavior.\n",
            f"{task_ref}/design.md": "# Candidate Design\n\nThe existing interval.py predicate and range_filter.py caller stay unchanged. test_interval.py verifies inclusive endpoints and singleton ranges; test_range_filter.py directly verifies production selection. Assertion support, when used, belongs only to tests.\n",
            f"{task_ref}/implement.md": "# Approved Implementation\n\nComplete boundary and singleton test coverage and run test_interval.py and test_range_filter.py, including any assertion support tests.\n",
            "test_range_filter.py": "import unittest\nfrom range_filter import select\nclass RangeFilterTests(unittest.TestCase):\n    def test_endpoints(self):\n        self.assertEqual(select([1, 2, 3, 4, 5], 2, 4), [2, 3, 4])\n    def test_singleton(self):\n        self.assertEqual(select([1, 2, 3], 2, 2), [2])\n    def test_negative(self):\n        self.assertEqual(select([-5, -4, -2, -1], -4, -2), [-4, -2])\n",
        })
        files["test_interval.py"] = files["test_interval.py"].replace(
            "\nif __name__ == '__main__':",
            "\nclass UpperEndpointTests(unittest.TestCase):\n    def test_upper_endpoint(self):\n        self.assertTrue(contains(4, 2, 4))\n\nif __name__ == '__main__':",
        )
        if test_support:
            files.update({
                "range_test_support.py": "from interval import contains\ndef assert_contains(testcase, value, lower, upper):\n    testcase.assertLess(lower, upper)\n    testcase.assertTrue(contains(value, lower, upper))\n",
                "test_range_test_support.py": "import unittest\nfrom range_test_support import assert_contains\nclass AssertionSupportTests(unittest.TestCase):\n    def test_singleton_assertion(self):\n        assert_contains(self, 2, 2, 2)\n",
            })
            files["docs/range.md"] += "\nThe existing range_test_support.assert_contains entry owns shared test assertions for contains. Its supported integer bounds are lower <= upper, including singleton ranges. New interval cases use this assertion entry; production filter tests call select directly.\n"
            files[f"{task_ref}/prd.md"] += "\nR2: Verify the existing shared assert_contains test entry and add singleton interval verification through that entry under its documented legal bounds.\n"
            files[f"{task_ref}/design.md"] += "\nThe singleton interval case calls the existing range_test_support.assert_contains entry; test_range_test_support.py also verifies this assertion entry.\n"
        if selection_assertion:
            files.update({
                "selection_test_support.py": "def assert_selection(testcase, actual_values, expected_values):\n    testcase.assertEqual(actual_values, expected_values.sort())\n",
                "test_selection_test_support.py": "import unittest\nfrom selection_test_support import assert_selection\nclass SelectionAssertionTests(unittest.TestCase):\n    def test_ordered_values(self):\n        assert_selection(self, [2], [2])\n",
                "test_selection.py": "import unittest\nclass SelectionTests(unittest.TestCase):\n    pass\n\nif __name__ == '__main__':\n    unittest.main()\n",
            })
            files["docs/range.md"] += "\nThe existing selection_test_support.assert_selection test entry compares actual and expected ordered lists of integers. New selection-verification cases use that assertion entry; independent production checks call select directly. The assertion helper has no interval validation or production imports.\n"
            files[f"{task_ref}/prd.md"] += "\nR2: Verify the existing ordered-list assert_selection test entry and add singleton selection verification through that entry.\n"
            files[f"{task_ref}/design.md"] += "\nThe new test_selection.py singleton case calls the existing generic selection_test_support.assert_selection entry with actual and expected lists. test_selection_test_support.py verifies that entry; test_range_filter.py retains independent direct production checks.\n"
    if dependent:
        files.update({
            "bounds_policy.py": "def ordered_bounds(lower, upper):\n    if not lower < upper:\n        raise ValueError('unordered bounds')\n    return lower, upper\n",
            "test_bounds_policy.py": "import unittest\nfrom bounds_policy import ordered_bounds\nclass BoundsTests(unittest.TestCase):\n    def test_ordered_singleton(self):\n        self.assertEqual(ordered_bounds(2, 2), (2, 2))\n",
            "test_range_filter.py": "import unittest\nfrom range_filter import select\nclass RangeFilterTests(unittest.TestCase):\n    def test_singleton_selection(self):\n        self.assertEqual(select([1, 2, 3], 2, 2), [2])\n",
            "docs/architecture/README.md": "# Architecture Baseline\n\nIdentity: range-v1. Active. bounds_policy.py owns pure ordered-bound validation reused by interval.py. interval.py owns the mathematical predicate; range_filter.py is its production caller. Each module has no I/O, external dependency, state or persistence.\n",
            f"{task_ref}/design.md": "# Candidate Design\n\ninterval.py delegates ordered-bound validation to bounds_policy.ordered_bounds and compares both endpoints inclusively. range_filter.py composes the predicate. Tests exercise the predicate, bound validation and production filtering.\n",
        })
    for relative, content in files.items():
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-qm", "stage inclusive range requirements and test fixture")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", run_git(fixture, "rev-parse", "HEAD"))
    historical = None
    if "historical-red" in request["case_id"]:
        historical = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_legacy_report"], cwd=fixture, text=True, capture_output=True, check=False)
    dependency_before = None
    if dependent:
        dependency_before = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_bounds_policy"], cwd=fixture, text=True, capture_output=True, check=False)
    test_modules = ["test_interval", "test_range_filter"] + (["test_range_test_support"] if test_support else [])
    if selection_assertion:
        test_modules.extend(["test_selection", "test_selection_test_support"])
    test_before = None
    direct_before = None
    if test_layer:
        test_before = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", *test_modules], cwd=fixture, text=True, capture_output=True, check=False)
        direct_before = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_range_filter"], cwd=fixture, text=True, capture_output=True, check=False)
    (fixture / "interval.py").write_bytes(sources[0].read_bytes())
    if test_layer:
        tests = fixture / "test_interval.py"
        if selection_assertion:
            (fixture / "test_selection.py").write_text("import unittest\nfrom range_filter import select\nfrom selection_test_support import assert_selection\nclass SelectionTests(unittest.TestCase):\n    def test_singleton_selection(self):\n        assert_selection(self, select([1, 2, 3], 2, 2), [2])\n\nif __name__ == '__main__':\n    unittest.main()\n", encoding="utf-8")
        elif test_support:
            tests.write_text(tests.read_text().replace("from interval import contains\n", "from interval import contains\nfrom range_test_support import assert_contains\n").replace("self.assertTrue(contains(2, 2, 2))", "assert_contains(self, 2, 2, 2)"), encoding="utf-8")
        else:
            tests.write_text(tests.read_text().replace("self.assertTrue(contains(4, 2, 4))", "self.assertFalse(contains(4, 2, 4))"), encoding="utf-8")
    validation_argv = [sys.executable, "-B", "-m", "unittest", "-v", "test_interval"]
    if test_layer:
        validation_argv = [sys.executable, "-B", "-m", "unittest", "-v", *test_modules]
    if dependent:
        validation_argv.extend(["test_bounds_policy", "test_range_filter"])
    validation = subprocess.run(
        validation_argv,
        cwd=fixture, capture_output=True, text=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    evidence = fixture / "docs/phase2-evidence"
    write_json(evidence / "validation.json", {
        "argv": validation_argv,
        "returncode": validation.returncode, "stdout": validation.stdout, "stderr": validation.stderr,
    })
    if test_before is not None:
        direct_after = subprocess.run(direct_before.args, cwd=fixture, text=True, capture_output=True, check=False)
        def receipt(process):
            return {"returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
        write_json(evidence / "test-layer-validation.json", {
            "argv": test_before.args, "before": receipt(test_before), "after": receipt(validation),
            "production_caller": {"argv": direct_before.args, "before": receipt(direct_before), "after": receipt(direct_after)},
        })
    if dependency_before is not None:
        dependency_after = subprocess.run(dependency_before.args, cwd=fixture, text=True, capture_output=True, check=False)
        write_json(evidence / "bounds-validation.json", {
            "argv": dependency_before.args,
            "before": {"returncode": dependency_before.returncode, "stdout": dependency_before.stdout, "stderr": dependency_before.stderr},
            "after": {"returncode": dependency_after.returncode, "stdout": dependency_after.stdout, "stderr": dependency_after.stderr},
        })
    if historical is not None:
        repeated = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_legacy_report"], cwd=fixture, text=True, capture_output=True, check=False)
        write_json(evidence / "external-observation.json", {"status": "unknown"})
        diagnostics = {}
        for module in ("test_legacy_environment", "test_external_diagnostic"):
            diagnostic_environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            diagnostic_environment.pop("LEGACY_REPORT_SERVICE_AVAILABLE", None)
            process = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", module], cwd=fixture, text=True, capture_output=True, check=False, env=diagnostic_environment)
            diagnostics[module] = {"returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
        write_json(evidence / "legacy-validation.json", {
            "baseline_head": run_git(fixture, "rev-parse", "HEAD"),
            "diagnostics_after_only": diagnostics,
            "before": {"returncode": historical.returncode, "stdout": historical.stdout, "stderr": historical.stderr},
            "after": {"returncode": repeated.returncode, "stdout": repeated.stdout, "stderr": repeated.stderr},
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
        "requirement_authority": "docs/range.md", "behavior_authority": f"{task_ref}/design.md",
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
    if historical is not None:
        required.extend(["docs/phase2-evidence/legacy-validation.json", "docs/phase2-evidence/external-observation.json"])
    if dependent:
        required.append("docs/phase2-evidence/bounds-validation.json")
    if test_layer:
        required.append("docs/phase2-evidence/test-layer-validation.json")
    write_json(fixture / FACTS, {
        "schema_version": "1.0", "required_reads": required,
        "architecture_reads": [
            "docs/architecture/00-foundation/design-constitution.md",
            "docs/architecture/README.md", "docs/architecture/06-governance/change-contract.md", f"{task_ref}/design.md",
            "docs/phase2-evidence/diff.patch", "interval.py", "range_filter.py",
            *(["bounds_policy.py"] if dependent else []),
            *(["test_interval.py", "test_range_filter.py"] if test_layer else []),
            *(["range_test_support.py", "test_range_test_support.py"] if test_support else []),
            *(["selection_test_support.py", "test_selection_test_support.py", "test_selection.py"] if selection_assertion else []),
            "docs/range.md",
            "docs/phase2-evidence/architecture-input.json",
        ],
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
        from runtime.io import project_intermediate_receipt
        artifact = project_intermediate_receipt(
            json.loads(receipts[0]["stdout"]), package.parents[1] / "schemas",
        )["artifact_path"]
        command = [str(package / "scripts/invoke.sh"),
                   "--input", str(public_path), "--owner-result", artifact]
        result = subprocess.run(command, cwd=repo, env=environment, capture_output=True, text=True)
        receipts.append({"argv": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        return result
    finally:
        write_json(repo.parent / "phase2-command-receipts.json", receipts)
        authoring.unlink(missing_ok=True)
        public_path.unlink(missing_ok=True)
