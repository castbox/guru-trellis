"""Completed-execution fixture binding, without native or grading claims."""
from __future__ import annotations

import builtins
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import eval_runner
from runtime.io import CommandError

SKILLS = Path(__file__).resolve().parents[1]


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n")


class Phase2CompletedBindingTests(unittest.TestCase):
    def fixture(self, root: Path, case: str, *, bound_task="current", visible_bound=True,
                business_staged="def contains(): return True\n"):
        root = root.resolve()
        skills = root / "selected-skills"
        package = skills / "packages/guru-check-task"
        case_root = root / "case"
        execution = case_root / "execution"
        workdir = execution / "workdir"
        owner = execution / "owner"
        model = execution / "model"
        projection = model / "public-package"
        public_file, business_file = "evals/files/public.json", "evals/files/interval.py"
        public = {"profile": "delivery_candidate_check", "mode": "workflow",
                  "task_ref": ".trellis/tasks/current", "delivery_key": {"delivery_id": "actual"}}
        write(package / public_file, {**public, "task_ref": ".trellis/tasks/template"})
        write(workdir / public_file, public)
        for path, text in ((package / business_file, "def contains(): return True\n"),
                           (workdir / business_file, business_staged),
                           (package / "scripts/invoke.sh", "unused saved wrapper\n"),
                           (projection / "scripts/invoke.sh", "unused saved wrapper\n")):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        write(model / "visible-public.json", public if visible_bound else {"profile": "old"})
        (model / "visible-interval.py").write_text(business_staged)
        facts = ".trellis/tasks/phase2-evidence/public-authoring-facts.json"
        bound_input = "docs/phase2-evidence/check-public-input.json"
        write(owner / facts, {"public_input_locator": bound_input})
        write(owner / bound_input, {**public, "task_ref": ".trellis/tasks/" + bound_task})

        # Use the original input locator reader. Only the pre-existing trace
        # subsystem is substituted, outside this test's fixture-binding boundary.
        adapters = skills / "adapters/eval"
        adapters.mkdir(parents=True)
        for name in ("fixture_io.py", "eval_constants.py"):
            shutil.copy2(SKILLS / "adapters/eval" / name, adapters / name)
        (adapters / "native_adapter.py").write_text(
            "def unwrap_native_output(adapter, stdout, output_path): return stdout\n"
            "def validate_native_trace(*args): return []\n")
        request = {"skill_id": "guru-check-task", "case_id": case,
            "native_execution_mode": "semantic_authoring", "adapter_id": "codex",
            "prompt": "Saved consumer fixture", "package_root": str(package),
            "workdir": str(workdir), "files": [public_file, business_file],
            "interface": {"public_invocation": {"wrapper": "scripts/invoke.sh"}}}
        native = {"skill_id": request["skill_id"], "case_id": case,
            "prompt": request["prompt"], "public_invocation": request["interface"]["public_invocation"],
            "native_execution_mode": "semantic_authoring",
            "files": ["visible-public.json", "visible-interval.py"]}
        native_path = execution / "native-request.json"
        write(native_path, native)
        trace = model / "native-trace.json"
        write(trace, {})
        context = model / "native-context.txt"
        context.write_text("Saved consumer test context.\n")
        protocol_path = execution / "private-control/native-protocol.json"
        protocol = {"native_request_path": str(native_path), "projection_root": str(projection),
            "wrapper_path": str(projection / "scripts/invoke.sh"), "model_root": str(model),
            "owner_repository": str(owner), "implementation_facts_locator": facts,
            "request_sha256": hashlib.sha256(native_path.read_bytes()).hexdigest(),
            "semantic_authoring": True, "trace_path": str(trace)}
        write(protocol_path, protocol)
        transcript_path = case_root / "adapter-transcript.json"
        transcript = {"adapter": "codex", "returncode": 0, "native_command": "codex",
            "protocol_path": str(protocol_path), "native_trace_path": str(trace),
            "context_path": str(context), "argv": ["codex"], "stdout": '{"exit_id":"passed"}\n',
            **{key: protocol[key] for key in ("native_request_path", "projection_root", "wrapper_path")},
            "model_input_audit": {"native_request": native, "argv": ["codex"],
                                  "context": context.read_text()}}
        write(transcript_path, transcript)
        write(case_root / "adapter-request.json", request)
        result = {"status": "executed", "actual_exit": "passed", "transcript_locator": str(transcript_path)}
        return skills, case_root, request, result, {"native_command": "codex"}

    def consume(self, values):
        original_import = builtins.__import__

        def selected_interpreter_only(name, *args, **kwargs):
            if name == "adapters" or name.startswith("adapters."):
                raise AssertionError("parent interpreter must not import adapter modules for this binding")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=selected_interpreter_only):
            eval_runner.completed_execution(*values)

    def test_actual_producer_binding_for_both_phase2_cases_uses_selected_skills(self):
        for case in ("native-owner-candidate-final", "native-owner-finding"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                self.consume(self.fixture(Path(temporary), case))

    def test_different_producer_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(CommandError, "saved native output/trace/receipts"):
                self.consume(self.fixture(Path(temporary), "native-owner-candidate-final", bound_task="other"))

    def test_other_changed_fixture_does_not_receive_the_public_input_exception(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(CommandError, "saved native output/trace/receipts"):
                self.consume(self.fixture(Path(temporary), "native-owner-candidate-final",
                    business_staged="def contains(): return False\n"))

    def test_model_visible_fixture_must_still_match_staged_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(CommandError, "saved model-visible fixture bytes mismatch"):
                self.consume(self.fixture(Path(temporary), "native-owner-candidate-final", visible_bound=False))


if __name__ == "__main__":
    unittest.main()
