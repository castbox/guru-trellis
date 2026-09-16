from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import eval_runner as runner
from runtime.io import CommandError

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
SKILL = "guru-review-change-request"
PACKAGE = SKILLS / "packages" / SKILL


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def snapshot(root):
    return {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}


class SemanticGradingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.run_root = self.root / "run"
        self.args = argparse.Namespace(skill=SKILL, adapter="codex", case="standard-intake-authoring-scope-conflict",
            run_root=str(self.run_root), current_package=None, comparison_package=None,
            semantic_grading=None, human_feedback=None, mode="source")
        self.corpus = json.loads((PACKAGE / "evals/evals.json").read_text())

    def adapter(self, skills, descriptor, request_path, host_environment=None):
        # Transport double only: these unit tests do not claim native semantics.
        request = json.loads(request_path.read_text())
        case = next(item for item in self.corpus["evals"] if item["id"] == request["case_id"])
        trace = request_path.parent / "native-trace.json"
        write(trace, {"terminal_skill_id": "guru-clarify-requirements"})
        write(request_path.parent / "adapter-transcript.json", {"adapter": "codex", "text": "unit transport"})
        return {"corpus_sha256": request["corpus_sha256"], "capability_status": "executed",
            "public_stdout": json.dumps({"exit_id": case["expected_exit"]}), "public_stderr": "",
            "trace_events": ["public_invocation", "evals_not_loaded", "private_runtime_not_read"],
            "transcript_locator": str(request_path.parent / "adapter-transcript.json"),
            "native_trace_locator": str(trace), "timing_ms": 123}

    def raw(self):
        with mock.patch.object(runner, "call_adapter", side_effect=self.adapter):
            return runner.run(REPO, SKILLS, self.args)

    def grading(self, report, passed=True):
        path = self.root / "grading.json"
        write(path, {"schema_version": "1.0", "results": [
            {"case_id": case["case_id"], "comparison_side": case["comparison_side"],
             "assertion_id": assertion["id"], "passed": passed, "summary": "independent test grade"}
            for case in report["cases"]
            for assertion in next(row for row in self.corpus["evals"] if row["id"] == case["case_id"])
                .get("assertions", {}).get("semantic", [])]})
        self.args.semantic_grading = str(path)
        return path

    def test_raw_intake_requires_transcript_grading(self):
        for case in self.corpus["evals"][:2]:
            self.assertTrue(case["assertions"]["semantic"])
            self.assertTrue(all(item["evidence_selector"] == "transcript" for item in case["assertions"]["semantic"]))
        report = self.raw()
        self.assertEqual(report["status"], "evaluation_failed")
        self.assertTrue(all(row["passed"] for row in report["cases"][0]["deterministic_results"]))
        self.assertFalse(report["cases"][0]["semantic_results"][0]["passed"])

    def test_post_grade_updates_only_grading_and_aggregate_without_execution(self):
        before = self.raw()
        self.grading(before)
        files = snapshot(self.run_root)
        with mock.patch.object(runner, "call_adapter") as adapter, \
                mock.patch.object(runner, "completed_execution") as validation:
            after = runner.run(REPO, SKILLS, self.args)
        adapter.assert_not_called()
        validation.assert_called_once()
        self.assertEqual(after["status"], "passed")
        for old, new in zip(before["cases"], after["cases"]):
            for field in old.keys() - {"status", "semantic_results"}:
                self.assertEqual(old[field], new[field])
        report_name = Path(after["evidence_path"]).name
        self.assertEqual({key: value for key, value in files.items() if key != report_name},
                         {key: value for key, value in snapshot(self.run_root).items() if key != report_name})

    def test_failed_execution_or_deterministic_check_cannot_be_graded_green(self):
        before = self.raw()
        self.grading(before)
        for status in ("execution_error", "unsupported", "evaluation_failed"):
            report = copy.deepcopy(before)
            report["status"] = report["cases"][0]["status"] = status
            if status == "evaluation_failed":
                report["cases"][0]["deterministic_results"][0]["passed"] = False
            write(Path(report["evidence_path"]), report)
            with mock.patch.object(runner, "completed_execution"), mock.patch.object(runner, "call_adapter") as adapter:
                after = runner.run(REPO, SKILLS, self.args)
            self.assertEqual(after["status"], status)
            adapter.assert_not_called()

    def test_negative_missing_invalid_or_wrong_identity_grade_never_passes(self):
        report = self.raw()
        path = self.grading(report, False)
        with mock.patch.object(runner, "completed_execution"):
            self.assertEqual(runner.run(REPO, SKILLS, self.args)["status"], "evaluation_failed")
        valid = json.loads(path.read_text())
        invalids = [{"schema_version": "1.0", "results": []}, {"schema_version": "wrong", "results": []}]
        for field, value in (("case_id", "other"), ("comparison_side", "comparison"), ("assertion_id", "other")):
            changed = copy.deepcopy(valid)
            changed["results"][0][field] = value
            invalids.append(changed)
        duplicate = copy.deepcopy(valid)
        duplicate["results"].append({**duplicate["results"][0], "summary": "second grade"})
        invalids.append(duplicate)
        for grading in invalids:
            with self.subTest(grading=grading):
                write(path, grading)
                files = snapshot(self.run_root)
                with mock.patch.object(runner, "call_adapter") as adapter, self.assertRaises(CommandError):
                    runner.run(REPO, SKILLS, self.args)
                adapter.assert_not_called()
                self.assertEqual(files, snapshot(self.run_root))

    def test_missing_completed_run_does_not_stage_or_execute(self):
        path = self.root / "grade.json"
        write(path, {"schema_version": "1.0", "results": []})
        self.args.semantic_grading = str(path)
        with mock.patch.object(runner, "call_adapter") as adapter, self.assertRaises(CommandError):
            runner.run(REPO, SKILLS, self.args)
        adapter.assert_not_called()
        self.assertFalse(self.run_root.exists())

    def test_raw_authoring_cannot_overwrite_a_completed_or_partial_run(self):
        self.raw()
        files = snapshot(self.run_root)
        with mock.patch.object(runner, "call_adapter") as adapter, self.assertRaises(CommandError):
            runner.run(REPO, SKILLS, self.args)
        adapter.assert_not_called()
        self.assertEqual(files, snapshot(self.run_root))

    def test_fresh_post_owner_keeps_existing_grading_startup_path(self):
        self.args.case = "ready-route"
        grade = self.run_root / "grade.json"
        write(grade, {"schema_version": "1.0", "results": []})
        self.args.semantic_grading = str(grade)
        with mock.patch.object(runner, "call_adapter", side_effect=self.adapter) as adapter:
            report = runner.run(REPO, SKILLS, self.args)
        adapter.assert_called_once()
        self.assertEqual(report["cases"][0]["actual_exit"], "ready")
        with mock.patch.object(runner, "call_adapter", side_effect=self.adapter) as adapter, \
                mock.patch.object(runner, "grade_completed_run") as regrade:
            runner.run(REPO, SKILLS, self.args)
        adapter.assert_called_once()
        regrade.assert_not_called()
        (self.run_root / f"{SKILL}-codex-run.json").unlink()
        self.args.semantic_grading = str(self.root / "grade.json")
        write(Path(self.args.semantic_grading), {"schema_version": "1.0", "results": []})
        with mock.patch.object(runner, "call_adapter", side_effect=self.adapter) as adapter, \
                mock.patch.object(runner, "grade_completed_run") as regrade:
            runner.run(REPO, SKILLS, self.args)
        adapter.assert_called_once()
        regrade.assert_not_called()

    def test_architecture_and_phase2_keep_original_fresh_and_saved_execution_path(self):
        for skill in ("guru-maintain-architecture-baseline", "guru-check-task"):
            package, interface, _ = runner.package_context(SKILLS, skill)
            self.corpus, _ = runner.corpus(SKILLS, package, interface)
            case = next(case for case in self.corpus["evals"] if case.get("native_execution_mode") == "semantic_authoring")
            self.args.skill, self.args.case = skill, case["id"]
            self.args.run_root = str(self.root / skill)
            grade = self.root / f"{skill}-grade.json"
            write(grade, {"schema_version": "1.0", "results": []})
            self.args.semantic_grading = str(grade)
            for selection in (case["id"], None):
                self.args.case = selection
                self.args.run_root = str(self.root / skill / (selection or "full"))
                for grading in (str(grade), None, str(grade)):
                    self.args.semantic_grading = grading
                    with mock.patch.object(runner, "call_adapter", side_effect=self.adapter) as adapter, \
                            mock.patch.object(runner, "grade_completed_run") as regrade:
                        runner.run(REPO, SKILLS, self.args)
                    self.assertEqual(adapter.call_count, 1 if selection else len(self.corpus["evals"]))
                    regrade.assert_not_called()

    def test_missing_saved_request_and_stale_request_fail_closed(self):
        report = self.raw()
        self.grading(report)
        path = self.run_root / "current" / self.args.case / "adapter-request.json"
        request = json.loads(path.read_text())
        for field in (None, "model_id", "native_authoring_flow", "corpus_sha256", "package_root", "skill_id", "interface"):
            with self.subTest(field=field):
                if field is None:
                    path.unlink()
                else:
                    write(path, {**request, field: "stale"})
                files = snapshot(self.run_root)
                with mock.patch.object(runner, "call_adapter") as adapter, self.assertRaises(CommandError):
                    runner.run(REPO, SKILLS, self.args)
                adapter.assert_not_called()
                self.assertEqual(files, snapshot(self.run_root))

    def test_mixed_selection_is_not_regraded(self):
        focused = self.raw()
        self.grading(focused)
        self.args.case = None
        with self.assertRaisesRegex(CommandError, "eval_completed_mixed_flow"):
            runner.run(REPO, SKILLS, self.args)
        self.args.current_package = str(PACKAGE)
        self.args.comparison_package = str(PACKAGE)
        self.args.semantic_grading = None
        self.args.run_root = str(self.root / "full")
        full = self.raw()
        self.assertEqual(len(full["cases"]), 2 * len(self.corpus["evals"]))
        self.grading(full)
        files = snapshot(Path(self.args.run_root))
        with mock.patch.object(runner, "grade_completed_run") as regrade, \
                mock.patch.object(runner, "call_adapter") as adapter, \
                self.assertRaisesRegex(CommandError, "eval_completed_mixed_flow"):
            runner.run(REPO, SKILLS, self.args)
        adapter.assert_not_called()
        regrade.assert_not_called()
        self.assertEqual(files, snapshot(Path(self.args.run_root)))
        for change in ("missing", "duplicate", "unknown", "focused"):
            report = copy.deepcopy(full)
            if change == "missing":
                report["cases"].pop()
            elif change == "duplicate":
                report["cases"].append(report["cases"][0])
            elif change == "unknown":
                report["cases"][0]["case_id"] = "unknown"
            else:
                self.args.case = self.corpus["evals"][0]["id"]
            write(Path(full["evidence_path"]), report)
            with mock.patch.object(runner, "call_adapter") as adapter, self.assertRaises(CommandError):
                runner.run(REPO, SKILLS, self.args)
            adapter.assert_not_called()

    def test_intake_comparison_identity_is_exact(self):
        self.args.current_package = self.args.comparison_package = str(PACKAGE)
        report = self.raw()
        self.grading(report)
        with mock.patch.object(runner, "completed_execution"), mock.patch.object(runner, "call_adapter") as adapter:
            self.assertEqual(runner.run(REPO, SKILLS, self.args)["status"], "passed")
        adapter.assert_not_called()
        for change in ("missing", "duplicate", "unknown", "side"):
            changed = copy.deepcopy(report)
            if change == "missing":
                changed["cases"].pop()
            elif change == "duplicate":
                changed["cases"].append(changed["cases"][0])
            elif change == "unknown":
                changed["cases"][0]["case_id"] = "other"
            else:
                changed["cases"][0]["comparison_side"] = "comparison"
            write(Path(report["evidence_path"]), changed)
            with self.assertRaises(CommandError):
                runner.run(REPO, SKILLS, self.args)

    def test_intake_transport_scoring_preserves_execution_in_both_model_layouts(self):
        from adapters.eval import native_adapter
        from adapters.eval.intake_authoring import FACTS_PATH, INTAKE_SKILLS

        # Real context/projection/helper/validator, with local transport receipts.
        # No installer, Git writes, native model, or semantic acceptance claim.
        for external_model in (False, True):
            with self.subTest(external_model=external_model):
                self.run_root = self.root / str(external_model)
                self.args.run_root = str(self.run_root)
                self.args.semantic_grading = None
                report = self.raw()
                case_root = self.run_root / "current" / self.args.case
                request = json.loads((case_root / "adapter-request.json").read_text())
                fixture = json.loads((PACKAGE / request["files"][0]).read_text())
                owner = self.root / f"owner-{external_model}"
                for relative, content in fixture["repository_files"].items():
                    path = owner / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                write(owner / FACTS_PATH, {"source": fixture["source"], "required_reads": list(fixture["repository_files"])})
                target = owner / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
                model = (self.root / "external-model" if external_model else case_root / "execution/model")
                model.mkdir(parents=True)
                with mock.patch.object(native_adapter, "stage_owner_execution", return_value=(PACKAGE, target, {})), \
                        mock.patch.object(native_adapter.tempfile, "mkdtemp", return_value=str(model)):
                    built = native_adapter.build_context(request, "codex")
                context, context_path, wrapper, trace, protocol_path, native_path, digest, _, thread, stop, _ = built
                try:
                    protocol = json.loads(protocol_path.read_text())
                    args = [sys.executable, "-B", protocol["helper_path"]]
                    for flag, field in (("trace", "trace_path"), ("request-sha256", "request_sha256"),
                            ("projection-root", "projection_root"), ("repository-root", "repository_projection_root"),
                            ("sandbox-root", "model_root"), ("request-fifo", "request_fifo"),
                            ("response-fifo", "response_fifo"), ("skill-sha256", "skill_sha256"),
                            ("wrapper-sha256", "wrapper_sha256")):
                        args.extend(["--" + flag, protocol[field]])
                    for kind, paths in protocol["intake_read_paths"].items():
                        for path in paths:
                            read = subprocess.run([*args, "--flow", "standard_intake", "read", "--kind", kind, "--path", path],
                                                  capture_output=True, timeout=10)
                            self.assertEqual(read.returncode, 0, read.stderr)
                    stdout = '{"exit_id":"blocked"}'
                    command = {"skill_id": INTAKE_SKILLS[2], "command": "invoke", "arguments": ["--invocation", "-"], "stdin": "{}"}
                    response = {"returncode": 0, "stdout": stdout, "stderr": ""}
                    write(Path(protocol["intake_receipts_path"]), [{"request": command, "response": response}])
                    payload = json.loads(trace.read_text())
                    payload["terminal_skill_id"] = command["skill_id"]
                    payload["events"].append({"kind": "command", "skill_id": command["skill_id"], "command": "invoke",
                        "arguments": command["arguments"], "stdin_sha256": hashlib.sha256(b"{}").hexdigest(),
                        "returncode": 0, "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
                        "stderr_sha256": hashlib.sha256(b"").hexdigest(), "request_sha256": digest})
                    write(trace, payload)
                    output = model / "last-message.json"
                    output.write_text(stdout)
                    argv = ["codex", "--model", request["model_id"], "--output-last-message", str(output)]
                    write(case_root / "adapter-transcript.json", {"adapter": "codex", "native_command": "codex", "argv": argv,
                        "returncode": 0, "stdout": stdout, "context_path": str(context_path), "protocol_path": str(protocol_path),
                        "projection_root": protocol["projection_root"], "wrapper_path": str(wrapper), "native_request_path": str(native_path),
                        "native_trace_path": str(trace), "model_input_audit": {"argv": argv, "context": context,
                            "native_request": json.loads(native_path.read_text())}})
                    self.grading(report)
                    before, visible = snapshot(case_root), snapshot(model)
                    with mock.patch.object(runner, "call_adapter") as adapter:
                        graded = runner.run(REPO, SKILLS, self.args)
                    self.assertEqual(graded["status"], "passed")
                    adapter.assert_not_called()
                    self.assertEqual(before, snapshot(case_root))
                    self.assertEqual(visible, snapshot(model))
                    for key in report["cases"][0].keys() - {"status", "semantic_results"}:
                        self.assertEqual(report["cases"][0][key], graded["cases"][0][key])
                    # Ordinary lost execution evidence must not be repaired by grading.
                    trace.unlink()
                    before = snapshot(case_root)
                    with self.assertRaises(CommandError):
                        runner.run(REPO, SKILLS, self.args)
                    self.assertEqual(before, snapshot(case_root))
                finally:
                    stop.set()
                    thread.join(timeout=3)



if __name__ == "__main__":
    unittest.main()
