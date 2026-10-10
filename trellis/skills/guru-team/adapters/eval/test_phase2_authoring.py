from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import phase2_authoring, native_adapter, owner_staging
from adapters.eval.eval_support import package_tree_sha256
from adapters.eval.owner_runtime import load_package_runtime_module
from runtime.schema import validate_json

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / "packages/guru-check-task"


def request(root: Path, case_id: str) -> dict:
    case = next(item for item in json.loads((PACKAGE / "evals/evals.json").read_text())["evals"] if item["id"] == case_id)
    workdir = root / "execution/workdir"
    workdir.mkdir(parents=True)
    for relative in case["files"]:
        target = workdir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE / relative, target)
    interface = json.loads((PACKAGE / "interface.json").read_text())
    return {
        "schema_version": "1.0", "skill_id": PACKAGE.name, "package_root": str(PACKAGE),
        "case_id": case_id, "prompt": case["prompt"], "files": case["files"],
        "workdir": str(workdir), "interface": {"public_invocation": interface["public_contracts"]["invocation"]},
        "runtime_target": str(REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"),
        "native_execution_mode": "semantic_authoring", "native_execution_adapter": "codex",
        "model_id": case["model_id"],
    }


class Phase2AuthoringTests(unittest.TestCase):
    def test_source_and_installed_package_identity_excludes_private_tests(self):
        installed = REPO / ".trellis/guru-team/skills/packages/guru-check-task"
        self.assertTrue((PACKAGE / "tests").is_dir())
        self.assertFalse((installed / "tests").exists())
        self.assertEqual(package_tree_sha256(PACKAGE), package_tree_sha256(installed))

    def test_fact_only_staging_executes_actual_boundary_tests(self):
        for case_id, successful in (("native-owner-clean", True), ("native-owner-finding", False)):
            with self.subTest(case=case_id), tempfile.TemporaryDirectory() as temp:
                req = request(Path(temp), case_id)
                package, target, _ = owner_staging.stage_owner_execution(
                    req, Path(req["workdir"]).parent, Path(req["runtime_target"]),
                )
                repo = target.parents[4]
                self.assertFalse((repo / ".trellis/.runtime/guru-team/evals/owner-result.json").exists())
                self.assertFalse((repo / ".trellis/.runtime/guru-team/owner-checkpoints").exists())
                facts = json.loads((repo / phase2_authoring.FACTS).read_text())
                self.assertNotIn("typed_exit", json.dumps(facts))
                self.assertNotIn("expected_exit", json.dumps(facts))
                for locator in facts["required_reads"]:
                    self.assertTrue((repo / locator).is_file(), locator)
                for name in ("semantic-retrieval.md", "subtraction-first-compatibility.md"):
                    relative = f".trellis/spec/workflow/{name}"
                    self.assertIn(relative, facts["required_reads"])
                    self.assertEqual((repo / relative).read_bytes(), (REPO / relative).read_bytes())
                self.assertIn("interval.py", facts["reviewed_paths"])
                evidence = json.loads((repo / "docs/phase2-evidence/validation.json").read_text())
                self.assertEqual(evidence["returncode"] == 0, successful)
                if not successful:
                    self.assertIn("test_singleton", evidence["stderr"])
                    self.assertIn("AssertionError", evidence["stderr"])
                architecture = json.loads((repo / "docs/phase2-evidence/architecture-input.json").read_text())
                validate_json(architecture, package.parent / phase2_authoring.ARCHITECTURE / "schemas/public-input-impact.schema.json", "input")
                self.assertEqual(architecture["constitution"]["identity_kind"], "version")
                qualifier = load_package_runtime_module(target, "guru-qualify-normal-scenario", "common")
                paths = [f".trellis/tasks/current/{name}" for name in ("prd.md", "design.md", "implement.md")]
                self.assertEqual(facts["qualification_target"]["planning_identity"], qualifier.file_set_identity(repo, paths))
                self.qualifier_roundtrips(repo, package, facts["qualification_target"], successful)

    def qualifier_roundtrips(self, repo, package, target, clean):
        # Deterministic contract fixtures only, never native semantic evidence.
        for skill in phase2_authoring.QUALIFIERS:
            public = {
                "profile": "phase2_candidate_set", "mode": "workflow", "caller": "guru-check-task",
                "target_locator": ".trellis/tasks/current", "target": target,
                "candidate_refs": ["upper-bound"],
                "candidate_locators": [{"candidate_ref": "upper-bound", "locators": ["path:interval.py", "path:test_interval.py"]}],
            }
            semantic = {
                "schema_version": "1.0", "skill_id": skill, "public_input": public,
                "candidate_results": [{
                    "candidate_ref": "upper-bound",
                    "decision": "rejected_not_reproduced" if clean else "qualified_current",
                    "reason": "The current upper-bound tests pass." if clean else "The supported upper-bound tests fail.",
                    "witness": {
                        "requirement_refs": [".trellis/tasks/current/prd.md:R1"],
                        "supported_entry_refs": ["interval.py:contains"],
                        "existing_caller_refs": ["test_interval.py"],
                        "honest_action_sequence": ["Run the current unit tests."],
                        "defect_observation": "No upper-bound defect reproduced." if clean else "Inclusive upper bound returns false.",
                        "excluded_assumptions": [],
                    },
                }],
                "ai_review_gate": {"status": "passed", "reviewed_candidate_refs": ["upper-bound"], "summary": "Deterministic roundtrip fixture."},
                "typed_exit": "classified",
                "consumer": {"kind": "workflow", "id": skill.replace("guru-qualify-", "guru-") + "-classified-router"},
            }
            result = subprocess.run(
                [str(package.parent / skill / "scripts/invoke.sh"), "--invocation", "-"],
                input=json.dumps({"schema_version": "1.0", "semantic_result": semantic}),
                cwd=repo, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, (skill, result.stderr))
            self.assertEqual(json.loads(result.stdout)["exit_id"], "classified")

    def test_unchanged_bound_dependency_has_real_before_after_and_production_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            req = request(Path(temp), "native-owner-required-dependency")
            _, target, _ = owner_staging.stage_owner_execution(req, Path(req["workdir"]).parent, Path(req["runtime_target"]))
            repo = target.parents[4]
            facts = json.loads((repo / phase2_authoring.FACTS).read_text())
            receipts = json.loads((repo / 'docs/phase2-evidence/bounds-validation.json').read_text())
            for side in ('before', 'after'):
                self.assertNotEqual(receipts[side]['returncode'], 0)
                self.assertIn('ValueError: unordered bounds', receipts[side]['stderr'])
            validation = json.loads((repo / 'docs/phase2-evidence/validation.json').read_text())
            self.assertNotEqual(validation['returncode'], 0)
            self.assertIn('test_singleton_selection', validation['stderr'])
            self.assertIn('test_singleton', validation['stderr'])
            self.assertIn('bounds_policy.py', facts['architecture_reads'])
            self.assertNotIn('bounds_policy.py', (repo / 'docs/phase2-evidence/diff.patch').read_text())
            self.assertNotIn('typed_exit', json.dumps(facts))
            self.assertNotIn('prerequisite', json.dumps(facts))

    def test_test_layer_red_has_real_causality_and_unchanged_green_production(self):
        for case_id, before_success in (("native-owner-test-boundary", True), ("native-owner-test-support", False)):
            with self.subTest(case=case_id), tempfile.TemporaryDirectory() as temp:
                req = request(Path(temp), case_id)
                _, target, _ = owner_staging.stage_owner_execution(req, Path(req["workdir"]).parent, Path(req["runtime_target"]))
                repo = target.parents[4]
                facts = json.loads((repo / phase2_authoring.FACTS).read_text())
                receipts = json.loads((repo / "docs/phase2-evidence/test-layer-validation.json").read_text())
                self.assertEqual(receipts["before"]["returncode"] == 0, before_success)
                self.assertNotEqual(receipts["after"]["returncode"], 0)
                direct_tests = subprocess.run([sys.executable, "-B", "test_interval.py"], cwd=repo, capture_output=True, text=True, check=False)
                self.assertNotEqual(direct_tests.returncode, 0, direct_tests.stderr)
                for side in ("before", "after"):
                    self.assertEqual(receipts["production_caller"][side]["returncode"], 0)
                    self.assertIn("Ran 3 tests", receipts["production_caller"][side]["stderr"])
                diff = (repo / "docs/phase2-evidence/diff.patch").read_text()
                self.assertIn("diff --git a/test_interval.py", diff)
                self.assertNotIn("diff --git a/interval.py", diff)
                self.assertNotIn("diff --git a/range_filter.py", diff)
                self.assertEqual((repo / "interval.py").read_text(), subprocess.check_output(["git", "show", "HEAD:interval.py"], cwd=repo, text=True))
                for locator in facts["required_reads"]:
                    self.assertTrue((repo / locator).is_file(), locator)
                for locator in ("test_interval.py", "test_range_filter.py"):
                    self.assertIn(locator, facts["architecture_reads"])
                for term in ("expected_exit", "typed_exit", "regression", "prerequisite"):
                    self.assertNotIn(term, json.dumps(facts))
                if before_success:
                    self.assertIn("AssertionError: True is not false", receipts["after"]["stderr"])
                    self.assertIn("+        self.assertFalse(contains(4, 2, 4))", diff)
                else:
                    for side in ("before", "after"):
                        self.assertIn("test_singleton_assertion", receipts[side]["stderr"])
                        self.assertIn("AssertionError: 2 not less than 2", receipts[side]["stderr"])
                    self.assertIn("test_singleton (test_interval.IntervalTests", receipts["after"]["stderr"])
                    self.assertIn("+        assert_contains(self, 2, 2, 2)", diff)
                    self.assertNotIn("diff --git a/range_test_support.py", diff)
                    for locator in ("range_test_support.py", "test_range_test_support.py"):
                        self.assertIn(locator, facts["architecture_reads"])

    def test_existing_generic_assertion_has_real_before_after_and_required_test_caller(self):
        with tempfile.TemporaryDirectory() as temp:
            req = request(Path(temp), "native-owner-selection-assertion")
            _, target, _ = owner_staging.stage_owner_execution(req, Path(req["workdir"]).parent, Path(req["runtime_target"]))
            repo = target.parents[4]
            facts = json.loads((repo / phase2_authoring.FACTS).read_text())
            receipts = json.loads((repo / "docs/phase2-evidence/test-layer-validation.json").read_text())
            for side in ("before", "after"):
                self.assertNotEqual(receipts[side]["returncode"], 0)
                self.assertIn("test_ordered_values", receipts[side]["stderr"])
                self.assertIn("AssertionError: [2] != None", receipts[side]["stderr"])
                self.assertEqual(receipts["production_caller"][side]["returncode"], 0)
                self.assertIn("Ran 3 tests", receipts["production_caller"][side]["stderr"])
            self.assertNotIn("test_singleton_selection", receipts["before"]["stderr"])
            self.assertIn("test_singleton_selection", receipts["after"]["stderr"])
            direct = subprocess.run([sys.executable, "-B", "test_selection.py"], cwd=repo, capture_output=True, text=True, check=False)
            self.assertNotEqual(direct.returncode, 0)
            diff = (repo / "docs/phase2-evidence/diff.patch").read_text()
            self.assertIn("diff --git a/test_selection.py", diff)
            self.assertIn("+        assert_selection(self, select([1, 2, 3], 2, 2), [2])", diff)
            for locator in ("interval.py", "range_filter.py", "selection_test_support.py", "test_range_filter.py"):
                self.assertNotIn(f"diff --git a/{locator}", diff)
                self.assertEqual((repo / locator).read_text(), subprocess.check_output(["git", "show", f"HEAD:{locator}"], cwd=repo, text=True))
            for locator in ("test_selection.py", "selection_test_support.py", "test_selection_test_support.py"):
                self.assertIn(locator, facts["architecture_reads"])
            helper = (repo / "selection_test_support.py").read_text()
            self.assertNotIn("import", helper)
            self.assertNotIn("lower", helper)
            self.assertNotIn("upper", helper)
            for locator in facts["required_reads"]:
                self.assertTrue((repo / locator).is_file(), locator)
            for term in ("expected_exit", "typed_exit", "regression", "prerequisite"):
                self.assertNotIn(term, json.dumps(facts))

    def test_transport_preserves_ai_fields_and_runs_original_commands(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            package = repo / "skills/packages/guru-check-task"
            shutil.copytree(SKILLS / "schemas", package.parents[1] / "schemas")
            envelope = {"public_input": {"task_ref": ".trellis/tasks/current"}, "owner_result": {"reason": "AI-authored sentinel"}}
            calls = []

            def execute(argv, **kwargs):
                calls.append(argv)
                if len(calls) == 1:
                    authored = json.loads(Path(argv[argv.index("--input") + 1]).read_text())
                    self.assertEqual(authored, envelope["owner_result"])
                    return subprocess.CompletedProcess(argv, 0, json.dumps({"schema_version": "1.0", "formal_exit": False, "result": {"artifact_path": "/checked/phase2-check.json"}}), "")
                return subprocess.CompletedProcess(argv, 0, '{"exit_id":"blocked"}', "")

            with patch.object(phase2_authoring.subprocess, "run", side_effect=execute):
                result = phase2_authoring.execute(package, repo, envelope, os.environ.copy())
            self.assertEqual(result.stdout, '{"exit_id":"blocked"}')
            self.assertEqual([Path(call[0]).name for call in calls], ["record-phase2-check.sh", "check-phase2-check.sh", "invoke.sh"])
            self.assertNotIn("--root", calls[-1])
            self.assertFalse((repo / ".trellis/.runtime/guru-team/evals/phase2-authoring.json").exists())

    def test_recorder_error_is_not_repaired_or_converted_to_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            error = subprocess.CompletedProcess([], 2, "", "schema_mismatch: semantic_review")
            with patch.object(phase2_authoring.subprocess, "run", return_value=error) as run:
                result = phase2_authoring.execute(repo, repo, {
                    "public_input": {"task_ref": ".trellis/tasks/current"}, "owner_result": {},
                }, os.environ.copy())
            self.assertIs(result, error)
            self.assertEqual(run.call_count, 1)

    def test_context_requires_phase2_not_architecture_schema_and_no_expected_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            req = request(Path(temp), "native-owner-clean")
            values = native_adapter.build_context(req, "codex")
            context, _, _, _, protocol_path, native_path, _, _, thread, stop, _ = values
            try:
                self.assertIn("schemas/phase2-check.schema.json", context)
                self.assertNotIn("--upstream-architecture", context)
                self.assertIn("--qualifier normal-scenario", context)
                self.assertIn("--qualifier solution-mechanism", context)
                self.assertNotIn("adapter has already completed", context)
                native = json.loads(native_path.read_text())
                self.assertNotIn("expected_exit", native)
                self.assertNotIn("assertions", native)
                projection = Path(json.loads(protocol_path.read_text())["projection_root"])
                self.assertTrue((projection / "schemas/phase2-check.schema.json").is_file())
                self.assertFalse((projection / "evals").exists())
                protocol = json.loads(protocol_path.read_text())
                self.assertIn("--upstream-architecture", protocol["architecture_context"])
                self.assertNotIn("prd.md", protocol["architecture_context"])
                self.assertNotIn("implement.md", protocol["architecture_context"])
                repository = Path(protocol["repository_projection_root"])
                facts = json.loads((repository / phase2_authoring.FACTS).read_text())
                self.assertEqual(facts['architecture_reads'][:3], [
                    'docs/architecture/00-foundation/design-constitution.md',
                    'docs/architecture/README.md', 'docs/architecture/06-governance/change-contract.md',
                ])
                trace = Path(protocol["trace_path"])
                architecture_skill = repository / ".trellis/guru-team/skills/packages" / phase2_authoring.ARCHITECTURE / "SKILL.md"
                events = [{"kind": "read", "target_kind": "owner_file", "path": str(architecture_skill),
                           "sha256": hashlib.sha256(architecture_skill.read_bytes()).hexdigest(), "request_sha256": values[6]}] + [
                    {"kind": "read", "target_kind": "owner_file", "path": str(repository / relative),
                     "sha256": hashlib.sha256((repository / relative).read_bytes()).hexdigest(),
                     "request_sha256": values[6]}
                    for relative in facts["architecture_reads"]
                ]
                reviewer_count = len(events)
                for kind, paths in (
                    ("skill_contract", [projection / path for path in phase2_authoring.PUBLIC_READS]),
                    ("case_file", sorted((Path(protocol["model_root"]) / "evidence/case").iterdir())),
                    ("owner_file", [repository / phase2_authoring.FACTS, *(repository / path for path in facts["required_reads"])]),
                ):
                    for path in paths:
                        events.append({
                            "kind": "read", "target_kind": kind, "path": str(path),
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "request_sha256": values[6],
                        })
                output = '{"exit_id":"passed"}'
                wrappers = [
                    repository / ".trellis/guru-team/skills/packages" / skill / "scripts/invoke.sh"
                    for skill in (phase2_authoring.ARCHITECTURE, *phase2_authoring.QUALIFIERS)
                ] + [projection / "scripts/invoke.sh"]
                for wrapper in wrappers:
                    events.append({
                        "kind": "invoke", "wrapper_path": str(wrapper),
                        "argv": [str(wrapper), "--invocation", "-"], "returncode": 0,
                        "stdout_sha256": hashlib.sha256(output.encode()).hexdigest(),
                        "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                        "request_sha256": values[6],
                    })
                # Upstream invocation occurred before the overall owner's task reads.
                upstream = events.pop(-4)
                events.insert(reviewer_count, upstream)
                receipt = {
                    "schema_version": "1.0", "request_sha256": values[6],
                    "projection_root": str(projection),
                    "skill_sha256": protocol["skill_sha256"], "wrapper_sha256": protocol["wrapper_sha256"],
                    "events": events,
                }
                trace.write_text(json.dumps(receipt))
                native_adapter.validate_native_trace(trace, values[6], req, wrappers[-1], output, protocol_path)
                receipt["events"] = events[:-3] + events[-1:]
                trace.write_text(json.dumps(receipt))
                with self.assertRaisesRegex(ValueError, "public wrapper invocation"):
                    native_adapter.validate_native_trace(trace, values[6], req, wrappers[-1], output, protocol_path)
                receipt["events"] = [event for event in events if event.get("path") != str(repository / "test_interval.py")]
                trace.write_text(json.dumps(receipt))
                with self.assertRaisesRegex(ValueError, "required authority reads"):
                    native_adapter.validate_native_trace(trace, values[6], req, wrappers[-1], output, protocol_path)
            finally:
                stop.set()
                thread.join(timeout=2)

    def test_existing_routes_remain_post_owner(self):
        cases = json.loads((PACKAGE / "evals/evals.json").read_text())["evals"]
        existing = {item["expected_exit"] for item in cases if item.get("native_execution_mode", "post_owner") == "post_owner"}
        self.assertEqual(existing, {"passed", "implementation_required", "planning_stale", "blocked"})


if __name__ == "__main__":
    unittest.main()
