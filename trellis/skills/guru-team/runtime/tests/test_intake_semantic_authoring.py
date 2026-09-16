from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter
from adapters.eval.intake_authoring import COMMANDS, FACTS_PATH, INTAKE_SKILLS, IntakeCommands, command_arguments, next_intake_owner, standard_intake
from jsonschema import Draft202012Validator

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / "packages" / INTAKE_SKILLS[-1]


def request_for(root: Path) -> dict:
    case = json.loads((PACKAGE / "evals/evals.json").read_text())["evals"][0]
    workdir = root / "execution/workdir"
    workdir.mkdir(parents=True)
    for relative in case["files"]:
        target = workdir / relative
        target.parent.mkdir(parents=True)
        shutil.copy2(PACKAGE / relative, target)
    interface = json.loads((PACKAGE / "interface.json").read_text())
    return {"schema_version": "1.0", "skill_id": INTAKE_SKILLS[-1],
            "case_id": case["id"], "prompt": case["prompt"], "files": case["files"],
            "native_execution_mode": "semantic_authoring", "native_authoring_flow": "standard_intake",
            "native_execution_adapter": "codex", "model_id": "gpt-5.6-sol",
            "package_root": str(PACKAGE), "workdir": str(workdir),
            "runtime_target": str(REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"),
            "interface": {"public_invocation": interface["public_contracts"]["invocation"]}}


class IntakeAuthoringTests(unittest.TestCase):
    def test_flow_parameter_belongs_only_to_isolated_helper(self):
        from adapters.eval import eval_constants, eval_support

        for source, isolated in ((eval_constants.TRACE_HELPER, False),
                                 (eval_support.qualification_trace_helper_source(), True)):
            with self.subTest(isolated=isolated):
                process = subprocess.run([sys.executable, "-B", "-c", source, "--help"],
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual("--flow" in process.stdout, isolated)
                self.assertEqual("{read,invoke,command}" in process.stdout, isolated)

    def test_installed_runner_terminal_schema_without_adapter_import(self):
        from adapters.eval.owner_staging import stage_owner_execution

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = request_for(root)
            _, target, _ = stage_owner_execution(request, root / "execution", Path(request["runtime_target"]))
            owner = target.parents[4]
            # Execute the installed runner in its real split module layout. Only the adapter
            # response is doubled to reproduce the captured blocked DTO, not native behavior.
            script = '''
import argparse, importlib.util, json, sys
from pathlib import Path
from unittest import mock
from runtime import eval_runner
assert importlib.util.find_spec("adapters") is None
root, run_root = Path(sys.argv[1]), Path(sys.argv[2])
skills = root / ".trellis/guru-team/skills"
observed = []
original_validate = eval_runner.validate_instance
def validate(value, schema, field):
    if field == "output.blocked": observed.append(str(schema))
    return original_validate(value, schema, field)
def adapter(_skills, _descriptor, request_path, host_environment=None):
    request = json.loads(request_path.read_text())
    trace = request_path.parent / "native-trace.json"
    trace.write_text(json.dumps({"terminal_skill_id": "guru-clarify-requirements"}))
    return {"corpus_sha256": request["corpus_sha256"], "capability_status": "executed",
            "public_stdout": '{"exit_id":"blocked"}', "public_stderr": "", "trace_events": trace_events,
            "transcript_locator": str(request_path.parent / "transcript.json"),
            "native_trace_locator": str(trace), "timing_ms": 0}
args = argparse.Namespace(adapter="codex", case="standard-intake-authoring-scope-conflict",
    comparison_package=None, current_package=None, human_feedback=None, mode="installed",
    run_root=str(run_root), semantic_grading=None, skill="guru-review-change-request")
for index, trace_events in enumerate(([],
        ["public_invocation", "evals_not_loaded", "private_runtime_not_read"])):
    args.run_root = str(run_root / str(index))
    with mock.patch.object(eval_runner, "call_adapter", side_effect=adapter), mock.patch.object(eval_runner, "validate_instance", side_effect=validate):
        result = eval_runner.run(root, skills, args)
    case = result["cases"][0]
    assert case["actual_exit"] == "blocked", result
    assert case["status"] == "evaluation_failed", result
    assert case["semantic_results"] and not any(row["passed"] for row in case["semantic_results"]), result
assert all(row["passed"] for row in case["deterministic_results"]), result
assert observed == [str(skills / "packages/guru-clarify-requirements/schemas/public-blocked-output.schema.json")] * 2, observed
assert Path(result["evidence_path"]).is_file()
print(json.dumps({"status": case["status"], "terminal_schema": observed[0]}))
'''
            process = subprocess.run([sys.executable, "-B", "-c", script, str(owner), str(root / "run")],
                cwd=owner, env={**os.environ, "PYTHONPATH": str(owner / ".trellis/guru-team"), "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True, text=True, timeout=60)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertEqual(json.loads(process.stdout)["status"], "evaluation_failed")

    def test_production_json_and_root_flags_preserve_original_argv(self):
        for skill, commands in COMMANDS.items():
            for command in commands:
                arguments = ["--query-json", '{"terms":["greeting"]}'] if command.startswith("preview-") else ["--invocation", "-"]
                if skill == INTAKE_SKILLS[2] and command != "invoke":
                    arguments = ["--input", "-"]
                    if command.startswith("record-"):
                        arguments = ["--mode", "workflow", *arguments]
                flags = ["--json", *arguments]
                if skill != INTAKE_SKILLS[0] and not (skill == INTAKE_SKILLS[2] and command == "invoke"):
                    flags = ["--root", ".", *flags]
                with self.subTest(skill=skill, command=command):
                    original = list(flags)
                    command_arguments(skill, command, flags)
                    self.assertEqual(flags, original)
        with tempfile.TemporaryDirectory() as temporary:
            dispatcher = IntakeCommands(Path(temporary), {}, Path(temporary) / "receipts.json")
            dispatcher.owner_index = 2
            arguments = ["--mode", "workflow", "--input", "-", "--json", "--root", "."]
            with mock.patch("adapters.eval.intake_authoring.subprocess.run", return_value=subprocess.CompletedProcess([], 0, '{}', '')) as run:
                dispatcher.forward({"skill_id": INTAKE_SKILLS[2], "command": "record-requirements-clarification",
                                    "arguments": arguments, "stdin": "{}"})
            self.assertEqual(run.call_args.args[0][1:], arguments)
            self.assertEqual(dispatcher.receipts[0]["request"]["arguments"], arguments)

    def test_closed_flow_declaration(self):
        corpus = json.loads((PACKAGE / "evals/evals.json").read_text())
        validator = Draft202012Validator(json.loads((SKILLS / "schemas/skill-evals.schema.json").read_text()))
        validator.validate(corpus)
        for mode in (None, "post_owner"):
            changed = copy.deepcopy(corpus)
            case = changed["evals"][0]
            if mode is None:
                case.pop("native_execution_mode")
            else:
                case["native_execution_mode"] = mode
            case.pop("native_execution_adapter")
            case.pop("model_id")
            self.assertTrue(list(validator.iter_errors(changed)))
        with self.assertRaises(ValueError):
            standard_intake({"native_authoring_flow": "standard_intake", "native_execution_mode": "post_owner"})

    def test_projection_and_original_sync_with_no_prebuilt_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            request = request_for(Path(temporary))
            built = native_adapter.build_context(request, "codex")
            context, _, _, _, protocol_path, native_request, _, _, thread, stop, _ = built
            protocol = json.loads(protocol_path.read_text())
            try:
                owner = Path(protocol["owner_repository"])
                self.assertFalse((owner / ".trellis/.runtime").exists())
                facts = json.loads((owner / FACTS_PATH).read_text())
                self.assertNotIn("owner_result", facts)
                model_request = json.loads(native_request.read_text())
                self.assertNotIn("case_id", model_request)
                self.assertNotIn("expected_exit", model_request)
                self.assertNotIn("external owner", context)
                self.assertNotIn("ARCHITECTURE", context)
                self.assertNotIn("semantic-result.schema.json", context)
                self.assertIn("--stdin reads the actual process stdin", context)
                self.assertIn("nonzero command exit is an invocation error", context)
                self.assertIn("call the same command again", context)
                self.assertIn("Only a successful invoke command's declared typed output can be terminal", context)
                root = Path(protocol["projection_root"])
                for skill in INTAKE_SKILLS:
                    projected = root if skill == INTAKE_SKILLS[-1] else root / "flow-packages" / skill
                    for name in ("SKILL.md", "references/contract.md", "interface.json"):
                        self.assertEqual((projected / name).read_bytes(), (SKILLS / "packages" / skill / name).read_bytes())
                        self.assertIn(str(projected / name), context)
                    for schema in (projected / "schemas").glob("*.json"):
                        self.assertIn(schema.relative_to(projected).as_posix(), context)
                self.assertFalse(list(root.rglob("evals")))
                helper = Path(protocol["helper_path"])
                compile(helper.read_text(), str(helper), "exec")
                # Execute the original installed Sync against the local fixture remote, not an owner recipe.
                binary = Path(temporary) / "execution/owner-bin"
                dispatcher = IntakeCommands(owner, {"PATH": str(binary) + os.pathsep + os.environ["PATH"]}, Path(temporary) / "sync-receipts.json")
                result = dispatcher.forward({"skill_id": INTAKE_SKILLS[0], "command": "invoke", "arguments": ["--invocation", "-"],
                    "stdin": json.dumps({"schema_version": "1.0", "public_input": {"source_exit": "start", "mode": "workflow", "route": "repo_change", "repo_root": ".", "base_branch": "main"}})})
                self.assertEqual(result["returncode"], 0, result)
                if json.loads(result["stdout"])["exit_id"] != "synced":
                    wrapper = owner / ".trellis/guru-team/skills/packages/guru-sync-base/scripts/sync-base.sh"
                    environment = {**os.environ, **dispatcher.environment}
                    resolved = subprocess.run([str(wrapper), "--root", ".", "--mode", "workflow", "--base", "main", "--resolve-only"], cwd=owner, env=environment, text=True, capture_output=True)
                    value = json.loads(resolved.stdout)
                    executed = subprocess.run([str(wrapper), "--root", ".", "--mode", "workflow", "--base", "main", "--execute", "--expected-resolution-sha256", value["resolution_sha256"]], cwd=owner, env=environment, text=True, capture_output=True)
                    self.fail(f"Sync failed: {executed.stdout} {executed.stderr}")
                self.assertEqual(json.loads(result["stdout"])["exit_id"], "synced", result)
                self.assertEqual(dispatcher.owner_index, 1)
                helper_args = [str(helper), "--trace", protocol["trace_path"],
                    "--request-sha256", protocol["request_sha256"], "--projection-root", protocol["projection_root"],
                    "--repository-root", protocol["repository_projection_root"], "--sandbox-root", protocol["model_root"],
                    "--request-fifo", protocol["request_fifo"], "--response-fifo", protocol["response_fifo"],
                    "--skill-sha256", protocol["skill_sha256"], "--wrapper-sha256", protocol["wrapper_sha256"],
                    "--flow", "standard_intake"]
                for name in ("SKILL.md", "references/contract.md", "interface.json"):
                    read = subprocess.run([*helper_args, "read", "--kind", "skill_contract", "--path",
                        str(root / "flow-packages" / INTAKE_SKILLS[0] / name)], text=True, capture_output=True, timeout=10)
                    self.assertEqual(read.returncode, 0, read.stderr)
                for stdin, arguments in (("{", ["--invocation", "-"]), ("{}", ["--input", "-"])):
                    failed = subprocess.run([*helper_args, "command", "--skill-id", INTAKE_SKILLS[0],
                        "--command", "invoke", "--stdin", "--", *arguments],
                        input=stdin, text=True, capture_output=True, timeout=10)
                    self.assertEqual(failed.returncode, 2, failed)
                    self.assertTrue(thread.is_alive())
                    receipts = json.loads(Path(protocol["intake_receipts_path"]).read_text())
                    self.assertEqual(receipts[-1]["request"]["stdin"], stdin)
                    self.assertEqual(receipts[-1]["response"]["stderr"], failed.stderr)
                # Exercise the context's shell transport example against the real FIFO and installed Sync.
                transport = context.split("```bash\n", 1)[1].split("\n```", 1)[0]
                self.assertIn("<<'GURU_COMMAND_JSON'", transport)
                transport = (transport.replace("<skill>", INTAKE_SKILLS[0]).replace("<command>", "invoke")
                    .replace("<original stdin arguments>", "--invocation -")
                    .replace("<current-command-input-json>", json.dumps({"schema_version": "1.0",
                        "public_input": {"mode": "workflow", "repo_root": ".", "base_branch": "main"}})))
                forwarded = subprocess.run(["bash", "-c", transport],
                    text=True, capture_output=True, timeout=30)
                self.assertEqual(forwarded.returncode, 0, forwarded.stderr)
                self.assertEqual(json.loads(forwarded.stdout)["exit_id"], "synced")
                trace = json.loads(Path(protocol["trace_path"]).read_text())
                self.assertEqual(trace["terminal_skill_id"], INTAKE_SKILLS[0])
                self.assertEqual(trace["events"][-1]["kind"], "command")
                Draft202012Validator(json.loads((SKILLS / "schemas/skill-eval-native-trace.schema.json").read_text())).validate(trace)
                receipts = json.loads(Path(protocol["intake_receipts_path"]).read_text())
                self.assertEqual(receipts[-1]["response"]["stdout"], forwarded.stdout)
                with self.assertRaisesRegex(ValueError, "next owner"):
                    native_adapter.validate_native_trace(Path(protocol["trace_path"]), protocol["request_sha256"],
                        request, Path(protocol["wrapper_path"]), forwarded.stdout, protocol_path)
                preview = subprocess.run([*helper_args, "command", "--skill-id", INTAKE_SKILLS[1],
                    "--command", "preview-change-context-history", "--stdin", "--", "--root", ".", "--json", "--query-json", '{"terms":["greeting"]}'],
                    input="", text=True, capture_output=True, timeout=30)
                self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
                receipts = json.loads(Path(protocol["intake_receipts_path"]).read_text())
                self.assertEqual(len(receipts), 4)
                self.assertEqual(receipts[-1]["response"]["stdout"], preview.stdout)
            finally:
                stop.set()
                thread.join(timeout=2)
                shutil.rmtree(protocol["model_root"])

    def test_fifo_projection_correction_and_single_skill_boundary(self):
        client = (
            "import json,sys\n"
            "with open(sys.argv[1], 'w') as handle: handle.write(sys.argv[3])\n"
            "with open(sys.argv[2]) as handle: print(handle.read())\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / ".trellis/guru-team/skills/packages" / INTAKE_SKILLS[2]
            (package / "scripts").mkdir(parents=True)
            wrapper = package / "scripts/invoke.sh"
            # Transport-only wrapper double; the other test executes real installed commands.
            wrapper.write_text(f"#!{sys.executable}\nprint('{{\"exit_id\":\"blocked\"}}')\n")
            wrapper.chmod(0o755)
            shutil.copy2(SKILLS / "packages" / INTAKE_SKILLS[2] / "interface.json", package / "interface.json")
            dispatcher = IntakeCommands(root, {}, root / "receipts.json")
            dispatcher.owner_index = 2
            dispatcher.completed = list(COMMANDS[INTAKE_SKILLS[2]][:2])
            dispatcher.recorded = {"typed_exit": "blocked"}
            transition = {"target_locator": "issue", "mode": "workflow"}
            dispatcher.outputs[INTAKE_SKILLS[1]] = {"exit_id": "context_ready", "handoff_continuation_id": "current",
                                                   "transition": transition, "duplicate_snapshot": {}}
            envelope = {"transition": transition, "owner_result": dispatcher.recorded,
                "public_input": {"source_exit": "context_ready", "mode": "workflow", "continuation_id": "current",
                                 "target_locator": "issue", "duplicate_snapshot": {}}}
            request_fifo, response_fifo = root / "request", root / "response"
            stop = threading.Event()
            thread = native_adapter.start_qualification_runtime_boundary(request_fifo, response_fifo, stop, root, package, {}, {}, dispatcher)
            try:
                for wrong in (True, False):
                    payload = {"skill_id": INTAKE_SKILLS[2], "command": "invoke", "arguments": ["--invocation", "-"],
                               "stdin": json.dumps({**envelope, "transition": {} if wrong else transition})}
                    call = subprocess.run([sys.executable, "-B", "-c", client, str(request_fifo), str(response_fifo), json.dumps(payload)],
                                          capture_output=True, text=True, timeout=10)
                    self.assertEqual(call.returncode, 0, call.stderr)
                    response = json.loads(call.stdout)
                    self.assertEqual(response["returncode"], 2 if wrong else 0)
                    self.assertTrue(thread.is_alive())
                self.assertEqual(len(dispatcher.receipts), 2)
                self.assertIn("transition", dispatcher.receipts[0]["response"]["stderr"])
                self.assertTrue(dispatcher.terminal)
            finally:
                stop.set()
                thread.join(timeout=2)
            stop = threading.Event()
            thread = native_adapter.start_qualification_runtime_boundary(request_fifo, response_fifo, stop, root, package, {}, {})
            try:
                call = subprocess.run([sys.executable, "-B", "-c", client, str(request_fifo), str(response_fifo), '{}'],
                                      capture_output=True, text=True, timeout=10)
                self.assertEqual(json.loads(call.stdout)["returncode"], 2)
                thread.join(timeout=2)
                self.assertFalse(thread.is_alive())
            finally:
                stop.set()
                thread.join(timeout=2)

    def test_shared_helper_preserves_phase2_four_invocations_and_error_close(self):
        from adapters.eval import eval_support, phase2_authoring

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            repository = root / "repository"
            projection = root / "public-package"
            projection.mkdir()
            package = repository / ".trellis/guru-team/skills/packages" / phase2_authoring.SKILL
            (package / "scripts").mkdir(parents=True)
            wrapper = package / "scripts/invoke.sh"
            wrapper.write_text("#!/bin/sh\nexit 0\n")
            wrapper.chmod(0o755)
            helper = root / "helper.py"
            helper.write_text(eval_support.qualification_trace_helper_source())
            helper.chmod(0o755)
            request_fifo, response_fifo = root / "request", root / "response"
            trace = root / "trace.json"
            arguments = [str(helper), "--trace", str(trace), "--request-sha256", "0" * 64,
                         "--projection-root", str(projection), "--repository-root", str(repository),
                         "--sandbox-root", str(root), "--request-fifo", str(request_fifo),
                         "--response-fifo", str(response_fifo), "--skill-sha256", "1" * 64,
                         "--wrapper-sha256", "2" * 64, "invoke", "--stdin"]
            envelope = {"public_input": {"profile": "initial_check"}, "owner_result": {}}
            for failed in (False, True):
                with self.subTest(failed=failed):
                    trace.unlink(missing_ok=True)
                    stop = threading.Event()
                    # Only command transport is doubled; the helper, FIFO, receipts and
                    # Phase 2 prerequisite/termination rules execute their real code.
                    outcome = subprocess.CompletedProcess([], 2 if failed else 0,
                        "" if failed else '{"exit_id":"passed"}', "schema_mismatch" if failed else "")
                    with mock.patch.object(native_adapter.subprocess, "run", return_value=outcome) as invoke, \
                            mock.patch.object(phase2_authoring, "execute", return_value=outcome) as execute:
                        thread = native_adapter.start_qualification_runtime_boundary(
                            request_fifo, response_fifo, stop, repository, package, {}, {})
                        try:
                            calls = [["--upstream-architecture"], ["--qualifier", "normal-scenario"],
                                     ["--qualifier", "solution-mechanism"], []]
                            for index, flags in enumerate(calls[:1] if failed else calls):
                                process = subprocess.Popen([*arguments, *flags], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                try:
                                    stdout, stderr = process.communicate(json.dumps(envelope), timeout=10)
                                except subprocess.TimeoutExpired:
                                    process.kill()
                                    process.communicate()
                                    self.fail("shared helper FIFO did not complete")
                                self.assertEqual(process.returncode, outcome.returncode, stderr)
                                self.assertEqual(stdout, outcome.stdout)
                                if not failed and index < 3:
                                    self.assertTrue(thread.is_alive())
                            thread.join(timeout=2)
                            self.assertFalse(thread.is_alive())
                            self.assertEqual(invoke.call_count, 1 if failed else 3)
                            self.assertEqual(execute.call_count, 0 if failed else 1)
                            if not failed:
                                self.assertEqual(execute.call_args.args[2], envelope)
                        finally:
                            stop.set()
                            thread.join(timeout=2)
                    receipt = json.loads(trace.read_text())
                    expected = [str(repository / ".trellis/guru-team/skills/packages" / skill / "scripts/invoke.sh")
                                for skill in (phase2_authoring.ARCHITECTURE, *phase2_authoring.QUALIFIERS)]
                    expected.append(str(projection / "scripts/invoke.sh"))
                    self.assertEqual([event["wrapper_path"] for event in receipt["events"]], expected[:1] if failed else expected)
                    self.assertNotIn("terminal_skill_id", receipt)

    def test_recorder_stdout_and_projection_are_required(self):
        with tempfile.TemporaryDirectory() as temporary:
            dispatcher = IntakeCommands(Path(temporary), {}, Path(temporary) / "receipts.json")
            dispatcher.owner_index = 2
            dispatcher.completed = [COMMANDS[INTAKE_SKILLS[2]][0]]
            dispatcher.recorded = {"recorded": "actual"}
            with self.assertRaisesRegex(ValueError, "recorder stdout"):
                dispatcher.forward({"skill_id": INTAKE_SKILLS[2], "command": COMMANDS[INTAKE_SKILLS[2]][1],
                                    "arguments": ["--input", "-"], "stdin": "{}"})
            dispatcher.outputs[INTAKE_SKILLS[1]] = {"transition": {"target_locator": "issue"}, "duplicate_snapshot": {"facts": "actual"}}
            with self.assertRaisesRegex(ValueError, "transition"):
                dispatcher.check_projection(INTAKE_SKILLS[2], {"transition": {}, "public_input": {}})

    def test_declared_workflow_routers_continue_only_current_intake(self):
        clarity = json.loads((SKILLS / "packages" / INTAKE_SKILLS[2] / "interface.json").read_text())
        wording = json.loads((SKILLS / "packages" / INTAKE_SKILLS[3] / "interface.json").read_text())
        self.assertEqual(next_intake_owner(INTAKE_SKILLS[2], {"exit_id": "clear", "resume_target": INTAKE_SKILLS[3]}, clarity), INTAKE_SKILLS[3])
        self.assertIsNone(next_intake_owner(INTAKE_SKILLS[2], {"exit_id": "blocked"}, clarity))
        self.assertIsNone(next_intake_owner(INTAKE_SKILLS[2], {"exit_id": "clear", "resume_target": "guru-standalone-caller"}, clarity))
        self.assertEqual(next_intake_owner(INTAKE_SKILLS[3], {"exit_id": "pass", "profile": "change_request"}, wording), INTAKE_SKILLS[4])
        self.assertIsNone(next_intake_owner(INTAKE_SKILLS[3], {"exit_id": "pass", "profile": "explicit_paths"}, wording))

    def test_failed_record_can_be_corrected_without_skipping_checker(self):
        with tempfile.TemporaryDirectory() as temporary:
            dispatcher = IntakeCommands(Path(temporary), {}, Path(temporary) / "receipts.json")
            dispatcher.owner_index = 2
            call = {"skill_id": INTAKE_SKILLS[2], "command": COMMANDS[INTAKE_SKILLS[2]][0],
                    "arguments": ["--mode", "workflow", "--input", "-"], "stdin": "{}"}
            responses = [subprocess.CompletedProcess([], 2, '{"code":"schema_mismatch"}', ''),
                         subprocess.CompletedProcess([], 0, '{"recorded":"complete"}', '')]
            with mock.patch("adapters.eval.intake_authoring.subprocess.run", side_effect=responses):
                self.assertEqual(dispatcher.forward(call)["returncode"], 2)
                self.assertEqual(dispatcher.completed, [])
                self.assertEqual(dispatcher.forward(call)["returncode"], 0)
                self.assertEqual(dispatcher.recorded, {"recorded": "complete"})
                self.assertEqual(len(dispatcher.receipts), 2)
                with self.assertRaisesRegex(ValueError, "order"):
                    dispatcher.forward({**call, "command": "invoke", "arguments": ["--invocation", "-"]})

    def test_actual_clarification_blocker_stops_downstream_commands(self):
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            package = repository / ".trellis/guru-team/skills/packages" / INTAKE_SKILLS[2]
            (package / "scripts").mkdir(parents=True)
            shutil.copy2(SKILLS / "packages" / INTAKE_SKILLS[2] / "interface.json", package / "interface.json")
            dispatcher = IntakeCommands(repository, {}, repository / "receipts.json")
            dispatcher.owner_index = 2
            dispatcher.completed = list(COMMANDS[INTAKE_SKILLS[2]][:2])
            dispatcher.recorded = {"typed_exit": "blocked"}
            transition = {"target_locator": "issue", "mode": "workflow"}
            dispatcher.outputs[INTAKE_SKILLS[1]] = {"exit_id": "context_ready", "handoff_continuation_id": "current",
                                                   "transition": transition, "duplicate_snapshot": {}}
            envelope = {"transition": transition, "owner_result": dispatcher.recorded,
                        "public_input": {"target_locator": "issue", "mode": "workflow", "continuation_id": "current",
                                         "source_exit": "context_ready", "duplicate_snapshot": {}}}
            # This is a transport unit double, not semantic or native acceptance evidence.
            with mock.patch("adapters.eval.intake_authoring.subprocess.run", return_value=subprocess.CompletedProcess([], 0, '{"exit_id":"blocked"}\n', '')) as run:
                result = dispatcher.forward({"skill_id": INTAKE_SKILLS[2], "command": "invoke", "arguments": ["--invocation", "-"], "stdin": json.dumps(envelope)})
                self.assertEqual(json.loads(result["stdout"]), {"exit_id": "blocked"})
                self.assertTrue(dispatcher.terminal)
                with self.assertRaisesRegex(ValueError, "terminal"):
                    dispatcher.forward({"skill_id": INTAKE_SKILLS[3], "command": "record-contract-wording-review", "arguments": ["--invocation", "-", "--scan-only"], "stdin": "{}"})
                self.assertEqual(run.call_count, 1)

    def test_real_clarification_invoke_omission_can_be_rerecorded(self):
        skill = INTAKE_SKILLS[2]
        package = SKILLS / "packages" / skill
        public = json.loads((package / "examples/public-initial-change-request-input-2.0.json").read_text())
        public["source_exit"] = "context_ready"
        snapshot = public["duplicate_snapshot"]
        authoring = json.loads((package / "examples/requirements-clarification.json").read_text())
        authoring.pop("content_identity")
        authoring["review_target"].pop("facts_sha256")
        authoring["review_target"].update(kind="issue", issue_number=145, url=public["target_locator"],
                                          state="open", updated_at=snapshot["checked_at"])
        authoring["invocation_context"]["kind"] = "initial_issue"
        disposition = authoring.pop("target_disposition")
        disposition.pop("disposition_digest")
        disposition.update(disposition="keep_current_open_issue", duplicate_query=snapshot["query"],
                           duplicate_checked_at=snapshot["checked_at"], duplicate_facts_sha256=snapshot["facts_sha256"])
        authoring.update(mode="workflow", target_disposition=None, typed_exit="blocked",
                         consumer={"kind": "stop", "id": "requirements-clarification-blocked"},
                         error={"codes": ["scope_conflict"], "summary": "Delivery scope needs a product choice."})
        authoring["open_questions"] = ["delivery_scope"]
        authoring["ai_review_gate"].update(status="blocked", summary="Delivery scope needs a product choice.")
        for action in authoring["source_actions"]:
            action.pop("payload_sha256")
            action.pop("action_digest")
        transition = {"mode": "workflow", "stage": "context_current",
                      "target_locator": public["target_locator"], "continuation_id": public["continuation_id"],
                      "authority_content_sha256": snapshot["authority_content_sha256"]}
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            projected = repository / ".trellis/guru-team/skills/packages" / skill
            projected.mkdir(parents=True)
            shutil.copy2(package / "interface.json", projected / "interface.json")
            dispatcher = IntakeCommands(repository, {"PYTHONDONTWRITEBYTECODE": "1"}, repository / "receipts.json")
            dispatcher.owner_index = 2
            dispatcher.outputs[INTAKE_SKILLS[1]] = {"exit_id": "context_ready", "transition": transition,
                "handoff_continuation_id": public["continuation_id"], "duplicate_snapshot": snapshot}
            actual_run = subprocess.run

            def canonical_command(argv, **kwargs):
                # Relocate transport only: run the real canonical production
                # wrappers, recorder, checker and invoke without installing.
                return actual_run([str(package / "scripts" / Path(argv[0]).name), *argv[1:]], **kwargs)

            def call(command, value):
                arguments = ["--invocation", "-"] if command == "invoke" else ["--input", "-"]
                if command.startswith("record-"):
                    arguments = ["--mode", "workflow", *arguments]
                return dispatcher.forward({"skill_id": skill, "command": command, "arguments": arguments,
                                           "stdin": json.dumps(value)})

            def success(command, value):
                result = call(command, value)
                self.assertEqual(result["returncode"], 0, result)
                return json.loads(result["stdout"])

            with mock.patch("adapters.eval.intake_authoring.subprocess.run", side_effect=canonical_command):
                old = success(COMMANDS[skill][0], authoring)
                success(COMMANDS[skill][1], old)
                envelope = {"schema_version": "1.0", "public_input": public, "transition": transition,
                            "owner_context": {}, "owner_result": old}
                failure = call("invoke", envelope)
                self.assertEqual(failure["returncode"], 3, failure)
                self.assertEqual(json.loads(failure["stdout"])["field_path"], "public_input.duplicate_snapshot")
                failed_receipt = copy.deepcopy(dispatcher.receipts[-1])
                self.assertFalse(dispatcher.terminal)
                self.assertNotIn(skill, dispatcher.outputs)
                with self.assertRaisesRegex(ValueError, "owner order"):
                    dispatcher.forward({"skill_id": INTAKE_SKILLS[3], "command": "record-contract-wording-review",
                                        "arguments": ["--invocation", "-"], "stdin": "{}"})
                authoring["target_disposition"] = disposition
                fresh = success(COMMANDS[skill][0], authoring)
                self.assertIsNone(dispatcher.checked)
                self.assertNotEqual(fresh["content_identity"], old["content_identity"])
                with self.assertRaisesRegex(ValueError, "recorder stdout"):
                    call(COMMANDS[skill][1], old)
                success(COMMANDS[skill][1], fresh)
                with self.assertRaisesRegex(ValueError, "recorder stdout"):
                    call("invoke", envelope)
                envelope["owner_result"] = fresh
                self.assertEqual(success("invoke", envelope), {"exit_id": "blocked"})
                self.assertTrue(dispatcher.terminal)
                with self.assertRaisesRegex(ValueError, "terminal"):
                    call(COMMANDS[skill][0], authoring)
            self.assertEqual(dispatcher.receipts[2], failed_receipt)
            self.assertEqual([row["response"]["returncode"] for row in dispatcher.receipts], [0, 0, 3, 0, 0, 0])
            self.assertEqual(json.loads(dispatcher.receipts_path.read_text()), dispatcher.receipts)

    def test_failed_check_reentry_keeps_scan_and_requires_fresh_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            dispatcher = IntakeCommands(Path(temporary), {}, Path(temporary) / "receipts.json")
            skill = INTAKE_SKILLS[3]
            dispatcher.owner_index = 3
            dispatcher.completed = ["scan", COMMANDS[skill][0]]
            dispatcher.recorded = {"owner": "old"}
            dispatcher.checked = {"validation_receipt": {"version": "old"}}
            record = {"skill_id": skill, "command": COMMANDS[skill][0],
                      "arguments": ["--invocation", "-"], "stdin": '{"owner_result":{"owner":"fresh"}}'}
            check = {**record, "command": COMMANDS[skill][1], "stdin": '{"owner_result":{"owner":"old"}}'}
            with self.assertRaisesRegex(ValueError, "order"):
                dispatcher.forward(record)
            replies = [subprocess.CompletedProcess([], 3, '{"code":"stale_identity"}', ''),
                       subprocess.CompletedProcess([], 0, '{"owner":"fresh"}', ''),
                       subprocess.CompletedProcess([], 0, '{"validation_receipt":{"version":"fresh"}}', '')]
            with mock.patch("adapters.eval.intake_authoring.subprocess.run", side_effect=replies) as run:
                self.assertEqual(dispatcher.forward(check)["returncode"], 3)
                self.assertEqual(dispatcher.forward(record)["returncode"], 0)
                self.assertEqual(dispatcher.completed, ["scan", COMMANDS[skill][0]])
                self.assertIsNone(dispatcher.checked)
                with self.assertRaisesRegex(ValueError, "order"):
                    dispatcher.forward({**record, "command": "invoke"})
                with self.assertRaisesRegex(ValueError, "recorder stdout"):
                    dispatcher.forward(check)
                self.assertEqual(dispatcher.forward({**record, "command": COMMANDS[skill][1]})["returncode"], 0)
                transition = {"mode": "workflow", "target_locator": "issue"}
                dispatcher.outputs[INTAKE_SKILLS[2]] = {"exit_id": "clear", "continuation_id": "current", "transition": transition}
                envelope = {"owner_result": {"owner": "fresh"}, "transition": transition,
                            "public_input": {"source_exit": "clear", "mode": "workflow", "target_locator": "issue", "continuation_id": "current"},
                            "validation_receipt": {"version": "old"}}
                with self.assertRaisesRegex(ValueError, "actual checker receipt"):
                    dispatcher.forward({**record, "command": "invoke", "stdin": json.dumps(envelope)})
                self.assertEqual(run.call_count, 3)
            self.assertEqual([row["response"]["returncode"] for row in dispatcher.receipts], [3, 0, 0])


if __name__ == "__main__":
    unittest.main()
