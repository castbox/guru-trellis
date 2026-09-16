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

    def test_transport_preserves_ai_fields_and_runs_original_commands(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            package = repo / "package"
            envelope = {"public_input": {"task_ref": ".trellis/tasks/current"}, "owner_result": {"reason": "AI-authored sentinel"}}
            calls = []

            def execute(argv, **kwargs):
                calls.append(argv)
                if len(calls) == 1:
                    authored = json.loads(Path(argv[argv.index("--input") + 1]).read_text())
                    self.assertEqual(authored, envelope["owner_result"])
                    return subprocess.CompletedProcess(argv, 0, json.dumps({"artifact_path": "/checked/phase2-check.json"}), "")
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
                self.assertIn("--upstream-architecture", context)
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
                repository = Path(protocol["repository_projection_root"])
                facts = json.loads((repository / phase2_authoring.FACTS).read_text())
                trace = Path(protocol["trace_path"])
                events = []
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
